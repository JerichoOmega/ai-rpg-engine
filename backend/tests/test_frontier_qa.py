"""Adversarial QA — First Region vertical slice (Frontier flow + Corruption Avatar).

An *adversarial* pass: rather than confirming the happy path, this suite tries to
break the slice. It exercises **every** choice combination, the preparedness math,
soft-lock / no-permanent-loss guarantees, the boss ward/expose/enrage invariants,
data-roster integrity, and the engine-interface / layer-rule discipline (no UI/IO
in the core). Design/validation code — canonical engine/AI untouched.
"""

import itertools
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tactical import frontier as F
from tactical import showcase_corruption_avatar as CA
from tactical import enemies as E

FULL_PARTY = {"Ronan", "Talos", "Maeve Ashwood", "Torren",
              "Corwin", "Eleanor", "Ragash"}
CHOICE_IDS = ["ambush_response", "settlement_help", "forge_approach",
              "investigation_method", "woods_approach", "howl_response",
              "finale_strategy"]
VALID_REGION = {"cleansed", "held", "overwhelmed"}
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _decider(picks):
    """picks: dict choice_id -> 'golden'|'other'."""
    def d(state, choice):
        if picks.get(choice.id, "golden") == "golden":
            return choice.golden_id()
        return next((o["id"] for o in choice.options if not o.get("golden")),
                    choice.golden_id())
    return d


# ---------------------------------------------------------------------------
# 1. Every one of the 128 choice combinations is safe (no soft locks)
# ---------------------------------------------------------------------------
def test_all_128_choice_combinations_are_safe():
    for combo in itertools.product(["golden", "other"], repeat=len(CHOICE_IDS)):
        picks = dict(zip(CHOICE_IDS, combo))
        state = F.run_frontier(seed=7, decider=_decider(picks))
        # No permanent companion loss under ANY combination.
        assert set(state.party) == FULL_PARTY, picks
        assert state.party[0] == "Ronan"
        # Ronan's climax always saves Bram (canonical character beat).
        assert state.howl_ending == "rescued", picks
        # The region always resolves to a real, valid state (never crashes/None).
        assert state.region_outcome in VALID_REGION, (picks, state.region_outcome)
        # The naive finale read must never win, no matter how well-prepared.
        if picks["finale_strategy"] == "other":
            assert state.region_outcome != "cleansed", picks
        assert -3 <= state.preparedness <= 6, (picks, state.preparedness)
        # 9 beats, all recorded with an outcome.
        assert len(state.beats) == 9
        for b in state.beats:
            assert isinstance(b["outcome"], str) and b["outcome"]


# ---------------------------------------------------------------------------
# 2. Preparedness math is exact at both extremes
# ---------------------------------------------------------------------------
def test_preparedness_extremes_are_exact():
    assert F.run_frontier(seed=7, decider=F.golden_decider).preparedness == 6
    assert F.run_frontier(seed=7, decider=F.worst_decider).preparedness == -3


def test_recruitment_never_gated_by_a_lost_skirmish():
    # Even if a travel skirmish is lost, the recruitment it carries still happens.
    state = F.run_frontier(seed=7)
    for b in state.beats:
        if b.get("recruited"):
            for name in b["recruited"]:
                assert name in state.party


# ---------------------------------------------------------------------------
# 3. Golden read robust across seeds; worst read fails but never loses anyone
# ---------------------------------------------------------------------------
def test_golden_read_cleanses_across_many_seeds():
    outs = [F.run_frontier(seed=s, decider=F.golden_decider).region_outcome
            for s in range(20)]
    assert all(o == "cleansed" for o in outs), outs


def test_worst_read_never_cleanses_but_party_intact_across_seeds():
    for s in range(20):
        st = F.run_frontier(seed=s, decider=F.worst_decider)
        assert st.region_outcome != "cleansed"
        assert set(st.party) == FULL_PARTY


# ---------------------------------------------------------------------------
# 4. Determinism (same seed + decider => identical run)
# ---------------------------------------------------------------------------
def test_full_run_is_deterministic():
    a = F.run_frontier(seed=13)
    b = F.run_frontier(seed=13)
    assert [x["outcome"] for x in a.beats] == [x["outcome"] for x in b.beats]
    assert a.party == b.party and a.flags == b.flags and a.clues == b.clues
    assert a.decisions == b.decisions and a.region_outcome == b.region_outcome


