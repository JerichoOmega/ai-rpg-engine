# The Visible Consequences Rule

> **Canon Status:** CONFIRMED — established July 2026.
> **Authority:** This document establishes a binding design rule for all major questlines. It builds on the outcome-tier canon in [`world_state/CONSEQUENCES.md`](world_state/CONSEQUENCES.md) and the reaction model in [`world_state/WORLD_REACTIONS.md`](world_state/WORLD_REACTIONS.md); how changes are *told* to the player is defined in [`PLAYER_COMMUNICATION.md`](PLAYER_COMMUNICATION.md).
> **Cross-references:** [`CORE_DESIGN_PILLARS.md`](CORE_DESIGN_PILLARS.md) (Pillars 1, 2, 8) · [`docs/systems/quests.md`](../systems/quests.md) · [`docs/systems/journal_system.md`](../systems/journal_system.md)

---

## The Rule

> **Every major questline must produce visible changes in the world.**

Not a number in the save file. Not a line in the epilogue. Something the player can *see, hear, or walk through* when they return to the affected place or people. Players should be able to see the effects of their decisions, not just read about them.

## What "Visible" Means

At least **two of the following channels/categories** (more for campaign-arc quests), chosen to fit the quest. Physical regional changes (roads, refugees, markets, patrols, shrines) are required **where applicable** — a contained personal, investigative, or intra-faction quest may satisfy the rule through NPC dialogue, journal, and other fitting channels instead:

| Change | Examples |
|---|---|
| **Roads reopen or close** | A cleared pass carries caravans again; a lost battle leaves a route marked unsafe and patrolled by scavengers |
| **Refugees appear or return home** | Displaced families camp outside a settlement — or their abandoned farms show lights again |
| **Markets expand or decline** | New goods and merchants after trade is restored; empty stalls and inflated prices after a route falls |
| **Shrines become restored or abandoned** | Shrine state transitions (Maintained / Neglected / Abandoned / Corrupted / Revitalized per [`docs/world/shrine_locations.md`](../world/shrine_locations.md)) — the canon's most legible barometer of regional Faith and Hope |
| **Faction patrols increase or disappear** | Covenant soldiers on a road they previously ignored; goblin warbands gone from a pacified pass |
| **NPC dialogue changes** | Named NPCs reference what happened — with the player's role, accurately attributed |
| **Journal entries update** | The journal records the outcome *and* its ripples as they land ([`docs/systems/journal_system.md`](../systems/journal_system.md)) |

## How It Binds

- **Quest authoring:** every major quest's design must list its visible changes per outcome tier — this is part of the Quest Integration Standard in [`docs/systems/quests.md`](../systems/quests.md). Different outcome tiers produce *different* visible changes, not more/less of the same one.
- **AI DM behavior:** when the party re-enters a region where a major quest resolved, the AI DM must surface at least one visible change unprompted before the player asks.
- **World State:** every visible change is backed by a state change ([`world_state/WORLD_STATE_SYSTEM.md`](world_state/WORLD_STATE_SYSTEM.md)). Never describe a change that isn't recorded; never record a change that is never described (see [`PLAYER_COMMUNICATION.md`](PLAYER_COMMUNICATION.md)).

## The Test

Six in-game weeks after a major quest, drop the player in the affected region with no journal access. Could they reconstruct what they did from the world alone? If not, the quest fails this rule.

---

## Document History

| Date | Change |
|---|---|
| 2026-07-31 | Created — visible-changes rule, change catalogue, binding requirements, and the six-weeks test. |
