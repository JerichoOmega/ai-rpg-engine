"""
Registry
========

The single place that wires the Legacy Questline content into the engine:

* ensures the ``world_state["legacy"]`` schema exists,
* seeds the known civilizations,
* loads and registers the three approved quests with the shared
  :data:`legacy.framework.quest_framework.manager`,
* registers their companion banter.

Adding a future Legacy Questline is a two-line change here plus one JSON
data file -- no engine code.
"""

from __future__ import annotations

from typing import List

from world_state import world_state
from .quest_framework import manager, Quest

_REGISTERED = False


def ensure_legacy_world_state() -> None:
    """Create the ``world_state["legacy"]`` namespace and civilization
    seeds if they are missing. Idempotent; safe to call repeatedly."""
    legacy = world_state.setdefault("legacy", {})
    for key in ("quests", "living_world", "companion_affinity",
                "civilizations", "split_party", "puzzles"):
        legacy.setdefault(key, {})

    from . import reputation
    for civ in reputation.KNOWN_CIVILIZATIONS:
        legacy["civilizations"].setdefault(civ, {"standing": 0,
                                                  "relations": {}})


def register_all() -> List[Quest]:
    """Import the quest modules, register their quests and banter, and
    return the registered quests. Idempotent."""
    global _REGISTERED
    ensure_legacy_world_state()

    # Connect Living-World flags to reusable world reactions (Phase 4).
    from . import living_world_reactions
    living_world_reactions.install()

    from legacy.quests import (debt_comes_due, what_the_forest_carries,
                               eternal_forge, the_jammed_mill)

    quests = []
    for module in (debt_comes_due, what_the_forest_carries, eternal_forge,
                   the_jammed_mill):
        quest = module.build()
        manager.register(quest)
        module.register_banter()
        quests.append(quest)

    _REGISTERED = True
    return quests


def is_registered() -> bool:
    return _REGISTERED


# Register on import so `import legacy` is enough to make the quests
# playable. Wrapped defensively so a content error never breaks engine
# start-up.
try:
    register_all()
except Exception as exc:  # pragma: no cover - defensive
    print(f"[legacy] quest registration deferred: {exc}")
