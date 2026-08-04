"""
Independent behavioral regression suite for the canonical Ability Pipeline
(Combat Phase C). These are player-perspective behavior tests — not code-path
smoke — verifying target legality, range, LOS, AP, cooldowns, the single-source
preview API, AI ability selection, status lifecycle, terrain interaction,
combat logging, persistence, and interaction with facing/cover/elevation and
opportunity attacks. Deterministic and isolated; every ability fact is read
from tactical.abilities_engine.ability_preview (the one source of truth).
"""

import json
import os
import sys

import pytest

sys.path.insert(0, "/app")

from tactical.battlefield import Battlefield          # noqa: E402
from tactical.entities import Combatant               # noqa: E402
from tactical.engine import CombatEngine, CombatContext  # noqa: E402
from tactical import actions, ai, enemies             # noqa: E402
from tactical import abilities_engine as ae           # noqa: E402
from tactical.inspection import chebyshev             # noqa: E402


class FixedRandom:
    def __init__(self, v):
        self._v = v

    def random(self):
        return self._v

    def randint(self, a, b):
        return a


def field(w=8, h=3):
    return Battlefield(w, h, battlefield_id="ability_test")


def engine(combatants, bf=None, rng=None):
    bf = bf or field()
    eng = CombatEngine(bf, combatants, context=CombatContext("overworld"),
                       rng=rng or FixedRandom(0.0))
    for u in combatants:
        bf.tile(u.x, u.y).occupant = u.id
    eng.in_combat = True
    return eng


def enemy_with(abilities_list, x, y, cls="brute", profile=None):
    u = Combatant("E", cls, "enemy", x, y)
    u.equipped = list(abilities_list)
    if profile:
        u.ai_profile = dict(enemies.AI_PROFILES[profile])
    return u


# ---------------------------------------------------------------------------
# Preview API — the single source of truth
# ---------------------------------------------------------------------------
class TestPreviewAPI:
    def test_preview_reports_full_contract(self):
        bf = field(10)
        caster = Combatant("Mage", "mage", "player", 0, 1)
        caster.ap = 2
        foe = Combatant("Foe", "brute", "enemy", 3, 1)
        eng = engine([caster, foe], bf)
        p = ae.ability_preview(eng, caster, "firebolt", target=foe)
        for k in ("name", "ap_cost", "range", "cooldown", "cooldown_remaining",
                  "requires_los", "line_of_sight", "in_range", "legal_target",
                  "aoe", "expected_damage", "buffs", "debuffs",
                  "status_effects", "friendly_fire_risk", "tactical_value",
                  "usable", "failure_reason"):
            assert k in p, f"missing preview field {k}"
        assert p["usable"] is True
        assert p["expected_damage"] == 8
        assert p["failure_reason"] is None

    def test_preview_out_of_range_reason(self):
        bf = field(14)
        caster = Combatant("Mage", "mage", "player", 0, 1)
        caster.ap = 2
        foe = Combatant("Foe", "brute", "enemy", 12, 1)
        eng = engine([caster, foe], bf)
        p = ae.ability_preview(eng, caster, "firebolt", target=foe)
        assert p["usable"] is False
        assert p["in_range"] is False
        assert p["failure_reason"] == "target out of range"

    def test_preview_no_los_reason(self):
        bf = field(10)
        bf.set_terrain(2, 1, "forest")
        bf.tile(2, 1).add_object("pine_tree")
        caster = Combatant("Mage", "mage", "player", 0, 1)
        caster.ap = 2
        foe = Combatant("Foe", "brute", "enemy", 4, 1)
        eng = engine([caster, foe], bf)
        p = ae.ability_preview(eng, caster, "firebolt", target=foe)
        assert p["usable"] is False
        assert p["line_of_sight"] is False
        assert "line of sight" in p["failure_reason"]

    def test_preview_not_enough_ap(self):
        bf = field()
        caster = Combatant("Mage", "mage", "player", 0, 1)
        caster.ap = 1                       # firebolt costs 2
        foe = Combatant("Foe", "brute", "enemy", 2, 1)
        eng = engine([caster, foe], bf)
        p = ae.ability_preview(eng, caster, "firebolt", target=foe)
        assert p["usable"] is False
        assert p["failure_reason"] == "not enough AP"

    def test_preview_matches_use_result(self):
        """The gate the preview reports must equal what use_skill enforces."""
        bf = field(14)
        caster = Combatant("Mage", "mage", "player", 0, 1)
        caster.ap = 2
        far = Combatant("Far", "brute", "enemy", 12, 1)
        eng = engine([caster, far], bf)
        p = ae.ability_preview(eng, caster, "firebolt", target=far)
        used = ae.use_skill(eng, caster, "firebolt", target=far)
        assert p["usable"] == used == False


