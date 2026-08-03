# System: Legacy Questline Architecture

> Status: **[CONFIRMED]** — implemented in `legacy/` and verified by the
> automated harness (`legacy/harness.py`, 6/6 scenarios passing).
> Last updated: 2026-06.

The Legacy Questline architecture is the reusable, production-quality quest
system that every future main quest, side quest, companion quest, and
Legacy Questline is meant to build on. It was delivered as the vertical
slice implementing the three approved quests:

* **The Debt Comes Due** (Humans ⇄ Stonefang)
* **What the Forest Carries** (Mossroot)
* **Eternal Forge** (Dwarven Kingdom)

**Design authority:** the quests are implemented from the approved design
packages verbatim. No lore was invented; gaps are marked `CANON_PENDING`.
Intentionally-unrevealed future content (the sealed lower Foundry chamber,
the ancient guardian of the deep, the Council of Embers foundations) is
registered only as inert hooks and never surfaced to the player.

---

## Where it lives

```
legacy/
├── framework/                 reusable engine systems (no quest-specific code)
│   ├── io.py                  IOAdapter: Interactive / Scripted transports
│   ├── world_flags.py         Living World State Manager (flags + counters)
│   ├── reputation.py          Reputation hooks + Civilization relationships
│   ├── companion_affinity.py  Affinity hooks + insight gates + banter
│   ├── speech_checks.py       Speech Check framework (5 skills)
│   ├── dialogue_trees.py      Branching, gated, check-driven dialogue
│   ├── puzzles.py             Environmental / engineering puzzles
│   ├── timed_objectives.py    Round-based escalating objectives
│   ├── encounters.py          Multi-stage + ritual-defense encounters
│   ├── split_party.py         Split-party plans + evacuation outcomes
│   ├── consequences.py        Quest Consequence framework
│   ├── quest_framework.py     Quest / Stage / step-runner / QuestManager
│   └── registry.py            wires content into the engine
├── quests/                    the three quests (thin loaders + banter)
│   ├── debt_comes_due.py
│   ├── what_the_forest_carries.py
│   └── eternal_forge.py
├── data/                      quest content as JSON (design authority)
│   ├── debt_comes_due.json
│   ├── what_the_forest_carries.json
│   └── eternal_forge.json
├── dev_tools.py               permanent developer utilities
├── harness.py                 automated regression harness
├── menu.py                    in-game menu (wired into game_loop.py option 11)
└── README.md                  package overview + deliverables report
```

## How it plugs into the existing engine

* **State:** everything persists under a single `world_state["legacy"]`
  namespace (`quests`, `living_world`, `companion_affinity`,
  `civilizations`, `split_party`, `puzzles`). It is added to
  `world_state.py`'s initial dict and backfilled in
  `ensure_world_state_defaults()`, so old saves migrate automatically.
* **Side effects:** all cross-module signals go through `event_bus.emit`
  (see *Events* below). The frameworks never reach into other managers to
  cause side effects.
* **Entry point:** `game_loop.py` main-menu option **11 → Legacy
  Questlines** calls `legacy.menu.show_legacy_menu()`. `import legacy`
  auto-registers all quests via `registry.register_all()`.

---

## The core idea: quests are data, the engine is generic

A quest is authored as a JSON file (`legacy/data/<quest>.json`) and executed
by a generic, step-based runner. **Adding a new quest requires no new engine
code** — only a data file and a two-line registration.

A quest is: `Quest → ordered Stages → a list of steps`. The runner walks
stages via their `next` link (a step can override with a `goto_stage`
effect for branching) and, at the end, applies the quest's consequences.

### Step types (the `"type"` field of a step)

| Step | Purpose |
|---|---|
| `narrate` | Speak narration / a line (`text`, optional `speaker`). |
| `banter` | Trigger companion banter for a `context` if a matching companion is present. |
| `dialogue` | Run an inline dialogue tree; map its `outcome` to effects via `on_outcome`. |
| `speech_check` | Resolve a speech check; branch into `on_success` / `on_failure` effects. |
| `choice` | Present player options (each with optional `available_if` gate and `effects`). |
| `effects` | Apply a list of declarative effects directly. |
| `complete_objective` | Mark a stage objective complete. |
| `encounter` | Run a `multi_stage` or `ritual_defense` encounter from its `spec`. |
| `split_party` | Execute (and optionally resolve) a split-party `plan`. |
| `resolve_evacuation` / `reunite` | Resolve the evacuation / regroup with reunion banter. |
| `puzzle` | Run an environmental/engineering puzzle. |

### Declarative effects (used by `choice`, `dialogue` outcomes, `effects`)

