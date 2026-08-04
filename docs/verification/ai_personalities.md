# Enemy AI Personalities + Behavior Memory — Verification Report

> Status: **COMPLETE** · Result: **PASS (independently verified)** · Date: 2026-06
> Priority 1/5 (Engine→Game directive). Technical Canon: `tactical/`.
> Independent suite: `backend/tests/test_ai_personalities.py` (25/25)
> Full backend suite: **116/116** · Harness: 47 checks, 46 PASS / 0 FAIL / 1 WARN
> Machine report: `test_reports/iteration_7.json`

## What shipped

A **reusable, data-driven enemy AI library** wired into one code path — enemies
now behave distinctly, and a short **behavior memory** makes them feel
intentional. No enemy-specific AI; adding an archetype is a JSON entry.

* **`tactical/data/ai_profiles.json`** — 20 archetypes (aggressive, brute,
  berserker, beast, aggressive_melee, defender/defensive, commander, skirmisher,
  hunter, ambusher/assassin, caster, necromancer, summoner, support, pack_hunter,
  cowardly, elite, boss). The four previously-missing referenced profiles
  (caster/ambusher/defender/aggressive) are now defined → **the "missing AI
  profiles" WARN is cleared.**
* **`tactical/ai.py`** — honours profile flags (`charges`, `kites`,
  `hold_position`, `prefers_flank`, `fearless`, `avoids`, `will_retreat`/
  `flees_when_low`+`flee_threshold`) through `_score_tile`/`take_turn`; added
  `_resolve_target` (sticky), `_update_memory`, `_retreat`.
* **Fail-loud**: `enemies.resolve()` warns to stderr and falls back to
  `aggressive_melee` on an undefined profile.
* **`Combatant.ai_memory`** — `target_id`, `turns_chasing`, `morale`,
  `commander_nearby`, `currently_flanking`, each influencing decisions.

## Result

| Gate | Status |
|------|--------|
| Implementation (data-driven, no enemy-specific AI) | ✅ PASS |
| Independent testing | ✅ PASS (25/25 new; 116/116 full) |
| Regression (harness stable, auto_battle terminates, bridge, 74 blueprints) | ✅ PASS |
| AI parity (shared functions, no hidden state) | ✅ PASS |
| Documentation | ✅ UPDATED (`docs/systems/tactical_ai.md`) |

## Verified behaviours

Distinct: defender holds, kiter avoids adjacency, ambusher prefers flank, charger
closes harder, fearless ignores threat. Flee/morale: coward retreats when
wounded, fearless never flees, commander presence steadies (halves threshold),
low morale breaks more easily. Memory: sticky targeting, lowest-health <50%
switch, turns_chasing increment/reset. Grep-confirmed: zero enemy-identity
branching in `ai.py`.

## Known follow-up (next phase)

Archetype aliases (defender≈defensive, ambusher≈assassin) and the descriptive
flags (`coordinates`/`buffs_allies`/`summons`) become fully distinct once the
**Skill/ability system** lands — the last remaining harness WARN. That is the
recommended next task: it closes the WARN and unlocks "uses defensive abilities
first / crowd control / buffs allies / waits for favorable attacks."

## Next (Engine→Game sequence)

1. **Ability/Item usage** (Skill action + AI casting) — closes the final WARN,
   differentiates the archetype aliases.
2. **Phase B** — Downed / Revive / Death.
3. Combat feedback/readability polish.
4. One exceptional **vertical-slice region**.
