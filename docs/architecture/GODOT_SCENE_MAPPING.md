# Godot Scene Mapping — Gameplay → Scenes / Nodes / Signals

> **Status:** Architecture documentation (2026-06). **Documentation only — nothing
> here is implemented.** Part of the architecture doc set — index:
> [`GODOT_MIGRATION_PLAN.md`](GODOT_MIGRATION_PLAN.md); contracts:
> [`ENGINE_INTERFACES.md`](ENGINE_INTERFACES.md); laws:
> [`LAYER_RULES.md`](LAYER_RULES.md).
>
> This describes **how** the engine-agnostic core would surface inside Godot when
> the port begins. The Python core stays the source of truth for rules; Godot is
> the presentation layer that reads **state**, reacts to **events**, and sends
> **intents** back.

## The pattern
```
Gameplay Module (core)  →  Godot Scene  →  Godot Nodes  →  Animation/UI  →  Signals
        (rules)              (view)          (visuals)       (feedback)     (events)
```
- **State →** how a scene is *built/refreshed* (spawn unit nodes from `CharacterState`).
- **Event →** what a node *plays* (a `damage` event → hit anim + floating number + SFX).
- **Signal (Godot) →** how the player's input becomes an **Intent** back to the core.

Godot never computes rules. It renders state, plays events, and emits intents.

---

## Combat
| Core (engine-agnostic) | Godot Scene | Nodes | Anim / UI | Signals ↔ core |
|---|---|---|---|---|
| `CombatEngine`, `BattlefieldState`, `TileState` | `Battle.tscn` | `TileMap`/`GridMap`, `Camera2D/3D`, `Line2D` (paths), `CanvasLayer` (HUD) | terrain tiles, cover/hazard overlays, movement range highlight | player taps tile → `MoveIntent`; taps enemy → `AttackIntent` |
| `CharacterState` | `Unit.tscn` (one per combatant) | `AnimatedSprite2D`/`Skeleton3D`, `Label` (HP/AP), facing indicator | idle/walk/attack/hit/cast/die from `AnimationEvent` | selection → highlight; hover → threat readout |
| `CombatEvent` stream (`engine.log` → structured, plan P1) | `BattleDirector` node | queue/sequencer | plays events in order: move → attack → damage → death | on animation finished → request next event |
| `abilities_engine` + `UseAbilityIntent` | `AbilityBar.tscn` | `Button` per equipped ability, cooldown radial | disabled when AP/cooldown blocks it (from `CharacterState`) | button pressed → `UseAbilityIntent` |
| `RewardEvent` (from `combat_bridge`) | `VictoryPanel.tscn` | `Label`s, item icons | XP/gold/loot popup | continue → resume overworld |

## Characters & Progression
| Core | Godot Scene | Signals |
|---|---|---|
| `hero_roster`/`player`/progression, `EquipmentState`, `InventoryState` | `CharacterSheet.tscn`, `PartyBar.tscn` | equip change → `loadout` update (validated by core; locked in combat) |

## Quests & Dialogue
| Core | Godot Scene | Nodes | Signals |
|---|---|---|---|
| `QuestState`, `QuestEvent` | `QuestLog.tscn` | objective list, flags | objective done → toast; reward → `RewardEvent` |
| `DialogueState`, `DialogueEvent` | `Dialogue.tscn` | portrait `TextureRect`, `RichTextLabel`, choice `Button`s | choice pressed → `DialogueChoice` |

## World, Factions, Relationships, Events
| Core | Godot Scene | Signals |
|---|---|---|
| `WorldState`, regions/travel | `WorldMap.tscn` | region tapped → travel intent; discovery → reveal |
| factions / companion relationships | `RelationsPanel.tscn` | standing change events → UI update |
| `event_bus` (structured, plan P1) | autoload `EventRouter` | core events fan out to Godot signals; no `print` |

## Save
| Core | Godot | Notes |
|---|---|---|
| `SaveState` (JSON via `save_manager`) | `FileAccess` + `JSON` (or a `Resource`) | same JSON shape; **save compatibility preserved** |

---

## Audio / VFX / Camera (pure presentation — no core counterpart)
These have **no** gameplay module and must never leak into the core:
- **Audio** — an `AudioManager` autoload subscribes to events (`attack`→swing SFX,
  `death`→sting).
- **VFX** — particles/shaders triggered by events; never gate rules on them.
- **Camera** — follows the active unit / frames the action; derived from `pos`
  data, never authoritative over it.
- **Navigation** — Godot pathing is *visual*; the **authoritative path** comes from
  the core's grid pathing in the `move` event.

## Reactive Combat → scenes / nodes / signals

Serves the **Reactive Combat** pillar ([`../design/REACTIVE_COMBAT.md`](../design/REACTIVE_COMBAT.md)); all presentation, driven by core events (Planned Additive).

- **Resolve meter** — a party-level HUD node bound to `ResolveState`; on `resolve_changed`
  it plays the earned-feedback trio (VFX pulse + audio cue + UI pulse). Purely reflective;
  never authoritative over the value.
- **Opportunity prompt** — on `opportunity_available`, presentation enters a **slow-motion**
  time-scale and shows a reaction chooser (labels, Resolve costs, companion bark). The
  slow-motion is a Godot `Engine.time_scale`/tween effect only — the core does not know or
  care that time slowed.
- **Authorize / decline** — the chooser emits `authorize_reaction` / `decline_opportunity`
  intents; decline simply closes the prompt and restores time-scale (no state change).
- **Partner Technique** — a cinematic scene/AnimationPlayer sequence triggered by the
  authorized technique's effect events; it **replays** core-authored results (determinism
  note below), never re-rolls. Companion-trust growth selects richer animation variants.

## Determinism note
The core owns RNG (`CombatEngine.rng`). Godot must **replay** results from events,
never re-roll. This keeps the headless core and the Godot view in lockstep and lets
the showcase harness remain the parity oracle.

## Document History
| Date | Change |
|---|---|
| 2026-06 | Authored the gameplay→Godot scene/node/signal mapping for combat, characters, quests, dialogue, world, save, and pure-presentation systems (audio/VFX/camera/nav). Documentation only; nothing implemented. |
