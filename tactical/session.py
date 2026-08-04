"""
Interactive Tactical Combat Session
===================================

The terminal UI that lets a player drive their party through the **canonical**
tactical engine (`tactical/`). Enemies use the shared AI; the player uses the
same actions, inspection and hit-chance the AI does — no hidden information.

This module only *drives* the engine; all rules live in the engine. Combat can
also run headless (AI plays both sides) for tests and quick resolution.
"""

from __future__ import annotations

from typing import Callable, Optional

from .actions import (move as act_move, attack as act_attack,
                      prepare as act_prepare, use_skill as act_skill,
                      use_item as act_item, ITEMS)
from .inspection import (compute_hit_chance, inspect_tile, movement_preview,
                         chebyshev)
from . import abilities_engine
from .render import render_battlefield


def _parse_xy(text: str):
    text = text.replace(",", " ").split()
    if len(text) != 2:
        return None
    try:
        return int(text[0]), int(text[1])
    except ValueError:
        return None


def _unit_line(unit) -> str:
    return (f"{unit.name}  HP {unit.hp}/{unit.max_hp}  "
            f"move {unit.move}  AP {unit.ap}  facing {unit.facing or '-'}")


def interactive_controller(read: Callable[[str], str] = input):
    """Return a per-unit controller closure bound to an input function."""

    def controller(engine, unit) -> None:
        abilities_engine.start_of_turn(engine, unit)
        while unit.alive and (unit.ap > 0 or unit.move > 0):
            print("\n" + render_battlefield(engine))
            print("\nYour turn: " + _unit_line(unit))
            if unit.statuses:
                print("Status: " + ", ".join(unit.statuses))
            print("1. Move   2. Attack   3. Skill   4. Use item   "
                  "5. Prepare (end turn)   6. Inspect tile   7. End turn")
            choice = read("Action: ").strip()

            if choice == "1":
                _do_move(engine, unit, read)
            elif choice == "2":
                _do_attack(engine, unit, read)
            elif choice == "3":
                _do_skill(engine, unit, read)
            elif choice == "4":
                _do_item(engine, unit, read)
            elif choice == "5":
                act_prepare(engine, unit)
                return
            elif choice == "6":
                _do_inspect(engine, unit, read)
            else:
                return

    return controller


def _do_skill(engine, unit, read) -> None:
    equipped = getattr(unit, "equipped", [])
    usable = [(aid, abilities_engine.get(aid)) for aid in equipped
              if abilities_engine.get(aid)]
    if not usable:
        print("No abilities equipped.")
        return
    print("\nAbilities (Information Before Commitment):")
    previews = []
    for i, (aid, ab) in enumerate(usable, start=1):
        prev = abilities_engine.ability_preview(engine, unit, aid)
        previews.append((aid, ab, prev))
        cd = (f", CD {prev['cooldown_remaining']}"
              if prev["cooldown_remaining"] else "")
        gate = "" if prev["usable"] else f"  [x {prev['failure_reason']}]"
        effect = _effect_summary(prev)
        print(f"{i}. {prev['name']} (AP {prev['ap_cost']}, range "
              f"{prev['range']}, {prev['type']}{cd}){effect}{gate}")
    pick = read("Ability #: ").strip()
    if not pick.isdigit() or not (1 <= int(pick) <= len(previews)):
        print("Cancelled.")
        return
    aid, ab, _ = previews[int(pick) - 1]
    target, tile = None, None
    if ab.get("type") in ("attack", "movement_attack", "control", "debuff",
                          "terrain"):
        enemies = [e for e in engine.enemies_of(unit) if e.alive]
        for j, e in enumerate(enemies, start=1):
            tp = abilities_engine.ability_preview(engine, unit, aid, target=e,
                                                  tile=e.pos)
            legal = "" if tp["usable"] else f" [x {tp['failure_reason']}]"
            print(f"{j}. {e.name} ({e.hp}/{e.max_hp}) @ {e.pos}{legal}")
        tp = read("Target #: ").strip()
        if tp.isdigit() and 1 <= int(tp) <= len(enemies):
            target = enemies[int(tp) - 1]
            tile = target.pos
    if act_skill(engine, unit, aid, target=target, tile=tile):
        print(engine.log[-1])
    else:
        prev = abilities_engine.ability_preview(engine, unit, aid,
                                                target=target, tile=tile)
        print(f"Ability could not be used: {prev.get('failure_reason') or 'no effect'}.")


