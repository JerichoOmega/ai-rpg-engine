"""
tactical.living_world — the Living World foundation for Elyndor
================================================================

An **additive, engine-agnostic** package that makes a region feel alive: it
remembers the player's actions, changes state over time, gives companions a
presence in the world, and closes a region with a reactive epilogue.

Design laws (see ``docs/architecture/LAYER_RULES.md``):

* **Pure rules + data only.** No ``print``/``input``, no engine imports, no
  UI/animation/audio/timing. Everything is returned as plain, JSON-shaped data
  or emitted as past-tense events. Presentation (terminal today, Godot later)
  decides how to show it.
* **State / Event / Intent** are the only channels
  (``docs/architecture/ENGINE_INTERFACES.md``). Every stateful object exposes
  ``to_state()``/``from_state()`` and round-trips through JSON.
* **Content is data, code is rules** (Layer Rule 4). The reusable *frameworks*
  live in this package's modules; the First Region's *content* lives in
  ``tactical/living_world/data/*.json`` and is loaded by :mod:`content`.

The systems (each a reusable framework, First-Region content supplied as data):

1. :mod:`region_state`  — Living Region System (Safe/Threatened/Recovering/
   Prosperous/Corrupted/Restored + transitions).
2. :mod:`reputation`    — Remembered deeds (no approval meter).
3. :mod:`events`        — Dynamic world-event templates for exploration.
4. :mod:`companions`    — Companion world presence + landmark moments.
5. :mod:`banter`        — Travel/camp banter framework.
6. :mod:`environment`   — Environmental storytelling details.
7. :mod:`memory`        — Regional memory (revisit evidence).
8. :mod:`epilogue`      — Reusable "Region Complete" sequence.
9. :mod:`world`         — :class:`LivingWorld` aggregate + serializable snapshot.
10. :mod:`frontier_overlay` — Binds the frameworks to the First Region.
11. :mod:`region_review`    — Runnable Region Completion Review report.
"""

from __future__ import annotations

from . import region_state, reputation, events, companions, banter
from . import environment, memory, epilogue, content
from .world import LivingWorld
from .region_state import LocationState, STATES

__all__ = [
    "LivingWorld",
    "LocationState",
    "STATES",
    "region_state",
    "reputation",
    "events",
    "companions",
    "banter",
    "environment",
    "memory",
    "epilogue",
    "content",
]
