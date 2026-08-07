"""Tests for the regional finale set-piece — **The Corruption Avatar**.

Validates the boss's core tactical lesson (break the wardstones before the
Avatar can be hurt) and its phase mechanic, using the canonical engine and the
reference party. Design evidence, not a re-test of engine internals.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tactical import showcase_corruption_avatar as ca


def test_encounter_builds_one_avatar_and_three_anchors():
    eng = ca.build_encounter()
    eng.start()
    assert ca._avatar(eng) is not None
    assert len(ca._anchors(eng)) == 3


def test_avatar_is_warded_while_anchors_stand():
    # While anchors live, the ward keeps the Avatar at full HP even if wounded.
    eng = ca.build_encounter()
    eng.start()
    avatar = ca._avatar(eng)
    avatar.hp = 10
    ca._apply_ward(eng)
    assert avatar.hp == avatar.max_hp


def test_avatar_exposed_and_enraged_when_all_anchors_fall():
    eng = ca.build_encounter()
    eng.start()
    avatar = ca._avatar(eng)
    base_ap = avatar.max_ap
    for a in ca._anchors(eng):
        a.hp = 0
    state = {"enraged": False}
    ca._enrage_if_exposed(eng, state)
    assert state["enraged"] is True
    assert avatar.max_ap == base_ap + 1
    # Now un-warded: a wounded Avatar stays wounded.
    avatar.hp = 10
    ca._apply_ward(eng)
    assert avatar.hp == 10


def test_breaking_the_wards_reliably_cleanses():
    rate = ca.outcome_rate(ca.siege_controller, "cleansed", seeds=20)
    assert rate >= 0.8, f"right read should reliably cleanse, got {rate:.2f}"


def test_tunneling_the_boss_never_cleanses():
    rate = ca.outcome_rate(ca.tunnel_controller, "cleansed", seeds=20)
    assert rate == 0.0, f"naive read must fail, got {rate:.2f}"


def test_good_preparedness_helps_and_golden_stays_winnable():
    prepared = ca.outcome_rate(ca.siege_controller, "cleansed", seeds=20, preparedness=1)
    rushed = ca.outcome_rate(ca.siege_controller, "cleansed", seeds=20, preparedness=-1)
    assert prepared >= rushed
    assert rushed >= 0.6, f"golden read must stay winnable even when rushed, got {rushed:.2f}"


def test_identity_is_reserved_tbd():
    man = ca.objective_manifest()
    assert "_TBD_" in man["name"]
    assert "manifestation" in man["framing"].lower()


def test_resolution_is_deterministic_for_a_seed():
    a = ca.resolve(ca.siege_controller, seed=3)[0]
    b = ca.resolve(ca.siege_controller, seed=3)[0]
    assert a == b
