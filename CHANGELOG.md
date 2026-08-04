# CHANGELOG

> Organized by development milestones.  
> Dates are approximate — derived from commit history and development notes.  
> Status: **[CONFIRMED]** = verified in code · **[INFERRED]** = derived from code analysis  
> Last updated: July 2026.

---

## [v0.5.1] — June 2026 — Legacy Framework Production Hardening [CONFIRMED]

Hardened the Legacy Quest Framework for long-term production (no new quests,
no canon changes, save-compatible, existing APIs preserved).

- **Audit:** every framework confirmed reusable and quest-type agnostic (`docs/systems/legacy_framework_audit.md`).
- **Dev tools:** expanded `legacy/dev_tools.py` (stage jump, complete/fail objective, fail quest, set stage, reputation/standing/relationship, force world update, spawn NPC, skip cinematic, export quest state, simulate speech, seat party).
- **Authoring toolkit:** `docs/systems/legacy_quest_authoring.md` — full JSON schema + worked examples for every step type.
- **Living World reactions:** `legacy/framework/living_world_reactions.py` + `legacy/data/living_world_reactions.json` — idempotent, data-driven reaction layer (merchant inventory/pricing, NPC schedules, patrols, refugee movement, ambient dialogue, tavern rumors, prosperity, road safety, regional reputation) with a query API.
- **Validator:** `legacy/validator.py` — static+dynamic quest-flow validation (0 errors/0 warnings across all three quests).
- **Additive APIs:** `QuestManager.complete_objective/fail_objective/fail_quest/set_stage/export_state`.
- **Verification:** harness 6/6, validator clean, independent testing-agent pass (100%, 0 issues).

---

## [v0.5] — June 2026 — Legacy Questline Architecture [CONFIRMED]

### Reusable, data-driven quest architecture (`legacy/` package)

Delivered the production-quality quest architecture as the vertical slice
implementing three approved Legacy Questlines: **The Debt Comes Due**,
**What the Forest Carries**, and **Eternal Forge**. Quests are authored as
JSON data and executed by a generic step-runner — a future questline needs a
data file and a two-line registration, no engine code.

**Reusable frameworks added (`legacy/framework/`):**
- Quest Framework (`quest_framework.py`) — Quest/Stage/step-runner/QuestManager
- Living World State Manager (`world_flags.py`)
- Reputation hooks + Civilization Relationship Tracking (`reputation.py`)
- Companion Affinity Hooks + Insight Gates + Banter (`companion_affinity.py`)
- Speech Check Framework — 5 skills (`speech_checks.py`)
- Dialogue Tree Framework (`dialogue_trees.py`)
- Environmental Puzzle Framework (`puzzles.py`)
- Timed Objective Framework (`timed_objectives.py`)
- Multi-Stage Combat Encounters (`encounters.py`)
- Split Party Framework (`split_party.py`)
- Quest Consequence Framework (`consequences.py`)
- IOAdapter (`io.py`) — Interactive/Scripted transports; registry (`registry.py`)

**Content + tooling:**
- `legacy/data/*.json` — the three quests (design authority)
- `legacy/quests/*.py` — thin loaders + banter
- `legacy/dev_tools.py` — permanent developer utilities
- `legacy/harness.py` — automated regression (6/6 scenarios pass)
- `legacy/menu.py` — in-game menu

**Engine integration:**
- `world_state.py` — added `world_state["legacy"]` namespace + save migration in `ensure_world_state_defaults()`
- `game_loop.py` — main-menu option 11 "Legacy Questlines" (Exit → 12)
- ~20 new event-bus events emitted by the frameworks

**Docs:** `docs/systems/legacy_quest_framework.md`, `legacy/README.md`
(deliverables report), `docs/handoffs/2026-06-15-legacy-questline-integration.md`.

---

## [v0.4] — July 2026 — Integration Complete + Documentation Complete

### Integration Pass (Task 3) — All import errors and state inconsistencies resolved

**Import fixes:**
- `travel_manager.py` — corrected import from non-existent `encounter_generator` → `encounter_manager`
- `equipment_system.py` — removed broken `from inventory import inventory`; wired to `world_state["player"]["inventory"]`
- `save_manager.py` — removed broken inventory import; all 3 usages wired to `world_state["player"]["inventory"]`
- `loot_manager.py` — fixed `add_item` import source from `inventory` → `world_state`
- `game_loop.py` — corrected `update_economy` → `evolve_economy`; aliased `show_all_settlements`; removed dead `world_social_reaction` import
- `region_manager.py` — added missing `show_regions()` wrapper; removed dead `discover_lore` import
- `npc_manager.py` — removed unused world_state object import
- `quests.py` — removed unused `fail_quest` import

**Duplicate DM brain logic removed:**
- `llm_bridge.py` — fully rewritten; stripped private state (`dm_state`, `change_story_pressure`, `evaluate_story_state`, `update_dm_brain`), event subscribers, and circular self-imports; now exports only four clean mock functions: `ai_narrate`, `ai_generate_quest`, `ai_combat_narration`, `ai_dialogue`

