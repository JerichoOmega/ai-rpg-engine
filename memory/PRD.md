# PRD — Elyndor RPG Engine

## Project
A terminal-based, engine-agnostic Python RPG (migrating toward Godot). Core:
`world_state.py` (state), `event_bus.py` (comms), `tactical/` (combat + region
slices). Documentation-first project; strict layer rules (gameplay ⟂ presentation).

## Latest milestone — Living Frontier Pass (2026-06)
Additive, non-breaking, engine-agnostic "living world" foundation for the First
Region, built as `tactical/living_world/`.

### Delivered (10 reusable systems + binding)
- Living Region System, Regional Epilogue ("The Frontier Endures"), Dynamic
  World Events, Companion Presence, Companion Banter, Reputation (remembered
  deeds, no meter), Environmental Storytelling, Landmark Moments, Regional
  Memory, Region Completion Review (runnable).
- `world.py` (`LivingWorld` aggregate, JSON round-trips), `frontier_overlay.py`
  (binds frameworks to the Frontier slice — slice unmodified), `content.py`
  (data loader). First-Region content in `tactical/living_world/data/*.json`.
- Interactive runner `scripts/play_frontier.py` renders the overlay
  (presentation only).
- Docs: `docs/systems/living_world.md`, handoff, `LIVING_FRONTIER_PASS_REPORT.md`.
- Tests: `backend/tests/test_living_world.py` (24).

### Validation (all green)
- pytest: **293 passed** (was 269; +24; 0 regressions).
- `python -m tactical.verify`: **62/62 PASS, FOUNDATION STABLE**.
- `python -m tactical.living_world.region_review`: **13/13 OK, REGION READY**.
- No combat/save/canon/engine-interface changes; core has zero print/input.

## Architecture rules honored
- Pure rules + data only in core (State/Event/Intent), content-as-JSON,
  composition over expanding legacy managers, everything JSON-serializable.

## Backlog / Next
- P1: Region Two content pass on top of these systems (content, not systems):
  add `<region>_region.json` manifest + content JSON, supply a run record, pass
  the CI gate.
- P2: In live play, call `runtime.apply_overlay(world)` / `install_event_hooks()`
  so a region's runtime auto-persists at checkpoints (save boundaries done).

## Runtime save + CI integration (2026-06, done)
- Live save hookup: `tactical/living_world/runtime.py` holds the session's
  authoritative `LivingWorld`, hydrated on `load_game` and flushed on
  `save_game`/`autosave` + gameplay checkpoints — through the existing save
  systems (`save_manager`, `state_manager`); no second save path.
- CI: `.github/workflows/ci.yml` (headless, no Godot) runs pytest + verify +
  region_review + quality gate; `Makefile` (`make ci`) mirrors it locally.
- Save-contract + Godot audit clean (single source of truth, deterministic
  load/defaults, no presentation state persisted).
- Validation: **315 pytest passed**, verify 62/62, review 15/15, gate PASS,
  8/8 new runtime tests. Report: `RUNTIME_SAVE_CI_INTEGRATION_REPORT.md`.

## Foundation hardening (2026-06, done)
- Persistence into `world_state["living_world"]` (additive; no save-module
  changes; legacy-safe; forward-compatible). `persistence.py` + `world.py`
  extended + `world_state.py` defaults.
- Region-agnostic overlay engine (`overlay.py`) + `RegionContent` manifest
  contract (`region.py`); Frontier reduced to a data-driven adapter; behaviour
  unchanged. `data/testregion_*` fixture proves arbitrary regions.
- CI quality gate `scripts/ci_quality_gate.py` (headless).
- ENGINE_INTERFACES `LivingWorldState` contract + Godot-migration note.
- Validation: **307 pytest passed**, verify 62/62, review 15/15, gate PASS.
- Reports: `LIVING_FRONTIER_PASS_REPORT.md`, `FOUNDATION_HARDENING_REPORT.md`.