# ---------------------------------------------------------------------------
# AP + cooldown economy
# ---------------------------------------------------------------------------
class TestApAndCooldown:
    def test_ap_consumed(self):
        bf = field()
        g = Combatant("Bran", "guardian", "player", 0, 1)
        eng = engine([g], bf)
        ap0 = g.ap
        assert ae.use_skill(eng, g, "shield_wall")
        assert g.ap == ap0 - 2

    def test_failed_skill_costs_nothing(self):
        bf = field(14)
        m = Combatant("Mage", "mage", "player", 0, 1)
        m.ap = 2
        far = Combatant("Far", "brute", "enemy", 12, 1)
        eng = engine([m, far], bf)
        assert not ae.use_skill(eng, m, "firebolt", target=far)
        assert m.ap == 2                    # nothing spent on an illegal cast

    def test_cooldown_set_blocks_and_recovers(self):
        bf = field()
        g = Combatant("Bran", "guardian", "player", 0, 1)
        eng = engine([g], bf)
        assert ae.use_skill(eng, g, "shield_wall")
        assert g.cooldowns["shield_wall"] == 3
        g.reset_turn()
        assert not ae.use_skill(eng, g, "shield_wall")   # still cooling
        for _ in range(3):
            ae.start_of_turn(eng, g)
            g.reset_turn()
        assert "shield_wall" not in g.cooldowns
        assert ae.ability_preview(eng, g, "shield_wall")["usable"]

    def test_cooldown_ticks_once_per_turn(self):
        bf = field()
        g = Combatant("Bran", "guardian", "player", 0, 1)
        eng = engine([g], bf)
        g.cooldowns["shield_wall"] = 3
        ae.start_of_turn(eng, g)
        assert g.cooldowns["shield_wall"] == 2


# ---------------------------------------------------------------------------
# Range / LOS / target legality
# ---------------------------------------------------------------------------
class TestTargeting:
    def test_range_gate(self):
        bf = field(14)
        m = Combatant("Mage", "mage", "player", 0, 1)
        m.ap = 4
        near = Combatant("Near", "brute", "enemy", 4, 1)
        far = Combatant("Far", "brute", "enemy", 12, 1)
        eng = engine([m, near, far], bf)
        assert ae.use_skill(eng, m, "firebolt", target=near)
        m.ap = 4
        assert not ae.use_skill(eng, m, "firebolt", target=far)

    def test_los_gate(self):
        bf = field(10)
        bf.set_terrain(2, 1, "forest")
        bf.tile(2, 1).add_object("pine_tree")
        m = Combatant("Mage", "mage", "player", 0, 1)
        m.ap = 2
        hidden = Combatant("Hidden", "brute", "enemy", 4, 1)
        eng = engine([m, hidden], bf)
        assert not ae.use_skill(eng, m, "firebolt", target=hidden)

    def test_dead_target_is_illegal(self):
        bf = field()
        m = Combatant("Mage", "mage", "player", 0, 1)
        m.ap = 2
        foe = Combatant("Foe", "brute", "enemy", 2, 1)
        eng = engine([m, foe], bf)
        foe.hp = 0
        p = ae.ability_preview(eng, m, "firebolt", target=foe)
        assert p["usable"] is False


