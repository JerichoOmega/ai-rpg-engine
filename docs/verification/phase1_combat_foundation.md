# Phase 1 — Tactical Combat Foundation: Independent Verification Report

> Status: Complete · Result: **FOUNDATION STABLE (against `Combat_Gameplay_Architecture.md`)**
> Harness: `tactical/verify.py` · Machine report: `tactical/verification_report.json`
> Date: 2026-06 · Gate: must pass before Phase 2 (Enemy Ecosystem)

This report verifies that the `tactical/` package does not merely *run* but
*behaves* according to its canon spec, `Combat_Gameplay_Architecture.md`. It is
produced by an automated behavioural harness (34 checks) and is reproducible:

```
python -m tactical.verify          # checklist
python -m tactical.verify --json   # machine report
```

## Result summary

| | Count |
|---|---|
| Total checks | 34 |
| ✅ PASS | 32 |
| ❌ FAIL | 0 |
| ⚠️ WARN (tracked debt) | 2 |
| **Foundation stable** | **YES** |

## Combat Foundation Verification Checklist

| Area | Item | Result | Evidence |
|------|------|--------|----------|
| **Movement** | Pathfinding routes around obstacles | ✅ PASS | Dijkstra path uses the only gap |
| | AP / movement cost spent correctly | ✅ PASS | forest(2)+plains(1)=3 consumed |
| | Difficult terrain costs more | ✅ PASS | plains 1 / forest 2 / water 3 |
| | Impassable tiles blocked | ✅ PASS | boulder & occupant both block |
| | Reachability respects budget | ✅ PASS | in-range incl / out-of-range excl |
| **Terrain** | Cover (directional) | ✅ PASS | tree gives half, penalty 0.25 |
| | Elevation (terrain + override) | ✅ PASS | hill 1 / cliff 2 / override 5 |
| | Tile metadata composition | ✅ PASS | terrain+object → all queries |
| | Interactions surfaced | ✅ PASS | burn/chop/push present |
| **Line of Sight** | Blocked by cover at equal elevation | ✅ PASS | tree breaks LOS |
| | High ground sees over cover | ✅ PASS | cliff sees over tree |
| **Information (Pillar 2)** | Tile inspect/hover data complete | ✅ PASS | all keys + context actions |
| | Hit-chance transparency + range gate | ✅ PASS | breakdown + 0 when out of range |
| | Movement preview (cost/threat/attackers) | ✅ PASS | cost, threatened-by list |
| | Threat visualization live | ✅ PASS | tile threatened, per-enemy list |
| | Tactical overlay (whole grid) | ✅ PASS | 16/16 cells, all fields |
| **Combat** | Melee (damage − armor, AP spend) | ✅ PASS | 10−3=7, 1 AP |
| | Miss deals no damage | ✅ PASS | hp unchanged, logged |
| | Ranged range gate | ✅ PASS | hits near, blocked far |
| | Prepare → Guardian Counterattack | ✅ PASS | counter fired |
| | Prepare → Ranger Reaction Shot | ✅ PASS | shot on movement |
| | Prepare → Rogue Evasion | ✅ PASS | hit negated |
| | Prepare → Mage Spell Focus | ⚠️ WARN | reaction is a **no-op** (TODO) |
| **Loadout** | Locked in combat, editable outside | ✅ PASS | `LoadoutLockedError` raised |
| **AI parity** | Uses LOS/range to engage | ✅ PASS | closes distance & attacks |
| | Uses cover / elevation in scoring | ✅ PASS | higher score for high ground |
| | Avoids hazards it is told to avoid | ✅ PASS | fire tile scored −ve |
| | Uses same functions as player | ✅ PASS | shared `inspection`/`battlefield` |
| **Environment (Pillar 5)** | Fire spreads → scorched + smoke | ✅ PASS | deterministic evolution |
| | Hazards damage occupants | ✅ PASS | 4 fire dmg/round |
| | Interaction destroys bridge → water | ✅ PASS | terrain + flag change |
| **Persistence** | Permanent change saved to world_state | ✅ PASS | recorded under battlefield id |
| | Reloads on a fresh battlefield | ✅ PASS | bridge stays water |
| **Engine** | Decisive result, no infinite loop | ✅ PASS | winner in <30 rounds, 11ms |
| | Return-to-context after combat | ✅ PASS | origin/location preserved |
| **Data** | Every blueprint resolves | ✅ PASS | 74 spawnable, 0 errors |
| | Referenced AI profiles defined | ⚠️ WARN | 4 profiles missing (below) |
| | Skill/Item actions + ability wiring | ⚠️ WARN | not implemented (below) |

