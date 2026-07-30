# PROJECT_STATE.md

> **This is the first document every future AI or developer should read.**  
> It answers the question: *"Where is this project right now?"*  
> Last updated: July 2026.

---

## Current Version

**v0.4 — Integration Complete / Documentation Complete**

Semantic versioning is not yet formally adopted. This version tag reflects the current development milestone.

---

## Current Completion %

| Area | % Complete | Notes |
|---|---|---|
| Core engine (loop, state, events) | 90% | Working; minor gaps noted below |
| Combat system | 75% | Turn-based combat functional; boss system present; balancing incomplete |
| Quest system | 65% | CRUD complete; faction bonus wiring is present but never fires (missing `type` field) |
| Progression / levelling | 60% | XP and level-up logic works; skill tree is scaffolded but not functional |
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
| **Overall** | **~58%** | Playable engine; content and polish incomplete |

---

## Last Updated

July 2026 — Integration pass (Task 3) completed; full documentation suite generated.

---

## Overall Project Health

🟡 **Stable with Known Issues**

- The game engine starts, runs, saves, and loads correctly.
- All 55 Python files pass syntax checks.
- All 31 engine modules import without errors.
- 12 known issues remain (see [`docs/known_issues.md`](docs/known_issues.md)); none are currently crashers.
- The most significant risk is the `player.py` singleton / `world_state["player"]` divergence, which can cause silent stat desync after combat.

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

- Real LLM integration (all calls are mocked)
- Crafting system — ⚠️ **NOT YET DEFINED** anywhere in the codebase
- Sound / audio — ⚠️ **NOT YET DEFINED** (terminal game; no audio layer)
- Visual art / sprites — ⚠️ **NOT YET DEFINED** (terminal game; no visual layer)
- Multiplayer — ⚠️ **NOT YET DEFINED**
- Proper testing framework (no pytest suite; syntax checks only)
- Formal versioning / release process
- Full lore (world name, history, mythology) — ⚠️ **NOT YET DEFINED**

---

## Highest Priority Tasks

1. **Fix `validate_world_state()`** — add `"npcs"` key initialization in `ensure_world_state_defaults()` to resolve validation failure on new games. (🔴 severity)
2. **Resolve player state divergence** — decide canonical source for player stats during combat: `player.py` singleton vs `world_state["player"]`. Document the decision. (🟠 severity)
3. **Add `rebels` to `faction_manager.FACTIONS`** — or remove it from world_state if it is not a real faction. (🟠 severity)
4. **Add `type` field to quest_database entries** — so the faction +10 bonus handler fires as designed. (🟡 severity)
5. **Connect real LLM** — swap mock functions in `llm_bridge.py` with real API calls.

*Full list with severity ratings: [`docs/known_issues.md`](docs/known_issues.md)*

---

## Current Bugs

| ID | Severity | Summary |
|---|---|---|
| BUG-001 | 🔴 | `validate_world_state()` fails on new game — `npcs` key never initialized |
| BUG-002 | 🟠 | Player stat divergence — singleton vs world_state can desync after combat |
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
| `player.py` singleton alongside `world_state["player"]` | Silent divergence risk |
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
4. Resolve `player.py` / `world_state["player"]` divergence — pick one canonical source
5. Unify region discovery state
6. Persist NPC changes in save
7. Remove or archive legacy root modules (`factions.py`, `regions.py`, `loot.py`, `memory.py`)

**Medium term (features):**
8. Connect real LLM to `llm_bridge.py`
9. Integrate `hub.py` into game loop
10. Activate skill tree effects in combat

**Long term:**
11. Establish pytest suite covering core systems
12. Define crafting system
13. Write world lore (name, history, factions background)

---

## Recently Completed Work

- **Integration pass (Task 3):** Fixed 8 broken imports, removed duplicate DM brain logic from `llm_bridge.py`, fixed 3 world_state path errors in `story.py`, added save migration guard (`ensure_world_state_defaults()`), fixed quest event payload, fixed faction event handler
- **Documentation suite (Task 4):** Created 19 documentation files across `docs/` covering all systems, architecture, known issues, roadmap, and AI continuation guide

---

## Blocked Work

- **Real LLM integration** — blocked on: API key selection, model choice, cost model decision
- **Crafting system** — blocked on: design (nothing defined yet)
- **World lore** — blocked on: author/designer input (cannot be generated without creative direction)

---

## Development Notes

- The Flask app (`app.py`, `preview.py`, `ui_mockup/`) is a **separate interface prototype** — it does not share code with the terminal game engine. Do not merge them without explicit instruction.
- All terminal game code lives in the root `.py` files and is entered via `main.py`.
- `world_state.py` is the single source of truth for all mutable game state. Always read/write through it.
- The event bus is the correct communication channel between modules. Do not import and call modules directly from each other outside their established relationships.
- Read [`docs/AI_CONTINUATION_GUIDE.md`](docs/AI_CONTINUATION_GUIDE.md) before making any changes to the engine.
