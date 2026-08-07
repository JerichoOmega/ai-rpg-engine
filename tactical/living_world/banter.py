"""
banter — Companion travel/camp banter framework (reusable).
===========================================================

Party conversations triggered by what is happening around them: weather,
entering towns, rivers, forests, caves, ruins, victories, defeats, camping,
boss arenas, and important discoveries. The goal is to make the party feel
alive between the set-pieces.

Exchanges are content (``data/banter.json``), keyed by trigger. Each exchange
lists its participants and an ordered set of lines; an exchange is only
eligible when *all* its participants are in the party. Selection rules live
here.

Engine-agnostic: pure data + rules. No I/O. Deterministic via injected rng.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional

# The reusable trigger vocabulary. Content may key any of these.
TRIGGERS: List[str] = [
    "weather", "enter_town", "river", "forest", "cave", "ruins",
    "victory", "defeat", "camping", "boss_arena", "discovery",
]


def eligible_exchanges(catalogue: dict, trigger: str,
                       party: List[str]) -> List[dict]:
    """Exchanges for ``trigger`` whose participants are all present."""
    party_set = set(party)
    out = []
    for ex in catalogue.get(trigger, []):
        participants = ex.get("participants", [])
        if all(p in party_set for p in participants):
            out.append(ex)
    return out


def banter_for(catalogue: dict, trigger: str, party: List[str],
               rng: Optional[random.Random] = None) -> Optional[dict]:
    """One eligible exchange for the trigger, or None.

    Returns plain data: ``{trigger, participants, lines:[{speaker,text}]}``.
    """
    rng = rng or random.Random()
    options = eligible_exchanges(catalogue, trigger, party)
    if not options:
        return None
    ex = options[rng.randrange(len(options))]
    return {
        "trigger": trigger,
        "participants": list(ex.get("participants", [])),
        "lines": [dict(l) for l in ex.get("lines", [])],
    }
