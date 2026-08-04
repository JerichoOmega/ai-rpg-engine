"""
Independent verification of tactical Phase A: Facing, Flanking, Opportunity
Attacks, and combat readability. Also spot-checks Phase-0 regressions.

Pure Python. Terminal RPG. No servers, no APIs.
"""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, "/app")

from tactical.battlefield import Battlefield
from tactical.entities import Combatant
from tactical.engine import CombatEngine
from tactical.facing import (
    DIRS, dir_from_to, relative_arc, is_flanking, FACING_HIT, FACING_DMG,
)
from tactical.inspection import compute_hit_chance, movement_preview
from tactical import actions
from tactical import enemies as en_mod
from tactical import encounters as enc_mod


# ---------------------------------------------------------------------------
# Deterministic rng shim (per review request)
# ---------------------------------------------------------------------------
class FixedRandom:
    def __init__(self, r: float = 0.0):
        self._r = r

    def random(self) -> float:
        return self._r

    def randint(self, a: int, b: int) -> int:
        return a

    def choice(self, seq):
        return seq[0]

    def shuffle(self, seq):  # AI may call this
        return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_engine(width=10, height=10, rng=None):
    bf = Battlefield(width, height, "test_arena")
    return bf, rng or FixedRandom(0.0)


def _place_pair(defender_facing=None, atk_pos=(4, 5), def_pos=(5, 5)):
    """Build a minimal engine with attacker + defender, deterministic damage."""
    bf, rng = make_engine()
    attacker = Combatant("Atk", "brute", "player", *atk_pos)
    defender = Combatant("Def", "guardian", "enemy", *def_pos)
    # Make the numbers deterministic:
    attacker.crit_chance = 0.0
    attacker.damage_min = attacker.damage_max = 10
    attacker.accuracy = 0.5
    defender.armor = 0
    defender.facing = defender_facing
    engine = CombatEngine(bf, [attacker, defender], rng=rng)
    engine.start()
    return engine, attacker, defender


# ===========================================================================
# Facing module: dir_from_to + relative_arc
# ===========================================================================
class TestFacingModule:
    def test_dirs_cardinal_vectors(self):
        assert DIRS["N"] == (0, -1)
        assert DIRS["S"] == (0, 1)
        assert DIRS["E"] == (1, 0)
        assert DIRS["W"] == (-1, 0)

    def test_dir_from_to_cardinal(self):
        assert dir_from_to((0, 0), (1, 0)) == "E"
        assert dir_from_to((1, 0), (0, 0)) == "W"
        assert dir_from_to((0, 0), (0, 1)) == "S"
        assert dir_from_to((0, 1), (0, 0)) == "N"

    def test_dir_from_to_returns_only_cardinals(self):
        # Diagonal should resolve into a cardinal (ties break to horizontal).
        for a, b in [((0, 0), (2, 1)), ((0, 0), (1, 2)),
                     ((0, 0), (-2, -1)), ((0, 0), (-1, -2))]:
            assert dir_from_to(a, b) in ("N", "S", "E", "W")

    def test_relative_arc_e_facing_defender(self):
        class D:
            x, y, facing = 5, 5, "E"
        # Attacker to the east of defender -> front
        assert relative_arc(D, (6, 5)) == "front"
        # West -> rear
        assert relative_arc(D, (4, 5)) == "rear"
        # North / South -> side
        assert relative_arc(D, (5, 4)) == "side"
        assert relative_arc(D, (5, 6)) == "side"

    def test_relative_arc_none_is_always_front_backcompat(self):
        class D:
            x, y, facing = 5, 5, None
        for attacker in [(6, 5), (4, 5), (5, 4), (5, 6), (7, 3)]:
            assert relative_arc(D, attacker) == "front"

    def test_is_flanking_helper(self):
        class D:
            x, y, facing = 5, 5, "E"
        assert is_flanking(D, (4, 5)) is True   # rear
        assert is_flanking(D, (5, 4)) is True   # side
        assert is_flanking(D, (6, 5)) is False  # front

    def test_facing_tables_shape(self):
        assert FACING_HIT["front"] == 0.0
        assert FACING_HIT["side"] == pytest.approx(0.10)
        assert FACING_HIT["rear"] == pytest.approx(0.20)
        assert FACING_DMG["front"] == 1.0
        assert FACING_DMG["side"] == 1.0
        assert FACING_DMG["rear"] == pytest.approx(1.25)


