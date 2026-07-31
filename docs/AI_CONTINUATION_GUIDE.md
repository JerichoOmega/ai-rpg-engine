# AI Continuation Guide

> This document is written specifically for AI assistants that will work on this project in future sessions. Read it before making any changes. Treat it as the project's single source of truth for intent and conventions.

---

## How to Understand This Project Quickly

### 1. Read These Files First

> **Before any of the below: open [`AI_START_HERE.md`](../AI_START_HERE.md)** (project root).  
> It is the official session entry point with startup checklist, development rules, and shutdown procedure.

In order of importance after `AI_START_HERE.md`:

| File | Why |
|---|---|
| `docs/handoffs/<latest date>.md` | What happened last time, warnings, and recommended next task |
| `PROJECT_CONSTITUTION.md` | Permanent governance — principles, rules, and decision process. Read before any major change. |
| `PROJECT_STATE.md` | Current project health — completion %, bugs, priorities. Always check first. |
| `PROJECT_MEMORY.md` | Full project quick-start — architecture, rules, common mistakes, file map |
| `docs/GAME_BIBLE.md` | What the game is, every confirmed mechanic |
| `docs/CAMPAIGN_DESIGN.md` | Canonical campaign design philosophy — Handcrafted First, DM role, replayability framework |
| `docs/COMBAT_SYSTEM.md` | Canonical combat design — grid, AP economy, facing, downed/death, party rules |
| `docs/world/WORLD_BIBLE.md` | Canonical regions, travel encounters, encounter philosophy, intelligent factions, goblin tribes, vampires, player choice philosophy |
| `docs/world/RACES.md` | Six playable races; race design philosophy; non-playable intelligent races |
| `docs/world/vampire_houses.md` | Three vampire houses: Vetharis (political), Drakmor (military), Soleth (knowledge) |
| `docs/world/religions.md` | Four major religions: Solari Covenant, The Old Ways, Ancestors' Path, Veiled Order; cults vs. legitimate religion; religious orders and reputation |
| `docs/world/goblin_tribes.md` | Three tribes: Stonefang (Warchief Grakkor), Mossroot (Elder Vess), Ashfire (Warchief Skarra); leadership, territory, traditions, inter-tribe relationships |
| `docs/systems/dynamic_story_arcs.md` | Dynamic Story Arc framework; The Fractured Circle (first confirmed arc); campaign-exclusive enemies; companion stakes per arc |
| `docs/HERO_BIBLE.md` | Companion design philosophy — Core Wound system, design requirements, confirmed wounds |
| `docs/CHARACTER_DESIGN_GUIDE.md` | How to design a new companion; checklist; mechanics-from-character principle |
| `docs/heroes/TALOS.md` | Full Hero Bible — Talos |
| `docs/heroes/ELEANOR.md` | Full Hero Bible — Eleanor |
| `docs/heroes/RAGASH.md` | Full Hero Bible — Ragash |
| `docs/heroes/RONAN.md` | Full Hero Bible — Ronan |
| `docs/heroes/STEVEN.md` | Full Hero Bible — Steven |
| `docs/architecture.md` | How modules connect, data flow |
| `docs/systems/world_state.md` | The central state object — everything reads from it |
| `docs/coding_standards.md` | How code is written here |
| `docs/known_issues.md` | What is broken / tech debt — do not accidentally fix these in unrelated PRs |
| `DESIGN_DECISIONS.md` | Why major decisions were made — read before any refactor |
| `world_state.py` | The actual central state implementation |
| `event_bus.py` | How systems communicate |
| `dm_brain.py` | The AI pacing system |
| `game_loop.py` | The main game tick and player interaction loop |

### 2. Understand the Module Ownership Model
Each `.py` file owns a specific domain. Before changing any file, check whether the function you are looking for already exists in that file's domain module:

| Domain | Module |
|---|---|
| Central game state | `world_state.py` |
| Save / load (full) | `save_manager.py` |
| Save / load (state only) | `state_manager.py` |
| Combat engine | `combat.py` |
| Enemies | `enemy_manager.py` |
| Bosses | `bosses.py` |
| Player object (combat-facing) | `player.py` |
| AI pacing / DM | `dm_brain.py` |
| LLM API calls | `llm_bridge.py` |
| Narrative generation | `narrative_ai.py` |
| Story context | `story.py` |
| Story arc tracking | `story_manager.py` |
| Memory | `memory_engine.py` |
| Quests (database + reward) | `quests.py` |
| Active quest tracking | `quest_manager.py` |
| Quest generation | `quest_generator.py` |
| Factions (data + evolution) | `faction_manager.py` |
| Economy | `economy_manager.py` |
| Inventory UI helpers | `inventory.py` |
| Equipment | `equipment_system.py` |
| Loot | `loot_manager.py` |
| Shop | `shop.py` |
| Progression / levelling | `progression_manager.py` |
| Skills | `skill_tree.py` |
| Regions | `region_manager.py` |
| Travel | `travel_manager.py` |
| Locations | `location_manager.py` |
| Settlements | `settlement_manager.py` |
| Dungeons | `dungeon_manager.py` |
| NPCs | `npc_manager.py` |
| Companions | `companion_manager.py` |
| Dialogue | `dialogue_manager.py` |
| Relationships | `relationship_manager.py` |
| Event pub/sub | `event_bus.py` |
| World events | `world_event_manager.py` |
| Consistency validation | `consistency_engine.py` |
| Session tracking | `session_manager.py` |
| Campaigns | `campaign_manager.py` |
| Utility functions | `utils.py` |

