"""
Developer Tools
===============

Permanent developer utilities for *all* Legacy Questlines -- not throwaway
test code. They let a developer:

* jump straight to any quest stage,
* set / inspect companion affinity,
* toggle / inspect Living-World flags and counters,
* simulate speech-check odds without playing,
* run a combat encounter (or the signature encounter) in isolation,
* seat a debug party so gated content can be exercised,
* print a full snapshot of the Legacy world-state.

Usage from a REPL or the in-game debug menu::

    from legacy import dev_tools as dt
    dt.seat_party(["talos", "corwin"], affinity=60)
    dt.jump("eternal_forge", "great_lift")
    dt.simulate_speech("insight", "hard", prep=["forge_oath_understood"])
"""

from __future__ import annotations

from typing import Dict, List, Optional

from world_state import world_state
from legacy.framework import (world_flags, companion_affinity, reputation,
                              speech_checks, encounters)
from legacy.framework.quest_framework import manager
from legacy.framework.io import ScriptedIO, InteractiveIO, set_io


# ---------------------------------------------------------------------------
# Party / affinity
# ---------------------------------------------------------------------------
def seat_party(names: List[str], affinity: int = 50) -> None:
    """Place ``names`` in the party (persisted + live roster) and set their
    affinity, so gated/optional content can be exercised in isolation."""
    world_state.setdefault("companions", {}).setdefault("party", [])
    party = world_state["companions"]["party"]
    for name in names:
        if name not in party:
            party.append(name)
        companion_affinity.set_affinity(name, affinity)
    try:
        from companion_manager import active_companions, COMPANIONS
        for name in names:
            template = COMPANIONS.get(name, {"role": name})
            entry = dict(template)
            entry["name"] = name
            if not any(c.get("name") == name for c in active_companions):
                active_companions.append(entry)
    except Exception:
        pass
    print(f"[dev] Seated party: {names} @ affinity {affinity}")


def set_affinity(companion: str, value: int) -> None:
    companion_affinity.set_affinity(companion, value)
    print(f"[dev] {companion} affinity = {value}")


# ---------------------------------------------------------------------------
# Flags / counters
# ---------------------------------------------------------------------------
def toggle(flag: str) -> None:
    value = world_flags.toggle_flag(flag)
    print(f"[dev] flag {flag} = {value}")


def set_flag(flag: str, value=True) -> None:
    world_flags.set_flag(flag, value)


def counter(name: str, amount: int) -> None:
    world_flags.adjust_counter(name, amount)


# ---------------------------------------------------------------------------
# Speech-check simulation (odds only, no roll)
# ---------------------------------------------------------------------------
def simulate_speech(skill: str, difficulty: str = "medium",
                    prep: Optional[List[str]] = None,
                    companion: Optional[str] = None,
                    tier: str = "warming",
                    civ: Optional[str] = None) -> float:
    """Print and return the computed success probability for a speech check
    with the given parameters, using current world-state."""
    check = speech_checks.SpeechCheck(
        id="dev.sim", skill=skill, difficulty=difficulty,
        preparation_flags=prep or [],
        companion_insight={"companion": companion, "tier": tier}
        if companion else None,
        civilization=civ,
    )
    result = speech_checks.compute_probability(check)
    print(f"[dev] {skill}/{difficulty} -> {result.probability:.0%}")
    for source, value in result.contributions.items():
        print(f"        {source}: {value:+.2f}")
    return result.probability


# ---------------------------------------------------------------------------
# Encounters
# ---------------------------------------------------------------------------
def run_encounter(spec: Dict) -> None:
    """Run an arbitrary encounter spec in isolation (interactive)."""
    set_io(InteractiveIO())
    encounters.run_encounter(spec)


def party_strength() -> int:
    strength = encounters.party_strength()
    print(f"[dev] party strength = {strength}")
    return strength


# ---------------------------------------------------------------------------
# Quest jumping
# ---------------------------------------------------------------------------
def jump(quest_id: str, stage_id: str, scripted: bool = False) -> str:
    """Play ``quest_id`` starting from ``stage_id``. Interactive by default;
    ``scripted=True`` auto-advances with default choices for a quick dry run.
    """
    io = ScriptedIO(verbose=True) if scripted else InteractiveIO()
    previous = set_io(io)
    try:
        return manager.jump_to_stage(quest_id, stage_id, io=io)
    finally:
        set_io(previous)


def stages(quest_id: str) -> List[str]:
    quest = manager.get(quest_id)
    order = quest.stage_order() if quest else []
    print(f"[dev] {quest_id} stages: {order}")
    return order


# ---------------------------------------------------------------------------
# Snapshot
# ---------------------------------------------------------------------------
def snapshot() -> None:
    print("\n===== LEGACY DEV SNAPSHOT =====")
    for quest in manager.all():
        print(f"\nQuest {quest.id}: {manager.status(quest.id)['state']} "
              f"(stage {manager.status(quest.id)['current_stage']})")
    world_flags.show_living_world()
    companion_affinity.show_affinity()
    reputation.show_civilizations()
