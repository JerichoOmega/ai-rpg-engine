# R-01 — Combat Canon Decision (APPROVED)

> Status: APPROVED · Date: 2026-06 · Type: Level-1 canon ruling
> Supersedes: the ambiguity between `docs/COMBAT_SYSTEM.md` and
> `Combat_Gameplay_Architecture.md`.

## Ruling

Combat has **two distinct kinds of canon**, and both are authoritative in their
own domain:

### 1. Gameplay Canon — *Design Authority*
**`docs/GAME_BIBLE.md` + `docs/COMBAT_SYSTEM.md`.** They define how combat should
ultimately *feel* and the long-term feature set. **Not being replaced.** Covers:
Facing, Flanking, Shield Stance, Downed/Death, Initiative, Support Actions,
four-hero party design, tactical identity, combat pacing, and the **Reactive
Combat** core pillar — *Reactive Combat · Resolve · Command Decisions · Partner
Techniques* ([`docs/design/REACTIVE_COMBAT.md`](../design/REACTIVE_COMBAT.md), the
authoritative spec for that pillar). All of it is **Planned Additive** on the
tactical runtime — evolved onto the one engine additively, never forked.

### 2. Technical Canon — *Implementation Authority*
**`tactical/` + `Combat_Gameplay_Architecture.md`.** The single combat runtime.
All future combat work builds on this engine.

## Rules

* **One** combat engine · **one** combat entry point · **one** enemy framework ·
  **one** player combat pipeline · **one** AI combat pipeline.
* Never rewrite the tactical engine just to match an older document.
* Never remove verified functionality.
* Add missing gameplay-canon mechanics **incrementally & additively**.
* Do not maintain, duplicate, or expand legacy combat implementations.
* The tactical engine evolves until it fully satisfies the gameplay canon —
  through **additive evolution, not replacement**.

## Feature Migration Order (each phase independently testable)

* **Phase A:** Facing · Flanking · Opportunity/Prepare interactions · combat
  readability improvements.
* **Phase B:** Downed state · Death mechanics · Recovery mechanics.
* **Phase C:** Shield Stance · Support Actions · advanced defensive mechanics.
* **Phase D:** Initiative refinements · party management · combat polish.

## Enemy / Ability / AI canon

* **Enemies:** all enemies exist as **Tactical Blueprints** (`tactical/data/
  enemies.json`). Legacy `enemy_manager.enemy_database` becomes a *compatibility
  layer* until retired. No new enemy content targets legacy combat.
* **Abilities:** every future ability targets the tactical framework. No parallel
  implementations.
* **AI:** all combat AI uses `tactical/ai.py`. Legacy combat AI is temporary
  compatibility code only.

## Documentation status taxonomy (use these labels going forward)

| Label | Meaning | Examples |
|-------|---------|----------|
| **Gameplay Canon** | Design authority (how it should feel) | `GAME_BIBLE.md`, `COMBAT_SYSTEM.md` |
| **Technical Canon** | Implementation authority (the runtime) | `tactical/`, `Combat_Gameplay_Architecture.md` |
| **Planned Additive** | Gameplay-canon mechanic not yet in the engine | Facing→Phase A, Downed→Phase B, etc. |
| **Compatibility Layer** | Old code kept working until migrated | `combat.py`, `enemy_manager.py`, legacy combat AI |
| **Deprecated** | Superseded; do not extend | legacy combat expansion, parallel ability impls |

## Success criteria (when the migration completes)

One combat engine, one entry point, one enemy framework, one player pipeline,
one AI pipeline, one authoritative implementation — with the Game Bible as design
authority and `tactical/` as implementation authority, moved into full alignment
by additive evolution.
