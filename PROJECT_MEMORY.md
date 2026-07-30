# PROJECT_MEMORY.md

> **AI Quick-Start Guide.**  
> Read this in under five minutes to understand the entire project.  
> Then read `PROJECT_STATE.md` to know exactly where it stands.  
> Last updated: July 2026.

---

## What This Project Is

A **terminal-based AI RPG** written in Python. The player types commands in a terminal. An AI Director (the "DM Brain") shapes the narrative pacing and story. The game features combat, quests, factions, economy, companions, exploration, and a save system — all running in a single Python process with no external dependencies.

**Entry point:** `main.py` → `game_loop.py`  
**Central state:** `world_state.py` (a single global dict, always the truth)  
**Communication:** `event_bus.py` (publish/subscribe pattern)

---

## Architecture in 60 Seconds

```
main.py
  └─ game_loop.py          ← command parser + turn dispatcher
       ├─ world_state.py   ← ALL mutable state lives here (dict)
       ├─ event_bus.py     ← modules talk via events, not direct imports
       ├─ combat.py        ← turn-based combat
       ├─ dm_brain.py      ← AI Director: pacing, pressure, story focus
       ├─ llm_bridge.py    ← LLM abstraction layer (currently mocked)
       ├─ quests.py        ← quest CRUD and lifecycle
       ├─ faction_manager.py ← reputation, faction events
       ├─ save_manager.py  ← JSON file save/load
       └─ [28 more modules]
```

Modules communicate through `event_bus.py` using `emit(event_name, data)` and `subscribe(event_name, handler)`. Direct cross-module function calls are used for returns only, not for triggering side effects.

The Flask app (`app.py`, `preview.py`, `ui_mockup/`) is a **separate** browser-based interface prototype. It does not share code with the terminal game.

---

## The Most Important Rule

> **`world_state.py` is the single source of truth.**

Every piece of mutable game state — player stats, inventory, factions, regions, quests, time, everything — lives in the `world_state` dict. Never store game state in module-level variables. Never shadow it with local copies. Always use `world_state["section"]["key"]`.

Helper functions in `world_state.py`:
- `get_player_stat(stat)` / `update_player_stat(stat, value)`
- `add_item(item)` / `remove_item(item)` / `has_item(item)`
- `add_experience(amount)`
- `update_faction_reputation(faction, delta)`
- `ensure_world_state_defaults()` — **call this after any load/restore**

---

## Major Systems (Where to Find Things)

| What you want to change | Go here |
|---|---|
| Player stats, inventory | `world_state.py` + `player.py` (see note below) |
| Combat mechanics | `combat.py`, `enemy_manager.py`, `bosses.py` |
| Quest logic | `quests.py`, `quest_manager.py`, `quest_generator.py` |
| Faction reputation | `faction_manager.py` |
| Economy prices | `economy_manager.py` |
| Save / load | `save_manager.py`, `state_manager.py` |
| AI narrative pacing | `dm_brain.py` |
| LLM calls | `llm_bridge.py` (swap mocks for real calls here) |
| Story generation | `story.py`, `story_manager.py`, `narrative_ai.py` |
| Events (emit/subscribe) | `event_bus.py` |
| World regions / travel | `region_manager.py`, `travel_manager.py` |
| NPCs / companions | `npc_manager.py`, `companion_manager.py` |
| Dialogue | `dialogue_manager.py` |
| Skills | `skills.py`, `skill_tree.py`, `progression_manager.py` |
| Loot / equipment | `loot_manager.py`, `equipment_system.py` |

---

## Current State Summary

- **~58% complete.** Playable core; content and polish incomplete.
- **Engine is clean.** All 55 files pass syntax. All 31 modules import without error.
- **6 active bugs** (none are crashers right now).
- **Full documentation** lives in `docs/` (19 files).
- **LLM is mocked.** `llm_bridge.py` returns dummy strings. Swap with real calls when ready.

Full status: [`PROJECT_STATE.md`](PROJECT_STATE.md)

---

## Known Limitations — Read Before Touching Anything

| # | Severity | What It Is |
|---|---|---|
| 1 | 🔴 | `validate_world_state()` fails on new game — `npcs` key never initialized |
| 2 | 🟠 | `player.py` singleton vs `world_state["player"]` — can desync after combat |
| 3 | 🟠 | `rebels` faction: in world_state but not in `faction_manager.FACTIONS` |
| 4 | 🟡 | Dual region discovery state (two separate trackers) |
| 5 | 🟡 | Quest `type` field absent — faction +10 bonus never fires |
| 6 | 🟡 | NPC changes not persisted across saves |

