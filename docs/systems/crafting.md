# Crafting, Cooking & Alchemy Systems

> **Canon Status:** CONFIRMED — established 2026-07-31.  
> **Authority:** This document defines the canonical crafting philosophy, cooking system, and alchemy system. All three are now designed systems. The previous "NOT YET DEFINED" status is retired.  
> **Cross-references:** [`docs/GAME_BIBLE.md`](../GAME_BIBLE.md) · [`docs/systems/journal_system.md`](journal_system.md) · [`docs/systems/inventory_equipment.md`](inventory_equipment.md)

---

## Core Crafting Philosophy

Crafting is **intentionally lightweight**.

The design principle: preparation should feel like a natural part of adventuring, not a burden imposed between adventures. Players should rarely feel forced into unnecessary menu management or repetitive maintenance systems.

### Availability

Players may craft **outside of combat**, regardless of location, provided they possess the required ingredients.

Crafting is unavailable only when:
- Actively in combat
- Being pursued during scripted events
- Participating in time-sensitive story sequences

There is **no requirement to locate crafting stations or camps.** The assumption is that the party takes a few moments to prepare items — this is adventurers doing what adventurers do, not a factory system.

### Design Intent

Crafting should feel like a moment of agency between challenges. The player gathering specific reagents across a region, then combining them into something useful, reinforces the connection between exploration and preparation. Crafting should reward attentive players without punishing those who prefer to rely on found or purchased items.

---

## Companion Passive Crafting Skills

Companions contribute to crafting outside of combat. These bonuses should be **meaningful without forcing specific party compositions** — they enhance what the player is already doing, rather than gating content.

| Companion | Passive Crafting Contribution |
|---|---|
| **Torren** | Improved smithing efficiency — crafted equipment items have better results or require fewer materials |
| **Healer** *(companion TBD)* | Stronger crafted potions — Alchemy outputs have higher magnitude or duration |
| **Ranger** *(companion TBD)* | Increased herb gathering — more materials collected per gathering opportunity |
| **Eleanor** | Preserves rare magical reagents — reagents that would otherwise be consumed have a chance to be retained |

Future companions should provide exploration and crafting benefits that reflect their personalities and professions. The passive skill system is designed to make companions feel like real members of an expedition, not simply combat units.

---

## Cooking

### Philosophy

Cooking is an **optional support mechanic**. It is not a survival system.

There are:
- No hunger mechanics
- No starvation penalties
- No mandatory meals

Food serves **two purposes only:**
1. **Moderate healing** outside of combat
2. **Temporary stat bonuses** — duration-limited improvements to specific combat or exploration stats

### Food vs. Potions

Food and potions occupy distinct roles and should not substitute for each other:

| System | Role |
|---|---|
| **Potions** | Emergency recovery during or immediately after combat |
| **Food** | Preparation before adventuring; sustained support during exploration |

Food should never replace potions. A player who has run out of potions mid-dungeon is not saved by cooking — cooking happens in preparation, not crisis.

### Recipes

Recipes are learned through play — exploration, merchants, quests, and companions. They are recorded in the Journal's Recipes section and persist across the campaign.

Regional recipes reinforce worldbuilding and local culture. A dwarven mountain community's recipes reflect different ingredients and purposes than a coastal halfling settlement's cuisine. Learning a region's recipes is a form of learning the region.

### Crafting Requirements

- Learned recipe
- Required ingredients (sourced through exploration, purchase, or gathering)
- Not in combat or a time-sensitive sequence

No cooking station required. The party is assumed to have basic cooking capability as a matter of expedition preparedness.

---

## Alchemy

### Philosophy

Alchemy follows the same lightweight philosophy as general crafting.

Players may craft potions **whenever they are not in combat.** No crafting stations required. Potion crafting should be **immediate and intuitive** — gather the reagents, know the formula, produce the result.

### Requirements

- Learned formula (recorded in the Journal's Alchemy section)
- Required ingredients (sourced through exploration, purchase, herb gathering, or trade)

### Formula Acquisition

Formulas are learned through:
- Discovery in the world (found in texts, laboratories, traveler's notes)
- Purchase from alchemists, herbalists, or specialty merchants
- Quest rewards
- Eleanor's passive skill interactions (rare reagent preservation may unlock formula discovery)

### Potion Design Principles

Potions are **emergency recovery tools** — their role is getting through a crisis that food and preparation did not prevent. They should be valuable enough that players feel the cost of using them, but available enough that players are not frustrated by absence.

The player who prepares well through cooking and alchemy enters dangerous situations with a meaningful buffer. The player who does not will spend more potions.

---

## Safe Area Activities

Cities, towns, inns, guild halls, forts, and other secure locations act as **preparation hubs** for the core gameplay loop. These locations represent civilization.

In safe areas, players can:
- **Shop** — purchase equipment, consumables, ingredients, recipes, and formulas
- **Upgrade equipment** — improvements available through specific merchants or Torren's passive skill
- **Accept quests** — quest givers are located in civilization, not wilderness
- **Change party members** — swap active companions from the full roster
- **Talk with NPCs** — advance relationships, learn rumors, gather information
- **Advance companion storylines** — companion quests and conversations triggered in civilization
- **Learn recipes** — cooking recipe merchants and questgivers
- **Learn alchemy formulas** — alchemist merchants and in-world discovery

Crafting (cooking and alchemy) is available here and everywhere outside of active combat. Safe areas are defined by access to services, NPCs, and the ability to swap party members — not by exclusive crafting access.

---

## Inventory Organization

The canonical inventory is organized into seven categories:

| Category | Contents |
|---|---|
| **Weapons** | All weapon types; equippable items |
| **Armor** | Body armor, helmets, shields |
| **Accessories** | Rings, amulets, utility wearables |
| **Consumables** | Potions, prepared food, single-use items |
| **Crafting Materials** | Raw ingredients (herbs, ores, reagents, gathered materials) |
| **Quest Items** | Items tied to active or completed quests; cannot be sold or discarded |
| **Valuables** | Coins, gems, artwork, tradeable goods |

Inventory should remain **clean and intuitive.** Organizational categories should reduce the time players spend searching for what they need, not add friction.

---

## Design Integration

The crafting, cooking, and alchemy systems reinforce the game's central design philosophy:

> *Small acts matter. The player changes the world through countless ordinary decisions that collectively leave it stronger than they found it.*

Gathering a rare herb across three sessions and using it to craft a potion that saves a companion in a critical moment is a small story. The crafting system exists to make those small stories possible — to connect the act of exploration to the act of preparation to the act of survival, without requiring the player to manage a complex production system.

**Every system should feel like it belongs in an adventure, not in a workshop.**

---

## Future Implementation Notes

The current terminal prototype has a partial shop and basic inventory system. The crafting, cooking, and alchemy systems are **design targets** for the 3D game. Implementation in the prototype should follow these principles when added:

- No crafting station requirement
- Formula/recipe tracking in world_state (compatible with save system)
- Companion passive bonuses applied as modifiers at craft time
- Journal integration for recipe/formula tracking

See [`docs/systems/inventory_equipment.md`](inventory_equipment.md) for current inventory implementation.

---

## Document History

| Date | Change |
|---|---|
| 2026-07-31 | Created — Crafting, Cooking, and Alchemy systems defined as canonical; companion passive crafting skills documented; safe area activities; canonical inventory categories; design integration philosophy |
