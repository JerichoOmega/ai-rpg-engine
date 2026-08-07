# Living World System (`tactical/living_world/`)

> **Status:** CONFIRMED — implemented 2026-06 as the *Living Frontier Pass*.
> **Type:** Additive, non-breaking, engine-agnostic reusable framework.
> **Laws:** [`docs/architecture/LAYER_RULES.md`](../architecture/LAYER_RULES.md) ·
> Contracts: [`docs/architecture/ENGINE_INTERFACES.md`](../architecture/ENGINE_INTERFACES.md)

## Purpose

Make a region feel **alive**: it remembers what the player did, it changes state
over time, companions have a presence in it, and it closes with a reactive
epilogue. Everything here is a **reusable foundation** — a future region ships
new *content* (JSON) and inherits every *system* (code) unchanged.

This is the point where the world itself becomes one of the game's main
characters.

## Design laws (why it looks the way it does)

- **Pure rules + data only.** No `print`/`input`, no engine imports, no
  UI/animation/audio/timing anywhere in the framework code. Output is returned
  as plain, JSON-shaped data; presentation (terminal today, Godot later) decides
  how to show it. The one exception is `region_review.py`, a dev/QA tool whose
  `main()` prints — exactly like `tactical/verify.py`.
- **State / Event / Intent** are the channels (ENGINE_INTERFACES). Every
  stateful object exposes `to_state()`/`from_state()` and round-trips through
  JSON, so Godot and Python agree on the data and saves stay compatible.
- **Content is data, code is rules** (Layer Rule 4). Frameworks live in the
  package modules; the First Region's content lives in
  `tactical/living_world/data/*.json`.
- **Composition over expansion.** Existing managers are *not* given new
  responsibilities; they consume this package through clean interfaces.

## The ten systems

| # | System | Module | First-Region content |
|---|---|---|---|
| 1 | Living Region System | `region_state.py` | `data/frontier_locations.json` |
| 2 | Regional Epilogue ("The Frontier Endures") | `epilogue.py` | `data/epilogue_threads.json` |
| 3 | Dynamic World Events | `events.py` | `data/event_templates.json` |
| 4 | Companion Presence | `companions.py` | `data/companion_presence.json` |
| 5 | Companion Banter | `banter.py` | `data/banter.json` |
| 6 | Reputation (remembered deeds) | `reputation.py` | recorded at runtime |
| 7 | Environmental Storytelling | `environment.py` | `data/environment.json` |
| 8 | Companion Landmark Moments | `companions.py` | `data/companion_landmarks.json` |
| 9 | Regional Memory (revisit evidence) | `memory.py` | `data/regional_memory.json` |
| 10 | Region Completion Review | `region_review.py` | — (runnable) |
| — | Aggregate state | `world.py` (`LivingWorld`) | — |
| — | First-Region binding | `frontier_overlay.py` | — |
| — | Content loader | `content.py` | — |

### 1. Living Region System (`region_state.py`)

Every settlement/landmark/region is a `LocationState` with one of six statuses:
`safe`, `threatened`, `recovering`, `prosperous`, `corrupted`, `restored`.
`set_status()` logs each transition (with a `natural` flag validated against the
documented `TRANSITIONS` arcs) so the world *remembers how it changed*.

### 2. Regional Epilogue (`epilogue.py`)

`build_epilogue(threads, flags)` assembles a reactive "Region Complete" sequence
from remembered choices. For the Frontier the working title is **"The Frontier
Endures"** and the eight threads are **Bram, the Hidden Pack, Corwin's
investigation, Maeve's settlement, Torren's forge work, Eleanor's diplomacy,
Talos's leadership, Ronan's acceptance.** It shows the world changing (positive
vs. bittersweet variants + a reactive closing tone), never a stat dump.

### 3. Dynamic World Events (`events.py`)

Reusable templates surfaced during exploration (merchant under attack, lost
child, traveling healer, Hidden Pack scouts, wandering knight, corrupted
wildlife, refugee caravan, traveling storyteller, abandoned campsite, injured
animal). `draw_events()` does a deterministic, weighted, tag-filtered,
no-replacement draw with an `exclude` list so seen events don't repeat.

