"""Tests for Living World persistence + region-agnostic overlay.

Additive foundational work: save round-trip, legacy-save compatibility,
multi-region state, and proving the overlay engine consumes ANY region's
content data (via a small test-region fixture — NOT real Region Two content).
"""

import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tactical import frontier
from tactical.living_world import (
    persistence, frontier_overlay, overlay, reputation, region_state,
)
from tactical.living_world.world import LivingWorld
from tactical.living_world.region import RegionContent
import world_state as ws_module


def _golden_world():
    state = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    _, world = frontier_overlay.build_overlay(state, seed=7)
    return world


# --- 1. Fresh save ---------------------------------------------------------
def test_fresh_save_roundtrips_through_world_state():
    world = _golden_world()
    ws = {}
    persistence.save_to_world_state(world, ws)
    ws = json.loads(json.dumps(ws))  # as the save layer serializes
    back = persistence.load_from_world_state(ws)
    assert back.to_state() == world.to_state()


# --- 2. Legacy / existing save --------------------------------------------
def test_legacy_save_without_living_world_initializes_defaults():
    legacy_ws = {}  # a save written before this feature
    persistence.ensure_defaults(legacy_ws)
    world = persistence.load_from_world_state(legacy_ws)
    assert world.to_state() == persistence.default_state()
    assert world.locations == {} and world.deeds == []


def test_load_from_world_state_missing_key_is_safe():
    world = persistence.load_from_world_state({})  # no living_world key at all
    assert isinstance(world, LivingWorld)
    assert world.to_state() == persistence.default_state()


# --- 3 & 4. Save/Load after regional changes ------------------------------
def test_save_then_load_after_regional_changes_is_identical():
    world = _golden_world()
    before = world.to_state()
    ws = {}
    persistence.save_to_world_state(world, ws)
    dumped = json.dumps(ws)
    reloaded = persistence.load_from_world_state(json.loads(dumped))
    assert reloaded.to_state() == before
    # region states, deeds, progression all survived
    assert reloaded.location("the_frontier") is not None
    assert reloaded.deeds
    assert reloaded.region_progression("the_frontier").get("status") == "complete"


# --- 5. Multiple regions in one world -------------------------------------
def test_multiple_regions_persist_together():
    world = _golden_world()  # already has the Frontier
    # layer a second region's locations onto the same world
    test_region = RegionContent.from_manifest("testregion_region")
    world.ensure_locations(test_region.locations)
    world.set_status("tr_keep", "restored", "test")
    world.set_progression("test_marches", {"status": "complete"})
    ws = {}
    persistence.save_to_world_state(world, ws)
    back = persistence.load_from_world_state(json.loads(json.dumps(ws)))
    assert back.location("the_frontier") is not None
    assert back.location("tr_keep").status == "restored"
    assert back.region_progression("test_marches")["status"] == "complete"
    assert back.to_state() == world.to_state()


# --- 6. Repeated save/load cycles are stable ------------------------------
def test_repeated_save_load_cycles_are_stable():
    world = _golden_world()
    target = world.to_state()
    for _ in range(5):
        ws = {}
        persistence.save_to_world_state(world, ws)
        world = persistence.load_from_world_state(json.loads(json.dumps(ws)))
        assert world.to_state() == target


# --- 7. Unknown future fields are ignored safely --------------------------
def test_unknown_future_fields_are_ignored():
    world = _golden_world()
    state = world.to_state()
    state["some_future_field"] = {"not": "known"}
    state["locations"]["the_frontier"]["future_loc_field"] = 123
    back = LivingWorld.from_state(state)
    # loads cleanly; unknown top-level + per-location keys dropped
    assert "some_future_field" not in back.to_state()
    assert "future_loc_field" not in back.to_state()["locations"]["the_frontier"]
    assert back.location("the_frontier") is not None


