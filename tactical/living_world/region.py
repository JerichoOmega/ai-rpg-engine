"""
region — the reusable Region Content contract.
===============================================

A :class:`RegionContent` bundles everything the region-agnostic overlay needs to
bring *any* region to life, loaded from a **manifest** (data) that references the
region's content files. This removes all region-specific assumptions from code:
a future region ships a manifest + content JSON and inherits every system.

Manifest shape (``data/<region>_region.json``)::

    {
      "region_id": "the_frontier",
      "region_name": "The Frontier",
      "beat_map": { "<beat_id>": {"loc","tags":[...],"triggers":[...]}, ... },
      "content": {
        "locations": "<json name>", "presence": "...", "landmarks": "...",
        "banter": "...", "event_templates": "...", "environment": "...",
        "regional_memory": "...", "epilogue_threads": "..."
      }
    }

Engine-agnostic: pure data + rules. No I/O beyond loading its own content files.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from . import content as _content
from . import banter as _banter

_CONTENT_KEYS = [
    "locations", "presence", "landmarks", "banter", "event_templates",
    "environment", "regional_memory", "epilogue_threads",
]


@dataclass
class RegionContent:
    region_id: str
    region_name: str
    beat_map: Dict[str, dict]
    locations: List[dict]
    presence: Dict[str, list]
    landmarks: Dict[str, list]
    banter: Dict[str, list]
    event_templates: List[dict]
    environment: List[dict]
    regional_memory: Dict[str, dict]
    epilogue_threads: Dict[str, dict]

    @classmethod
    def from_manifest(cls, manifest_name: str) -> "RegionContent":
        m = _content.load(manifest_name)
        refs = m["content"]
        loaded = {k: _content.load(refs[k]) for k in _CONTENT_KEYS}
        return cls(
            region_id=m["region_id"],
            region_name=m["region_name"],
            beat_map=m.get("beat_map", {}),
            **loaded,
        )

    def validate(self) -> List[str]:
        """Return a list of content-contract errors (empty == valid)."""
        errors: List[str] = []
        if not self.region_id:
            errors.append("missing region_id")
        if not self.region_name:
            errors.append("missing region_name")
        if not self.beat_map:
            errors.append("empty beat_map")

        loc_ids = {l.get("id") for l in self.locations}
        if not loc_ids:
            errors.append("no locations defined")
        for bid, ctx in self.beat_map.items():
            loc = ctx.get("loc")
            if loc and loc not in loc_ids:
                errors.append(f"beat {bid!r} references unknown location {loc!r}")
            for t in ctx.get("triggers", []):
                if t not in _banter.TRIGGERS:
                    errors.append(f"beat {bid!r} uses unknown banter trigger {t!r}")

        for l in self.locations:
            if "id" not in l or "name" not in l:
                errors.append(f"location missing id/name: {l}")

        threads = self.epilogue_threads.get("threads")
        if not threads:
            errors.append("epilogue has no threads")
        else:
            for th in threads:
                if "flag" not in th or "id" not in th:
                    errors.append(f"epilogue thread missing id/flag: {th}")

        # every banter exchange must reference the trigger vocabulary
        for trig in self.banter:
            if trig not in _banter.TRIGGERS:
                errors.append(f"banter uses unknown trigger {trig!r}")

        return errors
