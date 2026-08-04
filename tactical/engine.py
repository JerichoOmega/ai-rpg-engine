"""
Combat Engine
=============

Owns the battlefield, the combatants, and the turn flow (spec: Combat Flow).
It enforces "all combat uses the same tactical systems" and the
return-to-context rule after combat. The environment reacts every round
(Pillar 5) and permanent changes persist to ``world_state`` on end.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Optional, Tuple

from .battlefield import Battlefield
from .entities import Combatant
from . import actions, ai

XY = Tuple[int, int]


@dataclass
class CombatContext:
    """Where combat began, so we can return there afterwards."""
    origin: str          # "overworld" | "location"
    location_id: str = ""


class CombatEngine:
    def __init__(self, battlefield: Battlefield, combatants: List[Combatant],
                 context: Optional[CombatContext] = None,
                 rng: Optional[random.Random] = None, world_state=None):
        self.bf = battlefield
        self.combatants = combatants
        self.context = context or CombatContext("overworld")
        self.rng = rng or random.Random()
        self.world_state = world_state
        self.round = 0
        self.in_combat = False
        self.log: List[str] = []

    # -- lookups -----------------------------------------------------------
    def unit_at(self, xy: XY) -> Optional[Combatant]:
        for unit in self.combatants:
            if unit.alive and unit.pos == xy:
                return unit
        return None

    def living(self, team: str) -> List[Combatant]:
        return [u for u in self.combatants if u.alive and u.team == team]

    def enemies_of(self, unit) -> List[Combatant]:
        return [u for u in self.combatants if u.team != unit.team]

    def allies_of(self, unit) -> List[Combatant]:
        return [u for u in self.combatants if u.team == unit.team]

    # -- lifecycle ---------------------------------------------------------
    def start(self) -> None:
        if self.world_state is not None:
            self.bf.apply_persistent(self.world_state)
        for unit in self.combatants:
            self.bf.tile(unit.x, unit.y).occupant = unit.id
        self.in_combat = True
        self.round = 0
        self.log.append(f"Combat begins on '{self.bf.id}'.")

    def environment_reacts(self) -> None:
        """Pillar 5: the battlefield evolves, then hazards hurt occupants."""
        self.bf.step_environment()
        for unit in self.combatants:
            if unit.alive and "fire" in self.bf.tile(unit.x, unit.y).hazards():
                unit.hp -= 4
                self.log.append(f"{unit.name} takes 4 fire damage.")
                if unit.hp <= 0:
                    self.bf.tile(unit.x, unit.y).occupant = None
                    self.log.append(f"{unit.name} is consumed by the flames.")

    def take_team_turn(self, team: str, controller=None) -> None:
        """Run one team's turn. ``controller`` may drive player units; by
        default every unit uses the shared AI (proving parity)."""
        for unit in self.living(team):
            unit.reset_turn()
            if controller:
                controller(self, unit)
            else:
                ai.take_turn(self, unit)

    def check_victory(self) -> Optional[str]:
        players = self.living("player")
        enemies = self.living("enemy")
        if not enemies:
            return "player"
        if not players:
            return "enemy"
        return None

    def auto_battle(self, max_rounds: int = 30,
                    player_controller=None) -> str:
        """Run a full encounter to conclusion (used by the harness and by
        headless resolution). Returns the winning team."""
        self.start()
        while self.round < max_rounds:
            self.round += 1
            self.log.append(f"--- Round {self.round} ---")
            self.take_team_turn("player", controller=player_controller)
            if self.check_victory():
                break
            self.take_team_turn("enemy")
            if self.check_victory():
                break
            self.environment_reacts()
            if self.check_victory():
                break
        outcome = self.check_victory() or "draw"
        self.end()
        self.log.append(f"Combat ends: {outcome} (round {self.round}).")
        return outcome

    def end(self) -> CombatContext:
        """Persist permanent battlefield changes and leave combat, returning
        the context to resume (overworld or the named location)."""
        if self.world_state is not None:
            self.bf.persist(self.world_state)
        self.in_combat = False
        return self.context
