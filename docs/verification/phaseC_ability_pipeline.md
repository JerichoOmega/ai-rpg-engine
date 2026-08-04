# Verification — Combat Phase C: Canonical Ability Pipeline

**Date:** 2026-06 · **Result:** COMPLETE, independently verified, no regressions.

## Scope
Complete the ability/skill/item action as a first-class tactical action on the
canonical `tactical/` engine: a single authoritative preview API, data-driven
cooldowns, profile-driven AI ability usage, full transparency, and elimination
of the last combat WARN. No combat rewrite, no duplicate combat path.

## Implementation (files)
| File | Change |
|---|---|
| `tactical/abilities_engine.py` | Rewritten: `ability_preview()` single source of truth; `use_skill()` gated by preview; data-driven cooldowns; `start_of_turn()` ticks cooldowns + processes statuses; `_h_heal` + `heal_zone`; `choose_ability()` reads previews; `export_state`/`import_state`. |
| `tactical/ai.py` | `take_turn()` evaluates a worthwhile ability before movement, then move, then attack ability / basic attack. |
| `tactical/session.py` | `_do_skill()` player menu renders cost / cooldown / expected effect / per-target legality / failure reasons from the preview. |
| `tactical/entities.py` | `Combatant.cooldowns` store. |
| `tactical/actions.py` | `use_skill` = `abilities_engine.use_skill` (single entry); `use_item` (heal/cleanse). |
| `tactical/data/ability_library.json`, `abilities.json` | Added `cooldown` / `requires_los` / `status` / `effect`; added `raise_skeleton`; capped class abilities to AP≤2 to fit the 2-AP economy. |
| `tactical/verify.py` | New `[Abilities]` category (14 checks); removed the old Skill/Item WARN. |
| `backend/tests/test_ability_pipeline.py` | New independent behavioral suite (31 tests). |
| `backend/tests/test_tactical_independent.py` | Flipped the old "gap-asserting" tests into positive regression guards. |

## Results
* `python -m tactical.verify` → **TOTAL 62 · PASS 62 · FAIL 0 · WARN 0** · FOUNDATION STABLE: YES.
* `python -m pytest backend/tests/ -q` → **175 passed** (148 existing + 27 testing-agent).
* Independent testing agent (`/app/test_reports/iteration_8.json`): 100% backend,
  **0 critical / 0 minor**, authored its own 27-test suite from a fresh angle and
  confirmed `actions.use_skill is abilities_engine.use_skill` (no duplicate path).

## Behaviors verified
Preview contract completeness & accuracy; preview↔use_skill parity; AP consumed
on success / nothing on illegal cast; cooldown set → block → tick → recover;
range & LOS gates; attack damage + status (poison); poison DoT + antidote
cleanse; morale buff embolden→expire; shielded halves-then-drops; heal restores
wounded ally (and zero value with none wounded); summon adds ally + cap of 3;
terrain transforms tile; control roots / taunt forces target; AI: Support heals,
Commander rallies, cooldown skip, in-range attacker picks a damage ability;
JSON save/load round-trip; every blueprint ability id resolves; ability-rich
battle resolves within the round cap.

## Notes / accepted design
* `emboldened/marked/hexed/cursed` are one-round (cleared at bearer's next turn);
  `poison` persists until cleansed; `shielded` until it absorbs a hit — a
  deterministic, testable duration model (no separate counter system needed).
* `expected_damage` is now reported for any ability with an explicit `damage`
  field (including splash-damage control/terrain like `pinning_shot`).
