# Event Bus System

**Purpose:** Documents the publish/subscribe event communication system used for cross-module reactions.

**Module:** `event_bus.py`

---

## Overview

The event bus is the primary mechanism for cross-system communication. Rather than having modules call each other directly, systems emit events and interested modules subscribe to them at module load time. This reduces coupling and makes it easy to add new reactions without modifying the emitting code.

---

## Current Implementation

### Core API

```python
from event_bus import emit, subscribe

# Subscribe to an event (at module level, at module load)
subscribe("event_name", handler_function)

# Emit an event (anywhere)
emit("event_name", key=value, other_key=other_value)
```

### How It Works

1. `subscribe(event_name, handler)` registers `handler` in a dict of `{event_name: [handlers]}`.
2. `emit(event_name, **kwargs)` builds `event_data = kwargs` and calls every registered handler in registration order.
3. Handlers receive a single dict argument (`event_data`).

Subscriptions are registered when a module is first imported. All subscribers for an event must be imported before an event is emitted or they will miss it. In practice, `game_loop.py` imports all managers, so all subscribers are registered before any event fires.

---

## Registered Events

### `enemy_killed`

**Emitted by:** `combat.py` after enemy HP reaches 0.

**Payload:**
```python
emit("enemy_killed", enemy_name="Goblin")
```

**Subscribers:**
| Module | Handler | Effect |
|---|---|---|
| `dm_brain.py` | `on_enemy_killed` | Increments `recent_battles`; calls `change_story_pressure(+5)` |
| `narrative_ai.py` | `on_enemy_killed` | Records narrative beat |
| `quests.py` | (internal) | Increments quest kill counters |

---

### `quest_completed`

**Emitted by:** `quests.py` → `reward_quest()` after quest completion.

**Payload:**
```python
emit(
    "quest_completed",
    quest_name="Cult Hunt",
    quest={
        "description": "...",
        "faction": "kingdom",
        "type": "combat",       # present if defined on quest
        "gold_reward": 150,
        "xp_reward": 100,
        ...
    }
)
```

**Subscribers:**
| Module | Handler | Effect |
|---|---|---|
| `dm_brain.py` | `on_quest_completed` | Increments `recent_story_events`; evaluates story state |
| `faction_manager.py` | `on_quest_completed` | Grants +10 faction rep if `quest["type"] == "faction"` |
| `memory_engine.py` | (internal) | Stores quest completion in memory |

**Backward compatibility:** Emits without the `quest` key are handled gracefully. `faction_manager.on_quest_completed` uses `event_data.get("quest") or {}`.

---

### `faction_hostile`

**Emitted by:** `faction_manager.py` → `evaluate_faction_state()` when reputation falls into hostile range.

**Payload:**
```python
emit("faction_hostile", faction_name="shadow_cult")
```

**Subscribers:**
| Module | Handler | Effect |
|---|---|---|
| `faction_manager.py` | (internal) | Prints "X has become hostile" message |
| `world_event_manager.py` | (subscribed) | May trigger world events (e.g., "Cult Assassins") |

---

### `item_equipped`

**Emitted by:** `equipment_system.py` → `equip_item()`.

**Payload:**
```python
emit("item_equipped", item_name="Iron Sword")
```

**Subscribers:** None confirmed in current codebase beyond the emitter's print call.

---

### `narrative_encounter`

**Emitted by:** Encounter or story systems when a narrative beat occurs.

**Payload:** Varies — typically includes encounter context.

**Subscribers:**
| Module | Effect |
|---|---|
| `dm_brain.py` | Records narrative event count |

---

### `region_crisis`

**Emitted by:** `narrative_ai.py` → `on_region_crisis()`.

**Subscribers:** Regional event reaction handlers.

---

## Handler Rules

1. **Handlers must be defensive.** Use `.get()` on `event_data`, never bracket access.
   ```python
   def on_quest_completed(event_data):
       quest = event_data.get("quest") or {}   # safe
       quest_name = event_data.get("quest_name", "")
   ```

2. **Never emit from inside a handler.** Event cascades (event A triggers handler that emits event B) are not supported and will cause unexpected behavior.

3. **Subscribe at module level, not inside functions.** Subscriptions inside functions only register when that function is called.
   ```python
   # Correct — at bottom of module
   subscribe("enemy_killed", on_enemy_killed)
   
   # Incorrect — only registers if setup() is called
   def setup():
       subscribe("enemy_killed", on_enemy_killed)
   ```

4. **Import order matters.** Modules must be imported before events they subscribe to are emitted. `game_loop.py` imports all managers, so all subscriptions are registered before gameplay begins.

---

## Design Rationale

- **Decoupling:** `combat.py` does not need to know about `dm_brain.py`, `narrative_ai.py`, or `quests.py`. It just emits `"enemy_killed"` and each system reacts independently.
- **Extensibility:** Adding a new reaction to an existing event requires zero changes to the emitting module.
- **Module load subscription:** Simple, no registration framework needed.

---

## Adding New Events

1. Choose a clear `snake_case` event name.
2. Emit at the trigger point: `emit("new_event", relevant_key=value)`.
3. Create handler(s) in the interested module(s).
4. Subscribe at module level: `subscribe("new_event", handler)`.
5. Document in this file.

---

## Known Limitations

- No event priorities — handlers fire in registration (import) order.
- No event cancellation — once emitted, all handlers fire.
- No async support — handlers run synchronously, blocking the caller.
- No wildcard subscriptions.

---

## Future Expansion

- Event middleware for logging/debugging.
- Event history/replay for game recording.
- Priority queue for handler ordering.

---

## Related Systems

- `dm_brain.py` — Primary event consumer for pacing
- `faction_manager.py` — Faction event reactions
- `narrative_ai.py` — Narrative event reactions
- `quests.py` — Emits quest events; handles kill counting
- `combat.py` — Emits enemy_killed
- `equipment_system.py` — Emits item_equipped

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation; `quest_completed` backward-compat handler noted |
