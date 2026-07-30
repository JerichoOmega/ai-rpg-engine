# Factions & Economy Systems

**Purpose:** Documents the faction reputation system, faction evolution, the economy simulation, and how they interact.

**Modules:** `faction_manager.py`, `factions.py`, `economy_manager.py`

---

## Overview

Factions represent the major political powers in the game world. The player's reputation with each faction influences available quests, NPC behavior, world events, and narrative tone. The economy simulation models trade, inflation, and regional prosperity, affecting shop prices and world stability.

---

## Faction System

### Faction Data Stores

There are **two separate faction data structures** that must not be confused:

| Store | Location | Contains |
|---|---|---|
| Reputation values | `world_state["factions"]` | `{faction_key: int}` reputation scores |
| Full faction data | `faction_manager.FACTIONS` | Rich per-faction dict with military, economy, influence |

Both are serialized by `save_manager.py`.

### Factions Defined

| Key | Name | Notes |
|---|---|---|
| `kingdom` | The Kingdom | Ruling authority |
| `shadow_cult` | Shadow Cult | Primary antagonist faction |
| `mages_guild` | Mages Guild | Arcane institution |
| `rebels` | Rebels | Resistance faction |

> **`rebels` gap:** `world_state["factions"]` initializes `rebels: 0`. `faction_manager.FACTIONS` does **not** include `rebels`. Functions that iterate `FACTIONS` (like `evolve_factions()`) will miss rebel reputation. This is a known issue.

### Reputation Range and Thresholds

Reputation is an integer from **-100 to 100** (clamped).

| Range | Status |
|---|---|
| 61–100 | Allied |
| 31–60 | Friendly |
| -30–30 | Neutral |
| -31–60 | Hostile |
| -61–-100 | Enemy |

Exact threshold values are defined in `faction_manager.evaluate_faction_state()`.

### Key Functions (`faction_manager.py`)

| Function | Description |
|---|---|
| `change_reputation(faction_name, amount)` | Adjust rep; clamp; print change; evaluate state |
| `evaluate_faction_state(faction_name)` | Determine and print status tier; emit `faction_hostile` if hostile |
| `get_faction_status(faction_name)` | Return current status string |
| `evolve_factions()` | Called each tick; shifts faction relationships based on world conditions |
| `show_factions()` | Print all faction military, economy, influence, and rep |
| `on_quest_completed(event_data)` | Event handler: bonus +10 rep for type=faction quests |

### `factions.py`

A legacy module containing earlier faction definitions. Not integrated into the active manager flow. New code should use `faction_manager.py`.

### World Events from Factions

When `shadow_cult` reputation drops into hostile range:
1. `evaluate_faction_state("shadow_cult")` emits `faction_hostile`.
2. `world_event_manager` (subscribed) triggers "Cult Assassins" world event.
3. `"Cult assassins begin hunting the player."` is printed.

---

## Economy System

### Economy State

```python
# economy_manager.py (module level)
economy_state = {
    "inflation":         1.0,   # price multiplier (1.0 = base price)
    "trade_routes":      {},    # {route_name: {active: bool, bonus: float}}
    "global_stability":  1.0,   # 0.0–1.0 overall stability modifier
}
```

Serialized by `save_manager.py` under `"economy"` key.

### Key Functions (`economy_manager.py`)

| Function | Description |
|---|---|
| `get_item_price(item_name)` | Returns inflation-adjusted price from shop/loot database |
| `change_inflation(amount)` | Adjust inflation value |
| `change_global_stability(amount)` | Adjust stability modifier |
| `trigger_trade_route_event()` | Randomly disrupts or boosts a trade route |
| `evolve_economy()` | Called each game tick; adjusts inflation and stability |
| `trigger_economic_crisis()` | Sharply degrades stability and inflates prices |
| `update_region_economy()` | Updates per-region economic modifiers |
| `show_market_prices()` | Print current item prices |
| `show_trade_routes()` | Print trade route status |
| `add_trade_route(name, bonus)` | Register a new trade route |
| `disable_trade_route(name)` | Deactivate a trade route |
| `show_economy_summary()` | Print full economy state |

### Economy Tick

`evolve_economy()` is called by `game_loop.process_game_tick()` every game tick. It:
- Slightly adjusts inflation based on stability.
- May trigger random trade route events.
- Keeps economy state from being static.

### Price System

`shop.py` uses `economy_manager.get_item_price(item_name)` to adjust prices before presenting them to the player. A high-inflation economy makes all items more expensive.

---

## Interaction Between Factions and Economy

- When a faction triggers a world event, `story_manager` can increment `world_conditions.world_chaos`.
- Higher world chaos can suppress stability, affecting economy.
- Region control by hostile factions can decrease local prosperity.

These interactions are not directly wired in code — they flow through world_state as intermediate state, not direct function calls.

---

## Design Rationale

- **Reputation as a single integer:** Simple, auditable, and easy to adjust. More complex relationship modeling (fear, loyalty, history) is a future expansion.
- **Economy as a simulation layer:** Economy runs in the background, adding texture to prices without requiring the player to explicitly manage it.
- **Faction hostile events via event bus:** Faction manager does not call world_event_manager directly — it emits an event, keeping modules decoupled.

---

## Rules

- Always use `change_reputation()` to modify faction reputation — never write to `world_state["factions"]` directly.
- Always use `evolve_economy()` for economy ticks — do not modify `economy_state` directly from game_loop.
- When adding a new faction, add it to **both** `faction_manager.FACTIONS` **and** `world_state["factions"]` defaults in `ensure_world_state_defaults()`.

---

## Future Expansion

- Full faction lore: history, motivations, internal leadership, inter-faction relationships.
- Add `rebels` faction to `faction_manager.FACTIONS`.
- Faction war system — two factions at war affect regions, quests, and world events.
- Trade goods system — specific commodities with supply/demand.
- Player-owned trade routes.
- Crafting economy (production + selling).

---

## Lore Status

⚠️ **NOT YET DEFINED** — The four faction names are confirmed. All backstory, leadership, history, and lore are undefined. Do not invent canon.

---

## Related Systems

- `world_state.py` — Faction reputation lives in `world_state["factions"]`
- `quests.py` — Quest completion changes faction rep
- `region_manager.py` — Region faction control affects stability
- `event_bus.py` — `faction_hostile` event
- `world_event_manager.py` — Responds to faction events
- `story.py` — Reads faction reputation for narrative context

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation; rebels faction gap noted |
