# DESIGN_DECISIONS.md

> Records every important architectural and design decision discovered in the project.  
> Status markers: **[CONFIRMED]** = verified in code · **[INFERRED]** = derived from code patterns · **[PLANNED]** = roadmap only  
> Last updated: July 2026.

---

## Decision 001 — Single Global World State Dict

**Decision:** All mutable game state is stored in a single Python dict (`world_state`) in `world_state.py`, shared across all modules via import.

**Reason:** Simplifies serialization (the entire game state is one JSON-serializable dict), eliminates synchronization complexity between per-system state objects, and makes save/load trivially reliable.

**Alternatives Considered:**
- Per-system state objects (e.g. `CombatState`, `QuestState`) — rejected because serialization requires custom encoders per object and cross-system reads require more imports
- Database-backed state — rejected as over-engineering for a single-player terminal game
- Dataclasses with `__dict__` serialization — considered but not adopted; dict approach was already in place

**Trade-offs:**
- ✅ Simple serialization; easy to inspect saves; no circular dependency from state
- ❌ No type safety; typos in key names fail silently; schema must be maintained manually via `ensure_world_state_defaults()`

**Current Status:** [CONFIRMED] — active and stable. All modules use `world_state`.

**Future Considerations:** If the project grows significantly, consider typed sections (Pydantic models or dataclasses) for individual sections while keeping the top-level dict for serialization. Do not change the access pattern without also updating the migration guard.

---

## Decision 002 — Event Bus for Cross-Module Communication

**Decision:** Modules communicate side-effects through `event_bus.py` using `emit(event_name, data)` / `subscribe(event_name, handler)` rather than direct function imports.

**Reason:** Prevents circular imports (e.g. `combat.py` triggering quest completion without importing `quests.py`), keeps modules decoupled, and makes it easier to add new listeners without modifying the emitter.

**Alternatives Considered:**
- Direct function calls between modules — used in some places for return-value operations but explicitly avoided for side-effects
- Observer pattern via class inheritance — rejected; Python module-level functions are simpler
- Message queue — over-engineering for a synchronous single-player game

**Trade-offs:**
- ✅ Decoupled modules; easy to add new subscribers; no circular import risk
- ❌ Event flow is harder to trace (must search for `subscribe` calls); payloads must be agreed on by sender and receiver informally

**Current Status:** [CONFIRMED] — active. All major cross-system triggers go through the bus.

**Known Issue:** `quest_completed` event must include `quest=quest_data` dict in payload; handlers use `.get("quest", {})` for backward compatibility. See [`docs/systems/event_bus.md`](docs/systems/event_bus.md).

**Future Considerations:** Consider typed event payloads (TypedDict) as the event count grows. Document any new event immediately in `docs/systems/event_bus.md`.

---

## Decision 003 — LLM Bridge Isolation

**Decision:** All LLM/AI text generation calls are routed through `llm_bridge.py` as a thin abstraction layer. No other module calls an LLM directly. Currently all functions are mocked.

**Reason:** Decouples game logic from model selection. Switching from mock to real, or from one model to another, requires changing only `llm_bridge.py`. Prevents LLM API keys, costs, and latency from being scattered through the codebase.

**Alternatives Considered:**
- Direct API calls in `narrative_ai.py` and `dm_brain.py` — rejected; creates tight coupling to a specific provider
- LLM calls inline in `game_loop.py` — rejected; mixes concerns

**Trade-offs:**
- ✅ Single swap point for model integration; game logic never needs to change when models change
- ❌ Adds one layer of indirection; mock functions can mask integration problems until real calls are added

**Current Status:** [CONFIRMED] — mocked. `llm_bridge.py` exports `ai_narrate`, `ai_generate_quest`, `ai_combat_narration`, `ai_dialogue`. All return placeholder strings.

**Future Considerations:** When connecting a real model, implement only these four functions in `llm_bridge.py`. Add error handling and retry logic there. Do not add game logic to this file.

---

## Decision 004 — Two Save Systems

**Decision:** The project has two independent save systems: `save_manager.py` (explicit player-triggered save/load) and `state_manager.py` (auto-save / state persistence).

**Reason:** [INFERRED] — likely grew from different feature implementations at different times. `save_manager.py` was the original explicit save; `state_manager.py` was added for auto-save/checkpoint behaviour.

**Alternatives Considered:**
- Single unified save system — [PLANNED] as a future cleanup
- Cloud saves — ⚠️ NOT YET DEFINED

**Trade-offs:**
- ✅ Auto-save and manual save are independent; failure in one doesn't affect the other
- ❌ Two code paths to maintain; both must call `ensure_world_state_defaults()` on load or migration breaks

**Current Status:** [CONFIRMED] — both systems active. Both call `ensure_world_state_defaults()` after load (fixed in Task 3 integration pass).

**Future Considerations:** Merge into a single `save_system.py` in a future refactor. Until then, any change to save format must be applied to both files and the migration guard must be updated.

---

## Decision 005 — DM Brain Separated from LLM Bridge

