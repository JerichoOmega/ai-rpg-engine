"""
The Lost Howl — Final Encounter Playable Slice ("save, don't slay")
===================================================================

The climax of Ronan's companion quest [`The Lost Howl`] deliberately subverts the
boss fight. The party arrives believing it must **Defeat the Beast**. Partway in,
the **Hidden Pack Alpha** arrives and the objective flips to **Protect the Lost
Wolf until the Pack reaches him** — the victory condition becomes *saving*, not
*killing*.

This module is a headless, testable proof of that objective-swap: the *correct*
(compassionate) play rescues the Lost Wolf, while the naive "kill the boss" play
produces the tragic failure state. It is design/validation code — **no shared
gameplay systems are modified.**

Cast
----
* **The Lost Wolf (Bram)** — a young werewolf who awakened utterly alone; a
  panicked, dangerous, *non-evil* enemy. Killing him is the FAILURE state.
* **Ronan, Talos** — guardians who body-block and taunt to *subdue, not slay*.
* **Eleanor** — approaches with empty hands; never attacks (compassion is the
  intended solution, mirroring her canon scene).
* **The Alpha** — a Hidden Pack Warden who "arrives" mid-encounter and moves in to
  bring the Lost Wolf home. Reaching him = **rescue**.

Outcomes
--------
* ``"rescued"`` — the Alpha reaches a living Lost Wolf (the design-goal ending).
* ``"slain"``   — the Lost Wolf is killed (the tragic naive-play failure).
* ``"party_wiped"`` / ``"timeout"`` — the protectors fall / time runs out.

Proof (see ``scripts/lost_howl_report.py`` and ``backend/tests/test_lost_howl_encounter.py``):
compassion → ``rescued``; murder-hobo → ``slain``.
"""

from __future__ import annotations

import random
from typing import List, Optional, Tuple

from .battlefield import Battlefield
from .entities import Combatant
from .engine import CombatEngine, CombatContext
from . import actions
from . import abilities_engine as ae
from .inspection import chebyshev
from . import showcase

BATTLEFIELD_ID = "lost_howl_climax"
ALPHA_ARRIVES_ROUND = 4          # the objective flips when the Alpha arrives


def build_battlefield() -> Battlefield:
    bf = Battlefield(12, 7, battlefield_id=BATTLEFIELD_ID)
    bf.tile(8, 1).add_object("boulder")
    bf.tile(8, 5).add_object("boulder")
    return bf


def build_combatants() -> List[Combatant]:
    ronan = Combatant("Ronan", "guardian", "player", 6, 3)
    talos = Combatant("Talos", "guardian", "player", 6, 4)
    eleanor = Combatant("Eleanor", "mage", "player", 4, 3)
    alpha = Combatant("The Alpha", "guardian", "player", 0, 3)   # arrives later
    for h in (ronan, talos, eleanor, alpha):
        h.items = ["healing_potion"]
    lost = Combatant("The Lost Wolf", "brute", "enemy", 9, 3)
    lost.max_hp = 70
    lost.hp = 70
    lost.attack_damage = 9
    return [ronan, talos, eleanor, alpha, lost]


def build_encounter(rng: Optional[random.Random] = None) -> CombatEngine:
    return CombatEngine(build_battlefield(), build_combatants(),
                        context=CombatContext("location", "lost_howl_climax"),
                        rng=rng or random.Random(11))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _find(engine, name):
    return next((u for u in engine.combatants if u.name == name), None)


def _lost_wolf(engine):
    return _find(engine, "The Lost Wolf")


def _alpha(engine):
    return _find(engine, "The Alpha")


def _protectors(engine):
    return [u for u in engine.combatants
            if u.team == "player" and u.name != "The Alpha"]


