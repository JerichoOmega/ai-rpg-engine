"""
Encounter Groups
================

Reusable enemy compositions defined as data (``tactical/data/encounters.json``).
Building an encounter is a data lookup + placement, so designers assemble
fights without touching code. Positions default to the right-hand edge of the
battlefield (the "enemy side") but can be supplied explicitly.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Tuple

from .enemies import spawn_enemy
from .entities import Combatant

_DATA = os.path.join(os.path.dirname(__file__), "data")

with open(os.path.join(_DATA, "encounters.json"), "r", encoding="utf-8") as _fh:
    ENCOUNTERS: Dict[str, Dict] = json.load(_fh)


def list_encounters() -> List[str]:
    return list(ENCOUNTERS.keys())


def roster(group_id: str) -> List[str]:
    """Flatten a group into an ordered list of enemy ids."""
    group = ENCOUNTERS[group_id]
    ids: List[str] = []
    for member in group["members"]:
        ids.extend([member["enemy"]] * int(member.get("count", 1)))
    return ids


def build_group(group_id: str, positions: Optional[List[Tuple[int, int]]] = None,
                battlefield=None, team: str = "enemy") -> List[Combatant]:
    """Spawn all members of an encounter group.

    ``positions`` overrides placement; otherwise units are auto-placed down
    the right edge of ``battlefield`` (falling back to a simple column)."""
    ids = roster(group_id)

    if positions is None:
        positions = []
        if battlefield is not None:
            x = battlefield.width - 1
            for i in range(len(ids)):
                positions.append((x, i % battlefield.height))
        else:
            positions = [(0, i) for i in range(len(ids))]

    units = []
    for enemy_id, (x, y) in zip(ids, positions):
        units.append(spawn_enemy(enemy_id, x, y, team=team))
    return units