# --- world_state defaults backfill ----------------------------------------
def test_world_state_ensure_defaults_adds_living_world_block():
    ws = ws_module.world_state
    snapshot = copy.deepcopy(ws)
    try:
        ws.pop("living_world", None)
        ws_module.ensure_world_state_defaults()
        assert "living_world" in ws
        lw = ws["living_world"]
        for k in ("locations", "deeds", "events_seen", "landmarks_seen",
                  "presence_seen", "progression", "flags", "version"):
            assert k in lw
    finally:
        ws.clear()
        ws.update(snapshot)


def test_world_state_defaults_repair_wrong_typed_living_world():
    ws = ws_module.world_state
    snapshot = copy.deepcopy(ws)
    try:
        ws["living_world"] = "corrupted-not-a-dict"
        ws_module.ensure_world_state_defaults()
        assert isinstance(ws["living_world"], dict)
        assert isinstance(ws["living_world"]["deeds"], list)
    finally:
        ws.clear()
        ws.update(snapshot)


# --- Region-agnostic overlay ----------------------------------------------
def test_overlay_engine_is_region_agnostic_via_fixture():
    region = RegionContent.from_manifest("testregion_region")
    assert region.validate() == []
    run = {
        "party_start": ["Talos"],
        "beats": [
            {"id": "tr_gate", "title": "At the Holdfast", "recruited": ["Eleanor"]},
            {"id": "tr_wilds", "title": "Into the Wilds", "recruited": []},
            {"id": "tr_finale", "title": "The Keep", "recruited": []},
        ],
        "deeds": [("tr_holdfast", reputation.Deed(
            "tr_saved", "Saved the Holdfast", reputation.RESTORE, "s",
            npc_line="You saved us.", location_id="tr_holdfast",
            region_id="test_marches"))],
        "transitions": [("tr_holdfast", "recovering", "secured"),
                        ("tr_keep", "restored", "cleansed"),
                        ("tr_holdfast", "restored", "cleansed")],
        "epilogue_flags": {"holdfast_saved": True, "region_cleansed": True},
        "completed": True,
    }
    ov, world = overlay.build_overlay(region, run, seed=3)
    assert ov["region_id"] == "test_marches"
    assert len(ov["beats"]) == 3
    assert ov["epilogue"]["title"] == "The Marches Hold"
    assert ov["epilogue"]["positives"] == 2
    assert world.region_progression("test_marches")["status"] == "complete"
    # deterministic
    ov2, _ = overlay.build_overlay(RegionContent.from_manifest("testregion_region"),
                                   run, seed=3)
    assert json.dumps(ov) == json.dumps(ov2)


def test_frontier_still_behaves_after_refactor():
    # The Frontier overlay must be unchanged behaviourally after the
    # region-agnostic refactor.
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    ov, world = frontier_overlay.build_overlay(golden, seed=7)
    assert ov["region_id"] == "the_frontier"
    assert len(ov["beats"]) == 9
    assert ov["epilogue"]["title"] == "The Frontier Endures"
    assert ov["epilogue"]["positives"] == 8
    assert {"saved_bram", "helped_refugees", "broke_the_avatar"} <= {
        d.id for d in world.deeds}
    # progression recorded on completion
    assert world.region_progression("the_frontier")["status"] == "complete"


def test_beat_context_still_exposed_for_review():
    assert len(frontier_overlay.BEAT_CONTEXT) == 9
    assert "corruption_avatar" in frontier_overlay.BEAT_CONTEXT


# --- Content contracts -----------------------------------------------------
def test_all_region_manifests_validate():
    for name in ("frontier_region", "testregion_region"):
        assert RegionContent.from_manifest(name).validate() == []


def test_invalid_manifest_is_reported():
    region = RegionContent.from_manifest("frontier_region")
    region.beat_map = {"bad_beat": {"loc": "nonexistent_place",
                                    "tags": [], "triggers": ["not_a_trigger"]}}
    errs = region.validate()
    assert any("nonexistent_place" in e for e in errs)
    assert any("not_a_trigger" in e for e in errs)