**State consistency fixes:**
- `story.py` — fixed 3× `world_state["world_chaos"]` flat reads → `world_state["world_conditions"]["world_chaos"]` (canonical nested path)
- `story.py` — converted 5× hard `story_memory["key"]` reads to `.get()` for safety
- `story.py` — converted 3× hard `factions["key"]` reads to `.get(key, 0)` for safety
- `quests.py` — `quest_completed` event emit now includes `quest=quest_data` dict for faction handler
- `faction_manager.py` — `on_quest_completed` handler rewritten to use `event_data.get("quest") or {}`

**Save migration added:**
- `world_state.py` — added `ensure_world_state_defaults()` function; backfills 16+ keys/sections
- `save_manager.py` — calls `ensure_world_state_defaults()` immediately after load
- `state_manager.py` — calls `ensure_world_state_defaults()` immediately after load

**Documentation suite created (Phase 4–9):**
- `docs/README.md` — master index
- `docs/GAME_BIBLE.md` — 33-section game design reference (~700 lines)
- `docs/AI_CONTINUATION_GUIDE.md` — AI assistant continuation guide
- `docs/architecture.md` — technical architecture and component diagram
- `docs/coding_standards.md` — code style guide with examples
- `docs/known_issues.md` — 12 issues with severity ratings
- `docs/roadmap.md` — prioritized development plan
- `docs/dependencies.md` — runtime package inventory
- `docs/systems/` — 11 per-system deep-dive documents
- `PROJECT_STATE.md` — project health snapshot
- `PROJECT_MEMORY.md` — AI quick-start guide
- `DESIGN_DECISIONS.md` — architectural decision record
- `CHANGELOG.md` — this file

**Verification results:**
- 55/55 Python files pass syntax check
- 31/31 engine modules import without error

---

## [v0.3] — Prior to July 2026 — World State Refactor [INFERRED]

> *This milestone is reconstructed from code analysis. Exact date unknown.*

### Central state centralization

- `world_state.py` established as the single source of truth for all game state
- All major game state migrated from per-module variables into the `world_state` dict
- `world_state` structured into 11 named sections: `player`, `world_conditions`, `regions`, `factions`, `economy`, `quests`, `npcs`, `companions`, `story_memory`, `dm_state`, `crafting_recipes`
- Helper functions added: `get_player_stat`, `update_player_stat`, `add_item`, `remove_item`, `has_item`, `add_experience`, `update_faction_reputation`

### Event bus introduction

- `event_bus.py` introduced as cross-module communication layer
- Core events registered: `player_died`, `level_up`, `quest_completed`, `quest_failed`, `item_acquired`, `faction_reputation_changed`, `combat_started`, `combat_ended`, `settlement_discovered`, `dungeon_entered`, `world_event_triggered`, `npc_interaction`, `day_passed`

### Save system extension

- `state_manager.py` added alongside `save_manager.py` for auto-save capability
- Both systems write JSON to disk

---

## [v0.2] — Prior to World State Refactor — AI Director Merge [INFERRED]

> *This milestone is reconstructed from code analysis. Exact date unknown.*

### AI Director integration

- `dm_brain.py` introduced — narrative pacing and story pressure system
- `llm_bridge.py` introduced as abstraction for LLM calls (mock implementations)
- `narrative_ai.py` introduced — procedural text generation
- `story.py` and `story_manager.py` introduced — story arc and memory management
- `memory_engine.py` introduced — long-term story memory
- `campaign_manager.py` introduced — campaign-level progression

### Note on integration issues

During the v0.2 → v0.3 transition, `llm_bridge.py` accumulated duplicate DM brain logic (private `dm_state`, event subscribers, circular imports). This was fully resolved in the v0.4 integration pass.

---

## [v0.1] — Initial Development [INFERRED]

> *This milestone is reconstructed from code analysis. Exact date unknown.*

### Foundation systems

- `main.py` + `game_loop.py` — core game loop and command dispatch
- `player.py` — player character singleton
- `combat.py` — turn-based combat system
- `enemy_manager.py` — enemy definitions
- `quests.py` — quest CRUD
- `factions.py` — initial faction system (later superseded by `faction_manager.py`)
- `regions.py` — initial region system (later superseded by `region_manager.py`)
- `inventory.py` — initial inventory (later superseded by `world_state["player"]["inventory"]`)
- `loot.py` — initial loot (later superseded by `loot_manager.py`)
- `memory.py` — initial memory (later superseded by `memory_engine.py`)
- `save_manager.py` — original JSON save/load
- `shop.py` — buy/sell economy
- `equipment_system.py` — equipment slots

### Legacy modules

`factions.py`, `regions.py`, `loot.py`, and `memory.py` remain in the root directory from this milestone. They were not deleted during subsequent refactors. See [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) Decision 009.

---

## Planned Future Milestones

| Milestone | Target Features |
|---|---|
| v0.5 | Fix all 🔴/🟠 known issues; activate skill tree; real LLM connection |
| v0.6 | Crafting system; hub.py integration; lore writing |
| v1.0 | Content-complete alpha; full quest content; balanced economy |

*Full roadmap: [`docs/roadmap.md`](docs/roadmap.md)*

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial changelog created; all milestones reconstructed from codebase analysis |
