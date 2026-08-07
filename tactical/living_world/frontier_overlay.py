"""
frontier_overlay — bind the Living World frameworks to the First Region.
========================================================================

The Frontier vertical slice (``tactical/frontier.py``) stays untouched: this
module *consumes* a completed :class:`~tactical.frontier.FrontierState` and
produces an engine-neutral **living-world overlay** — the presence beats,
banter, environmental details and dynamic events that play *around* each combat
beat, the deeds the world now remembers, the region-status changes the player's
choices caused, and the reactive epilogue.

Additive and non-breaking: nothing here modifies the slice, combat, saves, or
canon. It only reads the slice's recorded decisions and returns data.

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
from . import content as _content
from . import reputation as _rep
from .world import LivingWorld


# beat id -> (location_id, context tags, banter triggers to try)
BEAT_CONTEXT: Dict[str, dict] = {
    "road_in": {"loc": "frontier_road", "tags": ["road", "wilderness"],
                "triggers": ["weather", "forest"]},
    "roadside_ambush": {"loc": "frontier_road",
                        "tags": ["road", "wilderness", "battlefield"],
                        "triggers": ["victory"]},
    "settlement": {"loc": "refugee_settlement",
                   "tags": ["settlement", "refugee_camp"],
                   "triggers": ["enter_town"]},
    "sundered_span": {"loc": "sundered_span",
                      "tags": ["river", "road", "battlefield"],
                      "triggers": ["river", "victory"]},
    "forge_stand": {"loc": "the_forge", "tags": ["forge", "ruins"],
                    "triggers": ["ruins", "victory"]},
    "investigation": {"loc": "dwarven_ruins",
                      "tags": ["ruins", "cave", "discovery"],
                      "triggers": ["ruins", "discovery"]},
    "corrupted_woods": {"loc": "corrupted_woods",
                        "tags": ["forest", "wilderness", "corrupted"],
                        "triggers": ["forest"]},
    "lost_howl": {"loc": "old_wolf_shrine",
                  "tags": ["shrine", "forest", "wilderness"],
                  "triggers": ["forest"]},
    "corruption_avatar": {"loc": "blight_heart",
                          "tags": ["boss_arena", "corrupted"],
                          "triggers": ["boss_arena", "victory"]},
}


def compute_epilogue_flags(state) -> Dict[str, bool]:
    """Derive the epilogue thread flags from a completed FrontierState."""
    flags = state.flags
    return {
        "bram_saved": state.howl_ending == "rescued",
        "pack_ally": bool(flags.get("pack_ally")),
        "knows_source": bool(flags.get("knows_source")),
        "settlement_secured": bool(flags.get("settlement_secured")),
        "forge_mastered": bool(flags.get("forge_mastered")),
        "region_cleansed": state.region_outcome == "cleansed",
        "talos_trust": bool(flags.get("talos_trust")),
    }


def _deeds_from_state(state) -> List[Tuple[str, _rep.Deed]]:
    """(location_id, Deed) pairs the world should remember, from choices made."""
    f = state.flags
    cleansed = state.region_outcome == "cleansed"
    out: List[Tuple[str, _rep.Deed]] = []
    if f.get("talos_trust"):
        out.append(("frontier_road", _rep.Deed(
            id="protected_travellers", title="Shielded the Travellers",
            kind=_rep.PROTECT_TRAVELLERS,
            summary="Body-blocked a roadside ambush so no traveller fell.",
            npc_line="You're the ones who stood over the wagons on the east road. We tell that one to the children.",
            location_id="frontier_road", region_id="the_frontier")))
    if f.get("settlement_secured"):
        out.append(("refugee_settlement", _rep.Deed(
            id="helped_refugees", title="A Light in the Ashes",
            kind=_rep.HELP_REFUGEES,
            summary="Stayed to fortify and heal the refugee camp.",
            npc_line="You gave the Ashen Camp its walls back. Half of us are alive because you didn't ride on.",
            location_id="refugee_settlement", region_id="the_frontier")))
    if f.get("forge_mastered"):
        out.append(("the_forge", _rep.Deed(
            id="restored_forge", title="Rekindled the Old Forge",
            kind=_rep.RESTORE,
            summary="Turned the forge into a working defence and left it burning.",
            npc_line="Every good axe on this Frontier came off that anvil since you woke it. That's your doing.",
            location_id="the_forge", region_id="the_frontier")))
    if f.get("woods_cleansed"):
        out.append(("corrupted_woods", _rep.Deed(
            id="cleansed_woods", title="Cleansed the Blightwood",
            kind=_rep.CLEANSE,
            summary="Advanced carefully and cleansed the corrupted woods.",
            npc_line="The wood doesn't weep anymore. My grandfather's grave is quiet again because of you.",
            location_id="corrupted_woods", region_id="the_frontier")))
    if state.howl_ending == "rescued":
        out.append(("old_wolf_shrine", _rep.Deed(
            id="saved_bram", title="Saved the Lost Wolf",
            kind=_rep.SAVE,
            summary="Saved Bram rather than slaying him at the Lost Howl.",
            npc_line="You saved a wolf when it would've been easier to kill it. The Pack remembers that. So do we.",
            location_id="old_wolf_shrine", region_id="the_frontier")))
    if cleansed:
        out.append(("blight_heart", _rep.Deed(
            id="broke_the_avatar", title="Broke the Corruption Avatar",
            kind=_rep.CLEANSE,
            summary="Defeated the Corruption Avatar and cleansed the region.",
            npc_line="You're the one who broke the thing in the deep woods. The whole Frontier owes you a night's sleep.",
            location_id="blight_heart", region_id="the_frontier")))
    return out


def _apply_transitions(world: LivingWorld, state) -> None:
    """Change region statuses to reflect the player's choices (natural arcs)."""
    f = state.flags
    cleansed = state.region_outcome == "cleansed"

    if f.get("talos_trust"):
        world.set_status("frontier_road", "safe", "travellers protected")
    if f.get("settlement_secured"):
        world.set_status("refugee_settlement", "recovering", "camp secured")
    # The Sundered Span is an anchor win — the bridge road is held either way.
    world.set_status("sundered_span", "recovering", "the span held")
    if f.get("forge_mastered"):
        world.set_status("the_forge", "recovering", "forge rekindled")
    if f.get("woods_cleansed"):
        world.set_status("corrupted_woods", "recovering", "woods cleansed")

    if cleansed:
        world.set_status("blight_heart", "restored", "avatar broken")
        world.set_status("greenhollow", "restored", "region cleansed")
        world.set_status("the_frontier", "recovering", "corruption broken")
        # Places already recovering are lifted the rest of the way home.
        for loc_id in ("refugee_settlement", "corrupted_woods"):
            loc = world.location(loc_id)
            if loc and loc.status == "recovering":
                loc.set_status("restored", "region cleansed")


