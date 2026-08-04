# PROJECT_STATE.md

> **This is the first document every future AI or developer should read.**  
> It answers the question: *"Where is this project right now?"*  
> Last updated: 2026-07-31.

---

## Current Version

**v0.4 — Integration Complete / Documentation Complete**

Semantic versioning is not yet formally adopted. This version tag reflects the current development milestone.

---

## Current Completion %

| Area | % Complete | Notes |
|---|---|---|
| Core engine (loop, state, events) | 95% | Dual player-state eliminated; `world_state` is sole authority; hero items and new-game reset fixed |
| Combat system | 75% | Terminal prototype functional; canonical 3D tactical design (grid, AP, facing, downed) documented in `docs/COMBAT_SYSTEM.md` — not yet implemented |
| Quest system | 65% | CRUD complete; faction bonus wiring is present but never fires (missing `type` field) |
| Progression / levelling | 60% | XP and level-up logic works; skill tree scaffolded; canonical design (level 25 cap, shared XP, companion scaling) documented — not yet implemented |
| Faction system | 55% | Reputation tracking works; `rebels` faction is in state but absent from manager |
| Economy system | 50% | Price evolution logic exists; shop buy/sell exists; deeper trade loops incomplete |
| NPC / companion system | 50% | Named NPC (Elandor) confirmed; companion combat present; NPC changes not persisted |
| World / travel / regions | 45% | Region travel works; dual discovery state inconsistency; dungeons and settlements present |
| Save system | 80% | Two save systems; migration guard added; JSON saves with backfill |
| AI Director / DM Brain | 40% | Pressure-pacing logic works; all LLM calls are mocked; real model not connected |
| Story / narrative | 40% | Story manager, memory engine, narrative AI all present; output is procedural/mock |
| Inventory / equipment | 80% | Canonical path established; equipment slots work; loot rarity works |
| UI / menus | 30% | Terminal-only; hub.py and world_map.py exist but are not integrated |
| Documentation | 95% | All major documents written; revision/update cadence not yet established |
| **Overall** | **~63%** | Engine stabilized; major lore Bible expansion completed |

---

## Last Updated

2026-07-31 — Engine stabilization (dual player-state eliminated; hero items; new-game reset); major lore Bible expansion (Four Ages framework, First Empire, Great Library Director, Soleth Archive, Capital dynasty).

---

## Overall Project Health

🟡 **Stable with Known Issues**

- The game engine starts, runs, saves, and loads correctly.
- All 55 Python files pass syntax checks.
- All 31 engine modules import without errors.
- 12 known issues remain (see [`docs/known_issues.md`](docs/known_issues.md)); none are currently crashers.
- The `player.py` / `world_state["player"]` desync was fixed this session — combat now immediately echoes HP mutations to both representations; `world_state["player"]` is the persistence authority; see 2026-07-31 handoff for synchronization boundary details.

---

## Completed Features

- [x] Central world state (`world_state.py`) with 11 sections and helper functions
- [x] Main game loop with command dispatch
- [x] Event bus with all core events registered and handled
- [x] Turn-based combat with player stats, enemies, status effects
- [x] Boss system with escalating encounters
- [x] Companion combat support
- [x] Quest CRUD (create, activate, complete, fail)
- [x] Faction reputation tracking with threshold events
- [x] Economy evolution (price drift over time)
- [x] Loot system with rarity tiers
- [x] Shop system (buy/sell)
- [x] Equipment slots (weapon, armor, accessory)
- [x] Inventory management in canonical world_state path
- [x] Save/load (JSON file) with state migration guard
- [x] Auto-save (state_manager) alongside manual save (save_manager)
- [x] XP system and level-up check
- [x] Skill tree scaffold
- [x] Region travel with encounter rolls
- [x] Settlement and dungeon managers
- [x] World event system
- [x] NPC system with named NPC (Elandor [CONFIRMED])
- [x] Companion system (join/leave/follow)
- [x] Dialogue system with skill checks
- [x] Relationship manager (reputation per NPC)
- [x] DM Brain pacing (story pressure → narrative focus)
- [x] Story manager with memory engine
- [x] Narrative AI (procedural text, mock LLM)
- [x] LLM bridge (isolated mock; ready for real model swap)
- [x] Campaign manager
- [x] Consistency engine (world state validator)
- [x] Region manager with `show_regions()` wrapper

