# Combat & Gameplay Architecture

> **Version 1.0 · Status: TECHNICAL CANON (Implementation Authority) · Priority: Critical**
>
> **Canon hierarchy (R-01, approved 2026-06):** this document + the `tactical/`
> package are the **Technical Canon** — the single combat runtime all future
> combat work builds on. The **Gameplay Canon** (design authority for how combat
> should *feel*) is `docs/GAME_BIBLE.md` + `docs/COMBAT_SYSTEM.md`. The engine
> evolves *additively* to satisfy the gameplay canon; it is never rewritten to
> match an older document. See `docs/design_decisions/R-01-combat-canon.md`.
>
> This is a foundational, canonical design document. From this point forward,
> **every new combat feature must be evaluated against this document before
> implementation.** If a mechanic does not reinforce these principles, it is
> redesigned or rejected.
>
> Implementation lives in the modular, data-driven `tactical/` package. This
> engine is terminal-based, so the spec's *visual* concepts (hover, on-tile
> icons, highlighting) are realized as **text inspection / preview / overlay
> APIs** that deliver the same guarantee: the game never hides tactical
> information. A future graphical client consumes the exact same data model.

---

## Core Gameplay Loop — three modes

1. **Overworld Travel (primary):** travel, landmarks, quests, resources,
   camping, encounters, story progression.
2. **Named Location Exploration (CRPG):** cities/villages/castles/ruins/
   dungeons/caves/temples/story locations — dialogue, quests, loot,
   exploration, shopping, crafting, puzzles. Combat may begin here.
3. **Tactical Combat (separate mode):** may begin from overworld encounters,
   story events, dungeons, settlements, boss fights, scripted encounters.

**All combat uses the exact same tactical systems, regardless of origin.**
After combat: return to the overworld if it started there; return to the
current named location if it started inside one. See
`tactical.engine.CombatContext`.

## Design Philosophy

Combat is *a tactical conversation between the player, the enemy, and the
battlefield.* Players win through **positioning, planning, terrain usage,
team synergy, and environmental interaction** — never through hidden
information.

## Core Combat Pillars

1. **The Battlefield Is a Character.** Terrain is gameplay; every battlefield
   is unique. → `tactical/battlefield.py`, data-driven terrain/objects.
2. **Information Before Commitment.** Before confirming a move the player
   sees movement cost, cover, threats, line of sight, terrain effects, and
   interactions. → `tactical/inspection.py` (`movement_preview`,
   `threat_visualization`, `tactical_overlay`). The game never intentionally
   hides tactical information.
3. **Every Tile Matters.** No meaningless tiles; each may offer cover,
   elevation, hazards, interactions, visibility changes, movement modifiers.
   → the authoritative `tactical.tiles.Tile` model.
4. **Position Wins Battles.** Movement decisions regularly outweigh attack
   decisions (cover, elevation, flanking, threat zones).
5. **The Battlefield Evolves.** Fire spreads, trees burn, smoke appears,
   walls collapse, ice melts/water freezes, bridges break. The battlefield
   at the end differs from the start. → `battlefield.step_environment`.

## Tile Data Model (authoritative source of truth)

Each tile stores: **terrain type, objects present, movement cost, cover
value, elevation, line-of-sight blocking, hazards, interactions, status
effects, current occupant, visibility, environmental state.** All combat
features consume this one model. Terrain and objects are defined in
`tactical/data/terrain.json` and `tactical/data/objects.json` — adding a new
terrain/object/interaction is a data change, not code.

## Information systems (text realization of the visual spec)

* **Tile hover → `inspection.inspect_tile`:** returns terrain, objects,
  movement cost, cover, elevation, status effects, interactions, occupant,
  visibility, and available context actions.
* **On-tile indicators → `render.tile_icon`:** shield=cover, ^=elevation,
  fire/lightning/poison/water hazards, etc., supplementing the tooltip.
* **Movement preview → `inspection.movement_preview`:** path, cost, final AP,
  threat zones entered, cover gained, enemies attackable, enemies that can
  attack the destination.
* **Threat visualization → `inspection.threat_visualization`:** enemies with
  LOS, enemies able to hit a tile, attack ranges, target intent — live.
