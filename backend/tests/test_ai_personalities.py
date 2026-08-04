"""Focused tests for the data-driven AI personality library and behavior memory.

Verifies:
    - fail-loud fallback when a blueprint references an undefined profile
    - all referenced ai_profiles resolve to non-empty definitions
    - distinct behaviors via _score_tile (hold / kite / flank / charge / fearless)
    - flee/morale (cowardly retreats, fearless holds, commander steadies)
    - behavior memory keys populated after take_turn (sticky targeting + turns_chasing)
    - reusability: no enemy-identity branching in tactical/ai.py
    - regression: auto_battle terminates for every canonical encounter group
    - combat_bridge.start_encounter(interactive=False) still terminates
"""
from __future__ import annotations

import copy
import json
import os
import random
import re
import sys

import pytest

sys.path.insert(0, "/app")

from tactical import ai, enemies
from tactical.battlefield import Battlefield
from tactical.engine import CombatEngine
from tactical.entities import Combatant
from tactical import encounters as tac_encounters


AI_PY = os.path.join("/app/tactical", "ai.py")


class _RNG:
    """Deterministic RNG stub."""
    def __init__(self, seed=0):
        self._r = random.Random(seed)
    def random(self):
        return self._r.random()
    def randint(self, a, b):
        return self._r.randint(a, b)


def _mk_engine(units, w=10, h=8, seed=0):
    bf = Battlefield(w, h, battlefield_id="t")
    engine = CombatEngine(bf, units, rng=_RNG(seed))
    engine.start()
    return engine


def _new_unit(name, team, x, y, profile_name=None, hp=30, mv=5, rng_=1,
              acc=0.9):
    u = Combatant(name, "guardian", team, x, y)
    u.max_hp = hp
    u.hp = hp
    u.max_move = mv
    u.move = mv
    u.attack_range = rng_
    u.accuracy = acc
    if profile_name is not None:
        u.ai_profile = copy.deepcopy(enemies.AI_PROFILES[profile_name])
        u.ai_memory = {}
    return u


# ---------------------------------------------------------------------------
# Profile library + fail-loud
# ---------------------------------------------------------------------------
class TestProfileLibrary:
    def test_all_referenced_profiles_defined_and_nonempty(self):
        for eid in enemies.list_enemies():
            resolved = enemies.resolve(eid)
            profile_name = resolved.get("ai_profile_name")
            assert profile_name in enemies.AI_PROFILES, (
                f"{eid} references undefined profile {profile_name!r}")
            assert enemies.AI_PROFILES[profile_name], (
                f"profile {profile_name!r} is empty")

    def test_bogus_profile_warns_and_falls_back(self, capsys):
        # Craft a temp blueprint with a bogus profile ref (monkeypatch dict)
        original = copy.deepcopy(enemies.BLUEPRINTS)
        enemies.BLUEPRINTS["_TEST_bogus"] = {
            "display_name": "Bogus", "archetype": "guardian",
            "stats": {"health": 10}, "attack": {"damage": 3, "range": 1},
            "ai_profile": "nonexistent_profile_xyz",
        }
        try:
            resolved = enemies.resolve("_TEST_bogus")
            captured = capsys.readouterr()
            assert "WARNING" in captured.err
            assert "nonexistent_profile_xyz" in captured.err
            # Falls back to aggressive_melee
            assert resolved["ai_profile"] == enemies.AI_PROFILES["aggressive_melee"] \
                or resolved["ai_profile"].get("preferred_range") == "melee"
        finally:
            enemies.BLUEPRINTS.clear()
            enemies.BLUEPRINTS.update(original)


