# Documentation Index

> **AI-Driven Terminal RPG** — Complete documentation suite.  
> Last updated: July 2026.  
> Start here. Every document in this directory is linked below.

---

## Quick Start for New Contributors

1. **Read the Game Bible first** → [`GAME_BIBLE.md`](GAME_BIBLE.md) — What the game is, every mechanic.
2. **Understand the architecture** → [`architecture.md`](architecture.md) — How modules connect.
3. **Know the coding style** → [`coding_standards.md`](coding_standards.md) — How to write code here.
4. **Check known issues** → [`known_issues.md`](known_issues.md) — What's broken; don't accidentally fix it mid-task.
5. **If you're an AI assistant** → [`AI_CONTINUATION_GUIDE.md`](AI_CONTINUATION_GUIDE.md) — Specifically written for you.

---

## Root-Level Project Documents

These live at the project root — read them first.

| Document | Description |
|---|---|
| [`../PROJECT_STATE.md`](../PROJECT_STATE.md) | **Current project health** — completion %, active bugs, priorities, blocked work |
| [`../PROJECT_MEMORY.md`](../PROJECT_MEMORY.md) | **AI quick-start guide** — understand the full project in under 5 minutes |
| [`../DESIGN_DECISIONS.md`](../DESIGN_DECISIONS.md) | Architectural decision record — why things were built the way they were |
| [`../CHANGELOG.md`](../CHANGELOG.md) | Development history — milestones, major architecture changes |

## Core Documents (in `docs/`)

| Document | Description |
|---|---|
| [`GAME_BIBLE.md`](GAME_BIBLE.md) | Complete game design reference — vision, mechanics, all systems |
| [`AI_CONTINUATION_GUIDE.md`](AI_CONTINUATION_GUIDE.md) | Guide for future AI assistants — how to understand and extend this project |
| [`architecture.md`](architecture.md) | Technical architecture — module map, data flow, component diagram |
| [`coding_standards.md`](coding_standards.md) | Code style guide — formatting, naming, patterns, anti-patterns |
| [`known_issues.md`](known_issues.md) | Confirmed bugs and tech debt with severity ratings |
| [`roadmap.md`](roadmap.md) | Development priorities and future expansion directions |
| [`dependencies.md`](dependencies.md) | Runtime dependencies and package inventory |

---

## System Documentation (`systems/`)

| Document | Systems Covered |
|---|---|
| [`systems/world_state.md`](systems/world_state.md) | `world_state.py` — central state schema, all sections, helper functions |
| [`systems/combat.md`](systems/combat.md) | `combat.py`, `enemy_manager.py`, `bosses.py`, `status_effects.py`, `encounter_manager.py` |
| [`systems/ai_director.md`](systems/ai_director.md) | `dm_brain.py`, `llm_bridge.py`, `narrative_ai.py`, `story.py`, `story_manager.py`, `memory_engine.py` |
| [`systems/save_system.md`](systems/save_system.md) | `save_manager.py`, `state_manager.py` — both save systems, migration |
| [`systems/event_bus.md`](systems/event_bus.md) | `event_bus.py` — all events, subscribers, emit rules |
| [`systems/quests.md`](systems/quests.md) | `quests.py`, `quest_manager.py`, `quest_generator.py` |
| [`systems/factions_economy.md`](systems/factions_economy.md) | `faction_manager.py`, `economy_manager.py` |
| [`systems/progression_skills.md`](systems/progression_skills.md) | `progression_manager.py`, `skill_tree.py`, `skills.py` |
| [`systems/inventory_equipment.md`](systems/inventory_equipment.md) | `inventory.py`, `equipment_system.py`, `loot_manager.py`, `shop.py` |
| [`systems/npcs_companions.md`](systems/npcs_companions.md) | `npc_manager.py`, `companion_manager.py`, `dialogue_manager.py`, `relationship_manager.py` |
| [`systems/world_regions.md`](systems/world_regions.md) | `region_manager.py`, `travel_manager.py`, `settlement_manager.py`, `dungeon_manager.py`, `world_event_manager.py` |

---

## Documentation Conventions

### Status Markers Used in These Docs

| Marker | Meaning |
|---|---|
| ⚠️ **NOT YET DEFINED** | Feature is a placeholder only — do not build on it without confirmation |
| **[CONFIRMED]** | Implemented and working in code |
| **[INFERRED]** | Derived from reading code; likely intent but not explicitly stated |
| **[FUTURE]** | Possible direction only — not committed, not canon |

### Canon Rule

> **If it is in the code, it is real. If it is not in the code, it is not canon.**

Never document speculative content as confirmed design. Never invent lore, mechanics, or characters not present in the codebase. Use the ⚠️ **NOT YET DEFINED** marker for all open areas.

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Full documentation suite created from codebase analysis (Phases 1–5) |
