---
name: Integration pass fixes
description: Broken imports, schema mismatches, and dead-code issues found and fixed in the Task 3 codebase integration pass.
---

## Fixed issues (by file)

### travel_manager.py
`encounter_generator` module never existed — fixed to `encounter_manager`.

### llm_bridge.py
Contained a full duplicate of dm_brain.py (private `dm_state`, `change_story_pressure`,
`evaluate_story_state`, `update_dm_brain`, `on_enemy_killed`, `on_world_collapse`).
Caused two independent DM states. Rewrote to mock-LLM bridge only:
`ai_narrate`, `ai_generate_quest`, `ai_combat_narration`, `ai_dialogue`.

### equipment_system.py, save_manager.py, loot_manager.py
All imported `inventory` from `inventory.py` — that module only exports functions,
not a module-level list. Canonical inventory is `world_state["player"]["inventory"]`.
- `equipment_system.py`: replaced with `world_state["player"]["inventory"]` references.
- `save_manager.py`: removed broken import; save/load + summary use world_state path.
- `loot_manager.py`: `add_item` was imported from `inventory` — moved to `world_state`.

### game_loop.py
- `update_economy` → `evolve_economy` (economy_manager.py's actual function name).
- `show_settlements` → `show_all_settlements` aliased from settlement_manager.
- Removed dead import `world_social_reaction` (from relationship_manager).

### region_manager.py
- Removed dead import `discover_lore`.
- Added missing `show_regions()` wrapper (game_loop imported it but it didn't exist).

### npc_manager.py
Removed unused `world_state` object from import; kept `remember_major_event`.

### quests.py
- Removed unused `fail_quest` import.
- Updated `quest_completed` emit to include `quest=quest_data` dict so
  `faction_manager.on_quest_completed` can access `quest.get("type")` and `quest.get("faction")`.

### faction_manager.py — on_quest_completed
Old handler crashed if `event_data.get("quest")` was None.
Rewritten to default `quest = event_data.get("quest") or {}` so old-style emits
(quest_name only, no quest dict) are handled without error.

### story.py
- Three `world_state["world_chaos"]` direct reads fixed to
  `world_state["world_conditions"]["world_chaos"]` — canonical location written by story_manager.
- Five `story_memory["key"]` hard-dict lookups → `.get("key")` to tolerate partial dicts.
- Three `factions["key"]` hard-dict lookups → `.get("key", 0)` to tolerate partial faction dicts.

### story_manager.py
**Why:** `story.py` reads `world_state["world_conditions"]["world_chaos"]`;
`story_manager.py` already writes there. The old flat `world_state["world_chaos"]` is kept
as a migration shim but `story.py` no longer reads it.

### world_state.py
Added `ensure_world_state_defaults()` — call after any `world_state.clear() + update()`
to backfill missing keys (all 11 typed sections + 5 flat flags) for old-save compatibility.

### save_manager.py + state_manager.py
Both call `ensure_world_state_defaults()` immediately after `world_state.clear() + update()`
on load. Import added to both files.

## Patterns / warnings for future work

**Why:** `inventory.py` is a UI helper module (show/give/take/use). It never owned the
inventory list; that lives in `world_state["player"]["inventory"]`. Any new code needing
the raw inventory list should reference `world_state["player"]["inventory"]` directly.

**Why:** All event-bus handlers (subscribe calls) only register when their module is
imported. In tests, always import the relevant manager before emitting events or handlers
won't fire.

**Why:** `generate_story(enemies, factions, story_memory)` — `enemies` must be a dict
(keys = enemy names), not a list. `factions` and `story_memory` can be empty dicts safely.
