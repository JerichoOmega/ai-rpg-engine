# Architecture

**Purpose:** Describes how the system components of the AI RPG are organized, how they communicate, and how data flows through the game at runtime.

---

## Overview

The project is a **modular Python terminal RPG**. Each game domain has one or more dedicated modules. Cross-system communication is handled primarily through a centralized event bus. A single shared state object (`world_state`) serves as the runtime source of truth for all persistent game data.

There is no framework, ORM, or dependency injection container. Module-level singletons are the primary pattern.

---

## Folder Structure

```
/
├── main.py                    Entry point (CLI start/load menu)
├── game_loop.py               Main game tick and player input loop
├── app.py                     Flask web app (separate, not part of terminal game)
├── preview.py                 Browser preview server
├── world_state.py             Central game state (the single source of truth)
├── event_bus.py               Publish/subscribe event system
│
├── — CORE SYSTEMS —
├── player.py                  Player object singleton (used by combat)
├── combat.py                  Turn-based combat engine
├── bosses.py                  Boss encounter definitions
├── enemy_manager.py           Enemy definitions and selection
├── status_effects.py          Status effect definitions and resolution
├── encounter_manager.py       Encounter generation and management
│
├── — AI LAYER —
├── dm_brain.py                AI director (pacing, pressure, session flow)
├── llm_bridge.py              LLM API bridge (currently mocked)
├── narrative_ai.py            Narrative generation functions
├── story.py                   Story context generation
├── story_manager.py           Story arc state and advancement
├── memory_engine.py           Event memory storage
├── memory.py                  Legacy memory module
├── prompt_manager.py          Prompt templates for LLM
│
├── — RPG SYSTEMS —
├── quests.py                  Quest database and reward logic
├── quest_manager.py           Active quest tracking and generation dispatch
├── quest_generator.py         Procedural quest creation
├── faction_manager.py         Faction data, evolution, event handlers
├── factions.py                Legacy faction definitions
├── economy_manager.py         Economy simulation
├── progression_manager.py     Level-up and XP tracking
├── skill_tree.py              Skill state tracking
├── skills.py                  Skill definitions
├── equipment_system.py        Equipment slots and stat application
├── inventory.py               Inventory UI helpers
├── loot_manager.py            Loot generation (rarity, scaling)
├── loot.py                    Legacy loot module
├── shop.py                    Shop transactions
│
├── — WORLD SYSTEMS —
├── region_manager.py          Region data, evolution, weather, corruption
├── regions.py                 Legacy region definitions
├── travel_manager.py          Inter-region movement
├── location_manager.py        Individual location data
├── settlement_manager.py      Settlement data and rumors
├── dungeon_manager.py         Dungeon state
├── world_map.py               Text map display
├── world_event_manager.py     Global event tracking and generation
├── hub.py                     Central hub location
│
├── — SOCIAL SYSTEMS —
├── npc_manager.py             NPC definitions and interaction
├── companion_manager.py       Party companions (recruit, combat, banter)
├── dialogue_manager.py        NPC dialogue, rumors, relationships
├── dialogue_ai.py             AI-powered dialogue wrapper
├── relationship_manager.py    Social state and decay
│
├── — INFRASTRUCTURE —
├── save_manager.py            Full game save/load (all state)
├── state_manager.py           Lightweight save/load (world_state only)
├── session_manager.py         Session tracking
├── campaign_manager.py        Campaign act progression
├── consistency_engine.py      State validation and error reporting
├── event_bus.py               Pub/sub event system
├── utils.py                   Utility functions
│
├── — DATA —
├── data/balance.py            Numeric balance constants
│
├── — LEGACY / ARCHIVE —
├── main_backup_v1.py          Legacy main entry point
├── archive/legacy/            Archived deprecated modules
│
├── — ASSETS —
├── attached_assets/           Uploaded reference files
├── save_data.json             Primary save file (state_manager.py)
├── savegame.json              Full save file (save_manager.py)
│
└── docs/                      This documentation directory
```

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                             │
│                    (CLI entry point)                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │  game_loop.py  │◄──── all manager modules
                    │  (tick + menu) │
                    └───────┬────────┘
                            │
          ┌─────────────────┼─────────────────────┐
          │                 │                     │
   ┌──────▼──────┐   ┌──────▼──────┐   ┌─────────▼────────┐
   │  combat.py  │   │  quests /   │   │ world_event_mgr  │
   │  (battles)  │   │  quest_mgr  │   │ faction_manager  │
   └──────┬──────┘   └──────┬──────┘   │ economy_manager  │
          │                 │          │ relationship_mgr  │
          └────────┬────────┘          └─────────┬────────┘
                   │                             │
           ┌───────▼───────────────────────────▼────────┐
           │                event_bus.py                 │
           │           (publish / subscribe)             │
           └───────┬──────────────────┬─────────────────┘
                   │                  │
          ┌────────▼────────┐ ┌───────▼────────┐
          │  dm_brain.py    │ │ faction_manager │
          │  (pacing)       │ │  narrative_ai   │
          └────────┬────────┘ └───────┬─────────┘
                   │                  │
           ┌───────▼──────────────────▼────────────────┐
           │               world_state.py               │
           │       (single source of truth)             │
           └───────────────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  save_manager.py    │
                    │  state_manager.py   │
                    │  (persistence)      │
                    └─────────────────────┘
