# Runtime Save Hookup + CI Enforcement — Final Report

> **Final infrastructure pass before Region Two content.** Makes the living
> world **survive real gameplay sessions** and puts the quality bar into an
> **actual CI pipeline**. Additive · non-breaking · engine-agnostic ·
> Godot-compatible. **Date:** 2026-06.

---

## 1. Outcome

The living world is no longer merely serializable — it is persisted at the
**real save boundaries** and gameplay checkpoints, and the project's quality bar
is enforced by a headless CI workflow. Region One behaves exactly as before.

## 2. Live save hookup — where it was integrated

New session service `tactical/living_world/runtime.py` holds the session's
single authoritative `LivingWorld` and keeps it mirrored into
`world_state["living_world"]`. It is wired into the **existing** save systems
(no second save path):

| Boundary | File · function | Call added |
|---|---|---|
| Save | `save_manager.py::save_game` | `runtime.sync_into_world_state(world_state)` (after player/roster sync, before serialize) |
| Load | `save_manager.py::load_game` | `runtime.hydrate_from_world_state(world_state)` (after `ensure_world_state_defaults`) |
| Save | `state_manager.py::save_game` | `runtime.sync_into_world_state(world_state)` |
| Load | `state_manager.py::load_game` | `runtime.hydrate_from_world_state(world_state)` |
| Autosave | both `autosave()` | inherits the `save_game` flush |

### Gameplay checkpoints that persist LivingWorldState
Via the runtime checkpoint API (mutate → flush), and via opt-in event-bus hooks
(`runtime.install_event_hooks()` subscribing `quest_completed`,
`world_event_resolved`, `region_state_changed`, `landmark_completed`,
`presence_changed`, `regional_milestone`, `game_saved`):

- remembered deed earned (`record_deed`)
- regional state change (`set_region_status`)
- dynamic world event resolved (`resolve_event`)
- landmark moment completed (`complete_landmark`)
- companion/world presence changed (`mark_presence`)
- major regional milestone (`complete_region`)
- normal save/checkpoint (`checkpoint` / save-boundary flush)

It does **not** save on every trivial mutation — only at these boundaries.

## 3. Save/load behavior & legacy compatibility

- **Real sequence proven:** PLAY → checkpoint changes → `save_game` → new
  session (memory + world reset) → `load_game` → LivingWorldState restored →
  gameplay continues. Verified through the actual `save_manager` **and**
  `state_manager` pathways.
- **Legacy saves** (no `living_world` key) load without crashing:
  `ensure_world_state_defaults()` backfills, then hydrate yields safe defaults.
- **Forward-compatible:** unknown/future keys ignored on load.
- **Inactive session:** when gameplay never touches the living world,
  `sync_into_world_state` is a no-op — save behaviour is byte-for-byte unchanged.

## 4. Tests added (10 required behaviors + more)

`backend/tests/test_living_world_runtime.py` — **8 tests** exercising the real
runtime pathway, each isolated from `/app/save_data.json` via a temp `SAVE_FILE`
and world_state snapshot/restore:

1. Fresh game → hydrate to defaults.
2. Legacy save (no `living_world`) → loads + backfills, no crash.
3–9. Full cycle via `save_manager`: quest/world-state change, save checkpoint,
   reload, and verify **deed / regional state / resolved event / landmark /
   presence / progression / transition-history (regional memory)** all survived;
   world_state mirror stays consistent with the runtime.
10. Multiple save/load cycles stable (×3).
- Full cycle also proven via `state_manager` (second save system).
- Inactive-session save unchanged.
- Real `save_data.json` untouched (mtime + content asserted).

**Total suite: 315 passed** (was 307; +8; 0 regressions).

## 5. CI workflow changes

No CI existed. Created the canonical pipeline (headless, **no Godot**):

- `.github/workflows/ci.yml` — on push/PR/dispatch, Ubuntu + Python 3.11:
  full `pytest` → `python -m tactical.verify` →
  `python -m tactical.living_world.region_review` →
  `python scripts/ci_quality_gate.py` (content contracts + save round-trip +
  docs). Build **fails** if any step fails.
- `Makefile` — `make ci` / `check` / `test` / `verify` / `review` / `gate`.

### Run the exact same checks locally
```
python scripts/ci_quality_gate.py --pytest   # everything (what CI runs)
make ci                                        # identical, via Makefile
python -m tactical.verify                      # combat foundation only
python -m tactical.living_world.region_review  # living-world review only
```

## 6. Save-contract audit (findings → clean)

- **One authoritative representation:** the runtime's active `LivingWorld`,
  mirrored into `world_state["living_world"]`. No manager keeps a parallel copy
  (`living_world` appears only in the two save systems as the hook call).
- **Deterministic load order:** restore `world_state` →
  `ensure_world_state_defaults()` → `runtime.hydrate_from_world_state()`.
- **Deterministic defaults:** `persistence.default_state()` /
  `ensure_world_state_defaults()` produce the same block every time.
- **Legacy compatible / forward-compatible:** confirmed by tests.
- **Serialization is presentation-independent:** `to_state`/`from_state` are pure
  data; no terminal/UI state is persisted (audited — no `print`/`input`/`open`
  in any core module including `runtime.py`).
- `ENGINE_INTERFACES.md` updated with the runtime persistence note.

## 7. Godot compatibility

Core stays engine-neutral: no Godot nodes/signals/resources, no UI/terminal/
filesystem coupling inside core rules (`runtime.py` only reads/writes the
in-memory `world_state` dict). The eventual Godot layer calls the **same**
`runtime` / `persistence` interfaces with the same JSON-shaped state. The
region-review Godot-compat check and a unit test both guard this.

## 8. Regression audit (all green)

| Check | Result |
|---|---|
| `python -m pytest` | **315 passed** (0 failed) |
| `python -m tactical.verify` | **62/62 — FOUNDATION STABLE** |
| `python -m tactical.living_world.region_review` | **15/15 — REGION READY** |
| `python scripts/ci_quality_gate.py` | **QUALITY GATE: PASS** |
| new runtime save-integration tests | **8/8 passed** |
| markdown/doc contract | required docs present (gate) |
| git scope | only intended files touched; `save_data.json` restored (pre-existing test artifact) |

## 9. Remaining risks

- **Low:** the interactive/main loop still drives the living world only in the
  Frontier demo runner; when a region's runtime consumes the overlay in live
  play it should call `runtime.apply_overlay(world)` (or `install_event_hooks()`)
  so checkpoints persist automatically. The plumbing + save boundaries are done
  and tested.
- **Low:** `LivingWorld.from_content()` still defaults to Frontier locations as a
  convenience; the generic engine never relies on it.

## 10. Readiness for Region Two

**READY.** The living world survives real sessions, CI enforces the quality bar
headlessly, and future regions build entirely on the engine-agnostic
foundation — content, not systems.
