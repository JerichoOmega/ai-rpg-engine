"""
environment — Environmental storytelling (reusable).
====================================================

Before a word of dialogue, the player should already sense that *something
happened here*: tracks, an abandoned camp, a ruined wagon, broken weapons,
damaged buildings, a memorial, a journal, a grave, a shrine.

Corwin frequently reads a detail everyone else overlooks — so each detail
template can carry a ``corwin_insight`` the framework surfaces when he is in
the party.

Details are content (``data/environment.json``); the selection rules live here.

Engine-agnostic: pure data + rules. No I/O. Deterministic via injected rng.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional


def eligible(details: List[dict], tags: List[str]) -> List[dict]:
    out = []
    for d in details:
        want = d.get("tags", [])
        if not want or (set(want) & set(tags)):
            out.append(d)
    return out


def details_for(details: List[dict], tags: List[str], count: int = 1,
                party: Optional[List[str]] = None,
                rng: Optional[random.Random] = None) -> List[dict]:
    """Sample environmental details for the current context.

    If Corwin is in ``party`` and a detail has a ``corwin_insight``, the insight
    is attached so presentation can show what he notices.
    """
    rng = rng or random.Random()
    party = party or []
    pool = eligible(details, tags)
    rng.shuffle(pool)
    corwin_here = any(p == "Corwin" for p in party)
    out: List[dict] = []
    for d in pool[:max(0, count)]:
        item = {
            "id": d["id"],
            "kind": d.get("kind", "detail"),
            "description": d.get("description", ""),
            "tags": list(d.get("tags", [])),
        }
        insight = d.get("corwin_insight")
        if corwin_here and insight:
            item["corwin_insight"] = insight
        out.append(item)
    return out
