"""
The Forge Stand — regression + design proof for Torren's Field-Forge identity.

These tests guard two things:
1. The six Field-Forge constructs actually *function* through the canonical
   ability pipeline (they place cover/walls, lay difficult ground, buff, shield
   and heal).
2. The encounter *proves* Torren's battlefield-shaping identity: with the same
   party and enemies, a Torren who BUILDS wins far more (and loses far less)
   than a Torren who only BRAWLS.
"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tactical import showcase_forge as sf          # noqa: E402
from tactical import abilities_engine as ae         # noqa: E402
from tactical.entities import CLASSES               # noqa: E402


# --------------------------------------------------------------------------
# 1. The smith class and its Field-Forge kit exist and are data-driven
# --------------------------------------------------------------------------
FORGE_KIT = ["field_barricade", "reinforced_wall", "spike_barrier",
             "forge_beacon", "reinforce_armor", "battle_repairs"]


def test_smith_class_and_kit_registered():
    assert "smith" in CLASSES
    for ab in FORGE_KIT:
        assert ae.get(ab) is not None, f"missing ability {ab}"
    assert set(CLASSES["smith"]["abilities"]) == set(FORGE_KIT)


def test_torren_equips_the_full_kit():
    torren = [u for u in sf.build_party() if u.cls == "smith"][0]
    assert torren.name == "Torren Ironhall"
    for ab in FORGE_KIT:
        assert ab in torren.equipped


# --------------------------------------------------------------------------
# 2. Each construct actually shapes the battlefield / helps allies
# --------------------------------------------------------------------------
def _torren(engine):
    return [u for u in engine.combatants if u.cls == "smith"][0]


def test_reinforced_wall_creates_full_cover_los_blocker():
    eng = sf.build_encounter(rng=random.Random(1))
    t = _torren(eng)
    t.ap = 6
    assert ae.use_skill(eng, t, "reinforced_wall", tile=(3, 3))
    tile = eng.bf.tile(3, 3)
    assert "wall_segment" in tile.objects
    assert tile.cover_value() == "full"
    assert tile.blocks_los() is True
    assert tile.is_passable() is False


def test_field_barricade_places_a_screen():
    eng = sf.build_encounter(rng=random.Random(1))
    t = _torren(eng)
    t.ap = 6
    assert ae.use_skill(eng, t, "field_barricade", tile=(2, 1))
    assert eng.bf.tile(2, 1).objects  # an object was built


def test_spike_barrier_lays_difficult_half_cover_without_blocking_los():
    eng = sf.build_encounter(rng=random.Random(1))
    t = _torren(eng)
    t.ap = 6
    assert ae.use_skill(eng, t, "spike_barrier", tile=(2, 3))
    tile = eng.bf.tile(2, 3)
    assert tile.terrain == "rubble"
    assert tile.cover_value() == "half"
    assert tile.blocks_los() is False          # allies can still shoot over it
    assert tile.movement_cost() >= 2           # and it slows a charge


def test_beacon_and_shield_and_repairs_apply():
    eng = sf.build_encounter(rng=random.Random(1))
    t = _torren(eng)
    t.ap = 9
    assert ae.use_skill(eng, t, "forge_beacon")
    assert ae.use_skill(eng, t, "reinforce_armor")
    assert "shielded" in t.statuses
    ally = [u for u in eng.combatants if u.team == "player" and u is not t][0]
    ally.hp = 5
    assert ae.use_skill(eng, t, "battle_repairs", target=ally)
    assert ally.hp > 5


def test_rubble_under_defender_grants_directional_cover():
    """The signature play: rubble one step toward the attacker lowers the
    enemy's hit chance on a fragile hero without blocking that hero's own shot."""
    from tactical.inspection import compute_hit_chance
    eng = sf.build_encounter(rng=random.Random(1))
    mage = [u for u in eng.combatants if u.cls == "mage"][0]
    archer = [u for u in eng.combatants if u.team == "enemy" and u.attack_range > 1][0]
    eng.bf.tile(*mage.pos).occupant = None
    mage.x, mage.y = 4, 3
    eng.bf.tile(4, 3).occupant = mage.id
    archer.x, archer.y = 8, 3
    before = compute_hit_chance(eng, archer, mage)["chance"]
    eng.bf.set_terrain(5, 3, "rubble")           # cover step toward the archer
    after = compute_hit_chance(eng, archer, mage)["chance"]
    assert after < before


# --------------------------------------------------------------------------
# 3. The design proof — building beats brawling
# --------------------------------------------------------------------------
def test_encounter_shape():
    eng = sf.build_encounter()
    party = [u for u in eng.combatants if u.team == "player"]
    enemies = [u for u in eng.combatants if u.team == "enemy"]
    assert len(party) == 3 and len(enemies) == 4
    # Torren is a sturdy but weak hitter — he cannot win by damage alone.
    torren = _torren(eng)
    assert torren.max_hp >= 40 and torren.attack_damage <= 5


def test_forge_tactics_win_far_more_than_brawling():
    seeds = 30
    forge = sf.win_rate(sf.forge_tactician_controller, seeds=seeds)
    brawl = sf.win_rate(sf.no_forge_controller, seeds=seeds)
    # Building wins a clear majority...
    assert forge >= 0.70, f"forge win rate too low: {forge:.0%}"
    # ...and decisively more than brute force.
    assert forge - brawl >= 0.30, f"delta too small: forge {forge:.0%} brawl {brawl:.0%}"


def test_brawling_is_unreliable():
    """Without the Field Forge the fragile party is overwhelmed as often as not."""
    brawl = sf.win_rate(sf.no_forge_controller, seeds=30)
    assert brawl <= 0.45, f"brute force unexpectedly reliable: {brawl:.0%}"


def test_manifest_and_identity_documented():
    m = sf.forge_manifest()
    for ab in FORGE_KIT:
        assert ab in m and "shapes" in m[ab] and "decision" in m[ab]
    ident = sf.identity_summary()
    assert "shaper" in ident["identity"].lower()