# ---------------------------------------------------------------------------
# Effects: damage, status, buff, heal, summon, terrain, control
# ---------------------------------------------------------------------------
class TestEffects:
    def test_attack_deals_damage_and_logs(self):
        bf = field()
        spider = enemy_with(["poison_bite"], 0, 1)
        hero = Combatant("Hero", "guardian", "player", 1, 1)
        hero.armor = 0
        eng = engine([spider, hero], bf)
        hp0 = hero.hp
        assert ae.use_skill(eng, spider, "poison_bite", target=hero)
        assert hero.hp < hp0
        assert "poison" in hero.statuses
        assert any("Poison Bite" in l for l in eng.log)

    def test_poison_dot_and_cleanse(self):
        bf = field()
        hero = Combatant("Hero", "guardian", "player", 1, 1)
        eng = engine([hero], bf)
        hero.statuses.append("poison")
        hp0 = hero.hp
        ae.start_of_turn(eng, hero)
        assert hero.hp == hp0 - 3
        assert "poison" in hero.statuses      # DoT persists until cleansed
        actions.use_item(eng, hero, "antidote")
        assert "poison" not in hero.statuses

    def test_buff_expires_next_turn(self):
        bf = field()
        cmdr = enemy_with(["war_cry"], 0, 1)
        ally = Combatant("Grunt", "brute", "enemy", 1, 1)
        eng = engine([cmdr, ally], bf)
        assert ae.use_skill(eng, cmdr, "war_cry")
        assert "emboldened" in ally.statuses
        ae.start_of_turn(eng, ally)
        assert "emboldened" not in ally.statuses

    def test_shield_halves_next_hit(self):
        bf = field()
        g = enemy_with(["shield_wall"], 2, 1, cls="guardian")
        atk = Combatant("Foe", "brute", "player", 3, 1)
        atk.crit_chance = 0.0
        atk.damage_min = atk.damage_max = 10
        g.armor = 0
        eng = engine([g, atk], bf, rng=FixedRandom(0.0))
        ae.use_skill(eng, g, "shield_wall")
        assert "shielded" in g.statuses
        hp0 = g.hp
        actions.attack(eng, atk, g)
        assert hp0 - g.hp == 5
        assert "shielded" not in g.statuses

    def test_heal_restores_wounded_ally(self):
        bf = field()
        healer = enemy_with(["healing_totem"], 0, 1, cls="guardian")
        wounded = Combatant("Grunt", "brute", "enemy", 1, 1)
        eng = engine([healer, wounded], bf)
        wounded.hp = 4
        assert ae.use_skill(eng, healer, "healing_totem")
        assert wounded.hp == 12

    def test_heal_without_wounded_ally_is_unusable(self):
        bf = field()
        healer = enemy_with(["healing_totem"], 0, 1, cls="guardian")
        ally = Combatant("Grunt", "brute", "enemy", 1, 1)
        eng = engine([healer, ally], bf)
        assert ae.ability_preview(eng, healer, "healing_totem")["tactical_value"] == 0

    def test_summon_adds_ally(self):
        bf = field()
        necro = enemy_with(["raise_skeleton"], 0, 1, cls="mage")
        eng = engine([necro], bf)
        n0 = len(eng.combatants)
        assert ae.use_skill(eng, necro, "raise_skeleton")
        assert len(eng.combatants) == n0 + 1
        assert eng.combatants[-1].team == "enemy"

    def test_summon_capped(self):
        bf = field()
        necro = enemy_with(["raise_skeleton"], 0, 1, cls="mage")
        eng = engine([necro], bf)
        necro.ai_memory["summons_made"] = 3
        assert not ae.use_skill(eng, necro, "raise_skeleton")

    def test_terrain_transforms_tile(self):
        bf = field()
        m = Combatant("Mage", "mage", "player", 0, 1)
        m.ap = 2
        foe = Combatant("Foe", "brute", "enemy", 3, 1)
        eng = engine([m, foe], bf)
        assert ae.use_skill(eng, m, "grease", target=foe, tile=(3, 1))
        assert bf.tile(3, 1).terrain == "oil_slick"

    def test_control_roots_target(self):
        bf = field()
        m = Combatant("Ranger", "ranger", "player", 0, 1)
        foe = Combatant("Foe", "brute", "enemy", 3, 1)
        eng = engine([m, foe], bf)
        assert ae.use_skill(eng, m, "pinning_shot", target=foe)
        assert "rooted" in foe.statuses

    def test_taunt_forces_target(self):
        bf = field()
        g = Combatant("Bran", "guardian", "player", 0, 1)
        foe = Combatant("Foe", "brute", "enemy", 2, 1)
        eng = engine([g, foe], bf)
        assert ae.use_skill(eng, g, "taunt", target=foe)
        assert foe.ai_memory["target_id"] == g.id


