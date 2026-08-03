"""
Legacy Questline Architecture
=============================

Production-quality, reusable quest architecture for Elyndor.

This package is the vertical slice that establishes the foundation every
future Legacy Questline, main quest, side quest, and companion quest builds
on. It is organised into two layers:

    legacy.framework  -- reusable engine systems (quest runner, dialogue
                         trees, speech checks, companion affinity, split
                         party, timed objectives, multi-stage encounters,
                         environmental puzzles, living-world state,
                         reputation, and quest consequences).

    legacy.quests      -- the three approved Legacy Questlines expressed as
                         data (JSON) plus thin registration modules:
                             * The Debt Comes Due
                             * What the Forest Carries
                             * Eternal Forge

Nothing in this package invents canon. Where the approved design packages
leave a gap, the code marks it with a ``CANON_PENDING`` note rather than
inventing lore.

Integrates with the existing engine through ``world_state`` (single source
of truth) and ``event_bus`` (cross-module side effects) only.
"""

from legacy.framework import registry  # noqa: F401  (re-export for convenience)

__all__ = ["registry"]