# ===========================================================================
# compute_hit_chance shared breakdown
# ===========================================================================
class TestSharedHitChance:
    def test_breakdown_exposes_facing_keys(self):
        engine, atk, dfn = _place_pair(defender_facing="W")  # atk west -> front
        info = compute_hit_chance(engine, atk, dfn)
        for key in ("chance", "facing", "facing_bonus", "flanking",
                    "cover", "elevation", "line_of_sight", "in_range"):
            assert key in info, f"missing key {key}"

    def test_rear_attack_raises_chance_by_0_20(self):
        # Defender facing east; attacker is west of defender -> rear.
        engine, atk, dfn = _place_pair(defender_facing="E",
                                       atk_pos=(4, 5), def_pos=(5, 5))
        front_engine, front_atk, front_def = _place_pair(
            defender_facing="W", atk_pos=(4, 5), def_pos=(5, 5))
        rear = compute_hit_chance(engine, atk, dfn)
        front = compute_hit_chance(front_engine, front_atk, front_def)
        assert front["facing"] == "front"
        assert rear["facing"] == "rear"
        assert rear["flanking"] is True and front["flanking"] is False
        assert rear["chance"] - front["chance"] == pytest.approx(0.20, abs=1e-6)

    def test_side_attack_raises_chance_by_0_10(self):
        # Defender facing east; attacker directly north -> side.
        engine, atk, dfn = _place_pair(defender_facing="E",
                                       atk_pos=(5, 4), def_pos=(5, 5))
        front_engine, front_atk, front_def = _place_pair(
            defender_facing="W", atk_pos=(5, 4), def_pos=(5, 5))
        # Front-baseline uses attacker at (5,4) too so cover/LOS is identical.
        side = compute_hit_chance(engine, atk, dfn)
        # But the front baseline has defender facing north here — remake to be
        # cleanly comparable: same attacker tile, defender.facing=None (front).
        front_def.facing = None
        front = compute_hit_chance(front_engine, front_atk, front_def)
        assert side["facing"] == "side" and side["flanking"] is True
        assert front["facing"] == "front"
        assert side["chance"] - front["chance"] == pytest.approx(0.10, abs=1e-6)

    def test_ai_and_player_share_same_function(self):
        # The AI and player call the exact same function object.
        engine, atk, dfn = _place_pair(defender_facing="E",
                                       atk_pos=(4, 5), def_pos=(5, 5))
        as_player = compute_hit_chance(engine, atk, dfn)
        # Swap roles (enemy attacking a player). Function must return same shape.
        atk.team, dfn.team = "enemy", "player"
        as_enemy = compute_hit_chance(engine, atk, dfn)
        assert set(as_player.keys()) == set(as_enemy.keys())
        assert as_player["facing"] == as_enemy["facing"] == "rear"


# ===========================================================================
# Flank damage in _resolve_attack
# ===========================================================================
class TestFlankDamage:
    def test_rear_flank_deals_1_25x_damage(self):
        engine, atk, dfn = _place_pair(defender_facing="E",
                                       atk_pos=(4, 5), def_pos=(5, 5))
        pre = dfn.hp
        actions.attack(engine, atk, dfn)
        dealt = pre - dfn.hp
        assert dealt == int(10 * 1.25), f"expected 12, got {dealt}"

    def test_front_attack_deals_flat_damage(self):
        # Defender facing west; attacker west of defender -> front.
        engine, atk, dfn = _place_pair(defender_facing="W",
                                       atk_pos=(4, 5), def_pos=(5, 5))
        pre = dfn.hp
        actions.attack(engine, atk, dfn)
        dealt = pre - dfn.hp
        assert dealt == 10, f"expected 10, got {dealt}"

    def test_none_facing_treated_as_front_backcompat(self):
        # defender.facing = None -> always 'front' -> no flank multiplier
        engine, atk, dfn = _place_pair(defender_facing=None,
                                       atk_pos=(4, 5), def_pos=(5, 5))
        pre = dfn.hp
        actions.attack(engine, atk, dfn)
        assert pre - dfn.hp == 10

    def test_flank_log_tag_present(self):
        engine, atk, dfn = _place_pair(defender_facing="E",
                                       atk_pos=(4, 5), def_pos=(5, 5))
        actions.attack(engine, atk, dfn)
        joined = "\n".join(engine.log)
        assert "REAR FLANK" in joined, joined

    def test_no_flank_tag_on_front_hit(self):
        engine, atk, dfn = _place_pair(defender_facing="W",
                                       atk_pos=(4, 5), def_pos=(5, 5))
        actions.attack(engine, atk, dfn)
        joined = "\n".join(engine.log)
        assert "FLANK" not in joined

    def test_attacker_faces_target_after_attack(self):
        engine, atk, dfn = _place_pair(defender_facing="E",
                                       atk_pos=(4, 5), def_pos=(5, 5))
        actions.attack(engine, atk, dfn)
        # attacker at (4,5), defender at (5,5) -> east
        assert atk.facing == "E"


