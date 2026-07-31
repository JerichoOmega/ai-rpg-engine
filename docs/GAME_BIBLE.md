# Game Bible
## AI-Driven Terminal RPG

> **Document Status:** Current as of July 2026. Reflects the codebase as it exists today. Sections marked ⚠️ **NOT YET DEFINED** contain confirmed placeholders — do not invent canon to fill them.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Vision Statement](#vision-statement)
3. [Core Design Pillars](#core-design-pillars)
4. [Playable Races](#playable-races)
5. [Genre](#genre)
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
34. [Player Character Philosophy](PLAYER_SYSTEM.md) *(separate file)*
35. [Campaign Design Philosophy](CAMPAIGN_DESIGN.md) *(separate file)*
36. [World Bible](world/WORLD_BIBLE.md) *(separate file)*
37. [Playable Races](world/RACES.md) *(separate file)*
38. [Vampire Houses](world/vampire_houses.md) *(separate file)*
39. [Goblin Tribes](world/goblin_tribes.md) *(separate file)*
40. [Religions of Elyndor](world/religions.md) *(separate file)*
41. [Dynamic Story Arcs](systems/dynamic_story_arcs.md) *(separate file)*
42. [History Bible](../elyndor/history/HISTORY_BIBLE.md) *(separate file — Four Ages framework)*
43. [Magic Bible](../elyndor/magic/MAGIC_BIBLE.md) *(separate file — Primordial Magic, Divine Chorus, magic limitations, Eleanor's Harmonic Soul)*
44. [Journey System](systems/journey_system.md) *(separate file — travel as storytelling, camp philosophy, companion relationships, interaction scheduling, camp evolution)*
45. [The Forgotten Eighth](../elyndor/history/the_eighth.md) *(separate file — the Ancient God's true identity, the Great Forgetting, the Imprisonment as tragedy, Corruption as amplified virtue)*
46. [Pronunciation Guide](PRONUNCIATION_GUIDE.md) *(separate file)*

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

## Lore Design Philosophy

All world-building in Project Dungeon Keeper follows five rules. These apply to history, factions, cultures, monsters, artifacts, locations, and everything else added to the canon.

| Rule | Principle |
|---|---|
| **Rule One — Gameplay purpose** | Never create lore that has no gameplay purpose. Every historical event, faction, culture, religion, artifact, monster, or location should eventually influence quests, dialogue, exploration, combat, politics, or companion interactions. |
| **Rule Two — Companions experience the world** | Companions are not observers — they are participants. Major world events should affect them emotionally. Dynamic Campaign Story Arcs should unlock unique conversations, disagreements, emotional growth, and camp scenes. |
| **Rule Three — Regional identity** | Every region must have a distinct identity the player immediately recognizes. The Frontier is adventure and danger. The Great Forest is ancient mystery and elven history. The Iron Peaks is dwarven civilization and craftsmanship. The Frozen Highlands is survival and resilience. Sol Kareth is trade, archaeology, and desert kingdoms. The Capital Province is politics, military, religion, and education. |
| **Rule Four — Internal faction conflict** | Every intelligent faction contains internal disagreements. No faction is completely unified. The world feels alive because its factions argue with each other. |
| **Rule Five — AI DM builds within canon** | The AI Dungeon Master creates stories inside established canon. It does not rewrite history. It builds on existing lore while respecting all canonical documentation. |

---

## Playable Races

Six races are confirmed playable at launch. Race defines cultural context — not personality.

> Not every dwarf enjoys mining. Not every elf embraces ancient traditions. Not every orc seeks battle. Individuals are shaped by experience, not ancestry.

| Race | Notes |
|---|---|
| **Humans** | Most widespread; culturally diverse |
| **Elves** | Long-lived; associated with the Great Forest and ancient traditions |
| **Dwarves** | Homeland in the Iron Peaks; mining and forging tradition |
| **Orcs** | Own society, culture, and politics — not defined by conflict |
| **Halflings** | Distributed across the continent along river and trade networks; the continent's most practiced trading people; cultural philosophy: "The road always continues" |
| **Gnomes** | Concentrated in the lower Iron Peaks and Capital; renowned archivists and instrument-makers; cultural philosophy: "What is not recorded is lost" |

**Non-playable intelligent races:** Goblins (three named tribes — Stonefang, Mossroot, Ashfire). Other intelligent races may be introduced if they naturally fit the setting.

Full race design philosophy: [`docs/world/RACES.md`](world/RACES.md)

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

For official pronunciation of all proper nouns in this universe, see [`docs/PRONUNCIATION_GUIDE.md`](PRONUNCIATION_GUIDE.md).

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

> **Full combat design spec:** [`docs/COMBAT_SYSTEM.md`](COMBAT_SYSTEM.md)  
> **Terminal prototype implementation:** [`docs/systems/combat.md`](systems/combat.md)

Combat is a **turn-based tactical system** fought on **square grids** in fully **3D isometric environments**. The design rewards tactical positioning, team synergy, and planning over speed.

### Combat Philosophy

| Pillar | Description |
|---|---|
| Tactical positioning | Where you stand shapes what you can do |
| Meaningful decisions | Every turn presents real choices |
| Team synergy | Heroes combine through positioning and ability chaining |
| Readable combat | What is happening is always clear |
| Flexible choice | Multiple valid approaches to any encounter |

### Action Economy

Each hero receives per turn:

| Resource | Purpose |
|---|---|
| **Movement Points (MP)** | Tile movement — flexible order (move → act, act → move, or split) |
| **Action Point Pool (AP)** | Attacks, spells, class abilities, dash, combat interactions |
| **Support Action** | One dedicated utility action (heal, buff, revive, potion) — separate from AP |
| **Reaction** | One reactive trigger per round (opportunity attack, block, counter, ally protection) |

### Initiative

Each combatant has an Initiative value. Heroes whose turns fall consecutively may activate in any player-chosen order before initiative passes to the enemy side — enabling tactical combinations.

### Facing

Combatants have directional facing: **Front / Side / Rear**. Facing affects shield coverage, defensive bonuses, flanking, and back attack damage. Positioning relative to enemies is a core tactical layer.

### Shield Stance

Shield-bearing heroes may spend their **Support Action** to enter Shield Stance — a persistent frontal defense mode granting increased block chance, reduced incoming damage from the front, and access to shield-specific Reactions. The stance persists between turns at no further cost. Lowering the shield is free and returns the Support Action to normal use on that turn. This makes shields an active tactical choice rather than a passive stat bonus. Full rules: [`docs/COMBAT_SYSTEM.md`](COMBAT_SYSTEM.md).

### Downed & Death

**Downed** (0 HP): hero cannot act; allies can revive them with a Support Action. If combat ends while downed, the hero survives with very low HP and enters Critical Condition.

**Death**: separate from Downed. Only through execution, special enemy abilities, or story events. Requires resurrection mechanics to reverse — not standard healing.

### Party

Four active heroes in combat. Party composition is locked during combat; swapping is available freely outside combat.

### Current Terminal Prototype

The Python implementation (`combat.py`) is a simplified placeholder: single player, no grid, Attack / Skill / Item / Flee menu, no AP economy or facing. It remains the authoritative *current implementation*. The design above is the *target* for the 3D game.

### Status Effects (Terminal Prototype)
Defined in `status_effects.py`: burn, freeze, stun, poison, bleed, slow, weaken, shield. Effects tick each round.

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

### Companion Specialization Philosophy

Each companion has three distinct specialization paths rather than a single progression line or Ultimate abilities. Players cannot unlock all three paths — every investment should matter, and every build should feel unique while remaining viable.

| Companion | Path 1 | Path 2 | Path 3 |
|---|---|---|---|
| **Talos** | Guardian | Commander | Duelist |
| **Eleanor** | Elemental Harmony | Battlefield Control | Arcane Support |
| **Ragash** | Ambusher | Survivalist | Skirmisher |
| **Ronan** | Beast Hunter | Controlled Lycan | Tracker |
| **Torren** | Forge Master | Engineer | War Smith |

**Design principle:** No build should invalidate another. Each path should encourage meaningfully different tactical strategies while preserving the companion's core identity. This is inspired by the philosophy of deep specialization games — meaningful choice, not overwhelming complexity.

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

> **Full technical spec:** [`docs/systems/progression_skills.md`](systems/progression_skills.md)

### Level Cap

The maximum character level is **25**.

Every level should feel impactful. The cap is designed to provide meaningful progression throughout the campaign without excessive stat inflation. Future expansions may raise it, but the base game is balanced around Level 25.

### Experience System — Shared XP

Experience earned from combat, quests, exploration, and other gameplay activities is awarded to the **entire roster** — not only the active party.

| Benefit | Description |
|---|---|
| Equal active levels | All active party members stay at the same level |
| Viable reserves | Bench heroes remain usable without grinding |
| Composition freedom | Players can experiment with different team builds |
| No mandatory grinding | Newly recruited or rotated companions do not fall behind |

### New Companion Level Scaling

When a new companion joins the roster, they **immediately join at the player's current level**.

A companion recruited at Level 7 arrives at Level 7. A companion recruited at Level 18 arrives at Level 18.

New companions join with level-appropriate:
- Attributes
- Equipment
- Learned abilities
- Passive talents
- Skill points (if applicable)

This keeps every newly recruited hero immediately usable in combat and reinforces the game's focus on tactical choice rather than maintenance grinding.

### Design Philosophy

Progression should encourage experimentation rather than punish it. Players should feel free to recruit new companions at any point, swap party compositions between encounters, and adapt their roster to upcoming battles without being penalized for doing so.

### Current Implementation Status

The terminal prototype tracks XP in `world_state["player"]["xp"]` and calls `check_level_up()` post-combat. Shared XP distribution across the roster and companion level scaling are ⚠️ **NOT YET IMPLEMENTED** — these are the design target. See `docs/systems/progression_skills.md` for the current technical state.

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

## Intelligent Factions Design Philosophy

Not every intelligent creature or group in this world is automatically evil.

Each faction in the world — whether goblin tribes, orc warbands, vampire covens, werewolf packs, witches, necromancers, cults, or mercenary companies — must possess:

- **Goals** — what they are trying to achieve
- **Territory** — where they operate and why
- **Leadership** — who leads and how that leadership holds
- **Politics** — internal power dynamics; factions are not monoliths
- **Internal conflicts** — dissent, fracture, and competing interests exist within every group

Diplomacy should sometimes be possible. The player's first instinct should not always be violence.

### Vampires

Vampires are one of the world's major supernatural factions and should never feel like generic enemies. They range from ancient vampire lords (politically significant, planning in decades) to vampire nobles (society-embedded, may operate under other identities), newly turned individuals (may not have chosen their condition), feral vampires (lost to instinct), and secret covens (operating within cities). Campaign vampire presence varies widely — some campaigns barely feature them; others may center on stopping an expanding vampire threat. Full details: [`docs/world/WORLD_BIBLE.md`](world/WORLD_BIBLE.md)

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

### Additional Factions (Design Target)

The full reputation system tracks many more factions than the current four. Confirmed factions for future implementation:

| Faction | Notes |
|---|---|
| **Adventurers Guild** | Neutral organization; monster contracts, exploration, escort, bounties, rumor gathering; major quest source |
| **Goblin Tribes** | Three named tribes tracked independently: **Stonefang** (raiders), **Mossroot** (survivalists), **Ashfire** (newly unified, expanding) |
| **Vampire Houses** | Three major houses tracked independently; ⚠️ names NOT YET DEFINED |
| **Religious Orders** | ⚠️ NOT YET DEFINED — depends on religion framework |
| **Mercenary Companies** | ⚠️ NOT YET DEFINED — specific companies to be established |

Full faction design philosophy: [`docs/world/WORLD_BIBLE.md`](world/WORLD_BIBLE.md)  
Full reputation system design: [`docs/systems/reputation.md`](systems/reputation.md)

### Lore Status
⚠️ **NOT YET DEFINED** — The four tracked faction names are confirmed in code. Detailed lore, history, leadership, motivations, internal structure, and inter-faction relationships have not been written. Do not invent this content.

---

## Exploration & World

> **Full technical spec:** [`docs/systems/world_regions.md`](systems/world_regions.md)  
> **Canonical regions, travel encounters & faction design:** [`docs/world/WORLD_BIBLE.md`](world/WORLD_BIBLE.md)

The game uses a **two-layer exploration system**: a strategic continent map for travel between major locations, and handcrafted explorable regions for detailed gameplay within each destination.

### Canonical Regions

Six regions are confirmed canon. Each has a distinct identity and a relationship to The Corruption.

| Region | Character | Corruption note |
|---|---|---|
| **The Frontier** | Untamed edge of civilization; frontier towns, military outposts, goblin/orc presence | First to show Corruption — weakest institutions fall first |
| **The Great Forest** | Ancient forests, elven settlements, magical wildlife, hidden shrines | Portions become twisted as Corruption spreads |
| **The Iron Peaks** | Massive mountain range; dwarven strongholds, cave systems, dragons | Wakes ancient buried things; Torren's craft knowledge and smith's eye for stone give him unique interactions here |
| **The Frozen Highlands** | Remote northern wilderness; ice caves, ancient fortresses, giant beasts | Corruption arrives late but hits hard |
| **Sol Kareth** *(The Desert Kingdom)* | Oasis cities, merchant caravans, ancient tombs, buried civilizations; one of the oldest civilizations on the continent | Wakes what was buried under sand |
| **The Capital Province** | Political center; noble houses, government, military, trade intrigue | Most responsive to player choices; Political Corruption most visible |

Full region details: [`docs/world/WORLD_BIBLE.md`](world/WORLD_BIBLE.md)

### Layer 1 — Strategic Continent Map

Players select destinations across the continent rather than manually traversing the world. The map is inspired by Solasta's strategic travel layer.

Travel between locations may trigger:

| Event type | Description |
|---|---|
| Random encounters | Combat or non-combat events on the road |
| Story events | Narrative moments tied to world state |
| Companion conversations | Character moments during the journey |
| Merchant caravans | Trading opportunities mid-travel |
| Ambushes | Enemy interception attempts |
| Dynamic world events | Events driven by current world conditions |

> Travel should feel like a journey rather than a loading screen.

The continent map **evolves throughout the story** — reflecting world events, political changes, and the consequences of player decisions. Locations may open, close, become contested, or change in character as the campaign progresses.

### Layer 2 — Regional Exploration

Upon arriving at a destination, the player enters a **handcrafted explorable region**.

Each region contains:
- Main story content
- Side quests
- Hidden areas
- Dungeons
- Companion content
- Treasure
- Environmental storytelling

Regions reward exploration while avoiding unnecessary empty space.

### Design Philosophy

The continent should feel vast without requiring players to manually traverse every mile. The strategic map handles scale; the regions handle depth.

### Technical Implementation (Terminal Prototype)

The terminal prototype implements a simplified version of this system:

- **Regions** (`region_manager.py`) — named regions with biome, danger, faction, weather, stability, prosperity. Evolve each tick via `evolve_world_regions()`.
- **Travel** (`travel_manager.py`) — `travel_to_region(destination)` moves the player and generates an encounter.
- **Settlements** (`settlement_manager.py`) — sub-region locations with services and rumors.
- **Dungeons** (`dungeon_manager.py`) — data structures defined; full crawl mechanics ⚠️ **NOT YET IMPLEMENTED**.
- **World Map** (`world_map.py`) — static text display; not connected to live region state.

The two-layer strategic/regional structure described above is the **design target** for the 3D game. The terminal prototype's region data model (biome, danger, faction, weather) carries forward; the visual map and travel UI will be replaced.

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

## Main Story

> **Universe lore:** [`elyndor/history/the_corruption.md`](../elyndor/history/the_corruption.md)  
> **Full campaign design philosophy:** [`docs/CAMPAIGN_DESIGN.md`](CAMPAIGN_DESIGN.md)

### The Central Conflict

An ancient god was imprisoned long ago by forces now forgotten. At the start of every campaign, the god remains sealed — but its prison has begun to weaken. As the seal deteriorates, the god's presence slowly leaks into the world.

This presence is **The Corruption**.

### The Corruption

The Corruption is not mind control. It does not force people to become evil. Instead, it **amplifies existing flaws** — fear, hatred, greed, ambition, despair, and violence already present in the world.

| What it affects | How |
|---|---|
| People & rulers | Amplifies flaws; ambitious rulers become tyrants; fearful communities turn hostile |
| Religion | Cults receive whispers; holy orders fracture; ancient temples awaken |
| Nature | Forests twist; crops fail; wildlife mutates; ancient monsters wake |
| Magic | Spells become unstable; ancient relics activate; magical disasters multiply |

> **Individuals remain responsible for their choices.** The Corruption accelerates darkness that already exists — it does not create it.

### The Mystery

Most people in the world do not know the true cause of the world's decline. Each faction has its own explanation, creating political conflict and misinformation throughout the campaign. The player experiences the consequences of the god's influence long before discovering its existence. The mystery unfolds gradually through exploration, quests, companion stories, ancient records, and environmental storytelling.

The imprisoned god is not simply a final boss — its awakening is the **catalyst for the entire campaign**.

### Campaign Variations

Every campaign shares the same overarching threat — the imprisoned god is awakening — but **how The Corruption spreads differs between playthroughs**:

| Variation type | Manifestations |
|---|---|
| **Political** | Kingdoms descend into civil war; nobles become oppressive; assassinations multiply |
| **Natural** | Forests become cursed; crops fail; wildlife mutates; ecosystems collapse |
| **Religious** | Cults spread rapidly; holy orders fracture; ancient temples awaken; religious war erupts |
| **Arcane** | Magic becomes unstable; ancient relics activate; mages lose control; magical disasters multiply |

Multiple types may appear in a single campaign, but each playthrough emphasizes different aspects of the world's decline.

### Design Philosophy

The main story framework is **consistent across campaigns; the expression is variable**:

- The imprisoned god is awakening — always
- The world is falling into chaos — always
- The player must uncover the truth — always

What changes: how The Corruption manifests, which factions rise or fall, which companions join the party, regional events, quest availability, world state, and the consequences of player choices.

This creates a game with a **handcrafted central narrative** while allowing the AI Director to generate meaningful variation across multiple playthroughs. Every campaign should feel like a different telling of the same great legend — not an entirely unrelated story.

### Design Goal

| Pillar | Description |
|---|---|
| Handcrafted central narrative | Consistent, authored story with established lore |
| Memorable companion stories | Heroes with distinct identities, wounds, and arcs |
| Tactical turn-based combat | Grid-based, strategic, readable |
| Dynamic world evolution | World changes based on The Corruption and player choices |
| Meaningful player choices | Consequences that persist across the campaign |
| High replayability | Campaign variation; every run feels worth having |

**Target player feeling:** *"What happened in someone else's world?"* — a player who finishes one campaign immediately wants to start another to discover how this version of the world unfolded differently. See [`docs/CAMPAIGN_DESIGN.md`](CAMPAIGN_DESIGN.md) for the full philosophy.

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

> **Companion design philosophy:** [`docs/HERO_BIBLE.md`](HERO_BIBLE.md)  
> **Design checklist & Core Wound system:** [`docs/CHARACTER_DESIGN_GUIDE.md`](CHARACTER_DESIGN_GUIDE.md)  
> **Individual Hero Bible entries:** [`docs/heroes/`](heroes/)

### Design Standard

Every companion is handcrafted. A companion is never simply "a tank" or "a mage." Their gameplay, abilities, dialogue, personality, equipment, and story all reinforce who they are as a person. Mechanics grow from character — not from slot-filling.

Each companion has one **Core Wound** — a defining emotional scar that connects their personality, dialogue, combat role, unique passive, personal quest, and relationships. No two companions share a unique passive. See [`docs/HERO_BIBLE.md`](HERO_BIBLE.md) for full philosophy.

### Confirmed Companions & Core Wounds

| Hero | Core Wound | Hero Bible |
|---|---|---|
| Talos | Lost faith in authority after years of war | [`docs/heroes/TALOS.md`](heroes/TALOS.md) ✅ |
| Eleanor | Naive optimism leaves her vulnerable to betrayal | [`docs/heroes/ELEANOR.md`](heroes/ELEANOR.md) ✅ |
| Ragash | Rejected by her people; found belonging with her hounds | [`docs/heroes/RAGASH.md`](heroes/RAGASH.md) ✅ |
| Ronan | Believes his curse makes him a danger to everyone | [`docs/heroes/RONAN.md`](heroes/RONAN.md) ✅ |
| Torren | He once refused to let go of something that could not be saved; his philosophy of restoration was built from that loss | [`docs/heroes/TORREN.md`](heroes/TORREN.md) ✅ |

### Technical Implementation (`companion_manager.py`)

Managed by `companion_manager.py`. A `COMPANIONS` dict defines recruitable companions and an `active_companions` list tracks the current party.

- **Companion fields:** role, abilities, loyalty score, story reactions
- **Loyalty:** `change_loyalty(companion_name, amount)`
- **Combat:** `companion_attack()`, `use_companion_ability()`, `calculate_party_bonus()`
- **Interaction:** `random_companion_banter()`, `show_party()`, `companion_story_reaction(event)`

⚠️ The terminal prototype infrastructure exists. Full ability implementation, recruitment conditions, and Hero Bible integration are not yet implemented.

### Journey System — How Companion Relationships Develop

Companion relationships are not built at a hub between missions. They develop **during travel** — on the road, at camp, through shared hardship and shared rest.

The Journey System governs:
- How travel segments distribute companion interactions across camps
- An invisible interaction scheduler that prevents conversation stacking and maintains emotional pacing
- Six camp event types: Companion Conversation, Group Conversation, Player Activity, Story Event, World Event, Quiet Camp
- A full companion relationship network (every pair, not only player↔companion)
- Corruption resistance as the primary mechanical reward for relationship depth
- Companion interventions during critical Corruption moments — available only when the relationship has been earned
- Dynamic Dialogue Memory — past interactions are referenced in future dialogue
- Camp evolution from strangers (early game) through trust (mid game) to family (late game)

Full system: [`docs/systems/journey_system.md`](systems/journey_system.md)

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

Five confirmed playable characters. Full character sheets: [`docs/characters/`](../characters/).

For the initial version of the game, players **select one of these predefined heroes** before the adventure begins. Each is a fully realized character with a unique identity, backstory, class, personality, story dialogue, and starting equipment loadout. Full details: [`docs/PLAYER_SYSTEM.md`](PLAYER_SYSTEM.md).

| Character | Race | Class | Key Trait |
|---|---|---|---|
| [Talos](../characters/talos.md) | Elf | Knight | Jaded veteran; protective, guarded, warm underneath |
| [Eleanor](../characters/eleanor.md) | Human | Mage | Young, optimistic, unnaturally strong elemental bond |
| [Ragash](../characters/ragash.md) | Orc | Houndmaster | Blunt and proud; devoted to her hounds above all else |
| [Ronan](../characters/ronan.md) | Human | Werewolf | Cursed drifter; seeks a cure; fears losing control |
| [Torren](../characters/torren.md) | Human | Master Blacksmith | Calm, patient; builds what endures; the party's craftsman and quiet optimist |

> **Future:** A fully customizable player character (name, appearance, class, background) is planned for a later phase. It is intentionally out of scope for v1 and must not influence current system design. The hero framework must support both predefined and custom heroes without a major rewrite. See [`docs/PLAYER_SYSTEM.md`](PLAYER_SYSTEM.md) for the architecture requirement.

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
