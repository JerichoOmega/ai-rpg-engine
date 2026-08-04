"""
Ability engine — the canonical "Skill" action
==============================================

Data-driven ability resolution shared by the player and the AI. Abilities come
from two data files, merged into one registry:

* ``abilities.json``       -- class (player) abilities
* ``ability_library.json`` -- shared/enemy abilities referenced by blueprints

No enemy-specific code: an enemy "uses" an ability purely because its blueprint
lists the id and its profile makes it worth casting. Effects are resolved by the
ability's ``type`` field.

Design pillar — *Information Before Commitment*: every consumer (player UI, AI,
verification harness, future graphical client) reads ability legality and
expected effect from a **single** authoritative source, :func:`ability_preview`,
exactly the way movement/attacks read :func:`inspection.movement_preview` and
:func:`inspection.compute_hit_chance`. There are no hidden calculations and no
duplicated ability logic.

Transient statuses used here: ``rooted`` (skip movement one turn), ``poison``
(damage-over-time until cleansed), ``shielded`` (halve the next hit),
``emboldened`` (+hit), ``marked`` (easier to hit), ``hexed``/``cursed`` (-hit).
Cooldowns are fully data-driven (each ability's ``cooldown`` field), tracked per
combatant in ``unit.cooldowns``, ticked once at the start of each activation.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Tuple

from .inspection import chebyshev

_DATA = os.path.join(os.path.dirname(__file__), "data")


def _load(name: str) -> Dict:
    with open(os.path.join(_DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


# class abilities first, shared library fills the rest (ids are unique enough)
REGISTRY: Dict[str, Dict] = {}
REGISTRY.update(_load("ability_library.json"))
REGISTRY.update(_load("abilities.json"))

# Ability-type taxonomy (drives targeting requirements + previews).
_TARGET_TYPES = ("attack", "movement_attack", "control", "debuff")
_TILE_TYPES = ("terrain", "movement")
_TRANSIENT = ("emboldened", "marked", "hexed", "cursed")
_SUMMON_CAP = 3

# Default tactical value per type — the AI's "why" for using an ability.
_BASE_VALUE = {
    "summon": 60.0, "heal": 55.0, "buff": 48.0, "zone": 48.0,
    "control": 42.0, "debuff": 34.0, "movement_attack": 32.0,
    "attack": 30.0, "terrain": 28.0, "movement": 15.0,
}


def get(ability_id: str) -> Optional[Dict]:
    return REGISTRY.get(ability_id)


def _ap(ab: Dict) -> int:
    return int(ab.get("ap", ab.get("ap_cost", 1)))


def _base_damage(unit, ab: Dict) -> int:
    if "damage" in ab:
        return int(ab["damage"])
    return int(getattr(unit, "damage_max", 6) + ab.get("damage_bonus", 0))


def _is_shield(ab: Dict) -> bool:
    return bool(ab.get("cover_grant")) or ab.get("effect") == "damage_shield"


def _is_morale(ab: Dict) -> bool:
    return ab.get("effect") in ("morale_boost", "embolden_pack")


# ---------------------------------------------------------------------------
# Save/load compatibility (combat ability state is plain JSON-able data)
# ---------------------------------------------------------------------------
def export_state(unit) -> Dict:
    return {"statuses": list(unit.statuses), "cooldowns": dict(unit.cooldowns)}


def import_state(unit, data: Dict) -> None:
    unit.statuses = list(data.get("statuses", []))
    unit.cooldowns = dict(data.get("cooldowns", {}))


# ---------------------------------------------------------------------------
# Start-of-turn upkeep: tick cooldowns, then process transient statuses.
# ---------------------------------------------------------------------------
def start_of_turn(engine, unit) -> None:
    if not unit.alive:
        return
    # Cooldowns tick once per activation (data-driven, no per-ability code).
    for aid in list(unit.cooldowns.keys()):
        unit.cooldowns[aid] -= 1
        if unit.cooldowns[aid] <= 0:
            del unit.cooldowns[aid]

    st = unit.statuses
    if "rooted" in st:
        unit.move = 0
        st.remove("rooted")
    if "poison" in st:
        unit.hp -= 3
        engine.log.append(f"{unit.name} suffers 3 poison damage.")
        if unit.hp <= 0:
            engine.bf.tile(unit.x, unit.y).occupant = None
            engine.log.append(f"{unit.name} succumbs to poison.")
            return
    for s in _TRANSIENT:
        while s in st:
            st.remove(s)


# ---------------------------------------------------------------------------
# THE single authoritative Ability Preview API
# ---------------------------------------------------------------------------
def ability_preview(engine, unit, ability_id: str, target=None,
                    tile=None) -> Dict:
    """Everything an ability hover/preview would show — and the exact data the
    AI scores on. One source of truth for legality, cost, and expected effect.
    """
    ab = get(ability_id)
    if ab is None:
        return {"ability_id": ability_id, "name": ability_id, "usable": False,
                "failure_reason": "unknown ability", "tactical_value": 0.0}

    typ = ab.get("type", "attack")
    ap_cost = _ap(ab)
    total_cd = int(ab.get("cooldown", 0))
    cd_remaining = int(unit.cooldowns.get(ability_id, 0))
    rng = int(ab.get("range", 1))
    requires_los = bool(ab.get("requires_los", rng > 0))
    target_required = typ in _TARGET_TYPES
    tile_required = typ in _TILE_TYPES

    if typ in ("attack", "movement_attack"):
        expected_damage = _base_damage(unit, ab)
    elif "damage" in ab:                    # control/terrain w/ splash damage
        expected_damage = int(ab["damage"])
    else:
        expected_damage = None
    expected_healing = (int(ab.get("heal", 8))
                        if typ == "heal" or ab.get("effect") == "heal_zone"
                        else None)

    buffs: List[str] = []
    debuffs: List[str] = []
    statuses: List[str] = []
    if ab.get("status"):
        (debuffs if typ == "debuff" else statuses).append(ab["status"])
    if typ in ("buff", "zone"):
        if _is_shield(ab):
            buffs.append("shielded")
        if _is_morale(ab):
            buffs.append("emboldened")

    friendly_fire_risk = bool(ab.get("ignites")) or (
        typ == "terrain" and bool(ab.get("creates") or "damage" in ab))

    info = {
        "ability_id": ability_id,
        "name": ab.get("name", ability_id),
        "type": typ,
        "ap_cost": ap_cost,
        "range": rng,
        "cooldown": total_cd,
        "cooldown_remaining": cd_remaining,
        "requires_los": requires_los,
        "target_required": target_required,
        "aoe": ab.get("aoe"),
        "summons": ab.get("summons"),
        "terrain_effect": ab.get("creates") or ab.get("creates_status"),
        "terrain_restrictions": ("target tile must be passable"
                                 if typ == "movement" else None),
        "buffs": buffs,
        "debuffs": debuffs,
        "status_effects": statuses,
        "expected_damage": expected_damage,
        "expected_healing": expected_healing,
        "friendly_fire_risk": friendly_fire_risk,
        "line_of_sight": None,
        "in_range": None,
        "legal_target": None,
        "description": ab.get("description", ""),
    }

    # -- legality gate (single source used by use_skill and the AI) --------
    usable, reason = True, None
    if unit.ap < ap_cost:
        usable, reason = False, "not enough AP"
    elif cd_remaining > 0:
        usable, reason = False, f"on cooldown ({cd_remaining} turn(s) left)"
    elif target_required:
        if target is None or not getattr(target, "alive", False):
            usable, reason = False, "requires a valid target"
        else:
            los = engine.bf.line_of_sight(unit.pos, target.pos)
            in_range = chebyshev(unit.pos, target.pos) <= rng if rng > 0 else True
            info["line_of_sight"] = los
            info["in_range"] = in_range
            info["legal_target"] = in_range and (los or not requires_los)
            if not in_range:
                usable, reason = False, "target out of range"
            elif requires_los and not los:
                usable, reason = False, "no line of sight to target"
    elif tile_required:
        spot = tile or (target.pos if target else None)
        if spot is None:
            usable, reason = False, "requires a target tile"
        else:
            los = engine.bf.line_of_sight(unit.pos, spot)
            in_range = chebyshev(unit.pos, spot) <= rng if rng > 0 else True
            passable = engine.bf.tile(*spot).is_passable()
            info["line_of_sight"] = los
            info["in_range"] = in_range
            info["legal_target"] = in_range and (los or not requires_los)
            if not in_range:
                usable, reason = False, "tile out of range"
            elif requires_los and not los:
                usable, reason = False, "no line of sight to tile"
            elif typ == "movement" and not passable:
                usable, reason = False, "destination tile is blocked"

    info["usable"] = usable
    info["failure_reason"] = reason
    info["tactical_value"] = _tactical_value(engine, unit, ab, typ, target,
                                              expected_damage)
    return info


def _tactical_value(engine, unit, ab, typ, target, expected_damage) -> float:
    """The 'why now' score. Role reinforcement happens naturally: a unit only
    scores the abilities its blueprint gives it (commanders buff, casters
    control, necromancers summon)."""
    allies = [a for a in engine.allies_of(unit) if a.alive]
    other_allies = [a for a in allies if a is not unit]
    base = _BASE_VALUE.get(typ, 20.0)

    if typ in ("attack", "movement_attack"):
        return base + float(expected_damage or 0)
    if typ == "summon":
        if ab.get("effect") == "heal_zone":
            wounded = [a for a in allies if a.hp < a.max_hp]
            return 55.0 if wounded else 0.0
        return 0.0 if unit.ai_memory.get("summons_made", 0) >= _SUMMON_CAP else base
    if typ == "heal":
        wounded = [a for a in allies if a.hp < a.max_hp]
        return base if wounded else 0.0
    if typ in ("buff", "zone"):
        if _is_shield(ab):
            recipients = [unit] + [a for a in other_allies
                                   if chebyshev(unit.pos, a.pos) <= 1]
            need = any("shielded" not in a.statuses for a in recipients)
            return base if need else 0.0
        if _is_morale(ab):
            return base if other_allies else 20.0
        return base
    if typ == "control":
        if target is None:
            return 0.0
        if ab.get("effect") == "force_target":
            return base if target.ai_memory.get("target_id") != unit.id else 0.0
        return base if ab.get("status", "rooted") not in target.statuses else 0.0
    if typ == "debuff":
        if target is None:
            return 0.0
        return base if ab.get("status", "hexed") not in target.statuses else 0.0
    if typ == "terrain":
        return base
    return 0.0


# ---------------------------------------------------------------------------
# The Skill action — gated entirely by the preview (one source of truth)
# ---------------------------------------------------------------------------
def use_skill(engine, unit, ability_id: str, target=None, tile=None) -> bool:
    prev = ability_preview(engine, unit, ability_id, target=target, tile=tile)
    if not prev["usable"]:
        return False
    ab = get(ability_id)
    handler = _HANDLERS.get(ab.get("type", "attack"), _h_attack)
    if not handler(engine, unit, ab, target, tile):
        return False
    unit.ap -= prev["ap_cost"]
    cd = int(ab.get("cooldown", 0))
    if cd > 0:
        unit.cooldowns[ability_id] = cd
    return True


# ---------------------------------------------------------------------------
# Effect handlers (keyed by ability type)
# ---------------------------------------------------------------------------
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
    if target is None or not target.alive:
        return False
    base = _base_damage(unit, ab)
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
    if target is None or not target.alive:
        return False
    for nb in engine.bf.neighbors(*target.pos):
        if engine.bf.tile(*nb).is_passable():
            engine.bf.tile(unit.x, unit.y).occupant = None
            unit.x, unit.y = nb
            engine.bf.tile(*nb).occupant = unit.id
            break
    return _h_attack(engine, unit, ab, target, tile)


def _h_summon(engine, unit, ab, target, tile) -> bool:
    if ab.get("effect") == "heal_zone":
        return _h_heal(engine, unit, ab, target, tile)
    from . import enemies as _enemies
    sid = ab.get("summons")
    if not sid:
        return False
    if unit.ai_memory.get("summons_made", 0) >= _SUMMON_CAP:
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
    unit.ai_memory["summons_made"] = unit.ai_memory.get("summons_made", 0) + 1
    engine.log.append(f"{unit.name} summons a {minion.name}!")
    return True


def _h_heal(engine, unit, ab, target, tile) -> bool:
    amount = int(ab.get("heal", 8))
    rng = int(ab.get("range", 3))
    recipients = [a for a in engine.allies_of(unit)
                  if a.alive and chebyshev(unit.pos, a.pos) <= rng
                  and a.hp < a.max_hp]
    if not recipients:
        return False
    for a in recipients:
        a.hp = min(a.max_hp, a.hp + amount)
    engine.log.append(f"{unit.name} uses {ab.get('name', 'a blessing')}, "
                      f"healing {len(recipients)} ally/allies for {amount}.")
    return True


def _h_buff(engine, unit, ab, target, tile) -> bool:
    name = ab.get("name", "a boon")
    if _is_shield(ab):
        recipients = [unit] + [a for a in engine.allies_of(unit)
                               if a.alive and a is not unit
                               and chebyshev(unit.pos, a.pos) <= 1]
        for a in recipients:
            if "shielded" not in a.statuses:
                a.statuses.append("shielded")
        engine.log.append(f"{unit.name} uses {name}, shielding "
                          f"{len(recipients)} ally/allies.")
        return True
    if _is_morale(ab):
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
    if target is None or not target.alive:
        return False
    if ab.get("effect") == "force_target":
        target.ai_memory["target_id"] = unit.id
        engine.log.append(f"{unit.name} taunts {target.name}!")
        return True
    status = ab.get("status", "rooted")
    target.statuses.append(status)
    if ab.get("damage"):
        _apply_damage(engine, unit, target, int(ab["damage"]))
    engine.log.append(f"{unit.name} afflicts {target.name} with {status}.")
    return True


def _h_debuff(engine, unit, ab, target, tile) -> bool:
    if target is None or not target.alive:
        return False
    target.statuses.append(ab.get("status", "hexed"))
    engine.log.append(f"{unit.name} uses {ab.get('name', 'a curse')} on "
                      f"{target.name}.")
    return True


def _h_terrain(engine, unit, ab, target, tile) -> bool:
    spot = tile or (target.pos if target else None)
    if spot is None:
        return False
    if ab.get("creates"):
        engine.bf.set_terrain(spot[0], spot[1], ab["creates"])
    if ab.get("creates_status"):
        engine.bf.tile(*spot).env[ab["creates_status"]] = True
    if ab.get("damage") and target is not None:
        _apply_damage(engine, unit, target, int(ab["damage"]))
    engine.log.append(f"{unit.name} shapes the battlefield with "
                      f"{ab.get('name', 'a spell')}.")
    return True


def _h_movement(engine, unit, ab, target, tile) -> bool:
    spot = tile or (target.pos if target else None)
    if spot is None or not engine.bf.tile(*spot).is_passable():
        return False
    if not engine.bf.line_of_sight(unit.pos, spot):
        return False
    engine.bf.tile(unit.x, unit.y).occupant = None
    unit.x, unit.y = spot
    engine.bf.tile(*spot).occupant = unit.id
    engine.log.append(f"{unit.name} repositions with {ab.get('name', 'a leap')}.")
    return True


_HANDLERS = {
    "attack": _h_attack, "movement_attack": _h_movement_attack,
    "summon": _h_summon, "heal": _h_heal, "buff": _h_buff,
    "control": _h_control, "debuff": _h_debuff, "terrain": _h_terrain,
    "zone": _h_buff, "movement": _h_movement,
}


# ---------------------------------------------------------------------------
# AI ability selection — reads the same preview the player sees.
# ---------------------------------------------------------------------------
def choose_ability(engine, unit, target) -> Optional[Tuple[str, dict]]:
    """Pick the highest-value *usable* ability, or None to fall back to a basic
    attack. Profile flags gently bias which role-abilities are preferred, but
    every legality/effect fact comes from :func:`ability_preview`."""
    p = getattr(unit, "ai_profile", {}) or {}
    best, best_val = None, 0.0
    for aid in getattr(unit, "equipped", []):
        ab = get(aid)
        if ab is None:
            continue
        typ = ab.get("type", "attack")
        if typ == "movement":                       # AI repositions via normal move
            continue
        kwargs: Dict = {}
        if typ in _TARGET_TYPES:
            kwargs = {"target": target}
        elif typ == "terrain":
            kwargs = {"target": target,
                      "tile": target.pos if target else None}
        prev = ability_preview(engine, unit, aid,
                               target=kwargs.get("target"),
                               tile=kwargs.get("tile"))
        if not prev["usable"] or prev["tactical_value"] <= 0:
            continue
        val = prev["tactical_value"]
        if typ in ("buff", "zone", "heal"):
            if p.get("coordinates"):
                val *= 1.4
            if p.get("buffs_allies"):
                val *= 1.4
        if typ == "summon" and p.get("summons"):
            val *= 1.4
        if typ in ("control", "debuff") and p.get("kites"):
            val *= 1.2
        if val > best_val:
            best_val, best = val, (aid, kwargs)
    return best
