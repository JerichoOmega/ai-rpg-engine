"""
Companion Affinity Hooks & Banter
=================================

Companion philosophy (from the design authority): companions are **never
mandatory**. Affinity influences dialogue, insight, and optional outcomes
-- it never locks the player out of a main quest.

This module provides:

* **Affinity** -- a richer per-companion relationship layer stored under
  ``world_state["legacy"]["companion_affinity"]``. It complements (does not
  replace) the existing ``companion_manager`` loyalty stat.
* **Insight hooks** -- ``has_companion``/``affinity_at_least`` gates that
  quests use to *offer extra* content (better insight, alternate solutions)
  when the right companion is present and warmed up.
* **Banter** -- register context-keyed banter lines once; quests trigger
  them by context (location, beat, encounter). Reusable across all content.

Featured companions for the three approved quests: ``talos`` (Eternal Forge)
and ``corwin`` (What the Forest Carries). More can be registered freely.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional

from world_state import world_state
from event_bus import emit
from .io import get_io

# Affinity thresholds shared across quests so gating is consistent.
AFFINITY_TIERS = {
    "wary": 0,
    "warming": 25,
    "trusted": 50,
    "devoted": 80,
}


def _affinity_store() -> Dict[str, int]:
    legacy = world_state.setdefault("legacy", {})
    return legacy.setdefault("companion_affinity", {})


def _active_party_names() -> List[str]:
    """Best-effort list of companions currently in the party.

    Reads the live ``companion_manager`` roster and falls back to the
    persisted ``world_state["companions"]["party"]`` list.
    """
    names: List[str] = []
    try:
        from companion_manager import active_companions, COMPANIONS
        role_to_name = {c["role"]: n for n, c in COMPANIONS.items()}
        for companion in active_companions:
            names.append(companion.get("name")
                         or role_to_name.get(companion.get("role"),
                                              companion.get("role")))
    except Exception:
        pass
    for name in world_state.get("companions", {}).get("party", []):
        if name not in names:
            names.append(name)
    return names


# ---------------------------------------------------------------------------
# Affinity
# ---------------------------------------------------------------------------
def get_affinity(companion: str) -> int:
    return int(_affinity_store().get(companion, 0))


def set_affinity(companion: str, value: int) -> int:
    store = _affinity_store()
    store[companion] = max(0, min(100, int(value)))
    emit("companion_affinity_changed", companion=companion,
         affinity=store[companion])
    return store[companion]


def adjust_affinity(companion: str, amount: int) -> int:
    new_value = set_affinity(companion, get_affinity(companion) + amount)
    print(f"\n[Affinity] {companion.title()} affinity {new_value} "
          f"({affinity_tier(companion)})")
    return new_value


def affinity_tier(companion: str) -> str:
    value = get_affinity(companion)
    tier = "wary"
    for name, threshold in AFFINITY_TIERS.items():
        if value >= threshold:
            tier = name
    return tier


def affinity_at_least(companion: str, tier: str) -> bool:
    """True when ``companion`` is in the party AND at/above the given tier.

    This is the canonical gate quests use to *offer* optional content.
    Because it returns False (rather than raising) when the companion is
    absent, the main quest always remains completable.
    """
    if companion not in _active_party_names():
        return False
    return get_affinity(companion) >= AFFINITY_TIERS.get(tier, 999)


def has_companion(companion: str) -> bool:
    return companion in _active_party_names()


# ---------------------------------------------------------------------------
# Banter
# ---------------------------------------------------------------------------
# context key -> list of (companion, line) banter entries.
_banter_registry: Dict[str, List[Dict[str, str]]] = {}


def register_banter(context: str, companion: str, line: str) -> None:
    """Register a banter line for a context. Idempotent per (context, line)."""
    entries = _banter_registry.setdefault(context, [])
    if not any(e["companion"] == companion and e["line"] == line
               for e in entries):
        entries.append({"companion": companion, "line": line})


def trigger_banter(context: str, io=None, rng: Optional[random.Random] = None
                   ) -> Optional[Dict[str, str]]:
    """Speak one eligible banter line for ``context`` if a matching
    companion is present. Returns the entry spoken, or None."""
    io = io or get_io()
    entries = _banter_registry.get(context, [])
    party = set(_active_party_names())
    eligible = [e for e in entries if e["companion"] in party]
    if not eligible:
        return None
    chosen = (rng or random).choice(eligible)
    io.say(chosen["line"], speaker=chosen["companion"].title())
    return chosen


def show_affinity() -> None:
    print("\n=== COMPANION AFFINITY ===")
    store = _affinity_store()
    if not store:
        print("No affinity recorded yet.")
        return
    for companion in sorted(store):
        print(f"  {companion.title()}: {store[companion]} "
              f"({affinity_tier(companion)})")
