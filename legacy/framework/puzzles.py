"""
Environmental Puzzle Framework
==============================

Reusable multi-step puzzles for exploration and infrastructure
restoration -- the Eternal Forge's engineering puzzles (Great Lift,
restoring the foundry's systems) are the first users, but the framework is
generic.

A :class:`Puzzle` is an ordered list of :class:`PuzzleStep` s. Each step
offers several actions; exactly one is correct. Wrong actions never
hard-fail -- they cost nothing but a hint and can be retried -- because
progression must be driven by investigation, not punished by it. Companion
insight and world flags can reveal the correct action outright (preparation
reward).

Solving a puzzle can set living-world flags (e.g. ``great_lift_restored``)
that downstream stages and consequences read.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from world_state import world_state
from event_bus import emit
from .io import get_io, Option
from . import companion_affinity, world_flags


@dataclass
class PuzzleStep:
    id: str
    prompt: str
    actions: List[Dict[str, str]]          # [{key,label}]
    correct: str                            # key of the correct action
    hint: str = ""
    # Companion who can reveal the answer if present at/above ``tier``.
    reveal_companion: Optional[str] = None
    reveal_tier: str = "warming"
    reveal_line: str = ""


@dataclass
class Puzzle:
    id: str
    title: str
    description: str
    steps: List[PuzzleStep]
    on_solve_flags: List[str] = field(default_factory=list)


def _puzzle_store() -> Dict[str, Any]:
    legacy = world_state.setdefault("legacy", {})
    return legacy.setdefault("puzzles", {})


def solve_puzzle(puzzle: Puzzle, io=None) -> bool:
    """Run ``puzzle`` interactively/scripted. Always returns True (puzzles
    are completable); records the number of missteps for optional scoring
    and preparation feedback."""
    io = io or get_io()
    io.say(f"=== {puzzle.title} ===")
    if puzzle.description:
        io.say(puzzle.description)

    missteps = 0
    for step in puzzle.steps:
        # Companion reveal (preparation reward): surface the answer.
        revealed = False
        if step.reveal_companion and companion_affinity.affinity_at_least(
                step.reveal_companion, step.reveal_tier):
            if step.reveal_line:
                io.say(step.reveal_line, speaker=step.reveal_companion.title())
            revealed = True

        while True:
            options = [Option(a["key"], a["label"]) for a in step.actions]
            chosen = io.choose(
                step.prompt, options,
                key=f"{puzzle.id}.{step.id}",
                # Under scripting/auto play, default to the correct action so
                # puzzles resolve; interactive players pick freely.
                default=step.correct,
            )
            if chosen == step.correct:
                io.say("The mechanism responds correctly.")
                break
            missteps += 1
            hint = step.hint or "That did not work. Study it again."
            io.say(hint)
            if revealed:
                # If the answer was revealed we still let them retry, but do
                # not loop forever in scripted mode.
                io.say(f"({step.reveal_companion.title()} already showed the "
                       f"correct approach.)")

    for flag in puzzle.on_solve_flags:
        world_flags.set_flag(flag, True)

    _puzzle_store()[puzzle.id] = {"solved": True, "missteps": missteps}
    emit("puzzle_solved", puzzle_id=puzzle.id, missteps=missteps)
    io.say(f"[{puzzle.title}] solved"
           + (f" cleanly." if missteps == 0 else f" ({missteps} missteps)."))
    return True


def from_dict(data: Dict[str, Any]) -> Puzzle:
    steps = [
        PuzzleStep(
            id=s["id"],
            prompt=s["prompt"],
            actions=list(s["actions"]),
            correct=s["correct"],
            hint=s.get("hint", ""),
            reveal_companion=s.get("reveal_companion"),
            reveal_tier=s.get("reveal_tier", "warming"),
            reveal_line=s.get("reveal_line", ""),
        )
        for s in data["steps"]
    ]
    return Puzzle(
        id=data["id"],
        title=data.get("title", data["id"]),
        description=data.get("description", ""),
        steps=steps,
        on_solve_flags=list(data.get("on_solve_flags", [])),
    )