def _effect_summary(prev) -> str:
    parts = []
    if prev.get("expected_damage"):
        parts.append(f"~{prev['expected_damage']} dmg")
    if prev.get("expected_healing"):
        parts.append(f"~{prev['expected_healing']} heal")
    if prev.get("aoe"):
        parts.append(f"AoE:{prev['aoe']}")
    if prev.get("summons"):
        parts.append(f"summons {prev['summons']}")
    for tag in prev.get("buffs", []) + prev.get("debuffs", []) + \
            prev.get("status_effects", []):
        parts.append(tag)
    if prev.get("friendly_fire_risk"):
        parts.append("friendly-fire risk")
    return ("  — " + ", ".join(parts)) if parts else ""



def _do_item(engine, unit, read) -> None:
    items = getattr(unit, "items", [])
    if not items:
        print("No usable items.")
        return
    for i, iid in enumerate(items, start=1):
        print(f"{i}. {ITEMS.get(iid, {}).get('name', iid)}")
    pick = read("Item #: ").strip()
    if pick.isdigit() and 1 <= int(pick) <= len(items):
        if act_item(engine, unit, items[int(pick) - 1]):
            print(engine.log[-1])


def _do_move(engine, unit, read) -> None:
    if unit.move <= 0:
        print("No movement left.")
        return
    print(f"Enter destination as 'x y' (you have {unit.move} movement).")
    xy = _parse_xy(read("Move to: "))
    if not xy:
        print("Cancelled.")
        return
    prev = movement_preview(engine, unit, xy)
    if not prev.get("reachable"):
        print("That tile is not reachable.")
        return
    if prev.get("provokes_opportunity_from"):
        print("WARNING: leaving reach of "
              f"{', '.join(prev['provokes_opportunity_from'])} "
              "may provoke an opportunity attack.")
    if act_move(engine, unit, xy):
        print(engine.log[-1])
    else:
        print("Move failed.")


def _do_attack(engine, unit, read) -> None:
    if unit.ap <= 0:
        print("No action points left.")
        return
    targets = [e for e in engine.enemies_of(unit) if e.alive]
    shown = []
    print("\nTargets:")
    for enemy in targets:
        info = compute_hit_chance(engine, unit, enemy)
        if info["in_range"] and info["line_of_sight"]:
            shown.append(enemy)
            flank = "" if info["facing"] == "front" else f" [{info['facing']} flank]"
            print(f"{len(shown)}. {enemy.name} ({enemy.hp}/{enemy.max_hp}) "
                  f"— hit {info['chance']:.0%}, cover {info['cover']}{flank}")
    if not shown:
        print("No enemies in range and line of sight.")
        return
    pick = read("Attack #: ").strip()
    if not pick.isdigit() or not (1 <= int(pick) <= len(shown)):
        print("Cancelled.")
        return
    if act_attack(engine, unit, shown[int(pick) - 1]):
        print(engine.log[-1])


def _do_inspect(engine, unit, read) -> None:
    xy = _parse_xy(read("Inspect tile 'x y': "))
    if not xy:
        return
    data = inspect_tile(engine, xy)
    print(f"\nTile {xy}: terrain={data['terrain']} cover={data['cover']} "
          f"move_cost={data['movement_cost']} elevation={data['elevation']} "
          f"blocks_los={data['blocks_los']} hazards={data['hazards']}")
    if data.get("occupant_name"):
        print(f"  Occupant: {data['occupant_name']}")
    if data.get("context_actions"):
        print(f"  Interactions: {data['context_actions']}")


def run_session(engine, interactive: bool = True,
                read: Optional[Callable[[str], str]] = None,
                max_rounds: int = 100) -> str:
    """Run an encounter to conclusion on the canonical engine.

    interactive=True  -> the player drives their units via the terminal.
    interactive=False -> headless (AI plays both sides); used by tests.
    """
    controller = interactive_controller(read or input) if interactive else None
    return engine.auto_battle(max_rounds=max_rounds,
                              player_controller=controller)
