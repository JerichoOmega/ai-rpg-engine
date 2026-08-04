# Tactical Abilities — Canonical Ability Pipeline (Combat Phase C)

**Status:** COMPLETE & independently verified (2026-06).
**Module:** `tactical/abilities_engine.py`
**Canon:** Technical Canon (R-01). Abilities are first-class tactical actions
alongside Move / Attack / Prepare / Interact, running on the single canonical
`tactical/` engine — no parallel ability system, no duplicate combat path.

## Design pillar: Information Before Commitment

There is exactly **one** authoritative source of ability truth,
`ability_preview()`. The player UI (`session.py`), the AI (`ai.py`,
`choose_ability`), the verification harness, and any future graphical client all
read legality and expected effect from it. `use_skill()` is gated by the same
preview, so what the player is shown is exactly what the engine enforces.

### `ability_preview(engine, unit, ability_id, target=None, tile=None) -> dict`
Returns (never raises):

| Field | Meaning |
|---|---|
| `name`, `type`, `description` | Display metadata |
| `ap_cost` | Action points required |
| `cooldown`, `cooldown_remaining` | Total cooldown and turns left |
| `range`, `requires_los` | Reach and whether line of sight is needed |
| `in_range`, `line_of_sight`, `legal_target` | Live legality vs the given target/tile |
| `aoe`, `summons`, `terrain_effect` | Area / summon / terrain footprint |
| `expected_damage`, `expected_healing` | Numeric effect preview |
| `buffs`, `debuffs`, `status_effects` | Applied conditions |
| `friendly_fire_risk` | True for hazards that can also harm allies |
| `tactical_value` | The AI's "why now" score |
| `usable`, `failure_reason` | The single verdict + human-readable reason |

`failure_reason` values: `not enough AP`, `on cooldown (N turn(s) left)`,
`requires a valid target`, `target out of range`, `no line of sight to target`,
`tile out of range`, `no line of sight to tile`, `destination tile is blocked`,
`requires a target tile`, `unknown ability`.

## Data-driven cooldowns

Every ability blueprint declares its own fields — nothing is hardcoded per
ability:

```json
"war_cry": {"type": "buff", "ap": 1, "range": 6, "effect": "morale_boost", "cooldown": 3}
```

* Tracked per combatant in `unit.cooldowns` (`ability_id -> turns_remaining`).
* Set on a **successful** cast (`cooldowns[id] = cooldown` when `cooldown > 0`).
* Ticked **once** per activation in `start_of_turn()` (decrement, drop at 0).
* Blocks reuse while active; the preview reports the remaining turns.
* Save/load compatible via `export_state()` / `import_state()` (plain JSON:
  `{statuses, cooldowns}`).

## Ability types & handlers (`_HANDLERS`)

`attack`, `movement_attack`, `summon` (incl. `heal_zone` → heal), `heal`,
`buff`, `zone`, `control`, `debuff`, `terrain`, `movement`. Effects are resolved
purely from the ability's data fields (`damage`, `damage_bonus`, `status`,
`aoe`, `ignites`, `cover_grant`, `effect`, `creates`, `creates_status`,
`summons`, `heal`).

### Status lifecycle
* `rooted` — movement set to 0 at the start of the bearer's turn, then cleared.
* `poison` — 3 damage-over-time at each start of turn; persists until cleansed
  (e.g. the `antidote` item).
* `shielded` — halves the next incoming hit, then drops.
* `emboldened` / `marked` / `hexed` / `cursed` — transient (+/- hit chance),
  cleared at the start of the bearer's next turn (a one-round duration).

## AI ability usage (role reinforcement without hardcoding)

`choose_ability()` scans the unit's equipped abilities, reads each one's
`ability_preview`, and picks the highest **usable** `tactical_value`. Roles
emerge because blueprints grant role-appropriate abilities and each type has an
intrinsic value; profile flags apply gentle multipliers only:

| Profile flag | Effect |
|---|---|
| `coordinates` (Commander) | ×1.4 to buff/zone/heal value |
| `buffs_allies` (Support) | ×1.4 to buff/zone/heal value |
| `summons` (Necromancer/Summoner) | ×1.4 to summon value |
| `kites` (Caster) | ×1.2 to control/debuff value |

`take_turn()` evaluates a worthwhile ability **before** movement (so a healer
does not charge past the ally it means to heal), then moves, then re-evaluates
attack abilities and finally a basic attack — all with one shared code path.

## Verification

* Harness: `python -m tactical.verify` → **62 PASS / 0 FAIL / 0 WARN**
  (category `[Abilities]`, 14 checks). The former Skill/Item **WARN** is gone.
* Independent suite: `backend/tests/test_ability_pipeline.py` (31 behavioral
  tests) + testing-agent's own 27 tests → full backend **175 passed**.
* Report: `docs/verification/phaseC_ability_pipeline.md`,
  `/app/test_reports/iteration_8.json`.