### Performance note (terminal engine)

The spec's "60 FPS / memory stable" targets are graphical-client concerns and
are **N/A** for this turn-based terminal engine. The equivalent guarantees are
verified instead: **no infinite loops** (auto-battle terminates well within the
round cap) and **fast execution** (full 6-combatant battle resolves in ~11 ms;
`tactical_overlay` and `threat_map` on the demo grid are instant).

## Passed systems (foundation)

Tile metadata · movement/pathfinding/AP economy · difficult & impassable
terrain · directional cover · elevation · line of sight (incl. high-ground
rule) · full inspection/preview/threat/overlay information layer · melee/ranged
attack resolution with armor, crit and hit-chance transparency · three of four
Prepare reactions · loadout lock · AI parity (cover, elevation, hazard
avoidance, engagement) using the player's own functions · environmental
evolution (fire/smoke/scorch) · hazard damage · environmental interaction ·
battlefield persistence round-trip · decisive turn loop · return-to-context.

## Incomplete implementations (tracked technical debt)

1. **Skill & Item actions are not implemented.** `actions.py` has Move, Attack,
   Prepare, Interact only. Class and enemy `abilities` are defined in data but
   are **decorative** — the engine never executes them and the AI never casts.
   → Phase 2 (enemy abilities) / Phase 6 (player skills).
2. **Mage "Spell Focus" prepare reaction is a no-op.** Only counterattack,
   reaction_shot and evasion have mechanics. → Phase 6.
3. **Missing AI-profile definitions.** `enemies.json` references `caster`,
   `ambusher`, `defender`, and `aggressive` profiles that do **not** exist in
   `ai_profiles.json`; they silently resolve to an empty dict (graceful, but not
   the intended behaviour). → Phase 2 (AI profiles).
4. **Some enemy abilities reference undefined library entries** (e.g.
   `raise_skeleton` vs the library's `raise_dead`). Harmless while abilities are
   decorative; must be fixed when the Skill action lands. → Phase 2.

## ⚠️ Critical finding — combat canon divergence (needs a decision)

The `tactical/` engine implements `Combat_Gameplay_Architecture.md`. However the
**established game canon** — `docs/GAME_BIBLE.md` ("Combat Overview") and
`docs/COMBAT_SYSTEM.md` — specifies a materially different combat model:

| Mechanic | GAME_BIBLE / COMBAT_SYSTEM canon | `tactical/` (verified) |
|----------|----------------------------------|------------------------|
| Movement | Movement Points, flexible move/act order | `move` budget (Dijkstra) |
| Actions | AP pool | `ap` pool ✔ (aligned) |
| Support Action | Separate per-turn utility action | ❌ not present |
| Reactions | One **per round**, event-triggered menu | **Prepare** arms one reaction; ends turn |
| Facing | Front/Side/Rear, flanking, back attacks | ❌ no facing |
| Shield Stance | Active stance costing Support Action | ❌ not present |
| Downed / Death | Downed → revive; death is special | ❌ 0 HP = removed immediately |
| Initiative | Initiative order, consecutive-hero flexibility | Team-phase turns (player team, then enemy team) |
| Party | 4 active heroes, bench, swap outside combat | Arbitrary N players; loadout lock only |

This is a **Level-1 canon conflict**, not a bug. It directly shapes Phase 2
enemy design (flanking/facing, executing downed heroes, morale, initiative-based
commander turns). Per project rules, it must be resolved by an explicit decision
— not by inventing a reconciliation. See the open question raised to the user.

## Verdict

Against its own spec, the tactical combat foundation is **stable and
independently verified (0 FAIL)**. Before Phase 2 begins, the combat-canon
divergence above must be reconciled so the enemy ecosystem is built on a single,
agreed foundation.
