"""
npcs — Region NPC content model + selection rules (reusable).
=============================================================

The smallest reusable model that makes a region feel *inhabited by people*.
NPC **static definitions are data** (``data/<region>_npcs.json``, loaded via
:class:`~tactical.living_world.region.RegionContent`); the selection *rules*
live here.

Philosophy (matches the Living World foundation):

* **No approval meter, no morality score.** An NPC's stance is expressed through
  concrete *remembered deeds* and the *region state* around them — "this person
  remembers what happened", not "+17 friendship".
* **No omniscient state.** An NPC only "knows" a deed if it has a plausible
  knowledge source (they were involved, witnessed it, it became public, a
  companion told them, or their faction tracks it). Derived from the deeds the
  world already persists — **no new persisted NPC state is introduced.**
* **No simulation.** Presence / role changes / dialogue variants are *derived*
  from the region state and deeds at query time, deterministically.

Engine-agnostic: pure data + rules. No ``print``/``input``, no file/UI/Godot
coupling. Everything returned is plain, JSON-shaped data.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .world import LivingWorld

# Reusable NPC categories (depth of characterization scales with importance).
CATEGORIES = [
    "major", "quest", "settlement", "merchant", "service", "guard",
    "civilian", "faction", "event", "ambient",
]

# Companion reaction hooks a scene can carry (which companion the NPC's
# situation naturally draws out). Content-tagged, resolved against the party.
COMPANION_HOOKS = {
    "medical": "Maeve Ashwood",
    "evidence": "Corwin",
    "military": "Talos",
    "craft": "Torren",
    "faith": "Eleanor",
    "beast": "Ragash",
    "belonging": "Ronan",
}

# Knowledge sources that plausibly let an NPC know a deed happened.
KNOWLEDGE_SOURCES = [
    "witnessed", "involved", "public", "companion_told", "faction_tracks",
    "found_evidence", "word_of_mouth",
]


def by_location(npcs: List[dict], location_id: str) -> List[dict]:
    return [n for n in npcs if n.get("location_id") == location_id]


def by_category(npcs: List[dict], category: str) -> List[dict]:
    return [n for n in npcs if n.get("category") == category]


def find(npcs: List[dict], npc_id: str) -> Optional[dict]:
    for n in npcs:
        if n.get("id") == npc_id:
            return n
    return None


def _location_status(npc: dict, world: LivingWorld) -> Optional[str]:
    loc = world.location(npc.get("location_id", "")) if world else None
    return loc.status if loc else None


def presence(npc: dict, world: LivingWorld) -> str:
    """Is the NPC ``present`` / ``fearful`` / ``absent`` given the world state?

    Derived from the NPC's location status; no separate persisted presence.
    """
    rules = npc.get("presence", {})
    status = _location_status(npc, world)
    if status and status in rules.get("absent_if_status", []):
        return "absent"
    if status and status in rules.get("fearful_if_status", []):
        return "fearful"
    return rules.get("default", "present")


def knows_deed(npc: dict, deed_id: str, world: LivingWorld) -> bool:
    """Does this NPC plausibly know ``deed_id`` happened?

    True only if (a) the deed is actually recorded in the world, and (b) the NPC
    has a declared knowledge source for it, or the deed is flagged public in the
    NPC's ``knows`` list. Prevents omniscient NPCs.
    """
    if not any(d.id == deed_id for d in world.deeds):
        return False
    for entry in npc.get("knows", []):
        if entry.get("deed") == deed_id:
            return entry.get("source") in KNOWLEDGE_SOURCES
        if entry.get("deed") == "*" and entry.get("source") == "public":
            # NPC keeps up with public news generally
            return True
    return False


def remembered_deeds(npc: dict, world: LivingWorld) -> List[str]:
    """The recorded deeds this NPC actually knows about (its memory)."""
    return [d.id for d in world.deeds if knows_deed(npc, d.id, world)]


def contextual_dialogue(npc: dict, world: LivingWorld,
                        flags: Optional[Dict[str, bool]] = None) -> str:
    """Pick the NPC's most relevant line for the current world.

    Priority (most specific first): a known deed → a set flag → the region
    status around them → their default line. An NPC never delivers the same line
    before and after a major regional event they know about.
    """
    flags = flags or {}
    dlg = npc.get("dialogue", {})

    by_deed = dlg.get("by_deed", {})
    if by_deed:
        for deed_id in remembered_deeds(npc, world):
            if deed_id in by_deed:
                return by_deed[deed_id]

    by_flag = dlg.get("by_flag", {})
    for flag, line in by_flag.items():
        if flags.get(flag):
            return line

    status = _location_status(npc, world)
    by_status = dlg.get("by_status", {})
    if status and status in by_status:
        return by_status[status]

    return dlg.get("default", "")


def companion_reactions(npc: dict, party: List[str]) -> List[dict]:
    """Which present companions would naturally react to this NPC's situation."""
    out = []
    party_set = set(party)
    for hook in npc.get("companion_hooks", []):
        companion = COMPANION_HOOKS.get(hook)
        if companion and companion in party_set:
            out.append({"hook": hook, "companion": companion})
    return out


def describe(npc: dict, world: LivingWorld, party: Optional[List[str]] = None,
            flags: Optional[Dict[str, bool]] = None) -> dict:
    """A full engine-neutral snapshot the presentation can render for one NPC."""
    return {
        "id": npc["id"],
        "name": npc["name"],
        "role": npc.get("role", ""),
        "category": npc.get("category", "civilian"),
        "location_id": npc.get("location_id", ""),
        "presence": presence(npc, world),
        "line": contextual_dialogue(npc, world, flags),
        "remembers": remembered_deeds(npc, world),
        "companion_reactions": companion_reactions(npc, party or []),
    }


def resolve_references(npcs: List[dict], region) -> List[str]:
    """Validate every NPC reference resolves. Returns error strings (empty=ok)."""
    errors: List[str] = []
    ids = {n.get("id") for n in npcs}
    loc_ids = {l.get("id") for l in region.locations}
    event_ids = {e.get("id") for e in region.event_templates}
    companions = set(COMPANION_HOOKS.values())

    seen = set()
    for npc in npcs:
        nid = npc.get("id")
        if not nid or not npc.get("name"):
            errors.append(f"npc missing id/name: {npc}")
            continue
        if nid in seen:
            errors.append(f"duplicate npc id {nid!r}")
        seen.add(nid)
        if npc.get("category") not in CATEGORIES:
            errors.append(f"npc {nid!r} unknown category {npc.get('category')!r}")
        loc = npc.get("location_id")
        if loc and loc not in loc_ids:
            errors.append(f"npc {nid!r} unknown location {loc!r}")
        for ev in npc.get("events", []):
            if ev not in event_ids:
                errors.append(f"npc {nid!r} unknown event {ev!r}")
        for hook in npc.get("companion_hooks", []):
            if hook not in COMPANION_HOOKS:
                errors.append(f"npc {nid!r} unknown companion hook {hook!r}")
        for rel in npc.get("relationships", []):
            target = rel.get("with")
            if target and target not in ids and target not in companions:
                errors.append(f"npc {nid!r} relationship to unknown {target!r}")
        for entry in npc.get("knows", []):
            if entry.get("source") not in KNOWLEDGE_SOURCES:
                errors.append(f"npc {nid!r} bad knowledge source {entry.get('source')!r}")
    return errors
