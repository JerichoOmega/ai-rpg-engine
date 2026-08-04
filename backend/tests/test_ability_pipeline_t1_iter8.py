"""Independent verification of the CANONICAL Ability Pipeline (Combat Phase C).

Written from a fresh perspective by testing agent T1 — NOT a rerun of the
existing suite. Focus is contract adherence: ability_preview as the single
source of truth, data-driven cooldowns, AP economy, AI selection, persistence,
and full-battle stability.
"""
from __future__ import annotations

import copy
import json
import pytest

from tactical.battlefield import Battlefield
from tactical.engine import CombatEngine, CombatContext
from tactical.entities import Combatant
from tactical import abilities_engine as AE
from tactical import actions as ACT
from tactical import enemies as ENEM


class FixedRNG:
    """Deterministic RNG: random()->0.0 (always hit), randint(a,b)->a."""
    def random(self):
        return 0.0
    def randint(self, a, b):
        return a


def build_engine(size=15, units=None, context="overworld"):
    bf = Battlefield(size, size)
    units = units or []
    for u in units:
        bf.tile(u.x, u.y).occupant = u.id
    eng = CombatEngine(bf, units, context=CombatContext(context), rng=FixedRNG())
    eng.in_combat = True
    return eng, bf


# ---------------------------------------------------------------------------
# 1. Preview contract (single source of truth)
# ---------------------------------------------------------------------------
class TestPreviewContract:
    def test_preview_returns_all_contract_fields(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        u.equipped = ["firebolt"]
        e = Combatant("Grunt", "guardian", "enemy", 3, 1)
        eng, _ = build_engine(units=[u, e])
        p = AE.ability_preview(eng, u, "firebolt", target=e)
        for key in ("ability_id", "name", "ap_cost", "range",
                    "cooldown", "cooldown_remaining", "requires_los",
                    "aoe", "expected_damage", "expected_healing",
                    "buffs", "debuffs", "status_effects",
                    "friendly_fire_risk", "tactical_value",
                    "usable", "failure_reason"):
            assert key in p, f"preview missing '{key}'"

    def test_in_range_usable_reports_expected_damage(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        u.equipped = ["firebolt"]
        e = Combatant("Foe", "guardian", "enemy", 4, 1)
        eng, _ = build_engine(units=[u, e])
        p = AE.ability_preview(eng, u, "firebolt", target=e)
        assert p["usable"] is True
        assert p["failure_reason"] is None
        assert p["expected_damage"] == 8
        assert p["in_range"] is True
        assert p["line_of_sight"] is True

    def test_out_of_range_reports_reason(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        u.equipped = ["firebolt"]
        e = Combatant("Foe", "guardian", "enemy", 10, 10)
        eng, _ = build_engine(units=[u, e])
        p = AE.ability_preview(eng, u, "firebolt", target=e)
        assert p["usable"] is False
        assert p["failure_reason"] == "target out of range"

    def test_los_blocked_reports_reason(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        u.equipped = ["firebolt"]
        e = Combatant("Foe", "guardian", "enemy", 4, 1)
        eng, bf = build_engine(units=[u, e], context="forest")
        # Put a pine_tree between them.
        bf.tile(2, 1).add_object("pine_tree")
        p = AE.ability_preview(eng, u, "firebolt", target=e)
        assert p["usable"] is False
        assert "line of sight" in p["failure_reason"]

    def test_insufficient_ap_reports_reason(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        u.equipped = ["firebolt"]
        e = Combatant("Foe", "guardian", "enemy", 3, 1)
        eng, _ = build_engine(units=[u, e])
        u.ap = 0
        p = AE.ability_preview(eng, u, "firebolt", target=e)
        assert p["usable"] is False
        assert p["failure_reason"] == "not enough AP"

    def test_unknown_ability_is_unusable(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        eng, _ = build_engine(units=[u])
        p = AE.ability_preview(eng, u, "no_such_id")
        assert p["usable"] is False
        assert p["failure_reason"] == "unknown ability"


# ---------------------------------------------------------------------------
# 2. Preview <=> use_skill parity + AP economy
# ---------------------------------------------------------------------------
class TestSingleSourceOfTruth:
    def test_illegal_cast_matches_preview_and_costs_nothing(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        u.equipped = ["firebolt"]
        e = Combatant("Foe", "guardian", "enemy", 12, 12)
        eng, _ = build_engine(units=[u, e])
        ap_before = u.ap
        p = AE.ability_preview(eng, u, "firebolt", target=e)
        assert p["usable"] is False
        ok = AE.use_skill(eng, u, "firebolt", target=e)
        assert ok is False
        assert u.ap == ap_before, "failed skill must NOT consume AP"
        assert "firebolt" not in u.cooldowns, "failed skill must not set cooldown"

    def test_successful_cast_consumes_ap_and_sets_cooldown(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        u.equipped = ["firebolt"]
        e = Combatant("Foe", "guardian", "enemy", 3, 1)
        eng, _ = build_engine(units=[u, e])
        ap_before, hp_before = u.ap, e.hp
        p = AE.ability_preview(eng, u, "firebolt", target=e)
        assert p["usable"]
        assert AE.use_skill(eng, u, "firebolt", target=e) is True
        assert u.ap == ap_before - p["ap_cost"]
        assert e.hp < hp_before, "damage should apply"
        assert u.cooldowns.get("firebolt") == 2


# ---------------------------------------------------------------------------
# 3. Data-driven cooldowns
# ---------------------------------------------------------------------------
class TestCooldowns:
    def test_cooldown_blocks_reuse_and_ticks_at_start_of_turn(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        u.equipped = ["firebolt"]
        e = Combatant("Foe", "guardian", "enemy", 3, 1)
        eng, _ = build_engine(units=[u, e])
        assert AE.use_skill(eng, u, "firebolt", target=e)
        assert u.cooldowns["firebolt"] == 2

        # Refresh AP each "turn" and tick.
        u.ap = u.max_ap
        AE.start_of_turn(eng, u)  # tick 1 -> cd=1
        assert u.cooldowns.get("firebolt") == 1
        p = AE.ability_preview(eng, u, "firebolt", target=e)
        assert not p["usable"] and "cooldown" in p["failure_reason"]

        u.ap = u.max_ap
        AE.start_of_turn(eng, u)  # tick 2 -> cd removed
        assert "firebolt" not in u.cooldowns
        p2 = AE.ability_preview(eng, u, "firebolt", target=e)
        assert p2["usable"] is True

    def test_zero_cooldown_ability_not_tracked(self):
        u = Combatant("Necro", "mage", "player", 1, 1)
        u.equipped = ["dark_bolt"]  # cooldown 0
        e = Combatant("Foe", "guardian", "enemy", 3, 1)
        eng, _ = build_engine(units=[u, e])
        assert AE.use_skill(eng, u, "dark_bolt", target=e)
        assert "dark_bolt" not in u.cooldowns


# ---------------------------------------------------------------------------
# 4. Effect resolution
# ---------------------------------------------------------------------------
class TestEffects:
    def test_poison_bite_applies_and_ticks_and_antidote_cleanses(self):
        biter = Combatant("Spider", "brute", "enemy", 1, 1)
        biter.equipped = ["poison_bite"]
        # Manually shove ability
        victim = Combatant("Hero", "guardian", "player", 2, 1)
        eng, _ = build_engine(units=[biter, victim])
        assert AE.use_skill(eng, biter, "poison_bite", target=victim)
        assert "poison" in victim.statuses
        hp_after_hit = victim.hp

        # Poison ticks 3 dmg at start_of_turn.
        AE.start_of_turn(eng, victim)
        assert victim.hp == hp_after_hit - 3
        assert "poison" in victim.statuses  # persists

        # Antidote cleanses.
        victim.ap = victim.max_ap
        assert ACT.use_item(eng, victim, "antidote", target=victim)
        assert "poison" not in victim.statuses

    def test_shielded_halves_next_hit_then_drops(self):
        tank = Combatant("Tank", "guardian", "player", 1, 1)
        tank.equipped = ["shield_wall"]
        foe = Combatant("Foe", "brute", "enemy", 2, 1)
        eng, _ = build_engine(units=[tank, foe])
        assert AE.use_skill(eng, tank, "shield_wall")
        assert "shielded" in tank.statuses
        hp0 = tank.hp
        # Simulate a 10-damage hit through the ability engine's damage helper.
        AE._apply_damage(eng, foe, tank, 10)
        assert "shielded" not in tank.statuses
        # Damage should be roughly halved (armor may subtract more).
        assert hp0 - tank.hp <= 10 // 2 + 1

    def test_war_cry_emboldens_allies_then_expires(self):
        cmdr = Combatant("Commander", "guardian", "enemy", 5, 5)
        cmdr.equipped = ["war_cry"]
        ally = Combatant("Grunt", "brute", "enemy", 6, 5)
        eng, _ = build_engine(units=[cmdr, ally])
        assert AE.use_skill(eng, cmdr, "war_cry")
        assert "emboldened" in ally.statuses
        # Expires on ally's next start_of_turn.
        ally.ap = ally.max_ap
        AE.start_of_turn(eng, ally)
        assert "emboldened" not in ally.statuses

    def test_heal_totem_ignored_when_no_wounded_ally(self):
        support = Combatant("Priest", "mage", "player", 1, 1)
        support.equipped = ["healing_totem"]
        ally = Combatant("Bud", "guardian", "player", 2, 1)
        assert ally.hp == ally.max_hp
        eng, _ = build_engine(units=[support, ally])
        p = AE.ability_preview(eng, support, "healing_totem", target=ally)
        assert p["tactical_value"] == 0.0

    def test_heal_totem_heals_when_wounded(self):
        support = Combatant("Priest", "mage", "player", 1, 1)
        support.equipped = ["healing_totem"]
        ally = Combatant("Bud", "guardian", "player", 2, 1)
        ally.hp = 5
        eng, _ = build_engine(units=[support, ally])
        assert AE.use_skill(eng, support, "healing_totem", target=ally)
        assert ally.hp == 5 + 8

    def test_raise_skeleton_summons_and_caps_at_three(self):
        necro = Combatant("Necro", "mage", "enemy", 5, 5)
        necro.equipped = ["raise_skeleton"]
        eng, bf = build_engine(units=[necro])
        team_size = len([u for u in eng.combatants if u.team == "enemy"])
        for _ in range(5):
            necro.ap = necro.max_ap
            necro.cooldowns.pop("raise_skeleton", None)
            AE.use_skill(eng, necro, "raise_skeleton")
        added = len([u for u in eng.combatants if u.team == "enemy"]) - team_size
        assert added == 3, f"summon cap must be 3, got {added}"

    def test_grease_transforms_target_tile_to_oil_slick(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        u.equipped = ["grease"]
        eng, bf = build_engine(units=[u])
        target_tile = (3, 1)
        assert AE.use_skill(eng, u, "grease", tile=target_tile)
        t = bf.tile(*target_tile)
        # Terrain slot is where set_terrain writes.
        assert getattr(t, "terrain", None) == "oil_slick" or \
               t.env.get("terrain") == "oil_slick" or \
               "oil_slick" in str(vars(t))

    def test_pinning_shot_roots_target(self):
        ranger = Combatant("Ranger", "ranger", "player", 1, 1)
        ranger.equipped = ["pinning_shot"]
        foe = Combatant("Foe", "brute", "enemy", 3, 1)
        eng, _ = build_engine(units=[ranger, foe])
        assert AE.use_skill(eng, ranger, "pinning_shot", target=foe)
        assert "rooted" in foe.statuses
        # start_of_turn zeroes movement then clears root.
        foe.ap = foe.max_ap
        AE.start_of_turn(eng, foe)
        assert foe.move == 0
        assert "rooted" not in foe.statuses

    def test_taunt_forces_target(self):
        tank = Combatant("Tank", "guardian", "player", 1, 1)
        tank.equipped = ["taunt"]
        foe = Combatant("Foe", "brute", "enemy", 3, 1)
        eng, _ = build_engine(units=[tank, foe])
        assert AE.use_skill(eng, tank, "taunt", target=foe)
        assert foe.ai_memory.get("target_id") == tank.id


# ---------------------------------------------------------------------------
# 5. AI ability selection
# ---------------------------------------------------------------------------
class TestAISelection:
    def test_support_profile_prefers_heal_when_ally_wounded(self):
        support = Combatant("Priest", "mage", "enemy", 5, 5)
        support.equipped = ["dark_bolt", "healing_totem"]
        support.ai_profile = {"coordinates": True, "buffs_allies": True}
        wounded = Combatant("Ally", "brute", "enemy", 6, 5)
        wounded.hp = 5
        foe = Combatant("Hero", "guardian", "player", 3, 5)
        eng, _ = build_engine(units=[support, wounded, foe])
        pick = AE.choose_ability(eng, support, foe)
        assert pick is not None
        assert pick[0] == "healing_totem"

    def test_commander_profile_casts_war_cry(self):
        cmdr = Combatant("Cap", "guardian", "enemy", 5, 5)
        cmdr.equipped = ["cleave", "war_cry"]
        cmdr.ai_profile = {"coordinates": True, "buffs_allies": True}
        ally = Combatant("Grunt", "brute", "enemy", 6, 5)
        foe = Combatant("Hero", "guardian", "player", 6, 6)
        eng, _ = build_engine(units=[cmdr, ally, foe])
        pick = AE.choose_ability(eng, cmdr, foe)
        assert pick is not None and pick[0] == "war_cry"

    def test_ai_skips_ability_on_cooldown(self):
        atk = Combatant("Beast", "brute", "enemy", 1, 1)
        atk.equipped = ["poison_bite"]
        foe = Combatant("Hero", "guardian", "player", 2, 1)
        eng, _ = build_engine(units=[atk, foe])
        atk.cooldowns["poison_bite"] = 2
        pick = AE.choose_ability(eng, atk, foe)
        assert pick is None

    def test_ai_selects_damage_ability_when_in_range(self):
        atk = Combatant("Beast", "brute", "enemy", 1, 1)
        atk.equipped = ["poison_bite"]
        foe = Combatant("Hero", "guardian", "player", 2, 1)
        eng, _ = build_engine(units=[atk, foe])
        pick = AE.choose_ability(eng, atk, foe)
        assert pick is not None and pick[0] == "poison_bite"


# ---------------------------------------------------------------------------
# 6. Persistence
# ---------------------------------------------------------------------------
class TestPersistence:
    def test_state_survives_json_round_trip(self):
        u = Combatant("Sable", "mage", "player", 1, 1)
        u.statuses = ["poison", "shielded"]
        u.cooldowns = {"firebolt": 2, "grease": 1}
        blob = json.dumps(AE.export_state(u))

        v = Combatant("Sable2", "mage", "player", 1, 1)
        AE.import_state(v, json.loads(blob))
        assert v.statuses == ["poison", "shielded"]
        assert v.cooldowns == {"firebolt": 2, "grease": 1}


# ---------------------------------------------------------------------------
# 7. Registry integrity — every ability referenced by any blueprint resolves.
# ---------------------------------------------------------------------------
class TestRegistryIntegrity:
    def test_every_blueprint_ability_id_resolves(self):
        with open("tactical/data/enemies.json", encoding="utf-8") as fh:
            enemies = json.load(fh)
        unresolved = []
        for eid, bp in enemies.items():
            for aid in bp.get("abilities", []):
                if AE.get(aid) is None:
                    unresolved.append((eid, aid))
        assert not unresolved, f"Unresolved ability ids: {unresolved}"


# ---------------------------------------------------------------------------
# 8. Full-battle stability — ability-rich fight resolves within a round cap.
# ---------------------------------------------------------------------------
class TestFullBattleStability:
    def test_ability_rich_battle_reaches_decisive_outcome(self):
        # 2 heroes vs summoner + support.
        heroes = [
            Combatant("Hero1", "guardian", "player", 1, 5),
            Combatant("Hero2", "ranger", "player", 1, 6),
        ]
        heroes[0].equipped = ["shield_wall"]
        heroes[1].equipped = ["pinning_shot"]

        necro = Combatant("Necro", "mage", "enemy", 8, 5)
        necro.equipped = ["dark_bolt", "raise_skeleton"]
        necro.ai_profile = {"summons": True}
        support = Combatant("Priest", "mage", "enemy", 9, 6)
        support.equipped = ["dark_bolt", "healing_totem"]
        support.ai_profile = {"coordinates": True, "buffs_allies": True}

        units = heroes + [necro, support]
        eng, bf = build_engine(size=14, units=units)

        rounds = 0
        MAX_ROUNDS = 40
        try:
            while rounds < MAX_ROUNDS:
                rounds += 1
                for u in list(eng.combatants):
                    if not u.alive:
                        continue
                    u.reset_turn()
                    AE.start_of_turn(eng, u)
                    if not u.alive:
                        continue
                    # Simple actor loop: try one ability, else damage some foe.
                    foe = next((f for f in eng.enemies_of(u) if f.alive), None)
                    if foe is None:
                        break
                    pick = AE.choose_ability(eng, u, foe)
                    if pick is not None:
                        aid, kwargs = pick
                        AE.use_skill(eng, u, aid, **kwargs)
                    else:
                        # brute-force damage to make progress
                        foe.hp -= 5
                        if foe.hp <= 0:
                            bf.tile(foe.x, foe.y).occupant = None
                p_alive = any(h.alive for h in heroes)
                e_alive = any(x.alive and x.team == "enemy"
                              for x in eng.combatants)
                if not (p_alive and e_alive):
                    break
        except Exception as exc:  # pragma: no cover
            pytest.fail(f"Battle raised: {exc!r}")

        assert rounds < MAX_ROUNDS, "battle failed to resolve within round cap"


# ---------------------------------------------------------------------------
# 9. Regression sanity — canonical use_skill is the *same* callable exposed by
#    actions.use_skill (proves no duplicate combat path).
# ---------------------------------------------------------------------------
def test_actions_use_skill_is_the_canonical_one():
    assert ACT.use_skill is AE.use_skill