def build_overlay(state, seed: int = 7,
                  world: Optional[LivingWorld] = None) -> Tuple[dict, LivingWorld]:
    """Produce the full living-world overlay for a completed FrontierState.

    Returns ``(overlay, world)`` where ``overlay`` is plain render-ready data
    and ``world`` is the resulting :class:`LivingWorld` (region states + deeds).
    """
    world = world or LivingWorld.from_content()
    presence = _content.companion_presence()
    landmarks = _content.companion_landmarks()
    banter_content = _content.banter()
    env_content = _content.environment_details()
    templates = _content.event_templates()

    # Record remembered deeds and apply region-state transitions.
    for loc_id, deed in _deeds_from_state(state):
        world.record_deed(deed)
    _apply_transitions(world, state)

    party: List[str] = ["Ronan"]
    beats_out: List[dict] = []
    for i, beat in enumerate(state.beats):
        for name in beat.get("recruited", []):
            if name not in party:
                party.append(name)
        ctx = BEAT_CONTEXT.get(beat["id"],
                               {"loc": "", "tags": [], "triggers": []})
        rng = random.Random(seed * 1000 + i)
        tags = ctx["tags"]
        loc = world.location(ctx["loc"]) if ctx["loc"] else None

        presence_beats = _companions.presence_here(presence, party, tags,
                                                    per_companion=1, rng=rng)
        landmark_beats = _companions.landmark_moments_here(landmarks, party, tags)
        env_beats = _environment.details_for(env_content, tags, count=1,
                                             party=party, rng=rng)
        banter_line = None
        for trig in ctx["triggers"]:
            banter_line = _banter.banter_for(banter_content, trig, party, rng=rng)
            if banter_line:
                break

        event = None
        drawn = _events.draw_events(
            templates, tags,
            status=(loc.status if loc else None),
            exclude=world.events_seen, rng=rng)
        if drawn:
            event = _events.instantiate(drawn[0])
            world.mark_event_seen(event["id"])

        beats_out.append({
            "beat_id": beat["id"],
            "title": beat.get("title", beat["id"]),
            "location_id": ctx["loc"],
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

    flags = compute_epilogue_flags(state)
    epi = _epilogue.build_epilogue(_content.epilogue_threads(), flags)

    overlay = {
        "region": "The Frontier",
        "beats": beats_out,
        "epilogue_flags": flags,
        "epilogue": epi,
        "deeds": [d.to_state() for d in world.deeds],
    }
    return overlay, world


def revisit_reports(world: LivingWorld,
                    rng: Optional[random.Random] = None) -> List[dict]:
    """Regional-memory reports for every location the player might revisit."""
    rng = rng or random.Random(7)
    mem = _content.regional_memory()
    out = []
    for loc in world.locations.values():
        if loc.kind == "region":
            continue
        out.append(_memory.revisit_report(mem, loc, deeds=world.deeds,
                                           count=3, rng=rng))
    return out
