"""
runtime — live session wiring for the Living World.
====================================================

Bridges the reusable :class:`~tactical.living_world.world.LivingWorld` to the
game's *actual* runtime and save boundaries. It holds the session's single
authoritative living world in memory and keeps it flushed into
``world_state["living_world"]`` at gameplay checkpoints, so the **existing** save
systems (``save_manager`` / ``state_manager``, which already serialize
``world_state``) persist it with no second save path.

Flow::

    load_game()  -> world_state restored -> runtime.hydrate_from_world_state()
    ...play...   -> checkpoint (deed / region state / event / landmark / ...)
                    -> mutate active world -> flush into world_state
    save_game()  -> runtime.sync_into_world_state() -> world_state serialized

Design laws honoured:
* No ``print``/``input``, no file I/O, no engine/UI/Godot coupling. It operates
  only on the in-memory ``world_state`` dict the save layer already reads/writes.
* Serializable state only (``LivingWorld`` round-trips through JSON).
* Single authoritative representation: the active :class:`LivingWorld`, mirrored
  into ``world_state["living_world"]``. Managers keep no parallel copy.

Subscribing to the event bus is **opt-in** via :func:`install_event_hooks` so
importing this module has no hidden global side effects.
"""

from __future__ import annotations

from typing import List, Optional

from world_state import world_state as _global_world_state
from . import persistence
from . import reputation as _rep
from .world import LivingWorld

# Gameplay checkpoints at which the living world should be persisted.
CHECKPOINT_EVENTS: List[str] = [
    "quest_completed",
    "world_event_resolved",
    "region_state_changed",
    "landmark_completed",
    "presence_changed",
    "regional_milestone",
    "game_saved",
]

_active: Optional[LivingWorld] = None
_hooks_installed = False


# -- session world ----------------------------------------------------------
def get_active() -> LivingWorld:
    """The session's authoritative LivingWorld (lazily created if absent)."""
    global _active
    if _active is None:
        _active = LivingWorld()
    return _active


def set_active(world: LivingWorld) -> None:
    global _active
    _active = world


def clear_active() -> None:
    """Drop the session world (used between sessions / in tests)."""
    global _active
    _active = None


def is_active() -> bool:
    return _active is not None


def _ws(world_state: Optional[dict]) -> dict:
    return world_state if world_state is not None else _global_world_state


# -- save-boundary integration ---------------------------------------------
def hydrate_from_world_state(world_state: Optional[dict] = None) -> LivingWorld:
    """Rebuild the active LivingWorld from a (freshly loaded) world_state."""
    world = persistence.load_from_world_state(_ws(world_state))
    set_active(world)
    return world


def sync_into_world_state(world_state: Optional[dict] = None) -> bool:
    """Flush the active LivingWorld into world_state before it is serialized.

    No-op (returns False) when no session world exists, so saves that never
    touched the living world behave exactly as before.
    """
    if _active is None:
        return False
    persistence.save_to_world_state(_active, _ws(world_state))
    return True


def _flush(world_state: Optional[dict]) -> None:
    persistence.save_to_world_state(get_active(), _ws(world_state))


# -- checkpoint API (mutate + persist) --------------------------------------
def apply_overlay(world: LivingWorld, world_state: Optional[dict] = None) -> None:
    """Adopt an overlay's resulting world as the session world and persist it."""
    set_active(world)
    _flush(world_state)


def record_deed(deed: _rep.Deed, world_state: Optional[dict] = None) -> bool:
    added = get_active().record_deed(deed)
    _flush(world_state)
    return added


def set_region_status(location_id: str, status: str, reason: str = "",
                      world_state: Optional[dict] = None) -> bool:
    changed = get_active().set_status(location_id, status, reason)
    _flush(world_state)
    return changed


def resolve_event(event_id: str, world_state: Optional[dict] = None) -> None:
    get_active().mark_event_seen(event_id)
    _flush(world_state)


def complete_landmark(companion: str, location_id: str,
                      world_state: Optional[dict] = None) -> str:
    key = get_active().mark_landmark_seen(companion, location_id)
    _flush(world_state)
    return key


def mark_presence(companion: str, location_id: str,
                  world_state: Optional[dict] = None) -> str:
    key = get_active().mark_presence_seen(companion, location_id)
    _flush(world_state)
    return key


def complete_region(region_id: str, data: dict,
                    world_state: Optional[dict] = None) -> None:
    get_active().set_progression(region_id, data)
    _flush(world_state)


def checkpoint(world_state: Optional[dict] = None) -> bool:
    """Generic checkpoint: flush current living-world state to world_state."""
    return sync_into_world_state(world_state)


# -- optional event-bus wiring ----------------------------------------------
def _on_checkpoint_event(_event_data) -> None:
    sync_into_world_state()


def install_event_hooks() -> bool:
    """Subscribe checkpoint persistence to the event bus (idempotent)."""
    global _hooks_installed
    if _hooks_installed:
        return False
    from event_bus import subscribe
    for name in CHECKPOINT_EVENTS:
        subscribe(name, _on_checkpoint_event)
    _hooks_installed = True
    return True