# ---------------------------------------------------------------------------
# Distinct behaviours via _score_tile
# ---------------------------------------------------------------------------
class TestDistinctBehaviors:
    def _setup(self, prof_name):
        actor = _new_unit("A", "enemy", 5, 3, profile_name=prof_name)
        target = _new_unit("T", "player", 5, 5)
        target.facing = "N"
        engine = _mk_engine([actor, target])
        return engine, actor, target

    def test_defender_holds_ground(self):
        engine, actor, target = self._setup("defender")
        threats = set()
        # Roaming far from start is worse than staying
        far = (0, 0)
        near = actor.pos
        s_far = ai._score_tile(engine, actor, far, target, threats)
        s_near = ai._score_tile(engine, actor, near, target, threats)
        assert s_near > s_far

        # Compare with aggressive profile: aggressive scores the far tile
        # HIGHER than defender does
        actor2 = _new_unit("A2", "enemy", 5, 3, profile_name="aggressive")
        engine2 = _mk_engine([actor2, _new_unit("T2", "player", 5, 5)])
        s_far_agg = ai._score_tile(engine2, actor2, far,
                                   engine2.combatants[1], threats)
        assert s_far_agg > s_far

    def test_kiter_avoids_adjacent_foe(self):
        for prof in ("skirmisher", "caster"):
            actor = _new_unit("A", "enemy", 5, 3, profile_name=prof,
                              rng_=4)
            target = _new_unit("T", "player", 5, 5)
            engine = _mk_engine([actor, target])
            threats = set()
            adjacent = (5, 4)   # adjacent to target
            spaced = (5, 2)     # 3 away, still in range=4
            s_adj = ai._score_tile(engine, actor, adjacent, target, threats)
            s_spc = ai._score_tile(engine, actor, spaced, target, threats)
            assert s_spc > s_adj, f"{prof}: spaced={s_spc} adjacent={s_adj}"

    def test_flanker_prefers_rear(self):
        for prof in ("ambusher", "assassin", "hunter"):
            actor = _new_unit("A", "enemy", 5, 3, profile_name=prof,
                              rng_=(4 if prof == "hunter" else 1))
            target = _new_unit("T", "player", 5, 5)
            target.facing = "N"   # rear is south (+y)
            engine = _mk_engine([actor, target])
            threats = set()
            front_tile = (5, 4)      # in front of target
            rear_tile = (5, 6)       # behind target
            s_front = ai._score_tile(engine, actor, front_tile, target, threats)
            s_rear = ai._score_tile(engine, actor, rear_tile, target, threats)
            assert s_rear > s_front, f"{prof}: rear={s_rear} front={s_front}"

    def test_charger_closes_distance_harder(self):
        # Out of range tile: charger should score higher than non-charger
        threats = set()
        # Attacker out of range, target far away
        actor_c = _new_unit("C", "enemy", 0, 0, profile_name="brute")
        target_c = _new_unit("T", "player", 8, 6)
        engine_c = _mk_engine([actor_c, target_c])
        tile_close = (4, 3)
        tile_far = (1, 1)
        s_close_c = ai._score_tile(engine_c, actor_c, tile_close,
                                   target_c, threats)
        s_far_c = ai._score_tile(engine_c, actor_c, tile_far,
                                 target_c, threats)

        actor_n = _new_unit("N", "enemy", 0, 0, profile_name="aggressive_melee")
        target_n = _new_unit("T2", "player", 8, 6)
        engine_n = _mk_engine([actor_n, target_n])
        s_close_n = ai._score_tile(engine_n, actor_n, tile_close,
                                   target_n, threats)
        s_far_n = ai._score_tile(engine_n, actor_n, tile_far,
                                 target_n, threats)
        # The delta (close vs far) is larger for a charger
        assert (s_close_c - s_far_c) > (s_close_n - s_far_n)

    def test_fearless_ignores_threat_penalty(self):
        actor = _new_unit("A", "enemy", 5, 3, profile_name="berserker")
        target = _new_unit("T", "player", 5, 5)
        engine = _mk_engine([actor, target])
        tile = (5, 4)
        threats = {tile}
        s_threatened = ai._score_tile(engine, actor, tile, target, threats)
        s_safe = ai._score_tile(engine, actor, tile, target, set())
        assert s_threatened == s_safe  # fearless == no penalty

        # And a non-fearless profile DOES pay the penalty
        actor2 = _new_unit("A2", "enemy", 5, 3, profile_name="aggressive_melee")
        engine2 = _mk_engine([actor2, _new_unit("T2", "player", 5, 5)])
        s_t = ai._score_tile(engine2, actor2, tile,
                             engine2.combatants[1], {tile})
        s_c = ai._score_tile(engine2, actor2, tile,
                             engine2.combatants[1], set())
        assert s_c > s_t


