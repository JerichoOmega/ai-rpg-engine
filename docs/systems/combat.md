# Combat System

**Purpose:** Documents the turn-based combat engine, enemy structure, status effects, boss encounters, and post-combat flow.

**Modules:** `combat.py`, `enemy_manager.py`, `bosses.py`, `status_effects.py`, `encounter_manager.py`

> **Target direction — Reactive Combat pillar:** the 3D combat target is built around
> *Reactive Combat* + **Resolve** + **Partner Techniques**
> ([`../design/REACTIVE_COMBAT.md`](../design/REACTIVE_COMBAT.md), [`../COMBAT_SYSTEM.md`](../COMBAT_SYSTEM.md)).
> This terminal prototype does **not** implement it; it is documented here as design direction only.

---

## Overview

Combat is **turn-based** and **terminal-driven**. The player faces one or more enemies per encounter. Companions in the active party contribute each round. The system is synchronous and blocking — the game waits for player input on each turn.

---

## Current Implementation

### Encounter Entry Points

| Function | Module | Description |
|---|---|---|
| `quick_encounter()` | `combat.py` | Standard random enemy encounter |
| `boss_encounter(boss_name)` | `combat.py` | Named boss fight |
| `generate_encounter()` | `encounter_manager.py` | Creates and configures an encounter |
| `generate_narrative_encounter()` | `encounter_manager.py` | Story-context encounter |
| `ambush_encounter()` | `encounter_manager.py` | Player-disadvantage encounter |
| `random_boss_encounter()` | `game_loop.py` | 10% post-explore boss trigger |

### Combat Turn Structure

```
encounter starts
  │
  ├── display enemy
  ├── display player stats
  │
  └── ROUND LOOP
        ├── Player turn
        │     ├── "1. Attack"      → roll damage, apply to enemy
        │     ├── "2. Use Skill"   → skill effect (if implemented)
        │     ├── "3. Use Item"    → item effect (potion, etc.)
        │     └── "4. Flee"        → % chance to escape
        │
        ├── Companion turns (auto)
        │     └── companion_attack() for each active companion
        │
        ├── Enemy turn
        │     ├── standard attack → player defense reduction
        │     ├── crit check → double damage if crit_chance hits
        │     └── special moves (boss only)
        │
        ├── Status effect resolution
        │     └── tick burn/poison/bleed per entity
        │
        └── Check win/loss conditions
              ├── enemy.hp <= 0 → VICTORY
              ├── player.hp <= 0 → DEFEAT
              └── flee success → ESCAPE
```

### Victory Flow

```
enemy dies
  → event_bus.emit("enemy_killed", enemy_name=name)
       → dm_brain.on_enemy_killed()       # +5 pressure
       → narrative_ai.on_enemy_killed()   # narrative record
       → quest kill-counter update
  → loot_manager.generate_loot()
  → add_item() for loot
  → progression_manager.check_level_up()
  → print victory message
```

### Defeat Flow

Current behavior: prints defeat message. Full death/respawn/game-over flow is ⚠️ **NOT YET FULLY DEFINED**.

---

## Player Combat Stats

| Stat | Source | Effect |
|---|---|---|
| `attack_bonus` | `player.attack_bonus` | Added to damage rolls |
| `defense` | `player.defense` | Subtracted from incoming damage |
| `evasion` | `player.evasion` | Chance to dodge entirely |
| `weapon_bonus` | `world_state["player"]["weapon_bonus"]` | Equipment modifier |

> **Dual-state note:** `combat.py` reads from the `player.py` singleton object, not `world_state["player"]`. Stat changes made to `world_state["player"]` during non-combat gameplay do not automatically propagate to the `Player` object. This is a known tech debt issue.

---

## Enemy Structure

Enemies are dicts defined in `enemy_manager.py`:

```python
{
    "name":          "Goblin",
    "hp":            30,
    "max_hp":        30,
    "damage":        8,
    "crit_chance":   10,        # percent, 1–100 (roll <= crit_chance on a d100)
    "elite":         False,     # enhanced stats flag
    "boss":          False,     # triggers boss behavior
    "status_effects": []        # active effects list
}
```

