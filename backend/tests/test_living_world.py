"""Tests for the Living World foundation (tactical/living_world).

Covers all ten systems of the Living Frontier Pass as reusable, engine-agnostic
frameworks, plus their binding to the First Region via the frontier overlay.
Additive: does not re-test combat, the frontier slice internals, or saves.
"""

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tactical import frontier
from tactical.living_world import (
    region_state, reputation, events, companions, banter, environment,
    memory, epilogue, content, frontier_overlay,
)
from tactical.living_world.world import LivingWorld


FULL_PARTY = ["Ronan", "Talos", "Maeve Ashwood", "Torren", "Corwin",
              "Eleanor", "Ragash"]


# --- 1. Living Region System ----------------------------------------------
def test_region_status_transitions_are_logged_and_validated():
    loc = region_state.LocationState("x", "X", status=region_state.CORRUPTED,
                                     tags=["forest"])
    assert loc.set_status(region_state.RECOVERING, "cleansed") is True
    assert loc.set_status(region_state.RECOVERING) is False  # no-op same status
    assert loc.status == region_state.RECOVERING
    assert loc.history[-1]["from"] == region_state.CORRUPTED
    assert loc.history[-1]["natural"] is True


def test_region_status_rejects_unknown_status():
    loc = region_state.LocationState("x", "X")
    try:
        loc.set_status("melancholy")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_all_six_states_exist():
    assert set(region_state.STATES) == {
        "safe", "threatened", "recovering", "prosperous", "corrupted", "restored"}


def test_location_state_json_roundtrips():
    loc = region_state.LocationState("a", "Alpha", kind="landmark",
                                     status="corrupted", tags=["forest"],
                                     region_id="r")
    loc.set_status("recovering", "x")
    back = region_state.LocationState.from_state(json.loads(json.dumps(loc.to_state())))
    assert back.to_state() == loc.to_state()


# --- 2. Reputation (remembered deeds, no meter) ---------------------------
def test_reputation_records_deeds_idempotently_and_references_by_location():
    deeds = []
    d = reputation.Deed("saved_bram", "Saved the Lost Wolf", reputation.SAVE,
                        "Saved Bram.", npc_line="You saved a wolf.",
                        location_id="old_wolf_shrine", region_id="the_frontier")
    assert reputation.record_deed(deeds, d) is True
    assert reputation.record_deed(deeds, d) is False  # idempotent by id
    assert reputation.npc_references(deeds, location_id="old_wolf_shrine") == \
        ["You saved a wolf."]
    assert reputation.npc_references(deeds, location_id="elsewhere") == []


# --- 3. Dynamic World Events ----------------------------------------------
def test_event_templates_include_all_ten_examples():
    ids = {t["id"] for t in content.event_templates()}
    assert {"merchant_under_attack", "lost_child", "traveling_healer",
            "hidden_pack_scouts", "wandering_knight", "corrupted_wildlife",
            "refugee_caravan", "traveling_storyteller", "abandoned_campsite",
            "injured_animal"} <= ids


def test_events_filter_by_tags_and_draw_is_deterministic():
    tpls = content.event_templates()
    forest = events.eligible(tpls, ["forest"])
    assert forest and all("forest" in t["tags"] for t in forest)
    a = events.draw_events(tpls, ["forest"], count=2, rng=random.Random(1))
    b = events.draw_events(tpls, ["forest"], count=2, rng=random.Random(1))
    assert [t["id"] for t in a] == [t["id"] for t in b]


def test_event_draw_respects_exclude():
    tpls = content.event_templates()
    drawn = events.draw_events(tpls, ["road", "forest"], count=3,
                               exclude=["lost_child"], rng=random.Random(3))
    assert "lost_child" not in {t["id"] for t in drawn}


# --- 4. Companion Presence + 8. Landmark Moments --------------------------
def test_every_companion_has_presence_and_a_landmark_moment():
    presence = content.companion_presence()
    landmarks = content.companion_landmarks()
    for c in FULL_PARTY:
        assert presence.get(c), f"{c} missing presence"
        assert landmarks.get(c), f"{c} missing landmark moment"


def test_presence_matches_context_tags():
    presence = content.companion_presence()
    beats = companions.presence_for(presence, "Eleanor", ["shrine"])
    assert any(b["kind"] == "blessing" for b in beats)
    # Maeve treats wounds at a settlement
    beats = companions.presence_for(presence, "Maeve Ashwood", ["refugee_camp"])
    assert beats


def test_landmark_moment_is_optional_and_tag_gated():
    landmarks = content.companion_landmarks()
    m = companions.landmark_moment(landmarks, "Ronan", ["shrine"])
    assert m and m["optional"] is True
    assert companions.landmark_moment(landmarks, "Ronan", ["forge"]) is None


# --- 5. Companion Banter ---------------------------------------------------
def test_banter_covers_all_triggers_and_only_fires_for_present_party():
    cat = content.banter()
    for trig in banter.TRIGGERS:
        assert cat.get(trig), f"no banter for trigger {trig}"
    # A two-person exchange should not fire if one is missing.
    ex = banter.banter_for(cat, "cave", ["Torren"], rng=random.Random(1))
    assert ex is None  # cave banter needs Torren AND Corwin
    ex = banter.banter_for(cat, "cave", ["Torren", "Corwin"], rng=random.Random(1))
    assert ex and set(ex["participants"]) <= {"Torren", "Corwin"}


