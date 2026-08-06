# Godot Migration Plan — Engine-Agnostic Core

> **Status:** Architecture documentation (2026-06). **Additive and non-breaking.**
> This document introduces **no gameplay, combat, AI, quest, save, or canon
> changes.** It is the **index** for the architecture doc set and records the audit,
> the target architecture, the migration roadmap, the risks, and the **Godot
> Readiness Assessment.**
>
> **This is not a rewrite into Godot.** The goal is to keep the game *rules*
> portable and testable so Godot can later become a pure **presentation layer.**

## Architecture doc set (index)
| Document | Purpose |
|---|---|
| **GODOT_MIGRATION_PLAN.md** *(this file)* | Audit, target architecture, dependency flow, roadmap, risks, effort, readiness assessment. |
| [`LAYER_RULES.md`](LAYER_RULES.md) | The dependency laws (what gameplay may/may not import) and the presentation-assumption audit. |
| [`ENGINE_INTERFACES.md`](ENGINE_INTERFACES.md) | Data contracts between the engine-agnostic core and any presentation layer (CharacterState, CombatResult, AnimationEvent, DialogueState, QuestState, SaveState…). |
| [`GODOT_SCENE_MAPPING.md`](GODOT_SCENE_MAPPING.md) | How each gameplay system would map to Godot scenes / nodes / signals (documentation only). |
| [`ARCHITECTURE_DECISIONS.md`](ARCHITECTURE_DECISIONS.md) | ADR log — *why* the major architectural choices were made. |

Design authority remains: gameplay/design → [`docs/GAME_BIBLE.md`](../GAME_BIBLE.md) ·
[`docs/COMBAT_SYSTEM.md`](../COMBAT_SYSTEM.md); combat technical authority →
[`tactical/`](../../tactical) + [`Combat_Gameplay_Architecture.md`](../../Combat_Gameplay_Architecture.md).

---

## 1. The principle
> **The engine asks the gameplay layer what happens. The gameplay layer never
> depends on the engine.**

```
Engine-Agnostic Game Logic            Presentation Layer (Godot, or the
(rules, math, state, data)      ->    current terminal driver)
  Characters, Combat Rules, AI,       Scenes, UI, Input, Animation, Audio,
  Status, Abilities, Quests,          VFX, Camera, Navigation, Rendering
  Dialogue State, Inventory,
  Save System, World State,           consumes DATA and EVENTS emitted by
  Events, Factions, Relationships     the gameplay layer; sends INTENTS back
```

Dependencies point **one way**: presentation → gameplay. Never the reverse.

---

## 2. Audit — current state (evidence-based)

### 2a. The tactical combat core is already engine-agnostic
The canonical combat runtime [`tactical/`](../../tactical) is a clean, testable,
**pure-logic package** with presentation deliberately isolated:

| Module | Role | Presentation coupling |
|---|---|---|
| `engine.py`, `entities.py`, `actions.py`, `ai.py`, `battlefield.py`, `abilities_engine.py`, `tiles.py`, `facing.py`, `inspection.py`, `encounters.py`, `enemies.py` | Rules, state, math, AI | **None** — no `print`, no `input`, no engine import |
| `render.py` | ASCII realisation of tile data | **Presentation** (isolated; self-documents "a future graphical client would render sprites from the same tile data") |
| `session.py` | Interactive terminal driver / turn loop | **Presentation** (the ~30 `print`/`input` calls live here, by design) |
| `showcase.py`, `showcase_forge.py`, `showcase_lost_howl.py` | Headless vertical slices | **None** — 0 `print`; proves the logic runs with zero I/O |
| `verify.py`, `demo.py` | Dev harness / demo | Dev-only I/O |

**Key evidence of readiness:** the three showcase encounters (Sundered Span, Forge
Stand, Lost Howl) run to completion, produce outcomes, and are unit-tested
**without any presentation layer at all.** The engine's output channel is
`engine.log` (a list of strings) plus queryable state — not screen writes.

- Combat is **data-driven** from [`tactical/data/`](../../tactical/data)
  (`classes.json`, `enemies.json`, `abilities.json`, `ai_profiles.json`,
  `terrain.json`, `objects.json`, `encounters.json`) — content is data, not code.
- **No graphics-engine lock-in anywhere** in the repo: no `curses`, `pygame`,
  `tkinter`, `blessed`, etc. Presentation is plain stdout. This is the single
  biggest thing in the project's favour for a future Godot port.

### 2b. The legacy overworld runtime mixes rules with terminal I/O
The root-level runtime (~29k LOC of managers + LLM DM systems) is the **original
terminal game** and is **presentation-coupled**:

- `world_actions.py` (~41 `print`/`input`), `game_loop.py` (~22) — game flow and
  screen output are interleaved.
