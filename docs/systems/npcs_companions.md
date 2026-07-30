# NPC, Companion, Dialogue & Relationship Systems

**Purpose:** Documents the NPC roster, companion party system, dialogue engine, and social relationship tracking.

**Modules:** `npc_manager.py`, `companion_manager.py`, `dialogue_manager.py`, `dialogue_ai.py`, `relationship_manager.py`

---

## Overview

The social layer models the player's relationships with individual NPCs, a companion party system, a dialogue engine with skill checks, and a community-level social state that decays over time. All are independent systems that share `world_state` and the event bus.

---

## NPC System

### NPC Data (`npc_manager.py`)

`NPCS` is a module-level dict defining named NPCs:

```python
NPCS = {
    "Elandor": {
        "role":         "merchant",
        "relationship": 0,
        "history":      [],
        ...
    },
    ...
}
```

### Key Functions

| Function | Description |
|---|---|
| `get_npc(name)` | Return NPC data dict; None if not found |
| `change_relationship(name, amount)` | Adjust NPC relationship score |
| `random_npc_event()` | Trigger a random NPC interaction |

### Import Rule

> `npc_manager.py` imports only `remember_major_event` from `world_state`. It does **not** import the `world_state` object itself. Do not reintroduce that import.

### NPC Roster

⚠️ **NOT YET FULLY DEFINED** — Confirmed NPC: **Elandor** (role: merchant). Full NPC roster, backstories, dialogue trees, and quest connections have not been written.

---

## Companion System

### Companion Data (`companion_manager.py`)

```python
# Module-level
COMPANIONS = {
    "companion_name": {
        "role":      "...",
        "abilities": [...],
        "loyalty":   50,
        ...
    }
}
active_companions = []   # names of currently recruited companions
```

Both are serialized by `save_manager.py` under `"companions"` and `"active_companions"` keys.

### Key Functions

| Function | Description |
|---|---|
| `recruit_companion(name)` | Add companion to `active_companions` |
| `remove_companion(name)` | Remove from active party |
| `companion_attack(name, enemy)` | Companion auto-attacks in combat |
| `use_companion_ability(name, ability)` | Trigger a companion ability |
| `change_loyalty(name, amount)` | Adjust loyalty score |
| `evaluate_loyalty(name)` | Check loyalty threshold; may affect behavior |
| `corrupt_companion(name)` | Apply corruption state to companion |
| `companion_story_reaction(event)` | Companion reacts to a narrative event |
| `calculate_party_bonus()` | Return aggregate party stat bonuses |
| `heal_party()` | Restore HP to all companions |
| `show_party()` | Print current party and stats |
| `random_companion_banter()` | Fire random banter during tick |
| `show_companion_summary()` | Print companion roster and status |

### Companion Roster

⚠️ **NOT YET DEFINED** — The companion infrastructure is in place. No specific companion characters, recruitment locations, abilities, or backstories have been defined.

---

## Dialogue System

### Dialogue Manager (`dialogue_manager.py`)

`npc_relationships` tracks per-NPC relationship values at the dialogue level:

```python
# module level
npc_relationships = {}   # {npc_name: relationship_int}
```

Serialized by `save_manager.py` under `"npc_relationships"` key.

| Function | Description |
|---|---|
| `start_dialogue(npc_name)` | Begin dialogue loop with an NPC |
| `get_npc_relationship(npc_name)` | Return current relationship score |
| `change_npc_relationship(npc_name, amount)` | Adjust relationship |
| `persuasion_check(dc)` | Roll persuasion vs. difficulty class |
| `intimidation_check(dc)` | Roll intimidation vs. difficulty class |
| `dialogue_choice(options)` | Present numbered choice to player |
| `generate_rumor()` | Generate a world-state-aware rumor string |
| `world_state_dialogue()` | Generate dialogue contextual to world conditions |
| `companion_dialogue(companion_name)` | Generate companion-specific dialogue |
| `show_relationships()` | Print all NPC relationships |
| `show_dialogue_summary()` | Print dialogue state overview |

### Dialogue AI (`dialogue_ai.py`)

Wraps `llm_bridge.ai_dialogue()` for generating NPC conversation lines. When called, passes NPC name and context, returning a flavour line from the mock bridge.

### Rumors

`generate_rumor()` in `dialogue_manager.py` produces a text string referencing current world conditions. Called probabilistically by `game_loop.process_game_tick()`.

---

## Relationship System

### Social State (`relationship_manager.py`)

```python
# module level
social_state = {}   # community-level relationship tracking
```

Serialized by `save_manager.py` under `"social_state"` key.

| Function | Description |
|---|---|
| `decay_relationships()` | Called each tick; relationships drift toward neutral |
| `generate_social_event()` | Fire a random community-level event |
| `world_social_reaction()` | Exists in module but is not currently called (dead function) |

### `world_social_reaction()` Status

This function exists in `relationship_manager.py` but is not imported or called anywhere in the current game loop (the import was removed as a dead import). It is available for future use.

---

## Design Rationale

- **Separate NPC relationship (npc_manager) from dialogue relationship (dialogue_manager):** The NPC manager tracks deep per-character data; the dialogue manager tracks the transactional relationship score used in dialogue skill checks.
- **Companion loyalty separate from companion relationship:** Loyalty affects willingness to follow commands; relationship is social closeness. These may diverge in future design.
- **Social state as a community metric:** Rather than tracking every individual townsperson, `social_state` tracks aggregate community standing, which decays naturally.

---

## Rules

- NPC data (NPCS dict) is not serialized by `save_manager.py`. NPC relationship changes through `npc_manager.change_relationship()` will be lost on save/load unless explicitly persisted. This is a known limitation.
- `npc_relationships` (dialogue_manager) IS serialized — it is the persistent relationship score.
- Do not import `world_state` into `npc_manager.py` — only import specific helper functions.

---

## Known Issues

- `npc_manager.py`'s NPCS dict changes are not persisted in the full save.
- `companion_manager.COMPANIONS` changes are persisted, but companion abilities and story reactions are not fully implemented.
- `world_social_reaction()` exists but is unused.

---

## Future Expansion

- Full NPC roster with lore, dialogue trees, and quest hooks.
- Named companions with backstories and recruitment missions.
- Companion relationship arc system (trust building over time).
- Romance / rivalry systems.
- Dynamic rumor propagation through the settlement network.
- NPC memory of player actions (e.g., "I heard you killed the dragon").

---

## Related Systems

- `world_state.py` — Companion party list in `world_state["companions"]`
- `combat.py` — `companion_attack()` called each round
- `faction_manager.py` — Faction reputation affects NPC dialogue tone
- `dialogue_ai.py` / `llm_bridge.py` — AI-generated NPC lines
- `settlement_manager.py` — Settlement rumors feed into `generate_rumor()`

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation; NPCS persistence gap noted |