# ---------------------------------------------------------------------------
# 5. Boss ward / expose / enrage invariants under adversarial states
# ---------------------------------------------------------------------------
def test_ward_restores_repeatedly_while_any_anchor_stands():
    eng = CA.build_encounter()
    eng.start()
    avatar = CA._avatar(eng)
    anchors = CA._anchors(eng)
    # Kill two of three — still warded.
    anchors[0].hp = 0
    anchors[1].hp = 0
    for _ in range(5):
        avatar.hp = 1
        CA._apply_ward(eng)
        assert avatar.hp == avatar.max_hp


def test_enrage_fires_exactly_once():
    eng = CA.build_encounter()
    eng.start()
    avatar = CA._avatar(eng)
    base_ap = avatar.max_ap
    for a in CA._anchors(eng):
        a.hp = 0
    state = {"enraged": False}
    CA._enrage_if_exposed(eng, state)
    CA._enrage_if_exposed(eng, state)   # second call must be a no-op
    assert avatar.max_ap == base_ap + 1


def test_no_win_path_for_tunnelling_even_when_fully_prepared():
    assert CA.outcome_rate(CA.tunnel_controller, "cleansed", seeds=30,
                           preparedness=6) == 0.0


def test_correct_read_stays_winnable_at_worst_reachable_preparedness():
    # -3 is the worst preparedness the Frontier flow can hand the finale.
    rate = CA.outcome_rate(CA.siege_controller, "cleansed", seeds=30,
                           preparedness=-3)
    assert rate >= 0.6, f"golden read must stay winnable when rushed, got {rate:.2f}"


def test_difficulty_gradient_is_monotone_ish():
    prepared = CA.outcome_rate(CA.siege_controller, "cleansed", seeds=30, preparedness=2)
    neutral = CA.outcome_rate(CA.siege_controller, "cleansed", seeds=30, preparedness=0)
    rushed = CA.outcome_rate(CA.siege_controller, "cleansed", seeds=30, preparedness=-3)
    assert prepared >= neutral >= rushed


# ---------------------------------------------------------------------------
# 6. Engine-interface / layer discipline (Godot-migration readiness)
# ---------------------------------------------------------------------------
def test_core_modules_carry_no_ui_or_io():
    for rel in ("tactical/frontier.py", "tactical/showcase_corruption_avatar.py"):
        src = open(os.path.join(_ROOT, rel), encoding="utf-8").read()
        assert not re.search(r"\binput\s*\(", src), f"{rel} must not read input()"
        assert not re.search(r"\bprint\s*\(", src), f"{rel} must not print()"


def test_terminal_ui_lives_in_the_presentation_script():
    src = open(os.path.join(_ROOT, "scripts/play_frontier.py"), encoding="utf-8").read()
    assert "input(" in src and "print(" in src   # the UI belongs here, not in core


# ---------------------------------------------------------------------------
# 7. Data-roster integrity (the additive boss blueprints)
# ---------------------------------------------------------------------------
def test_enemies_json_is_valid_and_ids_match_keys():
    path = os.path.join(_ROOT, "tactical/data/enemies.json")
    data = json.load(open(path, encoding="utf-8"))
    for key, bp in data.items():
        if "id" in bp:
            assert bp["id"] == key, key


def test_all_blueprints_resolve_and_spawnable_count():
    for k in E.BLUEPRINTS:
        E.resolve(k)                       # must not raise
    assert len(E.list_enemies()) == 76


def test_boss_and_anchor_blueprints_are_well_formed():
    av = E.resolve("corruption_avatar")
    assert av["ai_profile_name"] == "boss" and av["tier"] == "boss"
    an = E.resolve("corruption_anchor")
    assert an["ai_profile_name"] == "defender" and an["stats"]["movement"] == 0
    # Tag inheritance + query helpers see them.
    assert {"corruption_avatar", "corruption_anchor"} <= set(E.by_tag("Frontier"))
    # Spawn works; the abstract base does not.
    assert E.spawn_enemy("corruption_avatar", 0, 0).name == "The Corruption Avatar"
    try:
        E.spawn_enemy("enemy", 0, 0)
        assert False, "abstract base 'enemy' must not be spawnable"
    except ValueError:
        pass


def test_avatar_identity_is_reserved_tbd():
    av = E.resolve("corruption_avatar")
    assert "_TBD_identity" in av["traits"]
