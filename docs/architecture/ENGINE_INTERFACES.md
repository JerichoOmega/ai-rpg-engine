# Engine Interfaces — Data Contracts

> **Status:** Architecture documentation (2026-06). Additive/non-breaking. Part of
> the architecture doc set — index: [`GODOT_MIGRATION_PLAN.md`](GODOT_MIGRATION_PLAN.md);
> laws: [`LAYER_RULES.md`](LAYER_RULES.md).
> These are the **contracts** between the engine-agnostic core and any presentation
> layer (terminal today, Godot later). Field names below **mirror the real code**
> (see [`tactical/entities.py`](../../tactical/entities.py),
> [`tactical/engine.py`](../../tactical/engine.py),
> [`tactical/facing.py`](../../tactical/facing.py)) so freezing them is a thin
> `to_state()`/`to_dict()` pass, **not** a redesign. Nothing here is implemented by
> this document.

## Reading these contracts
- **State** = a serializable snapshot the engine can render at any time.
- **Event** = a past-tense fact ("what happened") the engine reacts to (animation,
  SFX, popups, camera).
- **Intent** = a request the engine sends *in* ("player wants to move here").
- All contracts are **plain data** (JSON-shaped): primitives, lists, maps. No
  behaviour, no engine references. This is what crosses the Python↔Godot boundary.

---

## STATE contracts

### CharacterState
Snapshot of one combatant. Sourced from `Combatant` (`tactical/entities.py`).
```
CharacterState {
  id: string              # stable unique id (Combatant.id)
  name: string
  cls: string             # archetype: guardian|ranger|mage|rogue|brute|smith|...
  team: "player" | "enemy"
  pos: [x, y]             # grid position
  facing: "N"|"S"|"E"|"W"|null
  hp: int,  max_hp: int
  armor: int
  ap: int,  max_ap: int              # action points (this turn / max)
  move: int, max_move: int           # movement budget (tiles)
  attack: { damage_min: int, damage_max: int, range: int,
            accuracy: float, crit_chance: float }
  statuses: [string]                 # active status effect ids
  cooldowns: { ability_id: turns_remaining }
  prepare_stance: string | null      # e.g. "brace"/"overwatch" reaction stance
  abilities: { learned: [id], equipped: [id], slots: int }
  traits: [string]
  immunities: [string]
  threat: "low"|"medium"|"high"      # (enemies) for UI threat readout
  alive: bool
}
```

### BattlefieldState
Snapshot of the grid. Sourced from `Battlefield`/`tiles.py` + `render.py` data.
```
BattlefieldState {
  id: string
  width: int, height: int
  tiles: [ TileState ]
  units: [ CharacterState ]
  round: int
  in_combat: bool
}
TileState {
  pos: [x, y]
  terrain: string           # plains|water|ice|hill|cliff_top|forest|rubble|road|...
  objects: [string]         # boulder|wall_segment|oil_barrel|bridge_plank|pine_tree
  hazards: [string]         # fire|smoke|...
  cover: "none"|"half"|"full"   # derived; presentation may show shields
  occupant_id: string | null
}
```

### InventoryState / EquipmentState
```
InventoryState { items: [ { id, name, qty, kind } ], gold: int }
EquipmentState { weapon: id|null, armor: id|null, accessories: [id],
                 loadout: [ability_id]   # equipped combat abilities }
```

### QuestState
```
QuestState {
  id: string, title: string
  status: "inactive"|"active"|"complete"|"failed"
  objectives: [ { id, text, done: bool, optional: bool } ]
  flags: { flag_name: value }        # arbitrary story flags
  rewards: [ { kind, id, amount } ]  # granted on completion
  triggers: [string]                 # ids that advance/unlock this quest
}
```

### DialogueState
```
DialogueState {
  node_id: string
  speaker: string                    # character id
  portrait: string | null            # portrait asset key (presentation resolves it)
  text: string
  choices: [ { id, text, enabled: bool, gated_by: flag|null } ]
}
```

### WorldState (overworld)
```
WorldState {
  player: { name, class, level, hp, max_hp, xp, gold, inventory: [id], ... }
  regions: { current_region, discovered: [id] }
  factions: { faction_id: { standing: int, flags: {...} } }
  companions: [ { id, name, role, hp, max_hp, relationship: int } ]
  events: { flag: value }
  time/world_flags: {...}
}
```
> Mirrors the existing `world_state.py` dict — already JSON-serializable.

### SaveState
```
SaveState {
  version: int
  world: WorldState
  quests: [QuestState]
  relationships: { pair_key: value }
  meta: { saved_at, playtime, checksum? }
}
```
> Today: JSON via `save_manager.py` → `save_data.json`. The contract formalizes the
> shape so save/load is engine-neutral and round-trippable (Godot reads the same
> JSON). **Freezing this contract must preserve current save compatibility.**

---

