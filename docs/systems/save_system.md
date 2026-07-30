# Save System

**Purpose:** Documents both save systems, their scope, file formats, migration strategy, and loading flow.

**Modules:** `save_manager.py`, `state_manager.py`, `world_state.py` (ensure_world_state_defaults)

---

## Overview

Two save systems coexist in the project. They serve different purposes and write to different files.

| System | Module | File | Scope |
|---|---|---|---|
| **Full save** | `save_manager.py` | `savegame.json` | All manager state dicts + world_state |
| **State save** | `state_manager.py` | `save_data.json` | `world_state` only |

Both systems use JSON serialization. Both call `ensure_world_state_defaults()` after loading to handle schema migrations.

---

## Current Implementation

### save_manager.py (Full Save)

Serializes and deserializes the complete game state across all systems.

#### What is saved

| Key | Source |
|---|---|
| `player` | `player.py` Player object fields |
| `inventory` | `world_state["player"]["inventory"]` |
| `equipment` | `equipment_system.equipment` dict |
| `progression` | `progression_manager.progression_state` |
| `skills` | `skill_tree.player_skills` |
| `world_state` | `world_state` dict (full) |
| `active_quests` | `quest_manager.active_quests` |
| `completed_quests` | `quest_manager.completed_quests` |
| `active_world_events` | `world_event_manager.active_world_events` |
| `completed_world_events` | `world_event_manager.completed_world_events` |
| `dungeons` | `dungeon_manager.DUNGEONS` |
| `settlements` | `settlement_manager.SETTLEMENTS` |
| `economy` | `economy_manager.economy_state` |
| `factions` | `faction_manager.FACTIONS` |
| `regions` | `region_manager.REGIONS` |
| `story_state` | `story_manager.story_state` |
| `npc_relationships` | `dialogue_manager.npc_relationships` |
| `social_state` | `relationship_manager.social_state` |
| `active_companions` | `companion_manager.active_companions` |
| `companions` | `companion_manager.COMPANIONS` |
| `dm_state` | `dm_brain.dm_state` |

#### Key Functions

| Function | Description |
|---|---|
| `save_game()` | Serializes all state to `savegame.json` |
| `load_game()` | Deserializes from `savegame.json`; calls migration |
| `autosave()` | Wraps `save_game()` with autosave banner |
| `delete_save()` | Removes `savegame.json` |
| `show_save_summary()` | Prints player HP, inventory count, active quests |
| `validate_save_data(data)` | Checks required keys are present |
| `safe_load_game()` | Load with additional error recovery |
| `export_save(path)` | Copy save to a named export path |

#### Load Flow

```
load_game()
  → open savegame.json
  → json.load()
  → restore player fields (hp, max_hp, attack_bonus, defense, magic_power, evasion)
  → inventory.extend(save_data["inventory"])    # world_state["player"]["inventory"]
  → equipment.update(...)
  → progression_state.update(...)
  → player_skills.update(...)
  → world_state.clear() + world_state.update(save_data["world_state"])
  → ensure_world_state_defaults()               # MIGRATION
  → active_quests / completed_quests extend(...)
  → active_world_events / completed_world_events extend(...)
  → DUNGEONS / SETTLEMENTS / economy_state / FACTIONS / REGIONS update(...)
  → story_state / npc_relationships / social_state update(...)
  → active_companions / COMPANIONS update(...)
  → dm_state.update(save_data.get("dm_state") or save_data.get("director_state", {}))
  → print "GAME LOADED"
```

> **Backward compatibility:** `dm_state` loading tries both `"dm_state"` key (current) and `"director_state"` key (pre-merge legacy) for saves written before the ai_director → dm_brain merge.

---

### state_manager.py (State Save)

A lighter-weight system focused on `world_state` only.

#### What is saved

```json
{
  "version": 1,
  "world_state": { ... }
}
```

#### Key Functions

| Function | Description |
|---|---|
| `save_game()` | Writes version + world_state to `save_data.json`; backs up previous |
| `load_game()` | Loads, version-checks, migrates, validates, restores world_state |
| `autosave()` | Prints autosave banner, calls save_game |
| `migrate_save(data)` | Upgrades old version saves to current schema |
| `validate_world_state(data)` | Checks required sections present |
| `delete_save()` | Removes `save_data.json` |

#### Version Migration

`migrate_save()` handles version upgrades:
- Version 0 → 1: adds missing `world_state` container key.
- Current save version: `SAVE_VERSION = 1`.

#### Validation Issue

`validate_world_state()` checks for an `"npcs"` key that `world_state.py` does not initialize. This will cause validation to fail on fresh-start games loaded through `state_manager`. This is a **known bug** — see `docs/known_issues.md`.

#### Load Flow

```
load_game()
  → open save_data.json
  → json.load()
  → check version
  → migrate_save() if version mismatch
  → validate_world_state()   # may fail on new games (npcs key bug)
  → world_state.clear() + world_state.update(loaded_state)
  → ensure_world_state_defaults()   # MIGRATION
  → print "GAME LOADED" with version
```

---

## Schema Migration: ensure_world_state_defaults()

This function in `world_state.py` is called by both save systems after loading. It backfills any keys missing from an older save file.

### What it initializes if missing

**Top-level flat keys:**
`civil_war`, `cult_rising`, `mages_rebellion`, `dragon_alive`, `world_chaos`, `events`

**Sections (creates entire section if absent, fills missing sub-fields if section exists):**
`time`, `inventory`, `quests`, `companions`, `regions`, `world_conditions`, `story_memory`, `history`, `sessions`, `factions`, `player`

### When to Update This Function

Any time a new key is added to `world_state`, add it to `ensure_world_state_defaults()` with a safe default. This is the save compatibility contract.

---

## Save Files

| File | Written by | Read by | Notes |
|---|---|---|---|
| `savegame.json` | `save_manager.py` | `save_manager.py` | Full save |
| `save_data.json` | `state_manager.py` | `state_manager.py` | State-only save |
| `save_backup.json` | `state_manager.py` | `state_manager.py` | Backup of previous state save |

---

## Entry Points

`main.py` presents three load options to the player:

| Option | Function | Description |
|---|---|---|
| "Continue" | `save_manager.load_game()` | Loads full save |
| "Safe Load" | `save_manager.safe_load_game()` | Load with extra error recovery |
| "New Game" | _(no load)_ | Starts with fresh world_state defaults |

---

## Design Rationale

- **Two systems** coexist because `state_manager` was the original lightweight system and `save_manager` is the full-featured version. They are not redundant — `state_manager` is used internally for quick state snapshots; `save_manager` is the player-facing save.
- **JSON format** — human-readable, debuggable without special tools, works with Python's standard library.
- **Migration on load** — `ensure_world_state_defaults()` runs on every load regardless of save age. This means older saves never crash; they are silently upgraded.

---

## Known Issues

- `validate_world_state()` in `state_manager.py` checks for `world_state["npcs"]` which is never initialized. This causes validation failures on new games.
- `save_manager.py` serializes the full `FACTIONS`, `REGIONS`, `DUNGEONS`, `SETTLEMENTS` dicts — these are large and will grow with content additions.

---

## Future Expansion

- Save slots (multiple named saves).
- Cloud save integration.
- Save file versioning with automated migration for all versions.
- Save file export/import for sharing.

---

## Related Systems

- `world_state.py` — Central state being saved
- `player.py` — Player object serialized separately
- `dm_brain.py` — DM state saved/loaded
- All manager modules — their state dicts are serialized by `save_manager.py`

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation; `director_state` → `dm_state` backward compat noted |