**Do not build features that depend on these systems being correct until the bugs are fixed.**

Full issue list: [`docs/known_issues.md`](docs/known_issues.md)

---

## Important Design Decisions

1. **Single global world_state dict** — chosen over per-system state objects for simplicity and serialization ease. Every system reads/writes the same dict.

2. **Event bus for cross-module communication** — modules subscribe to events rather than importing each other. This prevents circular imports and keeps systems decoupled.

3. **LLM bridge isolation** — all LLM calls go through `llm_bridge.py`. Switching models means touching one file only. Currently mocked.

4. **Two save systems** — `save_manager.py` (explicit player save) and `state_manager.py` (auto-save). Both write to JSON. Both call `ensure_world_state_defaults()` on load.

5. **DM Brain is separate from LLM** — `dm_brain.py` handles pacing/pressure logic; `llm_bridge.py` handles text generation. They are intentionally separate.

Full rationale: [`DESIGN_DECISIONS.md`](DESIGN_DECISIONS.md)

---

## Common Mistakes to Avoid

| Mistake | Why It Breaks Things |
|---|---|
| `from inventory import inventory` | `inventory.py` has no list export — use `world_state["player"]["inventory"]` |
| Reading `world_state["world_chaos"]` directly | The key is at `world_state["world_conditions"]["world_chaos"]` |
| Hard-reading `story_memory["key"]` | Use `.get()` — key may not exist yet |
| Writing game state to module-level variables | State is lost on save; always use world_state |
| Calling `update_economy` | The function is `evolve_economy` |
| Adding logic to `llm_bridge.py` | It must stay as a thin bridge only — no game logic |
| Forgetting `ensure_world_state_defaults()` after load | Old saves will be missing keys and crash on access |

---

## Important Files

| File | Why It Matters |
|---|---|
| `main.py` | Entry point |
| `game_loop.py` | Command dispatcher — the hub of all gameplay |
| `world_state.py` | All state; helpers; migration guard |
| `event_bus.py` | All cross-module communication |
| `dm_brain.py` | Pacing and story direction |
| `llm_bridge.py` | Only place to add real LLM calls |
| `save_manager.py` | Manual save/load |
| `docs/AI_CONTINUATION_GUIDE.md` | Read before any refactor |
| `docs/known_issues.md` | Check before touching any system |
| `PROJECT_STATE.md` | Current project health |

---

## Important Folders

| Folder | Contents |
|---|---|
| `/` (root) | All 55 Python game files + config |
| `docs/` | All documentation (19 files) |
| `docs/systems/` | Per-system deep-dives (11 files) |
| `ui_mockup/` | Separate Flask UI prototype — do not mix with game |
| `saves/` | JSON save files (runtime-generated) |

---

## Frequently Modified Systems

Based on the codebase history, these systems change most often and carry the most risk:

1. **`world_state.py`** — any change here affects every system; always add to `ensure_world_state_defaults()` when adding new keys
2. **`game_loop.py`** — command dispatch changes affect all player-facing features
3. **`quests.py`** — quest lifecycle is connected to factions, events, and progression
4. **`dm_brain.py`** — pacing logic is delicate; changing pressure thresholds affects the whole narrative feel
5. **`save_manager.py` / `state_manager.py`** — any save format change requires migration logic

---

## How to Safely Add a New Feature

1. Read the relevant system doc in `docs/systems/`
2. Check `docs/known_issues.md` — does your feature touch a broken system?
3. Store any new state in `world_state.py` — add the key to `ensure_world_state_defaults()`
4. Wire cross-module communication through `event_bus.py`, not direct calls
5. If adding an LLM call, add it to `llm_bridge.py` only
6. Update the relevant `docs/` file after implementing
7. Add the new state key to `docs/systems/world_state.md`

---

## Documentation Map

```
PROJECT_MEMORY.md        ← you are here (AI quick-start)
PROJECT_STATE.md         ← current health, bugs, priorities
DESIGN_DECISIONS.md      ← why things were built the way they were
CHANGELOG.md             ← history of major changes
docs/README.md           ← full docs index
docs/GAME_BIBLE.md       ← what the game is
docs/AI_CONTINUATION_GUIDE.md  ← how to continue development safely
docs/architecture.md     ← how modules connect
docs/coding_standards.md ← how to write code here
docs/known_issues.md     ← what's broken
docs/roadmap.md          ← what's planned
docs/systems/            ← deep dives per system (11 files)
```
