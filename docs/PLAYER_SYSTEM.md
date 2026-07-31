# Player System

> **Document Status:** Canonical design decision as of July 2026.  
> **Authority:** This document governs all decisions about how players interact with their character. Do not contradict it without an explicit update.  
> **Cross-references:** [`docs/GAME_BIBLE.md`](GAME_BIBLE.md) · [`docs/characters/`](characters/) · [`DESIGN_DECISIONS.md`](../DESIGN_DECISIONS.md)

---

## Overview

This document defines the player character philosophy for the initial version of the game and establishes the architecture requirements for future expansion.

There are two phases:

| Phase | Status | Description |
|---|---|---|
| **Phase 1 — Predefined Hero Roster** | ✅ **CURRENT SCOPE** | Players choose from a roster of confirmed, story-driven heroes |
| **Phase 2 — Custom Hero** | 🔵 **FUTURE — OUT OF SCOPE** | Fully customizable player character; planned but not designed yet |

---

## Phase 1 — Predefined Hero Roster

### Philosophy

For the initial version of the game, players will select from a roster of **predefined, story-driven heroes**.

Each playable hero is a fully realized character. They are not blank slates. They have:

- A unique identity
- A defined backstory
- A predetermined class
- A unique visual design
- Their own personality
- Story-specific dialogue where appropriate
- A fixed starting equipment loadout

The game begins with the player **selecting one of these heroes** before starting the adventure.

### Why Predefined Heroes

Predefined heroes allow for:
- Deep companion interactions — other party members know who you are
- Meaningful story integration — the hero's backstory can intersect with quests and factions
- Distinct playstyles per hero — each hero's class and equipment are designed together
- Polished writing — dialogue and story beats are authored specifically for each hero

### The Hero Roster

Five confirmed playable heroes. Full character sheets: [`docs/characters/`](characters/)

| Hero | Race | Class | Defining Trait |
|---|---|---|---|
| [Talos](characters/talos.md) | Elf | Knight | Jaded veteran; protective; warm underneath |
| [Eleanor](characters/eleanor.md) | Human | Mage | Young, optimistic; unusually strong elemental bond |
| [Ragash](characters/ragash.md) | Orc | Houndmaster | Blunt and proud; devoted to her hounds above all |
| [Ronan](characters/ronan.md) | Human | Werewolf | Cursed drifter; seeks a cure; fears losing control |
| [Torren](characters/torren.md) | Human | Master Blacksmith | Calm, reliable; builds what endures; the party's craftsman |

### Hero Selection Flow

At the start of a new game, the player is presented with the hero roster and selects one hero before the adventure begins. The selected hero determines:

- Starting class and combat stats
- Starting equipment loadout
- Story dialogue and companion reactions
- Any hero-specific quest hooks or faction relationships

### Development Priority

Current development should focus on making the predefined heroes feel **polished**. Priority order:

1. **Hero identity** — the hero should feel like a distinct person, not a stat block
2. **Story integration** — the hero's history and personality should surface in quests and dialogue
3. **Combat uniqueness** — each hero's class should produce a meaningfully different combat experience
4. **Companion interactions** — party members should react to and reference the chosen hero
5. **Distinct playstyles** — each hero's abilities should reward different strategies

**Quality is more important than quantity.** Five well-realized heroes are worth more than ten shallow ones.

---

## Phase 2 — Custom Hero System

### Status

⚠️ **OUT OF SCOPE FOR PHASE 1.** This feature is **intentionally not being designed or built** for the first playable version.

Do not:
- Add custom hero UI or screens
- Add character creation flows
- Design appearance or background selection systems

Document it here as a future goal only.

### Planned Features (Future Reference)

When eventually implemented, the Custom Hero system may include:

- Character name
- Appearance customization
- Class selection
- Background selection
- Cosmetic customization

These remain undecided design goals. No specific design for this system exists yet.

---

## Architecture Requirement

Although the Custom Hero system is postponed, the game's architecture should be designed so it can be integrated later **without requiring major rewrites**.

### Rule

> Avoid hard-coding assumptions that every playable character must always be predefined.

The hero framework should support both:
- **Canonical story heroes** — predefined, story-driven characters from the confirmed roster
- **Future custom-created heroes** — user-defined characters yet to be implemented

### In Practice

- Do not write code that assumes hero name, class, or backstory are constants
- Store hero identity in data (world_state or a hero config dict), not hardcoded strings
- A custom hero should eventually be able to be loaded in the same code path as a predefined hero
- Keep class selection, stat initialization, and equipment loadout data-driven rather than per-hero hardcoded logic

---

## Party System

### Active Party Size

The player controls **four active heroes** during combat.

- The player selects their chosen hero at the start of a new game
- Companions are recruited during play and join the available roster
- The player freely configures which four heroes form the active party — outside combat only
- Party swapping is **disabled during combat**; the active party is locked until the encounter ends

Heroes not in the active party remain on the bench and are available for future deployment.

### Recruitment Philosophy

**Not every hero is guaranteed to appear in every campaign.**

Recruitment opportunities may vary between playthroughs based on story decisions and encounter outcomes. This is intentional — different parties should produce meaningfully different experiences and increase replayability.

Do not assume all five heroes are always available. Design story and quest content with the possibility of a partial roster in mind.

See [`docs/COMBAT_SYSTEM.md`](COMBAT_SYSTEM.md) for full party combat rules.

---

## Relationship to Companions

The playable hero is distinct from companions:

| | Playable Hero | Companions |
|---|---|---|
| Selected at | New game start | Recruited during play |
| Count | 1 (the player's character) | Up to 3 others in active party (4 total) |
| Combat role | Player-controlled | Player-controlled (all four active heroes) |
| Character depth | Deep (story-integrated) | Also deep (see character sheets) |

The hero and companions are all members of the confirmed playable cast. See [`docs/characters/`](characters/) for all character sheets.

---

## Document History

| Date | Change |
|---|---|
| July 2026 | Created — established Phase 1 hero roster philosophy and Phase 2 architecture requirement |