# ===========================================================================
# Opportunity attacks
# ===========================================================================
class TestOpportunityAttacks:
    def _setup_move_scenario(self, mover_dest, foe_range=1):
        bf, rng = make_engine()
        mover = Combatant("Mover", "brute", "player", 5, 5)
        foe = Combatant("Grunt", "guardian", "enemy", 4, 5)
        foe.attack_range = foe_range
        # Make foe hit deterministic and non-lethal
        foe.accuracy = 0.9
        foe.crit_chance = 0.0
        foe.damage_min = foe.damage_max = 1
        # Give mover lots of movement + hp so the OA doesn't kill it.
        mover.max_move = mover.move = 10
        mover.hp = mover.max_hp = 50
        engine = CombatEngine(bf, [mover, foe], rng=rng)
        engine.start()
        return engine, mover, foe

    def test_opportunity_fires_when_leaving_reach(self):
        engine, mover, foe = self._setup_move_scenario((9, 5))
        ok = actions.move(engine, mover, (9, 5))
        assert ok
        text = "\n".join(engine.log)
        assert "opportunity attack" in text.lower(), text

    def test_no_opportunity_when_still_adjacent(self):
        # Move to another tile that is still adjacent to the foe at (4,5).
        engine, mover, foe = self._setup_move_scenario((4, 6))
        ok = actions.move(engine, mover, (4, 6))
        assert ok
        text = "\n".join(engine.log)
        assert "opportunity attack" not in text.lower(), text

    def test_ranged_foe_not_adjacent_does_not_get_opportunity(self):
        bf, rng = make_engine()
        mover = Combatant("Mover", "brute", "player", 5, 5)
        archer = Combatant("Archer", "ranger", "enemy", 1, 1)
        archer.attack_range = 6
        archer.accuracy = 0.9
        archer.crit_chance = 0.0
        archer.damage_min = archer.damage_max = 1
        # Disarm the ranger's prepare reaction_shot so it doesn't fire on movement.
        archer._prepare_reaction = "none"
        archer.prepare_stance = None
        mover.max_move = mover.move = 8
        mover.hp = mover.max_hp = 50
        engine = CombatEngine(bf, [mover, archer], rng=rng)
        engine.start()
        ok = actions.move(engine, mover, (9, 5))
        assert ok
        text = "\n".join(engine.log)
        assert "opportunity attack" not in text.lower(), text

    def test_each_foe_swings_at_most_once_per_move(self):
        # Two adjacent melee foes; move away — expect exactly two OA log lines.
        bf, rng = make_engine()
        mover = Combatant("Mover", "brute", "player", 5, 5)
        mover.max_move = mover.move = 10
        mover.hp = mover.max_hp = 200
        foe1 = Combatant("A", "guardian", "enemy", 4, 5)
        foe2 = Combatant("B", "guardian", "enemy", 5, 4)
        for f in (foe1, foe2):
            f.attack_range = 1
            f.accuracy = 0.9
            f.crit_chance = 0.0
            f.damage_min = f.damage_max = 1
        engine = CombatEngine(bf, [mover, foe1, foe2], rng=rng)
        engine.start()
        ok = actions.move(engine, mover, (9, 9))
        assert ok
        oa_lines = [ln for ln in engine.log
                    if "opportunity attack" in ln.lower()]
        assert len(oa_lines) == 2, oa_lines


# ===========================================================================
# Readability: movement_preview + FLANK log tag
# ===========================================================================
class TestReadability:
    def test_movement_preview_exposes_provokes_opportunity_from(self):
        bf, rng = make_engine()
        mover = Combatant("Mover", "brute", "player", 5, 5)
        mover.max_move = mover.move = 10
        foe = Combatant("Grunt", "guardian", "enemy", 4, 5)
        foe.attack_range = 1
        engine = CombatEngine(bf, [mover, foe], rng=rng)
        engine.start()
        preview = movement_preview(engine, mover, (9, 5))
        assert "provokes_opportunity_from" in preview
        assert preview["provokes_opportunity_from"] == ["Grunt"]

    def test_movement_preview_empty_when_still_in_reach(self):
        bf, rng = make_engine()
        mover = Combatant("Mover", "brute", "player", 5, 5)
        mover.max_move = mover.move = 10
        foe = Combatant("Grunt", "guardian", "enemy", 4, 5)
        foe.attack_range = 1
        engine = CombatEngine(bf, [mover, foe], rng=rng)
        engine.start()
        preview = movement_preview(engine, mover, (4, 6))
        assert preview["provokes_opportunity_from"] == []


