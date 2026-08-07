"""
reputation — remembered deeds, not an approval meter (reusable).
================================================================

Settlements remember the *specific* things the player did — saving Bram,
cleansing corruption, helping refugees, restoring a village, protecting
travellers. There is **no single good/evil score**: reputation here is a list
of remembered actions that NPCs can reference naturally.

This complements (does not replace) the numeric ``world_state["factions"]``
reputation described in ``docs/systems/reputation.md`` — that stays for
faction politics; this is the *memory of deeds* layer a living region needs.

Engine-agnostic: pure data + rules. No I/O.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Reusable deed kinds. Content may add more; these cover the First Region.
SAVE = "save"
CLEANSE = "cleanse"
HELP_REFUGEES = "help_refugees"
RESTORE = "restore"
PROTECT_TRAVELLERS = "protect_travellers"
DEFEND = "defend"


@dataclass
class Deed:
    """One remembered thing the player did.

    ``npc_line`` is the presentation-neutral sentence an NPC can say when they
    reference the deed ("You're the one who pulled the lost wolf from the
    ravine..."). The engine renders it; the rules just supply it.
    """

    id: str
    title: str
    kind: str
    summary: str
    npc_line: str = ""
    location_id: str = ""
    region_id: str = ""

    def to_state(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "kind": self.kind,
            "summary": self.summary,
            "npc_line": self.npc_line,
            "location_id": self.location_id,
            "region_id": self.region_id,
        }

    @classmethod
    def from_state(cls, data: dict) -> "Deed":
        return cls(
            id=data["id"],
            title=data.get("title", data["id"]),
            kind=data.get("kind", ""),
            summary=data.get("summary", ""),
            npc_line=data.get("npc_line", ""),
            location_id=data.get("location_id", ""),
            region_id=data.get("region_id", ""),
        )


def record_deed(deeds: List[Deed], deed: Deed) -> bool:
    """Append ``deed`` to ``deeds`` (idempotent by id). Returns True if added."""
    if any(d.id == deed.id for d in deeds):
        return False
    deeds.append(deed)
    return True


def deeds_for_location(deeds: List[Deed], location_id: str) -> List[Deed]:
    return [d for d in deeds if d.location_id == location_id]


def deeds_for_region(deeds: List[Deed], region_id: str) -> List[Deed]:
    return [d for d in deeds if d.region_id == region_id]


def npc_references(deeds: List[Deed], location_id: Optional[str] = None,
                   region_id: Optional[str] = None) -> List[str]:
    """The sentences NPCs can use to reference remembered deeds.

    Scoped to a location and/or region when given; otherwise every deed's line.
    """
    pool = list(deeds)
    if location_id is not None:
        pool = [d for d in pool if d.location_id == location_id]
    if region_id is not None:
        pool = [d for d in pool if d.region_id == region_id]
    return [d.npc_line for d in pool if d.npc_line]
