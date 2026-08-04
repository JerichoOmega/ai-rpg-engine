# Phase A — Facing / Flanking / Opportunity: Verification Report

> Status: **COMPLETE** · Result: **PASS (independently verified)** · Date: 2026-06
> R-01 migration, Phase A. Technical Canon: `tactical/`.
> Independent suite: `backend/tests/test_phase_a_facing_flanking.py` (29/29)
> Harness: `python -m tactical.verify` (40 checks, 38 PASS / 0 FAIL / 2 WARN)
> Machine report: `test_reports/iteration_5.json`

## Scope

Additively migrated the first slice of Gameplay Canon (`GAME_BIBLE.md` /
`COMBAT_SYSTEM.md`) onto the tactical engine, **without rewriting or removing
verified functionality**:

* **Facing** — every combatant has a `facing` (`tactical/facing.py`), set when it
  moves (direction of last step) or attacks (toward the target). A unit that has
  not acted (`facing is None`) is treated as facing every attacker (**front**),
  preserving all pre-Phase-A behaviour.
* **Flanking** — attacks resolve against the defender's arc via the *shared*
  `compute_hit_chance` (players and AI read identical data): front = no modifier,
  **side** = +0.10 hit, **rear** = +0.20 hit and **×1.25 damage**.
* **Opportunity attacks** — a melee foe the mover starts adjacent to gets one
  free swing if the mover leaves its reach (bounded: one per foe per move).
* **Readability** — `compute_hit_chance` exposes `facing` / `facing_bonus` /
  `flanking`; `movement_preview` exposes `provokes_opportunity_from`; hit log
  lines carry a `FLANK` tag.

## Result

| Gate | Status |
|------|--------|
| Implementation (additive, no rewrites, no removed features) | ✅ PASS |
| Independent testing | ✅ PASS (29/29 pytest + 38/38 non-WARN harness) |
| Regression (foundation, 74 blueprints, auto_battle termination) | ✅ PASS |
| Documentation | ✅ UPDATED |
| Independently testable | ✅ YES |

## Design acknowledgement (intentional, not a bug)

`compute_hit_chance` clamps to a 0.95 maximum. When a unit's base accuracy is
already high (~0.85), the nominal +0.20 rear-flank hit bonus is partially
absorbed by the clamp (0.85 → 0.95, a realized +0.10). This is **intended**: the
clamp preserves the "no guaranteed hits" tactical feel, and the **rear-flank
×1.25 damage bonus always applies regardless of the clamp**, so flanking remains
a meaningful positional reward. The full +0.20 hit delta is observable whenever
base accuracy ≤ ~0.75.

## Phase A tag

```
PHASE A — FACING / FLANKING / OPPORTUNITY
STATUS               COMPLETE
Implementation       PASS (additive)
Independent Testing  PASS (29/29 + 38/38)
Regression           PASS
Documentation        UPDATED
Independently testable  YES
```

## Next (R-01 order)

* **Phase B:** Downed state · Death mechanics · Recovery mechanics.
* **Phase C:** Shield Stance · Support Actions · advanced defensive mechanics.
* **Phase D:** Initiative refinements · party management · combat polish.

Still tracked (Phase 2/6, unchanged by Phase A): the 2 harness WARNs — missing
AI-profile subtypes and unwired Skill/Item/ability actions.
