"""
The Sundered Span — Gold-Standard Vertical-Slice Encounter
==========================================================

A single hand-built battle designed to demonstrate **every** canonical combat
pillar of the `tactical/` engine at once. It is the reference implementation
for the Encounter Design Bible: not a template to mass-produce, but the bar
every future encounter is measured against.

Premise
-------
A four-hero party is crossing a ravine on an old stone bridge in the Mossroot
borderlands when a corrupted goblin raiding party springs an ambush from the
eastern ridge. The party is outnumbered (4 vs 5) and out-massed (100 HP vs
148 HP) against armoured goblins that shrug off a hero's basic swing. The core
thesis: **button-mashing loses; tactics win.** Victory comes from focus-fire,
flanking, high ground, ability combos, the terrain, and healing potions — not
from trading blows.

Map (12 x 7) — west (players) vs east (goblins), split by a ravine at x=6::

     0   1   2   3   4   5   6   7   8   9  10  11
   +------------------------------------------------
 0 | .   .   .   .   .   .   #   .   H   a   C   .   <- Ridge Sniper (elev)
 1 | .   .   .   T   .   H   #   .   W   .   .   .
 2 | .   .   M   .   T   .   #   .   o   g   .   .   <- Warlord Gruk on oil
 3 | .   .   .   .   G   .   =   S   b   .   .   .   <- the Span (bridge =)
 4 | .   .   .   T   R   H   #   r   .   .   G   .       S=Warden r=Raider
 5 | .   .   h   h   .   ~   ~   ~   .   .   .   .   <- southern ford
 6 | .   C   h   .   .   .   #   .   .   .   .   .

Legend: ``.`` plains/road  ``T`` forest+tree (½ cover, blocks LOS, flammable)
``H/h`` hill (elev 1)  ``C`` cliff (elev 2)  ``#`` boulder (impassable, full
cover)  ``=`` bridge plank (destructible/flammable chokepoint)  ``~`` water
(difficult ford)  ``W`` wall (full cover)  ``o`` oil slick (flammable)  ``b``
oil barrel (explosive).

Why it is the gold standard
---------------------------
See :func:`pillar_manifest` — every entry maps a concrete battlefield feature
to the pillar it exercises and the player decision it creates. The encounter is
authored so that **multiple** distinct strategies contribute to a win (focus the
healer, take the high ground, flank the warlord, hold the span, spend potions),
verified independently in ``backend/tests/test_showcase_encounter.py``. The
reference :func:`tactician_controller` plays the intended combined-arms plan and
wins the majority of seeds — the playability proof.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional

from .battlefield import Battlefield
from .entities import Combatant
from .engine import CombatEngine, CombatContext
from . import enemies, actions
from . import abilities_engine as ae
from .inspection import chebyshev, compute_hit_chance, threat_map

BATTLEFIELD_ID = "sundered_span"


# ---------------------------------------------------------------------------
# Battlefield
# ---------------------------------------------------------------------------
def build_battlefield() -> Battlefield:
    bf = Battlefield(12, 7, battlefield_id=BATTLEFIELD_ID)

    for xy in [(4, 3), (5, 3), (7, 3)]:                 # approach lane -> bridge
        bf.set_terrain(*xy, "road")

    for xy in [(3, 1), (4, 2), (3, 4)]:                 # near-side woods (cover)
        bf.set_terrain(*xy, "forest")
        bf.tile(*xy).add_object("pine_tree")

    # The ravine: impassable chasm at column x=6; cross at the bridge (fast
    # chokepoint, y=3) or the slow southern ford (water, y=5).
    for y in (0, 1, 2, 4, 6):
        bf.tile(6, y).add_object("boulder")
    bf.set_terrain(6, 3, "road")
    bf.tile(6, 3).add_object("bridge_plank")
    for xy in [(5, 5), (6, 5), (7, 5)]:
        bf.set_terrain(*xy, "water")

    # Player-side high ground: a mid-field hill near the bridge (in ranged
    # reach of the whole enemy line) plus a scenic SW cliff.
    for xy in [(5, 1), (5, 4), (2, 5), (3, 5), (2, 6)]:
        bf.set_terrain(*xy, "hill")
    bf.set_terrain(1, 6, "cliff_top")

    # Enemy ridge (north-east): the sniper's high ground.
    bf.set_terrain(8, 0, "hill")
    bf.set_terrain(10, 0, "cliff_top")

    # Enemy fortification wall (full cover for the backline).
    bf.tile(8, 1).add_object("wall_segment")

    # Hazard cluster around the warlord: oil slicks + explosive barrel. Fire
    # here is zone-control and chip damage that forces the warlord off his spot.
    for xy in [(8, 2), (9, 2)]:
        bf.set_terrain(*xy, "oil_slick")
    bf.tile(8, 3).add_object("oil_barrel")

    return bf


# ---------------------------------------------------------------------------
# Combatants
# ---------------------------------------------------------------------------
def build_party() -> List[Combatant]:
    """The four heroes. Each carries signature abilities plus a healing potion
    (the Item pillar and the party's only sustain)."""
    bran = Combatant("Bran Stoneward", "guardian", "player", 4, 3)      # anchor
    sella = Combatant("Sella Quickbow", "ranger", "player", 4, 4)       # sniper
    corwin = Combatant("Corwin Vale", "mage", "player", 2, 2)           # control
    vesper = Combatant("Vesper Nightaine", "rogue", "player", 3, 3)     # flanker
    bran.items = ["healing_potion", "healing_potion", "antidote"]
    sella.items = ["healing_potion"]
    corwin.items = ["healing_potion"]
    vesper.items = ["healing_potion"]
    return [bran, sella, corwin, vesper]


def build_enemies() -> List[Combatant]:
    """A goblin ambush of five distinct AI archetypes (data-driven profiles)."""
    return [
        enemies.spawn_enemy("goblin_chief", 9, 2, name="Warlord Gruk"),         # commander/buffs
        enemies.spawn_enemy("goblin_shaman", 10, 4, name="Mossroot Shaman"),    # support/heals
        enemies.spawn_enemy("goblin_spearman", 7, 3, name="Bridge Warden"),     # defender/holds
        enemies.spawn_enemy("goblin_archer", 9, 0, name="Ridge Sniper"),        # skirmisher/kites
        enemies.spawn_enemy("goblin_warrior", 7, 4, name="Corrupted Raider"),   # brute/charges
    ]


def build_encounter(rng: Optional[random.Random] = None,
                    world_state: Optional[dict] = None) -> CombatEngine:
    bf = build_battlefield()
    combatants = build_party() + build_enemies()
    return CombatEngine(bf, combatants,
                        context=CombatContext("location", "sundered_span"),
                        rng=rng or random.Random(77),
                        world_state=world_state)


# ---------------------------------------------------------------------------
# Reference tactician — the intended combined-arms plan (playability oracle)
# ---------------------------------------------------------------------------
def _living_enemies(engine, unit):
    return [e for e in engine.enemies_of(unit) if e.alive]


def _priority(e) -> int:
    """Kill order: healer > sniper > commander > the rest (soft targets and
    force-multipliers first)."""
    p = e.ai_profile
    if p.get("buffs_allies"):
        return 0
    if p.get("kites"):
        return 1
    if p.get("coordinates") or "rally" in getattr(e, "equipped", []):
        return 2
    return 3


def _focus_target(engine, unit):
    es = _living_enemies(engine, unit)
    if not es:
        return None
    return sorted(es, key=lambda e: (_priority(e), e.hp,
                                     chebyshev(unit.pos, e.pos)))[0]


def _sip_if_hurt(engine, unit) -> bool:
    if unit.hp <= unit.max_hp * 0.4 and "healing_potion" in getattr(unit, "items", []):
        return actions.use_item(engine, unit, "healing_potion", target=unit)
    return False


def _move_toward(engine, unit, dest, stop_at: int = 0):
    reach = engine.bf.reachable(unit.pos, unit.move)
    reach[unit.pos] = 0
    best = min(reach, key=lambda xy: (chebyshev(xy, dest), -engine.bf.tile(*xy).elevation))
    if best != unit.pos:
        actions.move(engine, unit, best)


def _shoot(engine, unit, tgt, skill=None) -> bool:
    if chebyshev(unit.pos, tgt.pos) <= unit.attack_range and \
            compute_hit_chance(engine, unit, tgt)["chance"] > 0:
        if skill and ae.use_skill(engine, unit, skill, target=tgt):
            return True
        return actions.attack(engine, unit, tgt)
    return False


def tactician_controller(engine, unit) -> None:
    """A competent player: focus the priority target, use high ground, flank,
    combo abilities, and sip a potion when low. This is the reference 'good
    play' the encounter is balanced around."""
    ae.start_of_turn(engine, unit)
    _sip_if_hurt(engine, unit)
    tgt = _focus_target(engine, unit)
    if tgt is None:
        return
    cls = unit.cls

    if cls == "ranger":
        reach = engine.bf.reachable(unit.pos, unit.move)
        reach[unit.pos] = 0

        def rscore(xy):
            los = engine.bf.line_of_sight(xy, tgt.pos)
            inr = chebyshev(xy, tgt.pos) <= unit.attack_range
            return (engine.bf.tile(*xy).elevation * 5 + (10 if los and inr else 0)
                    - (3 if xy in threat_map(engine, unit) else 0))
        best = max(reach, key=rscore)
        if best != unit.pos:
            actions.move(engine, unit, best)
        if chebyshev(unit.pos, tgt.pos) <= unit.attack_range and \
                engine.bf.line_of_sight(unit.pos, tgt.pos):
            if "marked" not in tgt.statuses:
                ae.use_skill(engine, unit, "hunters_mark", target=tgt)
            if not _shoot(engine, unit, tgt, "aimed_shot"):
                _shoot(engine, unit, tgt)
        return

    if cls == "mage":
        # Prefer igniting an enemy standing on flammable ground; else firebolt
        # the softest reachable target.
        if not _shoot(engine, unit, tgt, "firebolt"):
            _move_toward(engine, unit, tgt.pos)
            for e in sorted(_living_enemies(engine, unit), key=lambda e: e.hp):
                if _shoot(engine, unit, e, "firebolt"):
                    break
        return

    if cls == "rogue":
        # Shadowstep to a rear tile of the priority target, then backstab.
        for nb in engine.bf.neighbors(*tgt.pos):
            if engine.bf.tile(*nb).is_passable() and \
                    chebyshev(unit.pos, nb) <= 4 and \
                    engine.bf.line_of_sight(unit.pos, nb):
                if ae.use_skill(engine, unit, "shadowstep", tile=nb):
                    break
        if chebyshev(unit.pos, tgt.pos) <= 1:
            if not ae.use_skill(engine, unit, "backstab", target=tgt):
                actions.attack(engine, unit, tgt)
        else:
            _move_toward(engine, unit, tgt.pos)
            adj = [e for e in _living_enemies(engine, unit)
                   if chebyshev(unit.pos, e.pos) <= 1]
            if adj:
                actions.attack(engine, unit, adj[0])
        return

    # guardian: anchor the bridge, taunt the biggest threat, else counter.
    if chebyshev(unit.pos, tgt.pos) > 1:
        _move_toward(engine, unit, (5, 3))
    adj = [e for e in _living_enemies(engine, unit)
           if chebyshev(unit.pos, e.pos) <= 1]
    if adj:
        actions.attack(engine, unit, adj[0])
    elif unit.ap >= 2 and any(chebyshev(unit.pos, e.pos) <= 3
                              for e in _living_enemies(engine, unit)):
        threat = min(_living_enemies(engine, unit),
                     key=lambda e: chebyshev(unit.pos, e.pos))
        if not ae.use_skill(engine, unit, "taunt", target=threat):
            actions.prepare(engine, unit)
    elif unit.ap > 0:
        actions.prepare(engine, unit)


def play_headless(seed: int = 77, max_rounds: int = 40) -> str:
    """Resolve the encounter with the reference tactician driving the party."""
    eng = build_encounter(rng=random.Random(seed))
    return eng.auto_battle(max_rounds=max_rounds,
                           player_controller=tactician_controller)


# ---------------------------------------------------------------------------
# Design manifest — the reference used by tests and the Encounter Design Bible
# ---------------------------------------------------------------------------
def pillar_manifest() -> Dict[str, Dict]:
    """Map each canonical combat pillar to the concrete feature that proves it
    and the player decision it creates. Single source cited by the verification
    suite and the Encounter Design Bible."""
    return {
        "battlefield_is_a_character": {
            "feature": "Ravine chokepoint + southern ford + woods + ridges.",
            "decision": "Cross fast at the bridge or slow at the ford?",
        },
        "difficult_terrain": {
            "feature": "Forest (cost 2), water ford (cost 3), hill/cliff (cost 2).",
            "decision": "Spend movement for cover/high ground, or stay mobile?",
        },
        "cover": {
            "feature": "Half cover (trees), full cover (wall, boulders).",
            "decision": "Advance behind cover vs the ridge sniper.",
        },
        "elevation": {
            "feature": "Player mid-field hill + SW cliff; enemy NE ridge.",
            "decision": "Take the hill for the elevation to-hit/LOS edge.",
        },
        "line_of_sight": {
            "feature": "Trees/walls/boulders block LOS; high ground sees over them.",
            "decision": "Break the sniper's LOS, or out-elevate it.",
        },
        "movement_and_ap": {
            "feature": "Wide field, a chokepoint, and a squishy back line.",
            "decision": "Ration move vs action every turn under threat.",
        },
        "facing_flanking_opportunity": {
            "feature": "Armoured goblins; the Bridge Warden (spear reach 2) zones the span; melee raiders chase.",
            "decision": "Flank for rear damage; leaving a melee raider's reach provokes an opportunity attack.",
        },
        "prepare_reactions": {
            "feature": "Guardian counter, ranger reaction shot, rogue evasion.",
            "decision": "Hold the span behind a prepared reaction wall.",
        },
        "abilities_and_cooldowns": {
            "feature": "Signature skills on every hero and the warlord/shaman.",
            "decision": "Sequence cooldowns; abilities punch through armour basics can't.",
        },
        "items": {
            "feature": "Each hero carries a healing potion (guardian also an antidote).",
            "decision": "Spend the party's only sustain at the right moment.",
        },
        "ai_personalities": {
            "feature": "Commander, Support, Defender, Skirmisher, Brute — 5 profiles.",
            "decision": "Read intent: the warlord buffs, the shaman heals — kill them first.",
        },
        "battlefield_evolves": {
            "feature": "Oil slicks + explosive barrel around the warlord.",
            "decision": "Ignite to deny ground and chip the backline — then respect the fire.",
        },
        "information_before_commitment": {
            "feature": "Hit-chance, movement and ability previews for every action.",
            "decision": "No blind moves — every threat is legible before you commit.",
        },
        "companion_party": {
            "feature": "A four-hero party with complementary, non-overlapping roles.",
            "decision": "Win by combined arms, not by any single hero.",
        },
        "multiple_solutions": {
            "feature": "Focus the healer / take the high ground / flank the warlord / "
                       "hold the span / spend potions.",
            "decision": "Several distinct strategies contribute to the win.",
        },
    }