```

---

## Data Flow

### New Game Startup
```
main.py → start_new_game()
  → game_loop.run_game()
       → world_state initialized with defaults (world_state.py module load)
       → ensure_world_state_defaults() not needed (fresh state)
       → show_main_menu() → player input → game actions
```

### Load Game
```
main.py → continue_game() → save_manager.load_game()
  → JSON deserialized
  → world_state.clear() + world_state.update(loaded_data)
  → ensure_world_state_defaults()   # backfill missing keys from old saves
  → all manager state dicts restored
  → game_loop.run_game()
```

### Explore (Combat path, most common)
```
game_loop.explore()
  → combat.quick_encounter()
       → enemy_manager.get_random_enemy()
       → combat loop (player turn → enemy turn → status resolve)
       → event_bus.emit("enemy_killed", enemy_name=...)
            → dm_brain.on_enemy_killed()   # +pressure
            → narrative_ai.on_enemy_killed()
            → quests handler (kill counter update)
       → loot_manager.generate_loot()
       → progression_manager.check_level_up()
  → combat.random_boss_encounter()   # 10% chance
  → game_loop.process_game_tick()    # advance world
```

### Game Tick
```
game_loop.process_game_tick()
  → world_event_manager.update_world_events()
  → faction_manager.evolve_factions()
  → economy_manager.evolve_economy()
  → relationship_manager.decay_relationships()
  → dm_brain.update_dm_brain()
  → dm_brain.evaluate_session_flow()
  → [probabilistic] generate_social_event()
  → [probabilistic] dialogue_manager.generate_rumor()
  → [probabilistic] companion_manager.random_companion_banter()
  → [probabilistic] world_event_manager.generate_random_world_event()
  → [every 5 ticks] save_manager.autosave()
```

---

## Central State: world_state

`world_state` is a plain Python dict defined at module load in `world_state.py`. It is imported directly by nearly every other module. Its sections are dict subclasses that expose both attribute-style and bracket-style access.

**Sections:**

| Section | Key | Description |
|---|---|---|
| Time | `time` | Day, hour, season |
| Player | `player` | Stats, class, resources, gold, inventory |
| Inventory | `inventory` | Items list, gold (legacy parallel) |
| Quests | `quests` | Active, completed, failed, progress |
| Companions | `companions` | Party, relationships, loyalty |
| Factions | `factions` | Reputation values per faction |
| Regions | `regions` | Current region, discovered, faction control |
| World Conditions | `world_conditions` | Chaos level, active disasters |
| Story Memory | `story_memory` | Major choices, story flags |
| History | `history` | Major events, choices, lore |
| Sessions | `sessions` | Session count, last summary |

**Top-level flat keys:** `civil_war`, `cult_rising`, `mages_rebellion`, `dragon_alive`, `world_chaos`, `events`

---

## Communication Patterns

| Pattern | When to use |
|---|---|
| Direct import + function call | Within the same domain (combat calling enemy_manager) |
| Event bus emit + subscribe | Cross-domain reactions (combat → dm_brain, quests → factions) |
| world_state read | Reading game data from any module |
| world_state write via helpers | Writing game data (use `add_gold`, `heal_player`, etc.) |

**Anti-patterns to avoid:**
- Importing a manager into another manager for a single function that should be an event reaction
- Storing player/faction/quest data in module-level dicts when it belongs in world_state
- Calling `llm_bridge` functions anywhere except narrative/AI modules

---

## Secondary Application: app.py

`app.py` is a Flask web application that exists in the same repository. It is **not** connected to the terminal game's state. It runs on its own port, has its own data models, and represents a separate interface prototype. It should not be modified as part of terminal game development unless that integration is explicitly planned.

---

## Dependencies

**Runtime (Python standard library only):**
- `json` — save file serialization
- `random` — combat, encounter, narrative randomness
- `os` — file path operations

**Optional / flask app:**
- `flask` — web server for `app.py`

No external packages are required to run the terminal game. See `docs/dependencies.md` for the complete list.

---

## Performance Considerations

- All operations are synchronous. No threading or async is used.
- World state is held entirely in memory; no database queries.
- Save/load involves full JSON serialization of all manager state dicts — acceptable for the current scale.
- The event bus uses simple list iteration over subscribers; no performance concern at current event volume.

---

## Related Documents

- `docs/GAME_BIBLE.md` — Game design reference
- `docs/systems/world_state.md` — World state schema detail
- `docs/systems/event_bus.md` — Event bus reference
- `docs/systems/save_system.md` — Save/load system detail
- `docs/coding_standards.md` — Code style guide
- `docs/known_issues.md` — Technical debt and open bugs

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation created from codebase analysis |
