# World State System

**Purpose:** Documents the structure, schema, access patterns, and rules for `world_state` — the central runtime state object of the game.

**Module:** `world_state.py`

---

## Overview

`world_state` is a plain Python dict that serves as the **single source of truth** for all persistent game data. It is imported directly by almost every other module. Its sections are typed dict subclasses that support both attribute-style and bracket-style access while remaining JSON-serializable.

The design choice to keep `world_state` as a plain dict (rather than a class instance) preserves compatibility with `dict.clear()` and `dict.update()` calls used by the save/load system.

---

## Current Implementation

### The Core Object

```python
# world_state.py — module level
world_state = { ... }   # plain dict, initialized at module load
```

All sections are initialized in one block (lines 406–457). Each section value is an instance of a typed dict subclass.

### Typed Section Subclasses

Each section is a dict subclass that adds `_dict_property` attribute proxies:

| Subclass | Key | Description |
|---|---|---|
| `TimeState` | `time` | In-game clock |
| `PlayerState` | `player` | Player stats, class, resources, equipment, inventory |
| `InventoryState` | `inventory` | Legacy items/gold store |
| `QuestState` | `quests` | Active/completed/failed quests and progress |
| `CompanionState` | `companions` | Party members, relationships, loyalty |
| `FactionState` | `factions` | Per-faction reputation values |
| `RegionState` | `regions` | Current region, discovered, faction control |
| `WorldConditions` | `world_conditions` | Chaos level, active disasters |
| `StoryMemory` | `story_memory` | Player choices, story flags |
| `HistoryState` | `history` | Event log, choices, lore |
| `SessionState` | `sessions` | Session count, last summary |

### Top-Level Flat Keys

| Key | Type | Default | Notes |
|---|---|---|---|
| `civil_war` | bool | `False` | Active civil war flag |
| `cult_rising` | bool | `False` | Shadow Cult is ascending |
| `mages_rebellion` | bool | `False` | Mages Guild in revolt |
| `dragon_alive` | bool | `True` | Dragon antagonist status |
| `world_chaos` | int | `0` | Legacy flat key (kept for save compat) |
| `events` | list | `[]` | Active world event names |

> **Important:** `story.py` reads chaos from `world_state["world_conditions"]["world_chaos"]`. The flat `world_state["world_chaos"]` is a legacy migration shim only. Do not use the flat key for new code.

---

## Section Schemas

### `time` — TimeState

| Field | Default | Notes |
|---|---|---|
| `day` | `1` | In-game day counter |
| `hour` | `8` | In-game hour (0–23) |
| `season` | `"spring"` | Current season string |

Updated by `update_world_state()` — increments hour by 1, rolls to next day at 24.

### `player` — PlayerState

| Field | Default | Notes |
|---|---|---|
| `class` | `"Warrior"` | Character class (bracket-only; `class` is reserved in Python) |
| `name` | `"Wanderer"` | Display name |
| `level` | `1` | Current level |
| `xp` | `0` | Current experience points |
| `xp_to_next_level` | `100` | XP threshold for next level |
| `gold` | `0` | Currency (also on Player object in player.py) |
| `hp` | `100` | Current health |
| `max_hp` | `100` | Maximum health |
| `resource_name` | `"Stamina"` | Label for the second resource pool |
| `resource` | `100` | Current second resource |
| `max_resource` | `100` | Maximum second resource |
| `attack_bonus` | `5` | Flat damage addition |
| `defense` | `2` | Flat damage reduction |
| `dodge` | `5` | Dodge chance |
| `weapon_bonus` | `0` | Equipment modifier |
| `equipped_weapon` | `"Rusty Sword"` | Active weapon name |
| `inventory` | `[]` | List of item name strings |

### `inventory` — InventoryState (legacy)

| Field | Default | Notes |
|---|---|---|
| `items` | `[]` | Legacy item list |
| `gold` | `0` | Legacy gold (prefer `player.gold`) |

> **Note:** The canonical inventory is `world_state["player"]["inventory"]`. The `inventory` section is a legacy parallel structure. New code should not use it.

### `quests` — QuestState

| Field | Default | Notes |
|---|---|---|
| `active` | `[]` | Quest names currently in progress |
| `completed` | `[]` | Quest names completed |
| `failed` | `[]` | Quest names failed |
| `progress` | `{}` | Kill counters and partial completion data |

### `companions` — CompanionState

| Field | Default | Notes |
|---|---|---|
| `party` | `[]` | Active companion names |
| `relationships` | `{}` | Per-companion relationship scores |
| `loyalty` | `{}` | Per-companion loyalty scores |

> **Note:** `companions.relationships` and `companions.loyalty` may be unused in current code. Companion data also lives in `companion_manager.py`'s `COMPANIONS` and `active_companions`.

### `factions` — FactionState

A dynamic dict of faction name → reputation integer. Default factions:

| Key | Default |
|---|---|
| `kingdom` | `0` |
| `mages_guild` | `0` |
| `shadow_cult` | `0` |
| `rebels` | `0` |

Reputation range: **-100 to 100** (clamped by `change_faction_reputation()`).

