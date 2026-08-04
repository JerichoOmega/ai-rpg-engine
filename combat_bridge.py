"""
Combat Bridge — the single overworld → tactical combat entry point
==================================================================

Per R-01, `tactical/` is the canonical combat runtime. This bridge builds a
tactical encounter from the current world state and region, runs it on the
tactical engine (interactive or headless), and writes results back into
`world_state` (HP, XP, gold, loot, companion survival).

Standard overworld encounters route through :func:`start_encounter`; the legacy
`combat.py` runtime is a compatibility layer and must not be extended.
"""

from __future__ import annotations

import random
from typing import List, Optional

from world_state import world_state
from tactical.battlefield import Battlefield
from tactical.entities import Combatant
from tactical import encounters as tac_encounters
from tactical.engine import CombatEngine, CombatContext
from tactical.session import run_session


# world/companion role -> tactical player class
CLASS_MAP = {
    "warrior": "guardian", "fighter": "guardian", "knight": "guardian",
    "guardian": "guardian", "paladin": "guardian", "barbarian": "guardian",
    "ranger": "ranger", "archer": "ranger", "hunter": "ranger", "scout": "ranger",
    "mage": "mage", "wizard": "mage", "sorcerer": "mage", "cleric": "mage",
    "warlock": "mage", "druid": "mage",
    "rogue": "rogue", "thief": "rogue", "assassin": "rogue",
}

# region biome -> canonical encounter group (all blueprint-based)
BIOME_GROUPS = {
    "forest": "forest_wolf_pack", "woods": "forest_wolf_pack",
    "plains": "roadside_ambush", "road": "roadside_ambush",
    "grassland": "roadside_ambush", "hills": "roadside_ambush",
    "mountain": "orc_warband", "mountains": "orc_warband", "snow": "orc_warband",
    "swamp": "cave_swarm", "marsh": "cave_swarm", "cave": "cave_swarm",
    "caves": "cave_swarm", "underground": "cave_swarm",
    "ruins": "ruins_undead", "crypt": "ruins_undead", "graveyard": "ruins_undead",
    "corrupted": "corrupted_incursion", "blighted": "corrupted_incursion",
}

# biome -> a little battlefield flavour (terrain + a scatter object)
BIOME_TERRAIN = {
    "forest": ("plains", "pine_tree"), "woods": ("plains", "pine_tree"),
    "mountain": ("hill", "boulder"), "mountains": ("hill", "boulder"),
    "snow": ("plains", "boulder"), "ruins": ("rubble", "wall_segment"),
    "crypt": ("rubble", "wall_segment"), "swamp": ("plains", "pine_tree"),
    "marsh": ("plains", "pine_tree"), "cave": ("plains", "boulder"),
    "corrupted": ("scorched", "boulder"),
}

WIDTH, HEIGHT = 9, 6


def _map_class(role: Optional[str]) -> str:
    return CLASS_MAP.get((role or "").lower(), "guardian")


def _build_battlefield(biome: str, region: str) -> Battlefield:
    bf = Battlefield(WIDTH, HEIGHT, battlefield_id=f"encounter_{region}")
    terrain, obj = BIOME_TERRAIN.get(biome, (None, None))
    if terrain:
        rng = random.Random()
        for _ in range(4):
            x, y = rng.randint(2, WIDTH - 3), rng.randint(0, HEIGHT - 1)
            bf.set_terrain(x, y, terrain)
            if obj:
                bf.tile(x, y).add_object(obj)
    return bf


def _build_party() -> List[Combatant]:
    ws_player = world_state["player"]
    party: List[Combatant] = []

    hero = Combatant(ws_player.get("name", "Hero"),
                     _map_class(ws_player.get("class")), "player", 0, 0)
    hero.max_hp = int(ws_player.get("max_hp", hero.max_hp))
    hero.hp = max(1, int(ws_player.get("hp", hero.max_hp)))
    # light level scaling so progression matters (does not touch class identity)
    lvl = int(ws_player.get("level", 1))
    hero.damage_min += (lvl - 1)
    hero.damage_max += (lvl - 1)
    hero._world_ref = "player"
    party.append(hero)

    try:
        from companion_manager import active_companions
    except Exception:
        active_companions = []
    y = 1
    for comp in active_companions:
        if y >= HEIGHT:
            break
        c = Combatant(comp.get("name", "Ally"),
                      _map_class(comp.get("role") or comp.get("class")),
                      "player", 0, y)
        c.max_hp = int(comp.get("max_hp", c.max_hp))
        c.hp = max(1, int(comp.get("hp", c.max_hp)))
        c._companion_ref = comp
        party.append(c)
        y += 1
    return party


