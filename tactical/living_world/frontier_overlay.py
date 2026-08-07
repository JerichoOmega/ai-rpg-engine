"""
frontier_overlay — the First Region's binding to the Living World engine.
=========================================================================

The Frontier vertical slice (``tactical/frontier.py``) stays untouched. This
adapter loads the Frontier's :class:`RegionContent` from its data manifest,
translates a completed :class:`~tactical.frontier.FrontierState` into a
region-agnostic **run record**, and delegates to the generic
:mod:`~tactical.living_world.overlay` engine.

All Frontier-specific knowledge (which choices earn which deeds, which region
states change, how epilogue flags are derived) lives here — the overlay engine
itself carries no region assumptions.

Public API is unchanged from the original pass (``build_overlay(state, seed)``,
``compute_epilogue_flags``, ``revisit_reports``) so existing callers/tests keep
working.

Engine-agnostic: pure data + rules. No I/O. Deterministic for a given seed.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Tuple

from . import content as _content
from . import overlay as _overlay
from . import reputation as _rep
from .region import RegionContent
from .world import LivingWorld

FRONTIER_MANIFEST = "frontier_region"

# Backward-compatible module attribute: the beat->context map, now sourced from
# the region manifest (data), not hard-coded here.
BEAT_CONTEXT: Dict[str, dict] = _content.load(FRONTIER_MANIFEST)["beat_map"]


def frontier_region() -> RegionContent:
    """The Frontier's RegionContent (loaded from its data manifest)."""
    return RegionContent.from_manifest(FRONTIER_MANIFEST)


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


def _transitions_from_state(state) -> List[Tuple[str, str, str]]:
    """Ordered (location_id, new_status, reason) changes from the player's play.

    Ordered so that a place first moves to ``recovering`` and is only lifted to
    ``restored`` once the region is cleansed — every step a natural transition.
    """
    f = state.flags
    cleansed = state.region_outcome == "cleansed"
    t: List[Tuple[str, str, str]] = []
    if f.get("talos_trust"):
        t.append(("frontier_road", "safe", "travellers protected"))
    if f.get("settlement_secured"):
        t.append(("refugee_settlement", "recovering", "camp secured"))
    t.append(("sundered_span", "recovering", "the span held"))
    if f.get("forge_mastered"):
        t.append(("the_forge", "recovering", "forge rekindled"))
    if f.get("woods_cleansed"):
        t.append(("corrupted_woods", "recovering", "woods cleansed"))
    if cleansed:
        t.append(("blight_heart", "restored", "avatar broken"))
        t.append(("greenhollow", "restored", "region cleansed"))
        t.append(("the_frontier", "recovering", "corruption broken"))
        if f.get("settlement_secured"):
            t.append(("refugee_settlement", "restored", "region cleansed"))
        if f.get("woods_cleansed"):
            t.append(("corrupted_woods", "restored", "region cleansed"))
    return t


def frontier_run_record(state) -> dict:
    """Translate a FrontierState into the region-agnostic run record."""
    return {
        "party_start": ["Ronan"],
        "beats": state.beats,
        "deeds": _deeds_from_state(state),
        "transitions": _transitions_from_state(state),
        "epilogue_flags": compute_epilogue_flags(state),
        "completed": state.region_outcome == "cleansed",
    }


def build_overlay(state, seed: int = 7,
                  world: Optional[LivingWorld] = None) -> Tuple[dict, LivingWorld]:
    """Produce the full living-world overlay for a completed FrontierState."""
    region = frontier_region()
    run = frontier_run_record(state)
    return _overlay.build_overlay(region, run, seed=seed, world=world)


def revisit_reports(world: LivingWorld,
                    rng: Optional[random.Random] = None) -> List[dict]:
    """Regional-memory reports for every Frontier location."""
    return _overlay.revisit_reports(frontier_region(), world, rng=rng)
