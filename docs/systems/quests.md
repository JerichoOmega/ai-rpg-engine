# Quest System

**Purpose:** Documents the quest database, tracking, reward flow, generation, and event chain.

**Modules:** `quests.py`, `quest_manager.py`, `quest_generator.py`

---

## Quest Design Philosophy

> **Canon Status:** CONFIRMED — 2026-07-31.

Every quest should matter. Avoid generic filler objectives.

Before approving a quest, it should ideally satisfy most of the following:

| Criterion | Question |
|---|---|
| **Teaches** | Does it teach the player something about the world? |
| **Develops** | Does it develop a character — companion, NPC, or the player's understanding of themselves? |
| **Decides** | Does it present an interesting decision with no obvious correct answer? |
| **Changes** | Does it change the player's understanding of something they thought they knew? |
| **Consequences** | Does it leave a lasting consequence in the world or a relationship? |

Players should remember quests because of their stories, not their rewards. Quest design draws inspiration from **The Witcher 3**: memorable narratives and meaningful consequences over repetitive objectives.

> **The test:** If a quest could be removed from the game without anyone noticing it was gone, it should not be in the game.

---

## Overview

The quest system combines a static quest database with a procedural generation layer and a tracking system embedded in `world_state`. Quest completion drives faction reputation, XP, gold, and narrative events.

---

## Current Implementation

### Quest Database (`quests.py`)

`quest_database` is a module-level dict. Each entry defines a completable quest:

```python
quest_database = {
    "Cult Hunt": {
        "description":       "Defeat members of the Shadow Cult.",
        "target_enemy":      "hidden cult",
        "required_kills":    3,
        "gold_reward":       150,
        "xp_reward":         100,
        "faction":           "shadow_cult",
        "reputation_reward": -15,   # killing cultists harms cult rep
    },
    "Dragon Slayer": {
        ...
    },
    ...
}
```

**Confirmed quests in the database:** Cult Hunt, Dragon Slayer, and others (see `quests.py` for the full list).

### Quest State (`world_state["quests"]`)

```python
world_state["quests"] = {
    "active":    [],    # quest names currently in progress
    "completed": [],    # quest names completed
    "failed":    [],    # quest names failed
    "progress":  {},    # {quest_name: {kill_count: N, ...}}
}
```

### Quest Lifecycle

```
1. Quest is generated / offered to player
        → quest_manager.generate_quest() or quest_generator
        → player accepts → quest_name added to world_state["quests"]["active"]

2. Progress tracked
        → enemy_killed event triggers kill counter update in progress dict

3. Quest complete check
        → update_quests_from_enemy(enemy_name) checks progress thresholds
        → calls reward_quest(quest_name) when threshold met

4. Reward
        → quest marked complete in world_state
        → add_gold(gold_reward)
        → world_state["player"]["xp"] += xp_reward
        → change_faction_reputation(faction, reputation_reward)
        → remember_major_event(quest_name)
        → emit("quest_completed", quest_name=name, quest=quest_data)
```

### Key Functions (`quests.py`)

| Function | Description |
|---|---|
| `initialize_quests()` | Sets up quest tracking state |
| `show_quests()` | Prints all quest statuses |
| `update_quests_from_enemy(enemy_name)` | Increments kill counters; triggers completion |
| `reward_quest(quest_name)` | Awards rewards and emits completion event |
| `handle_enemy_killed(event_data)` | Event handler subscribed to `enemy_killed` |

### Key Functions (`quest_manager.py`)

| Function | Description |
|---|---|
| `generate_quest()` | Offers a quest to the player from available pool |
| `show_active_quests()` | Displays active quest list |

### Quest Generator (`quest_generator.py`)

Procedural layer that can create new quest entries dynamically. Used when the static database is exhausted or for variety. Full procedural generation rules are ⚠️ **NOT YET FULLY DEFINED**.

---

## Quest Completion Event Chain

When `reward_quest()` fires:

```
emit("quest_completed", quest_name=name, quest=quest_data)
  │
  ├── dm_brain.on_quest_completed
  │     → increments recent_story_events
  │     → calls evaluate_story_state()
  │     → prints "DM Brain recognizes story progression"
  │
  ├── faction_manager.on_quest_completed
  │     → quest = event_data.get("quest") or {}
  │     → if quest.get("type") == "faction" and faction:
  │           change_reputation(faction, +10)   # bonus rep
  │
  └── memory_engine (internal)
        → stores "Completed quest: {name}"
```

> **Note on faction bonus:** The +10 bonus from `faction_manager.on_quest_completed` only fires when `quest["type"] == "faction"`. Current `quest_database` entries do not include a `"type"` field. The bonus is forward-compatible infrastructure — add `"type": "faction"` to quest entries to enable it.

---

## World State Integration

- `complete_quest(name)` — moves from `active` to `completed` (idempotent).
- `fail_quest(name)` — moves from `active` to `failed` (idempotent).
- Both are helpers in `world_state.py`.

---

## Design Rationale

- Static database for confirmed quests — predictable, auditable content.
- Procedural generator for variety — extends playability beyond the fixed database.
- Event-bus completion — quest completion effects are distributed across systems without `quests.py` needing to know about DM Brain or factions.

---

## Rules

- Always call `reward_quest()` to complete a quest — never directly manipulate `world_state["quests"]` for completion.
- `reward_quest()` is idempotent: calling it on an already-completed quest returns early.
- `update_quests_from_enemy()` must be called in the `enemy_killed` handler path to track kill-based quests.

---

## Future Expansion

- Add `"type": "faction"` to quest entries to enable the faction bonus handler.
- Timed quests (fail if not completed by a certain day).
- Multi-stage quests with branching.
- Quest log UI with progress bars.
- NPC-assigned quests with relationship consequences.

---

## Related Systems

- `world_state.py` — Quest state lives in `world_state["quests"]`
- `faction_manager.py` — Reputation changes on completion
- `dm_brain.py` — Pacing reaction to quest completion
- `event_bus.py` — `quest_completed` event

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation; faction bonus handler forward-compat noted |
| 2026-07-31 | Quest Design Philosophy section added — five-criterion checklist, Witcher 3 inspiration, canonical design standard |