> **Note:** `faction_manager.py`'s `FACTIONS` dict is a separate, richer structure (military_power, economy, influence). The `world_state["factions"]` section holds only reputation integers.

### `regions` — RegionState

| Field | Default | Notes |
|---|---|---|
| `current_region` | `"kingdom_capital"` | Active region key |
| `discovered_regions` | `["kingdom_capital"]` | List of visited region keys |
| `faction_control` | `{}` | Region → controlling faction map |
| `current_location` | `None` | Specific location within the region |

### `world_conditions` — WorldConditions

| Field | Default | Notes |
|---|---|---|
| `world_chaos` | `0` | Canonical chaos level (0–100+) |
| `active_disasters` | `[]` | Current active disaster names |

**This is the correct chaos source.** `story.py` and all new code should read from here.

### `story_memory` — StoryMemory

| Field | Default | Notes |
|---|---|---|
| `major_choices` | `[]` | List of major choice strings |
| `important_flags` | `{}` | Named story flags |

Dynamic flags (added via `remember_choice()`): `joined_shadow_cult`, `spared_cultist`, `executed_cultist`, `dragon_slain`, `mage_killed`, and others added at runtime.

**Access rule:** Always use `.get()` — never hard bracket. The dict may have only some flags set.

### `history` — HistoryState

| Field | Default | Notes |
|---|---|---|
| `major_events` | `[]` | Named major event strings |
| `choices` | `[]` | Player choice records |
| `discovered_lore` | `[]` | Discovered lore strings |

### `sessions` — SessionState

| Field | Default | Notes |
|---|---|---|
| `session_count` | `1` | Number of play sessions |
| `last_session_summary` | `""` | Text summary of previous session |

---

## Helper Functions

| Function | Description |
|---|---|
| `update_world_state()` | Advance clock by 1 hour; roll day at 24 |
| `show_world_state()` | Print day, region, chaos to terminal |
| `activate_world_event(name)` | Idempotently append event name to `events` list |
| `remember_major_event(name)` | Append to `history.major_events` |
| `remember_choice(choice)` | Record in `history.choices` and `story_memory` |
| `discover_lore(lore)` | Record in `history.discovered_lore` and print |
| `discover_region(name)` | Idempotently add to `regions.discovered_regions` |
| `set_current_region(name)` | Update `regions.current_region` |
| `heal_player(amount)` | Increase HP, capped at max_hp |
| `damage_player(amount)` | Subtract defense-reduced damage, clamp HP to 0 |
| `add_gold(amount)` | Increment `player.gold` |
| `remove_gold(amount)` | Decrement `player.gold`, floor at 0 |
| `add_item(name)` | Append to `player.inventory` |
| `remove_item(name)` | Remove first occurrence from `player.inventory` |
| `complete_quest(name)` | Move from `quests.active` to `quests.completed` |
| `fail_quest(name)` | Move from `quests.active` to `quests.failed` |
| `change_faction_reputation(faction, amount)` | Update `factions[faction]`, clamp to [-100, 100] |
| `ensure_world_state_defaults()` | Backfill missing keys after old-save load |
| `world_story_modifier()` | Return dict of story modifiers for narrative generation |

---

## Migration: ensure_world_state_defaults()

After `world_state.clear() + world_state.update(loaded_data)` in either save system, `ensure_world_state_defaults()` must be called immediately. It:

1. Adds any missing top-level flat keys with safe defaults.
2. Adds any missing section keys (creates the full section dict if absent).
3. Fills in missing sub-fields within existing sections.
4. Does **not** overwrite existing values — only fills gaps.

This function is the save schema migration mechanism. When new keys are added to world_state, add their defaults here.

---

## Design Rationale

- **Plain dict at top level** — preserves `clear()`/`update()` compatibility for save/load without custom serialization.
- **Dict subclasses for sections** — allows attribute-style access (`world_state["player"].hp`) for readability while keeping JSON round-trip safety.
- **`class` as bracket-only** — Python's reserved keyword means `player_state.class` is a syntax error; use `world_state["player"]["class"]`.
- **Dynamic story_memory** — flags are added at runtime as needed; no fixed schema required.

---

## Known Issues

- `player.py`'s `Player` object and `world_state["player"]` have overlapping fields (`hp`, `max_hp`, `attack_bonus`, `defense`, `evasion`, `gold`). Combat uses `player.py`; other systems use `world_state["player"]`. These can diverge.
- `state_manager.py`'s `validate_world_state()` checks for an `"npcs"` key that `world_state.py` never initializes. Validation will fail on fresh games.
- The flat `world_chaos` key and `world_conditions.world_chaos` are separate values. Only `world_conditions.world_chaos` is written by `story_manager.py` and read by `story.py`.

---

## Related Systems

- `save_manager.py` — full serialization/deserialization
- `state_manager.py` — lightweight serialization
- `event_bus.py` — events trigger world_state changes
- `faction_manager.py` — uses `world_state["factions"]` for reputation
- `story.py` — reads `world_conditions.world_chaos`, `story_memory`, flat flags
- `consistency_engine.py` — validates world_state integrity

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation created |
