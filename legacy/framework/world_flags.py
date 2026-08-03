"""
Living World State Manager
==========================

The Living World pillar: player choices permanently change the world.
Rather than scripting one-off events, quests record *flags* and *counters*
here. NPC dialogue, schedules, merchants, patrols, refugee populations,
travel safety and future quests all read these values, so a single flag
drives many downstream reactions.

Storage
-------
Everything lives under ``world_state["legacy"]["living_world"]`` so it is
saved and loaded automatically with the rest of the game state (see
``world_state.ensure_world_state_defaults``).

This module is deliberately tiny and dependency-light; it is the shared
substrate that :mod:`legacy.framework.consequences`,
:mod:`legacy.framework.reputation`, and every quest write through.
"""

from __future__ import annotations

from typing import Any, Dict

from world_state import world_state
from event_bus import emit


def _living_world() -> Dict[str, Any]:
    """Return the living-world flag store, initialising it lazily so the
    module is safe to import before ``ensure_world_state_defaults`` runs."""
    legacy = world_state.setdefault("legacy", {})
    return legacy.setdefault("living_world", {})


# ---------------------------------------------------------------------------
# Flags (booleans / strings / any JSON-serialisable value)
# ---------------------------------------------------------------------------
def set_flag(name: str, value: Any = True, *, silent: bool = False) -> None:
    """Set a living-world flag and announce the change on the event bus.

    Idempotent by nature -- setting the same value twice is harmless. Other
    systems subscribe to ``living_world_changed`` to react (e.g. a merchant
    manager enabling a new stall when ``talos_town_growing`` becomes True).
    """
    store = _living_world()
    old = store.get(name)
    store[name] = value
    if old != value:
        emit("living_world_changed", flag=name, value=value, previous=old)
        if not silent:
            print(f"\n[Living World] {name} -> {value}")


def get_flag(name: str, default: Any = None) -> Any:
    return _living_world().get(name, default)


def has_flag(name: str) -> bool:
    """True when a flag exists and is truthy."""
    return bool(_living_world().get(name))


def toggle_flag(name: str) -> Any:
    """Flip a boolean flag (developer/debug convenience)."""
    new_value = not bool(_living_world().get(name))
    set_flag(name, new_value)
    return new_value


# ---------------------------------------------------------------------------
# Counters (refugee populations, volunteers, restored infrastructure...)
# ---------------------------------------------------------------------------
def adjust_counter(name: str, amount: int) -> int:
    """Increment/decrement a named counter, clamped at zero, and return it."""
    store = _living_world()
    store[name] = max(0, int(store.get(name, 0)) + amount)
    emit("living_world_changed", flag=name, value=store[name])
    return store[name]


def get_counter(name: str, default: int = 0) -> int:
    return int(_living_world().get(name, default))


# ---------------------------------------------------------------------------
# Introspection (used by dev tools and the save/handoff summary)
# ---------------------------------------------------------------------------
def snapshot() -> Dict[str, Any]:
    """Return a copy of every living-world value for inspection/logging."""
    return dict(_living_world())


def show_living_world() -> None:
    print("\n=== LIVING WORLD STATE ===")
    store = _living_world()
    if not store:
        print("No living-world changes recorded yet.")
        return
    for name in sorted(store):
        print(f"  {name}: {store[name]}")
