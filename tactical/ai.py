"""
Enemy AI (shared rules, no hidden advantages)
=============================================

The AI evaluates cover, elevation, threats, hazards, LOS and range using the
**same** battlefield/inspection functions the player's UI uses -- it reads no
hidden state and gets no bonuses. Behaviour is tuned per enemy by a reusable
**AI profile** (``tactical/data/ai_profiles.json``): a Skirmisher kites, a
Defender holds ground, a Brute charges, an Ambusher seeks flanks, and a wounded
Coward flees -- all through one code path driven by data flags.

Profile flags honoured here:
``target_selection`` (nearest|lowest_health|lowest_armor), ``preferred_range``
(melee|ranged), ``charges``, ``kites``, ``hold_position``, ``prefers_flank``,
``fearless``, ``uses_cover``, ``avoids``, ``will_retreat`` / ``flees_when_low``
(+ ``flee_threshold``).
"""

from __future__ import annotations

from . import actions
from . import abilities_engine as abilities
from .facing import relative_arc
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
    p = unit.ai_profile
    score = 0.0
    los = bf.line_of_sight(xy, target.pos)
    in_range = chebyshev(xy, target.pos) <= unit.attack_range
    if los and in_range:
        atk_elev = bf.tile(*xy).elevation
        def_elev = bf.tile(*target.pos).elevation
        cover_pen = bf.cover_penalty(target.pos, xy)
        elev = 0.10 if atk_elev > def_elev else (-0.10 if atk_elev < def_elev else 0)
        score += 50 + (unit.accuracy - cover_pen + elev) * 20
        if p.get("preferred_range") == "ranged":
            score += min(chebyshev(xy, target.pos), unit.attack_range)
        if p.get("prefers_flank") and relative_arc(target, xy) in ("side", "rear"):
            score += 18
    else:
        score += (30 - chebyshev(xy, target.pos) * 2) if p.get("charges") \
            else (20 - chebyshev(xy, target.pos))
    if p.get("uses_cover", True):
        score += COVER_VALUE.get(bf.directional_cover(xy, target.pos), 0) * 20
    score += bf.tile(*xy).elevation * 3
    if p.get("kites"):
        nearest = min((chebyshev(xy, e.pos) for e in engine.enemies_of(unit)
                       if e.alive), default=9)
        if nearest <= 1:
            score -= 14
    if p.get("hold_position"):
        score -= chebyshev(xy, unit.pos) * 4
    if any(h in p.get("avoids", []) for h in bf.tile(*xy).hazards()):
        score -= 30
    if bf.tile(*xy).hazards():
        score -= 5
    if xy in threats and not p.get("fearless"):
        score -= 8
    return score


def _retreat(engine, unit, target, threats, reachable) -> None:
    """Wounded self-preservers back away from the nearest foe, then brace or
    snipe if a shot is still open."""
    living = [e for e in engine.enemies_of(unit) if e.alive]

    def safety(xy):
        dist = min((chebyshev(xy, e.pos) for e in living), default=0)
        return dist - (6 if xy in threats else 0) \
            - (20 if engine.bf.tile(*xy).hazards() else 0)

    retreat_xy = max(reachable, key=safety)
    if retreat_xy != unit.pos:
        actions.move(engine, unit, retreat_xy)
    if unit.alive and unit.ap > 0:
        if unit.ai_profile.get("preferred_range") == "ranged" and \
                compute_hit_chance(engine, unit, target)["chance"] > 0:
            actions.attack(engine, unit, target)
        else:
            actions.prepare(engine, unit)


def _update_memory(engine, unit, target):
    """Maintain a short tactical context so enemies act intentionally rather
    than recomputing from scratch each turn."""
    mem = unit.ai_memory
    allies = [a for a in engine.allies_of(unit) if a is not unit]
    team = [a for a in engine.combatants if a.team == unit.team]
    alive_team = [a for a in team if a.alive]
    mem["commander_nearby"] = any(
        a.alive and a.ai_profile.get("coordinates")
        and chebyshev(unit.pos, a.pos) <= 4 for a in allies)
    frac = len(alive_team) / max(1, len(team))
    mem["morale"] = "low" if frac <= 0.34 else ("high" if frac >= 1.0 else "normal")
    mem["currently_flanking"] = (
        engine.bf.line_of_sight(unit.pos, target.pos)
        and relative_arc(target, unit.pos) in ("side", "rear"))
    return mem


def _resolve_target(engine, unit):
    """Sticky targeting: keep chasing the remembered target unless it dies or
    a much weaker target appears (for health-focused hunters)."""
    mem = unit.ai_memory
    prev_id = mem.get("target_id")
    target = None
    if prev_id:
        target = next((e for e in engine.enemies_of(unit)
                       if e.alive and e.id == prev_id), None)
    if target is None:
        target = _select_target(engine, unit)
        mem["turns_chasing"] = 0
    else:
        fresh = _select_target(engine, unit)
        if (fresh and fresh.id != target.id
                and unit.ai_profile.get("target_selection") == "lowest_health"
                and fresh.hp < target.hp * 0.5):
            target = fresh
            mem["turns_chasing"] = 0
    if target is not None:
        mem["target_id"] = target.id
    return target


def take_turn(engine, unit) -> None:
    if not unit.alive:
        return
    abilities.start_of_turn(engine, unit)
    if not unit.alive:
        return
    target = _resolve_target(engine, unit)
    if target is None:
        return
    p = unit.ai_profile
    mem = _update_memory(engine, unit, target)

    threats = threat_map(engine, unit)
    reachable = engine.bf.reachable(unit.pos, unit.move)
    reachable[unit.pos] = 0

    # Self-preservation, modulated by morale + a nearby commander.
    hp_ratio = unit.hp / max(1, unit.max_hp)
    threshold = p.get("flee_threshold", 0.3)
    if mem.get("commander_nearby"):
        threshold *= 0.5                       # braver while led
    if mem.get("morale") == "low":
        threshold += 0.15                      # breaks more easily when routed
    if (not p.get("fearless")
            and (p.get("flees_when_low") or p.get("will_retreat"))
            and hp_ratio < threshold):
        _retreat(engine, unit, target, threats, reachable)
        return

    # Profile-driven abilities come BEFORE movement so support/casters/
    # summoners can act from a good position (a healer shouldn't charge past
    # the ally it means to heal). Attack abilities that need to close range are
    # re-evaluated after the move.
    used_ability = False
    if unit.alive and unit.ap > 0:
        choice = abilities.choose_ability(engine, unit, target)
        if choice is not None:
            aid, kwargs = choice
            used_ability = abilities.use_skill(engine, unit, aid, **kwargs)

    best_xy = max(reachable, key=lambda xy: _score_tile(
        engine, unit, xy, target, threats))
    if best_xy != unit.pos:
        actions.move(engine, unit, best_xy)

    if unit.alive and unit.ap > 0 and not used_ability:
        choice = abilities.choose_ability(engine, unit, target)
        if choice is not None:
            aid, kwargs = choice
            used_ability = abilities.use_skill(engine, unit, aid, **kwargs)

    in_range = compute_hit_chance(engine, unit, target)["chance"] > 0
    if unit.alive:
        if in_range and unit.ap >= actions.ATTACK_AP:
            actions.attack(engine, unit, target)
        elif unit.ap > 0 and not used_ability:
            actions.prepare(engine, unit)
    mem["turns_chasing"] = 0 if in_range else mem.get("turns_chasing", 0) + 1
