# Inventory, Equipment, Loot & Shop Systems

**Purpose:** Documents item storage, equipment slots, loot generation, and shop transactions.

**Modules:** `inventory.py`, `equipment_system.py`, `loot_manager.py`, `loot.py`, `shop.py`, `data/balance.py`

---

## Canonical Inventory Categories

> **Canon Status:** CONFIRMED — 2026-07-31.

The player inventory is organized into **seven categories**:

| Category | Contents |
|---|---|
| **Weapons** | All weapon types; equippable items |
| **Armor** | Body armor, helmets, shields |
| **Accessories** | Rings, amulets, utility wearables |
| **Consumables** | Potions, prepared food, single-use items |
| **Crafting Materials** | Raw ingredients — herbs, ores, reagents, gathered materials |
| **Quest Items** | Items tied to active or completed quests; cannot be sold or discarded |
| **Valuables** | Coins, gems, artwork, tradeable goods |

Inventory should remain **clean and intuitive.** Category organization reduces search time and avoids friction. The current terminal prototype uses a flat item list — the category structure is the design target for the 3D game.

For crafting material use, see [`docs/systems/crafting.md`](crafting.md).

---

## Overview

Items exist in the player's inventory as name strings. Equipment is a separate slot system that applies stat modifiers. Loot is generated post-combat. The shop provides a buy/sell interface with inflation-adjusted pricing.

---

## Inventory

### Canonical Inventory Location

```python
world_state["player"]["inventory"]   # list of item name strings
```

This is the **only** inventory list that should be used. All other references are either helpers or legacy.

### Inventory Helpers (`inventory.py`)

`inventory.py` provides UI and interaction helpers. It does **not** own the inventory list.