- `combat_bridge.py` — the overworld→tactical glue. Its *logic* is clean
  (build encounter from `world_state`, run it, write back HP/XP/gold/loot), but it
  emits player-facing `print()` lines directly (`_apply_results`, encounter banner).
  These are **presentation leaks in an orchestration layer.**
- `event_bus.py` — a real global pub/sub (`subscribe`/`emit`/`unsubscribe`) but
  `emit()` calls `print("[EVENT] …")`, i.e. logging is baked into the bus.

### 2c. State & save are portable
- `world_state.py` / `state_manager.py` / `save_manager.py` are **JSON-backed**
  (`save_data.json`). JSON persistence is engine-neutral and ports to Godot's
  `FileAccess`/`JSON` or resource files with no format change required.
- Canon/design docs (`docs/heroes/`, `docs/characters/`, `docs/quests/`,
  `docs/world/`, `docs/canon/`, `docs/design/`) are **already 100% engine-neutral** —
  they describe rules and story, never rendering. No change needed.

### Audit summary
| Area | Engine-independence today |
|---|---|
| Tactical combat core (`tactical/*` minus render/session) | **~90%** (already clean) |
| Tactical vertical slices (showcases) | **~95%** (headless, tested) |
| Combat data (`tactical/data/*.json`) | **100%** |
| Save / state (JSON) | **~85%** (portable format; some logic entangled with prints) |
| Canon / design documentation | **100%** |
| Overworld runtime (`world_actions`, `game_loop`, managers) | **~40%** (logic recoverable; heavy I/O interleave) |
| Combat bridge (`combat_bridge.py`) | **~70%** (clean logic, presentation leaks) |
| Event bus (`event_bus.py`) | **~60%** (real bus; `print` baked into `emit`) |

---

## 3. Target architecture (desired)
```
core/                 # engine-agnostic game logic (pure Python, no I/O)
  combat/             # <- promote tactical/ rules here over time
  characters/         # character state, progression, loadouts
  ai/                 # enemy AI, DM/narrative decision logic (data in/out)
  systems/            # status effects, abilities, inventory, economy
  quests/             # quest state machine, objectives, flags, rewards
  world/              # world state, regions, factions, relationships, events
  save/               # serialize/deserialize SaveState (engine-neutral)
engine/               # presentation adapters (thin; consume core data/events)
  terminal/           # today's ASCII driver (render.py + session.py move here)
  godot/              # FUTURE: GDScript/C# presentation (empty, reserved)
tools/                # harnesses, validators, report scripts, showcases
docs/architecture/    # this doc set
```
> **No file moves are performed by this plan.** The current layout is the
> **production baseline**; the tree above is the **documented destination**. Every
> move happens later, incrementally, with tests green after each step
> (see §5). Reserved root folders `core/`, `engine/`, `engine/godot/`, `tools/`
> have been created **empty** (README markers only, no code, not importable).

**Dependency flow (target):** `engine/*` → `core/*`. `core/*` → nothing outside
`core/` and the standard library. See [`LAYER_RULES.md`](LAYER_RULES.md).

---

## 4. Engine interfaces (summary — full spec in ENGINE_INTERFACES.md)
The boundary is **data + events**, never method calls into rendering:

- **Gameplay exposes state** — e.g. `CharacterState` (hp, ap, statuses, facing,
  position, equipment), `BattlefieldState`, `QuestState`, `DialogueState`,
  `InventoryState`, `WorldState`.
- **Gameplay emits events** — e.g. `CombatResult` (damage/heal/status/move/death),
  `AnimationEvent`, `DialogueEvent`, `QuestEvent`. Today these live informally in
  `engine.log` (strings) and `event_bus.emit`.
- **Presentation sends intents back** — e.g. `MoveIntent`, `AttackIntent`,
  `UseAbilityIntent`, `DialogueChoice`. Today `session.py` turns keypresses into
  `actions.*` calls; in Godot the same intents arrive from input/UI signals.

Full contracts: [`ENGINE_INTERFACES.md`](ENGINE_INTERFACES.md).

---

## 5. Migration roadmap (incremental, non-breaking)
Each phase keeps the game **playable and tests green** before the next begins.

| Phase | Goal | Work | Verification |
|---|---|---|---|
| **P0 (this doc)** | Establish rules & destination | Doc set + reserved dirs; **no code moves** | Docs validated; full pytest unchanged |
| **P1** | Formalize the event stream | Introduce a structured `CombatEvent` alongside `engine.log` (additive — strings stay). Route `event_bus.emit` logging through an injectable sink instead of `print`. | Showcases still pass; new event assertions |
| **P2** | Freeze the interfaces | Write `ENGINE_INTERFACES` contracts as thin dataclasses/`to_dict()` on existing objects (e.g. `Combatant.to_state()`). No behaviour change. | Serialize→deserialize round-trip tests |
| **P3** | Extract presentation | Move `render.py`/`session.py` behind an `engine/terminal/` adapter that only consumes state+events. Combat core imports nothing presentation. | Terminal game identical; core has 0 I/O |
| **P4** | Promote core packages | Physically relocate `tactical/*` rules into `core/combat/` etc. via re-export shims (old import paths keep working). | Imports resolve; full suite green each move |
| **P5** | Godot presentation | Stand up `engine/godot/` consuming the frozen contracts; port scene-by-scene. Python core remains source of truth during bring-up (or is transpiled/embedded). | Parity harness: Godot vs headless core |

