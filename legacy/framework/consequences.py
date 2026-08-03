"""
Quest Consequence Framework
===========================

The bridge between a finished quest and a permanently changed world. A
:class:`ConsequenceSet` is a declarative list of world changes that are
applied once, when a quest resolves. It reads the *branch flags* the quest
recorded during play, so the same quest can produce different worlds.

Consequence kinds (all data-driven, all reusable):

* ``flag``          -- set a Living-World flag (NPC dialogue, schedules,
                       merchants, patrols, refugee populations, travel
                       safety, companion dialogue all key off these).
* ``counter``       -- adjust a Living-World counter (refugees settled,
                       volunteers remaining, infrastructure restored...).
* ``standing`` /
  ``relationship`` /
  ``reputation``    -- civilization / faction shifts.
* ``future_hook``   -- register an *approved* hook for later content. Any
                       hook that would touch intentionally-unrevealed future
                       story is written with a ``CANON_PENDING`` marker and
                       left inert (a flag only), never surfaced to the
                       player.

Each consequence may be gated by ``requires`` (a flag that must be truthy)
so branch-specific outcomes are expressed cleanly in JSON.
"""

from __future__ import annotations

from typing import Any, Dict, List

from event_bus import emit
from . import world_flags, reputation


def _requirement_met(consequence: Dict[str, Any]) -> bool:
    requires = consequence.get("requires")
    if not requires:
        return True
    if isinstance(requires, str):
        return world_flags.has_flag(requires)
    # dict form: {"flag": "...", "equals": value}
    value = world_flags.get_flag(requires["flag"])
    return value == requires.get("equals", True)


def apply_consequences(quest_id: str, consequences: List[Dict[str, Any]],
                       io=None) -> List[str]:
    """Apply every eligible consequence and return a log of what changed."""
    applied: List[str] = []
    for consequence in consequences:
        if not _requirement_met(consequence):
            continue
        kind = consequence.get("type")

        if kind == "flag":
            world_flags.set_flag(consequence["name"],
                                 consequence.get("value", True), silent=True)
            applied.append(f"flag {consequence['name']}="
                           f"{consequence.get('value', True)}")

        elif kind == "counter":
            world_flags.adjust_counter(consequence["name"],
                                       int(consequence["amount"]))
            applied.append(f"counter {consequence['name']} "
                           f"{consequence['amount']:+d}")

        elif kind == "standing":
            reputation.adjust_standing(consequence["civ"],
                                       int(consequence["amount"]))
            applied.append(f"standing {consequence['civ']} "
                           f"{consequence['amount']:+d}")

        elif kind == "relationship":
            reputation.adjust_relationship(
                consequence["civ_a"], consequence["civ_b"],
                int(consequence["amount"]))
            applied.append(f"relationship {consequence['civ_a']}<->"
                           f"{consequence['civ_b']} "
                           f"{consequence['amount']:+d}")

        elif kind == "reputation":
            reputation.adjust_reputation(consequence["faction"],
                                         int(consequence["amount"]))
            applied.append(f"reputation {consequence['faction']} "
                           f"{consequence['amount']:+d}")

        elif kind == "future_hook":
            # Register an approved hook as an inert flag. If the design note
            # flags it as unrevealed future content, keep it CANON_PENDING
            # and never surface it to the player.
            hook_flag = f"hook_{consequence['name']}"
            world_flags.set_flag(hook_flag, True, silent=True)
            applied.append(f"future_hook {consequence['name']}"
                           + (" [CANON_PENDING]"
                              if consequence.get("canon_pending") else ""))

    emit("quest_consequences_applied", quest_id=quest_id, changes=applied)
    if applied:
        print(f"\n=== LIVING WORLD UPDATED ({quest_id}) ===")
        for line in applied:
            print(f"  - {line}")
    return applied
