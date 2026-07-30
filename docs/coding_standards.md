# Coding Standards

**Purpose:** Describes the code style, naming conventions, structural patterns, and rules that all new code in this project must follow.

**Rule:** New code must match existing code style. Do not introduce new style patterns without documenting the decision.

---

## Overview

The codebase has a distinctive, highly line-broken Python style. Every new contribution must match this style. Deviations break visual consistency and make diffs harder to read.

---

## Code Formatting Style

### Line Breaking
The codebase uses **maximum vertical expansion**. Arguments, conditions, and subscripts are placed on separate lines, not packed horizontally.

**Correct (matches project style):**
```python
world_state[
    "factions"
][faction_name] += amount

if world_state[
    "world_conditions"
]["world_chaos"] >= 60:

    locations.append(

        "A shattered landscape consumed by darkness."
    )
```

**Incorrect (do not use):**
```python
world_state["factions"][faction_name] += amount
if world_state["world_conditions"]["world_chaos"] >= 60:
    locations.append("A shattered landscape consumed by darkness.")
```

### Function Arguments
Multi-argument function calls place each argument on its own line:

```python
change_faction_reputation(

    quest_data[
        "faction"
    ],

    quest_data[
        "reputation_reward"
    ]
)
```

### Blank Lines Between Statements
Blank lines are used liberally between logical statements, even within functions. This is intentional.

```python
quest_state[
    "completed"
] = True

if (
    quest_name
    in
    world_state[
        "quests"
    ]["active"]
):

    world_state[
        "quests"
    ]["active"].remove(
        quest_name
    )

complete_quest(
    quest_name
)
```

---

## Section Headers

Every logical block within a file uses a standard three-line section header:

```python
# =========================
# SECTION NAME
# =========================
```

This applies to:
- Function groups
- Data structure definitions
- Configuration constants
- Event subscriptions

---

## Module Structure

Modules follow this ordering convention:

```python
# Standard library imports

# Third-party imports (if any)

# Local imports

# =========================
# CONSTANTS / CONFIG
# =========================

CONSTANT = value

# =========================
# STATE / DATA STRUCTURES
# =========================

module_state = { ... }

# =========================
# FUNCTION GROUP NAME
# =========================

def function_name():
    ...

# =========================
# EVENT SUBSCRIPTIONS
# =========================

subscribe("event_name", handler_function)
```

---

## Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| Module-level state dict | `snake_case` | `dm_state`, `economy_state` |
| Functions | `snake_case` | `change_story_pressure()` |
| Constants | `UPPER_SNAKE` | `SAVE_FILE`, `FACTIONS` |
| Classes | `PascalCase` | `Player`, `TimeState` |
| Event names | `snake_case` string | `"enemy_killed"`, `"quest_completed"` |
| World state keys | `snake_case` string | `"world_chaos"`, `"current_region"` |

---

## Module-Level State Pattern

State that persists across function calls lives in a **module-level dict** (or list). It is not passed as arguments. Consumers import the dict directly.

```python
# In dm_brain.py
dm_state = {
    "story_pressure": 25,
    "current_focus": "exploration",
    ...
}

# In another module
from dm_brain import dm_state
print(dm_state["story_pressure"])
```

This is a deliberate design choice. Do not convert module-level state to class instances, dataclasses, or argument-passing patterns without explicit authorization.

---

## World State Access

### Reading — always use bracket notation
```python
# Correct
value = world_state["player"]["hp"]
chaos = world_state["world_conditions"]["world_chaos"]

# Incorrect (don't use attribute style on world_state itself)
value = world_state.player.hp  # world_state is a plain dict
```

### Reading from story_memory / factions in generate_story context
Use `.get()` with a safe default — these dicts may be partial:

```python
# Correct
if story_memory.get("joined_shadow_cult"):
    ...
if factions.get("kingdom", 0) >= 30:
    ...

# Incorrect — crashes on missing keys
if story_memory["joined_shadow_cult"]:
    ...
```

### Writing — use world_state helper functions where available
```python
# Preferred — uses the helper
from world_state import add_gold, heal_player, add_item
add_gold(100)
heal_player(50)
add_item("Iron Sword")

# Acceptable — direct write for fields without a helper
world_state["player"]["xp"] += 50
world_state["quests"]["active"].append("New Quest")
```

---

## Event Bus Pattern

### Emitting
```python
from event_bus import emit

emit(
    "quest_completed",
    quest_name=quest_name,
    quest=quest_data
)
```

### Subscribing (at module level, after function definitions)
```python
from event_bus import subscribe

def on_quest_completed(event_data):
    quest = event_data.get("quest") or {}
    ...

subscribe(
    "quest_completed",
    on_quest_completed
)
```

**Rules:**
- Subscribe at module level, not inside functions.
- Handlers receive a single `event_data` dict.
- Handlers must be defensive: use `.get()` on event_data, not bracket access.
- Never emit an event from inside an event handler (no event cascades).

---

## Print Output Conventions

Section banners use `===`:
```python
print(
    "\n=== SECTION TITLE ==="
)
```

Normal output uses a leading newline:
```python
print(
    "\nSomething happened."
)
```

Multi-field display prints field + value on separate calls:
```python
print(
    "Player HP:",
    player.hp
)
```

---

## Error Handling

- Do not swallow exceptions silently.
- Print descriptive error messages before returning/exiting.
- Use `try/except` around I/O operations (file read/write) specifically.
- Do not use exceptions for control flow.

```python
# Correct pattern for file I/O
try:
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("\nNo save file found.")
    return
except Exception as error:
    print("\nLoad failed:")
    print(error)
    return
```

---

## Import Organization

```python
# Standard library first
import json
import random
import os

# Local imports — from specific, not wildcard
from world_state import (
    world_state,
    add_gold,
    heal_player
)

from event_bus import (
    subscribe,
    emit
)
```

- Never use `from module import *`.
- Always import explicitly named symbols.
- Group related imports from the same module together.

---

## What Not to Do

| ❌ Don't | ✅ Do instead |
|---|---|
| `from inventory import inventory` | `world_state["player"]["inventory"]` |
| `from encounter_generator import ...` | `from encounter_manager import ...` |
| Add DM Brain logic to llm_bridge.py | Keep DM logic in dm_brain.py only |
| Add LLM calls outside llm_bridge.py | Route all LLM calls through llm_bridge.py |
| Hard-key story_memory["key"] | `story_memory.get("key", False)` |
| Duplicate world_state fields in module state | Use world_state for the canonical value |
| Pack code horizontally | Use vertical multi-line format |
| Use `update_economy()` | `evolve_economy()` (actual function name) |
| Use `show_settlements()` | `show_all_settlements()` (actual function name) |

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial standards document created from codebase analysis |