def _pick_group(region: str) -> str:
    from region_manager import REGIONS
    biome = (REGIONS.get(region, {}) or {}).get("biome", "plains")
    return BIOME_GROUPS.get(str(biome).lower(), "roadside_ambush"), biome


def _apply_results(outcome: str, party: List[Combatant],
                   enemy_count: int) -> None:
    ws_player = world_state["player"]

    # HP write-back for the hero (authoritative world_state + runtime Player).
    hero = party[0]
    ws_player["hp"] = max(0 if outcome == "enemy" else 1, hero.hp)
    if ws_player["hp"] <= 0:
        ws_player["hp"] = 1  # avoid overworld softlock; defeat handled below
    try:
        from player import player as _p
        _p.hp = ws_player["hp"]
    except Exception:
        pass

    # Companion HP write-back.
    for c in party[1:]:
        ref = getattr(c, "_companion_ref", None)
        if isinstance(ref, dict):
            ref["hp"] = max(0, c.hp)

    if outcome != "player":
        print("\nYour party was overwhelmed. You withdraw, wounded.")
        return

    # Victory rewards (canonical XP entry point + gold + a loot roll).
    xp = enemy_count * 20
    try:
        from progression_manager import award_xp_to_roster
        award_xp_to_roster(xp)
    except Exception:
        ws_player["xp"] = ws_player.get("xp", 0) + xp
    gold = enemy_count * random.randint(8, 15)
    ws_player["gold"] = ws_player.get("gold", 0) + gold
    print(f"\nVictory! The party earns {xp} XP and {gold} gold.")

    try:
        from loot_manager import generate_loot
        drop = generate_loot()
        if drop:
            ws_player.setdefault("inventory", []).append(
                drop if isinstance(drop, str) else drop.get("name", str(drop)))
            print(f"Loot found: {drop if isinstance(drop, str) else drop.get('name', drop)}")
    except Exception:
        pass


def start_encounter(region: Optional[str] = None,
                    group_id: Optional[str] = None,
                    interactive: bool = True,
                    context_origin: str = "overworld",
                    location_id: str = "") -> str:
    """Build and run a standard overworld encounter on the tactical engine.

    Returns the winning team ("player" | "enemy" | "draw").
    """
    region = region or world_state["regions"]["current_region"]
    if group_id is None:
        group_id, biome = _pick_group(region)
    else:
        from region_manager import REGIONS
        biome = (REGIONS.get(region, {}) or {}).get("biome", "plains")

    bf = _build_battlefield(str(biome).lower(), region)
    party = _build_party()
    for i, unit in enumerate(party):
        bf.tile(0, i % HEIGHT).occupant = None  # placement handled by engine.start
        unit.x, unit.y = 0, i % HEIGHT

    enemies = tac_encounters.build_group(group_id, battlefield=bf)
    # Light fairness cap so a small party isn't swarmed (full threat-budget
    # scaling is a later phase). Reuses the existing roster, just trims it.
    cap = max(2, len(party) + 1)
    enemies = enemies[:cap]
    combatants = party + enemies

    print(f"\n=== ENCOUNTER: {group_id.replace('_', ' ').title()} "
          f"({len(enemies)} foes) ===")

    engine = CombatEngine(bf, combatants,
                          context=CombatContext(context_origin, location_id),
                          world_state=world_state)
    outcome = run_session(engine, interactive=interactive)

    print("\n" + "\n".join(engine.log[-6:]))
    _apply_results(outcome, party, len(enemies))
    # keep the runtime Player object and world_state in sync after combat
    try:
        from player import sync_world_state_from_player
        sync_world_state_from_player()
    except Exception:
        pass
    return outcome