# ---------------------------------------------------------------------------
# Flee / morale
# ---------------------------------------------------------------------------
class TestFleeMorale:
    def test_cowardly_low_hp_retreats(self):
        actor = _new_unit("C", "enemy", 5, 5, profile_name="cowardly",
                          hp=30, mv=5)
        target = _new_unit("T", "player", 5, 6)   # adjacent
        engine = _mk_engine([actor, target])
        actor.reset_turn()
        actor.hp = 5   # 5/30 ~ 17% < 0.5 threshold
        start_dist = abs(actor.x - target.x) + abs(actor.y - target.y)
        ai.take_turn(engine, actor)
        end_dist = abs(actor.x - target.x) + abs(actor.y - target.y)
        assert end_dist > start_dist, (
            f"cowardly did not retreat: start={start_dist} end={end_dist}")

    def test_fearless_at_1hp_does_not_flee(self):
        actor = _new_unit("F", "enemy", 5, 5, profile_name="berserker",
                          hp=30, mv=5)
        target = _new_unit("T", "player", 5, 6)
        engine = _mk_engine([actor, target])
        actor.reset_turn()
        actor.hp = 1
        start_pos = actor.pos
        ai.take_turn(engine, actor)
        # fearless never activates the retreat branch — should NOT flee
        end_dist = abs(actor.x - target.x) + abs(actor.y - target.y)
        # Berserker is a charger, so it will not increase distance
        assert end_dist <= 1

    def test_commander_nearby_halves_threshold(self):
        # Cowardly at ~35% hp: default threshold 0.5 -> flees.
        # With commander nearby -> threshold*0.5=0.25 -> should hold ground.
        actor = _new_unit("C", "enemy", 5, 5, profile_name="cowardly",
                          hp=100, mv=5)
        commander = _new_unit("Cmd", "enemy", 6, 5, profile_name="commander")
        target = _new_unit("T", "player", 5, 7)
        engine = _mk_engine([actor, commander, target])
        actor.reset_turn()
        actor.hp = 35   # 35% (< 0.5 -> would flee; > 0.25 with cmdr -> hold)
        start_dist = abs(actor.x - target.x) + abs(actor.y - target.y)
        ai.take_turn(engine, actor)
        end_dist = abs(actor.x - target.x) + abs(actor.y - target.y)
        assert actor.ai_memory.get("commander_nearby") is True
        # Held ground = did NOT increase distance to foe
        assert end_dist <= start_dist

    def test_low_morale_raises_threshold(self):
        # Team of two cowardly units, one dead -> alive_frac=0.5 (< 0.34? no).
        # Need alive_frac <= 0.34 -> team of 3 with 1 alive.
        c1 = _new_unit("C1", "enemy", 5, 5, profile_name="cowardly",
                       hp=100, mv=5)
        c2 = _new_unit("C2", "enemy", 4, 5, profile_name="cowardly", hp=100)
        c3 = _new_unit("C3", "enemy", 3, 5, profile_name="cowardly", hp=100)
        target = _new_unit("T", "player", 5, 7)
        engine = _mk_engine([c1, c2, c3, target])
        c2.hp = 0
        c3.hp = 0
        c1.reset_turn()
        c1.hp = 60   # 60%: default flee=0.5 -> hold; with morale low +0.15 -> 0.65 -> flees
        start_dist = abs(c1.x - target.x) + abs(c1.y - target.y)
        ai.take_turn(engine, c1)
        end_dist = abs(c1.x - target.x) + abs(c1.y - target.y)
        assert c1.ai_memory.get("morale") == "low"
        assert end_dist > start_dist


