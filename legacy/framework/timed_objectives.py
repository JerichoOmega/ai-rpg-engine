"""
Timed Objective Framework
=========================

Round-based objectives that *escalate over time* and end on a condition
other than "kill everything". The signature user is "What the Forest
Carries": an eight-round ritual defence that ends when the ritual succeeds,
not when enemies are eliminated -- but the framework is generic and reused
by any beat that needs "hold/act for N escalating rounds".

Design contract:

* Progress is measured in **rounds**.
* Each round may **escalate** (a stronger threat, a new hazard).
* **Optional objectives** can be met for extra reward without being
  required.
* The objective ends when the **success condition** is reached (typically
  "all rounds survived / ritual complete"), independent of enemy count.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from event_bus import emit
from .io import get_io


@dataclass
class OptionalObjective:
    id: str
    description: str
    # Called each round with (round_number, context) -> bool met-this-round.
    check: Optional[Callable[[int, Dict], bool]] = None
    met: bool = False
    flag_if_met: Optional[str] = None


@dataclass
class TimedObjectiveResult:
    id: str
    success: bool
    rounds_completed: int
    total_rounds: int
    optional_met: List[str] = field(default_factory=list)
    log: List[str] = field(default_factory=list)


class TimedObjective:
    """A round-driven objective.

    ``round_handler(round_number, context)`` is invoked once per round and
    returns a dict that may contain ``{"failed_round": bool}`` and any data
    the optional-objective checks need. The objective *does not* abort on a
    failed round -- setbacks are narrative pressure, not a quest fail --
    unless ``abort_on_fail`` is explicitly set.
    """

    def __init__(self, objective_id: str, total_rounds: int,
                 escalation: Optional[List[str]] = None,
                 optional: Optional[List[OptionalObjective]] = None,
                 success_flag: Optional[str] = None,
                 abort_on_fail: bool = False):
        self.id = objective_id
        self.total_rounds = total_rounds
        self.escalation = escalation or []
        self.optional = optional or []
        self.success_flag = success_flag
        self.abort_on_fail = abort_on_fail

    def run(self, round_handler: Callable[[int, Dict], Dict],
            io=None, context: Optional[Dict] = None) -> TimedObjectiveResult:
        io = io or get_io()
        context = context if context is not None else {}
        result = TimedObjectiveResult(
            self.id, success=False, rounds_completed=0,
            total_rounds=self.total_rounds)

        for round_number in range(1, self.total_rounds + 1):
            escalation_note = (
                self.escalation[round_number - 1]
                if round_number - 1 < len(self.escalation) else "")
            io.say(f"-- Round {round_number}/{self.total_rounds} --"
                   + (f" {escalation_note}" if escalation_note else ""))

            outcome = round_handler(round_number, context) or {}
            result.rounds_completed = round_number
            result.log.append(outcome.get("summary", ""))

            for objective in self.optional:
                if not objective.met and objective.check \
                        and objective.check(round_number, context):
                    objective.met = True
                    result.optional_met.append(objective.id)
                    io.say(f"[Optional objective met] {objective.description}")

            if outcome.get("failed_round") and self.abort_on_fail:
                io.say("The objective is lost.")
                emit("timed_objective_failed", objective_id=self.id,
                     round=round_number)
                return result

        result.success = True
        if self.success_flag:
            from . import world_flags
            world_flags.set_flag(self.success_flag, True)
        for objective in self.optional:
            if objective.met and objective.flag_if_met:
                from . import world_flags
                world_flags.set_flag(objective.flag_if_met, True)

        emit("timed_objective_completed", objective_id=self.id,
             rounds=result.rounds_completed,
             optional_met=result.optional_met)
        io.say(f"[{self.id}] complete after {result.rounds_completed} rounds "
               f"({len(result.optional_met)} optional objectives met).")
        return result
