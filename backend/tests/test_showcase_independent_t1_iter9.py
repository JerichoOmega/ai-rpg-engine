"""Iteration-9 INDEPENDENT verification of the Sundered Span showcase.

These tests are intentionally *not* a rerun of the developer's own
`test_showcase_encounter.py`.  They (a) statically confirm each canonical
combat pillar is physically present in showcase.build_battlefield /
build_party / build_enemies, and (b) empirically confirm playability by
running many seeds through the reference tactician vs. naive both-AI.
"""

import random
import statistics

import pytest

from tactical import showcase, actions
from tactical import abilities_engine as ae
from tactical.inspection import compute_hit_chance
from tactical.tiles import TERRAIN


# ---------------------------------------------------------------------------
# Static pillar structure
# ---------------------------------------------------------------------------
class TestBattlefieldStructure:
    def setup_method(self):
        self.bf = showcase.build_battlefield()

    def test_dimensions_12x7(self):
        assert (self.bf.width, self.bf.height) == (12, 7)

    def test_ravine_column_impassable_except_bridge_and_ford(self):
        passable = []
        for y in range(self.bf.height):
            if self.bf.tile(6, y).is_passable():
                passable.append(y)
        # Exactly two crossings: bridge at y=3, ford at y=5
        assert passable == [3, 5], f"Expected 2 crossings at y=3,5; got {passable}"
        assert "bridge_plank" in self.bf.tile(6, 3).objects
        assert self.bf.tile(6, 5).terrain == "water"

    def test_high_ground_on_both_sides_and_cliff_elev_2(self):
        # Player side (west of ravine, x<6): must contain elevation-2 cliff
        west_elev2 = [(x, y) for x in range(6) for y in range(self.bf.height)
                      if self.bf.tile(x, y).elevation >= 2]
        east_elev2 = [(x, y) for x in range(7, self.bf.width)
                      for y in range(self.bf.height)
                      if self.bf.tile(x, y).elevation >= 2]
        assert west_elev2, "No elevation>=2 tile on player side"
        assert east_elev2, "No elevation>=2 tile on enemy side"
        # Mid-field hill exists for the ranger to shoot from.
        assert self.bf.tile(5, 4).elevation >= 1

    def test_half_cover_and_full_cover_present(self):
        has_half, has_full = False, False
        for x in range(self.bf.width):
            for y in range(self.bf.height):
                t = self.bf.tile(x, y)
                if TERRAIN[t.terrain].get("cover") == "half":
                    has_half = True
                if "wall_segment" in t.objects or "boulder" in t.objects:
                    has_full = True
        assert has_half, "No half-cover tile (forest) present"
        assert has_full, "No full-cover object (wall/boulder) present"

    def test_difficult_terrain_costs(self):
        # Forest cost 2, water cost 3
        assert TERRAIN["forest"]["movement_cost"] == 2
        assert TERRAIN["water"]["movement_cost"] == 3
        # And these terrains are actually on the map.
        terrains = {self.bf.tile(x, y).terrain
                    for x in range(self.bf.width) for y in range(self.bf.height)}
        assert "forest" in terrains and "water" in terrains

    def test_oil_and_barrel_hazard_cluster(self):
        oil = [(x, y) for x in range(self.bf.width) for y in range(self.bf.height)
               if self.bf.tile(x, y).terrain == "oil_slick"]
        assert len(oil) >= 2, f"Expected >=2 oil slick tiles, got {oil}"
        barrels = [(x, y) for x in range(self.bf.width) for y in range(self.bf.height)
                   if "oil_barrel" in self.bf.tile(x, y).objects]
        assert barrels, "No explosive barrel present"


class TestPartyStructure:
    def test_party_of_four_with_abilities_and_potions(self):
        party = showcase.build_party()
        assert len(party) == 4
        classes = {u.cls for u in party}
        # Complementary roles
        assert {"guardian", "ranger", "mage", "rogue"} <= classes
        for u in party:
            assert u.team == "player"
            assert u.equipped, f"{u.name} has no equipped abilities"
            assert "healing_potion" in u.items, f"{u.name} has no healing potion"


class TestEnemyStructure:
    def test_five_enemies_with_four_distinct_profiles(self):
        enemies = showcase.build_enemies()
        assert len(enemies) == 5
        # Distinct AI archetypes: commander, healer/support, defender,
        # skirmisher, brute.
        profile_flags = []
        for u in enemies:
            flags = tuple(sorted(k for k in u.ai_profile
                                 if k in {"buffs_allies", "kites",
                                          "hold_position", "charges"}))
            profile_flags.append(flags)
        distinct = {f for f in profile_flags if f}
        assert len(distinct) >= 4, f"Only {distinct} distinct archetypes"

    def test_commander_has_rally_or_war_cry(self):
        warlord = next(u for u in showcase.build_enemies()
                       if u.name == "Warlord Gruk")
        assert set(warlord.equipped) & {"rally", "war_cry"}

    def test_support_healer_present(self):
        assert any(u.ai_profile.get("buffs_allies") or "healing_totem" in u.equipped
                   for u in showcase.build_enemies())


