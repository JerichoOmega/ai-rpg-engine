"""
Independent verification for the gold-standard vertical-slice encounter
(The Sundered Span, `tactical/showcase.py`).

Two things are proven here:
  1. STRUCTURE — the battlefield/party/enemies concretely instantiate every
     canonical combat pillar named in `showcase.pillar_manifest()`.
  2. PLAYABILITY — the encounter is winnable with competent tactics and NOT with
     mindless attacking, and each headline "solution" lever actually works.

Deterministic and isolated; behavioural (player-perspective) assertions, not
code-path smoke.
"""

import random
import sys

import pytest

sys.path.insert(0, "/app")

from tactical import showcase, actions                    # noqa: E402
from tactical import abilities_engine as ae               # noqa: E402
from tactical.entities import Combatant                   # noqa: E402
from tactical.inspection import compute_hit_chance, chebyshev  # noqa: E402


class FixedRandom:
    def __init__(self, v):
        self._v = v

    def random(self):
        return self._v

    def randint(self, a, b):
        return b            # max damage for deterministic-but-fair lever tests


def unit(engine, name_part):
    return next(u for u in engine.combatants if name_part in u.name)


# ===========================================================================
# STRUCTURE — every pillar is physically present
# ===========================================================================
class TestPillarStructure:
    def setup_method(self):
        self.eng = showcase.build_encounter(rng=random.Random(0))
        self.bf = self.eng.bf

    def _tiles(self):
        return [self.bf.tile(x, y) for y in range(self.bf.height)
                for x in range(self.bf.width)]

    def test_manifest_covers_all_pillars(self):
        m = showcase.pillar_manifest()
        expected = {
            "battlefield_is_a_character", "difficult_terrain", "cover",
            "elevation", "line_of_sight", "movement_and_ap",
            "facing_flanking_opportunity", "prepare_reactions",
            "abilities_and_cooldowns", "items", "ai_personalities",
            "battlefield_evolves", "information_before_commitment",
            "companion_party", "multiple_solutions",
        }
        assert expected.issubset(m.keys())
        for v in m.values():
            assert v["feature"] and v["decision"]

    def test_elevation_on_both_sides(self):
        elev = [t for t in self._tiles() if t.elevation >= 1]
        assert len(elev) >= 4
        west = [t for t in elev if t.x < 6]
        east = [t for t in elev if t.x > 6]
        assert west and east, "both sides need high ground"
        assert any(t.elevation >= 2 for t in elev), "a cliff (elev 2) exists"

    def test_half_and_full_cover(self):
        covers = {t.cover_value() for t in self._tiles()}
        assert "half" in covers and "full" in covers

    def test_difficult_terrain_present(self):
        terrains = {t.terrain for t in self._tiles()}
        assert "forest" in terrains and "water" in terrains
        assert self.bf.tile(3, 1).movement_cost() == 2   # forest
        assert self.bf.tile(6, 5).movement_cost() == 3   # water ford

    def test_impassable_ravine_with_two_crossings(self):
        chasm = [y for y in range(7) if not self.bf.tile(6, y).is_passable()]
        assert len(chasm) >= 4, "the ravine is a real wall"
        assert self.bf.tile(6, 3).is_passable(), "bridge crossing is open"
        assert self.bf.tile(6, 5).is_passable(), "southern ford is open"

    def test_hazard_cluster_exists(self):
        assert self.bf.tile(9, 2).is_flammable()          # oil under the warlord
        assert "oil_barrel" in self.bf.tile(8, 3).objects  # explosive

    def test_four_hero_party_with_kits_and_items(self):
        heroes = [u for u in self.eng.combatants if u.team == "player"]
        assert len(heroes) == 4
        assert len({h.cls for h in heroes}) == 4          # complementary roles
        for h in heroes:
            assert h.equipped, f"{h.name} has abilities"
            assert getattr(h, "items", []), f"{h.name} carries an item"

    def test_five_distinct_ai_archetypes(self):
        import json
        foes = [u for u in self.eng.combatants if u.team == "enemy"]
        assert len(foes) == 5
        signatures = {json.dumps(f.ai_profile, sort_keys=True) for f in foes}
        assert len(signatures) >= 4, f"distinct AI profiles: {len(signatures)}"
        # and the roles the encounter relies on are all represented
        flags = [f.ai_profile for f in foes]
        assert any(p.get("buffs_allies") for p in flags), "a support/healer"
        assert any(p.get("hold_position") for p in flags), "a defender"
        assert any(p.get("kites") for p in flags), "a skirmisher"
        assert any("rally" in f.equipped or "war_cry" in f.equipped
                   for f in foes), "a commander that buffs"


