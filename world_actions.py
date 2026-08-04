"""
World Actions — integration glue for the living world
======================================================

This module contains **no new gameplay systems**. It is a thin orchestration
layer that connects capabilities that already exist in the project into the
player's hands:

* Travel      -> ``travel_manager.travel_to_region`` (+ region graph, events)
* Settlements -> ``settlement_manager`` + ``shop`` + ``dialogue_manager`` +
                 ``npc_manager`` + ``quest_manager``
* Explore     -> player-chosen actions that reuse the existing encounter,
                 quest and world-event systems
* World map   -> ``world_map`` (already dynamic / discovery-filtered)

Standard overworld encounters route through the canonical tactical engine via
``combat_bridge.start_encounter`` (R-01 Technical Canon); the legacy
``combat.quick_encounter`` runtime is a compatibility layer and is no longer the
entry point for exploration combat.
"""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from world_state import world_state


# ---------------------------------------------------------------------------
# small terminal helpers
# ---------------------------------------------------------------------------
def _current_region() -> str:
    return world_state["regions"]["current_region"]


def _ask(prompt: str = "\nChoose: ") -> str:
    try:
        return input(prompt).strip()
    except EOFError:
        return ""


def _menu(title: str, options: List[Tuple[str, Callable]],
          back_label: str = "Back") -> None:
    """Render a numbered menu of (label, callable) once and dispatch."""
    print(f"\n=== {title} ===")
    for i, (label, _) in enumerate(options, start=1):
        print(f"{i}. {label}")
    print(f"{len(options) + 1}. {back_label}")
    choice = _ask()
    if not choice.isdigit():
        print("\nInvalid choice.")
        return
    idx = int(choice) - 1
    if 0 <= idx < len(options):
        options[idx][1]()
    # last option / anything else = back


def _tick() -> None:
    """Advance the world simulation using the existing game tick."""
    from game_loop import process_game_tick
    process_game_tick()


# ---------------------------------------------------------------------------
# 1 + 4 · Travel  (reuses travel_manager + region graph + world map)
# ---------------------------------------------------------------------------
def travel_menu() -> None:
    from region_manager import REGIONS, get_neighboring_regions
    from travel_manager import travel_to_region

    region = _current_region()
    neighbors = get_neighboring_regions(region)

    print("\n=== TRAVEL ===")
    here = REGIONS.get(region, {})
    print(f"Current region: {here.get('display_name', region)}")

    if not neighbors:
        print("\nThere are no roads leading onward from here.")
        return

    print("\nRoads lead to:")
    reachable: List[str] = []
    for name in neighbors:
        data = REGIONS.get(name)
        if not data:
            continue
        reachable.append(name)
        seen = "" if data.get("discovered") else "  (unexplored)"
        print(f"{len(reachable)}. {data.get('display_name', name)} "
              f"— danger {data.get('danger', '?')}, "
              f"{data.get('travel_difficulty', '?')} days min{seen}")
    print(f"{len(reachable) + 1}. View world map")
    print(f"{len(reachable) + 2}. Stay here")

    choice = _ask()
    if not choice.isdigit():
        print("\nYou decide to stay.")
        return
    n = int(choice)
    if n == len(reachable) + 1:
        world_map_menu()
        return
    if not (1 <= n <= len(reachable)):
        print("\nYou decide to stay.")
        return

    destination = reachable[n - 1]
    travel_to_region(destination)     # runs travel days + road events + arrival
    _tick()                            # advance factions/economy/director on arrival

    # Offer to step straight into a settlement of the new region.
    from region_manager import get_region_settlements
    if get_region_settlements(_current_region()):
        print("\nSettlements lie ahead — choose 'Settlements' from the menu "
              "to enter one.")


# ---------------------------------------------------------------------------
# 2 + 7 + 8 · Settlement entry (services, merchants, NPCs, faction, quests)
# ---------------------------------------------------------------------------
def _npcs_in_region(region: str) -> List[Tuple[str, dict]]:
    from npc_manager import NPCS
    return [(name, data) for name, data in NPCS.items()
            if data.get("region") == region]


def _talk_to_locals(region: str) -> None:
    from dialogue_manager import start_dialogue
    locals_here = _npcs_in_region(region)
    if not locals_here:
        print("\nNo one here is willing to talk right now.")
        return
    print("\n=== LOCALS ===")
    for i, (name, data) in enumerate(locals_here, start=1):
        print(f"{i}. {data.get('name', name)} "
              f"({data.get('faction', 'unaligned')})")
    print(f"{len(locals_here) + 1}. Leave")
    choice = _ask()
    if not choice.isdigit():
        return
    idx = int(choice) - 1
    if 0 <= idx < len(locals_here):
        name, data = locals_here[idx]
        try:
            start_dialogue(name, faction=data.get("faction"))
        except Exception as exc:                          # boundary guard
            print(f"\n{data.get('name', name)} has nothing to say. ({exc})")


def _quest_board(settlement_name: str) -> None:
    from quest_manager import generate_quest_board, show_active_quests
    try:
        generate_quest_board(settlement_name)
    except Exception as exc:                              # boundary guard
        print(f"\nThe quest board is empty. ({exc})")
    show_active_quests()


