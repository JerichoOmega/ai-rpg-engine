"""
Speech Check Framework
======================

Speech checks appear naturally throughout every quest. They *change
conversations, unlock alternate solutions, affect trust and optional
rewards* -- but by design they **do not hard-fail the main quest**.

Supported skills (design authority):

    persuasion | insight | diplomacy | intimidation | cultural

A check's success chance is computed transparently from:

* a base tied to the check ``difficulty`` (an easy/medium/hard band),
* the player's relevant aptitude (derived from class + level),
* **preparation** -- world flags gathered earlier in the quest,
* **companion insight** -- an eligible companion at sufficient affinity,
* **reputation / standing** with the relevant civilization.

Preparation and companions *stack the odds*; they never replace the check.
The final roll is delegated to the active :class:`~legacy.framework.io`
adapter, so the harness can force outcomes to validate both branches.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from world_state import world_state
from event_bus import emit
from .io import get_io
from . import companion_affinity, reputation, world_flags

SKILLS = ("persuasion", "insight", "diplomacy", "intimidation", "cultural")

# difficulty band -> base success chance (before modifiers)
DIFFICULTY_BASE = {
    "trivial": 0.85,
    "easy": 0.70,
    "medium": 0.55,
    "hard": 0.40,
    "daunting": 0.25,
}

# Rough per-class aptitude. Kept data-light and non-canon: it only nudges
# odds and never gates content.
CLASS_APTITUDE = {
    "Warrior": {"intimidation": 0.15, "persuasion": 0.05},
    "Mage": {"insight": 0.15, "cultural": 0.10},
    "Rogue": {"persuasion": 0.10, "insight": 0.10},
    "Cleric": {"diplomacy": 0.15, "insight": 0.10},
}


@dataclass
class SpeechCheck:
    """A single speech check embedded in a conversation."""

    id: str
    skill: str
    difficulty: str = "medium"
    # World flags that, if set, improve the odds (preparation reward).
    preparation_flags: List[str] = field(default_factory=list)
    # (companion, tier) that grants an insight bonus if present.
    companion_insight: Optional[Dict[str, str]] = None
    # Civilization whose standing modifies the odds.
    civilization: Optional[str] = None
    # Human-readable description for logs/UI.
    prompt: str = ""


@dataclass
class SpeechCheckResult:
    check_id: str
    skill: str
    success: bool
    probability: float
    contributions: Dict[str, float]


def _player_aptitude(skill: str) -> float:
    player_class = world_state.get("player", {}).get("class", "Warrior")
    level = int(world_state.get("player", {}).get("level", 1))
    base = CLASS_APTITUDE.get(player_class, {}).get(skill, 0.0)
    # A gentle level ramp so a prepared, higher-level party is favoured.
    return base + min(0.15, (level - 1) * 0.02)


def compute_probability(check: SpeechCheck) -> SpeechCheckResult:
    """Compute (but do not roll) the success probability, returning a full
    breakdown of contributions for transparency and debugging."""
    contributions: Dict[str, float] = {}

    base = DIFFICULTY_BASE.get(check.difficulty, 0.55)
    contributions["base"] = base

    aptitude = _player_aptitude(check.skill)
    if aptitude:
        contributions["aptitude"] = aptitude

    prep = sum(0.10 for flag in check.preparation_flags
               if world_flags.has_flag(flag))
    if prep:
        contributions["preparation"] = prep

    if check.companion_insight:
        companion = check.companion_insight.get("companion")
        tier = check.companion_insight.get("tier", "warming")
        if companion and companion_affinity.affinity_at_least(companion, tier):
            contributions["companion_insight"] = 0.15

    if check.civilization:
        standing = reputation.get_standing(check.civilization)
        if standing:
            contributions["standing"] = max(-0.2, min(0.2, standing / 200))

    probability = max(0.05, min(0.97, sum(contributions.values())))
    return SpeechCheckResult(check.id, check.skill, False, probability,
                             contributions)


def resolve(check: SpeechCheck, io=None) -> SpeechCheckResult:
    """Roll the check through the active IO adapter and announce the result.

    Never raises and never fails a quest -- callers branch on
    ``result.success`` to grant *optional* benefits only.
    """
    io = io or get_io()
    result = compute_probability(check)
    result.success = io.speech_outcome(check.id, result.probability)

    label = check.skill.title()
    outcome = "SUCCESS" if result.success else "no effect"
    io.say(f"[{label} check -- {check.difficulty}] {outcome}")
    emit("speech_check_resolved", check_id=check.id, skill=check.skill,
         success=result.success, probability=result.probability)
    return result


def from_dict(data: Dict) -> SpeechCheck:
    """Build a :class:`SpeechCheck` from a quest JSON fragment."""
    return SpeechCheck(
        id=data["id"],
        skill=data.get("skill", "persuasion"),
        difficulty=data.get("difficulty", "medium"),
        preparation_flags=list(data.get("preparation_flags", [])),
        companion_insight=data.get("companion_insight"),
        civilization=data.get("civilization"),
        prompt=data.get("prompt", ""),
    )
