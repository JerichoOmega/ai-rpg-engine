"""
The Corruption Avatar — Regional Finale Set-Piece ("break the wards first")
===========================================================================

The climactic battle the whole Frontier chapter builds toward. After Ronan's
emotional climax (**The Lost Howl**) and Corwin's investigation exposes the
source, the full party confronts a **manifestation of The Corruption** at the
heart of the blight.

Its true name, origin and deeper lore are **deliberately reserved** (canonical
``_TBD_``): the party defeats *this manifestation* and cleanses the region, but
the underlying source may reach beyond a single encounter. This module fully
defines its **tactical/mechanical role**, not its identity.

The tactical lesson (new to the slice)
--------------------------------------
Do **not** tunnel the boss. The Avatar is *warded*: while any **Corruption
Anchor** (wardstone) stands, damage to the Avatar is nullified — its blight
knits shut as fast as you cut it. You must **break the anchors first**; only
then does the Avatar become vulnerable and **enrage** for the true fight.

* ``siege_controller``   — anchors first, then the exposed Avatar  → **cleansed**
* ``tunnel_controller``  — ignore the anchors, focus the Avatar    → **held / overwhelmed**

This mirrors the Sundered Span (positioning), Forge Stand (use the environment)
and Lost Howl (save, don't slay) proofs: a distinct, measurable "right vs naive"
gap — no shared gameplay systems are modified; it reuses the canonical engine
and the reference party.

Outcomes
--------
* ``"cleansed"``    — the Avatar's manifestation is destroyed (design-goal win).
* ``"held"``        — time runs out with the Avatar still warded (the naive read).
* ``"overwhelmed"`` — the party falls.
"""

from __future__ import annotations

import random
from typing import List, Optional, Tuple

from .battlefield import Battlefield
from .entities import Combatant
from .engine import CombatEngine, CombatContext
from . import enemies, actions
from . import abilities_engine as ae
from .inspection import chebyshev
from . import showcase

BATTLEFIELD_ID = "corruption_avatar_finale"

AVATAR_ID = "corruption_avatar"
ANCHOR_ID = "corruption_anchor"
ANCHOR_SPOTS = [(8, 1), (8, 7), (12, 4)]   # a triangle warding the Avatar
AVATAR_SPOT = (10, 4)


# ---------------------------------------------------------------------------
# Battlefield — a blighted clearing at the heart of the woods
# ---------------------------------------------------------------------------
def build_battlefield() -> Battlefield:
    bf = Battlefield(14, 9, battlefield_id=BATTLEFIELD_ID)
    for xy in [(3, 2), (4, 6), (2, 4)]:                 # approach woods (cover)
        bf.set_terrain(*xy, "forest")
        bf.tile(*xy).add_object("pine_tree")
    for xy in [(6, 0), (6, 8)]:                          # flank boulders
        bf.tile(*xy).add_object("boulder")
    for xy in [(3, 4), (4, 4)]:                          # a low rise to fight from
        bf.set_terrain(*xy, "hill")
    return bf


# ---------------------------------------------------------------------------
# Combatants
# ---------------------------------------------------------------------------
def build_combatants(preparedness: int = 0) -> List[Combatant]:
    party = showcase.build_party()
    for i, hero in enumerate(party):                     # deploy on the west edge
        hero.x, hero.y = 1, 2 + i
    # Preparedness earned from good Frontier choices = extra sustain going in.
    if preparedness > 0:
        for hero in party:
            hero.items = list(getattr(hero, "items", [])) + ["healing_potion"] * preparedness

    avatar = enemies.spawn_enemy(AVATAR_ID, *AVATAR_SPOT)
    anchors = [enemies.spawn_enemy(ANCHOR_ID, x, y) for (x, y) in ANCHOR_SPOTS]
    # Poor preparedness (rushed/uninformed) = tougher wardstones, still winnable.
    if preparedness < 0:
        for a in anchors:
            a.max_hp += 8 * (-preparedness)
            a.hp = a.max_hp
    return party + anchors + [avatar]


def build_encounter(rng: Optional[random.Random] = None,
                    preparedness: int = 0) -> CombatEngine:
    return CombatEngine(build_battlefield(), build_combatants(preparedness),
                        context=CombatContext("location", "corruption_avatar_finale"),
                        rng=rng or random.Random(23))


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------
def _avatar(engine):
    return next((u for u in engine.combatants
                 if getattr(u, "blueprint_id", None) == AVATAR_ID), None)


def _anchors(engine):
    return [u for u in engine.combatants
            if getattr(u, "blueprint_id", None) == ANCHOR_ID and u.alive]


def _party(engine):
    return [u for u in engine.combatants if u.team == "player"]


# ---------------------------------------------------------------------------
# Ward mechanic + phases
# ---------------------------------------------------------------------------
def _apply_ward(engine) -> None:
    """While any anchor stands, the Avatar's wounds knit shut (damage nullified)."""
    avatar = _avatar(engine)
    if avatar and avatar.alive and _anchors(engine):
        if avatar.hp < avatar.max_hp:
            engine.log.append("The wardstones pulse — the Avatar's wounds knit shut.")
        avatar.hp = avatar.max_hp


