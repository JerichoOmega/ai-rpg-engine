"""
memory — Regional Memory: revisit evidence (reusable).
======================================================

When the player returns to a place, the world shows evidence of what they did:
villagers rebuilding, children playing again, fields restored, wildlife
returning, new memorials, shops reopening — or, if things went badly, the
opposite.

Change descriptors are content, keyed by region status
(``data/regional_memory.json``). Given a location's *current* status (and,
optionally, remembered deeds), this returns the concrete "what changed" beats a
returning player should see **before any dialogue begins**.

Engine-agnostic: pure data + rules. No I/O. Deterministic via injected rng.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional

from . import reputation as rep
from .region_state import LocationState


def changes_for_status(memory_content: dict, status: str,
                       count: int = 3,
                       rng: Optional[random.Random] = None) -> List[str]:
    """The visible changes appropriate to a location in ``status``."""
    rng = rng or random.Random()
    entry = memory_content.get(status, {})
    pool = list(entry.get("changes", []))
    rng.shuffle(pool)
    return pool[:max(0, count)]


def revisit_report(memory_content: dict, location: LocationState,
                   deeds: Optional[List[rep.Deed]] = None,
                   count: int = 3,
                   rng: Optional[random.Random] = None) -> dict:
    """A full engine-neutral revisit snapshot for one location.

    ``prompt`` is the "before dialogue" framing line for the status; ``changes``
    are the concrete evidence; ``remembered`` are NPC references to deeds done
    here (so a returning player is greeted by their own history).
    """
    rng = rng or random.Random()
    entry = memory_content.get(location.status, {})
    remembered = (rep.npc_references(deeds, location_id=location.id)
                  if deeds else [])
    return {
        "location_id": location.id,
        "name": location.name,
        "status": location.status,
        "mood": location.mood(),
        "prompt": entry.get("prompt", ""),
        "changes": changes_for_status(memory_content, location.status,
                                      count=count, rng=rng),
        "remembered": remembered,
    }