---

## Partially Completed Features

| Feature | What Works | What's Missing |
|---|---|---|
| Skill tree | Data structure and scaffold present | Active skills have no in-game effect |
| AI Director | Pressure logic, pacing, mock narration | Real LLM not connected |
| Quest faction bonus | Handler wired, event emitted | `type` field absent from all quest_database entries — bonus never fires |
| Faction: rebels | Present in `world_state["factions"]` | Absent from `faction_manager.FACTIONS`; skipped by evolve/show |
| Hub (`hub.py`) | Module exists | Not called from game loop |
| World map (`world_map.py`) | Module exists (static) | Not interactive; not integrated |
| NPC persistence | NPC state in memory | `npc_manager.NPCS` changes not written to save |
| State validation | `validate_world_state()` exists | Checks for `world_state["npcs"]` key that is never initialized — fails on new game |

---

## Missing Features

- **Hero selection screen** — the player character philosophy (Phase 1: predefined roster) is documented and canonical; the in-game selection UI at new-game-start is not yet implemented
- Real LLM integration (all calls are mocked)
- Crafting system — ⚠️ **NOT YET DEFINED** anywhere in the codebase
- Sound / audio — ⚠️ **NOT YET DEFINED** (terminal game; no audio layer)
- Visual art / sprites — ⚠️ **NOT YET DEFINED** (terminal game; no visual layer)
- Multiplayer — ⚠️ **NOT YET DEFINED**
- Proper testing framework (no pytest suite; syntax checks only)
- Formal versioning / release process
- Full lore (world name, history, mythology) — ⚠️ **NOT YET DEFINED**
- **Custom Hero system** — 🔵 **PLANNED FUTURE PHASE ONLY** — character name, appearance, class, background customization. Intentionally out of scope for v1. Architecture must support it later without major rewrite. See [`docs/PLAYER_SYSTEM.md`](docs/PLAYER_SYSTEM.md).

---

## Highest Priority Tasks

1. **Fix `validate_world_state()`** — add `"npcs"` key initialization in `ensure_world_state_defaults()` to resolve validation failure on new games. (🔴 severity)
2. **Add `rebels` to `faction_manager.FACTIONS`** — or remove it from world_state if it is not a real faction. (🟠 severity)
3. **Add `type` field to quest_database entries** — so the faction +10 bonus handler fires as designed. (🟡 severity)
4. **Connect real LLM** — swap mock functions in `llm_bridge.py` with real API calls.
5. **Define Voss's order (Task #122)** — structural load-bearer for Talos's personal quest arc; needed before Capital Province content can be run.

*Full list with severity ratings: [`docs/known_issues.md`](docs/known_issues.md)*

---

## Current Bugs

| ID | Severity | Summary |
|---|---|---|
| BUG-001 | 🔴 | `validate_world_state()` fails on new game — `npcs` key never initialized |
| BUG-002 | ✅ RESOLVED | Player stat desync — fixed 2026-07-31; combat now immediately echoes HP mutations to `world_state["player"]["hp"]`; `world_state` is persistence authority; `Player` object drives runtime with immediate mirroring |
| BUG-003 | 🟠 | `rebels` faction in state but absent from manager |
| BUG-004 | 🟡 | Dual region discovery state (two separate tracking locations) |
| BUG-005 | 🟡 | Quest `type` field absent — faction bonus never fires |
| BUG-006 | 🟡 | NPC changes lost on save (not written to save file) |

*Full list: [`docs/known_issues.md`](docs/known_issues.md)*

---

## Technical Debt

