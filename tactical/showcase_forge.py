"""
The Forge Stand — Torren's Field-Forge Vertical-Slice Encounter
===============================================================

A companion piece to :mod:`tactical.showcase` (The Sundered Span). Where the
Span proves the general combat pillars, **The Forge Stand exists to prove one
thing: Torren Ironhall's identity as the party's battlefield *shaper* and
craftsman-support is real in play, not just on paper.**

Premise
-------
Three heroes are caught on open ground when an aggressive goblin raiding swarm —
three brutes that charge, plus an archer that softens the line — closes in. Two
of the heroes (a ranger and a mage) are glass cannons: if the brutes reach them,
they die in a round or two. **Torren cannot save them with his hammer** — he is
sturdy but a deliberately weak hitter; he cannot out-damage the swarm. His only
answer is to *reshape the fight*: scatter spike-barriers (rubble) that both slow
the charge and give the fragile heroes cover, plant a forge beacon, field-temper
armour, body-block the gap between the boulders, and repair the wounded — turning
an exposed backline into a fortified line that grinds the swarm down.

Map (12 x 7): mostly open ground. Two boulders at (5,1) and (5,5) frame a natural
gap near the party's line — a partial choke Torren reinforces. The party holds
the west (Torren fronting the ranger and mage); the swarm charges from the east.

The thesis (verified — see ``scripts/forge_showcase_report.py``)
----------------------------------------------------------------
Two controllers drive the *same* party against the *same* raiders; the **only**
difference is Torren's behaviour:

* :func:`forge_tactician_controller` — Torren builds/slows, buffs and repairs.
  **The party wins ~85%+ of seeds and almost never loses.**
* :func:`no_forge_controller` — Torren only swings his (weak) hammer and
  advances; he **never uses a Field-Forge construct.** The fragile backline is
  overwhelmed and **the party loses far more often than it wins.**

The gap between the two outcomes *is* the proof that Torren's construct kit — not
raw stats — is what wins the fight. See ``backend/tests/test_forge_showcase.py``.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Tuple

from .battlefield import Battlefield
from .entities import Combatant
from .engine import CombatEngine, CombatContext
from . import enemies, actions
from . import abilities_engine as ae
from .inspection import chebyshev
from . import showcase

BATTLEFIELD_ID = "forge_stand"
XY = Tuple[int, int]


# ---------------------------------------------------------------------------
# Battlefield — a barren flat with scarce natural cover (so cover must be BUILT)
# ---------------------------------------------------------------------------
def build_battlefield() -> Battlefield:
    bf = Battlefield(12, 7, battlefield_id=BATTLEFIELD_ID)
    # Two boulders frame a natural gap near the party's line — a partial choke
    # that Torren can reinforce. Everything else is open ground.
    bf.tile(5, 1).add_object("boulder")
    bf.tile(5, 5).add_object("boulder")
    bf.set_terrain(10, 3, "hill")
    return bf


# ---------------------------------------------------------------------------
# Combatants
# ---------------------------------------------------------------------------
def build_party() -> List[Combatant]:
    """A weak-hitting but sturdy Torren fronting a fragile ranged backline. He
    cannot win by damage — only by shaping the fight and keeping the two glass
    cannons alive."""
    torren = Combatant("Torren Ironhall", "smith", "player", 3, 3)
    sella = Combatant("Sella Quickbow", "ranger", "player", 2, 2)
    corwin = Combatant("Corwin Vale", "mage", "player", 2, 4)
    for h in (torren, sella, corwin):
        h.items = ["healing_potion"]
    return [torren, sella, corwin]


def build_enemies() -> List[Combatant]:
    """An aggressive raiding swarm — three brutes that charge and an archer that
    softens the backline. Left unchecked they reach the fragile heroes in two
    turns and overwhelm them."""
    return [
        enemies.spawn_enemy("goblin_warrior", 9, 2, name="Corrupted Raider"),
        enemies.spawn_enemy("goblin_warrior", 9, 4, name="Ashfang Raider"),
        enemies.spawn_enemy("goblin_warrior", 10, 3, name="Bloodtusk Raider"),
        enemies.spawn_enemy("goblin_archer", 10, 1, name="Ridge Sniper"),
    ]


def build_encounter(rng: Optional[random.Random] = None,
                    world_state: Optional[dict] = None) -> CombatEngine:
    bf = build_battlefield()
    combatants = build_party() + build_enemies()
    return CombatEngine(bf, combatants,
                        context=CombatContext("location", "forge_stand"),
                        rng=rng or random.Random(77),
                        world_state=world_state)


# ---------------------------------------------------------------------------
# Field-Forge helpers
# ---------------------------------------------------------------------------
def _living_enemies(engine, unit):
    return showcase._living_enemies(engine, unit)


def _buildable(engine, unit, spot: XY, rng: int) -> bool:
    if not engine.bf.in_bounds(*spot) or spot == unit.pos:
        return False
    if chebyshev(unit.pos, spot) > rng:
        return False
    return engine.bf.line_of_sight(unit.pos, spot)


def _cover_step(defender: XY, attacker: XY) -> XY:
    """The tile one step from ``defender`` toward ``attacker`` — the tile that,
    if it holds cover, shields the defender (mirror of Battlefield.directional_cover)."""
    dx, dy = attacker[0] - defender[0], attacker[1] - defender[1]
    sx = defender[0] + (1 if dx > 0 else -1 if dx < 0 else 0) if abs(dx) >= abs(dy) else defender[0]
    sy = defender[1] + (1 if dy > 0 else -1 if dy < 0 else 0) if abs(dy) > abs(dx) else defender[1]
    return (sx, sy)


def _ally_has_cover(engine, ally, threats) -> bool:
    if not threats:
        return True
    enemy = min(threats, key=lambda e: chebyshev(ally.pos, e.pos))
    return engine.bf.directional_cover(ally.pos, enemy.pos) != "none"


def _lay_cover_for(engine, unit, ally, threats) -> bool:
    """Scatter a spike-barrier (rubble = half cover, does NOT block LOS) on the
    tile between a fragile ally and the nearest raider, so the ally fights from
    cover while keeping its own shots."""
    if not threats:
        return False
    enemy = min(threats, key=lambda e: chebyshev(ally.pos, e.pos))
    spot = _cover_step(ally.pos, enemy.pos)
    if not engine.bf.in_bounds(*spot):
        return False
    tile = engine.bf.tile(*spot)
    if tile.occupant is not None:
        return False
    if tile.terrain == "rubble" or tile.objects:      # already gives cover
        return False
    if not _buildable(engine, unit, spot, 3):
        return False
    return ae.use_skill(engine, unit, "spike_barrier", tile=spot)


def _slow_nearest_melee(engine, unit, threats) -> bool:
    """Drop rubble one step toward the nearest charger to meter its approach."""
    melee = [e for e in threats if e.attack_range <= 1]
    if not melee:
        return False
    charger = min(melee, key=lambda e: chebyshev(unit.pos, e.pos))
    spot = _cover_step(unit.pos, charger.pos)
    if not engine.bf.in_bounds(*spot):
        return False
    tile = engine.bf.tile(*spot)
    if tile.occupant is not None or tile.terrain == "rubble" or tile.objects:
        return False
    if not _buildable(engine, unit, spot, 3):
        return False
    return ae.use_skill(engine, unit, "spike_barrier", tile=spot)


def _torren_forge_turn(engine, unit) -> None:
    ae.start_of_turn(engine, unit)
    showcase._sip_if_hurt(engine, unit)
    threats = _living_enemies(engine, unit)
    backline = [a for a in engine.allies_of(unit) if a.alive and a is not unit]

    # 1) Emergency repair — keep a fragile hero alive.
    crit = [a for a in [unit] + backline
            if a.hp < a.max_hp * 0.4 and chebyshev(unit.pos, a.pos) <= 2]
    if unit.ap > 0 and crit:
        ae.use_skill(engine, unit, "battle_repairs", target=min(crit, key=lambda a: a.hp))

    # 2) SIGNATURE: give every exposed fragile hero cover (most-wounded first).
    for ally in sorted(backline, key=lambda a: a.hp):
        if unit.ap <= 0:
            break
        if not _ally_has_cover(engine, ally, threats):
            _lay_cover_for(engine, unit, ally, threats)

    # 3) Plant the forge beacon once, then field-temper armour when pressed.
    if unit.ap > 0 and not unit.ai_memory.get("beacon_set") and backline \
            and any(chebyshev(unit.pos, e.pos) <= 8 for e in threats):
        if ae.use_skill(engine, unit, "forge_beacon"):
            unit.ai_memory["beacon_set"] = True
    if unit.ap > 0 and "shielded" not in unit.statuses \
            and any(chebyshev(unit.pos, e.pos) <= 4 for e in threats):
        ae.use_skill(engine, unit, "reinforce_armor")

    # 4) Still have an action? Meter the charger with rubble.
    if unit.ap > 0:
        _slow_nearest_melee(engine, unit, threats)

    # 4b) Endgame mop-up only: when a single kiting raider is all that remains,
    # the sturdy smith runs it down himself rather than send a fragile hero into
    # the open. He never abandons the backline while the swarm is still a threat.
    if len(threats) == 1 and chebyshev(unit.pos, threats[0].pos) > 1:
        showcase._move_toward(engine, unit, threats[0].pos)

    # 5) Crack an adjacent skull, else brace for counters.
    adj = [e for e in threats if chebyshev(unit.pos, e.pos) <= 1]
    if unit.ap > 0 and adj:
        actions.attack(engine, unit, adj[0])
    elif unit.ap > 0:
        actions.prepare(engine, unit)


def _torren_brawler_turn(engine, unit) -> None:
    """The control case: a strong dwarf who *never builds* — advance and swing."""
    ae.start_of_turn(engine, unit)
    showcase._sip_if_hurt(engine, unit)
    tgt = showcase._focus_target(engine, unit)
    if tgt is None:
        return
    if chebyshev(unit.pos, tgt.pos) > 1:
        showcase._move_toward(engine, unit, tgt.pos)
    adj = [e for e in _living_enemies(engine, unit) if chebyshev(unit.pos, e.pos) <= 1]
    while unit.ap > 0 and adj:
        if not actions.attack(engine, unit, adj[0]):
            break
        adj = [e for e in _living_enemies(engine, unit) if chebyshev(unit.pos, e.pos) <= 1]
    if unit.ap > 0:
        actions.prepare(engine, unit)


def _backline_turn(engine, unit) -> None:
    """Shared fragile-hero play (identical in both controllers): hold position
    and shoot when there is a shot; otherwise brace a reaction. They do NOT roam
    into the open — surviving depends on Torren's cover."""
    ae.start_of_turn(engine, unit)
    showcase._sip_if_hurt(engine, unit)
    shots = [e for e in _living_enemies(engine, unit)
             if chebyshev(unit.pos, e.pos) <= unit.attack_range
             and engine.bf.line_of_sight(unit.pos, e.pos)]
    if not shots:
        # No lane: pursue the nearest raider to open one, but hold the defensive
        # line (never push east of x=6 into the open).
        living = _living_enemies(engine, unit)
        if living:
            nearest = min(living, key=lambda e: chebyshev(unit.pos, e.pos))
            # Hold the defensive line — fragile heroes never break into the open.
            reach = {xy: c for xy, c in engine.bf.reachable(unit.pos, unit.move).items()
                     if xy[0] <= 3}
            reach[unit.pos] = 0
            dest = min(reach, key=lambda xy: chebyshev(xy, nearest.pos))
            if dest != unit.pos:
                actions.move(engine, unit, dest)
        shots = [e for e in _living_enemies(engine, unit)
                 if chebyshev(unit.pos, e.pos) <= unit.attack_range
                 and engine.bf.line_of_sight(unit.pos, e.pos)]
        if not shots:
            if unit.ap > 0:
                actions.prepare(engine, unit)
            return
    tgt = sorted(shots, key=lambda e: (showcase._priority(e), e.hp))[0]
    if unit.cls == "ranger":
        if unit.ap > 0 and "marked" not in tgt.statuses:
            ae.use_skill(engine, unit, "hunters_mark", target=tgt)
        if not showcase._shoot(engine, unit, tgt, "aimed_shot"):
            showcase._shoot(engine, unit, tgt)
    else:  # mage
        if not showcase._shoot(engine, unit, tgt, "firebolt"):
            showcase._shoot(engine, unit, tgt)


