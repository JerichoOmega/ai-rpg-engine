# Combat Bridge — Verification Report

> Status: **COMPLETE** · Result: **PASS (independently verified)** · Date: 2026-06
> Audit item C1 · R-01 Technical Canon (`tactical/`)
> Independent suite: `backend/tests/test_combat_bridge.py` (18/18)
> Full backend suite: 91/91 · Harness: `python -m tactical.verify` STABLE (0 FAIL)
> Machine report: `test_reports/iteration_6.json`

## What shipped

Every **standard overworld encounter now runs on the canonical tactical
engine** — the legacy `combat.py` runtime is no longer the exploration-combat
entry point (it remains only as an unmodified Compatibility Layer per R-01).

* **`combat_bridge.py`** — the single overworld→tactical entry point:
  * builds the player party from `world_state["player"]` (class mapped via
    `CLASS_MAP`, level scales hero damage) plus `companion_manager.
    active_companions`;
  * builds **blueprint-based** enemies via `tactical.encounters.build_group`
    (does **not** touch `enemy_manager`);
  * builds a battlefield seeded by the region biome;
  * maps region biome → encounter group (`_pick_group`);
  * applies a fairness cap `max(2, party+1)` (full threat-budget scaling is a
    later phase);
  * runs the encounter and writes results back: hero + companion HP, XP
    (`progression_manager.award_xp_to_roster`), gold, and a `loot_manager`
    drop; player/world sync after combat.
* **`tactical/session.py`** — the interactive terminal combat UI driving the
  engine (Move / Attack with hit% + flank tags / Prepare / Inspect / End),
  with a headless mode (AI plays both sides) for tests. Blank/exhausted input
  safely ends a unit's turn, so combat always terminates.
* **Wiring** — `world_actions.explore_menu` "Hunt for trouble" now calls
  `combat_bridge.start_encounter`.

## Result

| Gate | Status |
|------|--------|
| Implementation | ✅ PASS |
| Independent testing | ✅ PASS (18/18 bridge; 91/91 full suite) |
| Regression (tactical harness, Phase A, Phase 1 wiring) | ✅ PASS |
| Documentation | ✅ UPDATED |
| Canonical single combat entry (standard encounters) | ✅ YES |

## Verified behaviours

Headless resolution + HP write-back (never <1) · party build from world +
companions · blueprint enemies via `build_group` (no `enemy_manager`) ·
biome→group mapping · fairness cap · victory rewards (XP/gold/loot) · defeat
grants no rewards but still writes HP · interactive controller full scripted
flow terminates · unreachable-move rejection · explore→Hunt wiring · legacy
`combat.py` still imports but is not reachable from the standard path ·
save/load round-trip after an encounter.

## Known follow-ups (not blockers)

* **Threat budget & party design** — the fairness cap is a stopgap; proper
  threat-budget encounter generation + a real 4-hero party belong to later
  phases (audit E-series / R-01 Phase D).
* **City encounters** — `urban` biome falls through to `roadside_ambush`
  (content gap, not a bug).
* Party placement assumes party ≤ battlefield height (safe today).

## Next (per approved sequence)

1. **Enemy personality profiles** (complete the missing AI profiles: caster,
   ambusher, defender, commander, etc. — closes one of the harness WARNs).
2. **Phase B** — Downed / Revive / Death.
3. **Combat feedback improvements.**
4. Then a single polished **vertical slice** before broad content expansion.
