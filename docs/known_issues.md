# Known Issues & Technical Debt

**Purpose:** Tracks confirmed bugs, architectural inconsistencies, and technical debt items. All entries are based on direct codebase analysis.

**Rule:** Do not fix issues listed here as part of unrelated work. Each item should be addressed intentionally with its own change.

---

## Severity Key

| Level | Meaning |
|---|---|
| 🔴 Critical | Will crash or corrupt data under normal use |
| 🟠 High | Produces incorrect behavior that a player will notice |
| 🟡 Medium | Inconsistency or tech debt that may cause future problems |
| 🟢 Low | Cosmetic, minor inconsistency, or future-proofing concern |

---

## Active Issues

---

### 🟡 TD-001 — Dual region-discovery state (immediate divergence FIXED; consolidate before beta)

**Files:** `region_manager.py` (`REGIONS[name]["discovered"]`), `world_state.py`
(`world_state["regions"]["discovered_regions"]`), `world_map.py`, `travel_manager.py`

**Status (2026-06):** *Immediate divergence FIXED.* `travel_manager.
complete_travel` now calls **both** `region_manager.discover_region` and
`world_state.discover_region`, so the two stores agree across save/load
(verified by `test_phase1_wiring_integration.py`). **Durable consolidation still
pending:** two discovery stores still exist.

**Impact (historical):** travel updated only `REGIONS[name]["discovered"]`; the
serialized `world_state` list lagged, so a loaded save could show the wrong
discovered set on the map.

**Durable fix (before beta):** pick one canonical source — recommended the
serialized `world_state["regions"]["discovered_regions"]` — and make
`region_manager.discover_region` delegate to `world_state.discover_region`; have
`world_map` read from it. Then remove the double-write in `complete_travel`.

**Priority:** before beta. Not blocking Phase 1.

---

### 🔴 `validate_world_state` checks for `npcs` key that does not exist

**File:** `state_manager.py` → `validate_world_state()`  
**Impact:** Save validation fails on new games loaded through `state_manager.load_game()`. The game may refuse to load a perfectly valid new-game state.

**Root cause:** `validate_world_state()` requires `world_state["npcs"]` to be present, but `world_state.py` never initializes this key (there is no `npcs` section in the schema).

**Fix options:**
1. Remove `"npcs"` from the validation required keys.
2. Add `"npcs": {}` to `ensure_world_state_defaults()`.

---

### 🟠 Dual player state: `player.py` object vs `world_state["player"]`

**Files:** `player.py`, `world_state.py`, `combat.py`  
**Impact:** Stats modified in `world_state["player"]` (level, XP, equipment bonuses) do not propagate to the `Player` object used by `combat.py`. Players who level up or equip gear between sessions may fight at old stats.

**Root cause:** Two representations were built incrementally. `player.py` predates the `world_state["player"]` section.

**Fix:** Establish one canonical source. Options:
1. Make `Player` a wrapper that reads/writes `world_state["player"]`.
2. Synchronize both on save/load.
3. Migrate combat.py to read `world_state["player"]` directly.

---

### 🟠 `rebels` faction missing from `faction_manager.FACTIONS`

**Files:** `faction_manager.py`, `world_state.py`  
**Impact:** `world_state["factions"]["rebels"]` is initialized and trackable via reputation changes, but `FACTIONS` in `faction_manager.py` does not include `rebels`. `evolve_factions()` and `show_factions()` will miss rebel-related processing entirely.

**Fix:** Add `"rebels"` to `faction_manager.FACTIONS` with appropriate starting values.

---

### 🟡 Dual region discovery state

**Files:** `region_manager.py`, `world_state.py`  
**Impact:** Region discovery is tracked in two places that can diverge: `REGIONS[name]['discovered']` (internal flag in the REGIONS dict) and `world_state["regions"]["discovered_regions"]` (the list in world_state). Code that reads one will not see changes made to the other.

**Fix:** Unify to a single source. The world_state list is the more appropriate canonical location since it is serialized in the player save.

---

### 🟡 `world_chaos` flat key vs `world_conditions.world_chaos`

**Files:** `world_state.py`, `story_manager.py`, `story.py`  
**Impact:** `story_manager.py` writes to `world_state["world_conditions"]["world_chaos"]`. `story.py` reads from `world_state["world_conditions"]["world_chaos"]` (correct — fixed in July 2026). The flat `world_state["world_chaos"]` exists as a legacy migration shim but is not kept in sync.

**Current state:** Fixed — `story.py` now reads from `world_conditions.world_chaos`. The flat key exists but is inert.

**Residual risk:** If any new code reads `world_state["world_chaos"]` directly it will see stale data. The flat key should eventually be removed or kept as a synchronized alias.

---

### 🟡 `npc_manager.NPCS` changes are not persisted

**Files:** `npc_manager.py`, `save_manager.py`  
**Impact:** `change_relationship()` in `npc_manager` updates `NPCS[name]["relationship"]`. This dict is **not** serialized by `save_manager.py`. NPC relationship changes are lost on save/load.

