"""
epilogue — reusable "Region Complete" sequence.
================================================

After a region's finale, the world should be *shown* changing — not summarised
as statistics. This builds a reactive epilogue from remembered choices: each
narrative *thread* (a companion or a storyline) resolves into a positive or a
reduced outcome depending on how the player played, and the whole thing is
framed by the region's working title.

For the First Region the working title is **"The Frontier Endures"** and the
threads are Bram, the Hidden Pack, Corwin's investigation, Maeve's settlement,
Torren's forge work, Eleanor's diplomacy, Talos's leadership, and Ronan's
acceptance. Thread content is data (``data/epilogue_threads.json``); the
assembly rules are here and reusable for every future region.

Engine-agnostic: pure data + rules. No I/O.
"""

from __future__ import annotations

from typing import Dict, List


def build_epilogue(threads_content: dict, flags: Dict[str, bool]) -> dict:
    """Assemble the epilogue from ``flags`` (a map of condition -> bool).

    ``threads_content`` shape::

        {
          "title": "The Frontier Endures",
          "region": "The Frontier",
          "threads": [
            {"id","subject","flag","positive","reduced"}, ...
          ]
        }

    Each thread's ``flag`` is looked up in ``flags``; the matching ``positive``
    or ``reduced`` line is chosen. Output is plain data the presentation renders
    as an unfolding sequence (never a stat dump).
    """
    threads_out: List[dict] = []
    positives = 0
    for t in threads_content.get("threads", []):
        good = bool(flags.get(t.get("flag", ""), False))
        positives += 1 if good else 0
        threads_out.append({
            "id": t["id"],
            "subject": t.get("subject", t["id"]),
            "outcome": "hopeful" if good else "bittersweet",
            "text": t.get("positive" if good else "reduced", ""),
        })

    total = len(threads_out) or 1
    # A closing tone that reacts to how much of the world was left better off.
    ratio = positives / total
    if ratio >= 0.85:
        closing = threads_content.get("closing_bright", "")
    elif ratio >= 0.5:
        closing = threads_content.get("closing_mixed", "")
    else:
        closing = threads_content.get("closing_grim", "")

    return {
        "title": threads_content.get("title", "The Region Endures"),
        "region": threads_content.get("region", ""),
        "threads": threads_out,
        "positives": positives,
        "total": total,
        "closing": closing,
    }
