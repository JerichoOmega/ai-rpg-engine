# AI Director (DM Brain)

**Purpose:** Documents the pacing and narrative orchestration system that monitors session flow and adjusts story intensity dynamically.

**Modules:** `dm_brain.py`, `llm_bridge.py`, `narrative_ai.py`, `story.py`, `story_manager.py`, `memory_engine.py`, `prompt_manager.py`

---

## Overview

The AI Director is the "Dungeon Master" of the game. It tracks a `story_pressure` value and adjusts its `current_focus` to guide pacing. It is invisible to the player — they feel a responsive world, not an algorithm.

The system was previously split between `ai_director.py` and `dm_brain.py`. These have been merged into `dm_brain.py`. The archive of the original `ai_director.py` is at `archive/legacy/ai_director.py`.

---

## Current Implementation

### DM State

```python
# dm_brain.py
dm_state = {
    "story_pressure":      25,           # 0–100 intensity
    "current_focus":       "exploration",# narrative mode
    "session_length":      0,            # ticks this session
    "last_event_type":     None,         # most recent event category
    "recent_battles":      0,            # battles since last story event
    "recent_story_events": 0,            # story beats since last battle
}
```

### Pressure → Focus Mapping

| `story_pressure` | `current_focus` | Intended Tone |
|---|---|---|
| 0–25 | `"recovery"` | Quiet; encourage exploration and rest |
| 26–50 | `"exploration"` | Standard pacing; discovery and quest |
| 51–75 | `"escalation"` | Building tension; encounters more meaningful |
| 76–100 | `"crisis"` | Peak intensity; major conflict imminent |

Focus is recalculated by `change_story_pressure()` every time pressure changes.

### Key Functions

| Function | Description |
|---|---|
| `change_story_pressure(amount)` | Add or subtract from pressure; recalculate focus; clamp 0–100 |
| `evaluate_story_state()` | Called on quest_completed; notes progression |
| `update_dm_brain()` | Called every game tick; evaluates session and campaign pressure |
| `evaluate_session_flow()` | Checks if session has been too combat-heavy or too quiet |
| `evaluate_campaign_pressure()` | Responds to world-level threats (chaos, war flags) |
| `reset_session_trackers()` | Resets `recent_battles` and `recent_story_events` |
| `show_dm_state()` | Prints the current dm_state to terminal |

### Event Bus Subscriptions

The DM Brain subscribes at module load to:

| Event | Handler | Effect |
|---|---|---|
| `enemy_killed` | `on_enemy_killed` | +5 pressure; increment `recent_battles` |
| `quest_completed` | `on_quest_completed` | Increment `recent_story_events`; call `evaluate_story_state()` |
| `narrative_encounter` | (internal) | Record narrative beat |

---

## LLM Bridge

`llm_bridge.py` is the single point where the game would connect to a real language model.

**Current state: all mock implementations.**

| Function | Signature | Current Behaviour |
|---|---|---|
| `ai_narrate(prompt)` | `prompt: str` | Prints one of 7 fixed narrative strings |
| `ai_generate_quest()` | _(no args)_ | Prints one of 7 fixed quest rumor strings |
| `ai_combat_narration(attacker, defender, damage)` | optional kwargs | Prints one of 7 fixed combat strings |
| `ai_dialogue(npc, context)` | optional kwargs | Returns one of 7 fixed NPC dialogue strings |

**To integrate a real LLM:**
1. Replace the function bodies in `llm_bridge.py` only.
2. No other file needs to change.
3. The `prompt` parameter in `ai_narrate` is the context string to pass to the model.

### Rules for llm_bridge.py
- Contains **no game logic**. State changes happen in the calling module before/after calling llm_bridge.
- No DM Brain state (`dm_state`, pressure logic) belongs here.
- No event bus subscriptions in this module.

---

## Narrative AI

`narrative_ai.py` provides richer contextual narrative than the simple mock lines in `llm_bridge.py`.

