# Game Bible
## AI-Driven Terminal RPG

> **Document Status:** Current as of July 2026. Reflects the codebase as it exists today. Sections marked ⚠️ **NOT YET DEFINED** contain confirmed placeholders — do not invent canon to fill them.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Vision Statement](#vision-statement)
3. [Core Design Pillars](#core-design-pillars)
4. [Genre](#genre)
5. [Target Audience](#target-audience)
6. [Gameplay Overview](#gameplay-overview)
7. [Player Experience Goals](#player-experience-goals)
8. [Core Gameplay Loop](#core-gameplay-loop)
9. [Combat Overview](#combat-overview)
10. [Character Systems](#character-systems)
11. [Enemy Systems](#enemy-systems)
12. [Boss Systems](#boss-systems)
13. [Equipment](#equipment)
14. [Skills](#skills)
15. [Items & Inventory](#items--inventory)
16. [Progression](#progression)
17. [Economy](#economy)
18. [Quests](#quests)
19. [Factions](#factions)
20. [Exploration & World](#exploration--world)
21. [AI Director (DM Brain)](#ai-director-dm-brain)
22. [Narrative & Story Generation](#narrative--story-generation)
23. [NPC & Social Systems](#npc--social-systems)
24. [Companions](#companions)
25. [User Interface Philosophy](#user-interface-philosophy)
26. [Accessibility Philosophy](#accessibility-philosophy)
27. [Art Direction](#art-direction)
28. [Audio Direction](#audio-direction)
29. [Technical Architecture](#technical-architecture)
30. [Save System](#save-system)
31. [Development Philosophy](#development-philosophy)
32. [Roadmap](#roadmap)
33. [Future Expansion Opportunities](#future-expansion-opportunities)

---

## Design Direction Notice

> **As of July 2026, the project's long-term design direction has been officially updated.**  
> The game is now targeting a **Stylized 3D Tactical RPG** with isometric camera and stylized fantasy art.  
> The previous sprite-based / gacha-inspired direction is no longer the primary foundation.  
> The current codebase is a **Python terminal prototype** that remains the authoritative implementation.  
> This is an intentional evolution, not a contradiction. The terminal engine's systems, mechanics, and architecture carry forward into the new direction.  
> See `DESIGN_DECISIONS.md` (Decision 011–014) for the full record of this pivot.

---

## Executive Summary

This is an **AI-driven Tactical RPG** currently implemented as a Python terminal prototype. The long-term design vision is a **Stylized 3D Tactical RPG** viewed from a fixed isometric camera. An AI Director (the "DM Brain") monitors session pacing and dynamically adjusts story pressure, encounter frequency, and narrative tone. The game blends tactical RPG structure (exploration, combat, quests, factions) with a runtime narrative layer that reacts to player decisions, world conditions, and session flow.

**Current implementation:** Python terminal (text-based, fully playable).  
**Target platform direction:** Stylized 3D with isometric camera.  
**Previous direction (gacha/sprite-based):** Archived as historical reference; individual mechanics may be reused where they fit.

A separate browser-based interface (`app.py`) exists in the repository but is currently independent of the terminal game. It is not in active use as the primary interface.

---

## Vision Statement

A single-player RPG experience in which the game feels like it is being run by an attentive, reactive Dungeon Master — one that remembers what the player has done, adjusts the pacing to keep sessions engaging, and generates narrative context appropriate to the current state of the world.

The game does not require real-time AI model access to function. The LLM layer (`llm_bridge.py`) is currently implemented as a mock that returns thematically appropriate hardcoded responses. The architecture is designed so that replacing mock functions with real API calls requires changes only inside `llm_bridge.py`.

---

## Core Design Pillars

### 1. Reactive World
The world changes in response to player actions. Faction reputation, completed quests, world events, and story memory all accumulate and affect future encounters, available quests, narrative tone, and NPC behavior.

### 2. AI-Paced Sessions
The DM Brain (`dm_brain.py`) tracks a `story_pressure` value (0–100) and a `current_focus` state. It adjusts narrative direction based on how many battles have occurred, how many story events have fired, and how much time has passed in the session. The player should never feel like the game is stuck at the same intensity level for too long.

### 3. Persistence and Memory
The game records major events, choices, discovered lore, and faction relationships across sessions. Story generation uses this memory to make narrative references feel earned and grounded.

### 4. Modular Architecture
Each game system is an independent Python module. Systems communicate through the event bus (`event_bus.py`) rather than direct cross-module calls where possible. This makes individual systems replaceable without breaking others.

### 5. Tactical Readability Over Realism
The visual design (in the 3D target) prioritizes clear communication of game state over photorealistic rendering. Silhouettes, readable environments, and expressive animation serve gameplay clarity first.

### 6. No External Dependencies at Runtime (Current Prototype)
The current terminal prototype runs entirely in Python with no external API calls required. The LLM layer is a drop-in module. This principle carries forward: the game must be functional without requiring a live AI connection.

---

## Genre

- **Target direction:** Stylized 3D Tactical RPG (isometric camera, turn-based or action-tactical combat)
- **Current implementation:** Text-based Role-Playing Game (Python terminal prototype)
- **Secondary elements:** Rogue-like pacing (session-based DM state), systemic RPG (faction/economy simulation)

> **Note:** Genre reflects the confirmed long-term design direction. The current terminal implementation is the active prototype from which the 3D game will grow.

---

## Setting — Elyndor

This game takes place within **Elyndor** — a standalone fantasy universe that exists independently of any single game.

- The world's lore, mythology, ancient legends, creatures, and history are maintained separately in [`elyndor/`](../elyndor/README.md)
- Do not mix universe-level world-building with game-specific content
- The Ancient Legends (Aurelia Sunstrider, Valen Ashfall) belong in the Elyndor Universe Bible — they are not members of this game's playable cast unless a future story explicitly establishes otherwise

See [`elyndor/world/world_overview.md`](../elyndor/world/world_overview.md) for the world description.

---

## Tone

A mix of **dark fantasy and adventure** — serious enough to honor real stakes, warm enough to make the characters worth caring about. Full details: [`docs/game_tone.md`](../game_tone.md).

---

## Target Audience

⚠️ **NOT YET DEFINED** — No explicit target audience document exists in the codebase. Based on the technical implementation (terminal Python, complex systems), the implied audience is players familiar with classic CRPGs and text adventure games.

---

## Gameplay Overview

The player starts from a CLI menu offering a new game or load. Once in the game, a main menu offers:

1. **Explore** — triggers a random event (60% combat, 20% quest, 20% world event)
2. **Travel** — moves to a new region (advances world tick)
3. **Rest** — recovers HP (advances world tick)
4. **View Character** — shows player stats
5. **View Regions** — shows region summaries
6. **View Settlements** — shows settlement summaries
7. **View Story** — shows current story summary
8. **View World Events** — shows active world events
9. **View DM State** — shows current AI director pacing state
10. **Save Game** — writes full save to disk
11. **Exit** — autosaves and exits

---

## Player Experience Goals

- The player should feel that their choices matter. Faction reputation, quest completions, and story memory are all persisted and reflected in narrative output and world conditions.
- Sessions should feel paced — not too quiet (only combat), not too intense (constant crises).
- The DM Brain should be invisible infrastructure. Players feel a responsive world, not an algorithm.

---

## Core Gameplay Loop

```
MAIN MENU
    │
    ├── EXPLORE
    │       ├── (60%) Combat encounter
    │       │       └── Resolve → loot, XP, faction/story events
    │       ├── (20%) Quest prompt
    │       │       └── Accept → track in active quests
    │       └── (20%) World event
    │               └── Apply effects → world_state, factions, story
    │
    ├── TRAVEL → advance tick, possible region change
    ├── REST   → recover HP, advance tick
    │
    └── TICK (every action)
            ├── World events update
            ├── Factions evolve
            ├── Economy evolves
            ├── Relationships decay
            ├── DM Brain evaluates pacing
            └── Autosave every 5 ticks
```

---

## Combat Overview

Combat is **turn-based** and terminal-driven. The player faces one or more enemies. Companions in the active party assist automatically.

### Combat Flow
1. Enemy (or boss) is selected and presented to the player.
2. Each round the player chooses: **Attack**, **Use Skill**, **Use Item**, or **Flee**.
3. Enemies counter-attack, apply status effects, and may use special moves (boss only).
4. Companions contribute attacks each round.
5. Combat ends when the enemy dies, the player dies, or the player successfully flees.

### Key Combat Mechanics
- **Attack Bonus** — player stat added to damage rolls.
- **Defense** — reduces incoming damage by a flat value.
- **Evasion** — chance to dodge attacks entirely.
- **Critical Hits** — enemies have a `crit_chance` field; crits deal doubled damage.
- **Elite enemies** — have enhanced stats flagged via `elite: True`.
- **Status Effects** — see Status Effects section below.
- **AI Narration** — `llm_bridge.ai_combat_narration()` is called for combat flavour text (mock implementation).
- **Post-combat** — enemy killed event fires on event bus, loot is awarded, XP is granted, DM Brain records the battle.

### Status Effects
Defined in `status_effects.py`. Current effects include: burn, freeze, stun, poison, bleed, slow, weaken, and shield. Effects are stored on the entity's `status_effects` list and resolved each round.

---

## Character Systems

### Player Model (`player.py`)
The `Player` class is a simple mutable object with:

| Field | Default | Notes |
|---|---|---|
| `name` | "Hero" | Display name |
| `hp` | 100 | Current health |
| `max_hp` | 100 | Maximum health |
| `attack_bonus` | 5 | Added to damage |
| `defense` | 2 | Flat damage reduction |
| `evasion` | 5 | Dodge chance |
| `level` | 1 | Current level |
| `gold` | 0 | Currency (also in world_state.player) |
| `status_effects` | [] | Active effects |

### Player State in World State (`world_state.py` — `PlayerState`)
A richer representation lives inside `world_state["player"]`:

| Field | Default | Notes |
|---|---|---|
| `class` | "Warrior" | Character class |
| `name` | "Wanderer" | Display name |
| `level` | 1 | Current level |
| `xp` | 0 | Current XP |
| `xp_to_next_level` | 100 | XP threshold |
| `gold` | 0 | Currency |
| `hp` / `max_hp` | 100 | Health |
| `resource_name` | "Stamina" | Second resource label |
| `resource` / `max_resource` | 100 | Second resource pool |
| `attack_bonus` | 5 | Combat stat |
| `defense` | 2 | Combat stat |
| `dodge` | 5 | Combat stat |
| `weapon_bonus` | 0 | Equipment modifier |
| `equipped_weapon` | "Rusty Sword" | Active weapon name |
| `inventory` | [] | Item list |

> **Note:** `player.py`'s `Player` object and `world_state["player"]` are **two separate data stores** with overlapping fields. `combat.py` uses the `Player` singleton; most other systems use `world_state["player"]`. This dual-state is a known tech debt item.

### Character Classes

⚠️ **NOT YET FULLY DEFINED** — `world_state["player"]["class"]` defaults to `"Warrior"`. No multi-class selection or class-specific ability trees are implemented beyond the default stat block.

---

## Enemy Systems

Enemies are defined as dictionaries in `enemy_manager.py`. Each enemy has:

| Field | Notes |
|---|---|
| `name` | Display name |
| `hp` / `max_hp` | Health pool |
| `damage` | Base damage per hit |
| `crit_chance` | Float probability of critical hit |
| `elite` | Bool — enhanced stats flag |
| `boss` | Bool — triggers boss behavior |
| `status_effects` | Active effects list |

Enemy selection is region- and world-state aware. Chaos level and world flags (cult_rising, civil_war, mages_rebellion) expand the available enemy pool in `story.py`.

---

## Boss Systems

Bosses are defined in `bosses.py`. The `boss_encounter()` function in `combat.py` handles boss-specific behavior. The currently confirmed boss is:

- **Ashen Guardian** — triggered with 10% probability via `random_boss_encounter()` in `game_loop.py`

Boss encounters have additional behavior beyond standard enemies (special moves, scaling). The full boss roster is ⚠️ **NOT YET FULLY DEFINED** beyond the Ashen Guardian.

---

## Equipment

Equipment is managed by `equipment_system.py`. Four equipment slots are defined:

| Slot | Key |
|---|---|
| Weapon | `weapon` |
| Armor | `armor` |
| Helmet | `helmet` |
| Accessory | `accessory` |

The `ITEM_DATABASE` in `equipment_system.py` defines items with stat modifiers applied to the `Player` object on equip and removed on unequip. Items are sourced from the player's inventory (`world_state["player"]["inventory"]`).

---

## Skills

Skills are defined in `skills.py` and tracked in `skill_tree.py`. A module-level `player_skills` dict holds active skill state and is serialized/loaded by `save_manager.py`.

⚠️ **NOT YET FULLY DEFINED** — The skill tree structure exists but the full skill roster, unlock conditions, and in-combat use pathways are not yet fully implemented.

---

## Items & Inventory

### Inventory
- Canonical inventory location: `world_state["player"]["inventory"]` (a list of item name strings).
- `inventory.py` provides UI helper functions: `show_inventory()`, `give_item()`, `take_item()`, `use_potion()`, `equip_weapon()`, `has_item()`, `inventory_count()`, `receive_loot()`, `show_gold()`.
- `add_item()` and `remove_item()` are world_state helpers (not in `inventory.py`).

### Loot
- `loot_manager.py` handles loot generation with rarity tiers (`RARITIES` dict) and stat scaling.
- `loot.py` is a legacy/standalone module (not integrated into manager flow).
- Post-combat loot is awarded via `award_loot()` / `add_loot_item()`.

### Shop
- `shop.py` defines the `SHOP_DATABASE` and transaction functions.
- Buy/sell prices are affected by `economy_manager` inflation.
- Players can buy potions, weapons, and other items.

---

## Progression

Managed by `progression_manager.py` with a `progression_state` dict serialized by `save_manager.py`.

- `check_level_up()` — evaluates whether XP threshold is reached.
- `show_progression()` — displays current level, XP, and threshold.

XP is granted post-combat and on quest completion (via `world_state["player"]["xp"] +=`). Level thresholds and stat growth on level-up are ⚠️ **NOT YET FULLY DEFINED** beyond the XP tracking infrastructure.

---

## Economy

Managed by `economy_manager.py` with a module-level `economy_state` dict.

| Key | Notes |
|---|---|
| `inflation` | Float modifier applied to prices |
| `trade_routes` | Dict of active trade connections |
| `global_stability` | Float affecting economy evolution |

Key functions:
- `get_item_price(item_name)` — returns inflation-adjusted price.
- `evolve_economy()` — called each game tick; adjusts inflation and stability.
- `trigger_economic_crisis()` — sharply degrades stability and inflation.
- `trigger_trade_route_event()` — randomly disrupts or boosts a trade route.

Economy state is serialized by `save_manager.py`.

---

## Quests

### Quest Database (`quests.py`)
The `quest_database` dict defines available quests. Each entry contains:

| Field | Notes |
|---|---|
| `description` | Player-facing text |
| `target_enemy` | Enemy type to defeat |
| `required_kills` | Number needed |
| `gold_reward` | Gold granted on completion |
| `xp_reward` | XP granted on completion |
| `faction` | Faction to receive reputation change |
| `reputation_reward` | Reputation delta |

Currently confirmed quests include: **Cult Hunt**, **Dragon Slayer**, and others defined in the database.

### Quest Tracking
- `world_state["quests"]["active"]` — list of active quest names.
- `world_state["quests"]["completed"]` — list of completed quest names.
- `world_state["quests"]["failed"]` — list of failed quest names.
- `world_state["quests"]["progress"]` — dict for kill counters / partial completion.

### Quest Manager (`quest_manager.py`)
Handles active quest list, `generate_quest()` (presents new quests), and `show_active_quests()`.

### Quest Generator (`quest_generator.py`)
Procedural quest generation layer. Can create new quest hooks dynamically.

### Quest Completion Flow
1. `reward_quest(quest_name)` in `quests.py` is called.
2. Quest marked complete in world_state.
3. Gold and XP awarded.
4. `change_faction_reputation()` called for the quest's faction.
5. `quest_completed` event emitted on event bus with `quest_name` and `quest` data dict.
6. DM Brain handler records the story event.
7. Faction manager handler grants a 10-point bonus if quest type is `"faction"`.

---

## Factions

Four factions are tracked in `world_state["factions"]`:

| Faction | Key | Notes |
|---|---|---|
| Kingdom | `kingdom` | Ruling authority |
| Shadow Cult | `shadow_cult` | Antagonist faction |
| Mages Guild | `mages_guild` | Arcane institution |
| Rebels | `rebels` | Resistance force |

Reputation is a value from **-100 to 100** (clamped). Each faction can enter `hostile`, `neutral`, `friendly`, or `allied` status tiers.

`faction_manager.py` owns the `FACTIONS` dict (deeper per-faction data: military_power, economy, influence) separate from the reputation values in `world_state["factions"]`.

When a faction becomes `hostile`, a `faction_hostile` event fires on the event bus, potentially triggering world events (e.g., "Cult Assassins" when shadow_cult turns hostile).

`evolve_factions()` is called each game tick and may shift faction relationships based on world conditions.

### Lore Status
⚠️ **NOT YET DEFINED** — The four faction names are confirmed. Detailed lore, history, leadership, motivations, internal structure, and inter-faction relationships have not been written. Do not invent this content.

---

## Exploration & World

### Regions (`region_manager.py`)
Each region is defined in `REGIONS` with:

| Field | Notes |
|---|---|
| `display_name` | Human-readable name |
| `biome` | Terrain type |
| `danger` | Encounter difficulty modifier |
| `faction` | Controlling faction |
| `weather` | Current weather string |
| `stability` | 0–100 stability value |
| `prosperity` | 0–100 prosperity value |
| `corrupted` | Bool |

Regions evolve over time via `evolve_world_regions()`. Corruption can spread. Weather changes. Faction control can shift.

The default starting region is `kingdom_capital`.

### Travel (`travel_manager.py`)
`travel_to_region(destination)` moves the player and generates an encounter via `encounter_manager.generate_encounter()`. `get_travel_options()` returns available destinations from the current region.

### Settlements (`settlement_manager.py`)
Settlements exist within regions. Each has prosperity, security, and service availability. `show_all_settlements()` prints a summary. Settlements generate rumors. Rumors feed into `dialogue_manager.generate_rumor()`.

### Dungeons (`dungeon_manager.py`)
A `DUNGEONS` dict defines dungeon locations. Dungeon state is serialized by `save_manager.py`. Full dungeon crawl mechanics are ⚠️ **NOT YET FULLY DEFINED** beyond the data structures.

### World Map (`world_map.py`)
Provides a text-based map representation. Currently a standalone display module.

### Hub (`hub.py`)
Defines a central hub location. Currently a standalone module, not integrated into the main game loop.

---

## AI Director (DM Brain)

The DM Brain (`dm_brain.py`) is the pacing and narrative orchestration system.

### DM State
```python
dm_state = {
    "story_pressure":     25,   # 0–100 intensity level
    "current_focus":      "exploration",  # current narrative mode
    "session_length":     0,    # ticks elapsed this session
    "last_event_type":    None, # most recent event category
    "recent_battles":     0,    # battles since last story event
    "recent_story_events": 0,   # story beats since last battle
}
```

### Pressure Levels → Focus States

| Pressure Range | Focus State | Meaning |
|---|---|---|
| 0–25 | `recovery` | Quiet; encourage exploration |
| 26–50 | `exploration` | Normal pacing |
| 51–75 | `escalation` | Building tension |
| 76–100 | `crisis` | Peak intensity |

### How Pressure Changes
- +5 per `enemy_killed` event
- `quest_completed` events call `evaluate_story_state()` which notes progression
- `evaluate_session_flow()` assesses if the session has been too combat-heavy or too quiet
- `evaluate_campaign_pressure()` responds to world-level threats
- `reset_session_trackers()` resets battle/event counts at session boundaries
- `change_story_pressure(amount)` can be called directly with positive or negative values (clamped 0–100)

### Event Bus Subscriptions
The DM Brain subscribes to:
- `enemy_killed` → increments `recent_battles`, adds pressure
- `quest_completed` → increments `recent_story_events`, evaluates story progression
- `narrative_encounter` → records story events
- `quest_completed` also triggers a memory store (via `memory_engine`)

---

## Narrative & Story Generation

### Story Generation (`story.py`)
`generate_story(enemies, factions, story_memory)` produces a narrative context string. It selects:
1. **Location** — from a pool expanded by world flags (civil_war, cult_rising, mages_rebellion, world_chaos ≥ 60)
2. **Quest hook** — from a pool expanded by faction reputation thresholds and story memory flags
3. **Enemy** — from enemies dict, expanded by world chaos (≥ 70: shadow beasts) and world flags

The function uses `world_state["world_conditions"]["world_chaos"]` as its chaos source (not the flat `world_chaos` key).

### Story Manager (`story_manager.py`)
Tracks `story_state` (act, flags, active story arcs) and `advance_story(amount)`. World events like "Cult Retaliation" increment `world_conditions.world_chaos` by 5.

### Narrative AI (`narrative_ai.py`)
Provides richer narrative functions:
- `narrate_region(region_name)` — generates region description
- `narrate_npc(npc_name)` — generates NPC description
- `generate_story_hook()` — creates a story premise
- `narrate_battle(enemy)` — generates battle description
- `narrate_quest(quest_name)` — generates quest context
- Subscribes to `enemy_killed` and `region_crisis` events

### LLM Bridge (`llm_bridge.py`)
**Current implementation: mock.** All functions return randomly selected hardcoded strings. The module is designed to be a drop-in replacement point.

| Function | Current behaviour |
|---|---|
| `ai_narrate(prompt)` | Prints one of 7 fixed narrative lines |
| `ai_generate_quest()` | Prints one of 7 fixed quest rumors |
| `ai_combat_narration(attacker, defender, damage)` | Prints one of 7 fixed combat lines |
| `ai_dialogue(npc, context)` | Returns one of 7 fixed NPC lines |

### Memory Engine (`memory_engine.py`)
Stores and retrieves major events for narrative reference. Used by DM Brain and narrative systems to check what the player has done.

### Prompt Manager (`prompt_manager.py`)
Manages prompt templates for future LLM integration. Currently a support module.

---

## NPC & Social Systems

### NPC Manager (`npc_manager.py`)
- `NPCS` dict defines named NPCs with roles, relationships, and interaction history.
- `get_npc(name)` retrieves NPC data.
- `change_relationship(name, amount)` updates relationship score.
- `random_npc_event()` fires a random NPC interaction.

### Dialogue Manager (`dialogue_manager.py`)
- `npc_relationships` dict tracks per-NPC relationship values (serialized by save_manager).
- `generate_rumor()` produces world-state-aware rumor text.
- `start_dialogue(npc_name)` drives conversation flow.
- `persuasion_check()` and `intimidation_check()` provide skill-check dialogue options.

### Dialogue AI (`dialogue_ai.py`)
Wraps `llm_bridge.ai_dialogue()` for NPC conversation generation.

### Relationship Manager (`relationship_manager.py`)
- `social_state` dict tracks community-level relationship scores (serialized by save_manager).
- `decay_relationships()` — called each tick; relationships drift toward neutral over time.
- `generate_social_event()` — fires random community events.
- `world_social_reaction()` — exists but is not currently called (dead import removed).

---

## Companions

Managed by `companion_manager.py`. A `COMPANIONS` dict defines recruitable companions and an `active_companions` list tracks the current party.

### Companion Fields (per companion)
- Role, abilities, loyalty score, story reactions
- Loyalty modified by `change_loyalty(companion_name, amount)`
- Corrupt state via `corrupt_companion()`

### Companion Combat
- `companion_attack(companion_name, enemy)` — companion attacks during combat rounds
- `use_companion_ability(companion_name, ability)` — ability use
- `calculate_party_bonus()` — returns aggregate party stat bonuses

### Companion Interaction
- `random_companion_banter()` — fires during game ticks
- `show_party()` — displays current companions
- `companion_story_reaction(event)` — companions react to narrative events

### Companion Roster
⚠️ **NOT YET FULLY DEFINED** — The infrastructure exists. Specific companion characters, their backstories, abilities, and recruitment conditions are not yet defined.

---

## User Interface Philosophy

The game is **entirely text-based** (terminal). There is no graphical UI.

- All output is `print()` statements to stdout.
- All input is `input()` prompts.
- Menu choices are number strings ("1", "2", etc.).
- Status information is shown on demand (player stats, regions, story, world events).
- A separate Flask browser application (`app.py`) exists in the repository but is not part of the terminal game's UX.

⚠️ **NOT YET DEFINED** — No formal UI style guide exists. Color, formatting conventions (beyond `===` banners), or screen layout standards have not been specified.

---

## Accessibility Philosophy

⚠️ **NOT YET DEFINED** — No accessibility guidelines have been specified. The text-based format is inherently compatible with screen readers and keyboard navigation.

---

## Art Direction

**[CONFIRMED — Design Direction]** The target visual style is **stylized fantasy**. This is the official art direction for the 3D version of the game.

### Core Principles

| Principle | Detail |
|---|---|
| **Stylized fantasy** | Not photorealistic; art style should feel timeless and expressive |
| **Strong character silhouettes** | Characters must be instantly readable at tactical camera distance |
| **Readable environments** | Terrain, obstacles, and pathways must be legible during gameplay |
| **Expressive animations** | Animations communicate character personality and ability impact |
| **Gameplay clarity first** | Visual design serves tactical understanding over aesthetic spectacle |
| **Timeless visuals** | Style choices that age well rather than chasing current trends |

### What Is NOT a Design Goal

- Photorealism — explicitly rejected
- High-fidelity texture detail that reduces gameplay readability
- Visual complexity that obscures tactical information

### Camera

The game uses a **fixed (or mostly fixed) isometric camera** in the 3D target implementation. Camera behavior prioritizes:
- Tactical readability — the player must always be able to see and understand the battlefield
- Strategic overview — the camera height and angle serve decision-making, not cinematic presentation

### Current Implementation Note

The current Python terminal prototype has no visual assets. This section defines the target direction. No art assets should be created that contradict these principles.

---

## Audio Direction

⚠️ **NOT APPLICABLE / NOT YET DEFINED** — No audio system exists. This section is reserved for future development.

---

## Technical Architecture

See `/docs/architecture.md` for the full technical breakdown.

**Summary:**
- **Language:** Python 3
- **Interface:** Terminal (stdin/stdout)
- **Architecture:** Module-per-system, event-bus communication
- **State:** Centralized in `world_state.py` + per-module state dicts
- **Persistence:** JSON save files (`save_data.json`, `savegame.json`)
- **AI Layer:** Mock LLM bridge (drop-in replacement ready)
- **Secondary app:** Flask web app (`app.py`) — unrelated to terminal game

---

## Save System

Two save systems coexist:
1. **`state_manager.py`** — Lightweight, saves only `world_state`. Used internally.
2. **`save_manager.py`** — Full save: world_state + all manager state dicts + player object + equipment + companions + dm_state.

Both use JSON serialization. Both call `ensure_world_state_defaults()` after loading to handle schema migrations from older saves.

See `/docs/systems/save_system.md` for details.

---

## Development Philosophy

- **Module isolation** — each system owns its own state and is imported by others, not the reverse (where possible).
- **Event bus communication** — cross-system reactions happen through `event_bus.py` subscriptions, not direct function calls.
- **No mandatory LLM dependency** — the game must be fully playable with mock AI responses.
- **Preserve existing patterns** — new code should match the existing coding style (see `/docs/coding_standards.md`).
- **Document before expanding** — before adding systems, document what exists.

---

## Playable Characters

Five confirmed playable characters / companions. Full character sheets: [`docs/characters/`](../characters/).

| Character | Race | Class | Key Trait |
|---|---|---|---|
| [Talos](../characters/talos.md) | Elf | Knight | Jaded veteran; protective, guarded, warm underneath |
| [Eleanor](../characters/eleanor.md) | Human | Mage | Young, optimistic, unnaturally strong elemental bond |
| [Ragash](../characters/ragash.md) | Orc | Houndmaster | Blunt and proud; devoted to her hounds above all else |
| [Ronan](../characters/ronan.md) | Human | Werewolf | Cursed drifter; seeks a cure; fears losing control |
| [Steven](../characters/steven.md) | Human | Miner | Silent, rare, mysterious; solves problems simply |

---

## Roadmap

See `/docs/roadmap.md` for the tracked development roadmap.

**Immediate priorities (based on known tech debt):**
1. Unify `player.py` singleton and `world_state["player"]` into a single source of truth.
2. Implement playable skill tree with combat integration.
3. Define and implement character class selection at new game.
4. Flesh out dungeon crawl mechanics.

---

## World Scope

**[CONFIRMED — Design Direction]**

- The playable game takes place on **one continent**.
- The existence of additional continents or other civilizations has **intentionally not been defined**.
- Do not invent additional continents, oceans, or civilizations beyond the playable continent.
- The world should remain open for natural expansion outward from the playable area.

### World-Building Philosophy

Future world-building should grow **outward from the playable continent** as it becomes relevant to gameplay. Avoid defining the full world before it becomes relevant to the player's experience. Undefined areas are not gaps — they are intentional creative space.

---

## Future Expansion Opportunities

These are **possible** future directions, not confirmed designs:

- **Lore and World-Building** — The faction names and world flags (civil_war, dragon_alive, etc.) are named placeholders ready for lore expansion. A full world history, NPC backstories, and location lore can be layered in without changing the data structure. World-building should expand from the single playable continent outward.
- **3D Engine Implementation** — The current terminal prototype's systems (combat, quests, factions, economy, AI Director) translate directly to the 3D target. The game logic layer does not depend on the rendering layer.
- **Real LLM Integration** — Swapping `llm_bridge.py` mock implementations for real API calls (OpenAI, Anthropic, local model) requires only changes inside that file.
- **Crafting System** — The economy and inventory infrastructure supports crafting but no crafting system is currently implemented.
- **Campaign Mode** — `campaign_manager.py` tracks act progression. A scripted multi-act campaign can be built on top of this.
- **Procedural World Generation** — The region and settlement systems support dynamic creation; a procedural generator could be added.
