# Player Communication Standard

> **Canon Status:** CONFIRMED — established July 2026.
> **Authority:** Binding rule for how world changes are communicated to the player. Partner document to [`VISIBLE_CONSEQUENCES.md`](VISIBLE_CONSEQUENCES.md): that rule says the world must change; this one says the player must be able to understand *that* it changed and *why*.
> **Cross-references:** [`VISIBLE_CONSEQUENCES.md`](VISIBLE_CONSEQUENCES.md) · [`../companions/COMPANION_REACTIVITY_STANDARD.md`](../companions/COMPANION_REACTIVITY_STANDARD.md) · [`docs/systems/journal_system.md`](../systems/journal_system.md) · [`world_state/WORLD_REACTIONS.md`](world_state/WORLD_REACTIONS.md) · [`REACTIVE_COMBAT.md`](REACTIVE_COMBAT.md)

> **Combat feedback (Reactive Combat pillar):** the same "the player must understand what
> happened and why" rule governs combat. Every **Resolve** gain must be communicated with
> **visual feedback + an audio cue + a UI pulse** so the player always knows they *earned* it,
> and every opportunity prompt must clearly show the available reactions and their Resolve
> costs before the player authorizes or declines ([`REACTIVE_COMBAT.md`](REACTIVE_COMBAT.md)).

---

## The Rule

> **The player should never wonder why the world has changed.**
>
> **Never rely solely on hidden variables.** Every meaningful state change must reach the player through at least one in-fiction channel.

Hidden variables may *drive* the simulation; they may never be its only expression. If a change matters enough to record, it matters enough to communicate.

## The Channels

Whenever possible, communicate changes through (in rough order of preference — diegetic first):

| Channel | Best for |
|---|---|
| **NPC dialogue** | Local changes; attribution of cause ("since the pass reopened…") |
| **Visual world changes** | Anything a returning player can see: markets, patrols, shrines, roads ([`VISIBLE_CONSEQUENCES.md`](VISIBLE_CONSEQUENCES.md)) |
| **Companion conversations** | Changes the party witnessed or caused; emotional framing ([`../companions/COMPANION_REACTIVITY_STANDARD.md`](../companions/COMPANION_REACTIVITY_STANDARD.md)) |
| **Journal updates** | The durable record — outcome and ripples as they land ([`docs/systems/journal_system.md`](../systems/journal_system.md)) |
| **Rumors** | Distant or uncertain changes; deliberately imperfect information |
| **Notices** | Official/institutional changes: bounties, edicts, closures, festivals |
| **Merchant comments** | Economic ripples: prices, scarcity, new goods, dead routes |
| **Frontier reports** | Regional escalation and security changes reaching settled areas |

## Craft Rules

1. **Two channels for major changes.** A major change (quest outcome, regional escalation shift, faction stance change) reaches the player through at least two channels — one immediate, one persistent (usually the journal).
2. **Attribution without narration.** Characters explain changes in their own understanding — which may be partial or wrong in interesting ways — but the *true* cause must be discoverable. Never have the world be confused about something the player did openly.
3. **Distance degrades fidelity.** Nearby changes are seen; distant changes arrive as rumor and report, later and less accurately. This is a feature: the information landscape is part of the Living World.
4. **No omniscient narrator dumps.** The AI DM should not announce state changes out of fiction ("Your reputation with X has decreased"). Mechanical summaries live in the journal; the world speaks in-world.
5. **Timing.** Communicate when the player can act on or feel the change — on re-entering a region, at camp, at the next settlement — not as an interrupt at the moment a variable ticks.

## The Test

Ask of any state change: *"Where would a player learn this, and would they understand why it happened?"* If the only answer is "by inspecting the save file," the change is not done.

---

## Document History

| Date | Change |
|---|---|
| 2026-07-31 | Created — channel catalogue, five craft rules, two-channel requirement, and the discoverability test. |