**Guiding rule:** never break a working slice to advance a phase. If a step can't
be made non-breaking, it is split into smaller steps.

---

## 6. Risks
| Risk | Severity | Mitigation |
|---|---|---|
| Legacy runtime logic/IO entanglement | High | Extract logic behind pure functions before any move; adapters last. |
| Two combat paths (`tactical/` vs legacy `combat.py`) | Medium | Legacy `combat.py` is compatibility-only; do **not** extend it (R-01). Everything routes through `combat_bridge` → `tactical`. |
| `engine.log` strings used as an API | Medium | Add structured events **alongside** strings (P1); never parse the human log for logic. |
| Python↔Godot language boundary | Medium | Freeze data contracts (P2) first; the boundary is JSON-shaped data, not objects. |
| Save-format drift during refactor | Medium | `SaveState` contract + round-trip tests before touching persistence. |
| Scope creep into a premature rewrite | High | This is documentation + reserved dirs only; code moves are later, incremental, verified. |

---

## 7. Effort estimate (order-of-magnitude)
| Phase | Complexity | Rough effort |
|---|---|---|
| P0 | Trivial | Done (docs) |
| P1 event stream | Low–Medium | ~1–2 focused sessions |
| P2 interfaces | Medium | ~2–3 sessions |
| P3 presentation extraction | Medium | ~2–4 sessions |
| P4 core promotion | Medium–High | incremental, many small verified steps |
| P5 Godot bring-up | High | the real port; scene-by-scene, ongoing |

---

## 8. Vertical slices — must remain gameplay-first
The following are **gameplay showcases, not engine features**, and must stay valid
and headless after any architecture work:

- **The Sundered Span** — [`gold_standard_sundered_span.md`](../design/encounters/gold_standard_sundered_span.md) · `tactical/showcase.py`
- **The Forge Stand** — [`forge_stand_torren.md`](../design/encounters/forge_stand_torren.md) · `tactical/showcase_forge.py`
- **The Lost Howl / Lost Wolf (Bram)** — [`the_lost_wolf_bram.md`](../design/encounters/the_lost_wolf_bram.md) · `tactical/showcase_lost_howl.py`

They are the **regression fixtures** for the migration: if a slice still runs
headless and its tests pass, the core stayed engine-agnostic.

---

## 9. Canon / gameplay separation (verified)
Canon documentation (character bibles, quests, encounters, factions, production
docs) describes **rules and story** and never references rendering, scenes, UI, or
input. It is **usable regardless of engine** and requires **no change** for this
migration. Keep it that way: never put engine details into canon docs, and never
put story into engine adapters.

---

## 10. Godot Readiness Assessment
> Snapshot at P0. Agent-assessed from the audit above; not a user-set gate.

- **Current readiness: ~55% overall.**
  - Tactical combat core & slices: **~90%** (already engine-agnostic, tested headless).
  - Combat data & canon docs: **~100%** (fully portable).
  - Save/state format: **~85%** (JSON is engine-neutral).
  - Overworld runtime: **~40%** (logic is recoverable but interleaved with I/O).
- **Major blockers:**
  1. `engine.log`/`event_bus` are human-string / `print`-based, not a structured
     event stream a Godot node can bind signals to. *(Highest-value fix — P1.)*
  2. Presentation (`print`/`input`) interleaved through the overworld runtime and
     leaking into `combat_bridge`/`event_bus`.
  3. No frozen data contracts yet (objects are passed directly; fine internally,
     but a language boundary needs stable serialized shapes).
- **Recommended next steps:** do **P1** (structured `CombatEvent` alongside the
  existing log; injectable event sink to remove `print` from `emit`) and **P2**
  (freeze the [`ENGINE_INTERFACES.md`](ENGINE_INTERFACES.md) contracts as
  `to_state()`/`to_dict()` on existing objects). Both are additive and low-risk.
- **Estimated migration complexity: Medium.** The absence of any graphics-engine
  lock-in and the already-clean, data-driven, headless-tested tactical core make
  this a favourable port; the effort concentrates in decoupling the legacy
  overworld runtime, not in the combat engine.

## Document History
| Date | Change |
|---|---|
| 2026-06 | Created the engine-agnostic architecture doc set and Godot migration plan (audit, target architecture, roadmap, risks, effort, readiness ~55%). Additive/documentation-only; reserved `core/`, `engine/`, `engine/godot/`, `tools/` dirs (README markers only). No gameplay/combat/AI/quest/save/canon changes. |