# ---------------------------------------------------------------------------
# Solution levers (deterministic mechanical checks)
# ---------------------------------------------------------------------------
class TestSolutionLevers:
    def test_high_ground_improves_ranger_hit_chance(self):
        engine = showcase.build_encounter(rng=random.Random(1))
        ranger = next(u for u in engine.combatants if u.cls == "ranger")
        warlord = next(u for u in engine.combatants if u.name == "Warlord Gruk")
        # Flat position vs hill position, same range.
        ranger.x, ranger.y = 4, 2   # plains
        flat = compute_hit_chance(engine, ranger, warlord)
        ranger.x, ranger.y = 5, 4   # hill elevation 1
        hilled = compute_hit_chance(engine, ranger, warlord)
        assert hilled["chance"] > flat["chance"], \
            f"High ground didn't boost hit chance: {flat} vs {hilled}"
        assert hilled["elevation"] > flat["elevation"]

    def test_backstab_vs_front_basic_damage(self):
        """Rear+backstab must strictly out-damage a front basic against armor."""
        class R:  # deterministic best-case rng
            def random(self): return 0.0
            def randint(self, a, b): return b

        # Front basic
        e1 = showcase.build_encounter(rng=R())
        rogue1 = next(u for u in e1.combatants if u.cls == "rogue")
        warlord1 = next(u for u in e1.combatants if u.name == "Warlord Gruk")
        rogue1.x, rogue1.y = warlord1.x - 1, warlord1.y
        warlord1.facing = "W"        # facing the rogue -> front hit
        hp_before = warlord1.hp
        actions.attack(e1, rogue1, warlord1)
        front_dmg = hp_before - warlord1.hp

        # Rear backstab
        e2 = showcase.build_encounter(rng=R())
        rogue2 = next(u for u in e2.combatants if u.cls == "rogue")
        warlord2 = next(u for u in e2.combatants if u.name == "Warlord Gruk")
        rogue2.x, rogue2.y = warlord2.x - 1, warlord2.y
        warlord2.facing = "E"        # facing away -> rear
        hp_before = warlord2.hp
        ok = ae.use_skill(e2, rogue2, "backstab", target=warlord2)
        assert ok, "backstab could not be used"
        back_dmg = hp_before - warlord2.hp
        assert back_dmg > front_dmg, \
            f"Backstab ({back_dmg}) did not beat front basic ({front_dmg})"

    def test_prepare_counters_and_opportunity_attacks(self):
        """Guardian's prepared counter fires and OA fires when leaving a
        melee raider's reach."""
        class R:
            def random(self): return 0.0
            def randint(self, a, b): return b

        # Prepared counter
        eng = showcase.build_encounter(rng=R())
        guard = next(u for u in eng.combatants if u.cls == "guardian")
        raider = next(u for u in eng.combatants if u.name == "Corrupted Raider")
        raider.x, raider.y = guard.x + 1, guard.y
        actions.prepare(eng, guard)
        hp_before = raider.hp
        actions.attack(eng, raider, guard)
        assert raider.hp < hp_before, "Guardian's prepared counter did not trigger"

        # Opportunity attack from the melee raider (attack_range=1)
        eng2 = showcase.build_encounter(rng=R())
        rogue = next(u for u in eng2.combatants if u.cls == "rogue")
        raider2 = next(u for u in eng2.combatants if u.name == "Corrupted Raider")
        assert raider2.attack_range <= 1, "Raider should be melee for OA"
        rogue.x, rogue.y = raider2.x - 1, raider2.y
        # Reset OA usage
        if hasattr(raider2, "opportunity_used"):
            raider2.opportunity_used = False
        hp_before = rogue.hp
        # Move rogue out of raider's reach
        dest = (rogue.x - 2, rogue.y)
        actions.move(eng2, rogue, dest)
        assert rogue.hp < hp_before, "Opportunity attack did not fire when leaving reach"

    def test_firebolt_ignites_oil_and_burns(self):
        class R:
            def random(self): return 0.0
            def randint(self, a, b): return b

        eng = showcase.build_encounter(rng=R())
        mage = next(u for u in eng.combatants if u.cls == "mage")
        warlord = next(u for u in eng.combatants if u.name == "Warlord Gruk")
        # Warlord already stands on oil at (9,2). Reposition the mage with LOS.
        assert eng.bf.tile(*warlord.pos).terrain == "oil_slick"
        eng.bf.tile(*mage.pos).occupant = None
        mage.x, mage.y = 7, 2
        eng.bf.tile(7, 2).occupant = mage.id
        mage.ap = 2
        ok = ae.use_skill(eng, mage, "firebolt", target=warlord)
        assert ok, "Firebolt could not be used"
        assert eng.bf.tile(*warlord.pos).env.get("burning"), \
            "Oil under the warlord did not ignite"
        hp_after_hit = warlord.hp
        for _ in range(3):
            eng.environment_reacts()
        assert warlord.hp < hp_after_hit, \
            f"Fire did not chip HP: still {warlord.hp}"

    def test_shaman_is_a_killable_priority_target(self):
        eng = showcase.build_encounter()
        shaman = next(u for u in eng.combatants if u.name == "Mossroot Shaman")
        assert shaman.armor <= 1
        assert shaman.max_hp <= 24

    def test_healing_potion_restores_hp(self):
        eng = showcase.build_encounter()
        ranger = next(u for u in eng.combatants if u.cls == "ranger")
        ranger.hp = 5
        ok = actions.use_item(eng, ranger, "healing_potion", target=ranger)
        assert ok
        assert ranger.hp > 5
        assert "healing_potion" not in ranger.items or \
               ranger.items.count("healing_potion") == 0