def _inn_rest() -> None:
    print("\nYou take a room for the night. The party recovers.")
    _tick()


def _service_actions(settlement_name: str, services: List[str], region: str
                     ) -> List[Tuple[str, Callable]]:
    from shop import shop, black_market
    from settlement_manager import get_random_rumor

    actions: List[Tuple[str, Callable]] = []
    added = set()
    for service in services:
        if service in ("market", "blacksmith") and "shop" not in added:
            actions.append(("Visit the market / blacksmith", shop))
            added.add("shop")
        elif service == "fence" and "fence" not in added:
            actions.append(("Seek out the fence (black market)", black_market))
            added.add("fence")
        elif service in ("tavern",) and "tavern" not in added:
            actions.append(("Drink at the tavern (hear a rumor)",
                            lambda s=settlement_name: get_random_rumor(s)))
            added.add("tavern")
        elif service == "inn" and "inn" not in added:
            actions.append(("Rest at the inn", _inn_rest))
            added.add("inn")
        elif service in ("healer", "herbalist") and "healer" not in added:
            actions.append(("Visit the healer / herbalist",
                            lambda s=settlement_name: get_random_rumor(s)))
            added.add("healer")
    return actions


def enter_settlement_scene(settlement_name: str) -> None:
    from settlement_manager import SETTLEMENTS, show_settlement

    region = _current_region()
    data = SETTLEMENTS.get(settlement_name)

    print(f"\n=== ENTERING {settlement_name.replace('_', ' ').upper()} ===")
    if data:
        show_settlement(settlement_name)
        services = list(data.get("services", []))
        faction = data.get("faction", "unaligned")
    else:
        print("\nA modest settlement with little to offer travellers.")
        services = []
        faction = "unaligned"

    print(f"\nFaction presence: {faction}")
    present = {d.get("faction") for _, d in _npcs_in_region(region)
               if d.get("faction")}
    if present:
        print("Notable figures aligned with: " + ", ".join(sorted(present)))

    while True:
        actions = _service_actions(settlement_name, services, region)
        actions.append(("Talk to the locals",
                        lambda r=region: _talk_to_locals(r)))
        actions.append(("Check the quest board",
                        lambda s=settlement_name: _quest_board(s)))
        print(f"\n--- {settlement_name.replace('_', ' ').title()} ---")
        for i, (label, _) in enumerate(actions, start=1):
            print(f"{i}. {label}")
        print(f"{len(actions) + 1}. Leave the settlement")
        choice = _ask()
        if not choice.isdigit():
            print("\nInvalid choice.")
            continue
        n = int(choice) - 1
        if 0 <= n < len(actions):
            actions[n][1]()
        else:
            print(f"\nYou leave {settlement_name.replace('_', ' ')}.")
            return


def settlement_menu() -> None:
    from region_manager import REGIONS, get_region_settlements

    region = _current_region()
    settlements = get_region_settlements(region)
    here = REGIONS.get(region, {})

    print("\n=== SETTLEMENTS ===")
    print(f"Region: {here.get('display_name', region)}")
    if not settlements:
        print("\nThere are no settlements in this region.")
        return

    for i, name in enumerate(settlements, start=1):
        print(f"{i}. {name.replace('_', ' ').title()}")
    print(f"{len(settlements) + 1}. Leave")

    choice = _ask()
    if not choice.isdigit():
        return
    idx = int(choice) - 1
    if 0 <= idx < len(settlements):
        enter_settlement_scene(settlements[idx])


# ---------------------------------------------------------------------------
# 3 · Explore -> player agency (reuses existing encounter/quest/event systems)
# ---------------------------------------------------------------------------
def explore_menu() -> None:
    from combat_bridge import start_encounter            # canonical tactical combat
    from quest_manager import generate_quest
    from world_event_manager import generate_random_world_event
    from location_manager import random_location_discovery

    def _search():
        print("\nYou search the area carefully...")
        try:
            random_location_discovery()
        except Exception:
            generate_random_world_event()

    def _hunt():
        print("\nYou seek out trouble...")
        start_encounter(interactive=True)

    def _opportunity():
        print("\nYou look for work and opportunity...")
        generate_quest()

    def _scout():
        print("\nYou scout the surroundings for signs of larger events...")
        generate_random_world_event()

    def _camp():
        print("\nYou make camp and let the world turn.")
        # world tick handled by the caller (game_loop) after explore.

    _menu("EXPLORE", [
        ("Search the area (discoveries)", _search),
        ("Hunt for trouble (fight)", _hunt),
        ("Seek opportunities (quests)", _opportunity),
        ("Scout the surroundings (events)", _scout),
        ("Make camp (rest)", _camp),
    ], back_label="Move on")


# ---------------------------------------------------------------------------
# 4 · World map (already dynamic; just surfaced to the player)
# ---------------------------------------------------------------------------
def world_map_menu() -> None:
    from world_map import (show_world_map, show_region_connections,
                           show_world_completion)
    show_world_map()
    show_region_connections(_current_region())
    show_world_completion()
