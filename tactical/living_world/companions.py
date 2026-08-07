"""
companions — Companion world presence + landmark moments (reusable).
====================================================================

Every companion naturally interacts with the world as the party moves through
it: Talos advises villagers, Eleanor blesses shrines, Maeve treats the wounded,
Corwin identifies corruption, Ragash's animals draw the children, Ronan reads
tracks, Torren examines damaged stonework.

Presence lines are keyed by **context tags** (``settlement``, ``shrine``,
``ruins``, ``forest`` …) so they compose with the region-state tags. Content is
data (``data/companion_presence.json`` / ``data/companion_landmarks.json``); the
selection rules live here.

Engine-agnostic: pure data + rules. No I/O.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional


def presence_for(catalogue: dict, companion: str, tags: List[str]) -> List[dict]:
    """Every presence beat a companion has whose contexts overlap ``tags``.

    Returns plain data: ``[{companion, kind, line, contexts}]``.
    """
    out: List[dict] = []
    for entry in catalogue.get(companion, []):
        contexts = entry.get("contexts", [])
        if not contexts or (set(contexts) & set(tags)):
            out.append({
                "companion": companion,
                "kind": entry.get("kind", "presence"),
                "line": entry.get("line", ""),
                "contexts": list(contexts),
            })
    return out


def presence_here(catalogue: dict, party: List[str], tags: List[str],
                  per_companion: int = 1,
                  rng: Optional[random.Random] = None) -> List[dict]:
    """Presence beats for everyone in ``party`` that fits the current context.

    At most ``per_companion`` beats each, chosen deterministically from ``rng``.
    """
    rng = rng or random.Random()
    beats: List[dict] = []
    for name in party:
        options = presence_for(catalogue, name, tags)
        if not options:
            continue
        rng.shuffle(options)
        beats.extend(options[:max(0, per_companion)])
    return beats


def landmark_moment(landmarks: dict, companion: str,
                    tags: List[str]) -> Optional[dict]:
    """A quiet, optional character moment at an important location.

    Returns the first landmark moment whose required tag is present, else None.
    """
    for entry in landmarks.get(companion, []):
        req = entry.get("tags", [])
        if not req or (set(req) & set(tags)):
            return {
                "companion": companion,
                "line": entry.get("line", ""),
                "tags": list(req),
                "optional": True,
            }
    return None


def landmark_moments_here(landmarks: dict, party: List[str],
                          tags: List[str]) -> List[dict]:
    out: List[dict] = []
    for name in party:
        m = landmark_moment(landmarks, name, tags)
        if m:
            out.append(m)
    return out