### 3. Know the Event Bus
Systems communicate through `event_bus.py`. Before adding a direct cross-module function call, check if an event already covers the use case.

Key events currently in use:
- `enemy_killed` — fired after combat; data: `enemy_name`
- `quest_completed` — fired after reward_quest; data: `quest_name`, `quest` (dict)
- `faction_hostile` — fired when faction rep drops into hostile range
- `item_equipped` — fired by equipment_system
- `narrative_encounter` — fired for story-beat encounters
- `region_crisis` — fired by narrative_ai when a region event occurs

To subscribe: `subscribe("event_name", handler_function)` at module load.  
To emit: `emit("event_name", key=value, key2=value2)`.  
Handler receives a single `event_data` dict.

---

## How to Preserve Existing Architecture

### The Central State Rule
**`world_state.py` is the single source of truth for runtime game state.** Do not create new module-level dicts that store player stats, quest state, faction reputation, or world conditions. Add new fields to the appropriate section of `world_state` instead.

The sections are: `time`, `player`, `inventory`, `quests`, `companions`, `factions`, `regions`, `world_conditions`, `story_memory`, `history`, `sessions`.

Top-level flat flags: `civil_war`, `cult_rising`, `mages_rebellion`, `dragon_alive`, `world_chaos` (kept for legacy compat; prefer `world_conditions.world_chaos`).

### The Save Compatibility Rule
If you add new keys to `world_state`, also add them to `ensure_world_state_defaults()` in `world_state.py`. This function is called on save load to backfill missing keys from old save files. Failing to do this breaks save compatibility.

### The LLM Bridge Rule
Never call an LLM API directly from a game system module. All LLM interaction goes through `llm_bridge.py`. This keeps the game functional with no external dependencies and provides a single swap point.

### The Event Bus Rule
Cross-module reactions (e.g., "when an enemy dies, record it in DM Brain AND give faction rep AND update story memory") should be implemented as event bus subscribers, not as a chain of function calls in `combat.py`. Each module subscribes to the events it cares about.

---

## How to Maintain Coding Standards

See `docs/coding_standards.md` for the full style guide. Critical points:

1. **Multiline format** — The codebase uses heavily line-broken Python (each bracket argument on its own line, aligned). New code must match this style.
2. **Section headers** — Each logical block uses `# =========================\n# SECTION NAME\n# =========================`.
3. **Module-level state** — State dicts are defined at module level and imported by consumers, not passed as arguments.
4. **No module does its own UI** — All print() output is acceptable at any layer; there is no strict MVC separation. Match the existing pattern.
5. **No silent failures** — Errors should print a message. Do not swallow exceptions without feedback.

---

## How to Avoid Breaking Existing Systems