### 4 & 8. Companion Presence + Landmark Moments (`companions.py`)

`presence_here()` returns each companion's contextual world interactions
(Talos advises villagers, Eleanor blesses shrines, Maeve treats the wounded,
Corwin identifies corruption, Ragash's hounds draw the children, Ronan reads
tracks, Torren examines stonework). `landmark_moments_here()` returns the quiet,
optional character beats at important locations (Ronan at the wolf shrine, Maeve
lighting her Lantern of Ashes, etc.).

### 5. Companion Banter (`banter.py`)

Travel/camp conversations keyed by eleven triggers: `weather`, `enter_town`,
`river`, `forest`, `cave`, `ruins`, `victory`, `defeat`, `camping`,
`boss_arena`, `discovery`. An exchange only fires when *all* its participants
are in the party.

### 6. Reputation (`reputation.py`)

**No approval meter.** Settlements remember *specific deeds* (`Deed` objects with
an `npc_line`) — saving Bram, cleansing corruption, helping refugees, restoring
a village, protecting travellers. NPCs reference them naturally on return. This
is the *memory of deeds* layer; the numeric faction reputation in
`docs/systems/reputation.md` is unchanged and complementary.

### 7. Environmental Storytelling (`environment.py`)

Detail templates (tracks, abandoned camps, ruined wagons, broken weapons,
damaged buildings, memorials, journals, graves, shrines) so the player *reads*
that something happened before dialogue begins. Each detail can carry a
`corwin_insight` that surfaces only when Corwin is in the party.

### 9. Regional Memory (`memory.py`)

`revisit_report()` returns the "before dialogue" evidence a returning player
sees, keyed by the location's current status (villagers rebuilding, children
playing, fields restored, wildlife returning, new memorials, shops reopening),
plus the NPC references to deeds done there.

### 10. Region Completion Review (`region_review.py`)

Runnable QA gate — the template for every future region:

```
python -m tactical.living_world.region_review          # human checklist
python -m tactical.living_world.region_review --json    # machine report
```

Evaluates region completion, companion/banter/quest/encounter/event coverage,
reputation & regional-memory triggers, world-state transitions (all-natural),
documentation completeness, Godot-migration compatibility (no screen I/O in
core), serialization round-trip, playtest readiness, and outstanding TODOs.
Writes `region_review_report.json`. Exit code `0` iff **REGION READY**.

## Integration with the First Region

`frontier_overlay.build_overlay(state, seed)` consumes a completed
`tactical.frontier.FrontierState` (the slice is **not** modified) and returns an
engine-neutral overlay: per-beat presence/banter/environment/dynamic-event, the
remembered deeds, the region-status transitions the player's choices caused, and
the reactive epilogue. `revisit_reports(world)` returns the regional-memory
evidence for every location.

The terminal runner `scripts/play_frontier.py` renders this overlay as a
temporary presentation layer — it consumes the data only; no rules live there.

## Persistence

`LivingWorld` is designed to live under `world_state["living_world"]` when wired
into the main save (additive key; backfilled by
`ensure_world_state_defaults()`). It is fully JSON-serializable and
round-trippable, preserving save compatibility (ENGINE_INTERFACES §Round-trip).

## Reuse for future regions

1. Add a `data/<region>_locations.json` and region-specific content files.
2. Point a new overlay (or a generalized loader) at that content.
3. Run `region_review` to confirm the region is feature-complete before ship.

No framework code changes — subsequent regions are **content, not systems**.

## Related

- `tactical/frontier.py` — the First-Region vertical slice (unmodified).
- `docs/systems/reputation.md` — numeric faction reputation (complementary).
- `docs/systems/world_regions.md` — legacy region manager.
- `docs/architecture/LAYER_RULES.md`, `ENGINE_INTERFACES.md` — the laws.

## Revision History

| Date | Change |
|---|---|
| 2026-06 | Created — Living Frontier Pass: ten reusable engine-agnostic systems, First-Region content, frontier overlay, and the Region Completion Review tool. Additive/non-breaking. |
