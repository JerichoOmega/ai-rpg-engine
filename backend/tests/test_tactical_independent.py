"""Independent behavioural verification of tactical/ package.

Written from scratch (not re-running tactical.verify) to confirm the
foundation behaves per /app/Combat_Gameplay_Architecture.md.
"""
import os
import sys
import json
import pytest

sys.path.insert(0, "/app")

from tactical.battlefield import Battlefield  # noqa: E402
from tactical.entities import Combatant, equip_ability, LoadoutLockedError  # noqa: E402
from tactical.engine import CombatEngine, CombatContext  # noqa: E402
from tactical import actions, enemies, encounters, demo  # noqa: E402


class FixedRandom:
    """Deterministic rng compatible with random.Random surface used by engine."""
    def __init__(self, val=0.0):
        self.val = val

    def random(self):
        return self.val

    def randint(self, a, b):
        return a  # min damage roll -> deterministic


# ---------------------------------------------------------------------------
# (a) Line of Sight
# ---------------------------------------------------------------------------
class TestLineOfSight:
    def test_tree_blocks_los_at_equal_elevation(self):
        bf = Battlefield(6, 3, "los1")
        bf.tile(3, 1).add_object("pine_tree")
        assert bf.line_of_sight((0, 1), (5, 1)) is False

    def test_cliff_top_sees_over_tree(self):
        bf = Battlefield(6, 3, "los2")
        bf.set_terrain(0, 1, "cliff_top", elevation=2)
        bf.tile(3, 1).add_object("pine_tree")
        assert bf.line_of_sight((0, 1), (5, 1)) is True

    def test_clear_los(self):
        bf = Battlefield(6, 3, "los3")
        assert bf.line_of_sight((0, 1), (5, 1)) is True


# ---------------------------------------------------------------------------
# (b) Pathfinding & reachability
# ---------------------------------------------------------------------------
class TestPathing:
    def test_path_routes_around_boulder_wall(self):
        bf = Battlefield(7, 5, "pf")
        # Wall of boulders at x=3 for y in 0..2, gap at y=3
        for y in range(3):
            bf.tile(3, y).add_object("boulder")
        p = bf.path((0, 1), (6, 1), ap=30)
        assert p is not None
        # Must not pass through any impassable boulder tile
        for step in p:
            t = bf.tile(*step)
            assert t.is_passable() or step == (6, 1)
        # Must use the gap at y=3
        assert any(step[1] == 3 for step in p)

    def test_reachable_respects_ap_budget(self):
        bf = Battlefield(10, 10, "pf2")
        reach = bf.reachable((5, 5), ap=2)
        # A tile 3 away (manhattan) must NOT be reachable with ap=2
        assert (5, 8) not in reach
        assert (5, 6) in reach  # 1 tile away
        assert (5, 5) in reach

    def test_path_none_when_blocked(self):
        bf = Battlefield(5, 3, "pf3")
        for y in range(3):
            bf.tile(2, y).add_object("boulder")
        assert bf.path((0, 1), (4, 1), ap=30) is None


# ---------------------------------------------------------------------------
# (c) Melee attack: damage=(dmg-armor,min 1), AP spend, forced miss
# ---------------------------------------------------------------------------
class TestAttack:
    def _setup(self, rng_val):
        bf = Battlefield(5, 3, "atk")
        atk = Combatant("Atk", "guardian", "player", 1, 1)
        deff = Combatant("Def", "guardian", "enemy", 2, 1)
        atk.crit_chance = 0.0
        deff.crit_chance = 0.0
        eng = CombatEngine(bf, [atk, deff], rng=FixedRandom(rng_val))
        eng.start()
        return eng, atk, deff

    def test_hit_reduces_hp_by_damage_minus_armor(self):
        eng, atk, deff = self._setup(0.0)  # always hit, min damage
        deff.armor = 2
        atk.damage_min = 5
        atk.damage_max = 5
        start_hp = deff.hp
        ap_before = atk.ap
        ok = actions.attack(eng, atk, deff)
        assert ok
        assert atk.ap == ap_before - 1
        expected_damage = max(1, 5 - 2)
        assert deff.hp == start_hp - expected_damage

    def test_armor_floor_min_one(self):
        eng, atk, deff = self._setup(0.0)
        deff.armor = 100
        atk.damage_min = 5
        atk.damage_max = 5
        start_hp = deff.hp
        actions.attack(eng, atk, deff)
        assert deff.hp == start_hp - 1  # min 1 damage

    def test_forced_miss_no_damage(self):
        eng, atk, deff = self._setup(1.0)  # always miss
        start_hp = deff.hp
        ap_before = atk.ap
        actions.attack(eng, atk, deff)
        # Still consumed AP
        assert atk.ap == ap_before - 1
        assert deff.hp == start_hp


