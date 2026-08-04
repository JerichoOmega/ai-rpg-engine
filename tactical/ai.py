"""
Enemy AI (shared rules, no hidden advantages)
=============================================

The AI evaluates cover, elevation, threats, hazards, LOS and range using the
**same** battlefield/inspection functions the player's UI uses -- it reads no
hidden state and gets no bonuses. Behaviour is tuned per enemy by the
blueprint's ``ai_profile`` (target selection, hazard avoidance, cover use),
so a mindless Skeleton and a cautious Goblin share one code path with
different data.
"""

from __future__ import annotations

from . import actions
from .inspection import compute_hit_chance, chebyshev, threat_map
from .tiles import COVER_VALUE


def _select_target(engine, unit):
    targets = [e for e in engine.enemies_of(unit) if e.alive]
    if not targets:
        return None
    mode = unit.ai_profile.get("target_selection", "nearest")
    if mode == "lowest_armor":
        return min(targets, key=lambda t: (getattr(t, "armor", 0),
                                           chebyshev(unit.pos, t.pos)))
    if mode == "lowest_health":
        return min(targets, key=lambda t: (t.hp, chebyshev(unit.pos, t.pos)))
    return min(targets, key=lambda t: chebyshev(unit.pos, t.pos))


def _score_tile(engine, unit, xy, target, threats) -> float:
    bf = engine.bf
    score = 0.0
    los = bf.line_of_sight(xy, target.pos)
    in_range = chebyshev(xy, target.pos) <= unit.attack_range
    if los and in_range:
        atk_elev = bf.tile(*xy).elevation
        def_elev = bf.tile(*target.pos).elevation
        cover_pen = bf.cover_penalty(target.pos, xy)
        elev = 0.10 if atk_elev > def_elev else (-0.10 if atk_elev < def_elev else 0)
        score += 50 + (unit.accuracy - cover_pen + elev) * 20
        # Ranged units like to keep their distance.
        if unit.ai_profile.get("preferred_range") == "ranged":
            score += min(chebyshev(xy, target.pos), unit.attack_range)
    else:
        score += 20 - chebyshev(xy, target.pos)
    if unit.ai_profile.get("uses_cover", True):
        score += COVER_VALUE.get(bf.directional_cover(xy, target.pos), 0) * 20
    score += bf.tile(*xy).elevation * 3
    if any(h in unit.ai_profile.get("avoids", []) for h in bf.tile(*xy).hazards()):
        score -= 30
    if bf.tile(*xy).hazards():
        score -= 5
    if xy in threats:
        score -= 8
    return score


def take_turn(engine, unit) -> None:
    if not unit.alive:
        return
    target = _select_target(engine, unit)
    if target is None:
        return

    threats = threat_map(engine, unit)
    reachable = engine.bf.reachable(unit.pos, unit.move)
    reachable[unit.pos] = 0

    best_xy = max(reachable, key=lambda xy: _score_tile(
        engine, unit, xy, target, threats))
    if best_xy != unit.pos:
        actions.move(engine, unit, best_xy)

    if unit.alive:
        if compute_hit_chance(engine, unit, target)["chance"] > 0 and \
                unit.ap >= actions.ATTACK_AP:
            actions.attack(engine, unit, target)
        elif unit.ap > 0:
            actions.prepare(engine, unit)
