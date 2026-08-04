"""
Actions
=======

The six actions (Move, Attack, Skill, Item, Prepare, Interact) plus the
class-specific reactions Prepare enables. Movement spends the ``move`` budget
(tiles); Attack/Interact spend action points (``ap``). Everything reads the
shared tile/battlefield model and the shared hit-chance from
:mod:`tactical.inspection`, so the AI and the player play by identical rules.
"""

from __future__ import annotations

from typing import Tuple

from .inspection import compute_hit_chance, chebyshev
from .facing import dir_from_to, FACING_DMG
from .tiles import OBJECTS
from . import abilities_engine

# The canonical "Skill" action flows through the shared combat pipeline.
use_skill = abilities_engine.use_skill

ITEMS = {
    "healing_potion": {"name": "Healing Potion", "ap": 1, "heal": 20},
    "antidote": {"name": "Antidote", "ap": 1, "cleanse": ["poison", "hexed", "cursed"]},
}


def use_item(engine, unit, item_id: str, target=None) -> bool:
    item = ITEMS.get(item_id)
    if item is None or unit.ap < item.get("ap", 1):
        return False
    who = target or unit
    if item.get("heal"):
        who.hp = min(who.max_hp, who.hp + item["heal"])
        engine.log.append(f"{unit.name} uses {item['name']}: {who.name} heals "
                          f"{item['heal']}.")
    for s in item.get("cleanse", []):
        while s in who.statuses:
            who.statuses.remove(s)
    if item.get("cleanse"):
        engine.log.append(f"{unit.name} uses {item['name']} on {who.name}.")
    unit.ap -= item.get("ap", 1)
    if item_id in getattr(unit, "items", []):
        unit.items.remove(item_id)
    return True

XY = Tuple[int, int]

ATTACK_AP = 1
INTERACT_AP = 1


# ---------------------------------------------------------------------------
# Move (with opportunity reactions)
# ---------------------------------------------------------------------------
def move(engine, unit, target: XY) -> bool:
    bf = engine.bf
    path = bf.path(unit.pos, target, unit.move)
    if not path or path[-1] != target:
        return False
    cost = sum(bf.tile(*p).movement_cost() for p in path[1:])
    if cost > unit.move:
        return False

    # Melee foes the mover starts adjacent to may get an opportunity attack
    # if the mover leaves their reach (Phase A).
    adj_before = [e for e in engine.enemies_of(unit)
                  if e.alive and e.attack_range <= 1
                  and chebyshev(e.pos, unit.pos) == 1]

    bf.tile(unit.x, unit.y).occupant = None
    prev = unit.pos
    for step in path[1:]:
        unit.facing = dir_from_to(prev, step)
        unit.x, unit.y = step
        prev = step
        _trigger_reaction_shots(engine, mover=unit)
        if not unit.alive:
            break
    unit.move -= cost
    if unit.alive:
        bf.tile(unit.x, unit.y).occupant = unit.id
    engine.log.append(f"{unit.name} moves to {unit.pos} (cost {cost})")

    if unit.alive:
        for foe in adj_before:
            if foe.alive and chebyshev(foe.pos, unit.pos) > 1:
                engine.log.append(
                    f"{foe.name} makes an opportunity attack on {unit.name}!")
                _resolve_attack(engine, foe, unit, reaction=True)
                if not unit.alive:
                    break
    return True


def _trigger_reaction_shots(engine, mover) -> None:
    for other in engine.enemies_of(mover):
        if other.alive and other.prepare_stance == "reaction_shot":
            if engine.bf.line_of_sight(other.pos, mover.pos) and \
                    chebyshev(other.pos, mover.pos) <= other.attack_range:
                other.prepare_stance = None
                engine.log.append(f"{other.name} takes a reaction shot!")
                _resolve_attack(engine, other, mover, reaction=True)
                if not mover.alive:
                    return


# ---------------------------------------------------------------------------
# Attack (cover / elevation / evasion / counterattack / armor / crit)
# ---------------------------------------------------------------------------
def attack(engine, attacker, defender) -> bool:
    if attacker.ap < ATTACK_AP:
        return False
    info = compute_hit_chance(engine, attacker, defender)
    if info["chance"] <= 0:
        return False
    attacker.ap -= ATTACK_AP
    _resolve_attack(engine, attacker, defender)
    return True


