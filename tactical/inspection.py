"""
Inspection & preview (Pillar 2: Information Before Commitment)
=============================================================

These functions are the terminal realisation of the spec's hover / preview /
overlay UI. They expose *all* tactical information the player needs to decide
before committing -- and the AI calls the exact same functions, so neither
side has hidden information.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from .facing import relative_arc, FACING_HIT

XY = Tuple[int, int]


def chebyshev(a: XY, b: XY) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def inspect_tile(engine, xy: XY) -> Dict:
    """Everything a tile hover would show, plus available context actions."""
    tile = engine.bf.tile(*xy)
    data = tile.to_dict()
    occupant = engine.unit_at(xy)
    data["occupant_name"] = occupant.name if occupant else None
    data["context_actions"] = tile.interactions()
    return data


def compute_hit_chance(engine, attacker, defender) -> Dict:
    """Transparent hit-chance breakdown, shared by attack resolution, the AI,
    and the movement/threat preview."""
    bf = engine.bf
    base = attacker.accuracy
    cover_penalty = bf.cover_penalty(defender.pos, attacker.pos)
    atk_elev = bf.tile(*attacker.pos).elevation
    def_elev = bf.tile(*defender.pos).elevation
    elevation = 0.10 if atk_elev > def_elev else (-0.10 if atk_elev < def_elev
                                                  else 0.0)
    los = bf.line_of_sight(attacker.pos, defender.pos)
    in_range = chebyshev(attacker.pos, defender.pos) <= attacker.attack_range
    arc = relative_arc(defender, attacker.pos)
    facing_bonus = FACING_HIT[arc]
    chance = 0.0 if not (los and in_range) else max(
        0.05, min(0.95, base - cover_penalty + elevation + facing_bonus))
    return {
        "chance": chance, "base": base, "cover_penalty": cover_penalty,
        "elevation": elevation, "line_of_sight": los, "in_range": in_range,
        "cover": bf.directional_cover(defender.pos, attacker.pos),
        "facing": arc, "facing_bonus": facing_bonus,
        "flanking": arc in ("side", "rear"),
    }


def enemies_threatening(engine, unit, xy: XY) -> List[Dict]:
    """Enemies that could hit ``xy`` (LOS + range) -- the threat at a tile."""
    threats = []
    for other in engine.enemies_of(unit):
        if not other.alive:
            continue
        los = engine.bf.line_of_sight(other.pos, xy)
        in_range = chebyshev(other.pos, xy) <= other.attack_range
        if los and in_range:
            threats.append({"id": other.id, "name": other.name,
                            "pos": other.pos, "range": other.attack_range})
    return threats


def threat_map(engine, unit) -> set:
    """All tiles threatened by any living enemy of ``unit`` (live)."""
    threatened = set()
    for other in engine.enemies_of(unit):
        if not other.alive:
            continue
        for y in range(engine.bf.height):
            for x in range(engine.bf.width):
                if chebyshev(other.pos, (x, y)) <= other.attack_range and \
                        engine.bf.line_of_sight(other.pos, (x, y)):
                    threatened.add((x, y))
    return threatened


def movement_preview(engine, unit, target: XY) -> Dict:
    """Path, cost, remaining AP, threat entered, cover gained, and who you
    can hit / who can hit you from the destination -- before you commit."""
    bf = engine.bf
    path = bf.path(unit.pos, target, unit.move)
    if path is None:
        return {"reachable": False}
    cost = sum(bf.tile(*p).movement_cost() for p in path[1:])
    threats = threat_map(engine, unit)
    threat_entered = [p for p in path if p in threats]
    attackable, attackers = [], []
    for enemy in engine.enemies_of(unit):
        if not enemy.alive:
            continue
        if bf.line_of_sight(target, enemy.pos) and \
                chebyshev(target, enemy.pos) <= unit.attack_range:
            attackable.append(enemy.name)
        if bf.line_of_sight(enemy.pos, target) and \
                chebyshev(enemy.pos, target) <= enemy.attack_range:
            attackers.append(enemy.name)
    provoke = [e.name for e in engine.enemies_of(unit)
               if e.alive and e.attack_range <= 1
               and chebyshev(e.pos, unit.pos) == 1
               and chebyshev(e.pos, target) > 1]
    return {
        "reachable": True, "path": path, "cost": cost,
        "final_move": unit.move - cost,
        "cover_at_destination": bf.tile(*target).cover_value(),
        "elevation_at_destination": bf.tile(*target).elevation,
        "threat_tiles_entered": threat_entered,
        "enemies_attackable": attackable,
        "enemies_that_can_hit_you": attackers,
        "provokes_opportunity_from": provoke,
    }


def tactical_overlay(engine, unit) -> Dict[str, Dict]:
    """Optional overlay data: movement cost, cover, elevation, hazards, LOS
    from the unit, and enemy vision -- for the whole grid."""
    bf = engine.bf
    reach = bf.reachable(unit.pos, unit.move)
    threats = threat_map(engine, unit)
    overlay = {}
    for y in range(bf.height):
        for x in range(bf.width):
            tile = bf.tile(x, y)
            overlay[f"{x},{y}"] = {
                "move_cost": reach.get((x, y)),
                "cover": tile.cover_value(),
                "elevation": tile.elevation,
                "hazards": tile.hazards(),
                "visible_to_unit": bf.line_of_sight(unit.pos, (x, y)),
                "under_enemy_threat": (x, y) in threats,
            }
    return overlay
