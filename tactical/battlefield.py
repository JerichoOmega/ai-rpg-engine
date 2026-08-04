"""
Battlefield
===========

The battlefield is a grid of authoritative :class:`~tactical.tiles.Tile` s
plus the shared tactical algorithms every other system (and the AI) calls:

* line of sight (Bresenham + elevation "see over" rule),
* directional cover,
* movement (Dijkstra over per-tile movement cost),
* reachability / threat maps,
* environmental evolution (fire spread, burn-out, ice melt, smoke decay),
* battlefield memory + persistence to ``world_state["tactical"]``.

Pillar 1 (The Battlefield Is a Character) and Pillar 5 (The Battlefield
Evolves) live here. There are **no hidden values** -- every query is
available to the player (via inspection) and the AI alike.
"""

from __future__ import annotations

import heapq
from typing import Dict, List, Optional, Set, Tuple

from .tiles import Tile, COVER_VALUE, TERRAIN

XY = Tuple[int, int]
ORTHO = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Battlefield:
    def __init__(self, width: int, height: int, battlefield_id: str = "arena"):
        self.width = width
        self.height = height
        self.id = battlefield_id
        self.grid: List[List[Tile]] = [
            [Tile(x, y) for x in range(width)] for y in range(height)]
        self.change_log: List[str] = []

    # -- access ------------------------------------------------------------
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def tile(self, x: int, y: int) -> Tile:
        return self.grid[y][x]

    def neighbors(self, x: int, y: int) -> List[XY]:
        return [(x + dx, y + dy) for dx, dy in ORTHO
                if self.in_bounds(x + dx, y + dy)]

    def set_terrain(self, x: int, y: int, terrain: str,
                    elevation: Optional[int] = None) -> None:
        tile = self.tile(x, y)
        tile.terrain = terrain if terrain in TERRAIN else tile.terrain
        if elevation is not None:
            tile._elevation_override = elevation

    # -- line of sight -----------------------------------------------------
    def _line(self, a: XY, b: XY) -> List[XY]:
        (x0, y0), (x1, y1) = a, b
        points: List[XY] = []
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            points.append((x, y))
            if (x, y) == (x1, y1):
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        return points

    def line_of_sight(self, a: XY, b: XY) -> bool:
        """True if ``a`` can see ``b``. A blocker stops LOS unless the
        viewer's elevation is strictly greater than the blocker's (high
        ground sees over cover)."""
        if a == b:
            return True
        viewer_elev = self.tile(*a).elevation
        for point in self._line(a, b)[1:-1]:
            blocker = self.tile(*point)
            if blocker.blocks_los() and blocker.elevation >= viewer_elev:
                return False
        return True

    # -- cover -------------------------------------------------------------
    def directional_cover(self, defender: XY, attacker: XY) -> str:
        """Cover the defender has *from* the attacker: the tile one step from
        the defender toward the attacker provides it (a tree/wall between
        them)."""
        dx = attacker[0] - defender[0]
        dy = attacker[1] - defender[1]
        step = (defender[0] + (1 if dx > 0 else -1 if dx < 0 else 0)
                if abs(dx) >= abs(dy) else defender[0],
                defender[1] + (1 if dy > 0 else -1 if dy < 0 else 0)
                if abs(dy) > abs(dx) else defender[1])
        if not self.in_bounds(*step) or step == defender:
            return "none"
        return self.tile(*step).cover_value()

    def cover_penalty(self, defender: XY, attacker: XY) -> float:
        return COVER_VALUE.get(self.directional_cover(defender, attacker), 0.0)

    # -- movement ----------------------------------------------------------
    def reachable(self, start: XY, ap: int) -> Dict[XY, int]:
        """Dijkstra over movement cost; returns reachable tiles -> cost."""
        dist: Dict[XY, int] = {start: 0}
        heap: List[Tuple[int, XY]] = [(0, start)]
        while heap:
            cost, current = heapq.heappop(heap)
            if cost > dist.get(current, 1 << 30):
                continue
            for nx, ny in self.neighbors(*current):
                tile = self.tile(nx, ny)
                if not tile.is_passable():
                    continue
                step = tile.movement_cost()
                new_cost = cost + step
                if new_cost <= ap and new_cost < dist.get((nx, ny), 1 << 30):
                    dist[(nx, ny)] = new_cost
                    heapq.heappush(heap, (new_cost, (nx, ny)))
        return dist

    def path(self, start: XY, target: XY, ap: int) -> Optional[List[XY]]:
        """Shortest path within ``ap``; returns list of tiles or None."""
        prev: Dict[XY, XY] = {}
        dist: Dict[XY, int] = {start: 0}
        heap: List[Tuple[int, XY]] = [(0, start)]
        while heap:
            cost, current = heapq.heappop(heap)
            if current == target:
                break
            if cost > dist.get(current, 1 << 30):
                continue
            for nx, ny in self.neighbors(*current):
                tile = self.tile(nx, ny)
                if not tile.is_passable() and (nx, ny) != target:
                    continue
                new_cost = cost + tile.movement_cost()
                if new_cost <= ap and new_cost < dist.get((nx, ny), 1 << 30):
                    dist[(nx, ny)] = new_cost
                    prev[(nx, ny)] = current
                    heapq.heappush(heap, (new_cost, (nx, ny)))
        if target not in dist:
            return None
        node, out = target, [target]
        while node != start:
            node = prev[node]
            out.append(node)
        out.reverse()
        return out

    # -- environmental evolution ------------------------------------------
    def ignite(self, x: int, y: int) -> bool:
        tile = self.tile(x, y)
        if not tile.is_flammable():
            return False
        tile.env["burning"] = True
        tile.env["burn_timer"] = tile.env.get("burn_timer", 2)
        self.change_log.append(f"({x},{y}) catches fire")
        return True

    def step_environment(self) -> List[str]:
        """Advance the battlefield one tick (Pillar 5). Deterministic: fire
        spreads to all adjacent flammable tiles, burns out into scorched
        ground (removing cover/LOS), ignites explosives, and melts ice."""
        changes: List[str] = []
        burning = [(x, y) for y in range(self.height) for x in range(self.width)
                   if self.grid[y][x].env.get("burning")]

        for x, y in burning:
            tile = self.tile(x, y)
            # spread to flammable neighbours
            for nx, ny in self.neighbors(x, y):
                ntile = self.tile(nx, ny)
                if ntile.is_flammable() and not ntile.env.get("burning"):
                    ntile.env["burning"] = True
                    ntile.env["burn_timer"] = ntile.env.get("burn_timer", 2)
                    changes.append(f"fire spreads to ({nx},{ny})")
                if ntile.terrain == "ice":
                    self.set_terrain(nx, ny, "water")
                    ntile.env.pop("frozen", None)
                    changes.append(f"ice melts at ({nx},{ny})")
            # explosives detonate immediately
            if any(self.tile(x, y).object_defs()[i].get("explosive")
                   for i in range(len(tile.object_defs()))):
                changes.append(f"explosion at ({x},{y})")
            # burn down
            tile.env["burn_timer"] -= 1
            if tile.env["burn_timer"] <= 0:
                for obj in list(tile.objects):
                    from .tiles import OBJECTS
                    if OBJECTS.get(obj, {}).get("flammable"):
                        tile.remove_object(obj)
                tile.env["burning"] = False
                tile.env["burned"] = True
                if tile.terrain in ("forest", "oil_slick", "grass"):
                    self.set_terrain(x, y, "scorched")
                if "smoke" not in tile.status_effects:
                    tile.status_effects.append("smoke")
                    tile.env["smoke_timer"] = 2
                changes.append(f"({x},{y}) burns out to scorched ground")

        # decay smoke
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                if "smoke" in tile.status_effects and not tile.env.get("burning"):
                    tile.env["smoke_timer"] = tile.env.get("smoke_timer", 1) - 1
                    if tile.env["smoke_timer"] <= 0:
                        tile.status_effects.remove("smoke")
                        changes.append(f"smoke clears at ({x},{y})")

        self.change_log.extend(changes)
        return changes

    def destroy_object(self, x: int, y: int, name: str) -> None:
        tile = self.tile(x, y)
        tile.remove_object(name)
        tile.env["destroyed_" + name] = True
        self.change_log.append(f"{name} destroyed at ({x},{y})")

    # -- persistence -------------------------------------------------------
    def persist(self, world_state: Dict) -> Dict:
        """Write permanent changes (destroyed objects, scorched/altered
        terrain) so they survive after combat ends."""
        record: Dict[str, Dict] = {}
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                permanent = {k: v for k, v in tile.env.items()
                             if k.startswith("destroyed_") or k == "burned"}
                if permanent or tile.terrain == "scorched":
                    record[f"{x},{y}"] = {"terrain": tile.terrain,
                                          "env": permanent,
                                          "objects": list(tile.objects)}
        store = world_state.setdefault("tactical", {}).setdefault(
            "persistent", {})
        store[self.id] = record
        return record

    def apply_persistent(self, world_state: Dict) -> None:
        """Re-apply previously persisted permanent changes on load."""
        record = world_state.get("tactical", {}).get("persistent", {}).get(
            self.id, {})
        for key, data in record.items():
            x, y = (int(v) for v in key.split(","))
            if self.in_bounds(x, y):
                tile = self.tile(x, y)
                tile.terrain = data.get("terrain", tile.terrain)
                tile.objects = list(data.get("objects", tile.objects))
                tile.env.update(data.get("env", {}))
