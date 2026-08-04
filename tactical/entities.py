"""
Combatants, class-driven player progression, and data-driven enemy
blueprints.

Movement and actions are separate resources (per the Combat & Enemy specs):

* ``move``  -- movement budget in tiles (spent by moving).
* ``ap``    -- action points (spent by Attack/Skill/Item/Interact).

Player units are built from ``classes.json`` (tactical identity + learnable/
equippable abilities). Enemy units are built from ``enemies.json`` blueprints
(see :mod:`tactical.enemies`) so a new enemy is mostly a value swap.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Tuple

_DATA = os.path.join(os.path.dirname(__file__), "data")


def _load(name: str):
    with open(os.path.join(_DATA, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


CLASSES = _load("classes.json")
ABILITIES = _load("abilities.json")

DEFAULT_ACTION_POINTS = 2
DEFAULT_ACCURACY = 0.85


class Combatant:
    _counter = 0

    def __init__(self, name: str, archetype: str, team: str, x: int, y: int,
                 blueprint: Optional[Dict] = None):
        Combatant._counter += 1
        self.id = f"{team}_{archetype}_{Combatant._counter}"
        self.name = name
        self.cls = archetype          # used for icon + class abilities
        self.team = team              # "player" | "enemy"
        self.x = x
        self.y = y
        self.statuses: List[str] = []
        self.prepare_stance: Optional[str] = None
        self.facing: Optional[str] = None      # set on move/attack (Phase A)
        self.ai_memory: Dict = {}              # short tactical context (Phase 2)

        if blueprint is not None:
            self._init_from_blueprint(blueprint)
        else:
            self._init_from_class(archetype)

        self.hp = self.max_hp
        self.move = self.max_move
        self.ap = self.max_ap

    # -- construction paths ------------------------------------------------
    def _init_from_class(self, cls: str) -> None:
        spec = CLASSES[cls]
        self.max_hp = spec["max_hp"]
        self.armor = spec.get("armor", 0)
        self.max_move = spec["max_ap"]          # movement tiles
        self.max_ap = spec.get("action_points", DEFAULT_ACTION_POINTS)
        self.attack_damage = spec["attack_damage"]
        self.damage_min = spec.get("damage_min", spec["attack_damage"])
        self.damage_max = spec.get("damage_max", spec["attack_damage"])
        self.attack_range = spec["attack_range"]
        self.accuracy = spec.get("accuracy", DEFAULT_ACCURACY)
        self.crit_chance = spec.get("crit_chance", 0.05)
        self.ability_slots = spec.get("ability_slots", 2)
        self.learned: List[str] = list(spec.get("abilities", []))
        self.equipped: List[str] = list(self.learned)[:self.ability_slots]
        self._prepare_reaction = spec.get("prepare", {}).get("reaction", "none")
        self.traits: List[str] = []
        self.immunities: List[str] = []
        self.ai_profile: Dict = {}
        self.loot_table: List = []
        self.threat = "medium"
        self.encounter_weight = 1

    def _init_from_blueprint(self, bp: Dict) -> None:
        stats = bp.get("stats", {})
        atk = bp.get("attack", {})
        self.max_hp = stats.get("health", 30)
        self.armor = stats.get("armor", 0)
        self.max_move = stats.get("movement", 5)
        self.max_ap = stats.get("action_points", DEFAULT_ACTION_POINTS)
        self.damage_min = atk.get("damage_min", atk.get("damage", 6))
        self.damage_max = atk.get("damage_max", atk.get("damage", 8))
        self.attack_damage = (self.damage_min + self.damage_max) // 2
        self.attack_range = atk.get("range", 1)
        self.accuracy = atk.get("accuracy", 0.9)
        self.crit_chance = atk.get("crit_chance", 0.05)
        self.ability_slots = len(bp.get("abilities", []))
        self.learned = list(bp.get("abilities", []))
        self.equipped = list(bp.get("abilities", []))
        self._prepare_reaction = bp.get("prepare", {}).get("reaction", "none")
        self.traits = list(bp.get("traits", []))
        self.immunities = list(bp.get("immunities", []))
        self.ai_profile = dict(bp.get("ai_profile", {}))
        self.loot_table = list(bp.get("loot", []))
        self.threat = bp.get("threat", "low")
        self.encounter_weight = bp.get("encounter_weight", 1)
        self.blueprint_id = bp.get("id")

    # -- state -------------------------------------------------------------
    @property
    def pos(self) -> Tuple[int, int]:
        return (self.x, self.y)

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def reset_turn(self) -> None:
        self.move = self.max_move
        self.ap = self.max_ap
        self.prepare_stance = None

    def prepare_reaction(self) -> str:
        return self._prepare_reaction

    def is_immune(self, effect: str) -> bool:
        return effect in self.immunities


# ---------------------------------------------------------------------------
# Player progression / loadout rules
# ---------------------------------------------------------------------------
class LoadoutLockedError(RuntimeError):
    """Raised when a loadout change is attempted during active combat."""


def learn_ability(unit: Combatant, ability: str) -> None:
    if ability in ABILITIES and ability not in unit.learned:
        unit.learned.append(ability)


def equip_ability(unit: Combatant, ability: str, *, in_combat: bool) -> None:
    if in_combat:
        raise LoadoutLockedError(
            "Combat loadouts can only be changed outside of combat.")
    if ability not in unit.learned:
        raise ValueError(f"{unit.name} has not learned {ability!r}.")
    if len(unit.equipped) >= unit.ability_slots:
        raise ValueError(f"{unit.name} has no free ability slots.")
    if ability not in unit.equipped:
        unit.equipped.append(ability)


def unequip_ability(unit: Combatant, ability: str, *, in_combat: bool) -> None:
    if in_combat:
        raise LoadoutLockedError(
            "Combat loadouts can only be changed outside of combat.")
    if ability in unit.equipped:
        unit.equipped.remove(ability)