**Decision:** `dm_brain.py` handles pacing, pressure scoring, and narrative focus decisions. `llm_bridge.py` handles text generation. They are separate modules with separate responsibilities.

**Reason:** Pacing logic is deterministic game logic (pressure scores, threshold comparisons, focus mappings). Text generation is an AI call. Separating them allows pacing to work even when LLM is mocked, and allows the pacing algorithm to change independently of the text model.

**Alternatives Considered:**
- Single AI module handling both pacing and generation — existed previously (in an earlier version that was merged away); removed during Task 3 integration pass because it created circular imports and duplicate state

**Trade-offs:**
- ✅ Pacing works without a real LLM; clean separation of concerns
- ❌ Two modules to understand when reasoning about AI-driven narrative

**Current Status:** [CONFIRMED] — `dm_brain.py` calls `llm_bridge.py` for text but handles all scoring/pressure internally.

---

## Decision 006 — Terminal-First Interface

**Decision:** The game is a terminal application. All I/O is via Python `print()` and `input()`. No GUI framework is used for the game itself.

**Reason:** Simplicity of implementation; focus on systems and content over UI polish; allows rapid development of game logic without UI overhead.

**Alternatives Considered:**
- Curses/blessed for a richer terminal UI — not adopted; plain terminal is sufficient
- Web-based UI (Flask) — exists as a separate prototype (`app.py`) but is not integrated with game engine
- Pygame / Unity — ⚠️ NOT YET DEFINED as future direction

**Trade-offs:**
- ✅ Zero UI dependencies; highly portable; fast to develop
- ❌ Limited visual feedback; no animations; navigation is entirely text-command-based

**Current Status:** [CONFIRMED] — terminal only. The Flask app (`app.py`) is a prototype, not canon game UI.

---

## Decision 007 — Player State Dual Representation (Open Issue)

**Decision:** Player stats exist in both `player.py` (a singleton object) and `world_state["player"]` (a dict section). This is an **unresolved split** — the decision of which is canonical has not been made.

**Reason:** [INFERRED] — `player.py` was likely the original player representation. `world_state["player"]` was added during the world_state centralization. Neither was fully retired.

**Current Behavior:** Combat reads from `player.py` singleton. Save/load operates on `world_state["player"]`. After levelling or equipping in world_state, the singleton may not reflect the change.

**Recommended Resolution:** Pick one canonical source. Options:
- Make `player.py` a view/proxy over `world_state["player"]` — keeps existing code working, fixes divergence
- Remove `player.py` singleton, port all combat reads to `world_state["player"]` — cleaner long-term but more changes

**Current Status:** 🟠 **UNRESOLVED** — active risk. Do not add new features that read player stats without understanding this split.

See: [`docs/known_issues.md`](docs/known_issues.md) BUG-002.

---

## Decision 008 — State Migration Guard

**Decision:** `world_state.py` includes `ensure_world_state_defaults()`, which backfills all expected keys after loading an old save. This is called by both save systems on load.

**Reason:** As new state sections are added (e.g. `world_conditions`, `crafting_recipes`), old save files will be missing those keys. Rather than versioned migrations, a single function backfills all missing keys with safe defaults.

**Alternatives Considered:**
- Versioned migrations (v1 → v2 → v3 upgrade chain) — more precise but more maintenance burden
- Strict save format enforcement (fail on missing keys) — would break all existing saves

**Trade-offs:**
- ✅ Backward compatible with all existing saves; simple to extend
- ❌ Old saves are silently upgraded; no record of what was migrated; easy to forget adding new keys to the defaults function

**Current Status:** [CONFIRMED] — active. Any new top-level world_state key must be added to `ensure_world_state_defaults()`.

**Rule:** When you add a new key to world_state, you MUST also add it to `ensure_world_state_defaults()` in `world_state.py`.

---

## Decision 009 — Legacy Modules Retained at Root

**Decision:** Older modules (`factions.py`, `regions.py`, `loot.py`, `memory.py`) remain in the root directory alongside their newer `*_manager.py` equivalents. They have not been deleted.

**Reason:** [INFERRED] — retained to avoid breaking potential import paths during refactor; no formal decision to remove them was made.

**Trade-offs:**
- ❌ Ambiguity about which module is canonical; risk of accidentally importing the old version
- ❌ Dead code; maintenance noise

**Recommended Resolution:** Archive or delete the legacy modules. Confirm no remaining code imports them, then remove. Update `docs/architecture.md` afterward.

**Current Status:** 🟡 **DEFERRED** — retained but flagged. Do not import from legacy modules for any new code.

---

## Decision 010 — No External Dependencies for Game Engine

**Decision:** The terminal game uses only Python standard library modules (`json`, `random`, `os`). No pip packages required.

**Reason:** Maximum portability; no dependency management burden; no version conflicts; game runs anywhere Python 3 is installed.

**Trade-offs:**
- ✅ Zero install friction; always works
- ❌ Must implement all utilities manually (no rich terminal libraries, no typed data validation)

**Current Status:** [CONFIRMED] — active. `requirements.txt` may exist for the Flask prototype only.

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial document created from codebase analysis |