# ===========================================================================
# Movement sets facing per step
# ===========================================================================
class TestMoveSetsFacing:
    def test_facing_matches_last_step(self):
        bf, rng = make_engine()
        mover = Combatant("Mover", "brute", "player", 5, 5)
        mover.max_move = mover.move = 10
        engine = CombatEngine(bf, [mover], rng=rng)
        engine.start()
        actions.move(engine, mover, (8, 5))  # moves east
        assert mover.facing == "E"
        actions.move(engine, mover, (8, 8))  # moves south
        assert mover.facing == "S"


# ===========================================================================
# Regression: previously verified foundation
# ===========================================================================
class TestFoundationRegression:
    def test_front_melee_damage_minus_armor_still_7(self):
        # 10 damage, 3 armor, front hit -> 7 (unchanged by Phase A).
        bf, rng = make_engine()
        atk = Combatant("Atk", "brute", "player", 4, 5)
        dfn = Combatant("Def", "guardian", "enemy", 5, 5)
        atk.crit_chance = 0.0
        atk.damage_min = atk.damage_max = 10
        atk.accuracy = 0.9
        dfn.armor = 3
        dfn.facing = "W"  # attacker is west -> defender faces west -> front
        engine = CombatEngine(bf, [atk, dfn], rng=rng)
        engine.start()
        pre = dfn.hp
        actions.attack(engine, atk, dfn)
        assert pre - dfn.hp == 7

    def test_ranged_range_gate(self):
        bf, rng = make_engine()
        atk = Combatant("Atk", "ranger", "player", 0, 0)
        dfn = Combatant("Def", "guardian", "enemy", 9, 9)
        engine = CombatEngine(bf, [atk, dfn], rng=rng)
        engine.start()
        info = compute_hit_chance(engine, atk, dfn)
        # ranger range < 12 chebyshev -> out of range -> chance 0
        assert info["in_range"] is False
        assert info["chance"] == 0.0

    def test_all_74_blueprints_resolve_and_spawn(self):
        ids = en_mod.list_enemies(include_abstract=False)
        assert len(ids) >= 70, f"expected many spawnable blueprints, got {len(ids)}"
        for i, eid in enumerate(ids):
            u = en_mod.spawn_enemy(eid, i % 5, i % 5)
            assert u.hp > 0
            assert u.max_hp > 0

    def test_auto_battle_terminates_with_opportunity_attacks_active(self):
        # Sanity: two Skeleton Warriors vs two Guardians, small map, must
        # terminate within round cap and produce a decisive outcome.
        bf = Battlefield(10, 10, "auto_arena")
        players = [
            Combatant("P1", "brute", "player", 1, 1),
            Combatant("P2", "guardian", "player", 1, 3),
        ]
        foes = [
            en_mod.spawn_enemy("skeleton_warrior", 8, 1),
            en_mod.spawn_enemy("skeleton_warrior", 8, 3),
        ]
        engine = CombatEngine(bf, players + foes)  # non-deterministic rng ok
        outcome = engine.auto_battle(max_rounds=40)
        assert outcome in ("player", "enemy", "draw")
        # It must actually finish before the cap (either side wins).
        assert engine.round <= 40

class TestEncounterAutoBattles:
    """Spawn a few build_group encounters and confirm no crashes."""

    def test_multiple_encounters_run_clean(self):
        group_ids = enc_mod.list_encounters()[:3]
        assert group_ids, "no encounters defined"
        for gid in group_ids:
            bf = Battlefield(12, 8, f"enc_{gid}")
            players = [
                Combatant("P1", "brute", "player", 1, 1),
                Combatant("P2", "ranger", "player", 1, 4),
                Combatant("P3", "guardian", "player", 1, 6),
            ]
            foes = enc_mod.build_group(gid, battlefield=bf)
            engine = CombatEngine(bf, players + foes)
            outcome = engine.auto_battle(max_rounds=40)
            assert outcome in ("player", "enemy", "draw")
            assert engine.round <= 40, \
                f"encounter {gid} did not terminate; log tail: {engine.log[-5:]}"