# ---------------------------------------------------------------------------
# (d) Prepare reactions
# ---------------------------------------------------------------------------
class TestPrepareReactions:
    def test_guardian_counterattacks_adjacent_enemy(self):
        bf = Battlefield(5, 3, "prep1")
        guardian = Combatant("G", "guardian", "player", 2, 1)
        foe = Combatant("F", "brute", "enemy", 3, 1)
        guardian.crit_chance = 0.0
        foe.crit_chance = 0.0
        foe.armor = 0
        guardian.damage_min = guardian.damage_max = 5
        eng = CombatEngine(bf, [guardian, foe], rng=FixedRandom(0.0))
        eng.start()
        actions.prepare(eng, guardian)
        assert guardian.prepare_stance == "counterattack"
        foe_hp_before = foe.hp
        actions.attack(eng, foe, guardian)
        # Counterattack should have fired and hit foe
        assert any("counterattack" in l.lower() for l in eng.log)
        assert foe.hp < foe_hp_before

    def test_rogue_evasion_negates_hit(self):
        bf = Battlefield(5, 3, "prep2")
        rogue = Combatant("R", "rogue", "player", 2, 1)
        foe = Combatant("F", "brute", "enemy", 3, 1)
        eng = CombatEngine(bf, [rogue, foe], rng=FixedRandom(0.0))
        eng.start()
        actions.prepare(eng, rogue)
        assert rogue.prepare_stance == "evasion"
        hp_before = rogue.hp
        actions.attack(eng, foe, rogue)
        assert rogue.hp == hp_before
        assert any("evades" in l.lower() for l in eng.log)

    def test_ranger_reaction_shot_on_movement(self):
        bf = Battlefield(10, 3, "prep3")
        ranger = Combatant("Rg", "ranger", "player", 1, 1)
        foe = Combatant("F", "brute", "enemy", 5, 1)
        ranger.crit_chance = 0.0
        foe.crit_chance = 0.0
        eng = CombatEngine(bf, [ranger, foe], rng=FixedRandom(0.0))
        eng.start()
        actions.prepare(eng, ranger)
        assert ranger.prepare_stance == "reaction_shot"
        foe.reset_turn()
        foe_hp_before = foe.hp
        # Move foe closer within ranger's range/LOS
        actions.move(eng, foe, (3, 1))
        assert any("reaction shot" in l.lower() for l in eng.log)
        assert foe.hp < foe_hp_before


# ---------------------------------------------------------------------------
# (e) Environment evolution
# ---------------------------------------------------------------------------
class TestEnvironment:
    def test_fire_spreads_burns_out_to_scorched_with_smoke(self):
        bf = Battlefield(4, 3, "env")
        bf.set_terrain(1, 1, "forest")
        bf.set_terrain(2, 1, "forest")
        assert bf.ignite(1, 1)
        # Step until fire fully resolves; check smoke immediately after burnout
        smoke_seen = False
        scorched_seen = False
        spread_seen = False
        for _ in range(8):
            bf.step_environment()
            t1 = bf.tile(1, 1)
            t2 = bf.tile(2, 1)
            if t1.terrain == "scorched":
                scorched_seen = True
            if "smoke" in t1.status_effects:
                smoke_seen = True
            if t2.env.get("burning") or t2.env.get("burned") or t2.terrain == "scorched":
                spread_seen = True
        assert scorched_seen, "tile never became scorched"
        assert smoke_seen, "smoke was never present after burnout"
        assert spread_seen, "fire never spread to adjacent flammable tile"