| Function | Description |
|---|---|
| `get_world_tone()` | Returns current narrative tone string based on world conditions |
| `narrate_region(region_name)` | Describes a region |
| `narrate_npc(npc_name)` | Describes an NPC |
| `generate_story_hook()` | Creates a narrative premise string |
| `narrate_battle(enemy)` | Generates battle context |
| `narrate_quest(quest_name)` | Describes a quest |
| `on_enemy_killed(event_data)` | Event handler: records narrative beat |
| `on_region_crisis(event_data)` | Event handler: region crisis narrative |
| `on_faction_war_started(event_data)` | Event handler: war narrative |

Subscribes to `enemy_killed` and `region_crisis` at module load.

---

## Story Generation

`story.py` provides `generate_story(enemies, factions, story_memory)` — the main narrative context generator.

### Parameters
- `enemies` — **dict** of `{enemy_name: dict}`. Keys are enemy name strings. Do not pass a list.
- `factions` — dict of `{faction_key: reputation_int}`. Access with `.get(key, 0)`.
- `story_memory` — dict of story flags. Access with `.get(key, False)`.

### What It Returns
A text description of the current narrative context, including: location, quest hook, active enemy type, world modifier context.

### Selection Logic
1. **Location pool** — starts with 6 default locations; expands based on `civil_war`, `cult_rising`, `mages_rebellion`, `world_conditions.world_chaos >= 60`.
2. **Quest pool** — starts with 3 default quests; expands based on faction reputation thresholds and story memory flags.
3. **Enemy pool** — starts from `enemies.keys()`; expands based on `cult_rising`, `civil_war`, `mages_rebellion`, `world_chaos >= 70`; contracts if `joined_shadow_cult` is True (removes hidden cult).

---

## Story Manager

`story_manager.py` tracks the story arc state.

### Story State
```python
story_state = {
    "current_act": 1,         # narrative act number
    "story_flags": {},        # persistent story flags
    "active_arcs": [],        # ongoing story arcs
    ...
}
```

| Function | Description |
|---|---|
| `advance_story(amount)` | Increment story progression |
| `set_story_flag(flag, value)` | Set a story flag |
| `show_story_summary()` | Print current story state |

World events processed in `story_manager` (e.g., "Cult Retaliation") increment `world_state["world_conditions"]["world_chaos"]` by 5.

---

## Memory Engine

`memory_engine.py` stores major events for narrative reference.

Events recorded: enemy deaths, quest completions, major player choices. Used by DM Brain handlers and narrative functions to reference what the player has done.

`memory.py` is a legacy parallel module. New code should use `memory_engine.py`.

---

## Prompt Manager

`prompt_manager.py` holds prompt templates for future LLM integration. Currently a support module that would provide structured prompts to `llm_bridge.py` once a real model is connected.

---

## Campaign Manager

`campaign_manager.py` tracks multi-act campaign progression.

### Campaign State
```python
campaign_state = {
    "current_act":      1,
    "main_threat":      "shadow_cult",
    "campaign_stage":   "emergence",
    "villains": {
        "Varkun": {
            "alive":     True,
            "power":     50,
            "last_seen": "shadow_marsh"
        }
    }
}
```

The villain "Varkun" is confirmed as a character name in the codebase. All other lore around this character is ⚠️ **NOT YET DEFINED**.

---

## Design Rationale

- **Separate pressure from game logic:** `dm_brain.py` is a listener, not an actor. It observes the event stream and adjusts state but does not directly trigger encounters.
- **Mock-first LLM bridge:** The game works without any API key. The LLM layer is additive, not required.
- **Event-driven DM state:** Pressure changes are reaction-based, not scheduled. This prevents artificial timer-driven pacing.

---

## Rules

- Do not add DM Brain logic outside `dm_brain.py`.
- Do not call LLM functions from anywhere except `narrative_ai.py`, `dialogue_ai.py`, and `story.py`.
- `dm_state` is the only AI pacing state dict. Do not create parallel pacing state in other modules.

---

## Dungeon Master Philosophy

The AI Director is **not** responsible for generating completely different stories between playthroughs.

Its role is to **guide, adapt, and personalize** each campaign by responding to player actions and orchestrating dynamic world events. It ensures every playthrough feels natural, coherent, and unique while respecting the established lore and handcrafted narrative backbone.

- It does not invent new lore
- It does not contradict established canon
- It works within the authored world to create variation and meaningful response

