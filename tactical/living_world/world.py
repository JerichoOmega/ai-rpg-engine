"""
world — the LivingWorld aggregate + serializable snapshot.
==========================================================

:class:`LivingWorld` is the single, serializable home for a region's living
state: the status of every location (and its transition history — i.e. regional
memory), the deeds the world remembers (reputation), which dynamic events have
been resolved, which companion landmark moments / presence beats have played,
per-region progression, and any additional living-world flags. It composes the
reusable systems rather than expanding any legacy manager.

It round-trips through JSON (``to_state()``/``from_state()``) and is designed to
live under ``world_state["living_world"]`` — the existing save systems already
serialize ``world_state``, so persistence is a clean, additive extension of the
WorldState contract (no duplicate save path). See :mod:`persistence`.

Forward-compatible: ``from_state`` ignores unknown keys, so a save written by a
future version loads without crashing.

Engine-agnostic: pure data + rules. No I/O.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import content as _content
from . import reputation as _rep
from .region_state import LocationState

# Bump when the persisted LivingWorld shape changes in a non-additive way.
SCHEMA_VERSION = 1


@dataclass
class LivingWorld:
    """Aggregate living-world state for one or more regions."""

    locations: Dict[str, LocationState] = field(default_factory=dict)
    deeds: List[_rep.Deed] = field(default_factory=list)
    events_seen: List[str] = field(default_factory=list)
    landmarks_seen: List[str] = field(default_factory=list)   # "companion@location"
    presence_seen: List[str] = field(default_factory=list)    # "companion@location"
    progression: Dict[str, dict] = field(default_factory=dict)  # region_id -> {...}
    flags: Dict[str, Any] = field(default_factory=dict)
    version: int = SCHEMA_VERSION

    # -- construction -------------------------------------------------------
    @classmethod
    def from_content(cls, location_records: Optional[List[dict]] = None
                     ) -> "LivingWorld":
        """Build from a list of location dicts (defaults to Frontier content)."""
        records = (location_records if location_records is not None
                   else _content.locations())
        locs = {r["id"]: LocationState.from_state(r) for r in records}
        return cls(locations=locs)

    def ensure_locations(self, location_records: List[dict]) -> None:
        """Add any locations from ``location_records`` not already present.

        Lets a region's content be layered onto an existing (loaded) world
        without clobbering statuses/history already recorded for it.
        """
        for r in location_records:
            if r["id"] not in self.locations:
                self.locations[r["id"]] = LocationState.from_state(r)

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

    # -- events / moments ---------------------------------------------------
    def mark_event_seen(self, event_id: str) -> None:
        if event_id not in self.events_seen:
            self.events_seen.append(event_id)

    def mark_landmark_seen(self, companion: str, location_id: str) -> str:
        key = f"{companion}@{location_id}"
        if key not in self.landmarks_seen:
            self.landmarks_seen.append(key)
        return key

    def landmark_seen(self, companion: str, location_id: str) -> bool:
        return f"{companion}@{location_id}" in self.landmarks_seen

    def mark_presence_seen(self, companion: str, location_id: str) -> str:
        key = f"{companion}@{location_id}"
        if key not in self.presence_seen:
            self.presence_seen.append(key)
        return key

    # -- progression / flags ------------------------------------------------
    def set_progression(self, region_id: str, data: dict) -> None:
        self.progression[region_id] = dict(data)

    def region_progression(self, region_id: str) -> dict:
        return self.progression.get(region_id, {})

    def set_flag(self, name: str, value: Any = True) -> None:
        self.flags[name] = value

    def get_flag(self, name: str, default: Any = None) -> Any:
        return self.flags.get(name, default)

    # -- serialization ------------------------------------------------------
    def to_state(self) -> dict:
        return {
            "version": self.version,
            "locations": {k: v.to_state() for k, v in self.locations.items()},
            "deeds": [d.to_state() for d in self.deeds],
            "events_seen": list(self.events_seen),
            "landmarks_seen": list(self.landmarks_seen),
            "presence_seen": list(self.presence_seen),
            "progression": {k: dict(v) for k, v in self.progression.items()},
            "flags": dict(self.flags),
        }

    @classmethod
    def from_state(cls, data: dict) -> "LivingWorld":
        # Unknown/future keys are ignored (forward-compatible).
        data = data if isinstance(data, dict) else {}
        return cls(
            locations={k: LocationState.from_state(v)
                       for k, v in data.get("locations", {}).items()},
            deeds=[_rep.Deed.from_state(d) for d in data.get("deeds", [])],
            events_seen=list(data.get("events_seen", [])),
            landmarks_seen=list(data.get("landmarks_seen", [])),
            presence_seen=list(data.get("presence_seen", [])),
            progression={k: dict(v) for k, v in data.get("progression", {}).items()},
            flags=dict(data.get("flags", {})),
            version=int(data.get("version", SCHEMA_VERSION)),
        )
