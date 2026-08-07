"""
persistence — wire LivingWorld into the existing save architecture.
===================================================================

The game's save systems (``save_manager.py`` / ``state_manager.py``) already
serialize the whole ``world_state`` dict to JSON. So the living world persists
by living under ``world_state["living_world"]`` as a plain, JSON-shaped snapshot
— a clean, additive extension of the WorldState/SaveState contract with **no
second save path** and **no changes to the existing save modules**.

Backward compatibility:
* A save written before this feature simply has no ``living_world`` key;
  :func:`load_from_world_state` returns a fresh, default :class:`LivingWorld`.
* ``world_state.ensure_world_state_defaults()`` backfills a safe default
  ``living_world`` block on load, so every code path sees the full schema.
* Unknown/future fields are ignored on load (see ``LivingWorld.from_state``).

Engine-agnostic: pure data + rules. No file I/O here — it operates on the
in-memory ``world_state`` dict the save layer already reads and writes.
"""

from __future__ import annotations

from typing import Optional

from .world import LivingWorld, SCHEMA_VERSION

WORLD_STATE_KEY = "living_world"


def default_state() -> dict:
    """The safe default ``living_world`` block for a fresh or legacy save."""
    return LivingWorld().to_state()


def load_from_world_state(world_state: dict) -> LivingWorld:
    """Reconstruct the LivingWorld from ``world_state`` (defaults if missing)."""
    data = world_state.get(WORLD_STATE_KEY)
    if not isinstance(data, dict):
        data = {}
    return LivingWorld.from_state(data)


def save_to_world_state(world: LivingWorld, world_state: dict) -> None:
    """Write the LivingWorld snapshot into ``world_state`` for the save layer."""
    world_state[WORLD_STATE_KEY] = world.to_state()


def ensure_defaults(world_state: dict) -> None:
    """Backfill a safe ``living_world`` block (mirrors the world_state guard).

    Idempotent; safe to call after any ``world_state.clear()/update()``.
    """
    lw = world_state.get(WORLD_STATE_KEY)
    if not isinstance(lw, dict):
        lw = world_state[WORLD_STATE_KEY] = {}
    lw.setdefault("version", SCHEMA_VERSION)
    for key, default in (
        ("locations", {}), ("deeds", []), ("events_seen", []),
        ("landmarks_seen", []), ("presence_seen", []),
        ("progression", {}), ("flags", {}),
    ):
        if not isinstance(lw.get(key), type(default)):
            lw[key] = type(default)()