See [`docs/CAMPAIGN_DESIGN.md`](../CAMPAIGN_DESIGN.md) for the full philosophy governing the DM's scope.

---

## Campaign Narrative Framework

The AI Director's variation system is directly connected to the game's main story structure. See [`docs/GAME_BIBLE.md — Main Story`](../GAME_BIBLE.md) and [`elyndor/history/the_corruption.md`](../../elyndor/history/the_corruption.md) for full details.

### The Corruption as Campaign Seed

Every campaign shares the same central threat — an imprisoned god's weakening seal leaking The Corruption into the world. What varies between campaigns is **how The Corruption manifests**:

| Corruption type | World state signals | AI Director role |
|---|---|---|
| **Political** | `civil_war`, hostile faction reputations | Emphasize faction conflict, betrayals, oppressive rulers |
| **Natural** | High `world_chaos`, corrupted regions | Emphasize twisted environments, wildlife encounters, crop/settlement failures |
| **Religious** | `cult_rising`, `mages_rebellion` | Emphasize cult spread, fractured alliances, ancient temple events |
| **Arcane** | `mages_rebellion`, unstable magic flags | Emphasize magical disasters, relic activations, mage encounters |

The existing `world_state` flags (`civil_war`, `cult_rising`, `mages_rebellion`, `world_chaos`) already align with these corruption types. Future DM Brain expansion should use these flags to **seed the campaign's corruption emphasis** at campaign start and reinforce it through narrative event selection throughout the playthrough.

### Campaign Manager Connection

`campaign_manager.py`'s `campaign_state` has:
- `"main_threat"` — currently `"shadow_cult"`; should eventually support multiple threat types
- `"campaign_stage"` — currently `"emergence"`; maps to how far the god's influence has spread

These fields are the natural home for tracking which corruption type is dominant in the current campaign.

---

## Dynamic Story Arc Selection

During campaign generation, the AI Dungeon Master selects one or more **Dynamic Story Arcs** for the campaign. These are authored large-scale world events that shape the entire playthrough — regions, factions, companion stories, questlines, and enemy types.

The DM Brain is responsible for:

1. **Selecting arcs** at campaign generation based on campaign parameters (corruption type, companion roster, regional setup)
2. **Seeding world state** to match the selected arcs — setting `world_state` flags that reflect which factions are affected and which crisis is developing
3. **Pacing arc development** — arcs should escalate gradually, not reveal themselves immediately; the DM Brain controls when arc-related events surface
4. **Tracking companion stakes** — which companions have personal connection to the active arc; narrative emphasis should increase when those companions are present
5. **Introducing arc-exclusive content** — campaign-exclusive enemies and locations exist only while their arc is active; the DM Brain gates their appearance appropriately

Not every campaign contains every arc. Campaign identity emerges from the arcs selected.

Arc definitions and design framework: [`docs/systems/dynamic_story_arcs.md`](dynamic_story_arcs.md)

**Current confirmed arcs:**

| Arc | Primary Faction | Corruption Type |
|---|---|---|
| **The Fractured Circle** | Mages Guild | Arcane |

---

## Future Expansion

**Canonical targets (connected to main story framework):**
- Campaign corruption type selected at start; AI Director seeds `world_state` flags to match and reinforces throughout
- Dynamic Story Arc selected at campaign generation; DM Brain paces arc escalation and gates arc-exclusive content
- DM Brain issuing proactive narrative prompts tied to active corruption type (not just reacting to events)
- Multi-act campaign scripting: Corruption grows across acts until confrontation with its source

**Not yet defined:**
- Real LLM integration via `llm_bridge.py` function replacement
- Emotion/relationship tracking to personalize narrative tone
- Persistent DM memory across sessions via `memory_engine.py`

---

## Related Systems

- `event_bus.py` — DM Brain subscribes to combat and quest events
- `world_state.py` — Reads chaos, flags, story_memory
- `game_loop.py` — Calls `update_dm_brain()` and `show_dm_state()`
- `narrative_ai.py` — Parallel narrative system subscribing to same events

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation created; merger of ai_director into dm_brain noted |
| July 2026 | Dynamic Story Arc selection section added; The Fractured Circle confirmed as first arc |
