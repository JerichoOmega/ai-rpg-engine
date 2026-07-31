# The Living World System

> **Canon Status:** Confirmed — established July 2026. **Foundational design pillar — one of the game's defining features.**
> **Authority:** Master document for the Living World Difficulty System. Supersedes any earlier assumption that difficulty scales with player level, elapsed time, or a chosen difficulty setting.
> **Cross-references:** [`README.md`](README.md) · [`WORLD_STATE_SYSTEM.md`](WORLD_STATE_SYSTEM.md) · [`WORLD_REACTIONS.md`](WORLD_REACTIONS.md) · [`REGIONAL_ESCALATION.md`](REGIONAL_ESCALATION.md) · [`CONSEQUENCES.md`](CONSEQUENCES.md)

---

## Core Philosophy

The game does not primarily become harder because the player selected a higher difficulty. **The world itself changes based on the player's actions and inaction.**

- The player does not choose how difficult the world becomes.
- The world responds naturally to the player's decisions.
- Difficulty emerges from consequence rather than artificial scaling.
- The world must feel alive, interconnected, and believable.
- The player should never feel punished by the game — they should feel that civilization is responding to success and failure.

## Canonical Design Principle

**The game never arbitrarily increases enemy levels or spawns stronger enemies simply because time has passed.**

Every increase in danger must have a believable in-world explanation:

- corruption spreading
- roads becoming unsafe
- military forces becoming stretched thin
- settlements declining
- monster populations increasing
- political instability
- famine
- trade disruption

**The player should always understand *why* the world has become more dangerous.**

## Dynamic Difficulty Philosophy

Difficulty emerges naturally through a causal chain:

> **Player decisions → Regional changes → World reactions → Gameplay consequences**

The game never says: *"Enemies are now stronger."*

Instead the player sees:

- stronger enemy factions
- increased monster activity
- worsening corruption
- deteriorating infrastructure

Everything has an in-world explanation. Escalation patterns: [`REGIONAL_ESCALATION.md`](REGIONAL_ESCALATION.md).

## Traditional Combat Difficulty (Retained, Separate)

Optional combat difficulty settings are retained:

| Setting | Intent |
|---|---|
| **Story** | Narrative-first; forgiving combat |
| **Adventurer** | Standard challenge |
| **Veteran** | Demanding tactical play |
| **Legend** | Maximum tactical challenge |

These settings affect **only**: enemy AI, damage, health, tactical challenge.

They must **never** alter: World State, story outcomes, regional changes, faction behavior, or dynamic world systems.

**Combat difficulty and Living World simulation are independent systems.** This separation is canon and non-negotiable.

## Developer Notes (Canon)

The player does not simply complete quests — they influence the health and resilience of an entire civilization.

**Every playthrough should produce a different version of the continent.** One player may travel thriving cities connected by safe roads and active trade; another may find abandoned villages, dangerous wilderness, fractured institutions, and desperate refugees. **Neither experience is "more correct"** — both are the natural result of the player's priorities and the world's response to them.

This system reinforces the central theme: **civilization survives — or falters — through the choices of ordinary people, not because of destiny or a chosen hero.**

All future quest, region, faction, companion, and world design documents must reference this system.
