"""Tests for the Frontier first-region vertical-slice orchestrator.

Verifies the end-to-end flow stitches recruitment/investigation beats between the
three existing showcases, reaches the full party, and lands the 'save, don't slay'
finale — deterministically. Combat is delegated to the canonical engine/showcases;
this suite does not re-test those internals.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tactical import frontier


EXPECTED_BEATS = [
    "road_in", "roadside_ambush", "settlement", "sundered_span",
    "forge_stand", "investigation", "corrupted_woods", "lost_howl",
]
FULL_PARTY = {"Ronan", "Talos", "Maeve Ashwood", "Torren",
              "Corwin", "Eleanor", "Ragash"}
ANCHORS = {"sundered_span", "forge_stand", "lost_howl"}


def test_all_eight_beats_run_in_order():
    state = frontier.run_frontier(seed=7)
    assert [b["id"] for b in state.beats] == EXPECTED_BEATS


def test_full_party_recruited_by_the_end():
    state = frontier.run_frontier(seed=7)
    assert set(state.party) == FULL_PARTY
    assert state.party[0] == "Ronan"          # Ronan starts with you


def test_finale_saves_the_lost_wolf():
    state = frontier.run_frontier(seed=7)
    assert state.ending == "rescued"
    lh = next(b for b in state.beats if b["id"] == "lost_howl")
    assert lh["won"] is True


def test_anchor_showcases_win():
    # The three separately-tested set-pieces are the reliable win-anchors.
    state = frontier.run_frontier(seed=7)
    for b in state.beats:
        if b["id"] in ANCHORS:
            assert b["won"] is True, f"anchor {b['id']} should win: {b['outcome']}"


def test_every_combat_beat_produces_an_outcome():
    state = frontier.run_frontier(seed=7)
    for b in state.beats:
        if b["type"] == "combat":
            assert isinstance(b["outcome"], str) and b["outcome"]


def test_recruitment_and_investigation_beats_advance_story():
    state = frontier.run_frontier(seed=7)
    settlement = next(b for b in state.beats if b["id"] == "settlement")
    assert settlement["type"] == "recruit" and "Maeve Ashwood" in settlement["recruited"]
    invest = next(b for b in state.beats if b["id"] == "investigation")
    assert invest["type"] == "investigate" and state.clues


def test_run_is_deterministic_for_a_seed():
    a = frontier.run_frontier(seed=7)
    b = frontier.run_frontier(seed=7)
    assert [x["outcome"] for x in a.beats] == [x["outcome"] for x in b.beats]
    assert a.party == b.party and a.ending == b.ending


def test_manifest_matches_flow():
    man = frontier.slice_manifest()
    assert man["region"] == "The Frontier"
    assert man["beat_count"] == len(EXPECTED_BEATS)
    assert set(man["companions"]) == FULL_PARTY
    assert man["finale_goal"] == "rescued"