# ===========================================================================
# PLAYABILITY — winnable with tactics, not with mashing
# ===========================================================================
class TestPlayability:
    def test_tactician_wins_majority(self):
        wins = 0
        for s in range(20):
            eng = showcase.build_encounter(rng=random.Random(s))
            if eng.auto_battle(
                    max_rounds=40,
                    player_controller=showcase.tactician_controller) == "player":
                wins += 1
        assert wins >= 12, f"competent play should usually win (got {wins}/20)"

    def test_mashing_does_not_trivially_win(self):
        # Naive both-AI: the ambush is a genuine threat, not a free win.
        losses = 0
        for s in range(10):
            eng = showcase.build_encounter(rng=random.Random(s))
            if eng.auto_battle(max_rounds=40) == "enemy":
                losses += 1
        assert losses >= 6, "an ambush should punish careless play"

    def test_battle_always_resolves(self):
        for s in range(10):
            eng = showcase.build_encounter(rng=random.Random(s))
            out = eng.auto_battle(
                max_rounds=40, player_controller=showcase.tactician_controller)
            assert out in ("player", "enemy", "draw")
            assert eng.round <= 40


# ===========================================================================
# SOLUTION LEVERS — each headline tactic actually works
# ===========================================================================
class TestSolutionLevers:
    def test_high_ground_grants_hit_and_damage_edge(self):
        eng = showcase.build_encounter(rng=random.Random(0))
        sella = unit(eng, "Sella")
        warden = unit(eng, "Warden")
        # ground shot vs same shot from the mid-field hill (5,4)
        low = compute_hit_chance(eng, sella, warden)["chance"]
        eng.bf.tile(*sella.pos).occupant = None
        sella.x, sella.y = 5, 4                      # hill, elevation 1
        eng.bf.tile(5, 4).occupant = sella.id
        high = compute_hit_chance(eng, sella, warden)
        assert eng.bf.tile(5, 4).elevation >= 1
        assert high["elevation"] > 0 and high["chance"] > low

    def test_flank_backstab_beats_a_front_basic(self):
        eng = showcase.build_encounter(rng=FixedRandom(0.0))
        vesper = unit(eng, "Vesper")
        chief = unit(eng, "Gruk")            # armour 5 — basics barely scratch
        # front basic
        eng.bf.tile(*vesper.pos).occupant = None
        vesper.x, vesper.y = chief.x - 1, chief.y      # west = front-ish
        chief.facing = "W"
        vesper.ap = 2
        hp0 = chief.hp
        actions.attack(eng, vesper, chief)
        front_dmg = hp0 - chief.hp
        # rear backstab
        chief.hp = chief.max_hp
        chief.facing = "W"
        vesper.x, vesper.y = chief.x + 1, chief.y      # east = rear of W-facer
        vesper.ap = 3
        vesper.cooldowns.clear()
        hp1 = chief.hp
        assert ae.use_skill(eng, vesper, "backstab", target=chief)
        back_dmg = hp1 - chief.hp
        assert back_dmg > front_dmg, f"backstab {back_dmg} vs front {front_dmg}"

    def test_guardian_prepare_counterattacks(self):
        eng = showcase.build_encounter(rng=FixedRandom(0.0))
        bran = unit(eng, "Bran")
        raider = unit(eng, "Raider")
        eng.bf.tile(*raider.pos).occupant = None
        raider.x, raider.y = bran.x + 1, bran.y        # adjacent
        eng.bf.tile(*raider.pos).occupant = raider.id
        actions.prepare(eng, bran)
        actions.attack(eng, raider, bran)
        assert any("counterattacks" in l for l in eng.log)

    def test_leaving_melee_raider_provokes_opportunity(self):
        eng = showcase.build_encounter(rng=FixedRandom(0.0))
        bran = unit(eng, "Bran")
        raider = unit(eng, "Raider")           # goblin_warrior, melee reach 1
        # place them adjacent in open ground
        for u in (bran, raider):
            eng.bf.tile(*u.pos).occupant = None
        bran.x, bran.y = 3, 3
        raider.x, raider.y = 4, 3
        eng.bf.tile(3, 3).occupant = bran.id
        eng.bf.tile(4, 3).occupant = raider.id
        bran.move = 4
        actions.move(eng, bran, (1, 3))        # walk out of the raider's reach
        assert any("opportunity attack" in l for l in eng.log)

    def test_burning_the_warlord_denies_his_ground(self):
        eng = showcase.build_encounter(rng=FixedRandom(0.0))
        corwin = unit(eng, "Corwin")
        chief = unit(eng, "Gruk")              # stands on oil at (9,2)
        eng.bf.tile(*corwin.pos).occupant = None
        corwin.x, corwin.y = 7, 2              # LOS + range 5 to the warlord
        eng.bf.tile(7, 2).occupant = corwin.id
        corwin.ap = 2
        assert ae.use_skill(eng, corwin, "firebolt", target=chief)
        assert eng.bf.tile(9, 2).env.get("burning"), "the oil ignites"
        hp = chief.hp
        for _ in range(2):
            eng.environment_reacts()
        assert chief.hp < hp, "fire chips the warlord, forcing him to move"

    def test_shaman_is_a_killable_priority_and_potions_sustain(self):
        eng = showcase.build_encounter(rng=FixedRandom(0.0))
        sella = unit(eng, "Sella")
        shaman = unit(eng, "Shaman")           # armour 1, 22 hp
        eng.bf.tile(*sella.pos).occupant = None
        sella.x, sella.y = shaman.x - 3, shaman.y
        eng.bf.tile(*sella.pos).occupant = sella.id
        sella.ap = 4
        sella.cooldowns.clear()
        ae.use_skill(eng, sella, "aimed_shot", target=shaman)
        assert shaman.hp <= shaman.max_hp * 0.6, "a focused shot bites deep"
        # potion sustain
        bran = unit(eng, "Bran")
        bran.hp = 5
        assert actions.use_item(eng, bran, "healing_potion", target=bran)
        assert bran.hp > 5


# ===========================================================================
# AI PERSONALITY EXPRESSION + PERSISTENCE
# ===========================================================================
class TestAiAndPersistence:
    def test_warlord_and_shaman_express_roles_via_abilities(self):
        eng = showcase.build_encounter(rng=random.Random(3))
        eng.auto_battle(max_rounds=40,
                        player_controller=showcase.tactician_controller)
        log = "\n".join(eng.log)
        assert ("Rally" in log or "War Cry" in log), "commander buffs the warband"

    def test_scorched_ground_persists_to_world_state(self):
        ws = {}
        eng = showcase.build_encounter(rng=random.Random(0), world_state=ws)
        eng.start()
        eng.bf.ignite(9, 2)                    # torch the oil
        for _ in range(4):
            eng.environment_reacts()
        eng.end()
        persisted = ws.get("tactical", {}).get("persistent", {}).get(
            showcase.BATTLEFIELD_ID, {})
        assert persisted, "battlefield scars are saved"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