* **Tactical Inspection Mode → `inspection.tactical_overlay`:** optional
  overlay of movement costs, cover, elevation, enemy vision, hazards, LOS,
  terrain categories.

## Combat Flow

`Start Turn → Survey → Hover/Inspect → Plan → Move → Act (Attack/Skill/Item/
Prepare/Interact) → Environment Reacts → End Turn → Enemy Turn → Battlefield
Updates → Repeat.` Implemented in `tactical.engine.CombatEngine`.

## Actions

`Move · Attack · Skill · Item · Prepare · Interact`. **Prepare** replaces
"Wait" and grants a class-specific reaction: Guardian = Counterattack,
Ranger = Reaction Shot, Mage = Spell Focus, Rogue = Evasion. →
`tactical/actions.py`.

## Battlefield Memory & Persistence

Terrain remembers state (burning tree, destroyed bridge, broken wall, active
smoke, ignited oil) for the whole encounter. Where appropriate, permanent
changes persist to `world_state["tactical"]["persistent"][battlefield_id]`
so a destroyed bridge stays destroyed in the overworld/location.

## Class Philosophy — tactical identity over raw power

* **Guardian:** protects allies, controls space, creates defensive zones.
* **Ranger:** controls line of sight, uses elevation, punishes movement.
* **Mage:** manipulates terrain, creates hazards, changes battlefield state.
* **Rogue:** flanking, ambush, mobility, battlefield disruption.

Defined in `tactical/data/classes.json` + `abilities.json`.

## Character Progression & Loadouts

Abilities are learned **permanently** as characters level (mastered
techniques; never lost). Characters may **equip only a limited number** of
combat abilities at once. **Loadouts may be changed only outside combat**
(overworld, camp, settlements, safe areas) — never during an active
encounter. Enforced in `tactical/classes.py` (`equip_ability` raises if
`in_combat`).

## AI Requirements

Enemy AI uses the **same systems as the player** — it evaluates cover,
elevation, movement, hazards, threats, terrain, LOS, and interactions by
calling the identical battlefield/inspection functions. **AI receives no
hidden gameplay advantages.** → `tactical/ai.py`.

## Development Principles

Modular systems · data-driven architecture · extensible tile metadata ·
reusable combat logic · shared player/AI rules · minimal hardcoded behavior ·
easy addition of new terrain, interactions, classes, abilities, and
environmental effects. Every feature consumes the same tile/battlefield data
model.

## Reactive Combat, Resolve & Partner Techniques (Planned Additive)

> **Core combat pillar** — design authority: [`docs/design/REACTIVE_COMBAT.md`](docs/design/REACTIVE_COMBAT.md)
> + [`docs/COMBAT_SYSTEM.md`](docs/COMBAT_SYSTEM.md). **Planned Additive** on this runtime — not
> yet implemented. It evolves the `tactical/` engine additively (R-01); it does not fork it.

When implemented on this engine, the split follows the existing engine-agnostic discipline:

- **Rules (this runtime — `tactical/`):** a single **shared party Resolve** value; opportunity
  *detection* hooks off existing combat events (flanking, blocks, crits, environmental
  interactions, reactions — several already modelled here); the reaction catalogue and Resolve
  costs; Partner-Technique eligibility (companion pairing + positioning + Resolve + cooldown);
  and applying an authorized action's effects. All headless and testable via the showcase
  harness, like every other tactical system.
- **Presentation (terminal / Godot):** the time-slow decision window, the authorize/decline
  prompt, and the visual + audio + UI-pulse feedback. The slowdown is presentation-only — never
  a rule the engine depends on (Reactive Combat is decision-support, not a QTE).

No parallel combat path: this reuses the one engine, one entry point, one AI pipeline (R-01).
Contracts: [`docs/architecture/ENGINE_INTERFACES.md`](docs/architecture/ENGINE_INTERFACES.md).

## Final Design Principle

> The player should never lose because the game hid information. They should
> lose because they made a tactical decision that, in hindsight, was not the
> best one.

This philosophy guides every combat mechanic, UI decision, and future
gameplay system built on this foundation.