# ---------------------------------------------------------------------------
# Party controllers — identical backline play; only Torren differs
# ---------------------------------------------------------------------------
def forge_tactician_controller(engine, unit) -> None:
    if unit.cls == "smith":
        _torren_forge_turn(engine, unit)
    else:
        _backline_turn(engine, unit)


def no_forge_controller(engine, unit) -> None:
    if unit.cls == "smith":
        _torren_brawler_turn(engine, unit)
    else:
        _backline_turn(engine, unit)


# ---------------------------------------------------------------------------
# Headless resolution + win-rate proof
# ---------------------------------------------------------------------------
def play_headless(seed: int = 77, max_rounds: int = 40, controller=None) -> str:
    eng = build_encounter(rng=random.Random(seed))
    return eng.auto_battle(max_rounds=max_rounds,
                           player_controller=controller or forge_tactician_controller)


def win_rate(controller, seeds: int = 30, max_rounds: int = 40) -> float:
    wins = sum(1 for s in range(seeds)
               if play_headless(seed=s, max_rounds=max_rounds, controller=controller) == "player")
    return wins / seeds


# ---------------------------------------------------------------------------
# Design manifest — Field-Forge constructs mapped to the decisions they create
# ---------------------------------------------------------------------------
def forge_manifest() -> Dict[str, Dict]:
    return {
        "spike_barrier": {
            "shapes": "Rubble = half cover that does NOT block LOS, and difficult ground.",
            "decision": "Lay it in front of a fragile hero for cover, or in a "
                        "charger's path to slow it — you rarely have AP for both.",
        },
        "reinforced_wall": {
            "shapes": "Full-cover, LOS-blocking wall segment (impassable).",
            "decision": "Hard-cut a sniper's lane without walling off your own shots.",
        },
        "field_barricade": {
            "shapes": "Half-cover crate that also blocks LOS (cheaper, 1 AP).",
            "decision": "A quick 1-AP screen now, or save for a full 2-AP wall.",
        },
        "forge_beacon": {
            "shapes": "Morale aura — emboldens allies (+hit) in range.",
            "decision": "Group up for the beacon vs spread out to spread the risk.",
        },
        "reinforce_armor": {
            "shapes": "Shields Torren and adjacent allies (halves one hit).",
            "decision": "Time it for the incoming alpha strike, not the chip damage.",
        },
        "battle_repairs": {
            "shapes": "Restores a wounded ally in reach (the party's sustain).",
            "decision": "Repair now, or spend the action shaping the field first.",
        },
    }


def identity_summary() -> Dict[str, str]:
    return {
        "identity": "Battlefield shaper + craftsman-support (not a duelist).",
        "proof": "Same party, same enemies: building wins; brawling loses. The "
                 "delta is the Field Forge.",
    }
