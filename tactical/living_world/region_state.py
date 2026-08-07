"""
region_state — the Living Region System (reusable).
====================================================

Every settlement, landmark and region carries a **status** describing how the
world currently feels there. Statuses change because of what the player does,
and each change is logged so the world can *remember*.

Engine-agnostic: pure data + rules. No I/O, no engine references.
Every object round-trips through JSON via ``to_state()``/``from_state()``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

# --- the six reusable statuses ---------------------------------------------
SAFE = "safe"
THREATENED = "threatened"
RECOVERING = "recovering"
PROSPEROUS = "prosperous"
CORRUPTED = "corrupted"
RESTORED = "restored"

STATES: List[str] = [SAFE, THREATENED, RECOVERING, PROSPEROUS, CORRUPTED, RESTORED]

# Intended narrative flow between statuses. Non-strict: the game may move a
# location to any valid status, but this table documents the natural arcs and
# lets a designer/QA check that a transition "makes sense".
TRANSITIONS: Dict[str, List[str]] = {
    SAFE: [THREATENED, PROSPEROUS, CORRUPTED],
    THREATENED: [CORRUPTED, RECOVERING, SAFE],
    CORRUPTED: [THREATENED, RECOVERING, RESTORED],
    RECOVERING: [RESTORED, PROSPEROUS, THREATENED],
    RESTORED: [PROSPEROUS, SAFE, THREATENED],
    PROSPEROUS: [SAFE, THREATENED, CORRUPTED],
}

# A short, presentation-neutral mood line per status (data, not rendering).
STATUS_MOOD: Dict[str, str] = {
    SAFE: "quiet and watchful, but unbroken",
    THREATENED: "tense; people glance at the tree line",
    RECOVERING: "bruised but mending, hands busy again",
    PROSPEROUS: "thriving, markets loud and full",
    CORRUPTED: "wrong; the air itself feels sick",
    RESTORED: "reborn — scarred, yet standing taller than before",
}


def is_valid_status(status: str) -> bool:
    return status in STATES


def is_natural_transition(old: str, new: str) -> bool:
    """True if ``old -> new`` follows the documented natural arc."""
    return new in TRANSITIONS.get(old, [])


@dataclass
class LocationState:
    """A single place the player can visit and change.

    ``kind`` is ``settlement`` | ``landmark`` | ``region``. ``tags`` are the
    engine-neutral context labels (e.g. ``forest``, ``shrine``, ``refugee_camp``)
    that companion presence, banter, events and environmental storytelling key
    off — so the same content frameworks work for any region.
    """

    id: str
    name: str
    kind: str = "settlement"
    status: str = SAFE
    tags: List[str] = field(default_factory=list)
    region_id: str = ""
    history: List[dict] = field(default_factory=list)  # [{from,to,reason}]

    def set_status(self, new_status: str, reason: str = "") -> bool:
        """Change status, logging the transition. Returns True if it changed.

        Raises ``ValueError`` on an unknown status so bad content fails fast.
        """
        if new_status not in STATES:
            raise ValueError(
                f"unknown region status {new_status!r}; "
                f"valid: {', '.join(STATES)}"
            )
        if new_status == self.status:
            return False
        self.history.append(
            {"from": self.status, "to": new_status, "reason": reason,
             "natural": is_natural_transition(self.status, new_status)}
        )
        self.status = new_status
        return True

    def mood(self) -> str:
        return STATUS_MOOD.get(self.status, "")

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags

    # -- serialization (round-trips through JSON) ---------------------------
    def to_state(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "status": self.status,
            "tags": list(self.tags),
            "region_id": self.region_id,
            "history": [dict(h) for h in self.history],
        }

    @classmethod
    def from_state(cls, data: dict) -> "LocationState":
        return cls(
            id=data["id"],
            name=data.get("name", data["id"]),
            kind=data.get("kind", "settlement"),
            status=data.get("status", SAFE),
            tags=list(data.get("tags", [])),
            region_id=data.get("region_id", ""),
            history=[dict(h) for h in data.get("history", [])],
        )
