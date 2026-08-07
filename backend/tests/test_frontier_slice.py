"""Tests for the Frontier first-region vertical-slice orchestrator.

Verifies the end-to-end flow: interactive recruitment/investigation scenes with
real branching consequences, the three anchor showcases, Ronan's Lost Howl
climax, and the regional finale (The Corruption Avatar) — deterministically.
Combat is delegated to the canonical engine/showcases; this suite does not
re-test those internals.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tactical import frontier


EXPECTED_BEATS = [
    "road_in", "roadside_ambush", "settlement", "sundered_span",
    "forge_stand", "investigation", "corrupted_woods", "lost_howl",
    "corruption_avatar",
]
FULL_PARTY = {"Ronan", "Talos", "Maeve Ashwood", "Torren",
              "Corwin", "Eleanor", "Ragash"}
ANCHORS = {"sundered_span", "forge_stand", "lost_howl"}


def test_all_nine_beats_run_in_order():
    state = frontier.run_frontier(seed=7)
    assert [b["id"] for b in state.beats] == EXPECTED_BEATS


def test_full_party_recruited_regardless_of_choices():
    # No permanent companion loss in the main campaign — even the worst reads
    # still assemble the whole party.
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    worst = frontier.run_frontier(seed=7, decider=frontier.worst_decider)
    assert set(golden.party) == FULL_PARTY
    assert set(worst.party) == FULL_PARTY
    assert golden.party[0] == "Ronan"          # Ronan starts with you


def test_ronan_climax_saves_the_lost_wolf():
    state = frontier.run_frontier(seed=7)
    assert state.howl_ending == "rescued"
    lh = next(b for b in state.beats if b["id"] == "lost_howl")
    assert lh["won"] is True


def test_golden_read_cleanses_the_region():
    state = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    assert state.region_outcome == "cleansed"
    finale = next(b for b in state.beats if b["id"] == "corruption_avatar")
    assert finale["won"] is True
    assert "_TBD_" in finale["identity"]


def test_worst_read_fails_the_finale_but_loses_no_companion():
    state = frontier.run_frontier(seed=7, decider=frontier.worst_decider)
    assert state.region_outcome != "cleansed"     # the naive strategy fails
    assert set(state.party) == FULL_PARTY          # ...but nobody is lost


def test_choices_branch_flags_preparedness_and_clues():
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    worst = frontier.run_frontier(seed=7, decider=frontier.worst_decider)
    assert golden.preparedness > worst.preparedness
    assert golden.flags != worst.flags
    # The careful investigation surfaces the deeper foreshadowing clue.
    assert golden.flags.get("knows_source") is True
    assert worst.flags.get("knows_source") is not True
    assert golden.clues != worst.clues


def test_every_decision_is_recorded():
    state = frontier.run_frontier(seed=7)
    ids = {d["choice"] for d in state.decisions}
    assert {"ambush_response", "settlement_help", "forge_approach",
            "investigation_method", "woods_approach", "howl_response",
            "finale_strategy"} <= ids
    assert all(d["golden"] for d in state.decisions)   # golden decider


def test_anchor_showcases_win():
    state = frontier.run_frontier(seed=7)
    for b in state.beats:
        if b["id"] in ANCHORS:
            assert b["won"] is True, f"anchor {b['id']} should win: {b['outcome']}"


def test_every_combat_beat_produces_an_outcome():
    state = frontier.run_frontier(seed=7)
    for b in state.beats:
        if b["type"] in ("combat", "boss"):
            assert isinstance(b["outcome"], str) and b["outcome"]


def test_run_is_deterministic_for_a_seed_and_decider():
    a = frontier.run_frontier(seed=7)
    b = frontier.run_frontier(seed=7)
    assert [x["outcome"] for x in a.beats] == [x["outcome"] for x in b.beats]
    assert a.party == b.party and a.region_outcome == b.region_outcome


def test_manifest_matches_flow():
    man = frontier.slice_manifest()
    assert man["region"] == "The Frontier"
    assert man["beat_count"] == len(EXPECTED_BEATS)
    assert set(man["companions"]) == FULL_PARTY
    assert man["howl_goal"] == "rescued"
    assert man["finale_goal"] == "cleansed"
    assert man["finale"] == "The Corruption Avatar"