# ---------------------------------------------------------------------------
# Behavior memory + sticky targeting
# ---------------------------------------------------------------------------
class TestBehaviorMemory:
    def test_memory_keys_populated_after_turn(self):
        actor = _new_unit("A", "enemy", 3, 3, profile_name="aggressive_melee")
        target = _new_unit("T", "player", 6, 3)
        engine = _mk_engine([actor, target])
        actor.reset_turn()
        ai.take_turn(engine, actor)
        for k in ("target_id", "turns_chasing", "morale",
                  "commander_nearby", "currently_flanking"):
            assert k in actor.ai_memory, f"missing memory key {k}"

    def test_sticky_targeting_keeps_committed_target(self):
        actor = _new_unit("A", "enemy", 3, 3, profile_name="aggressive_melee")
        near = _new_unit("N", "player", 4, 3, hp=30)
        far = _new_unit("F", "player", 8, 3, hp=30)
        engine = _mk_engine([actor, near, far])
        # Commit to `far`
        actor.ai_memory["target_id"] = far.id
        chosen = ai._resolve_target(engine, actor)
        assert chosen.id == far.id

    def test_lowest_health_switches_when_weaker_appears(self):
        actor = _new_unit("A", "enemy", 3, 3, profile_name="skirmisher",
                          rng_=4)
        current = _new_unit("Cur", "player", 4, 3, hp=30)
        weak = _new_unit("Weak", "player", 5, 3, hp=30)
        engine = _mk_engine([actor, current, weak])
        actor.ai_memory["target_id"] = current.id
        # weak is at < 50% of current (30 -> 10)
        weak.hp = 10
        current.hp = 30
        chosen = ai._resolve_target(engine, actor)
        assert chosen.id == weak.id

    def test_turns_chasing_resets_in_range_and_increments_out(self):
        # Out of range -> increments
        actor = _new_unit("A", "enemy", 0, 0, profile_name="aggressive_melee",
                          rng_=1, mv=1)
        target = _new_unit("T", "player", 9, 7)
        engine = _mk_engine([actor, target])
        actor.reset_turn()
        ai.take_turn(engine, actor)
        assert actor.ai_memory.get("turns_chasing", 0) >= 1

        # Now in range -> resets to 0
        actor2 = _new_unit("A", "enemy", 5, 5, profile_name="aggressive_melee",
                           rng_=1)
        target2 = _new_unit("T", "player", 5, 6)
        engine2 = _mk_engine([actor2, target2])
        actor2.reset_turn()
        actor2.ai_memory["turns_chasing"] = 4
        ai.take_turn(engine2, actor2)
        assert actor2.ai_memory["turns_chasing"] == 0


# ---------------------------------------------------------------------------
# Reusability: no enemy-specific branching
# ---------------------------------------------------------------------------
class TestReusability:
    def test_no_enemy_identity_branching_in_ai_py(self):
        with open(AI_PY, "r", encoding="utf-8") as fh:
            src = fh.read()
        # Strip comments/docstrings before searching
        code = re.sub(r'"""[\s\S]*?"""', "", src)
        code = re.sub(r"'''[\s\S]*?'''", "", code)
        code = re.sub(r"#.*", "", code)
        offenders = []
        for tok in ("goblin", "skeleton", "orc", "kobold", "bandit",
                    "wolf", "spider", "zombie", "necromancer"):
            # allow lowercase profile refs like "necromancer" only inside
            # AI_PROFILES access -- but ai.py doesn't reference profile names
            # by string; the actual profile keys are read via .get() flags,
            # not name checks.
            if re.search(rf"\b{tok}\b", code, re.IGNORECASE):
                offenders.append(tok)
        assert not offenders, f"enemy-identity branching found: {offenders}"


# ---------------------------------------------------------------------------
# Regression: auto_battle terminates
# ---------------------------------------------------------------------------
class TestRegression:
    @pytest.mark.parametrize("group_id", [
        "forest_wolf_pack", "roadside_ambush", "ruins_undead",
        "goblin_camp", "cave_swarm", "orc_warband", "corrupted_incursion",
    ])
    def test_auto_battle_terminates(self, group_id):
        bf = Battlefield(10, 8, battlefield_id=f"reg_{group_id}")
        # Player party
        party = []
        for i in range(2):
            p = Combatant(f"P{i}", "guardian", "player", 0, i)
            party.append(p)
        foes = tac_encounters.build_group(group_id, battlefield=bf)
        engine = CombatEngine(bf, party + foes, rng=_RNG(42))
        outcome = engine.auto_battle(max_rounds=30)
        assert outcome in ("player", "enemy", "draw")
        # Any 'draw' means it hit max_rounds - allowed but flag for report
        assert engine.round <= 30

    def test_combat_bridge_headless(self):
        # Minimal world state to run start_encounter(interactive=False)
        import combat_bridge
        outcome = combat_bridge.start_encounter(
            region=None, group_id="roadside_ambush", interactive=False)
        assert outcome in ("player", "enemy", "draw")

    def test_all_blueprints_spawn(self):
        for eid in enemies.list_enemies():
            u = enemies.spawn_enemy(eid, 0, 0)
            assert u.alive
            assert isinstance(u.ai_profile, dict) and u.ai_profile
