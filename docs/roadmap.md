# Development Roadmap

**Purpose:** Documents confirmed development priorities and future directions.

**Rule:** Items marked **[CONFIRMED]** are based on implemented infrastructure and clear next steps. Items marked **[FUTURE]** are speculative directions, not committed work.

---

## Immediate Priorities (Infrastructure)

These address known issues and complete partially-implemented systems.

### 1. Fix `validate_world_state` npcs key bug 🔴
**What:** `state_manager.validate_world_state()` requires `world_state["npcs"]` which is never initialized.  
**Why:** New games fail validation; save loads through state_manager may be refused.  
**How:** Remove `"npcs"` from required keys, or add `"npcs": {}` to `ensure_world_state_defaults()`.  
**Files:** `state_manager.py`, optionally `world_state.py`

### 2. Unify player state (player.py vs world_state["player"])
**What:** The `Player` object in `player.py` and `world_state["player"]` contain overlapping fields that can diverge.  
**Why:** Players who level up or equip gear won't see those changes reflected in combat.  
**How:** Choose one canonical source; add sync logic on save/load, or migrate combat to read world_state.  
**Files:** `player.py`, `world_state.py`, `combat.py`, `save_manager.py`

### 3. Add `rebels` to `faction_manager.FACTIONS`
**What:** `rebels` faction exists in world_state but is missing from `FACTIONS` dict.  
**Why:** `evolve_factions()` ignores rebels; rebel reputation changes have no faction-level effects.  
**How:** Add rebels entry to `FACTIONS` with default values.  
**Files:** `faction_manager.py`

---

## Near-Term Gameplay (Completing Stubbed Systems)

### 4. Implement skill tree and combat skill use
**What:** `skills.py`, `skill_tree.py`, and the "Use Skill" combat option are stubs.  
**Why:** Core class fantasy depends on having usable skills.  
**How:** Define skill roster; implement in-combat skill resolution; wire to resource pool.  
**Files:** `skills.py`, `skill_tree.py`, `combat.py`, `progression_manager.py`

### 5. Implement character class selection at new game
**What:** Character class defaults to "Warrior"; no class selection exists.  
**Why:** Class identity is foundational to RPG experience.  
**How:** Add class selection to `main.py` new game flow; set starting stats per class.  
**Files:** `main.py`, `world_state.py`, `player.py`

### 6. Implement level-up stat growth
**What:** `check_level_up()` increments the level number but doesn't improve stats.  
**Why:** Progression must feel meaningful.  
**How:** Define stat growth per level; apply in `check_level_up()`.  
**Files:** `progression_manager.py`, `data/balance.py`

### 7. Activate quest type field for faction bonus
**What:** Quest database entries lack `"type": "faction"` so the faction bonus handler never fires.  
**How:** Review quest entries; add `"type": "faction"` where appropriate.  
**Files:** `quests.py`

---

## Medium-Term (New Systems)

### 8. Dungeon crawl system
**What:** Implement floor-by-floor dungeon exploration using the `DUNGEONS` data structure.  
**Scope:** Room events, trap encounters, floor bosses, dungeon loot tables.  
**Files:** `dungeon_manager.py`, new `dungeon_crawler.py` potentially

### 9. Unify region discovery state
**What:** `REGIONS[name]['discovered']` and `world_state["regions"]["discovered_regions"]` can diverge.  
**How:** Make `region_manager.discover_region()` update both; or deprecate the internal flag.  
**Files:** `region_manager.py`, `world_state.py`

### 10. Live world map
**What:** `world_map.py` shows a static map; connect to `world_state["regions"]["discovered_regions"]`.  
**Files:** `world_map.py`

### 11. Integrate hub.py into game loop
**What:** The hub location exists as a module but is unreachable.  
**How:** Add "Return to Hub" as a travel or menu option; wire hub services.  
**Files:** `hub.py`, `game_loop.py`, `travel_manager.py`

### 12. Persist NPC relationship changes
**What:** `npc_manager.NPCS` changes (via `change_relationship()`) are not saved.  
**How:** Either serialize NPCS dict in `save_manager.py`, or route npc_manager writes through `dialogue_manager.npc_relationships`.  
**Files:** `npc_manager.py`, `save_manager.py`

---

## Long-Term (Future Expansion)

These are directions, not commitments. Do not implement without explicit design work first.

### [FUTURE] Real LLM integration
- Replace mock functions in `llm_bridge.py` with real API calls.
- `prompt_manager.py` provides the template infrastructure.
- No other files need to change.

### [FUTURE] World lore development
- Define specific lore for the Kingdom, Shadow Cult, Mages Guild, Rebels.
- Name locations, write region histories.
- Define NPC backstories and companion characters.
- All lore additions go into `docs/GAME_BIBLE.md` first as confirmed canon.

### [FUTURE] Browser UI integration
- Connect `app.py` (Flask) to terminal game state.
- Requires a shared state layer or API contract between the two systems.

### [FUTURE] Crafting system
- Economy and inventory infrastructure is ready.
- Design: recipes, component gathering, crafted item database.

### [FUTURE] Multi-act campaign
- `campaign_manager.py` tracks act progression.
- Script act-specific events, villain encounters, and world state changes per act.

### [FUTURE] Companion characters
- Define specific companions with backstories, abilities, and recruitment missions.
- Implement loyalty arc and companion story reactions fully.

### [FUTURE] Save slots
- Multiple named save files with slot selection UI.

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial roadmap created from codebase analysis and known issues |
