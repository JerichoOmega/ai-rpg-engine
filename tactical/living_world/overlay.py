"""
overlay — the region-agnostic living-world overlay engine.
==========================================================

Consumes a :class:`~tactical.living_world.region.RegionContent` (all content is
data) plus a **run record** (the per-playthrough facts: beats, recruited party,
deeds earned, region-state transitions, epilogue flags) and produces the
engine-neutral living-world overlay: per-beat companion presence, banter,
environmental detail, dynamic events; the remembered deeds; the resulting region
states; and the reactive epilogue.

There are **no region-specific assumptions here** — the Frontier binding lives
in :mod:`frontier_overlay`, which builds the RegionContent + run record and
delegates to this engine.

Engine-agnostic: pure data + rules. No I/O. Deterministic for a given seed.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Tuple

from . import companions as _companions
from . import banter as _banter
from . import environment as _environment
from . import events as _events
from . import epilogue as _epilogue
from . import memory as _memory
from .region import RegionContent
from .world import LivingWorld


def build_overlay(region: RegionContent, run: dict, seed: int = 7,
                  world: Optional[LivingWorld] = None) -> Tuple[dict, LivingWorld]:
    """Assemble the living-world overlay for one region playthrough.

    ``run`` keys:
        party_start: [str]                       initial party
        beats: [ {id, title, recruited:[str]} ]  ordered beat records
        deeds: [ (location_id, Deed) ]           remembered deeds to record
        transitions: [ (location_id, status, reason) ]  ordered status changes
        epilogue_flags: { flag: bool }           drives the epilogue + progression
        completed: bool                          region finale reached (optional)

    Returns ``(overlay, world)``.
    """
    if world is None:
        world = LivingWorld.from_content(region.locations)
    else:
        world.ensure_locations(region.locations)

    for _loc_id, deed in run.get("deeds", []):
        world.record_deed(deed)
    for loc_id, status, reason in run.get("transitions", []):
        world.set_status(loc_id, status, reason)

    party: List[str] = list(run.get("party_start", []))
    beats_out: List[dict] = []
    for i, beat in enumerate(run.get("beats", [])):
        for name in beat.get("recruited", []):
            if name not in party:
                party.append(name)
        ctx = region.beat_map.get(beat["id"],
                                  {"loc": "", "tags": [], "triggers": []})
        rng = random.Random(seed * 1000 + i)
        tags = ctx.get("tags", [])
        loc_id = ctx.get("loc", "")
        loc = world.location(loc_id) if loc_id else None

        presence_beats = _companions.presence_here(region.presence, party, tags,
                                                    per_companion=1, rng=rng)
        for p in presence_beats:
            world.mark_presence_seen(p["companion"], loc_id)
        landmark_beats = _companions.landmark_moments_here(region.landmarks,
                                                           party, tags)
        for m in landmark_beats:
            world.mark_landmark_seen(m["companion"], loc_id)
        env_beats = _environment.details_for(region.environment, tags, count=1,
                                             party=party, rng=rng)
        banter_line = None
        for trig in ctx.get("triggers", []):
            banter_line = _banter.banter_for(region.banter, trig, party, rng=rng)
            if banter_line:
                break

        event = None
        drawn = _events.draw_events(
            region.event_templates, tags,
            status=(loc.status if loc else None),
            exclude=world.events_seen, rng=rng)
        if drawn:
            event = _events.instantiate(drawn[0])
            world.mark_event_seen(event["id"])

        beats_out.append({
            "beat_id": beat["id"],
            "title": beat.get("title", beat["id"]),
            "location_id": loc_id,
            "location_name": loc.name if loc else "",
            "status_after": loc.status if loc else "",
            "tags": list(tags),
            "party": list(party),
            "presence": presence_beats,
            "landmark_moments": landmark_beats,
            "banter": banter_line,
            "environment": env_beats,
            "event": event,
        })

    flags = run.get("epilogue_flags", {})
    epi = _epilogue.build_epilogue(region.epilogue_threads, flags)

    if run.get("completed") or flags.get("region_cleansed"):
        world.set_progression(region.region_id, {
            "status": "complete",
            "epilogue": epi["title"],
            "threads_hopeful": epi["positives"],
            "threads_total": epi["total"],
        })

    overlay = {
        "region": region.region_name,
        "region_id": region.region_id,
        "beats": beats_out,
        "epilogue_flags": flags,
        "epilogue": epi,
        "deeds": [d.to_state() for d in world.deeds],
    }
    return overlay, world


def revisit_reports(region: RegionContent, world: LivingWorld,
                    rng: Optional[random.Random] = None) -> List[dict]:
    """Regional-memory reports for every non-region location in ``region``."""
    rng = rng or random.Random(7)
    reports = []
    for loc in world.locations.values():
        if loc.kind == "region":
            continue
        if loc.region_id and loc.region_id != region.region_id:
            continue
        reports.append(_memory.revisit_report(region.regional_memory, loc,
                                              deeds=world.deeds, count=3, rng=rng))
    return reports
