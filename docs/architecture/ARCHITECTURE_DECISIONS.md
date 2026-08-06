# Architecture Decision Records (ADR)

> **Status:** Architecture documentation (2026-06). Additive/non-breaking. Part of
> the architecture doc set — index: [`GODOT_MIGRATION_PLAN.md`](GODOT_MIGRATION_PLAN.md).
> This log records **why** major architectural choices were made, so future
> contributors (and future us) understand the rationale — not just the result.
>
> **Format:** each ADR has Context · Decision · Consequences · Status. New
> decisions are **appended**; superseding an ADR adds a new one that references the
> old (never edit history).

---

## ADR-0001 — Engine-agnostic gameplay core
- **Context.** The project is growing past a prototype and will likely target Godot
  as its presentation engine. If rules and rendering entangle, a future port becomes
  a rewrite.
- **Decision.** Keep all game *rules* (combat, AI, status, abilities, quests,
  dialogue state, inventory, save, world/faction/relationship state, events) in an
  **engine-agnostic core** with a strict one-way dependency: `presentation → core`,
  never the reverse. See [`LAYER_RULES.md`](LAYER_RULES.md).
- **Consequences.** Rules stay portable and unit-testable headless; any engine
  (terminal now, Godot later) is a swappable consumer. Costs some indirection at the
  boundary (state/events/intents instead of direct calls).
- **Status.** Accepted. Already largely true for [`tactical/`](../../tactical).

## ADR-0002 — `tactical/` is the single canonical combat runtime
- **Context.** A legacy `combat.py` runtime predates the tactical engine.
- **Decision.** [`tactical/`](../../tactical) is canonical (R-01). Legacy `combat.py`
  is **compatibility-only and must not be extended**; overworld combat routes through
  [`combat_bridge.py`](../../combat_bridge.py) → tactical.
- **Consequences.** One combat code path to maintain and port. Avoids a second,
  divergent engine. The bridge is the only overworld→combat seam.
- **Status.** Accepted.

## ADR-0003 — Combat content is data, not code
- **Context.** Encounters/enemies/classes/abilities must scale without engine edits.
- **Decision.** Keep combat content in [`tactical/data/*.json`](../../tactical/data)
  (`classes`, `enemies`, `abilities`, `ai_profiles`, `terrain`, `objects`,
  `encounters`). Code reads data; content authors edit JSON.
- **Consequences.** New content = a value swap; the same data serves terminal and
  Godot. Requires schema discipline (documented in `ENGINE_INTERFACES`).
- **Status.** Accepted.

## ADR-0004 — The engine boundary is state + events + intents
- **Context.** A Python↔Godot boundary needs stable, serializable shapes, and rules
  must not "reach into" rendering.
- **Decision.** The core communicates only via **State** (snapshots), **Events**
  (past-tense facts), and **Intents** (incoming requests). Contracts:
  [`ENGINE_INTERFACES.md`](ENGINE_INTERFACES.md). Field names mirror existing code so
  freezing them is a `to_state()`/`to_dict()` pass, not a redesign.
- **Consequences.** Presentation can be replaced without touching rules; the same
  contracts enable a parity harness between the headless core and Godot. Adds a
  serialization layer to maintain.
- **Status.** Accepted (contracts drafted; freezing is migration phase P2).

## ADR-0005 — Structured event stream alongside the human log
- **Context.** The engine currently emits **human-readable strings** via
  `engine.log`, and [`event_bus.py`](../../event_bus.py) bakes `print()` into
  `emit()`. Strings are great for the terminal but are **not** a signal source a
  Godot node can bind to, and logic must never parse them.
- **Decision.** Introduce a **structured `CombatEvent` stream additively** (the
  string log stays for the terminal). Route event-bus logging through an
  **injectable sink** (no-op by default) so `emit` carries data, not `print`.
- **Consequences.** Godot binds signals to structured events; the terminal keeps its
  log; nothing existing breaks. This is the **highest-value migration prep** (plan
  P1) and the top readiness blocker to clear.
- **Status.** Accepted (planned, not yet implemented).

## ADR-0006 — JSON save format, engine-neutral
- **Context.** Saves must survive an engine change.
- **Decision.** Keep the **JSON** save format (`save_manager.py` → `save_data.json`),
  formalized as the `SaveState` contract. Godot reads the same JSON via
  `FileAccess`/`JSON`. Any change must preserve save compatibility and pass
  round-trip tests.
- **Consequences.** No migration of save data needed for the port. Constrains save
  contents to JSON-serializable shapes.
- **Status.** Accepted.

## ADR-0007 — Core owns RNG; presentation replays
- **Context.** Deterministic, reproducible encounters power the test harness and
  keep any view in lockstep with the rules.
- **Decision.** The core owns randomness (`CombatEngine.rng`); presentation
  **replays** results from the event stream and never re-rolls.
- **Consequences.** Headless showcases stay the parity oracle for a future Godot
  view; seed-based tests remain valid. Godot must not introduce independent RNG for
  gameplay outcomes.
- **Status.** Accepted.

## ADR-0008 — Non-destructive, incremental migration
- **Context.** The repo has ~29k LOC of legacy runtime plus the clean tactical core;
  a big-bang reorg risks breaking a playable game.
- **Decision.** Treat the current layout as the **production baseline** and the
  target tree (`core/`, `engine/`, `engine/godot/`, `tools/`) as the **documented
  destination**. Move nothing now; reserved dirs are README markers only. Future
  moves happen incrementally with tests green after each step (plan §5), using
  re-export shims so old import paths keep working.
- **Consequences.** The game stays playable throughout; slower than a rewrite but far
  lower risk. Requires discipline to keep steps small and verified.
- **Status.** Accepted.

## ADR-0009 — Canon documentation stays engine-neutral
- **Context.** Character bibles, quests, encounters, and factions must outlive any
  engine choice.
- **Decision.** Canon/design docs describe **rules and story only** — never
  rendering, scenes, UI, or input. Engine details never enter canon; story never
  enters engine adapters.
- **Consequences.** Canon is reusable across engines and safe from refactors. Design
  and technical concerns stay cleanly separated.
- **Status.** Accepted (already true across `docs/`).

## Document History
| Date | Change |
|---|---|
| 2026-06 | Created the ADR log with ADR-0001…0009 (engine-agnostic core, tactical canonical runtime, data-driven content, state/events/intents boundary, structured event stream, JSON save format, core-owned RNG, non-destructive incremental migration, engine-neutral canon). Documentation-only. |
