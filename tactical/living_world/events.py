"""
events — Dynamic World Event templates (reusable).
==================================================

Reusable, data-driven templates for the small, living moments that surface
during exploration: a merchant under attack, a lost child, a traveling healer,
Hidden Pack scouts, a wandering knight, corrupted wildlife, a refugee caravan,
a traveling storyteller, an abandoned campsite, an injured animal…

Templates are content (``data/event_templates.json``); the selection *rules*
live here. Future regions add templates to the JSON; the framework is unchanged.

Engine-agnostic: pure data + rules. No I/O. Determinism via an injected
``random.Random`` so tests and Godot replays agree.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional


def _matches(template: dict, tags: List[str], status: Optional[str]) -> bool:
    want = template.get("tags")
    if want and not (set(want) & set(tags)):
        return False
    only = template.get("only_status")
    if only and status is not None and status not in only:
        return False
    return True


def eligible(templates: List[dict], tags: List[str],
             status: Optional[str] = None) -> List[dict]:
    """Every template whose context tags overlap ``tags`` (and status fits)."""
    return [t for t in templates if _matches(t, tags, status)]


def draw_events(templates: List[dict], tags: List[str], count: int = 1,
                status: Optional[str] = None, exclude: Optional[List[str]] = None,
                rng: Optional[random.Random] = None) -> List[dict]:
    """Weighted, no-replacement sample of eligible event templates.

    ``exclude`` lets a caller avoid repeating events the player already saw.
    Deterministic for a given ``rng`` seed.
    """
    rng = rng or random.Random()
    exclude = set(exclude or [])
    pool = [t for t in eligible(templates, tags, status) if t["id"] not in exclude]
    chosen: List[dict] = []
    pool = list(pool)
    while pool and len(chosen) < count:
        weights = [max(1, int(t.get("weight", 1))) for t in pool]
        total = sum(weights)
        r = rng.uniform(0, total)
        upto = 0.0
        pick_i = len(pool) - 1
        for i, w in enumerate(weights):
            upto += w
            if r <= upto:
                pick_i = i
                break
        chosen.append(pool.pop(pick_i))
    return chosen


def instantiate(template: dict) -> dict:
    """Turn a template into a concrete event *state* the presentation renders.

    Plain data only: id, title, category, description, teaches, and the player
    choices (each with id/label). No behaviour — the caller resolves choices.
    """
    return {
        "id": template["id"],
        "title": template.get("title", template["id"]),
        "category": template.get("category", "encounter"),
        "description": template.get("description", ""),
        "teaches": template.get("teaches", ""),
        "choices": [dict(c) for c in template.get("choices", [])],
        "tags": list(template.get("tags", [])),
    }
