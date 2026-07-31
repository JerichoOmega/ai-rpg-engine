# Living World Difficulty System — Folder Index

> **Canon Status:** Confirmed — established July 2026. **Foundational design pillar.**
> **Authority:** This folder is the canonical design reference for the Living World Difficulty System — how the world responds to player action and inaction, and how difficulty emerges from consequence rather than artificial scaling. All future quest, region, faction, companion, and world design documents must reference and comply with this system.
> **Relationship to the technical doc:** [`docs/systems/world_state.md`](../../systems/world_state.md) documents the *runtime* `world_state` object (schema, helpers, save compatibility). This folder documents the *design* the runtime serves. Where implementation lags design, this folder is the target; the systems doc is the current truth of the code.

---

## Core Philosophy

- The player does not choose how difficult the world becomes.
- The world responds naturally to the player's decisions.
- **Difficulty emerges from consequence rather than artificial scaling.**
- The goal is a world that feels alive, interconnected, and believable.
- The player should never feel punished by the game — they should feel that civilization is responding to success and failure.

## File Index

| File | Contents |
|---|---|
| [`LIVING_WORLD_SYSTEM.md`](LIVING_WORLD_SYSTEM.md) | The master document: philosophy, dynamic difficulty, the combat-difficulty separation, developer notes. |
| [`WORLD_STATE_SYSTEM.md`](WORLD_STATE_SYSTEM.md) | What the World State measures (ten categories), what it is not, and implementation status. |
| [`WORLD_REACTIONS.md`](WORLD_REACTIONS.md) | How factions, companions, and the Journal respond to World State changes. |
| [`REGIONAL_ESCALATION.md`](REGIONAL_ESCALATION.md) | Escalation patterns: how ignored threats grow believably (bandits, corruption, the vampire crisis). |
| [`CONSEQUENCES.md`](CONSEQUENCES.md) | Outcome tiers, shrine and settlement consequences, and the canonical quest-integration checklist. |

## The Canonical Design Rules

Every major quest must answer:

1. **If completed:** How does civilization improve?
2. **If ignored:** How does civilization decline?
3. Who is affected?
4. What regions change?
5. Which factions respond?
6. How does the World State evolve?

**If a quest cannot answer these questions, it is not yet fully integrated into the Living World system.**

## Cross-References

- [`docs/systems/world_state.md`](../../systems/world_state.md) — runtime schema (current implementation)
- [`docs/systems/ai_director.md`](../../systems/ai_director.md) — the AI Director enacts world reactions
- [`docs/systems/quests.md`](../../systems/quests.md) · [`docs/systems/dynamic_story_arcs.md`](../../systems/dynamic_story_arcs.md)
- [`docs/world/factions/FACTION_BIBLE.md`](../../world/factions/FACTION_BIBLE.md) — faction World State responses
- [`docs/systems/journal_system.md`](../../systems/journal_system.md) — the Journal as living historical record