def _enrage_if_exposed(engine, state: dict) -> None:
    """The first instant the last anchor falls, the Avatar is exposed and enrages."""
    avatar = _avatar(engine)
    if avatar and avatar.alive and not _anchors(engine) and not state.get("enraged"):
        state["enraged"] = True
        avatar.max_ap += 1
        avatar.damage_min += 4
        avatar.damage_max += 4
        avatar.attack_damage = (avatar.damage_min + avatar.damage_max) // 2
        engine.log.append("The wards shatter — the Corruption Avatar is EXPOSED and enrages!")


# ---------------------------------------------------------------------------
# Controllers
# ---------------------------------------------------------------------------
def _engage(engine, unit, tgt) -> None:
    if tgt is None or not tgt.alive:
        return
    showcase._sip_if_hurt(engine, unit)
    cls = unit.cls
    if cls == "ranger":
        if chebyshev(unit.pos, tgt.pos) > unit.attack_range:
            showcase._move_toward(engine, unit, tgt.pos)
        if "marked" not in tgt.statuses:
            ae.use_skill(engine, unit, "hunters_mark", target=tgt)
        if not showcase._shoot(engine, unit, tgt, "aimed_shot"):
            showcase._shoot(engine, unit, tgt)
        return
    if cls == "mage":
        if not showcase._shoot(engine, unit, tgt, "firebolt"):
            showcase._move_toward(engine, unit, tgt.pos)
            showcase._shoot(engine, unit, tgt, "firebolt") or showcase._shoot(engine, unit, tgt)
        return
    if cls == "rogue":
        if chebyshev(unit.pos, tgt.pos) > 1:
            showcase._move_toward(engine, unit, tgt.pos)
        if chebyshev(unit.pos, tgt.pos) <= 1 and not ae.use_skill(engine, unit, "backstab", target=tgt):
            pass
        while unit.ap > 0 and chebyshev(unit.pos, tgt.pos) <= 1 and tgt.alive:
            if not actions.attack(engine, unit, tgt):
                break
        return
    # guardian / melee
    if chebyshev(unit.pos, tgt.pos) > 1:
        showcase._move_toward(engine, unit, tgt.pos)
    while unit.ap > 0 and chebyshev(unit.pos, tgt.pos) <= 1 and tgt.alive:
        if not actions.attack(engine, unit, tgt):
            break
    if unit.ap > 0:
        actions.prepare(engine, unit)


def _nearest_anchor(engine, unit):
    live = _anchors(engine)
    if not live:
        return None
    return sorted(live, key=lambda a: chebyshev(unit.pos, a.pos))[0]


def siege_controller(engine, unit) -> None:
    """The intended plan: break the wardstones first, then the exposed Avatar."""
    ae.start_of_turn(engine, unit)
    tgt = _nearest_anchor(engine, unit) or _avatar(engine)
    _engage(engine, unit, tgt)


def tunnel_controller(engine, unit) -> None:
    """The naive read: everyone hammers the Avatar and ignores the wardstones —
    the blight simply knits shut. Reaches the 'held' failure state."""
    ae.start_of_turn(engine, unit)
    _engage(engine, unit, _avatar(engine))


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------
def _outcome(engine) -> Optional[str]:
    avatar = _avatar(engine)
    if avatar is None or not avatar.alive:
        return "cleansed"
    if not any(p.alive for p in _party(engine)):
        return "overwhelmed"
    return None


def resolve(controller, seed: int = 23, max_rounds: int = 30,
            preparedness: int = 0) -> Tuple[str, CombatEngine]:
    eng = build_encounter(rng=random.Random(seed), preparedness=preparedness)
    eng.start()
    state: dict = {"enraged": False}
    outcome = None
    _apply_ward(eng)
    while eng.round < max_rounds:
        eng.round += 1
        eng.log.append(f"--- Round {eng.round} ---")
        eng.take_team_turn("player", controller=controller)
        _enrage_if_exposed(eng, state)
        _apply_ward(eng)
        outcome = _outcome(eng)
        if outcome:
            break
        eng.take_team_turn("enemy")
        _apply_ward(eng)
        outcome = _outcome(eng)
        if outcome:
            break
        eng.environment_reacts()
        _apply_ward(eng)
        outcome = _outcome(eng)
        if outcome:
            break
    outcome = outcome or "held"
    eng.end()
    eng.log.append(f"Finale ends: {outcome} (round {eng.round}).")
    return outcome, eng


def outcome_rate(controller, target: str, seeds: int = 20,
                 max_rounds: int = 30, preparedness: int = 0) -> float:
    hits = sum(1 for s in range(seeds)
               if resolve(controller, seed=s, max_rounds=max_rounds,
                          preparedness=preparedness)[0] == target)
    return hits / seeds


def objective_manifest() -> dict:
    return {
        "name": "The Corruption Avatar (identity: _TBD_)",
        "framing": "A manifestation of The Corruption at the heart of the blight — "
                   "an ancient force, not a named individual.",
        "mechanic": "WARDED: while any Corruption Anchor stands, damage to the "
                    "Avatar is nullified.",
        "phases": ["Phase 1 — break the wardstones (Avatar invulnerable).",
                   "Phase 2 — the wards shatter; the Avatar is exposed and enrages."],
        "lesson": "Don't tunnel the boss — dismantle what sustains it first.",
        "foreshadowing": "Cleansing this manifestation frees the Frontier, but the "
                         "true source of the blight is left unresolved (_TBD_).",
        "outcomes": {"cleansed": "manifestation destroyed (win)",
                     "held": "time runs out, still warded (naive read)",
                     "overwhelmed": "the party falls"},
    }
