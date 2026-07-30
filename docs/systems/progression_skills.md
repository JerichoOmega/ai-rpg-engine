# Progression & Skills System

**Purpose:** Documents the character progression system (XP, levelling), the skill tree, and their current implementation state.

**Modules:** `progression_manager.py`, `skill_tree.py`, `skills.py`

---

## Overview

The progression system tracks the player's experience points and level. The skill tree tracks unlocked skills. Both systems have their infrastructure in place but are not yet fully implemented in terms of combat integration and skill roster.

---

## Current Implementation

### Progression State

```python
# progression_manager.py (module level)
progression_state = {
    # Fields defined at module level; serialized by save_manager.py
    # under "progression" key
}
```

The `progression_state` dict is serialized and deserialized by `save_manager.py`.

### XP Tracking

XP is stored in `world_state["player"]["xp"]`. The threshold for the next level is `world_state["player"]["xp_to_next_level"]` (default: 100).

XP is granted in two places:
1. Post-combat: `world_state["player"]["xp"] += quest_data["xp_reward"]` in `quests.py` (actually on quest completion).
2. On kill (if implemented in combat path): increments XP directly.

### Key Functions (`progression_manager.py`)

| Function | Description |
|---|---|
| `check_level_up()` | Tests if `xp >= xp_to_next_level`; increments level if so |
| `show_progression()` | Prints current level, XP, and threshold |

`check_level_up()` is called by `combat.py` after a successful encounter.

### Level Up Effects

⚠️ **NOT YET FULLY DEFINED** — `check_level_up()` increments the level. Stat growth on level-up (increases to max_hp, attack_bonus, defense, etc.) and threshold scaling have not been finalized beyond the infrastructure.

---

## Skill Tree

### Skill State

```python
# skill_tree.py (module level)
player_skills = {
    # skill_name: {unlocked: bool, level: int, ...}
}
```

`player_skills` is serialized by `save_manager.py` under `"skills"` key.

### Skills Module (`skills.py`)

Defines available skills. The skill roster structure exists in this module.

⚠️ **NOT YET FULLY DEFINED** — The full skill list, unlock conditions, XP/level requirements, and combat integration pathways are not yet implemented. The infrastructure (skill_tree.py, skills.py, player_skills dict) is in place.

### In-Combat Skill Use

Combat's `"2. Use Skill"` option exists in the menu. Full skill-in-combat mechanics are ⚠️ **NOT YET FULLY DEFINED**.

---

## Player Level in world_state

| Field | Location | Notes |
|---|---|---|
| `level` | `world_state["player"]["level"]` | Current level |
| `xp` | `world_state["player"]["xp"]` | Current XP |
| `xp_to_next_level` | `world_state["player"]["xp_to_next_level"]` | Threshold (default 100) |

---

## Design Rationale

- XP in `world_state["player"]` — keeps all player state in one place.
- `progression_manager.py` as a separate module — allows levelling logic to be expanded without touching world_state or combat directly.
- `skill_tree.py` as a state tracker separate from `skills.py` (definitions) — clean separation of data from state.

---

## Rules

- Always call `check_level_up()` after awarding XP, not inside XP award functions.
- Do not modify `player_skills` directly — use skill_tree functions when implemented.

---

## Future Expansion

- Finalize stat growth formula on level-up.
- Scale `xp_to_next_level` with each level.
- Implement full skill roster in `skills.py`.
- Wire skill use into combat's "Use Skill" option.
- Class-specific skill trees (Warrior, Mage, Rogue archetypes).
- Passive skills that modify player stats.
- Skill point allocation system.

---

## Related Systems

- `world_state.py` — Player XP and level live in `world_state["player"]`
- `combat.py` — Calls `check_level_up()` post-victory
- `quests.py` — Awards XP on quest completion
- `save_manager.py` — Serializes `progression_state` and `player_skills`

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation; skill tree marked as infrastructure-only |