**Current state:** `dialogue_manager.npc_relationships` IS persisted and is the transactional relationship tracker. The two systems are parallel but only one persists.

**Fix:** Either serialize `NPCS` in `save_manager.py` or migrate `npc_manager.change_relationship()` to write to `dialogue_manager.npc_relationships` instead.

---

### 🟡 Quest `"type"` field missing — faction bonus never fires for current quests

**Files:** `quests.py`, `faction_manager.py`  
**Impact:** `faction_manager.on_quest_completed` grants +10 bonus reputation when `quest["type"] == "faction"`. No entries in `quest_database` currently have a `"type"` field. The bonus infrastructure is working but inactive.

**Fix:** Add `"type": "faction"` to qualifying quest entries in `quest_database`.

---

### 🟡 Legacy modules exist alongside active manager modules

**Files:** `factions.py`, `regions.py`, `loot.py`, `memory.py`  
**Impact:** Legacy standalone modules exist in the root directory that duplicate or predate their manager equivalents (`faction_manager.py`, `region_manager.py`, `loot_manager.py`, `memory_engine.py`). They may confuse future developers about which module to use.

**Current state:** They are not imported by any active code path. They exist as historical artifacts.

**Fix:** Move to `archive/legacy/` or delete. Document the decision.

---

### 🟡 `world_map.py` is a static display, not live

**File:** `world_map.py`  
**Impact:** The map display does not reflect dynamically discovered regions from `world_state["regions"]["discovered_regions"]`. A player who has discovered the shadow_marsh will see the same static map as a player who hasn't.

**Fix:** Connect `world_map.py` to world_state discovered_regions list.

---

### 🟢 `hub.py` not integrated into game loop

**File:** `hub.py`  
**Impact:** Hub location exists as a module but is not accessible from the main game loop.

**Fix:** Add hub as a travel destination or main menu option.

---

### 🟢 `world_social_reaction()` in relationship_manager is unused

**File:** `relationship_manager.py`  
**Impact:** The function exists but is never called. It was previously imported by `game_loop.py` (dead import removed). Dead code.

**Fix:** Either integrate into the game loop or remove.

---

### 🟢 `progression_state` schema not documented

**File:** `progression_manager.py`  
**Impact:** The schema of `progression_state` (what fields it contains) is not documented in this codebase. It is serialized but the structure is unclear without reading the module.

**Fix:** Document the dict schema in `docs/systems/progression_skills.md`.

---

### 🟢 `state_manager.validate_world_state` requires `"npcs"` key (see Critical above)

Duplicate entry — see the 🔴 Critical item at the top.

---

## Resolved Issues (Historical Record)

| Issue | Fixed | Notes |
|---|---|---|
| `ai_director.py` duplicate DM state | July 2026 | Merged into `dm_brain.py`; archived |
| `llm_bridge.py` contained full duplicate dm_brain logic | July 2026 | Rewrote llm_bridge as mock-only bridge |
| `travel_manager.py` imported non-existent `encounter_generator` | July 2026 | Changed to `encounter_manager` |
| `equipment_system.py` imported non-existent `inventory` list | July 2026 | Changed to `world_state["player"]["inventory"]` |
| `save_manager.py` imported non-existent `inventory` list | July 2026 | Changed to `world_state["player"]["inventory"]` |
| `loot_manager.py` imported `add_item` from `inventory` | July 2026 | Changed to `from world_state import add_item` |
| `game_loop.py` imported `update_economy` (doesn't exist) | July 2026 | Changed to `evolve_economy` |
| `game_loop.py` imported `show_settlements` (doesn't exist) | July 2026 | Changed to `show_all_settlements` aliased |
| `story.py` hard-keyed `story_memory["key"]` lookups | July 2026 | Changed to `.get()` |
| `story.py` hard-keyed `factions["key"]` lookups | July 2026 | Changed to `.get(key, 0)` |
| `story.py` read from flat `world_chaos` instead of `world_conditions.world_chaos` | July 2026 | Fixed to read from nested path |
| `region_manager.py` missing `show_regions()` function | July 2026 | Added wrapper function |
| Dead imports in 5 modules | July 2026 | All removed |
| Old save files missing new world_state schema keys | July 2026 | `ensure_world_state_defaults()` added |
| Tactical combat: Skill/Item abilities unwired (decorative) | June 2026 | Combat Phase C: full canonical ability pipeline (preview API, data-driven cooldowns, AI ability usage). Harness WARN eliminated. See `docs/verification/phaseC_ability_pipeline.md` |
| Class abilities cost 3 AP but classes only had 2 AP (unusable) | June 2026 | Capped class abilities to AP≤2 (full-turn cost) in `abilities.json` |
| Enemy blueprint referenced undefined ability `raise_skeleton` | June 2026 | Added `raise_skeleton` to `ability_library.json`; harness guards every blueprint ability id resolves |

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial document created from codebase analysis; resolved issues table populated |
