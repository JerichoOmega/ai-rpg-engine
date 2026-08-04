"""
Tile data model (authoritative source of gameplay truth)
========================================================

Every combat tile is the single source of tactical information (Pillar 3:
Every Tile Matters). Terrain and object definitions are **data** loaded from
``tactical/data/terrain.json`` and ``objects.json`` -- adding a new terrain
type or object is a data change, not code.

A :class:`Tile` composes its terrain with the objects on it to answer every
tactical question the rest of the engine (and the AI, via the same code)
asks: movement cost, cover, elevation, LOS blocking, hazards, interactions,
occupant, visibility, and live environmental state.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

_DATA = os.path.join(os.path.dirname(__file__), "data")

# Cover is stored as a label; COVER_VALUE maps it to a to-hit penalty.
COVER_VALUE = {"none": 0.0, "half": 0.25, "full": 0.45}


def _load(name: str) -> Dict:
    with open(os.path.join(_DATA, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


TERRAIN: Dict[str, Dict] = _load("terrain.json")
OBJECTS: Dict[str, Dict] = _load("objects.json")


def _best_cover(*labels: str) -> str:
    """Return the strongest cover label among the given labels."""
    best = "none"
    for label in labels:
        if COVER_VALUE.get(label, 0) > COVER_VALUE.get(best, 0):
            best = label
    return best


class Tile:
    def __init__(self, x: int, y: int, terrain: str = "plains",
                 objects: Optional[List[str]] = None,
                 elevation: Optional[int] = None):
        self.x = x
        self.y = y
        self.terrain = terrain if terrain in TERRAIN else "plains"
        self.objects: List[str] = list(objects or [])
        # Elevation defaults to the terrain's, but can be overridden per-tile.
        self._elevation_override = elevation
        self.occupant: Optional[str] = None       # combatant id
        self.status_effects: List[str] = []        # e.g. "smoke"
        self.visibility: str = "visible"
        # Live environmental state (burning, timers, destroyed, ...).
        self.env: Dict = {}

    # -- terrain / object helpers ------------------------------------------
    @property
    def terrain_def(self) -> Dict:
        return TERRAIN[self.terrain]

    def object_defs(self) -> List[Dict]:
        return [OBJECTS[o] for o in self.objects if o in OBJECTS]

    @property
    def elevation(self) -> int:
        if self._elevation_override is not None:
            return self._elevation_override
        return int(self.terrain_def.get("elevation", 0))

    # -- authoritative tactical queries ------------------------------------
    def movement_cost(self) -> int:
        cost = int(self.terrain_def.get("movement_cost", 1))
        # Difficult objects on the tile add cost; scorched/destroyed clear it.
        if any(not d.get("passable", True) for d in self.object_defs()):
            return 99  # impassable marker
        return max(1, cost)

    def is_passable(self) -> bool:
        if self.occupant is not None:
            return False
        if any(not d.get("passable", True) for d in self.object_defs()):
            return False
        return self.movement_cost() < 99

    def cover_value(self) -> str:
        labels = [self.terrain_def.get("cover", "none")]
        labels += [d.get("cover", "none") for d in self.object_defs()]
        return _best_cover(*labels)

    def blocks_los(self) -> bool:
        if "smoke" in self.status_effects:
            return True
        if self.terrain_def.get("blocks_los"):
            return True
        return any(d.get("blocks_los") for d in self.object_defs())

    def is_flammable(self) -> bool:
        if self.env.get("burning") or self.env.get("burned"):
            return False
        return bool(self.terrain_def.get("flammable")) or \
            any(d.get("flammable") for d in self.object_defs())

    def hazards(self) -> List[str]:
        result = []
        if self.terrain_def.get("hazard"):
            result.append(self.terrain_def["hazard"])
        if self.env.get("burning"):
            result.append("fire")
        result.extend(self.status_effects)
        return result

    def interactions(self) -> List[str]:
        actions: List[str] = []
        for obj_name in self.objects:
            for action in OBJECTS.get(obj_name, {}).get("interactions", []):
                actions.append(f"{action}:{obj_name}")
        return actions

    def add_object(self, name: str) -> None:
        if name in OBJECTS and name not in self.objects:
            self.objects.append(name)

    def remove_object(self, name: str) -> None:
        if name in self.objects:
            self.objects.remove(name)

    def to_dict(self) -> Dict:
        """Full tactical snapshot -- the data behind tile hover/tooltip."""
        return {
            "pos": (self.x, self.y),
            "terrain": self.terrain,
            "objects": list(self.objects),
            "movement_cost": self.movement_cost(),
            "cover": self.cover_value(),
            "elevation": self.elevation,
            "blocks_los": self.blocks_los(),
            "hazards": self.hazards(),
            "interactions": self.interactions(),
            "status_effects": list(self.status_effects),
            "occupant": self.occupant,
            "visibility": self.visibility,
            "environment": dict(self.env),
        }
