"""The Lost Howl climax — regression + design proof for the 'save, don't slay'
objective swap. Design/validation only; no shared gameplay systems change."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tactical import showcase_lost_howl as lh  # noqa: E402


def test_encounter_cast_and_setup():
    eng = lh.build_encounter()
    assert lh._lost_wolf(eng) is not None
    assert lh._alpha(eng) is not None
    protectors = {p.name for p in lh._protectors(eng)}
    assert protectors == {"Ronan", "Talos", "Eleanor"}
    # The Lost Wolf is a real, dangerous threat (so standing around isn't free).
    assert lh._lost_wolf(eng).max_hp >= 60


def test_alpha_starts_offset_and_arrives_later():
    eng = lh.build_encounter()
    alpha, lost = lh._alpha(eng), lh._lost_wolf(eng)
    # Alpha begins far from the wolf; the objective swap is gated on a later round.
    from tactical.inspection import chebyshev
    assert chebyshev(alpha.pos, lost.pos) > 1
    assert lh.ALPHA_ARRIVES_ROUND >= 2


def test_compassion_play_rescues_the_lost_wolf():
    # Subdue-not-slay reliably reaches the design-goal ending.
    rate = lh.outcome_rate(lh.compassion_controller, "rescued", seeds=20)
    assert rate >= 0.9, f"compassion rescue rate too low: {rate:.0%}"


def test_murderhobo_play_kills_the_wolf_and_fails():
    # Naive 'defeat the beast' reaches the tragic failure state.
    rate = lh.outcome_rate(lh.murderhobo_controller, "slain", seeds=20)
    assert rate >= 0.9, f"murder-hobo slain rate too low: {rate:.0%}"


def test_rescue_requires_a_living_wolf():
    outcome, eng = lh.resolve(lh.compassion_controller, seed=0)
    assert outcome == "rescued"
    assert lh._lost_wolf(eng).alive


def test_objective_manifest_documents_the_swap():
    m = lh.objective_manifest()
    assert m["initial_objective"] == "Defeat the Beast"
    assert "Protect the Lost Wolf" in m["swapped_objective"]
    assert "sav" in m["design_goal"].lower()
