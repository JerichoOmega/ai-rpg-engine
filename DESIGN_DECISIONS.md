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

## Decision 011 — Stylized 3D Tactical RPG as Long-Term Direction

**Decision:** The game's long-term design direction is officially a **Stylized 3D Tactical RPG** with a fixed isometric camera. The previous sprite-based / gacha-inspired direction is no longer the primary foundation.

**Reason:** Explicit creative direction decision from the project owner. Documented as an intentional evolution rather than a contradiction.

**What Changes:**
- Art direction now has confirmed principles: stylized fantasy, strong silhouettes, readable environments, expressive animations, gameplay clarity over realism
- Camera: fixed (or mostly fixed) isometric, prioritizing tactical readability
- Photorealism is explicitly NOT a design goal

**What Stays the Same:**
- The current Python terminal prototype remains the active implementation
- All existing systems (combat, quests, factions, economy, AI Director) carry forward
- The terminal engine's architecture is the foundation the 3D game grows from

**Current Status:** [CONFIRMED — design direction]. Implementation is still the Python terminal prototype.

**Trade-offs:**
- ✅ Clear creative vision; art decisions can now be made with direction
- ❌ Gap between current implementation (text) and target (3D) is significant; bridging it is a major future milestone

---

## Decision 012 — World Scope: One Continent, Open Outward

**Decision:** The playable game takes place on one continent. The existence of additional continents or civilizations is intentionally undefined. World-building grows outward from the playable continent as it becomes relevant.

**Reason:** Avoids over-defining a world before it matters to players. Keeps the setting open for natural expansion across future games or stories without contradiction.

**Alternatives Considered:**
- Defining a full world map up front — rejected; creates canon debt before it is needed
- Leaving world scope entirely undefined — rejected; one-continent scope gives contributors a useful constraint

**Trade-offs:**
- ✅ World can expand naturally; no risk of contradicting future creative directions
- ❌ Contributors cannot reference "other continents" without explicit approval

**Current Status:** [CONFIRMED — design direction]

**Rule:** Do not invent continents, civilizations, or geography beyond the single playable continent without explicit instruction.

---

## Decision 013 — Elyndor as a Standalone Universe (Separate from Any Game)

**Decision:** The fantasy world is named **Elyndor** and exists as a standalone universe, independent of any single game. Universe-level lore is maintained in `elyndor/` and is strictly separated from game-specific documentation in `docs/`.

**Reason:** Future games, books, comics, or other media may all take place within Elyndor. Mixing universe lore with game-specific content would make reuse across projects difficult and risk game-specific decisions overwriting universal canon.

**Alternatives Considered:**
- Single documentation system covering both universe and game — rejected; impossible to reuse cleanly across multiple projects
- Universe lore inside `docs/GAME_BIBLE.md` — rejected; conflates the universe with one game's story

**Trade-offs:**
- ✅ Clean separation; universe lore is reusable; game docs can change without affecting world canon
- ❌ Two systems to maintain; contributors must know which system to place content in

**Rule:** Ancient Legends, world overview, bestiary, magic, and history → `elyndor/`. Playable characters, quests, mechanics, classes → `docs/`.

**Current Status:** [CONFIRMED] — two-system structure established.

---

## Decision 014 — Character Category Separation (Legends vs. Playable Cast)

**Decision:** Characters belong in one of two strictly separate groups: **Ancient Legends** (mythological/historical figures from Elyndor's past, in `elyndor/ancient_legends/`) and **Present-Day Characters** (the playable cast and companions, in `docs/characters/`).

**Reason:** Ancient Legends are part of the world's mythology — they belong to Elyndor as a universe, not to any one game. Playable characters are game-specific. Mixing them creates confusion about who is canon in the world vs. who is playable in the current game.

**Confirmed Legends:** Aurelia Sunstrider, Valen Ashfall  
**Confirmed Playable Cast:** Talos, Eleanor, Ragash, Ronan, Steven

**Rule:** An Ancient Legend does not become a playable character unless a future story explicitly establishes that connection. Do not assume or infer.

**Current Status:** [CONFIRMED]

---

## Decision 015 — Previous Gacha/Sprite Direction Archived

**Decision:** The previous sprite-based / gacha-inspired direction is no longer the primary foundation of this project. Documents and concepts from that era are treated as archived historical material.

**What This Means:**
- Individual gameplay mechanics, classes, monsters, or character ideas from the previous direction may be reused if they fit naturally into the new direction
- The previous story, lore, and world are not considered active canon
- No documents from the old direction should be treated as authoritative without explicit confirmation

**Current Status:** [CONFIRMED] — archived. Refer to new direction documents for all canon decisions.

---

## Decision 016 — Predefined Hero Roster for Phase 1; Custom Hero Deferred to Phase 2

**Decision:** The initial version of the game uses a roster of **predefined, story-driven heroes**. Players select one hero before starting a campaign. A fully customizable Custom Hero system is explicitly deferred to Phase 2 and is out of scope for the current build.

**Source document:** [`docs/PLAYER_SYSTEM.md`](docs/PLAYER_SYSTEM.md)

**Phase 1 — Predefined Hero Roster (current scope):**

Five confirmed playable heroes, each with a unique identity, backstory, class, equipment loadout, and authored story dialogue:

| Hero | Race | Class |
|---|---|---|
| Talos | Elf | Knight |
| Eleanor | Human | Mage |
| Ragash | Orc | Houndmaster |
| Ronan | Human | Werewolf |
| Torren | Human | Master Blacksmith |

**Phase 2 — Custom Hero System (future; not designed):**
- Character name, appearance, class, and background selection
- No UI, screens, or code for this system should be built in Phase 1

**Reason:** Predefined heroes enable deep companion interactions, meaningful story integration, authored dialogue, and polished per-hero writing. A custom character system would require content to accommodate an unknown identity — significantly increasing content scope and reducing narrative depth for Phase 1.

**Alternatives Considered:**
- Custom hero from the start — rejected; too broad a content surface before core systems are stable; narrative depth suffers
- Hybrid (pick class + predefined identity) — not adopted; predefined heroes are preferred for Phase 1 story integration

**Trade-offs:**
- ✅ Deeper story integration per hero; polished writing; companion dialogue can reference the hero's known history
- ✅ Smaller scope for Phase 1; each hero's combat kit can be designed as a coherent whole
- ❌ Players cannot project their own character onto the protagonist in Phase 1
- ❌ Adds Phase 2 migration burden if Custom Hero requires different code paths

**Architecture Requirement:**
The hero framework must support both predefined and custom heroes **without a major rewrite** when Phase 2 arrives. In practice:
- Do not hardcode hero name, class, or backstory as constants
- Store hero identity in data (`world_state` or a hero config dict), not inline strings
- Keep class selection, stat initialization, and equipment loadout data-driven
- A custom hero must eventually be loadable through the same code path as a predefined hero

**Rule:** Do not write code that assumes every playable character is always predefined. Do not begin Custom Hero UI or character-creation flows until Phase 2 is explicitly scoped.

**Current Status:** [CONFIRMED — design direction] Phase 1 predefined roster is active. Phase 2 is deferred with no design yet.

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial document created from codebase analysis |
| July 2026 | Decision 016 added — Predefined Hero Roster (Phase 1) and Custom Hero deferral (Phase 2) |
