# First Region Vertical Slice — Independent QA Report

> **Type:** Adversarial QA pass (2026-06). Agent-tested; **not user-confirmed.**
> Scope: the Frontier flow ([`tactical/frontier.py`](../../tactical/frontier.py)),
> the Corruption Avatar finale ([`tactical/showcase_corruption_avatar.py`](../../tactical/showcase_corruption_avatar.py)),
> the interactive choice/preparedness system, and the additive boss data. This
> was an attempt to **break** every branch, not to confirm the happy path.
> New adversarial suite: [`backend/tests/test_frontier_qa.py`](../../backend/tests/test_frontier_qa.py).

## Method
- **Exhaustive branch sweep:** all **128** choice combinations (2⁷) run end-to-end.
- **Cross-seed robustness:** golden vs worst deciders across 20 seeds each.
- **Boss invariants:** ward-restore, expose, single-shot enrage under crafted states.
- **Balance sweep:** correct vs naive read across the full reachable preparedness
  range (−3 … +6), 30–40 seeds per point.
- **Layer discipline:** static assertions that the core carries no UI/IO.
- **Data integrity:** every blueprint resolves; id/key parity; spawn/abstract guards.
- **Save compatibility:** verified the Frontier/boss code path never mutates saves.

## Issues discovered & fixed
1. **Unfair finale at worst preparedness (balance / fairness).**
   At the worst reachable preparedness (−3) the *correct* strategy cleansed only
   ~30% and **failed at the default seed** — violating the design rule that the
   golden resolution stays attainable through good judgement. The anchor HP
   penalty (+8 HP each per negative point → +24 at −3) was too steep.
   **Fix:** reduced the penalty to +3 HP each per negative point. Correct read is
   now winnable across the whole range (−3 → ~80–90%) while the difficulty
   gradient is preserved. *(showcase_corruption_avatar.py)*
2. **Dead "abstract base not spawnable" guard (latent bug in existing code).**
   `spawn_enemy` checked `resolve(id).get("abstract")`, but `resolve()` strips the
   `abstract` flag first, so the guard never fired — an abstract base could be
   spawned into a malformed combatant. Surfaced adversarially.
   **Fix:** check the *raw* blueprint's `abstract` flag before resolving.
   *(tactical/enemies.py — minimal, no behaviour change for real units.)*

Both fixes were made immediately and re-validated before continuing.

## What passed (no issues)
- **No soft locks / no permanent loss:** all 128 combinations assemble the full
  7-companion party, always save Bram (Ronan's climax), and always resolve the
  region to a valid state — a lost travel skirmish never blocks the recruitment it
  carries.
- **Naive finale never wins:** tunnelling the Avatar cleanses **0%** even at max
  preparedness — the wardstone lesson cannot be brute-forced.
- **Determinism:** identical seed + decider ⇒ identical beats, party, flags, clues,
  decisions, and outcome.
- **Preparedness math exact:** golden = **+6**, worst = **−3**; always within range.
- **Boss invariants:** ward restores the Avatar repeatedly while any anchor stands;
  it becomes vulnerable only when all anchors fall; enrage fires exactly once.
- **Engine-interface / Godot-readiness:** the core modules contain **no** `input()`
  or `print()`; all terminal I/O lives in `scripts/play_frontier.py`. No layer-rule
  regressions.
- **Data roster:** 76 spawnable units; every blueprint resolves; id/key parity;
  boss/anchor well-formed and tag-inheriting; abstract base now correctly rejected.
- **Save compatibility:** the Frontier + boss test path leaves `save_data.json`
  byte-identical. *(The full legacy suite still rewrites the save — pre-existing,
  unrelated to this slice.)*

## Balance observations
- Right vs naive strategic gap: **~93 percentage points** (30 seeds).
- Correct read by preparedness: prepared ~97% · neutral ~95% · rushed(−1) ~90% ·
  worst(−3) ~80%. Fair gradient — choices matter without being punishing.
- Travel skirmishes retain intentional variance (can be lost) while the three
  showcase anchors and the finale (with the correct read) are reliable.

## Remaining risks
- **Not user-playtest-confirmed** (pacing, prompt clarity, felt difficulty).
- **No persistence of Frontier results** — flags/preparedness don't carry to a
  later region yet (planned: "Persistent Regional Choices").
- **Phase 2 is numeric, not spectacular** — enrage is +AP/+damage; no telegraphed
  signature attack yet (planned: "Telegraphed Phase Two").
- **No Champion tier** between elite and the boss — the elite→boss jump is bridged
  by the wardstone mechanic and preparedness, not by a mid-tier unit yet.
- Boss balance is validated against the **reference tactician party**, not a
  hand-tuned full-companion loadout.

## Playtest recommendations
1. Play `python scripts/play_frontier.py` interactively; sanity-check prompt
   wording and that consequences *feel* meaningful.
2. Deliberately make poor early choices, then play the finale correctly — confirm
   it feels "hard but fair," not unwinnable.
3. Try the "strike the heart" finale read once to feel the lesson land.
4. Compare `... golden` vs `... worst` end screens for the choice-weight recap.

## Readiness assessment
**READY for external human playtest** of the First Region vertical slice.
Full pytest **269 passed**; `python -m tactical.verify` **FOUNDATION STABLE 62/62**;
task-owned markdown links **0 broken**; save-compat verified for this slice; two
issues found and fixed. Recommend a human pacing/clarity pass before building the
Champion tier.

## Document History
| Date | Change |
|---|---|
| 2026-06 | Adversarial QA pass on the First Region slice: 128-combo sweep, cross-seed robustness, boss invariants, layer/IO discipline, data integrity, save-compat. Found & fixed 2 issues (worst-prep finale fairness; dead abstract-spawn guard). Added 17-test adversarial suite. Assessed ready for human playtest. |
