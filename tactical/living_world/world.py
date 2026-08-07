"""
world — the LivingWorld aggregate + serializable snapshot.
==========================================================

:class:`LivingWorld` is the single, serializable home for a region's living
state: the status of every location, the deeds the world remembers, and which
dynamic events have already been seen. It composes the reusable systems rather
than expanding any legacy manager.

It round-trips through JSON (``to_state()``/``from_state()``) and is designed to
live under ``world_state["living_world"]`` when integrated with the main game —
additive and non-breaking.

Engine-agnostic: pure data + rules. No I/O.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from . import content as _content
from . import reputation as _rep
from .region_state import LocationState


@dataclass
class LivingWorld:
    """Aggregate living-world state for one or more regions."""

    locations: Dict[str, LocationState] = field(default_factory=dict)
    deeds: List[_rep.Deed] = field(default_factory=list)
    events_seen: List[str] = field(default_factory=list)

    # -- construction -------------------------------------------------------
    @classmethod
    def from_content(cls, location_records: Optional[List[dict]] = None
                     ) -> "LivingWorld":
        """Build from a list of location dicts (defaults to Frontier content)."""
        records = (location_records if location_records is not None
                   else _content.locations())
        locs = {r["id"]: LocationState.from_state(r) for r in records}
        return cls(locations=locs)

    # -- region-state helpers ----------------------------------------------
    def location(self, location_id: str) -> Optional[LocationState]:
        return self.locations.get(location_id)

    def add_location(self, loc: LocationState) -> None:
        self.locations[loc.id] = loc

    def set_status(self, location_id: str, status: str, reason: str = "") -> bool:
        loc = self.locations.get(location_id)
        if loc is None:
            return False
        return loc.set_status(status, reason)

    def locations_with_tag(self, tag: str) -> List[LocationState]:
        return [l for l in self.locations.values() if l.has_tag(tag)]

    def locations_in_region(self, region_id: str) -> List[LocationState]:
        return [l for l in self.locations.values() if l.region_id == region_id]

    # -- reputation helpers -------------------------------------------------
    def record_deed(self, deed: _rep.Deed) -> bool:
        return _rep.record_deed(self.deeds, deed)

    def deeds_at(self, location_id: str) -> List[_rep.Deed]:
        return _rep.deeds_for_location(self.deeds, location_id)

    # -- events -------------------------------------------------------------
    def mark_event_seen(self, event_id: str) -> None:
        if event_id not in self.events_seen:
            self.events_seen.append(event_id)

    # -- serialization ------------------------------------------------------
    def to_state(self) -> dict:
        return {
            "locations": {k: v.to_state() for k, v in self.locations.items()},
            "deeds": [d.to_state() for d in self.deeds],
            "events_seen": list(self.events_seen),
        }

    @classmethod
    def from_state(cls, data: dict) -> "LivingWorld":
        return cls(
            locations={k: LocationState.from_state(v)
                       for k, v in data.get("locations", {}).items()},
            deeds=[_rep.Deed.from_state(d) for d in data.get("deeds", [])],
            events_seen=list(data.get("events_seen", [])),
        )