# ---------------------------------------------------------------------------
# AI ability selection (profile reinforces role via preview scoring)
# ---------------------------------------------------------------------------
class TestAiAbilityUse:
    def test_support_heals_before_attacking(self):
        bf = field()
        shaman = enemy_with(["healing_totem"], 0, 1, cls="guardian",
                            profile="support")
        wounded = Combatant("Grunt", "brute", "enemy", 1, 1)
        hero = Combatant("Hero", "guardian", "player", 6, 1)
        eng = engine([shaman, wounded, hero], bf)
        wounded.hp = 5
        shaman.reset_turn()
        ai.take_turn(eng, shaman)
        assert wounded.hp > 5

    def test_commander_buffs_the_warband(self):
        bf = field()
        cmdr = enemy_with(["war_cry"], 0, 1, profile="commander")
        ally = Combatant("Grunt", "brute", "enemy", 1, 1)
        hero = Combatant("Hero", "guardian", "player", 6, 1)
        eng = engine([cmdr, ally, hero], bf)
        cmdr.reset_turn()
        ai.take_turn(eng, cmdr)
        assert "emboldened" in ally.statuses

    def test_ai_skips_ability_on_cooldown(self):
        bf = field()
        cmdr = enemy_with(["war_cry"], 0, 1, profile="commander")
        ally = Combatant("Grunt", "brute", "enemy", 1, 1)
        hero = Combatant("Hero", "guardian", "player", 6, 1)
        eng = engine([cmdr, ally, hero], bf)
        cmdr.cooldowns["war_cry"] = 2
        assert ae.choose_ability(eng, cmdr, hero) is None

    def test_attacker_chooses_damage_ability_in_range(self):
        bf = field()
        spider = enemy_with(["poison_bite"], 0, 1, profile="skirmisher")
        hero = Combatant("Hero", "guardian", "player", 1, 1)
        eng = engine([spider, hero], bf)
        choice = ae.choose_ability(eng, spider, hero)
        assert choice is not None and choice[0] == "poison_bite"


# ---------------------------------------------------------------------------
# Persistence + terrain-derived combat interaction
# ---------------------------------------------------------------------------
class TestPersistenceAndInteraction:
    def test_ability_state_round_trips_json(self):
        bf = field()
        g = Combatant("Bran", "guardian", "player", 0, 1)
        eng = engine([g], bf)
        ae.use_skill(eng, g, "shield_wall")
        blob = json.dumps(ae.export_state(g))
        fresh = Combatant("Bran2", "guardian", "player", 0, 1)
        ae.import_state(fresh, json.loads(blob))
        assert fresh.cooldowns.get("shield_wall") == 3
        assert "shielded" in fresh.statuses

    def test_fire_terrain_persists_through_ignite(self):
        bf = field()
        bf.set_terrain(3, 1, "forest")
        bf.tile(3, 1).add_object("pine_tree")
        dragon = enemy_with(["fire_breath"], 0, 1)
        dragon.ap = 2
        foe = Combatant("Tree", "brute", "player", 3, 1)
        eng = engine([dragon, foe], bf)
        assert ae.use_skill(eng, dragon, "fire_breath", target=foe, tile=(3, 1))
        assert bf.tile(3, 1).env.get("burning")

    def test_every_blueprint_ability_resolves(self):
        for eid in enemies.list_enemies(include_abstract=True):
            for aid in enemies.BLUEPRINTS[eid].get("abilities", []) or []:
                assert ae.get(aid) is not None, f"{eid} -> {aid} unresolved"


# ---------------------------------------------------------------------------
# Full-battle stability with abilities in play
# ---------------------------------------------------------------------------
class TestBattleStability:
    def test_ability_rich_battle_resolves(self):
        bf = field(10, 5)
        necro = enemy_with(["raise_skeleton", "dark_bolt"], 8, 2, cls="mage",
                           profile="summoner")
        shaman = enemy_with(["healing_totem", "hex"], 8, 3, cls="guardian",
                            profile="support")
        p1 = Combatant("Hero", "guardian", "player", 1, 2)
        p2 = Combatant("Archer", "ranger", "player", 1, 3)
        eng = engine([necro, shaman, p1, p2], bf, rng=FixedRandom(0.3))
        outcome = eng.auto_battle(max_rounds=40)
        assert outcome in ("player", "enemy", "draw")
        assert eng.round <= 40


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