`flag`, `counter`, `affinity`, `standing`, `relationship`, `reputation`,
`complete_objective`, `goto_stage`. Each is a small dict, e.g.
`{"type": "affinity", "companion": "talos", "amount": 5}`.

---

## Framework reference & extension points

### IOAdapter (`io.py`)
The single seam that lets identical quest data run interactively, under the
harness, and from dev tools. Framework code only uses `say`, `choose`,
`speech_outcome`, `roll`. Swap transports with `set_io(...)`.
**Extend:** add a new adapter (e.g. a web transport) by subclassing
`IOAdapter`.

### Living World State Manager (`world_flags.py`)
Flags and counters under `world_state["legacy"]["living_world"]`. Every
change emits `living_world_changed`, so NPC schedules, merchants, patrols,
refugee populations, travel safety and companion dialogue can all react to a
single flag. **Extend:** subscribe to `living_world_changed` in any manager.

### Reputation & Civilization Relationships (`reputation.py`)
Thin wrapper over `faction_manager` reputation **plus** a civilization
relationship matrix (player↔civ standing and civ↔civ relations).
**Extend:** register a new civilization name; call `adjust_relationship`
from a consequence set.

### Companion Affinity (`companion_affinity.py`)
Richer per-companion layer (complements existing loyalty). `affinity_at_least`
is the canonical gate to *offer optional content* — it returns `False`
(never raises) when a companion is absent, guaranteeing the main quest stays
completable. Banter is registered once per context and triggered by quests.

### Speech Checks (`speech_checks.py`)
Five skills (`persuasion`, `insight`, `diplomacy`, `intimidation`,
`cultural`). Success chance is a transparent sum of base difficulty, class
aptitude, **preparation flags**, **companion insight**, and civilization
**standing**. Checks never hard-fail a quest — callers branch on
`result.success` for optional benefits only. `compute_probability` returns a
full contribution breakdown for dev tools.

### Dialogue Trees (`dialogue_trees.py`)
Branching nodes with choices that can be gated (companion/affinity/flag/
standing), check-driven (route by success/failure), and effectful. Locked
choices are still shown so players see what preparation unlocks. Guaranteed
to terminate.

### Puzzles (`puzzles.py`)
Ordered steps; wrong actions cost a hint, never a fail. Companion insight can
reveal the correct action (preparation reward). Solving sets
`on_solve_flags`.

### Timed Objectives (`timed_objectives.py`)
Round-based, escalating, with optional objectives, ending on a **success
condition** rather than enemy elimination. Basis for the eight-round ritual
defence.

### Multi-Stage Encounters (`encounters.py`)
`multi_stage` (waves) and `ritual_defense` (round-based). Resolution is a
transparent `party_strength` vs threat model so it runs in the harness and is
designer-reasonable. A lost wave/round is a **setback flag**, not a
game-over. `launch_interactive()` bridges to the turn-based `combat.py` for
studios that want full manual combat.

### Split Party (`split_party.py`)
Records a plan (main companion + evacuation group), resolves the evacuation
by composition/affinity (never a fail — a quality band), and reunites with
banter. Absent companions are dropped so the main path is unaffected.

### Consequences (`consequences.py`)
Declarative world changes applied once at quest completion, each optionally
gated by a branch flag (`requires`). Handles flags, counters, standings,
relationships, reputation, and inert `future_hook`s
(`CANON_PENDING`-aware).

---

## Events emitted (add to `docs/systems/event_bus.md`)

`living_world_changed`, `reputation_changed`, `civ_standing_changed`,
`civ_relationship_changed`, `companion_affinity_changed`,
`speech_check_resolved`, `puzzle_solved`, `timed_objective_completed`,
`timed_objective_failed`, `encounter_started`, `encounter_wave_started`,
`encounter_completed`, `party_split`, `evacuation_resolved`,
`party_reunited`, `quest_started`, `quest_stage_entered`,
`quest_objective_completed`, `quest_consequences_applied`. Legacy quests also
emit the engine's existing `quest_completed` event on completion.

---

## How to add a future Legacy Questline

1. Write `legacy/data/<quest>.json` using the step schema above.
2. Add `legacy/quests/<quest>.py` with `build()` (loads the JSON) and
   `register_banter()`.
3. List the module in `registry.register_all()`.
4. Add a harness `Scenario` (prepared + minimal branches) to
   `legacy/harness.py`.

No engine changes are required. That is the whole point.

---

## Testing

* `python legacy/harness.py` — non-interactive regression across all three
  quests, both prepared and minimal parties (validates completion,
  objectives, branch-specific consequences, and that ritual defence endures
  without the recommended companion). Report: `legacy/harness_report.json`.
* Developer dry-runs / stage jumps: `legacy/dev_tools.py`.
