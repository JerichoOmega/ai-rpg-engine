"""
Enemy Blueprints (data-driven, with inheritance)
================================================

Every enemy inherits from a base blueprint via ``extends`` (see
``tactical/data/enemies.json``). The Skeleton Warrior is the canonical base
melee enemy and the balancing benchmark; variants (Veteran, Shieldbearer,
Archer, Captain) and other enemies (Goblin Raider, Bandit Swordsman) inherit
and override **only the values that change**.

This keeps the content pipeline consistent: adding an enemy is a value swap,
not a new character definition. Blueprints are resolved by deep-merging the
``extends`` chain, then a :class:`~tactical.entities.Combatant` is built from
the resolved data.
"""

from __future__ import annotations

import copy
import json
import os
from typing import Dict, List, Optional, Tuple

from .entities import Combatant

_DATA = os.path.join(os.path.dirname(__file__), "data")

with open(os.path.join(_DATA, "enemies.json"), "r", encoding="utf-8") as _fh:
    BLUEPRINTS: Dict[str, Dict] = json.load(_fh)

with open(os.path.join(_DATA, "ai_profiles.json"), "r", encoding="utf-8") as _fh:
    AI_PROFILES: Dict[str, Dict] = json.load(_fh)


def _deep_merge(base: Dict, override: Dict) -> Dict:
    """Merge ``override`` onto a copy of ``base`` (nested dicts merge; lists
    and scalars are replaced)."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def resolve(enemy_id: str) -> Dict:
    """Resolve a blueprint by walking and merging its ``extends`` chain."""
    if enemy_id not in BLUEPRINTS:
        raise KeyError(f"Unknown enemy blueprint: {enemy_id!r}")
    node = BLUEPRINTS[enemy_id]
    parent_id = node.get("extends")
    if parent_id:
        resolved = _deep_merge(resolve(parent_id), node)
    else:
        resolved = copy.deepcopy(node)
    resolved.pop("extends", None)
    resolved.pop("abstract", None)
    resolved["id"] = enemy_id

    # Resolve the AI profile reference into a concrete profile dict so the AI
    # (which reads a dict) stays decoupled from how it was authored.
    profile = resolved.get("ai_profile", "aggressive_melee")
    if isinstance(profile, str):
        if profile not in AI_PROFILES:
            import sys
            print(f"[tactical] WARNING: enemy {enemy_id!r} references undefined "
                  f"AI profile {profile!r}; falling back to 'aggressive_melee'.",
                  file=sys.stderr)
            base_profile = AI_PROFILES["aggressive_melee"]
        else:
            base_profile = AI_PROFILES[profile]
        resolved["ai_profile_name"] = profile
        resolved["ai_profile"] = _deep_merge(
            base_profile, resolved.get("ai_overrides", {}))
    return resolved


def list_enemies(include_abstract: bool = False) -> List[str]:
    return [eid for eid, bp in BLUEPRINTS.items()
            if include_abstract or not bp.get("abstract")]


def tags_for(enemy_id: str) -> List[str]:
    """Resolved encounter tags for an enemy (inherits via ``extends``)."""
    return list(resolve(enemy_id).get("tags", []))


def by_tag(tag: str, include_abstract: bool = False) -> List[str]:
    """All spawnable enemy ids carrying ``tag`` — for encounter generation."""
    return [eid for eid in list_enemies(include_abstract)
            if tag in tags_for(eid)]


def all_tags() -> List[str]:
    """Every distinct encounter tag present across the roster (sorted)."""
    seen = set()
    for eid in list_enemies():
        seen.update(tags_for(eid))
    return sorted(seen)



def spawn_enemy(enemy_id: str, x: int, y: int, team: str = "enemy",
                name: Optional[str] = None) -> Combatant:
    """Build a Combatant from a resolved enemy blueprint."""
    bp = resolve(enemy_id)
    if bp.get("abstract"):
        raise ValueError(f"{enemy_id!r} is an abstract base, not spawnable.")
    archetype = bp.get("archetype", enemy_id)
    display = name or bp.get("display_name", enemy_id)
    return Combatant(display, archetype, team, x, y, blueprint=bp)


def spawn_group(spec: List[Tuple[str, int, int]], team: str = "enemy"
                ) -> List[Combatant]:
    """Spawn several enemies from ``(enemy_id, x, y)`` tuples."""
    return [spawn_enemy(eid, x, y, team=team) for eid, x, y in spec]
