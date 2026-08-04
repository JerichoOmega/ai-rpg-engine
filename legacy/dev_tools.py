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


# ---------------------------------------------------------------------------
# Objectives / quest state
# ---------------------------------------------------------------------------
def complete_objective(quest_id: str, objective_id: str) -> None:
    manager.complete_objective(quest_id, objective_id)
    print(f"[dev] {quest_id}: objective '{objective_id}' completed")


def fail_objective(quest_id: str, objective_id: str) -> None:
    manager.fail_objective(quest_id, objective_id)
    print(f"[dev] {quest_id}: objective '{objective_id}' failed")


def fail_quest(quest_id: str) -> None:
    manager.fail_quest(quest_id)
    print(f"[dev] {quest_id}: quest failed")


def set_stage(quest_id: str, stage_id: str) -> None:
    """Set the persisted current stage without playing (jump-in point)."""
    manager.set_stage(quest_id, stage_id)
    print(f"[dev] {quest_id}: current stage set to '{stage_id}'")


def export_quest_state(quest_id: str, path: Optional[str] = None) -> Dict:
    """Return (and optionally write) a JSON snapshot of a quest's state."""
    import json
    state = manager.export_state(quest_id)
    if path:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2)
        print(f"[dev] exported {quest_id} state -> {path}")
    else:
        print(json.dumps(state, indent=2))
    return state


# ---------------------------------------------------------------------------
# Reputation / civilizations
# ---------------------------------------------------------------------------
def change_reputation(faction: str, amount: int) -> None:
    reputation.adjust_reputation(faction, amount)
    print(f"[dev] reputation {faction} {amount:+d}")


def set_standing(civ: str, amount: int) -> None:
    reputation.adjust_standing(civ, amount)


def set_relationship(civ_a: str, civ_b: str, amount: int) -> None:
    reputation.adjust_relationship(civ_a, civ_b, amount)


# ---------------------------------------------------------------------------
# Living World
# ---------------------------------------------------------------------------
def force_world_update() -> None:
    """Force a full recompute of Living-World reactions and print them."""
    from legacy.framework import living_world_reactions
    living_world_reactions.recompute()
    living_world_reactions.show_reactions()


def show_reactions() -> None:
    from legacy.framework import living_world_reactions
    living_world_reactions.show_reactions()


# ---------------------------------------------------------------------------
# NPCs / cinematics
# ---------------------------------------------------------------------------
def spawn_npc(name: str, **attributes) -> Dict:
    """Register a quest-specific NPC in the engine roster (best-effort).

    Falls back to a Living-World record if npc_manager is unavailable, so a
    developer always has a spawned marker to work with.
    """
    entry = {"name": name, **attributes}
    try:
        import npc_manager
        registry_dict = getattr(npc_manager, "NPCS", None)
        if isinstance(registry_dict, dict):
            registry_dict[name] = entry
            print(f"[dev] spawned NPC '{name}' in npc_manager.NPCS")
            return entry
    except Exception:
        pass
    world_state.setdefault("legacy", {}).setdefault(
        "debug_npcs", {})[name] = entry
    print(f"[dev] spawned NPC '{name}' (legacy debug registry)")
    return entry


def skip_cinematic(quest_id: str, to_stage: str) -> None:
    """Skip narrative and jump the persisted state to a later stage.

    Cinematics in this engine are ``narrate`` steps; skipping is simply
    advancing the current stage past them without replaying narration.
    """
    manager.set_stage(quest_id, to_stage)
    print(f"[dev] {quest_id}: skipped ahead to '{to_stage}'")