# ---------------------------------------------------------------------------
# (f) Persistence round-trip
# ---------------------------------------------------------------------------
class TestPersistence:
    def test_destroyed_bridge_persists_and_reloads(self):
        bf = Battlefield(5, 3, "persist1")
        bf.set_terrain(2, 1, "bridge")
        bf.tile(2, 1).add_object("bridge_plank")
        unit = Combatant("U", "guardian", "player", 1, 1)
        ws = {}
        eng = CombatEngine(bf, [unit], rng=FixedRandom(0.0), world_state=ws)
        eng.start()
        ok = actions.interact(eng, unit, (2, 1), "destroy_bridge:bridge_plank")
        assert ok
        eng.end()
        persistent = ws.get("tactical", {}).get("persistent", {}).get("persist1", {})
        assert persistent, "world_state didn't record persistent changes"
        assert "2,1" in persistent

        # Fresh battlefield; apply and confirm water
        bf2 = Battlefield(5, 3, "persist1")
        bf2.apply_persistent(ws)
        assert bf2.tile(2, 1).terrain == "water"


# ---------------------------------------------------------------------------
# (g) Return-to-context
# ---------------------------------------------------------------------------
class TestReturnContext:
    def test_context_preserved_after_auto_battle(self):
        eng = demo.build_demo()
        eng.context = CombatContext("location", "some_id")
        eng.auto_battle(max_rounds=15)
        assert eng.context.origin == "location"
        assert eng.context.location_id == "some_id"
        assert eng.in_combat is False


# ---------------------------------------------------------------------------
# (h) Every enemy blueprint spawns
# ---------------------------------------------------------------------------
class TestEnemyRoster:
    def test_all_enemies_spawn(self):
        ids = enemies.list_enemies()
        assert len(ids) >= 70
        errors = []
        for eid in ids:
            try:
                enemies.spawn_enemy(eid, 0, 0)
            except Exception as e:  # noqa: BLE001
                errors.append((eid, str(e)))
        assert not errors, f"spawn failures: {errors}"

    def test_encounter_groups_run(self):
        names = encounters.list_encounters()
        assert names
        # Try 3 groups through short auto_battle
        for name in list(names)[:3]:
            bf = Battlefield(12, 8, f"enc_{name}")
            group = encounters.build_group(name, battlefield=bf)
            assert group
            player = Combatant("P", "guardian", "player", 1, 1)
            eng = CombatEngine(bf, [player] + list(group), rng=FixedRandom(0.5))
            eng.auto_battle(max_rounds=5)


# ---------------------------------------------------------------------------
# WARN verification
# ---------------------------------------------------------------------------
class TestWarnsAreReal:
    def test_no_skill_or_item_action(self):
        assert not hasattr(actions, "skill")
        assert not hasattr(actions, "use_skill")
        assert not hasattr(actions, "item")
        assert not hasattr(actions, "use_item")

    def test_ai_does_not_cast_abilities(self):
        from tactical import ai
        src = open(ai.__file__).read()
        # Confirm ai doesn't invoke abilities (no reference to use_ability/cast/ABILITIES)
        assert "use_ability" not in src
        assert "cast(" not in src

    def test_referenced_ai_profiles_now_defined(self):
        """REGRESSION GUARD (fixed): every AI profile referenced by an enemy
        blueprint now exists in ai_profiles.json (previously caster/ambusher/
        defender/aggressive were missing and resolved to an empty dict)."""
        with open("/app/tactical/data/ai_profiles.json") as f:
            profiles = json.load(f)
        with open("/app/tactical/data/enemies.json") as f:
            data = json.load(f)
        entries = data if isinstance(data, list) else list(data.values())
        refs = {e.get("ai_profile") for e in entries
                if isinstance(e, dict) and isinstance(e.get("ai_profile"), str)}
        undefined = {r for r in refs if r not in profiles}
        assert not undefined, f"undefined referenced profiles: {undefined}"
        for m in ("caster", "ambusher", "defender", "aggressive"):
            assert m in profiles, f"{m} should now be defined"


# ---------------------------------------------------------------------------
# (i) Loadout locking sanity
# ---------------------------------------------------------------------------
class TestLoadoutLocking:
    def test_loadout_locked_error_in_combat(self):
        unit = Combatant("U", "guardian", "player", 0, 0)
        # Learn any ability then try to equip in-combat
        # Just use existing learned; try equip beyond slots to force checks
        # We just verify the LoadoutLockedError path
        with pytest.raises(LoadoutLockedError):
            equip_ability(unit, "shield_bash", in_combat=True)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