| Function | Description |
|---|---|
| `show_inventory()` | Print all items with indices |
| `give_item(item_name)` | Add item (calls `world_state`'s `add_item`) |
| `take_item(item_name)` | Remove item (calls `world_state`'s `remove_item`) |
| `use_potion()` | Find and use a potion from inventory |
| `equip_weapon(item_name)` | Equip a weapon (delegates to equipment_system) |
| `has_item(item_name)` | Return bool — item in inventory? |
| `inventory_count()` | Return count of items |
| `receive_loot(loot)` | Add a list of items to inventory |
| `show_gold()` | Print current gold |

### World State Item Helpers (`world_state.py`)

| Function | Description |
|---|---|
| `add_item(name)` | Append to `world_state["player"]["inventory"]` |
| `remove_item(name)` | Remove first occurrence from inventory |
| `add_gold(amount)` | Increment `world_state["player"]["gold"]` |
| `remove_gold(amount)` | Decrement gold, floor at 0 |

### Import Rule

> **Critical:** `inventory.py` exports only functions, not a list called `inventory`. Do not `from inventory import inventory` — this will raise `ImportError`. Use `world_state["player"]["inventory"]` directly for the raw list.

---

## Equipment System

### Equipment Slots

```python
# equipment_system.py (module level)
equipment = {
    "weapon":    None,
    "armor":     None,
    "helmet":    None,
    "accessory": None
}
```

Serialized by `save_manager.py` under `"equipment"` key.

### Item Database

`ITEM_DATABASE` in `equipment_system.py` defines equippable items with stat modifiers:

```python
ITEM_DATABASE = {
    "Iron Sword": {
        "slot":         "weapon",
        "attack_bonus": 8,
        ...
    },
    ...
}
```

### Key Functions (`equipment_system.py`)

| Function | Description |
|---|---|
| `equip_item(item_name)` | Equip from inventory; apply stats; unequip old item; emit `item_equipped` |
| `unequip_item(slot)` | Remove from slot; remove stat modifiers; return to inventory |
| `apply_item_stats(item_name)` | Add item stat bonuses to player |
| `remove_item_stats(item_name)` | Remove item stat bonuses from player |
| `show_equipment()` | Print current equipment by slot |

### Equip Flow

```
equip_item("Iron Sword")
  → check item_name in ITEM_DATABASE
  → check item_name in world_state["player"]["inventory"]
  → unequip old item in that slot (if any) → put old item back in inventory
  → equipment[slot] = item_name
  → world_state["player"]["inventory"].remove(item_name)
  → apply_item_stats(item_name) → modifies player object stats
  → emit("item_equipped", item_name=item_name)
```

---

## Loot Manager

### Loot Rarity System

```python
# loot_manager.py (module level)
RARITIES = {
    "common":    { "weight": 60, "bonus_range": (0, 2) },
    "uncommon":  { "weight": 25, "bonus_range": (2, 5) },
    "rare":      { "weight": 12, "bonus_range": (5, 10) },
    "legendary": { "weight":  3, "bonus_range": (10, 20) },
}
```

### Key Functions (`loot_manager.py`)

| Function | Description |
|---|---|
| `roll_rarity()` | Returns a rarity tier string based on weighted roll |
| `generate_loot(enemy)` | Generate loot appropriate to enemy type and level |
| `generate_dungeon_loot()` | Generate higher-quality dungeon loot |
| `generate_boss_loot()` | Generate boss-tier loot |
| `scale_stat(base, rarity)` | Apply rarity scaling to a stat value |
| `random_treasure_event()` | Random treasure discovery |
| `add_loot_item(item_name)` | Add generated loot to player inventory |
| `trigger_legendary_drop()` | Force a legendary item drop |
| `show_loot_tables()` | Print loot table configuration |
| `show_loot_summary()` | Print recent loot history |

### `loot.py`

A legacy standalone loot module. Not integrated into the active loot_manager flow. New code should use `loot_manager.py`.

### Import Rule

> `add_item` is in `world_state.py`, **not** `inventory.py`. `loot_manager.py` imports it from `world_state`: `from world_state import (add_item)`.

---

## Shop System

### Shop Database

```python
# shop.py (module level)
SHOP_DATABASE = {
    "Health Potion": { "base_price": 50, ... },
    "Iron Sword":    { "base_price": 120, ... },
    ...
}
```

### Key Functions (`shop.py`)

| Function | Description |
|---|---|
| `buy_item(item_name)` | Check gold, deduct, add to inventory |
| `sell_item(item_name)` | Remove from inventory, add gold |
| `show_shop()` | Print available items with inflation-adjusted prices |
| `enter_shop()` | Interactive shop loop |

### Price Calculation

Prices are fetched via `economy_manager.get_item_price(item_name)`, which applies the current inflation multiplier from `economy_state`.

### Transaction Flow

```
buy_item("Health Potion")
  → economy_manager.get_item_price("Health Potion")  → adjusted price
  → check world_state["player"]["gold"] >= price
  → remove_gold(price)
  → give_item("Health Potion")   # inventory.py helper → world_state.add_item
```

---

## Balance Data

`data/balance.py` contains numeric constants used for balancing. These values (damage ranges, price bases, XP rewards, etc.) are imported by combat, loot, and economy modules to keep magic numbers out of game logic.

⚠️ **NOT YET FULLY DOCUMENTED** — The full contents of `data/balance.py` should be reviewed and documented when balancing work begins.

---

## Design Rationale

- **Strings as item identifiers:** Simple, JSON-serializable, human-readable.
- **Equipment system separate from inventory:** Equipped items are not in the inventory list — prevents double-counting and simplifies "what am I wearing" queries.
- **Rarity-based loot:** Standard RPG rarity tiers give the loot system a clear upgrade path.

---

## Known Issues

- Legacy `loot.py` and `inventory.py` overlap in purpose with `loot_manager.py` and `world_state.py` helpers. These legacy modules are not integrated into the active flow but are not yet removed.
- `player.gold` (on `player.py` Player object) and `world_state["player"]["gold"]` can diverge if one is updated without the other.

---

## Future Expansion

- Item stacking (e.g., "Health Potion x3").
- Item descriptions visible in inventory UI.
- Crafting system using inventory components.
- Item durability and repair.
- Unique/named legendary items with lore.
- Merchant reputation affecting buy/sell prices.

---

## Related Systems

- `world_state.py` — Canonical inventory and gold storage
- `equipment_system.py` — Slot management and stat application
- `combat.py` — Post-combat loot trigger
- `economy_manager.py` — Inflation-adjusted shop prices
- `event_bus.py` — `item_equipped` event

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation; inventory import anti-pattern documented |
| 2026-07-31 | Canonical inventory categories added (seven categories: Weapons, Armor, Accessories, Consumables, Crafting Materials, Quest Items, Valuables) |
