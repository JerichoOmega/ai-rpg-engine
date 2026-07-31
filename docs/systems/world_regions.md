# World, Regions & Travel System

**Purpose:** Documents the region model, travel mechanics, settlements, dungeons, locations, and world map.

**Modules:** `region_manager.py`, `regions.py`, `travel_manager.py`, `location_manager.py`, `settlement_manager.py`, `dungeon_manager.py`, `world_map.py`, `hub.py`, `world_event_manager.py`

---

## Overview

The world is divided into named regions. Each region has its own biome, danger level, faction control, weather, and economic conditions. Players travel between regions, encountering events along the way. Settlements within regions provide services, rumors, and economic interaction. Dungeons represent challenging sub-locations.

---

## Canonical Design Direction

The following defines the target exploration system. See **Current Implementation** below for the terminal prototype's current state.

### Two-Layer Exploration System

**Layer 1 — Strategic Continent Map**

Travel between major locations occurs on a continent map (inspired by Solasta). Players select destinations rather than manually traversing the world. Travel can trigger: random encounters, story events, companion conversations, merchant caravans, ambushes, and dynamic world events. The map evolves throughout the story to reflect world events, political changes, and player decisions.

> Travel should feel like a journey rather than a loading screen.

**Layer 2 — Regional Exploration**

On arrival, the player enters a handcrafted explorable region containing: main story content, side quests, hidden areas, dungeons, companion content, treasure, and environmental storytelling. Regions reward exploration without unnecessary empty space.

### Design Philosophy

The continent should feel vast without requiring players to traverse every mile. The strategic map handles scale; regions provide depth.

---

---

## Region System

### Region Data (`region_manager.py`)

`REGIONS` is a module-level dict defining all regions. Serialized by `save_manager.py`.

```python
REGIONS = {
    "kingdom_capital": {
        "display_name": "The Capital",
        "biome":        "urban",
        "danger":       2,        # encounter difficulty modifier
        "faction":      "kingdom",
        "weather":      "clear",
        "stability":    80,       # 0–100
        "prosperity":   70,       # 0–100
        "corrupted":    False,
        "discovered":   True,     # internal flag (separate from world_state discovered list)
        "settlements":  [...],
        "events":       [],
        "neighbors":    [...],
    },
    ...
}
```

> **Dual discovery state:** `region_manager.py`'s `discover_region()` sets `REGIONS[name]['discovered'] = True` internally. `world_state["regions"]["discovered_regions"]` is a separate list. Both exist and can diverge. See Known Issues.

### Default Starting Region

`kingdom_capital` — set as `world_state["regions"]["current_region"]` default.

### Key Functions (`region_manager.py`)

| Function | Description |
|---|---|
| `get_region_data(name)` | Return region dict |
| `get_current_region()` | Return current region key from world_state |
| `get_region_story_themes(name)` | Return narrative themes for region |
| `get_neighboring_regions(name)` | Return list of neighboring region keys |
| `get_region_settlements(name)` | Return settlement list for region |
| `get_region_weather(name)` | Return current weather string |
| `change_region_weather(name, weather)` | Update weather |
| `change_region_stability(name, amount)` | Adjust stability |
| `change_region_prosperity(name, amount)` | Adjust prosperity |
| `random_weather_update()` | Randomly update weather for all regions |
| `evolve_region(name)` | Advance a single region's state |
| `evolve_world_regions()` | Advance all regions each tick |
| `show_region(name)` | Print region info |
| `show_regions()` | Print all region summaries |
| `discover_region(name)` | Mark as discovered (internal REGIONS flag) |
| `change_danger(name, amount)` | Adjust danger level |
| `evaluate_region(name)` | Assess region health and print report |
| `add_region_event(name, event)` | Add an event to a region |
| `change_region_control(name, faction)` | Change controlling faction |
| `corrupt_region(name)` | Apply corruption state |
| `random_region_event()` | Generate a random region event |

### `regions.py`

A legacy module with earlier region definitions. Not integrated into the active manager flow. Use `region_manager.py` for all region operations.

---

## Travel System

### Key Functions (`travel_manager.py`)

| Function | Description |
|---|---|
| `travel_to_region(destination)` | Move player to destination; generate travel encounter |
| `get_travel_options()` | Return available destinations from current region |

### Travel Flow

```
travel_to_region("shadow_marsh")
  → world_state["regions"]["current_region"] = "shadow_marsh"
  → encounter_manager.generate_encounter()   # travel encounter
  → print travel narrative
```

The travel encounter uses `encounter_manager.generate_encounter()` (not the deprecated `encounter_generator` module).

---

## Settlement System

### Settlement Data (`settlement_manager.py`)

`SETTLEMENTS` is a module-level dict. Serialized by `save_manager.py`.