## EVENT contracts (core → presentation)
Events are **past-tense, data-only**. Today they exist informally as
`engine.log` strings and `event_bus.emit(name, **data)`; the migration formalizes
them (see plan P1) **without removing the existing log**.

### CombatEvent (union)
```
CombatEvent =
  | { type:"move",    unit_id, from:[x,y], to:[x,y], path:[[x,y]], cost:int }
  | { type:"attack",  attacker_id, target_id, hit:bool, crit:bool,
                      arc:"front"|"side"|"rear", cover:"none"|"half"|"full" }
  | { type:"damage",  unit_id, amount:int, source_id, kind:"melee"|"ranged"|"hazard" }
  | { type:"heal",    unit_id, amount:int, source_id }
  | { type:"status",  unit_id, status:string, applied:bool, duration:int }
  | { type:"ability", unit_id, ability_id, targets:[id], result:{...} }
  | { type:"death",   unit_id, killer_id|null }
  | { type:"turn",    team:"player"|"enemy", round:int }
  | { type:"environment", tile:[x,y], change:string }   # fire spreads, ice melts...
  | { type:"outcome", winner:"player"|"enemy"|"draw", round:int }
```
> `arc`/`cover`/`crit` already exist in the rules (`facing.py`, hit computation).
> The AnimationEvent below is **derived** from CombatEvents by the presentation
> layer — the core never decides *how long* an animation plays.

### AnimationEvent (presentation-derived, documented for mapping)
```
AnimationEvent { unit_id, clip:"idle|walk|attack|hit|cast|die", facing, at:[x,y] }
```

### DialogueEvent / QuestEvent
```
DialogueEvent { type:"line"|"choice_made"|"end", node_id, speaker, choice_id? }
QuestEvent    { type:"started"|"objective"|"completed"|"failed", quest_id,
                objective_id?, rewards?:[...] }
```

### RewardEvent
```
RewardEvent { xp:int, gold:int, loot:[ {id,name} ], recipients:[unit_id] }
```
> Replaces the direct `print()` of rewards in `combat_bridge._apply_results`: the
> bridge returns a `RewardEvent`; presentation displays it.

---

## INTENT contracts (presentation → core)
The engine translates input/UI into intents; the core validates and resolves them
(exactly what `tactical/session.py` does with keypresses today, via `actions.*`).
```
MoveIntent       { unit_id, to:[x,y] }
AttackIntent     { unit_id, target_id }
UseAbilityIntent { unit_id, ability_id, target_id|target_tile }
PrepareIntent    { unit_id, stance }
UseItemIntent    { unit_id, item_id, target_id? }
EndTurnIntent    { team }
DialogueChoice   { node_id, choice_id }
```
- Intents are **requests**, not guarantees: the core returns the resulting
  events (or a rejection reason) so presentation never assumes success.

---

## Round-trip requirement
For each STATE contract, `deserialize(serialize(x)) == x` must hold once P2 lands.
This is the test that proves the boundary is engine-neutral and that Godot and the
Python core agree on the data. `SaveState` round-trips must additionally preserve
**exact save compatibility**.

## Reactive Combat contract (Resolve / opportunities / techniques)

> Serves the **Reactive Combat** core pillar ([`../design/REACTIVE_COMBAT.md`](../design/REACTIVE_COMBAT.md)). Planned Additive — not implemented.

- **STATE — `ResolveState`:** a single **shared party** integer `resolve` (+ `max`). Not
  per-unit. Round-trips like any STATE contract.
- **EVENT — `resolve_changed`:** `{delta, reason, source_unit_id}` where `reason` is an
  earned source (flank, save, perfect_block, guard_break, crit, environment, reaction,
  positioning, teamwork). Presentation renders visual + audio + UI-pulse; it never invents a
  delta. Passive gain is not representable by contract (there is no "tick" source).
- **EVENT — `opportunity_available`:** `{opportunity_id, source_unit_id, reactions:[{id,
  label, resolve_cost, bark}]}`. Emitted by the core when it detects an opening; presentation
  triggers the time-slow and shows the choices.
- **INTENT — `authorize_reaction(opportunity_id, reaction_id)`** or **`decline_opportunity
  (opportunity_id)`.** Decline is a guaranteed no-op (no state change, no penalty). The core
  validates cost/availability and replies with the resulting events or a rejection reason.
- **STATE — Partner Techniques:** eligibility (`partner_technique_available`) is core-derived
  from companion pairing + positioning + Resolve + cooldown; the cinematic is presentation
  replaying core-authored effect events (determinism preserved).

## Document History
| Date | Change |
|---|---|
| 2026-06 | Authored the engine/gameplay data contracts (CharacterState, BattlefieldState, Inventory/Equipment, QuestState, DialogueState, WorldState, SaveState; Combat/Animation/Dialogue/Quest/Reward events; movement & action intents). Field names mirror existing code. Documentation-only; nothing implemented. |
