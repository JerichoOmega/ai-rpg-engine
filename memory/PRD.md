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
- P1: Persist `LivingWorld` under `world_state["living_world"]` + add to
  `ensure_world_state_defaults()` when wiring into the main runtime save.
- P1: Region Two content pass on top of these systems (content, not systems).
- P2: Promote overlay beat→context map into per-region content (fully
  region-agnostic overlay).
- P2: Add `region_review` to CI alongside `tactical.verify`.
