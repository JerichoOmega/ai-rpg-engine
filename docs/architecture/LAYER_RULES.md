# Layer Rules — Gameplay ⟂ Presentation

> **Status:** Architecture documentation (2026-06). Additive/non-breaking. Part of
> the architecture doc set — index: [`GODOT_MIGRATION_PLAN.md`](GODOT_MIGRATION_PLAN.md).
> These are the **dependency laws** the codebase migrates toward. They describe the
> target discipline; they do **not** change any current behaviour.

## The one law
> **Gameplay depends on nothing above it. Presentation depends on gameplay.**
> Dependencies point one way: `presentation → gameplay`. Never the reverse.

## What "gameplay" means here
The engine-agnostic core: characters, combat rules, AI logic, status effects,
abilities, quests, dialogue **state**, inventory, save system, world state, events,
factions, companion relationships. Pure rules, math, and state.

## What "presentation" means here
Anything a specific engine owns: **rendering, UI, scenes, animation, camera,
audio, input devices, navigation meshes, particle/visual effects.**

---

## Rule 1 — Gameplay may NEVER import or reference presentation
Gameplay modules must not import, call, or assume:
- rendering / drawing / sprites / textures / shaders
- UI / menus / buttons / widgets / HUD / labels
- scenes / nodes / scene trees
- animation systems, animation players, tweens
- camera behaviour, viewport, resolution
- audio / sound / music
- input devices (keyboard, mouse, gamepad, touch)
- engine singletons (`get_node`, `SceneTree`, `Input`, `AudioServer`, …)

**Gameplay exposes data; the engine decides how to show it.**

### Concrete "no-fly" list for the core
- No `print(...)` / `input(...)` inside rules code. *(Output = returned data +
  emitted events; input = intents passed in.)*
- No string formatting intended for a human screen inside decision logic.
- No sleeping, no frame timing, no `await` on engine signals.
- No file dialogs, no clipboard, no OS windows.

## Rule 2 — Gameplay talks to the world through three channels only
1. **State** — queryable, serializable snapshots (see
   [`ENGINE_INTERFACES.md`](ENGINE_INTERFACES.md): `CharacterState`,
   `BattlefieldState`, `QuestState`, …).
2. **Events** — structured facts about what happened (`CombatResult`,
   `AnimationEvent`, `DialogueEvent`, `QuestEvent`). Past tense, data-only.
3. **Intents** — structured requests coming *in* from presentation
   (`MoveIntent`, `AttackIntent`, `UseAbilityIntent`, `DialogueChoice`).

## Rule 3 — Presentation is replaceable
The terminal driver today and Godot tomorrow are **interchangeable consumers** of
the same state/events and producers of the same intents. If swapping the
presentation layer requires touching gameplay code, a layer rule was violated.

## Rule 4 — Data is content; code is rules
Encounters, enemies, classes, abilities, terrain, AI profiles live in
[`tactical/data/*.json`](../../tactical/data). Adding content must not require
engine changes. Presentation may *style* content but never *define* it.

## Rule 5 — Canon stays engine-neutral
Story/design docs (`docs/heroes/`, `docs/quests/`, `docs/canon/`, `docs/design/`,
`docs/world/`) describe rules and narrative only — never rendering. Do not put
engine details into canon, and do not put story into engine adapters.

---

## Presentation-assumption audit (current occurrences)
Documented for later remediation. **No fixes are applied by this document.**

| Location | Assumption / coupling | Engine-neutral alternative |
|---|---|---|
| `tactical/session.py` | Terminal turn loop: `print` map/log, `input()` for commands | Move to `engine/terminal/`; feed the core **intents**, render from **state + events**. |
| `tactical/render.py` | ASCII glyphs for tiles/units | Keep as the terminal renderer; Godot reads the same `BattlefieldState`/tile data and draws sprites. Already isolated. |
| `combat_bridge.py` (`_apply_results`, encounter banner) | `print(...)` of victory/defeat/loot/XP directly in orchestration | Return a `CombatOutcome`/`RewardEvent`; let the caller's presentation display it. |
| `event_bus.py` (`emit`) | `print("[EVENT] …")` baked into the bus; also `clear_event_bus`/`show_registered_events` print | Inject a **logging sink** (no-op by default); the bus emits data, a subscriber decides whether/how to log. |
| `world_actions.py`, `game_loop.py` (legacy runtime) | Rules and screen I/O interleaved (`print`/`input` throughout) | Extract decision logic into pure functions returning data; a driver renders + collects input. Incremental. |
| `hub.py`, `hero_select.py`, `shop.py`, `preview.py`, etc. | Menu/flow modules built around terminal prompts | Presentation modules by nature → live in `engine/terminal/`; keep their *rules* (pricing, roster) in the core. |

> Everything under [`tactical/`](../../tactical) **except** `render.py`,
> `session.py`, `demo.py`, and dev I/O in `verify.py` already complies with Rules
> 1–2 today (0 `print`/`input`, no engine imports). That is the model the rest of
> the project migrates toward.

## Enforcement (future, optional)
A lightweight import-lint could later assert that modules under `core/` never
import `engine/`, and that rules code contains no `print`/`input`. Documented as a
recommendation only; not implemented here.

## Document History
| Date | Change |
|---|---|
| 2026-06 | Authored the gameplay⟂presentation layer rules and the current presentation-assumption audit. Documentation-only; no code changed. |