```python
SETTLEMENTS = {
    "capital_market": {
        "name":       "Capital Market",
        "region":     "kingdom_capital",
        "prosperity": 75,
        "security":   80,
        "services":   ["shop", "inn", "blacksmith"],
        "events":     [],
    },
    ...
}
```

### Key Functions (`settlement_manager.py`)

| Function | Description |
|---|---|
| `get_settlement_data(name)` | Return settlement dict |
| `show_settlement(name)` | Print settlement details |
| `get_random_rumor()` | Return a rumor generated from settlement state |
| `add_settlement_event(name, event)` | Add event to settlement |
| `change_settlement_prosperity(name, amount)` | Adjust prosperity |
| `change_settlement_security(name, amount)` | Adjust security |
| `random_settlement_event()` | Generate random settlement event |
| `evolve_settlement(name)` | Advance settlement state |
| `evolve_settlements()` | Advance all settlements each tick |
| `settlement_has_service(name, service)` | Check if service available |
| `show_settlement_services(name)` | Print available services |
| `show_all_settlements()` | Print all settlement summaries |

> **Import note:** `game_loop.py` imports `show_all_settlements` aliased as `show_settlements`:
> `from settlement_manager import (show_all_settlements as show_settlements)`.

---

## Dungeon System

### Dungeon Data (`dungeon_manager.py`)

`DUNGEONS` is a module-level dict. Serialized by `save_manager.py`.

```python
DUNGEONS = {
    "crypt_of_shadows": {
        "name":       "Crypt of Shadows",
        "region":     "shadow_marsh",
        "danger":     8,
        "floors":     3,
        "boss":       "Lich King",
        "cleared":    False,
        ...
    },
    ...
}
```

Full dungeon crawl mechanics (floor-by-floor progression, trap encounters, room events) are ⚠️ **NOT YET IMPLEMENTED** beyond the data structure.

---

## Location System

### Location Data (`location_manager.py`)

Defines specific named locations within regions. A more granular layer below region, above settlement.

`world_state["regions"]["current_location"]` tracks the player's specific location within a region.

---

## World Map

`world_map.py` provides a text-based map visualization. Currently a standalone display module — not connected to the live region state (it does not reflect discovered/undiscovered regions dynamically).

---

## Hub

`hub.py` defines a central hub location. Currently a standalone module, not integrated into the main game loop. Intended as a home-base / safe zone.

---

## World Event Manager

### World Events (`world_event_manager.py`)

```python
# module level
active_world_events = []    # currently active event names
completed_world_events = [] # resolved event names
```

Both serialized by `save_manager.py`.

| Function | Description |
|---|---|
| `update_world_events()` | Called each tick; resolves pending events |
| `generate_random_world_event()` | Probabilistically create a new world event |
| `show_active_world_events()` | Print active events |

World events are appended to `world_state["events"]` via `activate_world_event()` and to `active_world_events` in the manager. Events have names like "Cult Assassins", "Dragon Sighted", "Trade Route Collapse".

---

## Design Rationale

- **Region as the primary world unit:** Large enough to be meaningful (biome, faction), small enough to have distinct identity.
- **Settlement as sub-region:** Settlements anchor the economy and social layer within a region.
- **Dungeon as opt-in content:** Dungeons are defined but not forced on the player — they require explicit entry.
- **evolve_world_regions() each tick:** The world does not stand still. Regions degrade, weather changes, corruption spreads passively.

---

## Known Issues

- **Dual discovery state:** `REGIONS[name]['discovered']` (internal) and `world_state["regions"]["discovered_regions"]` (state) track discovery separately and can diverge.
- `world_map.py` is a static display, not connected to live region discovery state.
- `hub.py` is not integrated into the game loop.

---

## Future Expansion

**Canonical targets (confirmed design direction):**
- Strategic continent map — visual, selectable destination layer with travel events
- Continent map evolves dynamically to reflect world events and player choices
- Handcrafted regions with story content, side quests, hidden areas, dungeons, and environmental storytelling

**Not yet defined:**
- Dynamic region generation (procedural biomes, names)
- Full dungeon crawl system with floor maps and room events
- World map updated dynamically as regions are discovered
- Hub as a persistent player base with upgrades
- Region conquest / liberation mechanics
- Climate and season effects on region conditions
- Faction wars shifting region control dynamically

---

## Lore Status

⚠️ **NOT YET DEFINED** — Specific region names, their lore, history, notable locations, and characters are defined only as data structure stubs. Do not invent canon. Document confirmed region keys only.

---

## Related Systems

- `world_state.py` — Current region and discovered regions
- `faction_manager.py` — Faction control of regions
- `economy_manager.py` — Regional economy modifiers
- `encounter_manager.py` — Travel encounters
- `settlement_manager.py` — Settlement rumors and services
- `narrative_ai.py` — Region narration

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation; dual discovery state issue noted |
| July 2026 | Added canonical design direction: two-layer exploration system (strategic continent map + handcrafted regions) |