### Enemy Selection

Enemy selection is world-state aware. `story.py`'s `generate_story()` builds an `enemy_pool` list that expands based on:

| Condition | Added enemy |
|---|---|
| `cult_rising == True` | `"hidden cult"` (×2 weight) |
| `civil_war == True` | `"corrupted knight"` |
| `mages_rebellion == True` | `"necromancer"` |
| `world_chaos >= 70` | `"shadow beast"` (×2 weight) |
| `story_memory.joined_shadow_cult` | Removes `"hidden cult"` |

---

## Status Effects

Defined in `status_effects.py`. Status effects are stored as dicts in an entity's `status_effects` list.

| Effect | Behavior |
|---|---|
| `burn` | Damage over time each round |
| `freeze` | Skip turn probability |
| `stun` | Forced miss this turn |
| `poison` | Damage over time (lower than burn) |
| `bleed` | Damage over time, worsens with movement |
| `slow` | Reduced action frequency |
| `weaken` | Reduced damage output |
| `shield` | Absorbs a set amount of incoming damage |

Effects are resolved in the status phase of each round. Duration is tracked per-effect.

---

## Boss System

### Current Boss: Ashen Guardian

Defined in `bosses.py`. Triggered via `random_boss_encounter()` in `game_loop.py` with a 10% probability after each exploration.

```python
# game_loop.py
def random_boss_encounter():
    if random.random() < 0.10:
        boss_encounter("Ashen Guardian")
```

Bosses use the same `boss_encounter()` function as standard combat but:
- Have higher HP and damage.
- May use special moves.
- Trigger different post-combat events.

Full boss roster is ⚠️ **NOT YET DEFINED** beyond the Ashen Guardian.

---

## Companion Combat

Active companions from `companion_manager.active_companions` attack automatically each round:

```python
# Each companion in active_companions gets a turn
companion_attack(companion_name, enemy)
```

`calculate_party_bonus()` can return aggregate stat bonuses from the party composition.

---

## AI Narration

`llm_bridge.ai_combat_narration(attacker, defender, damage)` is called to print flavour text. Currently returns one of 7 fixed mock strings. Replace the mock with a real LLM call when a model is available.

---

## Encounter Manager

`encounter_manager.py` wraps encounter creation with:

| Function | Description |
|---|---|
| `generate_encounter()` | Creates a standard encounter |
| `generate_narrative_encounter()` | Creates a story-linked encounter |
| `boss_encounter(name)` | Delegates to combat.boss_encounter |
| `ambush_encounter()` | Player-disadvantage start state |

---

## Design Rationale

- Turn-based, synchronous: simple to reason about, no async complexity.
- Enemy dicts (not classes): consistent with the module-level dict pattern; easy to create dynamically.
- AI narration as a drop-in layer: combat flavour text is decoupled from combat logic.

---

## Rules

- Always emit `"enemy_killed"` on enemy death — downstream systems depend on it.
- Never modify `world_state["player"]` HP directly in combat — use `damage_player()` and `heal_player()`.
- Boss encounters are separate code paths from `quick_encounter()`.

---

## Examples

```python
# Standard combat
from combat import quick_encounter
quick_encounter()

# Boss fight
from combat import boss_encounter
boss_encounter("Ashen Guardian")

# Check if player has status effect
if "burn" in [e["type"] for e in player.status_effects]:
    ...
```

---

## Future Expansion

- Full death / game-over / respawn flow.
- Spell system using the `resource` / `max_resource` pool.
- Class-specific combat abilities.
- Multi-enemy encounters.
- Environmental combat modifiers (region weather/biome effects).
- Full boss roster with unique mechanics.
- Combat log / replay summary.

---

## Related Systems

- `player.py` — Player singleton used in combat
- `enemy_manager.py` — Enemy definitions
- `companion_manager.py` — Party combat contributions
- `loot_manager.py` — Post-combat loot
- `progression_manager.py` — XP and level-up
- `event_bus.py` — `enemy_killed` event
- `dm_brain.py` — Pacing response to combat frequency

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation created |
