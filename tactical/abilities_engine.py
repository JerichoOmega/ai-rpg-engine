"""
Ability engine (the canon "Skill" action, completed)
=====================================================

Data-driven ability resolution shared by the player and the AI. Abilities come
from two data files, merged into one registry:

* ``abilities.json``       -- class (player) abilities
* ``ability_library.json`` -- shared/enemy abilities referenced by blueprints

No enemy-specific code: an enemy "uses" an ability purely because its blueprint
lists the id and its profile makes it worth casting. Effects are resolved by the
ability's ``type`` field.

Transient statuses used here: ``rooted`` (skip movement one turn), ``poison``
(damage-over-time), ``shielded`` (halve the next hit), ``emboldened`` (+hit),
``marked`` (easier to hit), ``hexed``/``cursed`` (-hit).
"""

from __future__ import annotations

import json
import os
from typing import Dict, Optional, Tuple

from .inspection import compute_hit_chance, chebyshev
from .facing import dir_from_to

_DATA = os.path.join(os.path.dirname(__file__), "data")


def _load(name: str) -> Dict:
    with open(os.path.join(_DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


# class abilities first, shared library fills the rest (ids are unique enough)
REGISTRY: Dict[str, Dict] = {}
REGISTRY.update(_load("ability_library.json"))
REGISTRY.update(_load("abilities.json"))


def get(ability_id: str) -> Optional[Dict]:
    return REGISTRY.get(ability_id)


def _ap(ab: Dict) -> int:
    return int(ab.get("ap", ab.get("ap_cost", 1)))


# ---------------------------------------------------------------------------
# Status processing (called at the start of a unit's activation)
# ---------------------------------------------------------------------------
_TRANSIENT = ("emboldened", "marked", "hexed", "cursed")


def start_of_turn(engine, unit) -> None:
    if not unit.alive:
        return
    st = unit.statuses
    if "rooted" in st:
        unit.move = 0
        st.remove("rooted")
    if "poison" in st:
        unit.hp -= 3
        engine.log.append(f"{unit.name} suffers 3 poison damage.")
        if unit.hp <= 0:
            engine.bf.tile(unit.x, unit.y).occupant = None
            return
    for s in _TRANSIENT:
        while s in st:
            st.remove(s)


# ---------------------------------------------------------------------------
# The Skill action
# ---------------------------------------------------------------------------
def use_skill(engine, unit, ability_id: str, target=None, tile=None) -> bool:
    ab = get(ability_id)
    if ab is None:
        return False
    ap = _ap(ab)
    if unit.ap < ap:
        return False
    rng = int(ab.get("range", 1))
    typ = ab.get("type", "attack")

    if target is not None and rng > 0:
        if chebyshev(unit.pos, target.pos) > rng or \
                not engine.bf.line_of_sight(unit.pos, target.pos):
            return False

    handler = _HANDLERS.get(typ, _h_attack)
    if not handler(engine, unit, ab, target, tile):
        return False
    unit.ap -= ap
    return True


def _apply_damage(engine, attacker, defender, amount: int) -> None:
    dmg = max(1, int(amount) - getattr(defender, "armor", 0))
    if "shielded" in defender.statuses:
        dmg = max(1, dmg // 2)
        defender.statuses.remove("shielded")
    defender.hp -= dmg
    engine.log.append(f"{attacker.name} strikes {defender.name} for {dmg}.")
    if defender.hp <= 0:
        engine.bf.tile(defender.x, defender.y).occupant = None
        engine.log.append(f"{defender.name} is defeated.")


def _h_attack(engine, unit, ab, target, tile) -> bool:
    if target is None:
        return False
    base = int(ab.get("damage", max(unit.damage_max,
                                    unit.damage_max + ab.get("damage_bonus", 0))))
    engine.log.append(f"{unit.name} uses {ab.get('name', 'an ability')}!")
    _apply_damage(engine, unit, target, base)
    if ab.get("status"):
        target.statuses.append(ab["status"])
    if ab.get("aoe"):                       # splash to foes adjacent to target
        for e in engine.enemies_of(unit):
            if e.alive and e is not target and chebyshev(e.pos, target.pos) == 1:
                _apply_damage(engine, unit, e, max(1, base // 2))
    if ab.get("ignites"):
        engine.bf.ignite(*target.pos)
    return True


def _h_movement_attack(engine, unit, ab, target, tile) -> bool:
    if target is None:
        return False
    # close to an adjacent tile, then strike
    for nb in engine.bf.neighbors(*target.pos):
        if engine.bf.tile(*nb).is_passable():
            engine.bf.tile(unit.x, unit.y).occupant = None
            unit.x, unit.y = nb
            unit.facing = dir_from_to(nb, target.pos)
            engine.bf.tile(*nb).occupant = unit.id
            break
    return _h_attack(engine, unit, ab, target, tile)


def _h_summon(engine, unit, ab, target, tile) -> bool:
    from . import enemies as _enemies
    sid = ab.get("summons")
    if not sid:
        return False
    # termination guard: cap summons per caster
    made = unit.ai_memory.get("summons_made", 0)
    if made >= 3:
        return False
    spot = None
    for nb in engine.bf.neighbors(*unit.pos):
        if engine.bf.tile(*nb).is_passable():
            spot = nb
            break
    if spot is None:
        return False
    minion = _enemies.spawn_enemy(sid, spot[0], spot[1], team=unit.team)
    engine.combatants.append(minion)
    engine.bf.tile(*spot).occupant = minion.id
    unit.ai_memory["summons_made"] = made + 1
    engine.log.append(f"{unit.name} summons a {minion.name}!")
    return True


def _h_buff(engine, unit, ab, target, tile) -> bool:
    name = ab.get("name", "a boon")
    if ab.get("cover_grant") or ab.get("effect") == "damage_shield":
        recipients = [unit] + [a for a in engine.allies_of(unit)
                               if a.alive and chebyshev(unit.pos, a.pos) <= 1]
        for a in recipients:
            if "shielded" not in a.statuses:
                a.statuses.append("shielded")
        engine.log.append(f"{unit.name} uses {name}, shielding "
                          f"{len(recipients)} ally/allies.")
        return True
    if ab.get("effect") in ("morale_boost", "embolden_pack"):
        rng = int(ab.get("range", 6))
        allies = [a for a in engine.allies_of(unit)
                  if a.alive and chebyshev(unit.pos, a.pos) <= rng]
        for a in allies:
            a.statuses.append("emboldened")
            a.ai_memory["morale"] = "high"
        engine.log.append(f"{unit.name} uses {name}; the ranks steady.")
        return True
    return False


def _h_control(engine, unit, ab, target, tile) -> bool:
    if target is None:
        return False
    if ab.get("effect") == "force_target":
        target.ai_memory["target_id"] = unit.id
        engine.log.append(f"{unit.name} taunts {target.name}!")
        return True
    status = ab.get("status", "rooted")
    target.statuses.append(status)
    engine.log.append(f"{unit.name} afflicts {target.name} with {status}.")
    return True


def _h_debuff(engine, unit, ab, target, tile) -> bool:
    if target is None:
        return False
    target.statuses.append(ab.get("status", "hexed"))
    engine.log.append(f"{unit.name} uses {ab.get('name', 'a curse')} on "
                      f"{target.name}.")
    return True


def _h_terrain(engine, unit, ab, target, tile) -> bool:
    tile = tile or (target.pos if target else None)
    if tile is None:
        return False
    if ab.get("creates"):
        engine.bf.set_terrain(tile[0], tile[1], ab["creates"])
    if ab.get("creates_status"):
        engine.bf.tile(*tile).env[ab["creates_status"]] = True
    if ab.get("damage") and target is not None:
        _apply_damage(engine, unit, target, int(ab["damage"]))
    engine.log.append(f"{unit.name} shapes the battlefield with "
                      f"{ab.get('name', 'a spell')}.")
    return True


def _h_movement(engine, unit, ab, target, tile) -> bool:
    tile = tile or (target.pos if target else None)
    if tile is None or not engine.bf.tile(*tile).is_passable():
        return False
    if not engine.bf.line_of_sight(unit.pos, tile):
        return False
    engine.bf.tile(unit.x, unit.y).occupant = None
    unit.x, unit.y = tile
    engine.bf.tile(*tile).occupant = unit.id
    engine.log.append(f"{unit.name} repositions with {ab.get('name', 'a leap')}.")
    return True


_HANDLERS = {
    "attack": _h_attack, "movement_attack": _h_movement_attack,
    "summon": _h_summon, "buff": _h_buff, "control": _h_control,
    "debuff": _h_debuff, "terrain": _h_terrain, "zone": _h_buff,
    "movement": _h_movement,
}


# ---------------------------------------------------------------------------
# AI ability selection -- "when and why"
# ---------------------------------------------------------------------------
def choose_ability(engine, unit, target) -> Optional[Tuple[str, dict]]:
    """Pick a worthwhile ability for the AI to cast this turn, or None."""
    for aid in getattr(unit, "equipped", []):
        ab = get(aid)
        if ab is None or unit.ap < _ap(ab):
            continue
        typ = ab.get("type", "attack")
        rng = int(ab.get("range", 1))
        in_range = target is not None and \
            chebyshev(unit.pos, target.pos) <= rng and \
            engine.bf.line_of_sight(unit.pos, target.pos)

        if typ == "summon":
            if unit.ai_memory.get("summons_made", 0) < 3:
                return aid, {}
        elif typ in ("buff", "zone"):
            if ab.get("cover_grant") or ab.get("effect") == "damage_shield":
                if "shielded" not in unit.statuses:
                    return aid, {}
            elif [a for a in engine.allies_of(unit) if a.alive and a is not unit]:
                return aid, {}
        elif typ in ("attack", "movement_attack") and in_range:
            return aid, {"target": target}
        elif typ == "control" and in_range:
            if ab.get("effect") == "force_target" or "rooted" not in target.statuses:
                return aid, {"target": target}
        elif typ == "debuff" and in_range:
            if ab.get("status", "hexed") not in target.statuses:
                return aid, {"target": target}
        elif typ == "terrain" and in_range:
            return aid, {"target": target, "tile": target.pos}
    return None