# ---------------------------------------------------------------------------
# Controllers
# ---------------------------------------------------------------------------
def compassion_controller(engine, unit) -> None:
    """Subdue, don't slay. Guardians taunt and body-block; Eleanor walks toward
    the wolf with empty hands; the Alpha closes in to bring him home. NOBODY
    attacks the Lost Wolf."""
    ae.start_of_turn(engine, unit)
    lost = _lost_wolf(engine)
    if lost is None or not lost.alive:
        return
    showcase._sip_if_hurt(engine, unit)

    if unit.name == "The Alpha":
        if engine.round >= ALPHA_ARRIVES_ROUND and chebyshev(unit.pos, lost.pos) > 1:
            showcase._move_toward(engine, unit, lost.pos)
        elif unit.ap > 0:
            actions.prepare(engine, unit)
        return

    if unit.cls == "guardian":                       # Ronan / Talos: hold the line
        if chebyshev(unit.pos, lost.pos) > 1:
            showcase._move_toward(engine, unit, lost.pos)
        if unit.ap > 0:
            ae.use_skill(engine, unit, "taunt", target=lost)   # draw the panic onto us
        if unit.ap > 0:
            actions.prepare(engine, unit)            # brace — never attack
        return

    # Eleanor: approach with compassion, never attack.
    if chebyshev(unit.pos, lost.pos) > 2:
        showcase._move_toward(engine, unit, lost.pos)
    if unit.ap > 0:
        actions.prepare(engine, unit)


def murderhobo_controller(engine, unit) -> None:
    """The naive 'defeat the beast' read: everyone focuses the Lost Wolf. This
    reaches the FAILURE state — the frightened wolf is cut down before the Pack
    can save him."""
    ae.start_of_turn(engine, unit)
    lost = _lost_wolf(engine)
    if lost is None or not lost.alive:
        return
    if unit.name == "The Alpha":
        if engine.round >= ALPHA_ARRIVES_ROUND and chebyshev(unit.pos, lost.pos) > 1:
            showcase._move_toward(engine, unit, lost.pos)
        return
    if unit.cls == "mage":
        if not showcase._shoot(engine, unit, lost, "firebolt"):
            showcase._shoot(engine, unit, lost)
        return
    if chebyshev(unit.pos, lost.pos) > 1:
        showcase._move_toward(engine, unit, lost.pos)
    while unit.ap > 0 and chebyshev(unit.pos, lost.pos) <= 1 and lost.alive:
        if not actions.attack(engine, unit, lost):
            break


# ---------------------------------------------------------------------------
# Custom resolution — objective swap
# ---------------------------------------------------------------------------
def _outcome(engine) -> Optional[str]:
    lost, alpha = _lost_wolf(engine), _alpha(engine)
    if lost is None or not lost.alive:
        return "slain"
    if engine.round >= ALPHA_ARRIVES_ROUND and alpha.alive \
            and chebyshev(alpha.pos, lost.pos) <= 1:
        return "rescued"
    if not any(p.alive for p in _protectors(engine)):
        return "party_wiped"
    return None


def resolve(controller, seed: int = 11, max_rounds: int = 16) -> Tuple[str, CombatEngine]:
    eng = build_encounter(rng=random.Random(seed))
    eng.start()
    outcome = None
    while eng.round < max_rounds:
        eng.round += 1
        eng.log.append(f"--- Round {eng.round} ---")
        if eng.round == ALPHA_ARRIVES_ROUND:
            eng.log.append("The Hidden Pack Alpha arrives! Objective: protect the Lost Wolf.")
        eng.take_team_turn("player", controller=controller)
        outcome = _outcome(eng)
        if outcome:
            break
        eng.take_team_turn("enemy")
        outcome = _outcome(eng)
        if outcome:
            break
        eng.environment_reacts()
        outcome = _outcome(eng)
        if outcome:
            break
    outcome = outcome or "timeout"
    eng.end()
    eng.log.append(f"Encounter ends: {outcome} (round {eng.round}).")
    return outcome, eng


def outcome_rate(controller, target: str, seeds: int = 20, max_rounds: int = 16) -> float:
    hits = sum(1 for s in range(seeds) if resolve(controller, seed=s, max_rounds=max_rounds)[0] == target)
    return hits / seeds


def objective_manifest() -> dict:
    return {
        "initial_objective": "Defeat the Beast",
        "twist": "The Hidden Pack Alpha arrives (round %d)." % ALPHA_ARRIVES_ROUND,
        "swapped_objective": "Protect the Lost Wolf until the Pack reaches him.",
        "design_goal": "The climax rewards SAVING, not killing. Cutting the Lost "
                       "Wolf down is the tragic failure state, not the win.",
    }
