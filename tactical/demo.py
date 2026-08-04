"""
Demo battlefield
================

A hand-built encounter that showcases every pillar: unique terrain (forest,
hill, cliff, water, a bridge, oil barrels, a wall), elevation, cover, line of
sight, hazards, environmental interactions, and a mixed party vs. mixed
enemies. Used by the in-game demo and the harness.

Map (8x6):
    - a wooded left flank (trees = cover + flammable)
    - a hill/cliff on the right (elevation for the ranger)
    - a river down the middle crossed by a wooden bridge
    - oil barrels + a wall near the enemy side
"""

from __future__ import annotations

import random
from typing import Optional

from .battlefield import Battlefield
from .entities import Combatant
from .engine import CombatEngine, CombatContext


def build_battlefield() -> Battlefield:
    bf = Battlefield(8, 6, battlefield_id="riverside_ambush")

    # Wooded left flank
    for (x, y) in [(1, 1), (1, 2), (2, 3), (1, 4)]:
        bf.set_terrain(x, y, "forest")
        bf.tile(x, y).add_object("pine_tree")

    # Hill + cliff on the right (elevation)
    bf.set_terrain(6, 1, "hill")
    bf.set_terrain(7, 1, "cliff_top")
    bf.set_terrain(6, 4, "hill")

    # River down the middle (column x=4) with a bridge at y=2,3
    for y in range(6):
        bf.set_terrain(4, y, "water")
    for y in (2, 3):
        bf.set_terrain(4, y, "road")
        bf.tile(4, y).add_object("bridge_plank")

    # Oil barrels + wall near the enemy side
    bf.tile(5, 2).add_object("oil_barrel")
    bf.set_terrain(5, 0, "oil_slick")
    bf.tile(6, 2).add_object("wall_segment")
    bf.tile(2, 0).add_object("boulder")

    return bf


def build_demo(rng: Optional[random.Random] = None,
               world_state: Optional[dict] = None) -> CombatEngine:
    bf = build_battlefield()
    combatants = [
        Combatant("Bran the Guardian", "guardian", "player", 1, 3),
        Combatant("Sella the Ranger", "ranger", "player", 0, 2),
        Combatant("Corwin the Mage", "mage", "player", 0, 4),
        Combatant("Marauder", "brute", "enemy", 7, 2),
        Combatant("Skirmisher", "brute", "enemy", 6, 3),
        Combatant("Crossbowman", "archer", "enemy", 7, 4),
    ]
    return CombatEngine(bf, combatants,
                        context=CombatContext("overworld"),
                        rng=rng or random.Random(2026),
                        world_state=world_state)
