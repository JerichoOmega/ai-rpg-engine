"""
Living World Reactions (Phase 4)
================================

The quest frameworks already *record* Living-World flags and counters. This
module turns those flags into concrete, reusable world reactions that any
current or future quest gets for free -- with no quest-specific code.

It is entirely **data-driven**: a mapping (``legacy/data/living_world_reactions.json``)
associates each flag with one or more reactions across these systems:

    merchant_inventory | merchant_pricing | npc_schedule | guard_patrol |
    refugee_movement | ambient_dialogue | tavern_rumor |
    settlement_prosperity | road_safety | regional_reputation

Design
------
On every ``living_world_changed`` event we **recompute the whole reaction
state from scratch** by re-applying the reactions for all currently-true
flags. This makes the system:

* idempotent (re-setting a flag never double-applies),
* order-independent,
* save/load safe (recompute on load reproduces the derived state).

Other engine systems query the derived state through the getters below
(e.g. a merchant screen calls :func:`merchant_modifiers`, a tavern calls
:func:`tavern_rumors`). Nothing writes into other managers directly, so this
layer stays decoupled and reusable.
"""

from __future__ import annotations

import json
import os
from collections import defaultdict
from typing import Any, Dict, List

from world_state import world_state
from event_bus import subscribe, emit

_MAPPING_PATH = os.path.join(os.path.dirname(__file__), "..", "data",
                             "living_world_reactions.json")
_mapping: Dict[str, Any] = {}
_subscribed = False


def _load_mapping() -> Dict[str, Any]:
    global _mapping
    if not _mapping:
        with open(os.path.abspath(_MAPPING_PATH), "r", encoding="utf-8") as fh:
            _mapping = json.load(fh)
    return _mapping


def _living_world() -> Dict[str, Any]:
    return world_state.setdefault("legacy", {}).setdefault("living_world", {})


def _reactions_store() -> Dict[str, Any]:
    return world_state.setdefault("legacy", {}).setdefault("world_reactions", {})


# ---------------------------------------------------------------------------
# Recompute
# ---------------------------------------------------------------------------
def recompute(*_event_args, **_event_kwargs) -> Dict[str, Any]:
    """Rebuild the derived reaction state from all currently-true flags.

    Safe to call directly or as an event-bus handler (extra args ignored).
    """
    mapping = _load_mapping()
    flags = _living_world()

    merchant_inventory: Dict[str, List[str]] = defaultdict(list)
    merchant_pricing: Dict[str, float] = defaultdict(float)
    npc_schedule: Dict[str, str] = {}
    guard_patrol: Dict[str, int] = defaultdict(int)
    refugee_movement: List[Dict[str, str]] = []
    ambient_dialogue: Dict[str, List[str]] = defaultdict(list)
    tavern_rumors: List[str] = []
    settlement_prosperity: Dict[str, int] = defaultdict(int)
    road_safety: Dict[str, int] = defaultdict(int)
    regional_reputation: Dict[str, Dict[str, int]] = defaultdict(dict)

    for flag_name, spec in mapping.items():
        value = flags.get(flag_name)
        expected = spec.get("when", True)
        active = bool(value) if expected is True else value == expected
        if not active:
            continue
        for reaction in spec.get("reactions", []):
            system = reaction.get("system")
            if system == "merchant_inventory":
                for item in reaction.get("add", []):
                    if item not in merchant_inventory[reaction["target"]]:
                        merchant_inventory[reaction["target"]].append(item)
            elif system == "merchant_pricing":
                merchant_pricing[reaction["target"]] += float(
                    reaction.get("modifier", 0))
            elif system == "npc_schedule":
                npc_schedule[reaction["target"]] = reaction["schedule"]
            elif system == "guard_patrol":
                guard_patrol[reaction["target"]] = max(
                    guard_patrol[reaction["target"]],
                    int(reaction.get("level", 0)))
            elif system == "refugee_movement":
                move = {"from": reaction.get("from"), "to": reaction.get("to")}
                if move not in refugee_movement:
                    refugee_movement.append(move)
            elif system == "ambient_dialogue":
                line = reaction["line"]
                if line not in ambient_dialogue[reaction["target"]]:
                    ambient_dialogue[reaction["target"]].append(line)
            elif system == "tavern_rumor":
                if reaction["line"] not in tavern_rumors:
                    tavern_rumors.append(reaction["line"])
            elif system == "settlement_prosperity":
                settlement_prosperity[reaction["target"]] += int(
                    reaction.get("delta", 0))
            elif system == "road_safety":
                road_safety[reaction["target"]] += int(
                    reaction.get("delta", 0))
            elif system == "regional_reputation":
                region = regional_reputation[reaction["region"]]
                civ = reaction["civ"]
                region[civ] = region.get(civ, 0) + int(reaction.get("delta", 0))

    store = _reactions_store()
    store.clear()
    store.update({
        "merchant_inventory": dict(merchant_inventory),
        "merchant_pricing": dict(merchant_pricing),
        "npc_schedule": dict(npc_schedule),
        "guard_patrol": dict(guard_patrol),
        "refugee_movement": refugee_movement,
        "ambient_dialogue": dict(ambient_dialogue),
        "tavern_rumors": tavern_rumors,
        "settlement_prosperity": dict(settlement_prosperity),
        "road_safety": dict(road_safety),
        "regional_reputation": {k: dict(v)
                                for k, v in regional_reputation.items()},
    })
    emit("world_reactions_recomputed", systems=list(store.keys()))
    return store


# ---------------------------------------------------------------------------
# Query API (used by merchants, taverns, NPCs, travel, etc.)
# ---------------------------------------------------------------------------
def merchant_inventory_additions(target: str) -> List[str]:
    return _reactions_store().get("merchant_inventory", {}).get(target, [])


def merchant_modifiers(target: str) -> float:
    """Price multiplier delta for a merchant/settlement (e.g. -0.10 = 10% off)."""
    return _reactions_store().get("merchant_pricing", {}).get(target, 0.0)


def npc_schedule(target: str) -> str:
    return _reactions_store().get("npc_schedule", {}).get(target, "default")


def guard_patrol_level(target: str) -> int:
    return _reactions_store().get("guard_patrol", {}).get(target, 0)


def refugee_movements() -> List[Dict[str, str]]:
    return list(_reactions_store().get("refugee_movement", []))


def ambient_dialogue(target: str) -> List[str]:
    return _reactions_store().get("ambient_dialogue", {}).get(target, [])


def tavern_rumors() -> List[str]:
    return list(_reactions_store().get("tavern_rumors", []))


def settlement_prosperity(target: str) -> int:
    return _reactions_store().get("settlement_prosperity", {}).get(target, 0)


def road_safety(target: str) -> int:
    return _reactions_store().get("road_safety", {}).get(target, 0)


def regional_reputation(region: str) -> Dict[str, int]:
    return _reactions_store().get("regional_reputation", {}).get(region, {})


# ---------------------------------------------------------------------------
# Wiring
# ---------------------------------------------------------------------------
def install() -> None:
    """Subscribe to Living-World changes and do an initial recompute.
    Idempotent; called from the registry on import."""
    global _subscribed
    if not _subscribed:
        subscribe("living_world_changed", recompute)
        _subscribed = True
    recompute()


def show_reactions() -> None:
    print("\n=== LIVING WORLD REACTIONS ===")
    store = _reactions_store()
    if not store:
        recompute()
        store = _reactions_store()
    for system, value in store.items():
        if value:
            print(f"  {system}: {value}")
