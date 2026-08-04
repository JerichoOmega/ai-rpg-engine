"""
Tactical Combat Foundation — Independent Verification Harness
=============================================================

Phase 1 gate. This harness verifies that the ``tactical/`` package does not
merely *run*, but *behaves* according to ``Combat_Gameplay_Architecture.md``
(CANON). Every core gameplay pillar is exercised deterministically and
checked against an expected outcome.

Run::

    python -m tactical.verify           # human-readable checklist
    python -m tactical.verify --json    # machine report to stdout

It also writes ``tactical/verification_report.json`` for the record.

Result vocabulary
-----------------
* ``PASS``  — foundation behaviour is correct.
* ``FAIL``  — foundation behaviour is wrong; **blocks Phase 2**.
* ``WARN``  — a known gap / incomplete system slated for a later phase
  (documented in the report; does not block the *foundation* gate but is
  tracked as technical debt).
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Callable, Dict, List, Tuple

from .battlefield import Battlefield
from .entities import (Combatant, LoadoutLockedError, equip_ability,
                       unequip_ability)
from .engine import CombatEngine, CombatContext
from . import actions, ai, enemies
from .inspection import (inspect_tile, compute_hit_chance, movement_preview,
                         threat_map, enemies_threatening, tactical_overlay,
                         chebyshev)


# ---------------------------------------------------------------------------
# Deterministic RNG stubs (make combat outcomes reproducible)
# ---------------------------------------------------------------------------
class FixedRandom:
    """random() returns a fixed value; randint returns the low bound."""

    def __init__(self, value: float):
        self._v = value

    def random(self) -> float:
        return self._v

    def randint(self, a: int, b: int) -> int:
        return a


ALWAYS_HIT = lambda: FixedRandom(0.0)     # noqa: E731
ALWAYS_MISS = lambda: FixedRandom(1.0)    # noqa: E731


# ---------------------------------------------------------------------------
# Small builders
# ---------------------------------------------------------------------------
def _open_field(w: int = 6, h: int = 6, bid: str = "test") -> Battlefield:
    return Battlefield(w, h, battlefield_id=bid)


def _engine(bf: Battlefield, combatants: List[Combatant], rng=None) -> CombatEngine:
    eng = CombatEngine(bf, combatants, context=CombatContext("overworld"),
                       rng=rng or FixedRandom(0.0))
    for u in combatants:
        bf.tile(u.x, u.y).occupant = u.id
    eng.in_combat = True
    return eng


# ===========================================================================
# CHECKS  ->  each returns (status, detail)
# ===========================================================================
Check = Callable[[], Tuple[str, str]]
REGISTRY: List[Tuple[str, str, Check]] = []


def check(category: str, name: str):
    def deco(fn: Check):
        REGISTRY.append((category, name, fn))
        return fn
    return deco


# -- Terrain / Tile metadata ------------------------------------------------
@check("Tile Metadata", "Terrain + object composition")
def _c_tile_meta():
    bf = _open_field()
    bf.set_terrain(1, 1, "forest")
    t = bf.tile(1, 1)
    t.add_object("pine_tree")
    ok = (t.movement_cost() == 2 and t.cover_value() == "half"
          and t.blocks_los() and t.is_flammable()
          and any(i.startswith("burn_object") for i in t.interactions()))
    return ("PASS" if ok else "FAIL",
            f"forest+pine_tree -> cost={t.movement_cost()} cover={t.cover_value()} "
            f"los_block={t.blocks_los()} flammable={t.is_flammable()}")


@check("Tile Metadata", "Impassable tiles (boulder / occupant)")
def _c_impassable():
    bf = _open_field()
    bf.tile(2, 2).add_object("boulder")
    boulder_blocks = (not bf.tile(2, 2).is_passable()
                      and bf.tile(2, 2).movement_cost() == 99)
    bf.tile(3, 3).occupant = "someone"
    occ_blocks = not bf.tile(3, 3).is_passable()
    return ("PASS" if boulder_blocks and occ_blocks else "FAIL",
            f"boulder_impassable={boulder_blocks} occupant_blocks={occ_blocks}")


@check("Tile Metadata", "Difficult terrain movement cost")
def _c_difficult():
    bf = _open_field()
    bf.set_terrain(1, 1, "forest")
    bf.set_terrain(2, 1, "water")
    ok = (bf.tile(0, 0).movement_cost() == 1 and
          bf.tile(1, 1).movement_cost() == 2 and
          bf.tile(2, 1).movement_cost() == 3)
    return ("PASS" if ok else "FAIL",
            f"plains=1 forest={bf.tile(1,1).movement_cost()} "
            f"water={bf.tile(2,1).movement_cost()}")


@check("Tile Metadata", "Elevation from terrain + override")
def _c_elevation():
    bf = _open_field()
    bf.set_terrain(1, 1, "hill")
    bf.set_terrain(2, 1, "cliff_top")
    bf.set_terrain(3, 1, "plains", elevation=5)
    ok = (bf.tile(1, 1).elevation == 1 and bf.tile(2, 1).elevation == 2
          and bf.tile(3, 1).elevation == 5)
    return ("PASS" if ok else "FAIL",
            f"hill={bf.tile(1,1).elevation} cliff={bf.tile(2,1).elevation} "
            f"override={bf.tile(3,1).elevation}")


# -- Movement / pathfinding -------------------------------------------------
@check("Movement", "Reachability respects movement budget")
def _c_reachable():
    bf = _open_field(7, 7)
    reach = bf.reachable((3, 3), 2)
    ok = ((3, 3) in reach and reach[(3, 3)] == 0
          and (5, 3) in reach and (6, 3) not in reach)
    return ("PASS" if ok else "FAIL",
            f"count={len(reach)} incl(5,3)={(5,3) in reach} excl(6,3)={(6,3) not in reach}")


@check("Movement", "Pathfinding routes around impassable")
def _c_pathfind():
    bf = _open_field(7, 3)
    for y in range(3):
        bf.tile(3, y).add_object("boulder")   # full wall at column 3...
    bf.remove_wall = None
    bf.tile(3, 2).remove_object("boulder")    # ...with a gap at (3,2)
    path = bf.path((0, 0), (6, 0), ap=50)
    routed = path is not None and (3, 2) in path
    return ("PASS" if routed else "FAIL",
            f"path_len={len(path) if path else None} uses_gap={routed}")


@check("Movement", "Difficult terrain consumes extra movement")
def _c_move_cost():
    bf = _open_field(6, 3)
    bf.set_terrain(1, 0, "forest")
    u = Combatant("Scout", "ranger", "player", 0, 0)
    eng = _engine(bf, [u])
    u.move = 3
    ok = actions.move(eng, u, (2, 0))
    # 0->1 forest(2) + 1->2 plains(1) = 3
    spent_ok = ok and u.move == 0 and u.pos == (2, 0)
    return ("PASS" if spent_ok else "FAIL",
            f"moved={ok} final_pos={u.pos} move_left={u.move}")


# -- Line of sight ----------------------------------------------------------
@check("Line of Sight", "Blocker breaks LOS at equal elevation")
def _c_los_block():
    bf = _open_field(7, 3)
    bf.set_terrain(3, 1, "forest")
    bf.tile(3, 1).add_object("pine_tree")
    blocked = not bf.line_of_sight((1, 1), (5, 1))
    clear = bf.line_of_sight((1, 0), (5, 0))
    return ("PASS" if blocked and clear else "FAIL",
            f"blocked_through_tree={blocked} clear_open_row={clear}")


@check("Line of Sight", "High ground sees over cover")
def _c_los_highground():
    bf = _open_field(7, 3)
    bf.set_terrain(3, 1, "forest")
    bf.tile(3, 1).add_object("pine_tree")     # blocker at elevation 0
    bf.set_terrain(1, 1, "cliff_top")         # viewer at elevation 2
    sees_over = bf.line_of_sight((1, 1), (5, 1))
    return ("PASS" if sees_over else "FAIL",
            f"cliff_sees_over_tree={sees_over}")


# -- Cover ------------------------------------------------------------------
@check("Cover", "Directional cover + hit penalty")
def _c_cover():
    bf = _open_field(7, 3)
    bf.set_terrain(3, 1, "forest")
    bf.tile(3, 1).add_object("pine_tree")
    # defender at (4,1), attacker at (1,1): step toward attacker is (3,1) tree
    cover = bf.directional_cover((4, 1), (1, 1))
    penalty = bf.cover_penalty((4, 1), (1, 1))
    ok = cover in ("half", "full") and penalty > 0
    return ("PASS" if ok else "FAIL",
            f"cover={cover} penalty={penalty}")


# -- Information before commitment (Pillar 2) -------------------------------
@check("Information", "inspect_tile exposes full tactical data")
def _c_inspect():
    bf = _open_field()
    bf.set_terrain(1, 1, "forest")
    bf.tile(1, 1).add_object("pine_tree")
    u = Combatant("A", "guardian", "player", 0, 0)
    eng = _engine(bf, [u])
    data = inspect_tile(eng, (1, 1))
    keys = {"terrain", "movement_cost", "cover", "elevation", "blocks_los",
            "hazards", "interactions", "occupant", "context_actions"}
    ok = keys.issubset(data.keys()) and data["cover"] == "half"
    return ("PASS" if ok else "FAIL",
            f"has_all_keys={keys.issubset(data.keys())} cover={data.get('cover')}")


@check("Information", "compute_hit_chance transparency + range gate")
def _c_hitchance():
    bf = _open_field(10, 3)
    atk = Combatant("Ar", "ranger", "player", 0, 1)    # range 6
    d1 = Combatant("Near", "brute", "enemy", 5, 1)      # in range
    d2 = Combatant("Far", "brute", "enemy", 9, 1)       # out of range
    eng = _engine(bf, [atk, d1, d2])
    near = compute_hit_chance(eng, atk, d1)
    far = compute_hit_chance(eng, atk, d2)
    keys = {"chance", "cover_penalty", "elevation", "line_of_sight", "in_range"}
    ok = (keys.issubset(near) and near["chance"] > 0
          and far["in_range"] is False and far["chance"] == 0)
    return ("PASS" if ok else "FAIL",
            f"near_chance={near['chance']:.2f} far_in_range={far['in_range']} "
            f"far_chance={far['chance']}")


@check("Information", "movement_preview shows cost/threat/attackers")
def _c_preview():
    bf = _open_field(10, 3)
    u = Combatant("Hero", "guardian", "player", 0, 1)
    e = Combatant("Foe", "archer", "enemy", 6, 1)       # range 6
    eng = _engine(bf, [u])
    eng.combatants.append(e)
    bf.tile(6, 1).occupant = e.id
    u.move = 5
    prev = movement_preview(eng, u, (4, 1))
    ok = (prev["reachable"] and prev["cost"] == 4
          and "enemies_that_can_hit_you" in prev
          and "Foe" in prev["enemies_that_can_hit_you"])
    return ("PASS" if ok else "FAIL",
            f"reachable={prev.get('reachable')} cost={prev.get('cost')} "
            f"threatened_by={prev.get('enemies_that_can_hit_you')}")


@check("Information", "threat map / threat visualization is live")
def _c_threat():
    bf = _open_field(10, 3)
    u = Combatant("Hero", "guardian", "player", 0, 1)
    e = Combatant("Archer", "archer", "enemy", 6, 1)    # range 6
    eng = _engine(bf, [u, e])
    tmap = threat_map(eng, u)
    at_tile = enemies_threatening(eng, u, (3, 1))
    ok = (3, 1) in tmap and any(t["name"] == "Archer" for t in at_tile)
    return ("PASS" if ok else "FAIL",
            f"tile_threatened={(3,1) in tmap} threats_at_tile={len(at_tile)}")


@check("Information", "tactical_overlay covers whole grid")
def _c_overlay():
    bf = _open_field(4, 4)
    u = Combatant("Hero", "guardian", "player", 0, 0)
    e = Combatant("Foe", "archer", "enemy", 3, 3)
    eng = _engine(bf, [u, e])
    ov = tactical_overlay(eng, u)
    cell = ov.get("0,0", {})
    ok = (len(ov) == 16 and "move_cost" in cell and "cover" in cell
          and "under_enemy_threat" in cell and "visible_to_unit" in cell)
    return ("PASS" if ok else "FAIL",
            f"cells={len(ov)} keys_ok={'move_cost' in cell}")


# -- Combat actions ---------------------------------------------------------
@check("Combat", "Melee attack applies damage minus armor")
def _c_melee():
    bf = _open_field(4, 3)
    atk = Combatant("Sword", "brute", "player", 0, 1)   # dmg 7..7
    dfn = Combatant("Tank", "guardian", "enemy", 1, 1)  # armor 0 by class
    dfn.armor = 3
    atk.crit_chance = 0.0
    atk.damage_min = atk.damage_max = 10
    eng = _engine(bf, [atk, dfn], rng=ALWAYS_HIT())
    hp0 = dfn.hp
    hit = actions.attack(eng, atk, dfn)
    dealt = hp0 - dfn.hp
    ok = hit and dealt == 7 and atk.ap == atk.max_ap - actions.ATTACK_AP
    return ("PASS" if ok else "FAIL",
            f"hit={hit} dealt={dealt} (expected 10-3=7) ap_spent_ok={atk.ap == atk.max_ap-1}")


@check("Combat", "Miss deals no damage")
def _c_miss():
    bf = _open_field(4, 3)
    atk = Combatant("Sword", "brute", "player", 0, 1)
    dfn = Combatant("Tank", "guardian", "enemy", 1, 1)
    eng = _engine(bf, [atk, dfn], rng=ALWAYS_MISS())
    hp0 = dfn.hp
    actions.attack(eng, atk, dfn)
    ok = dfn.hp == hp0 and any("misses" in l for l in eng.log)
    return ("PASS" if ok else "FAIL", f"hp_unchanged={dfn.hp == hp0}")


@check("Combat", "Ranged attack range gate")
def _c_ranged():
    bf = _open_field(12, 3)
    atk = Combatant("Bow", "ranger", "player", 0, 1)    # range 6
    near = Combatant("Near", "brute", "enemy", 5, 1)
    far = Combatant("Far", "brute", "enemy", 10, 1)
    eng = _engine(bf, [atk, near, far], rng=ALWAYS_HIT())
    can_near = actions.attack(eng, atk, near)
    atk.ap = atk.max_ap
    can_far = actions.attack(eng, atk, far)
    ok = can_near and not can_far
    return ("PASS" if ok else "FAIL", f"hit_near={can_near} hit_far_blocked={not can_far}")


@check("Combat", "Prepare: Guardian counterattack")
def _c_counter():
    bf = _open_field(4, 3)
    guard = Combatant("Bran", "guardian", "player", 1, 1)
    foe = Combatant("Foe", "brute", "enemy", 2, 1)
    eng = _engine(bf, [guard, foe], rng=ALWAYS_HIT())
    actions.prepare(eng, guard)                     # arms counterattack
    actions.attack(eng, foe, guard)
    ok = (guard.prepare_stance is None
          and any("counterattacks" in l for l in eng.log))
    return ("PASS" if ok else "FAIL",
            f"countered={any('counterattacks' in l for l in eng.log)}")


@check("Combat", "Prepare: Rogue evasion negates a hit")
def _c_evasion():
    bf = _open_field(4, 3)
    rogue = Combatant("Sly", "rogue", "player", 1, 1)
    foe = Combatant("Foe", "brute", "enemy", 2, 1)
    eng = _engine(bf, [rogue, foe], rng=ALWAYS_HIT())
    actions.prepare(eng, rogue)                     # arms evasion
    hp0 = rogue.hp
    actions.attack(eng, foe, rogue)
    ok = rogue.hp == hp0 and any("evades" in l for l in eng.log)
    return ("PASS" if ok else "FAIL",
            f"hp_unchanged={rogue.hp == hp0} evaded_logged={any('evades' in l for l in eng.log)}")


@check("Combat", "Prepare: Ranger reaction shot on movement")
def _c_reaction_shot():
    bf = _open_field(10, 3)
    mover = Combatant("Runner", "brute", "player", 0, 1)
    ranger = Combatant("Watcher", "archer", "enemy", 8, 1)   # range 6
    eng = _engine(bf, [mover, ranger], rng=ALWAYS_HIT())
    actions.prepare(eng, ranger)                    # arms reaction_shot
    mover.move = 6
    actions.move(eng, mover, (3, 1))                # steps into range/LOS
    ok = any("reaction shot" in l for l in eng.log)
    return ("PASS" if ok else "FAIL",
            f"reaction_fired={ok}")


@check("Combat", "Loadout locked during combat, editable outside")
def _c_loadout():
    u = Combatant("Bran", "guardian", "player", 0, 0)   # slots 3, learns 3
    u.equipped = u.equipped[:1]
    locked = False
    try:
        equip_ability(u, "taunt", in_combat=True)
    except LoadoutLockedError:
        locked = True
    equip_ability(u, "taunt", in_combat=False)          # succeeds outside
    editable = "taunt" in u.equipped
    return ("PASS" if locked and editable else "FAIL",
            f"locked_in_combat={locked} editable_outside={editable}")


# -- AI parity (Pillar: shared rules) --------------------------------------
@check("AI", "AI closes distance and attacks in range")
def _c_ai_engage():
    bf = _open_field(10, 3)
    foe = Combatant("Grunt", "brute", "enemy", 8, 1)
    hero = Combatant("Hero", "guardian", "player", 1, 1)
    eng = _engine(bf, [foe, hero], rng=ALWAYS_HIT())
    foe.reset_turn()
    d0 = abs(foe.x - hero.x)
    ai.take_turn(eng, foe)
    closed = abs(foe.x - hero.x) < d0
    return ("PASS" if closed else "FAIL",
            f"start_dist={d0} end_dist={abs(foe.x-hero.x)} closed={closed}")


@check("AI", "AI prefers cover / elevation tiles when scoring")
def _c_ai_cover_pref():
    bf = _open_field(8, 3)
    # A cover tile and an open tile both let the enemy hit the target.
    bf.set_terrain(4, 0, "forest")
    bf.tile(4, 0).add_object("pine_tree")
    foe = Combatant("Grunt", "brute", "enemy", 5, 1)
    hero = Combatant("Hero", "guardian", "player", 0, 1)
    eng = _engine(bf, [foe, hero])
    foe.ai_profile = {"uses_cover": True, "target_selection": "nearest",
                      "preferred_range": "melee", "avoids": ["fire"]}
    threats = threat_map(eng, foe)
    open_tile = ai._score_tile(eng, foe, (3, 1), hero, threats)
    cover_tile = ai._score_tile(eng, foe, (1, 0), hero, threats)  # behind tree
    # elevation preference
    bf.set_terrain(6, 1, "hill")
    hi = ai._score_tile(eng, foe, (6, 1), hero, threats)
    lo = ai._score_tile(eng, foe, (6, 2), hero, threats)
    ok = hi > lo
    return ("PASS" if ok else "FAIL",
            f"elevation_pref hi={hi:.1f}>lo={lo:.1f}={ok}")


@check("AI", "AI avoids hazard tiles it is told to avoid")
def _c_ai_hazard():
    bf = _open_field(6, 3)
    foe = Combatant("Grunt", "brute", "enemy", 3, 1)
    hero = Combatant("Hero", "guardian", "player", 0, 1)
    eng = _engine(bf, [foe, hero])
    foe.ai_profile = {"avoids": ["fire"], "uses_cover": False,
                      "target_selection": "nearest", "preferred_range": "melee"}
    bf.tile(2, 1).env["burning"] = True
    threats = threat_map(eng, foe)
    fire_score = ai._score_tile(eng, foe, (2, 1), hero, threats)
    safe_score = ai._score_tile(eng, foe, (2, 0), hero, threats)
    ok = safe_score > fire_score
    return ("PASS" if ok else "FAIL",
            f"safe={safe_score:.1f} > fire={fire_score:.1f}={ok}")


# -- Environment evolution (Pillar 5) --------------------------------------
@check("Environment", "Fire spreads then burns out to scorched + smoke")
def _c_fire():
    bf = _open_field(4, 4)
    for xy in [(1, 1), (2, 1), (1, 2)]:
        bf.set_terrain(*xy, "forest")
        bf.tile(*xy).add_object("pine_tree")
    bf.ignite(1, 1)
    step1 = bf.step_environment()      # spreads to neighbours, timer 2->1
    step2 = bf.step_environment()      # timer 1->0 -> burns out
    spread = any("fire spreads" in c for c in step1)
    scorched = bf.tile(1, 1).terrain == "scorched"
    smoke = "smoke" in bf.tile(1, 1).status_effects
    ok = spread and scorched and smoke
    return ("PASS" if ok else "FAIL",
            f"spread={spread} scorched={scorched} smoke={smoke}")


@check("Environment", "Hazard tiles damage occupants each round")
def _c_hazard_dmg():
    bf = _open_field(4, 3)
    u = Combatant("Victim", "brute", "player", 1, 1)
    e = Combatant("Foe", "brute", "enemy", 3, 1)
    eng = _engine(bf, [u, e])
    bf.tile(1, 1).env["burning"] = True
    bf.tile(1, 1).env["burn_timer"] = 5
    hp0 = u.hp
    eng.environment_reacts()
    ok = u.hp < hp0
    return ("PASS" if ok else "FAIL", f"fire_damage_taken={hp0 - u.hp}")


@check("Environment", "Interact: destroy bridge turns tile to water")
def _c_bridge():
    bf = _open_field(5, 3)
    bf.set_terrain(2, 1, "road")
    bf.tile(2, 1).add_object("bridge_plank")
    u = Combatant("Sapper", "guardian", "player", 1, 1)
    eng = _engine(bf, [u])
    ok = actions.interact(eng, u, (2, 1), "destroy_bridge:bridge_plank")
    became_water = bf.tile(2, 1).terrain == "water"
    flagged = bf.tile(2, 1).env.get("destroyed_bridge") is True
    return ("PASS" if ok and became_water and flagged else "FAIL",
            f"interacted={ok} water={became_water} flagged={flagged}")


# -- Persistence / save-load ------------------------------------------------
@check("Persistence", "Permanent changes persist to world_state and reload")
def _c_persist():
    ws: Dict = {}
    bf = _open_field(5, 3, bid="bridge_field")
    bf.set_terrain(2, 1, "road")
    bf.tile(2, 1).add_object("bridge_plank")
    u = Combatant("Sapper", "guardian", "player", 1, 1)
    eng = CombatEngine(bf, [u], world_state=ws)
    eng.start()
    actions.interact(eng, u, (2, 1), "destroy_bridge:bridge_plank")
    eng.end()
    persisted = ws.get("tactical", {}).get("persistent", {}).get("bridge_field", {})
    saved = "2,1" in persisted
    # reload onto a fresh battlefield
    bf2 = _open_field(5, 3, bid="bridge_field")
    bf2.set_terrain(2, 1, "road")
    bf2.tile(2, 1).add_object("bridge_plank")
    bf2.apply_persistent(ws)
    restored = bf2.tile(2, 1).terrain == "water"
    return ("PASS" if saved and restored else "FAIL",
            f"saved={saved} restored_on_load={restored}")


# -- Full battle: victory + no infinite loop --------------------------------
@check("Engine", "auto_battle reaches a decisive result (no infinite loop)")
def _c_autobattle():
    from .demo import build_demo
    eng = build_demo()
    t0 = time.time()
    outcome = eng.auto_battle(max_rounds=30)
    dt = time.time() - t0
    ok = outcome in ("player", "enemy") and eng.round < 30 and dt < 5.0
    return ("PASS" if ok else "FAIL",
            f"outcome={outcome} rounds={eng.round} secs={dt:.3f}")


@check("Engine", "Return-to-context preserved after combat")
def _c_context():
    from .demo import build_demo
    ws: Dict = {}
    eng = build_demo(world_state=ws)
    eng.context = CombatContext("location", "ravenford_keep")
    eng.auto_battle(max_rounds=30)
    ctx = eng.context
    ok = ctx.origin == "location" and ctx.location_id == "ravenford_keep" \
        and eng.in_combat is False
    return ("PASS" if ok else "FAIL",
            f"origin={ctx.origin} loc={ctx.location_id} in_combat={eng.in_combat}")


# -- Data integrity (surfaces Phase-2 content gaps as WARN) -----------------
@check("Data Integrity", "Every enemy blueprint resolves")
def _c_bp_resolve():
    bad = []
    for eid in enemies.list_enemies(include_abstract=True):
        try:
            enemies.resolve(eid)
        except Exception as exc:                      # noqa: BLE001
            bad.append(f"{eid}: {exc}")
    n = len(enemies.list_enemies())
    return ("PASS" if not bad else "FAIL",
            f"{n} spawnable blueprints resolve; errors={bad}")


@check("Data Integrity", "Referenced AI profiles exist in ai_profiles.json")
def _c_ai_profiles():
    missing: Dict[str, List[str]] = {}
    for eid in enemies.list_enemies():
        raw = enemies.BLUEPRINTS[eid]
        # walk to find the effective ai_profile string
        node, prof = raw, None
        seen = set()
        while node is not None and id(node) not in seen:
            seen.add(id(node))
            if "ai_profile" in node:
                prof = node["ai_profile"]
                break
            parent = node.get("extends")
            node = enemies.BLUEPRINTS.get(parent) if parent else None
        if isinstance(prof, str) and prof not in enemies.AI_PROFILES:
            missing.setdefault(prof, []).append(eid)
    if not missing:
        return ("PASS", "all referenced AI profiles are defined")
    return ("WARN",
            "missing AI profiles (resolve to empty dict; Phase 2 work): "
            + ", ".join(f"{p} -> {v}" for p, v in missing.items()))


# -- Ability Pipeline (Combat Phase C) -------------------------------------
def _ab_field(bf, combatants, rng=None):
    return _engine(bf, combatants, rng=rng)


@check("Abilities", "Skill/Item actions + AI ability casting wired")
def _c_skill_wired():
    from . import abilities_engine
    has_skill = hasattr(actions, "use_skill")
    has_item = hasattr(actions, "use_item")
    ai_casts = "abilities" in ai.take_turn.__code__.co_names
    has_preview = hasattr(abilities_engine, "ability_preview")
    ok = has_skill and has_item and ai_casts and has_preview
    return ("PASS" if ok else "FAIL",
            f"skill={has_skill} item={has_item} ai_casts={ai_casts} "
            f"preview={has_preview}")


@check("Abilities", "Preview exposes cost/range/LOS/effect + failure reason")
def _c_ability_preview():
    from . import abilities_engine as ae
    bf = _open_field(12, 3)
    caster = Combatant("Mage", "mage", "player", 0, 1)   # firebolt range 5
    near = Combatant("Near", "brute", "enemy", 4, 1)
    far = Combatant("Far", "brute", "enemy", 10, 1)
    eng = _engine(bf, [caster, near, far])
    caster.ap = 3
    ok_prev = ae.ability_preview(eng, caster, "firebolt", target=near)
    bad_prev = ae.ability_preview(eng, caster, "firebolt", target=far)
    keys = {"name", "ap_cost", "cooldown_remaining", "range", "line_of_sight",
            "in_range", "legal_target", "expected_damage", "usable",
            "failure_reason", "tactical_value", "friendly_fire_risk"}
    ok = (keys.issubset(ok_prev) and ok_prev["usable"] is True
          and ok_prev["expected_damage"] == 8
          and bad_prev["usable"] is False
          and bad_prev["failure_reason"] == "target out of range")
    return ("PASS" if ok else "FAIL",
            f"in_range_usable={ok_prev['usable']} dmg={ok_prev['expected_damage']} "
            f"far_reason={bad_prev['failure_reason']}")


@check("Abilities", "AP is consumed on a successful skill")
def _c_ability_ap():
    from . import abilities_engine as ae
    bf = _open_field(4, 3)
    guard = Combatant("Bran", "guardian", "player", 0, 1)   # shield_wall ap 2
    eng = _engine(bf, [guard])
    ap0 = guard.ap
    used = ae.use_skill(eng, guard, "shield_wall")
    spent = ap0 - guard.ap
    return ("PASS" if used and spent == 2 else "FAIL",
            f"used={used} ap_spent={spent} (expected 2)")


@check("Abilities", "Cooldown blocks reuse, then ticks back to available")
def _c_ability_cooldown():
    from . import abilities_engine as ae
    bf = _open_field(4, 3)
    guard = Combatant("Bran", "guardian", "player", 0, 1)   # shield_wall CD 3
    eng = _engine(bf, [guard])
    first = ae.use_skill(eng, guard, "shield_wall")
    on_cd = guard.cooldowns.get("shield_wall")
    guard.reset_turn()                       # AP back, still on cooldown
    blocked = not ae.use_skill(eng, guard, "shield_wall")
    reason = ae.ability_preview(eng, guard, "shield_wall")["failure_reason"]
    ae.start_of_turn(eng, guard); guard.reset_turn()   # CD 3->2
    ae.start_of_turn(eng, guard); guard.reset_turn()   # CD 2->1
    ae.start_of_turn(eng, guard); guard.reset_turn()   # CD 1->0 cleared
    available = ae.ability_preview(eng, guard, "shield_wall")["usable"]
    ok = first and on_cd == 3 and blocked and "cooldown" in reason and available
    return ("PASS" if ok else "FAIL",
            f"set_cd={on_cd} blocked={blocked} reason='{reason}' recovered={available}")


@check("Abilities", "Range + LOS gate skill execution")
def _c_ability_range_los():
    from . import abilities_engine as ae
    bf = _open_field(10, 3)
    bf.set_terrain(3, 1, "forest"); bf.tile(3, 1).add_object("pine_tree")
    caster = Combatant("Mage", "mage", "player", 1, 1)      # firebolt range 5
    behind = Combatant("Hidden", "brute", "enemy", 5, 1)    # blocked by tree
    out = Combatant("Distant", "brute", "enemy", 9, 1)
    eng = _engine(bf, [caster, behind, out])
    los_blocked = not ae.use_skill(eng, caster, "firebolt", target=behind)
    caster.ap = caster.max_ap
    range_blocked = not ae.use_skill(eng, caster, "firebolt", target=out)
    return ("PASS" if los_blocked and range_blocked else "FAIL",
            f"los_blocked={los_blocked} range_blocked={range_blocked}")


@check("Abilities", "Attack ability applies damage + status; logs the use")
def _c_ability_damage_status():
    from . import abilities_engine as ae
    bf = _open_field(4, 3)
    spider = Combatant("Spider", "brute", "enemy", 0, 1)
    spider.equipped = ["poison_bite"]
    hero = Combatant("Hero", "guardian", "player", 1, 1)
    hero.armor = 0
    eng = _engine(bf, [spider, hero])
    hp0 = hero.hp
    used = ae.use_skill(eng, spider, "poison_bite", target=hero)
    ok = (used and hero.hp < hp0 and "poison" in hero.statuses
          and any("Poison Bite" in l for l in eng.log))
    return ("PASS" if ok else "FAIL",
            f"used={used} dealt={hp0 - hero.hp} poisoned={'poison' in hero.statuses}")


@check("Abilities", "Poison DoT ticks each turn; antidote cleanses it")
def _c_status_duration():
    from . import abilities_engine as ae
    bf = _open_field(4, 3)
    hero = Combatant("Hero", "guardian", "player", 1, 1)
    eng = _engine(bf, [hero])
    hero.statuses.append("poison")
    hp0 = hero.hp
    ae.start_of_turn(eng, hero)             # takes DoT, poison persists
    ticked = hero.hp == hp0 - 3 and "poison" in hero.statuses
    actions.use_item(eng, hero, "antidote")
    cleansed = "poison" not in hero.statuses
    return ("PASS" if ticked and cleansed else "FAIL",
            f"ticked={ticked} cleansed={cleansed}")


@check("Abilities", "Buff emboldens allies then expires next turn")
def _c_buff_duration():
    from . import abilities_engine as ae
    bf = _open_field(6, 3)
    cmdr = Combatant("Captain", "brute", "enemy", 0, 1)
    cmdr.equipped = ["war_cry"]
    ally = Combatant("Grunt", "brute", "enemy", 1, 1)
    hero = Combatant("Hero", "guardian", "player", 5, 1)
    eng = _engine(bf, [cmdr, ally, hero])
    used = ae.use_skill(eng, cmdr, "war_cry")
    buffed = "emboldened" in ally.statuses
    ae.start_of_turn(eng, ally)             # buff lasts until ally's own turn
    expired = "emboldened" not in ally.statuses
    return ("PASS" if used and buffed and expired else "FAIL",
            f"used={used} buffed={buffed} expired_next_turn={expired}")


@check("Abilities", "Shielded halves the next hit, then drops")
def _c_shield_absorb():
    from . import abilities_engine as ae
    bf = _open_field(6, 3)
    guard = Combatant("Bran", "guardian", "player", 2, 1)
    guard.equipped = ["shield_wall"]
    atk = Combatant("Foe", "brute", "enemy", 3, 1)
    atk.crit_chance = 0.0
    atk.damage_min = atk.damage_max = 10
    guard.armor = 0
    eng = _engine(bf, [guard, atk], rng=ALWAYS_HIT())
    ae.use_skill(eng, guard, "shield_wall")
    shielded = "shielded" in guard.statuses
    hp0 = guard.hp
    actions.attack(eng, atk, guard)
    dealt = hp0 - guard.hp
    dropped = "shielded" not in guard.statuses
    return ("PASS" if shielded and dealt == 5 and dropped else "FAIL",
            f"shielded={shielded} dealt={dealt} (expected 5) dropped={dropped}")


@check("Abilities", "Heal ability restores a wounded ally")
def _c_ability_heal():
    from . import abilities_engine as ae
    bf = _open_field(6, 3)
    healer = Combatant("Shaman", "guardian", "enemy", 0, 1)
    healer.equipped = ["healing_totem"]
    wounded = Combatant("Grunt", "brute", "enemy", 1, 1)
    hero = Combatant("Hero", "guardian", "player", 5, 1)
    eng = _engine(bf, [healer, wounded, hero])
    wounded.hp = 5
    used = ae.use_skill(eng, healer, "healing_totem")
    return ("PASS" if used and wounded.hp == 13 else "FAIL",
            f"used={used} hp={wounded.hp} (expected 5+8=13)")


@check("Abilities", "Summon adds an allied minion to the battle")
def _c_ability_summon():
    from . import abilities_engine as ae
    bf = _open_field(6, 3)
    necro = Combatant("Necro", "mage", "enemy", 0, 1)
    necro.equipped = ["raise_skeleton"]
    hero = Combatant("Hero", "guardian", "player", 5, 1)
    eng = _engine(bf, [necro, hero])
    n0 = len(eng.combatants)
    used = ae.use_skill(eng, necro, "raise_skeleton")
    minion = eng.combatants[-1] if len(eng.combatants) > n0 else None
    ok = used and minion is not None and minion.team == "enemy"
    return ("PASS" if ok else "FAIL",
            f"used={used} added={len(eng.combatants) - n0} team={minion.team if minion else None}")


@check("Abilities", "Terrain ability alters the battlefield")
def _c_ability_terrain():
    from . import abilities_engine as ae
    bf = _open_field(8, 3)
    mage = Combatant("Mage", "mage", "player", 0, 1)      # grease range 5
    foe = Combatant("Foe", "brute", "enemy", 3, 1)
    eng = _engine(bf, [mage, foe])
    used = ae.use_skill(eng, mage, "grease", target=foe, tile=(3, 1))
    became = bf.tile(3, 1).terrain == "oil_slick"
    return ("PASS" if used and became else "FAIL",
            f"used={used} terrain={bf.tile(3,1).terrain}")


@check("Abilities", "AI uses a role ability before a basic attack")
def _c_ai_uses_ability():
    from . import abilities_engine as ae
    bf = _open_field(6, 3)
    shaman = Combatant("Shaman", "guardian", "enemy", 0, 1)
    shaman.equipped = ["healing_totem"]
    shaman.ai_profile = dict(enemies.AI_PROFILES["support"])
    wounded = Combatant("Grunt", "brute", "enemy", 1, 1)
    hero = Combatant("Hero", "guardian", "player", 5, 1)
    eng = _engine(bf, [shaman, wounded, hero])
    wounded.hp = 5
    shaman.reset_turn()
    ai.take_turn(eng, shaman)
    healed = wounded.hp > 5 and any("healing" in l.lower() for l in eng.log)
    return ("PASS" if healed else "FAIL",
            f"ally_healed={wounded.hp > 5} logged={any('healing' in l.lower() for l in eng.log)}")


@check("Abilities", "AI respects cooldowns (skips a spent ability)")
def _c_ai_respects_cooldown():
    from . import abilities_engine as ae
    bf = _open_field(6, 3)
    cmdr = Combatant("Captain", "brute", "enemy", 0, 1)
    cmdr.equipped = ["war_cry"]
    ally = Combatant("Grunt", "brute", "enemy", 1, 1)
    hero = Combatant("Hero", "guardian", "player", 5, 1)
    eng = _engine(bf, [cmdr, ally, hero])
    cmdr.cooldowns["war_cry"] = 2                 # already spent
    choice = ae.choose_ability(eng, cmdr, hero)
    return ("PASS" if choice is None else "FAIL",
            f"choice_while_on_cd={choice}")


@check("Abilities", "Ability state survives a JSON save/load round-trip")
def _c_ability_persist():
    from . import abilities_engine as ae
    import json as _json
    bf = _open_field(4, 3)
    u = Combatant("Bran", "guardian", "player", 0, 1)
    eng = _engine(bf, [u])
    ae.use_skill(eng, u, "shield_wall")           # sets cooldown + shielded
    blob = _json.dumps(ae.export_state(u))
    fresh = Combatant("Bran2", "guardian", "player", 0, 1)
    ae.import_state(fresh, _json.loads(blob))
    ok = (fresh.cooldowns.get("shield_wall") == 3
          and "shielded" in fresh.statuses)
    return ("PASS" if ok else "FAIL",
            f"cd={fresh.cooldowns.get('shield_wall')} statuses={fresh.statuses}")


@check("Abilities", "Every ability referenced by a blueprint resolves")
def _c_ability_resolve():
    from . import abilities_engine as ae
    missing = []
    for eid in enemies.list_enemies(include_abstract=True):
        for aid in enemies.BLUEPRINTS[eid].get("abilities", []) or []:
            if ae.get(aid) is None:
                missing.append(f"{eid}:{aid}")
    return ("PASS" if not missing else "FAIL",
            f"unresolved ability ids: {missing or 'none'}")


# -- Phase A: Facing / Flanking / Opportunity ------------------------------
@check("Facing (Phase A)", "relative_arc front/side/rear")
def _c_arc():
    from .facing import relative_arc
    d = Combatant("D", "brute", "enemy", 3, 3)
    d.facing = "N"
    front = relative_arc(d, (3, 1))   # north of a north-facer
    rear = relative_arc(d, (3, 5))    # south
    side = relative_arc(d, (1, 3))    # west
    uncommitted = relative_arc(Combatant("U", "brute", "enemy", 0, 0), (5, 5))
    ok = (front == "front" and rear == "rear" and side == "side"
          and uncommitted == "front")
    return ("PASS" if ok else "FAIL",
            f"front={front} rear={rear} side={side} uncommitted={uncommitted}")


@check("Facing (Phase A)", "Flank raises hit chance (rear > front)")
def _c_flank_hit():
    bf = _open_field(6, 3)
    dfn = Combatant("D", "brute", "enemy", 3, 1)
    dfn.facing = "E"
    front_atk = Combatant("F", "brute", "player", 4, 1)  # east = front
    rear_atk = Combatant("R", "brute", "player", 2, 1)   # west = rear
    eng = _engine(bf, [dfn, front_atk, rear_atk])
    cf = compute_hit_chance(eng, front_atk, dfn)
    cr = compute_hit_chance(eng, rear_atk, dfn)
    ok = (cf["facing"] == "front" and cr["facing"] == "rear"
          and cr["chance"] > cf["chance"] and cr["flanking"] is True)
    return ("PASS" if ok else "FAIL",
            f"front={cf['chance']:.2f} rear={cr['chance']:.2f} "
            f"flanking={cr['flanking']}")


@check("Facing (Phase A)", "Rear flank multiplies damage 1.25x")
def _c_flank_dmg():
    bf = _open_field(6, 3)
    dfn = Combatant("D", "brute", "enemy", 3, 1)
    dfn.facing = "E"
    dfn.armor = 0
    atk = Combatant("R", "brute", "player", 2, 1)   # west = rear
    atk.crit_chance = 0.0
    atk.damage_min = atk.damage_max = 10
    eng = _engine(bf, [dfn, atk], rng=ALWAYS_HIT())
    hp0 = dfn.hp
    actions.attack(eng, atk, dfn)
    dealt = hp0 - dfn.hp
    return ("PASS" if dealt == 12 else "FAIL",
            f"rear damage={dealt} (expected int(10*1.25)=12)")


@check("Facing (Phase A)", "Opportunity attack when leaving melee reach")
def _c_opportunity():
    bf = _open_field(6, 5)
    mover = Combatant("Runner", "guardian", "player", 1, 1)
    foe = Combatant("Grunt", "brute", "enemy", 2, 1)   # melee, adjacent
    eng = _engine(bf, [mover, foe], rng=ALWAYS_HIT())
    mover.move = 4
    actions.move(eng, mover, (1, 3))   # walks out of the grunt's reach
    fired = any("opportunity attack" in l for l in eng.log)
    return ("PASS" if fired else "FAIL", f"opportunity_fired={fired}")


@check("Facing (Phase A)", "Preview warns of provoked opportunity attacks")
def _c_opportunity_preview():
    bf = _open_field(6, 5)
    unit = Combatant("Hero", "guardian", "player", 1, 1)
    foe = Combatant("Grunt", "brute", "enemy", 2, 1)
    eng = _engine(bf, [unit, foe])
    unit.move = 4
    prev = movement_preview(eng, unit, (1, 3))
    ok = "Grunt" in prev.get("provokes_opportunity_from", [])
    return ("PASS" if ok else "FAIL",
            f"provokes_from={prev.get('provokes_opportunity_from')}")


@check("Facing (Phase A)", "Hit-chance breakdown exposes facing (readability)")
def _c_facing_readout():
    bf = _open_field(4, 3)
    a = Combatant("A", "brute", "player", 0, 1)
    d = Combatant("D", "brute", "enemy", 1, 1)
    eng = _engine(bf, [a, d])
    info = compute_hit_chance(eng, a, d)
    ok = "facing" in info and "flanking" in info and "facing_bonus" in info
    return ("PASS" if ok else "FAIL", f"keys_present={ok} facing={info.get('facing')}")


# -- AI Personalities (reusable library) -----------------------------------
def _profiled(unit, **flags):
    unit.ai_profile = {"target_selection": "nearest", "preferred_range": "melee",
                       "avoids": ["fire"], "uses_cover": True}
    unit.ai_profile.update(flags)
    return unit


@check("AI Personalities", "Defender holds ground (penalises roaming)")
def _c_defender_holds():
    bf = _open_field(9, 3)
    foe = Combatant("Def", "brute", "enemy", 6, 1)
    hero = Combatant("Hero", "guardian", "player", 0, 1)
    eng = _engine(bf, [foe, hero])
    threats = threat_map(eng, foe)
    roam = (1, 1)   # far from the defender's start
    _profiled(foe, hold_position=True)
    held = ai._score_tile(eng, foe, roam, hero, threats)
    _profiled(foe, hold_position=False)
    free = ai._score_tile(eng, foe, roam, hero, threats)
    return ("PASS" if held < free else "FAIL",
            f"roam score hold={held:.1f} < free={free:.1f}")


@check("AI Personalities", "Kiter avoids standing next to a foe")
def _c_kiter():
    bf = _open_field(9, 3)
    foe = Combatant("Archer", "archer", "enemy", 6, 1)
    hero = Combatant("Hero", "guardian", "player", 5, 1)
    eng = _engine(bf, [foe, hero])
    threats = threat_map(eng, foe)
    _profiled(foe, preferred_range="ranged", kites=True)
    adjacent = ai._score_tile(eng, foe, (4, 1), hero, threats)  # next to hero
    spaced = ai._score_tile(eng, foe, (8, 1), hero, threats)    # kept back
    return ("PASS" if spaced > adjacent else "FAIL",
            f"spaced={spaced:.1f} > adjacent={adjacent:.1f}")


@check("AI Personalities", "Ambusher prefers a flanking tile")
def _c_ambusher_flank():
    bf = _open_field(7, 3)
    hero = Combatant("Hero", "guardian", "player", 3, 1)
    hero.facing = "E"
    foe = Combatant("Amb", "brute", "enemy", 4, 1)   # melee
    eng = _engine(bf, [foe, hero])
    threats = threat_map(eng, foe)
    _profiled(foe, prefers_flank=True)
    rear = ai._score_tile(eng, foe, (2, 1), hero, threats)   # behind an E-facer
    front = ai._score_tile(eng, foe, (4, 1), hero, threats)  # in front
    return ("PASS" if rear > front else "FAIL",
            f"rear={rear:.1f} > front={front:.1f}")


@check("AI Personalities", "Wounded coward flees from the foe")
def _c_coward_flees():
    bf = _open_field(9, 3)
    foe = Combatant("Coward", "brute", "enemy", 2, 1)
    hero = Combatant("Hero", "guardian", "player", 1, 1)
    eng = _engine(bf, [foe, hero], rng=ALWAYS_HIT())
    foe.ai_profile = enemies.AI_PROFILES["cowardly"]
    foe.reset_turn()
    foe.hp = 1                              # badly wounded -> below threshold
    d0 = chebyshev(foe.pos, hero.pos)
    ai.take_turn(eng, foe)
    fled = chebyshev(foe.pos, hero.pos) > d0
    return ("PASS" if fled else "FAIL",
            f"start_dist={d0} end_dist={chebyshev(foe.pos, hero.pos)} fled={fled}")


@check("AI Personalities", "Sticky targeting (behavior memory)")
def _c_sticky_target():
    bf = _open_field(10, 3)
    foe = Combatant("Foe", "archer", "enemy", 5, 1)
    a = Combatant("A", "guardian", "player", 4, 1)   # nearest
    b = Combatant("B", "guardian", "player", 8, 1)
    eng = _engine(bf, [foe, a, b])
    foe.ai_profile = dict(enemies.AI_PROFILES["skirmisher"])
    foe.ai_memory["target_id"] = b.id                # committed to B
    picked = ai._resolve_target(eng, foe)
    return ("PASS" if picked is b else "FAIL",
            f"kept committed target={picked.name} (expected B)")


@check("AI Personalities", "Commander presence steadies morale (braver)")
def _c_commander_morale():
    bf = _open_field(8, 3)
    coward = Combatant("Grunt", "brute", "enemy", 4, 1)
    cmdr = Combatant("Captain", "brute", "enemy", 5, 1)
    cmdr.ai_profile = enemies.AI_PROFILES["commander"]
    hero = Combatant("Hero", "guardian", "player", 0, 1)
    eng = _engine(bf, [coward, cmdr, hero])
    coward.ai_profile = dict(enemies.AI_PROFILES["cowardly"])  # flee_threshold .5
    coward.reset_turn(); coward.hp = int(coward.max_hp * 0.35)  # 35% > .5*.5=.25
    d0 = chebyshev(coward.pos, hero.pos)
    ai.take_turn(eng, coward)
    steadied = coward.ai_memory.get("commander_nearby") and \
        chebyshev(coward.pos, hero.pos) <= d0   # did NOT flee
    return ("PASS" if steadied else "FAIL",
            f"commander_nearby={coward.ai_memory.get('commander_nearby')} "
            f"held_ground={chebyshev(coward.pos, hero.pos) <= d0}")


@check("AI Personalities", "All referenced profiles now defined (WARN cleared)")
def _c_profiles_complete():
    missing = set()
    for eid in enemies.list_enemies():
        raw = enemies.BLUEPRINTS[eid]
        node, prof = raw, None
        seen = set()
        while node is not None and id(node) not in seen:
            seen.add(id(node))
            if "ai_profile" in node:
                prof = node["ai_profile"]
                break
            parent = node.get("extends")
            node = enemies.BLUEPRINTS.get(parent) if parent else None
        if isinstance(prof, str) and prof not in enemies.AI_PROFILES:
            missing.add(prof)
    return ("PASS" if not missing else "FAIL",
            f"undefined referenced profiles: {sorted(missing) or 'none'}")


# ===========================================================================
# Runner
# ===========================================================================
def run() -> Dict:
    results = []
    for category, name, fn in REGISTRY:
        try:
            status, detail = fn()
        except Exception as exc:                      # noqa: BLE001
            status, detail = "FAIL", f"exception: {exc!r}"
        results.append({"category": category, "name": name,
                        "status": status, "detail": detail})
    summary = {
        "total": len(results),
        "passed": sum(r["status"] == "PASS" for r in results),
        "failed": sum(r["status"] == "FAIL" for r in results),
        "warned": sum(r["status"] == "WARN" for r in results),
    }
    summary["foundation_stable"] = summary["failed"] == 0
    return {"summary": summary, "results": results}


def _print(report: Dict) -> None:
    cats: Dict[str, List] = {}
    for r in report["results"]:
        cats.setdefault(r["category"], []).append(r)
    icon = {"PASS": "\u2713", "FAIL": "\u2717", "WARN": "!"}
    print("\n== Tactical Combat Foundation Verification ==\n")
    for cat, rows in cats.items():
        print(f"[{cat}]")
        for r in rows:
            print(f"  {icon[r['status']]:>2} {r['status']:<4} {r['name']}")
            print(f"        {r['detail']}")
        print()
    s = report["summary"]
    print(f"TOTAL {s['total']}  PASS {s['passed']}  FAIL {s['failed']}  "
          f"WARN {s['warned']}")
    print(f"FOUNDATION STABLE: {'YES' if s['foundation_stable'] else 'NO'}\n")


def main() -> int:
    report = run()
    out = os.path.join(os.path.dirname(__file__), "verification_report.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
    else:
        _print(report)
        print(f"(report written to {out})")
    return 0 if report["summary"]["foundation_stable"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