# ---------------------------------------------------------------------------
# Playability across many seeds
# ---------------------------------------------------------------------------
class TestPlayability:
    SEEDS = list(range(1, 21))  # 20 seeds

    def test_tactician_wins_majority(self):
        wins, losses, draws = 0, 0, 0
        outcomes = []
        for s in self.SEEDS:
            eng = showcase.build_encounter(rng=random.Random(s))
            r = eng.auto_battle(max_rounds=40,
                                player_controller=showcase.tactician_controller)
            outcomes.append((s, r))
            if r == "player": wins += 1
            elif r == "enemy": losses += 1
            else: draws += 1
        assert wins >= 12, f"Tactician only won {wins}/20 seeds: {outcomes}"

    def test_naive_both_ai_ambush_is_real_threat(self):
        """With NO player controller (naive both-AI on both sides),
        the ambush should punish the party — enemy should win the majority."""
        wins, losses, draws = 0, 0, 0
        for s in self.SEEDS:
            eng = showcase.build_encounter(rng=random.Random(s))
            r = eng.auto_battle(max_rounds=40)  # no controller = naive both AI
            if r == "player": wins += 1
            elif r == "enemy": losses += 1
            else: draws += 1
        assert losses > wins, \
            f"Naive both-AI: expected enemies to dominate but got " \
            f"player_wins={wins} enemy_wins={losses} draws={draws}"

    def test_battle_resolves_within_round_cap(self):
        for s in self.SEEDS:
            eng = showcase.build_encounter(rng=random.Random(s))
            r = eng.auto_battle(max_rounds=40,
                                player_controller=showcase.tactician_controller)
            assert r in {"player", "enemy", "draw"}
            assert getattr(eng, "round", 0) <= 40


# ---------------------------------------------------------------------------
# AI personality expression + persistence
# ---------------------------------------------------------------------------
class TestAiAndPersistence:
    def test_commander_uses_a_buff_ability_in_a_full_run(self):
        used = False
        # Try up to a few seeds — should express at least once.
        for s in range(1, 11):
            eng = showcase.build_encounter(rng=random.Random(s))
            log = []

            orig = ae.use_skill

            def tap(engine, unit, sid, **kw):
                r = orig(engine, unit, sid, **kw)
                if r and unit.name == "Warlord Gruk" and sid in {"rally", "war_cry"}:
                    log.append(sid)
                return r

            ae.use_skill = tap
            try:
                eng.auto_battle(max_rounds=40,
                                player_controller=showcase.tactician_controller)
            finally:
                ae.use_skill = orig
            if log:
                used = True
                break
        assert used, "Warlord never used rally/war_cry across seeds 1..10"

    def test_fire_scorched_terrain_persists_to_world_state(self):
        """After combat, fire-scorched terrain should be persisted to world_state.

        We verify persistence directly (per the developer's design contract):
        ignite oil, run environment ticks, then call engine start/end so the
        battlefield writes its scars to world_state["tactical"]["persistent"].
        """
        ws = {}
        eng = showcase.build_encounter(rng=random.Random(0), world_state=ws)
        eng.start()
        eng.bf.ignite(9, 2)
        for _ in range(6):
            eng.environment_reacts()
        eng.end()
        persisted = ws.get("tactical", {}).get("persistent", {}).get(
            showcase.BATTLEFIELD_ID, {})
        assert persisted, f"Battlefield scars not saved. ws={ws!r}"
        serialised = repr(persisted)
        assert "scorch" in serialised or "fire" in serialised or "burn" in serialised, \
            f"Persisted snapshot has no fire evidence: {serialised[:400]}"


# ---------------------------------------------------------------------------
# Manifest coverage
# ---------------------------------------------------------------------------
class TestPillarManifest:
    def test_manifest_covers_all_canonical_pillars(self):
        m = showcase.pillar_manifest()
        required = {
            "battlefield_is_a_character", "difficult_terrain", "cover",
            "elevation", "line_of_sight", "movement_and_ap",
            "facing_flanking_opportunity", "prepare_reactions",
            "abilities_and_cooldowns", "items", "ai_personalities",
            "battlefield_evolves", "information_before_commitment",
            "companion_party", "multiple_solutions",
        }
        assert required <= set(m.keys()), \
            f"Missing pillars: {required - set(m.keys())}"
        for k, v in m.items():
            assert v.get("feature") and v.get("decision"), \
                f"Pillar {k} missing feature/decision"
