"""
legacy.framework
================

Reusable engine systems for the Legacy Questline architecture. Import the
submodules you need; the two most common entry points are:

    from legacy.framework import registry          # register + play quests
    from legacy.framework.quest_framework import manager
"""

from . import (  # noqa: F401
    io,
    world_flags,
    reputation,
    companion_affinity,
    speech_checks,
    dialogue_trees,
    puzzles,
    timed_objectives,
    encounters,
    split_party,
    consequences,
    quest_framework,
)

__all__ = [
    "io", "world_flags", "reputation", "companion_affinity",
    "speech_checks", "dialogue_trees", "puzzles", "timed_objectives",
    "encounters", "split_party", "consequences", "quest_framework",
]