### Before Adding Any Import
Check whether the module you're importing from actually exports what you need. Use `grep -n "^def " filename.py` to list exports. Key historical mistakes that were fixed:
- `inventory.py` only exports functions, not a list called `inventory` — use `world_state["player"]["inventory"]`
- `add_item` is in `world_state.py`, not `inventory.py`
- `encounter_manager.py` is the correct module, not `encounter_generator` (doesn't exist)

### Before Adding Cross-Module Function Calls
Check if an event bus subscription would be cleaner. Direct calls create tight coupling.

### Before Changing world_state Schema
1. Add new keys with defaults inside `ensure_world_state_defaults()`.
2. Update `state_manager.py`'s `validate_world_state()` if you're adding required sections.
3. Check `save_manager.py` to see if the new field needs explicit save/load handling.

### Before Touching story.py
- `generate_story()` expects `enemies` as a **dict** (keys = enemy name strings), `factions` as a dict, and `story_memory` as a dict.
- Access `story_memory` keys with `.get()` — never hard bracket access.
- Access `factions` keys with `.get(key, 0)` — the dict may be partial.
- Read world chaos from `world_state["world_conditions"]["world_chaos"]`, not the flat `world_state["world_chaos"]`.

### Before Touching dm_brain.py
- This is the only AI pacing module. There is no separate `ai_director.py` (it was merged here and archived).
- Do not add dm_state logic anywhere else.

### Before Touching llm_bridge.py
- This file is intentionally a mock. Do not add game logic here.
- The four exported functions are: `ai_narrate`, `ai_generate_quest`, `ai_combat_narration`, `ai_dialogue`.

---

## How to Document Future Work

### For new confirmed features (being implemented now)
Add to the relevant `docs/systems/*.md` file under **Current Implementation** and update **Revision History**.

### For new game design decisions
Add to `docs/GAME_BIBLE.md` in the appropriate section. If it is confirmed, document it as fact. If it is speculative, add it to the section's **Future Expansion** sub-block.

### For new technical decisions
Add to `docs/architecture.md` and the relevant system doc.

### For known bugs or tech debt
Add to `docs/known_issues.md` with the file, nature of the issue, and severity.

### Never present speculation as canon
If a feature is not yet implemented or decided, use the ⚠️ **NOT YET DEFINED** marker in the Game Bible. Do not fill in lore, mechanics, or design decisions that are not in the codebase.

---

## How to Distinguish Confirmed Design Decisions from Future Ideas

| Marker | Meaning |
|---|---|
| ⚠️ **NOT YET DEFINED** | Feature is a placeholder only. Do not build on it without confirmation. |
| **[CONFIRMED]** | Implemented and working in code. |
| **[INFERRED]** | Derived from reading code; likely intent but not explicitly stated. |
| **[FUTURE EXPANSION]** | Not yet built. Possible direction only. Not canon. |

When in doubt: read the code. If it is in the code, it is real. If it is not in the code, it is not canon.

---

## How to Extend the Project While Maintaining Consistency

### Adding a New Hero to the Roster
1. Create a character sheet at `docs/characters/<name>.md` using `docs/characters/_character_template.md`.
2. Add a pronunciation entry to `docs/PRONUNCIATION_GUIDE.md`.
3. The hero's class, starting stats, and equipment loadout must be data-driven — no hardcoded per-hero logic in the game loop.
4. Add the hero to the roster table in `docs/PLAYER_SYSTEM.md` and `docs/GAME_BIBLE.md`.
5. **Do not** add a Custom Hero creation screen or character customization UI — that is Phase 2 and explicitly out of scope. See [`docs/PLAYER_SYSTEM.md`](PLAYER_SYSTEM.md).

### Adding a New System
1. Create a new `system_name_manager.py`.
2. Define the system's state as a module-level dict.
3. Import and use `world_state` for player/faction/region data — do not duplicate.
4. Subscribe to relevant events via `event_bus.py`.
5. Register save/load in `save_manager.py` (serialize/deserialize the module-level dict).
6. Document in `docs/systems/system_name.md`.
7. Update `docs/architecture.md` with the new module's place in the graph.

### Adding a New Event
1. Choose a clear snake_case event name.
2. Emit with `emit("event_name", key=value)` at the trigger point.
3. Subscribe with `subscribe("event_name", handler)` in all interested modules.
4. Document in `docs/systems/event_bus.md`.

### Adding New World State Fields
1. Add the field to the appropriate section subclass in `world_state.py`.
2. Set a safe default value.
3. Add it to `ensure_world_state_defaults()`.
4. Update `docs/systems/world_state.md`.

### Adding New Content (enemies, quests, items)
- Enemies: add to the dict in `enemy_manager.py`.
- Quests: add to `quest_database` in `quests.py`.
- Items: add to `ITEM_DATABASE` in `equipment_system.py` and/or `loot_manager.py`.
- Factions: add to `FACTIONS` in `faction_manager.py` AND to `world_state["factions"]` defaults.

---

## Known Architectural Risks

See `docs/known_issues.md` for the full list. Critical risks to be aware of:

1. **Dual player state** — `player.py` Player object and `world_state["player"]` have overlapping fields. Changes to one do not automatically propagate to the other. Combat uses `player.py`; most other systems use `world_state["player"]`.

2. **Region dual state** — `region_manager.py`'s `discover_region()` modifies `REGIONS[name]['discovered']` internally, while world_state tracks `discovered_regions` separately. These can diverge.

3. **`rebels` faction gap** — `world_state["factions"]` has a `rebels` key; `faction_manager.py`'s `FACTIONS` dict does not include rebels. Functions that iterate `FACTIONS` will miss rebel reputation.

4. **`validate_world_state` checks for `npcs` key** — `state_manager.py`'s validator expects `world_state["npcs"]` but no such key is initialized in `world_state.py`. This validation will fail on new games.

---

## Quick-Reference: Key File Relationships

```
main.py
  └── game_loop.py (run_game)
        ├── combat.py (quick_encounter, boss_encounter)
        │     ├── player.py (singleton)
        │     ├── enemy_manager.py
        │     ├── status_effects.py
        │     ├── companion_manager.py
        │     └── llm_bridge.py (ai_narrate, ai_combat_narration)
        ├── quest_manager.py (generate_quest)
        ├── world_event_manager.py
        ├── faction_manager.py (evolve_factions)
        ├── economy_manager.py (evolve_economy)
        ├── relationship_manager.py (decay_relationships)
        ├── companion_manager.py (banter, show_party)
        ├── dm_brain.py (update_dm_brain, show_dm_state)
        ├── story_manager.py (show_story_summary)
        ├── save_manager.py (autosave)
        ├── region_manager.py (show_regions)
        ├── settlement_manager.py (show_all_settlements)
        └── dialogue_manager.py (generate_rumor)

world_state.py ← imported by almost every module
event_bus.py   ← subscriptions wired at module load time
dm_brain.py    ← subscribes to enemy_killed, quest_completed
faction_manager.py ← subscribes to quest_completed, faction events
narrative_ai.py ← subscribes to enemy_killed, region_crisis
```