| Item | Impact |
|---|---|
| Legacy modules (`factions.py`, `regions.py`, `loot.py`, `memory.py`) coexist with manager equivalents | Confusing; dead code risk; import ambiguity |
| ~~`player.py` / `world_state["player"]` desync risk~~ | ✅ Resolved 2026-07-31 — combat immediately echoes HP mutations; `sync_world_state_from_player()` called before every save; synchronization boundaries documented in 2026-07-31 handoff |
| No formal test suite | Regressions caught manually only |
| `world_social_reaction()` is dead code in `faction_manager.py` | Noise |
| `hub.py` and `world_map.py` unintegrated | Modules with no callers |
| LLM bridge entirely mocked | No real AI narration |

---

## Architecture Status

✅ **Stable.** Central-state + event-bus pattern is clean and consistent.  
All import errors from the Task 3 integration pass have been resolved.  
All 31 modules import without error.  
See [`docs/architecture.md`](docs/architecture.md) for the full component map.

---

## UI Status

🟡 **Terminal-only. Minimal.** The game runs entirely in a Python terminal. There is no GUI, no web frontend integrated with the game, and no visual art layer. `hub.py` exists as a potential hub-screen module but is not called. `world_map.py` is static. A separate Flask app (`app.py`) exists but is unrelated to the game engine.

---

## Gameplay Status

🟡 **Playable core. Content-sparse.** A player can start the game, explore, enter combat, complete quests, and save progress. Content (quests, enemies, lore, events) is minimal. No crafting. Skill tree is inactive.

---

## Art Status

⚠️ **NOT APPLICABLE.** Terminal game. No visual art assets.

---

## Audio Status

⚠️ **NOT APPLICABLE.** Terminal game. No audio assets.

---

## Database Status

✅ **No external database.** State is persisted as JSON files on disk. No SQL, no cloud DB.

---

## Networking Status

⚠️ **NOT DEFINED.** No networking layer. Single-player only.

---

## Performance Status

🟢 **No concerns.** The game runs entirely in a Python terminal with in-memory state. No performance bottlenecks have been identified.

---

## Recommended Next Steps

**Immediate (fix before adding features):**
1. Fix `ensure_world_state_defaults()` — add `"npcs": {}` initialization
2. Add `type` field to quest_database entries
3. Add `rebels` to `faction_manager.FACTIONS` dict

**Short term (system completion):**
4. Unify region discovery state
5. Persist NPC changes in save
6. Remove or archive legacy root modules (`factions.py`, `regions.py`, `loot.py`, `memory.py`)

