"""
Reputation Hooks & Civilization Relationship Tracking
=====================================================

Two related, reusable concerns:

1. **Reputation hooks** -- a thin, safe wrapper over the existing
   ``faction_manager`` reputation integers. Quests call
   :func:`adjust_reputation` so faction bookkeeping stays in one place and
   every change is announced on the event bus.

2. **Civilization relationship tracking** -- Legacy Questlines are about
   *civilizations* (Humans, the Stonefang goblins, the Mossroot tribe, the
   Dwarven Kingdom...) and the relationships *between* them, not just the
   player's standing. This tracks a directed relationship matrix so that,
   e.g., brokering peace in "The Debt Comes Due" permanently raises the
   Human<->Stonefang relationship and that fact is available to every
   future quest.

Storage lives under ``world_state["legacy"]["civilizations"]``.
"""

from __future__ import annotations

from typing import Any, Dict, List

from world_state import world_state
from event_bus import emit

# Canon civilizations referenced by the three approved packages. New entries
# may be registered at runtime; nothing here invents lore beyond names that
# already appear in the design documents / world bible.
KNOWN_CIVILIZATIONS: List[str] = [
    "humans",
    "stonefang",   # the Stonefang goblin clan
    "mossroot",    # the Mossroot forest tribe
    "dwarves",     # the Dwarven Kingdom of the Eternal Forge
]

# Standing bands for the player's reputation with a civilization.
STANDING_BANDS = [
    (75, "revered"),
    (25, "trusted"),
    (-24, "neutral"),
    (-74, "distrusted"),
    (-100, "reviled"),
]


def _civ_store() -> Dict[str, Any]:
    legacy = world_state.setdefault("legacy", {})
    return legacy.setdefault("civilizations", {})


def _civ_entry(name: str) -> Dict[str, Any]:
    store = _civ_store()
    if name not in store:
        store[name] = {"standing": 0, "relations": {}}
    return store[name]


# ---------------------------------------------------------------------------
# Faction reputation hook
# ---------------------------------------------------------------------------
def adjust_reputation(faction_name: str, amount: int) -> None:
    """Adjust the player's standing with an engine faction.

    Delegates to ``faction_manager.change_reputation`` when the faction is
    known there, otherwise falls back to the ``world_state`` helper so brand
    new civilization-factions still track cleanly.
    """
    try:
        from faction_manager import change_reputation
        change_reputation(faction_name, amount)
    except Exception:
        from world_state import change_faction_reputation
        change_faction_reputation(faction_name, amount)
    emit("reputation_changed", faction=faction_name, amount=amount)


# ---------------------------------------------------------------------------
# Player <-> civilization standing
# ---------------------------------------------------------------------------
def adjust_standing(civ: str, amount: int) -> int:
    entry = _civ_entry(civ)
    entry["standing"] = max(-100, min(100, entry["standing"] + amount))
    emit("civ_standing_changed", civ=civ, standing=entry["standing"],
         amount=amount)
    print(f"\n[Civilization] Standing with {civ}: {entry['standing']} "
          f"({standing_band(civ)})")
    return entry["standing"]


def get_standing(civ: str) -> int:
    return _civ_entry(civ)["standing"]


def standing_band(civ: str) -> str:
    value = get_standing(civ)
    for threshold, label in STANDING_BANDS:
        if value >= threshold:
            return label
    return "reviled"


# ---------------------------------------------------------------------------
# Civilization <-> civilization relations (directed, symmetric helper)
# ---------------------------------------------------------------------------
def adjust_relationship(civ_a: str, civ_b: str, amount: int) -> int:
    """Adjust the relationship between two civilizations (symmetric).

    Returns the new relationship value. Used by consequence sets, e.g.
    Human<->Stonefang peace after "The Debt Comes Due".
    """
    entry_a = _civ_entry(civ_a)
    entry_b = _civ_entry(civ_b)
    new_value = max(-100, min(
        100, entry_a["relations"].get(civ_b, 0) + amount))
    entry_a["relations"][civ_b] = new_value
    entry_b["relations"][civ_a] = new_value
    emit("civ_relationship_changed", civ_a=civ_a, civ_b=civ_b,
         value=new_value)
    print(f"\n[Civilization] {civ_a} <-> {civ_b} relationship: {new_value}")
    return new_value


def get_relationship(civ_a: str, civ_b: str) -> int:
    return _civ_entry(civ_a)["relations"].get(civ_b, 0)


def show_civilizations() -> None:
    print("\n=== CIVILIZATION RELATIONS ===")
    store = _civ_store()
    if not store:
        print("No civilization relationships recorded yet.")
        return
    for civ in sorted(store):
        entry = store[civ]
        print(f"\n{civ}: standing {entry['standing']} ({standing_band(civ)})")
        for other, value in sorted(entry["relations"].items()):
            print(f"    <-> {other}: {value}")
