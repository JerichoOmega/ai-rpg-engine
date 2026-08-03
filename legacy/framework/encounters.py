"""
Multi-Stage Combat Encounters
=============================

Tactical combat exists to serve the story. This framework expresses the
*one memorable signature encounter* every Legacy Questline is required to
have, plus ordinary skirmishes, as **data**.

Two shapes, one entry point (:func:`run_encounter`):

* ``multi_stage`` -- escalating waves with per-wave threat. Reinforces
  companion roles and environmental storytelling.
* ``ritual_defense`` -- a round-based defence built on
  :mod:`legacy.framework.timed_objectives`; it ends on the **success
  condition** (ritual complete), never on enemy elimination.

Resolution is a transparent strength-vs-threat model so encounters can run
non-interactively in the harness and be reasoned about by designers.
"Party strength" rewards preparation (level, party size, companion
affinity, civilization standing) without ever requiring a specific party.
A lost wave/round is a **setback** (a flag, narrative pressure), not a
game-over -- the story always continues.

For studios that want the full turn-based engine, ``launch_interactive``
bridges to the existing ``combat.py`` loop; the data model here stays the
source of truth for structure and outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from world_state import world_state
from event_bus import emit
from .io import get_io
from . import companion_affinity, reputation, world_flags
from .timed_objectives import TimedObjective, OptionalObjective


@dataclass
class EncounterResult:
    id: str
    success: bool
    setbacks: int = 0
    optional_met: List[str] = field(default_factory=list)
    rounds: int = 0


def party_strength() -> int:
    """A single transparent number summarising how prepared the party is.

    Base 40, +5 per player level, +12 per companion, + affinity/8 across
    the party, + a small civilization-standing bonus. Never zero, so a solo
    player can always make progress (setbacks, not walls).
    """
    player = world_state.get("player", {})
    strength = 40 + int(player.get("level", 1)) * 5

    party = []
    try:
        from companion_manager import active_companions
        party = active_companions
    except Exception:
        pass
    strength += len(party) * 12

    for name, affinity in world_state.get("legacy", {}).get(
            "companion_affinity", {}).items():
        strength += int(affinity) // 8

    return strength


def _resolve_wave(name: str, threat: int, io) -> bool:
    """True if the wave is held. Uses the IO adapter's roll for RNG so the
    harness is deterministic."""
    roll = io.roll(40)
    total = party_strength() + roll
    held = total >= threat
    io.say(f"Wave '{name}': party {total} vs threat {threat} -> "
           + ("held" if held else "setback"))
    return held


def _run_multi_stage(spec: Dict[str, Any], io) -> EncounterResult:
    result = EncounterResult(spec["id"], success=True)
    for wave in spec.get("waves", []):
        emit("encounter_wave_started", encounter=spec["id"],
             wave=wave.get("name"))
        if wave.get("banter_context"):
            companion_affinity.trigger_banter(wave["banter_context"], io=io)
        held = _resolve_wave(wave.get("name", "wave"),
                             int(wave.get("threat", 60)), io)
        result.rounds += 1
        if not held:
            result.setbacks += 1
            if wave.get("setback_flag"):
                world_flags.set_flag(wave["setback_flag"], True)
    # The encounter as a whole "succeeds" (story continues) regardless of
    # setbacks; setbacks feed consequences.
    for flag in spec.get("on_complete_flags", []):
        world_flags.set_flag(flag, True)
    _finish(spec, result, io)
    return result


def _run_ritual_defense(spec: Dict[str, Any], io) -> EncounterResult:
    total_rounds = int(spec.get("rounds", 8))
    escalation = list(spec.get("escalation", []))

    # Base threat rises each round; optional objectives reward preparation.
    base_threat = int(spec.get("base_threat", 55))
    threat_step = int(spec.get("threat_step", 6))

    optionals = []
    for opt in spec.get("optional_objectives", []):
        req = opt.get("requires", {})

        def make_check(req):
            def check(round_number, ctx):
                # Met if a required companion is present at tier, OR party
                # strength clears a bar -- i.e. rewards preparation.
                companion = req.get("companion")
                tier = req.get("tier", "warming")
                if companion and companion_affinity.affinity_at_least(
                        companion, tier):
                    return True
                return party_strength() >= int(req.get("strength", 9999))
            return check

        optionals.append(OptionalObjective(
            id=opt["id"], description=opt.get("description", opt["id"]),
            check=make_check(req), flag_if_met=opt.get("flag_if_met")))

    result_holder = EncounterResult(spec["id"], success=False)

    def round_handler(round_number, ctx):
        threat = base_threat + (round_number - 1) * threat_step
        roll = io.roll(40)
        total = party_strength() + roll
        held = total >= threat
        ctx["last_held"] = held
        if not held:
            result_holder.setbacks += 1
        summary = (f"ritual guarded (party {total} vs threat {threat})"
                   if held else
                   f"ritual falters (party {total} vs threat {threat})")
        return {"failed_round": not held, "summary": summary}

    timed = TimedObjective(
        objective_id=spec["id"],
        total_rounds=total_rounds,
        escalation=escalation,
        optional=optionals,
        success_flag=spec.get("success_flag"),
        abort_on_fail=False,   # ritual defence never aborts: it endures.
    )
    timed_result = timed.run(round_handler, io=io)

    result_holder.success = timed_result.success
    result_holder.optional_met = timed_result.optional_met
    result_holder.rounds = timed_result.rounds_completed
    for flag in spec.get("on_complete_flags", []):
        world_flags.set_flag(flag, True)
    _finish(spec, result_holder, io)
    return result_holder


def _finish(spec: Dict[str, Any], result: EncounterResult, io) -> None:
    emit("encounter_completed", encounter=spec["id"],
         success=result.success, setbacks=result.setbacks,
         signature=spec.get("signature", False))
    tag = " (SIGNATURE)" if spec.get("signature") else ""
    io.say(f"[Encounter '{spec.get('name', spec['id'])}'{tag}] resolved -- "
           f"{result.setbacks} setback(s), "
           f"{len(result.optional_met)} optional objective(s).")


def run_encounter(spec: Dict[str, Any], io=None) -> EncounterResult:
    """Run an encounter from its data ``spec`` and return the result."""
    io = io or get_io()
    io.say(f"=== {spec.get('name', spec['id'])} ===")
    emit("encounter_started", encounter=spec["id"],
         type=spec.get("type"), signature=spec.get("signature", False))

    kind = spec.get("type", "multi_stage")
    if kind == "ritual_defense":
        return _run_ritual_defense(spec, io)
    return _run_multi_stage(spec, io)


def launch_interactive(enemy_specs: Optional[List[Dict]] = None) -> bool:
    """Bridge to the existing turn-based ``combat.py`` loop for studios that
    want full manual combat. Returns True on victory. Kept optional so the
    data model above remains the reusable source of truth."""
    from combat import quick_encounter
    return bool(quick_encounter())