# --- 6. Environmental Storytelling ----------------------------------------
def test_environment_details_and_corwin_insight_only_with_corwin():
    env = content.environment_details()
    with_corwin = environment.details_for(env, ["road"], count=5,
                                          party=["Corwin"], rng=random.Random(2))
    assert any("corwin_insight" in d for d in with_corwin)
    without = environment.details_for(env, ["road"], count=5,
                                      party=["Talos"], rng=random.Random(2))
    assert all("corwin_insight" not in d for d in without)


# --- 7/9. Regional Memory --------------------------------------------------
def test_regional_memory_has_all_states_and_reports_changes():
    mem = content.regional_memory()
    for s in region_state.STATES:
        assert mem.get(s, {}).get("changes")
    loc = region_state.LocationState("v", "Village", status="restored",
                                     tags=["village"])
    rep_report = memory.revisit_report(mem, loc, rng=random.Random(1))
    assert rep_report["status"] == "restored"
    assert rep_report["changes"] and rep_report["prompt"]


# --- 2/9. Regional memory surfaces remembered deeds -----------------------
def test_revisit_report_surfaces_remembered_deeds():
    mem = content.regional_memory()
    deeds = [reputation.Deed("d", "Deed", reputation.RESTORE, "s",
                             npc_line="We remember you.", location_id="v")]
    loc = region_state.LocationState("v", "Village", status="restored")
    r = memory.revisit_report(mem, loc, deeds=deeds, rng=random.Random(1))
    assert "We remember you." in r["remembered"]


# --- 10-style: LivingWorld aggregate --------------------------------------
def test_living_world_builds_from_content_and_roundtrips():
    world = LivingWorld.from_content()
    assert world.location("the_frontier") is not None
    world.set_status("greenhollow", "restored", "x")
    world.record_deed(reputation.Deed("z", "Z", reputation.CLEANSE, "s"))
    back = LivingWorld.from_state(json.loads(json.dumps(world.to_state())))
    assert back.to_state() == world.to_state()


# --- 2. Regional Epilogue --------------------------------------------------
def test_epilogue_is_reactive_to_flags():
    threads = content.epilogue_threads()
    bright = epilogue.build_epilogue(threads, {t["flag"]: True for t in threads["threads"]})
    grim = epilogue.build_epilogue(threads, {})
    assert bright["title"] == "The Frontier Endures"
    assert bright["positives"] == bright["total"]
    assert grim["positives"] == 0
    assert bright["closing"] != grim["closing"]
    assert all(th["outcome"] == "hopeful" for th in bright["threads"])
    assert all(th["outcome"] == "bittersweet" for th in grim["threads"])


def test_epilogue_covers_all_eight_named_threads():
    subjects = {t["id"] for t in content.epilogue_threads()["threads"]}
    assert subjects == {"bram", "hidden_pack", "corwin_investigation",
                        "maeve_settlement", "torren_forge", "eleanor_diplomacy",
                        "talos_leadership", "ronan_acceptance"}


# --- Overlay: binding to the First Region ---------------------------------
def test_overlay_is_deterministic_and_reactive_to_choices():
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    o1, w1 = frontier_overlay.build_overlay(golden, seed=7)
    o2, _ = frontier_overlay.build_overlay(
        frontier.run_frontier(seed=7, decider=frontier.golden_decider), seed=7)
    assert json.dumps(o1) == json.dumps(o2)  # deterministic

    worst = frontier.run_frontier(seed=7, decider=frontier.worst_decider)
    ow, ww = frontier_overlay.build_overlay(worst, seed=7)
    # The world remembers more when the player plays well.
    assert len(w1.deeds) > len(ww.deeds)
    assert o1["epilogue"]["positives"] > ow["epilogue"]["positives"]


def test_overlay_produces_nine_beats_with_living_content():
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    overlay, _ = frontier_overlay.build_overlay(golden, seed=7)
    assert len(overlay["beats"]) == 9
    # every beat is bound to a real location and has some living-world content
    for b in overlay["beats"]:
        assert b["location_id"]
        assert b["presence"] or b["banter"] or b["environment"] or b["event"]


def test_golden_run_restores_locations_and_records_key_deeds():
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    _, world = frontier_overlay.build_overlay(golden, seed=7)
    restored = [l for l in world.locations.values() if l.status == "restored"]
    assert restored, "cleansing the region should restore locations"
    deed_ids = {d.id for d in world.deeds}
    assert {"saved_bram", "helped_refugees", "broke_the_avatar"} <= deed_ids


def test_all_region_transitions_from_golden_run_are_natural():
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    _, world = frontier_overlay.build_overlay(golden, seed=7)
    for loc in world.locations.values():
        for h in loc.history:
            assert h["natural"], f"unnatural transition {h} at {loc.id}"


def test_core_modules_have_no_screen_io():
    # Layer Rule: gameplay never prints/inputs. Guard the whole package
    # (except the region_review dev/QA tool).
    import re
    here = os.path.dirname(frontier_overlay.__file__)
    pat = re.compile(r"(?<![A-Za-z_])(print|input)\s*\(")
    offenders = []
    for fn in os.listdir(here):
        if fn.endswith(".py") and fn != "region_review.py":
            with open(os.path.join(here, fn), encoding="utf-8") as fh:
                if pat.search(fh.read()):
                    offenders.append(fn)
    assert not offenders, f"screen I/O in core modules: {offenders}"


# --- Region Completion Review (runnable QA) --------------------------------
def test_region_review_runs_and_reports_ready():
    from tactical.living_world import region_review
    report = region_review.run()
    assert report["summary"]["gap"] == 0, report["results"]
    assert report["summary"]["region_ready"] is True