def _resolve_attack(engine, attacker, defender, reaction: bool = False) -> None:
    info = compute_hit_chance(engine, attacker, defender)
    # Attacker turns to face its target (even if the swing is then evaded).
    attacker.facing = dir_from_to(attacker.pos, defender.pos)
    if defender.prepare_stance == "evasion":
        defender.prepare_stance = None
        engine.log.append(f"{defender.name} evades {attacker.name}'s attack.")
        return

    if engine.rng.random() <= info["chance"]:
        damage = engine.rng.randint(attacker.damage_min, attacker.damage_max)
        if info["elevation"] > 0:
            damage += 1
        crit = engine.rng.random() < getattr(attacker, "crit_chance", 0.05)
        if crit:
            damage = int(damage * 1.5)
        # Flanking (side/rear) increases damage (Phase A).
        damage = int(damage * FACING_DMG.get(info.get("facing", "front"), 1.0))
        # Armor reduces damage (minimum 1 gets through).
        damage = max(1, damage - getattr(defender, "armor", 0))
        if "shielded" in defender.statuses:
            damage = max(1, damage // 2)
            defender.statuses.remove("shielded")
        defender.hp -= damage
        flank = "" if info.get("facing") == "front" else \
            f" {info['facing'].upper()} FLANK"
        tag = " CRIT" if crit else ""
        engine.log.append(
            f"{attacker.name} hits {defender.name} for {damage}{tag}{flank} "
            f"(chance {info['chance']:.0%}, cover {info['cover']}, "
            f"armor {getattr(defender, 'armor', 0)})")
        if defender.hp <= 0:
            engine.bf.tile(defender.x, defender.y).occupant = None
            engine.log.append(f"{defender.name} is defeated.")
            return
    else:
        engine.log.append(
            f"{attacker.name} misses {defender.name} "
            f"(chance {info['chance']:.0%}, cover {info['cover']})")

    if not reaction and defender.prepare_stance == "counterattack" and \
            chebyshev(defender.pos, attacker.pos) <= defender.attack_range:
        defender.prepare_stance = None
        engine.log.append(f"{defender.name} counterattacks!")
        _resolve_attack(engine, defender, attacker, reaction=True)


# ---------------------------------------------------------------------------
# Prepare (replaces Wait) -- arms the class/enemy reaction, ends the turn
# ---------------------------------------------------------------------------
def prepare(engine, unit) -> bool:
    unit.prepare_stance = unit.prepare_reaction()
    unit.ap = 0
    unit.move = 0
    engine.log.append(f"{unit.name} prepares: {unit.prepare_stance}")
    return True


# ---------------------------------------------------------------------------
# Interact -- environmental manipulation
# ---------------------------------------------------------------------------
def interact(engine, unit, target: XY, interaction: str) -> bool:
    if unit.ap < INTERACT_AP or chebyshev(unit.pos, target) > 1:
        return False
    action, _, obj = interaction.partition(":")
    bf = engine.bf
    tile = bf.tile(*target)
    unit.ap -= INTERACT_AP

    if action == "burn_object":
        bf.ignite(*target)
    elif action in ("chop_object", "smash_object"):
        bf.destroy_object(target[0], target[1], obj)
    elif action == "collapse_wall":
        bf.destroy_object(target[0], target[1], obj)
        tile.env["destroyed_" + obj] = True
    elif action == "destroy_bridge":
        bf.destroy_object(target[0], target[1], obj)
        bf.set_terrain(target[0], target[1], "water")
        tile.env["destroyed_bridge"] = True
    elif action == "push_into_object":
        _push_into(engine, unit, target, obj)
    else:
        return False
    engine.log.append(f"{unit.name} uses {action} on {obj} at {target}")
    return True


def _push_into(engine, unit, target: XY, obj: str) -> None:
    victim = engine.unit_at(target)
    if victim:
        damage = OBJECTS.get(obj, {}).get("push_damage", 2)
        victim.hp -= damage
        engine.log.append(f"{victim.name} is shoved into {obj} for {damage}.")
        if victim.hp <= 0:
            engine.bf.tile(victim.x, victim.y).occupant = None