**Lore (highest-value open items):**
7. Define the order Voss gave Talos (Task #122) — prerequisite for Capital Province personal quest arc
8. Author the Soleth Accounting's specific contents (Task #120) — prerequisite for Great Library endgame revelation scene
9. Define vampire house player entry points (Task #81) — prerequisite for all three house questlines

**Medium term (features):**
8. Implement hero selection screen at new game start (roster UI, hero confirmation, stat/equipment initialization by hero)
9. Connect real LLM to `llm_bridge.py`
10. Integrate `hub.py` into game loop
11. Activate skill tree effects in combat

**Long term:**
11. Establish pytest suite covering core systems
12. Define crafting system
13. Write world lore (name, history, factions background)

---

## Recently Completed Work

- **Gold-Standard Encounter "The Sundered Span" (2026-06):** The single
  hand-built reference battle demonstrating every canonical combat pillar at
  once — the benchmark for all future encounter design. `tactical/showcase.py`
  (4 heroes with potions vs 5 distinct goblin AI archetypes on a ravine-bridge
  ambush with high ground, cover, a chokepoint + ford, and an oil/barrel
  hazard). Thesis verified: button-mashing loses (naive AI 0/30), competent
  tactics win (~77%), decisive in ~13 rounds. Play: `python scripts/play_showcase.py`;
  demo: `python scripts/showcase_report.py`. Tests
  `backend/tests/test_showcase_encounter.py` 19/19; full backend 216/216;
  independent testing-agent `test_reports/iteration_9.json` 100%. Reference doc:
  [`docs/design/encounters/gold_standard_sundered_span.md`](docs/design/encounters/gold_standard_sundered_span.md).

- **Combat Phase C — Canonical Ability Pipeline (2026-06):** The tactical
  combat engine is now **feature-complete**. Abilities are first-class actions
  on the single canonical `tactical/` pipeline: one authoritative
  `ability_preview()` API (AP/cooldown/range/LOS/legal-target/AoE/expected
  effect/failure reason), data-driven cooldowns (`unit.cooldowns`, ticked in
  `start_of_turn`, save/load compatible), and profile-driven AI ability usage
  (Commander rally, Support heal, Necromancer summon, Caster control) with no
  enemy-specific code. Harness `python -m tactical.verify` 62/62 PASS 0 WARN
  (last Skill/Item WARN eliminated); backend suite 175 passed; independent
  testing-agent 100% (`test_reports/iteration_8.json`). See
  [`docs/systems/tactical_abilities.md`](docs/systems/tactical_abilities.md)
  and [`docs/verification/phaseC_ability_pipeline.md`](docs/verification/phaseC_ability_pipeline.md).
  **Next:** one polished vertical-slice showcase encounter (not Phase B yet).

- **Legacy Questline Architecture (2026-06-15):** New reusable `legacy/` package delivering the three approved Legacy Questlines (The Debt Comes Due, What the Forest Carries, Eternal Forge) as data-driven content on 13 reusable frameworks (quest runner, dialogue trees, speech checks, companion affinity + banter, split party, timed objectives, multi-stage/ritual encounters, environmental puzzles, living world, reputation, civilization relationships, consequences). Wired into `game_loop.py` (menu option 11) and `world_state["legacy"]` with save migration. Automated harness passes 6/6. See [`docs/handoffs/2026-06-15-legacy-questline-integration.md`](docs/handoffs/2026-06-15-legacy-questline-integration.md), [`docs/systems/legacy_quest_framework.md`](docs/systems/legacy_quest_framework.md), and [`legacy/README.md`](legacy/README.md).
- **Engine stabilization (2026-07-31):** Eliminated dual player-state (`world_state` is now sole authority); fixed hero starting items and equipment; fixed new-game reset (progression, equipment, skills); fixed level-up stat persistence; fixed `equipped_weapon`/`weapon_bonus` sync
- **Lore Bible expansion (2026-07-31):** Four Ages canonical framework; First Empire / First Council (`docs/lore/civilization/`); Great Library Director (Maret Cosse); House Soleth Sealed Archive contribution and exchange terms; Capital Province ruling dynasty (House Aldenmoor) and Key Figures (Queen Merveth, Marshal Voss); Ragash and Eleanor hero arc depth; Mossroot first contact scene
- **Full session handoff:** See [`docs/handoffs/2026-07-31-lore-design-session.md`](docs/handoffs/2026-07-31-lore-design-session.md) for complete session record
- **Integration pass (Task 3):** Fixed 8 broken imports, removed duplicate DM brain logic from `llm_bridge.py`, fixed 3 world_state path errors in `story.py`, added save migration guard (`ensure_world_state_defaults()`), fixed quest event payload, fixed faction event handler
- **Documentation suite:** Created 27 documentation files covering game bible, all systems, architecture, known issues, roadmap, governance, AI continuation guide, and handoff system
- **Prior session handoff:** See [`docs/handoffs/2026-07-30-documentation-session.md`](docs/handoffs/2026-07-30-documentation-session.md)

---

## Blocked Work

- **Real LLM integration** — blocked on: API key selection, model choice, cost model decision
- **Crafting system** — blocked on: design (nothing defined yet)
- **World lore** — blocked on: author/designer input (cannot be generated without creative direction)

---

## Development Notes

- **New to this project? Start with [`AI_START_HERE.md`](AI_START_HERE.md)** — the official session startup guide with checklists and reading order.
- The Flask app (`app.py`, `preview.py`, `ui_mockup/`) is a **separate interface prototype** — it does not share code with the terminal game engine. Do not merge them without explicit instruction.
- All terminal game code lives in the root `.py` files and is entered via `main.py`.
- `world_state.py` is the single source of truth for all mutable game state. Always read/write through it.
- The event bus is the correct communication channel between modules. Do not import and call modules directly from each other outside their established relationships.
- Read [`docs/AI_CONTINUATION_GUIDE.md`](docs/AI_CONTINUATION_GUIDE.md) before making any changes to the engine.
