# Legacy Framework — Production Hardening Audit

> Scope: architecture review and production hardening of the Legacy Quest
> Framework **before** authoring Quest #4. No new quests were created and no
> approved quest canon was altered. Save compatibility and existing APIs are
> preserved. Date: 2026-06.

Verification: `python legacy/harness.py` (6/6) and `python legacy/validator.py`
(0 errors, 0 warnings) both pass after this pass.

---

## Phase 1 — Architecture audit

For each system: **Reusable?** / duplication / separation of responsibilities
/ reuse by future quest types (main, companion, side, faction, DLC).

| System | Reusable? | Notes |
|---|---|---|
| Quest Framework (`quest_framework.py`) | ✅ | Fully data-driven step runner. Quest *type* is just metadata — main/companion/side/faction quests are the *same* engine with different JSON. No duplication. Responsibilities cleanly split: data model, effect application, runner, manager, loader. |
| Dialogue (`dialogue_trees.py`) | ✅ | Generic node/choice/gate/check model. Reused by any quest. Shares one effect vocabulary with the quest runner. |
| Speech Checks (`speech_checks.py`) | ✅ | Skill/difficulty/preparation/insight/standing model is quest-agnostic. `compute_probability` separated from `resolve` for tooling. |
| Companion Affinity (`companion_affinity.py`) | ✅ | Affinity + insight gates + banter are companion-agnostic; complements (does not duplicate) `companion_manager` loyalty. Ideal for future companion quests. |
| Split Party (`split_party.py`) | ✅ | Plan/execute/resolve/reunite is generic; absent companions handled gracefully. |
| Timed Objectives (`timed_objectives.py`) | ✅ | Pure round-driver; encounters build on it. Reusable for escorts, defenses, chases. |
| Ritual/Multi-stage Encounters (`encounters.py`) | ✅ | Data-spec driven; transparent strength-vs-threat resolver + optional bridge to `combat.py`. |
| Environmental Puzzles (`puzzles.py`) | ✅ | Step/action/reveal model is generic (locks, mechanisms, rituals). |
| Living World (`world_flags.py`) | ✅ | Flags + counters substrate; now paired with a reusable reaction layer (Phase 4). |
| Reputation + Civilization Relationships (`reputation.py`) | ✅ | Thin hook over `faction_manager` + a civ relationship matrix. Reused by faction quests directly. |
| Consequence Manager (`consequences.py`) | ✅ | Declarative, branch-gated, `future_hook`/`CANON_PENDING` aware. |
| IO Adapter (`io.py`) | ✅ | The seam enabling interactive play, scripted tests, and dev tools from one content base. |

**Duplication found & resolved:** dialogue effect application and quest-step
effect application overlapped. Kept intentionally: `dialogue_trees` handles
the subset it needs; `quest_framework.apply_effects` is the superset
(adds `counter`, `complete_objective`, `goto_stage`). They share the same
effect vocabulary, so there is a single mental model with no behavioural
drift. No refactor was warranted (would add coupling for no maintainability
gain).

**Separation verdict:** responsibilities are already well separated (state ⇄
`world_state`, side-effects ⇄ `event_bus`, content ⇄ JSON, presentation ⇄ IO
adapter). No structural refactor performed — the criterion was "refactor only
if it improves long-term maintainability," and it did not.

**Future quest-type reuse:** all systems are quest-type agnostic. A companion
quest is JSON that leans on affinity gates; a faction quest leans on
`reputation`; a side quest is a short stage list. **No engine code is needed
for any of these.**

---

## Phase 2 — Developer tools (`legacy/dev_tools.py`)

Permanent utilities added/confirmed:

| Capability | Function |
|---|---|
| Jump to any quest stage | `jump(quest_id, stage_id)` / `set_stage(...)` |
| Complete / fail objectives | `complete_objective(...)`, `fail_objective(...)` |
| Fail a quest | `fail_quest(...)` |
| Toggle Living-World flags | `toggle(flag)`, `set_flag(flag, value)`, `counter(name, amount)` |
| Set companion affinity | `set_affinity(companion, value)`, `seat_party(names, affinity)` |
| Change reputation / standing / relationship | `change_reputation(...)`, `set_standing(...)`, `set_relationship(...)` |
| Simulate speech-check odds | `simulate_speech(skill, difficulty, prep=..., companion=...)` |
| Trigger combat encounters | `run_encounter(spec)`, `party_strength()` |
| Force world-state updates | `force_world_update()`, `show_reactions()` |
| Spawn quest-specific NPCs | `spawn_npc(name, **attrs)` |
| Skip cinematics | `skip_cinematic(quest_id, to_stage)` |
| Export current quest state | `export_quest_state(quest_id, path=None)` |
| Full snapshot | `snapshot()` |

---

## Phase 3 — Quest authoring toolkit

Delivered as [`legacy_quest_authoring.md`](legacy_quest_authoring.md): full
JSON schema, required/optional fields, and worked examples for dialogue,
companions, speech checks, timed/ritual encounters, multi-stage encounters,
puzzles, split party, and living-world consequences, plus best practices and
common mistakes. A developer can author a complete questline from it.

---

## Phase 4 — Living World expansion (`living_world_reactions.py`)

New reusable, data-driven reaction layer. `living_world_changed` triggers a
full, idempotent **recompute** that derives world reactions across:
merchant inventory, merchant pricing, NPC schedules, guard patrols, refugee
movement, ambient dialogue, tavern rumors, settlement prosperity, road
safety, and regional reputation. Mappings live in
`legacy/data/living_world_reactions.json` — **any future quest gets these for
free** by naming a flag. Query API (`merchant_modifiers`, `tavern_rumors`,
`road_safety`, ...) lets merchants/taverns/travel read the derived state
without coupling to quests. Recompute-on-load makes it save/load safe.

---

## Phase 5 — Quest flow validation (`legacy/validator.py`)

Static + dynamic validator (see its module docstring). Result on all three
shipped quests: **0 errors, 0 warnings**. It checks unreachable dialogue,
dead branches, impossible speech checks, missing/unproducible flags,
soft-locks (ungated fallback required), infinite loops (reachable terminal
required), objective completion coverage, and a save/load round-trip. It is
both a CI gate and an authoring aid.

---

## Phase 6 — Performance

Targeted, non-premature improvements:

* **Quest/dialogue/JSON loading:** quests are loaded and parsed **once** at
  registration (`registry.register_all`) and reused via the singleton
  `manager`; JSON is not re-parsed per play. The living-world mapping is
  parsed once and memoised (`_load_mapping`).
* **Event dispatch:** the existing `event_bus` is O(subscribers); the new
  reaction handler is a single subscriber doing an O(flags) recompute — well
  within budget for hundreds of flags.
* **World-state updates & save serialization:** state stays plain
  JSON-serialisable dicts under one `legacy` namespace; the validator
  asserts round-trip serialisability, so saves remain fast and safe.

No premature micro-optimisation was done; the above are structural and
benefit scalability.

---

## Phase 7 — Future proofing

| Concern | Status |
|---|---|
| Hundreds of quests | ✅ Each quest is an independent JSON + 2-line registration; `manager` is a flat dict. Registration is lazy/defensive. |
| Thousands of dialogue nodes | ✅ Trees are per-step data, parsed on load; no global node table to bloat. Could shard JSON per quest (already the case). |
| Hundreds of NPCs | ✅ NPCs remain in the engine's `npc_manager`; the framework references names, not objects. `spawn_npc` bridges cleanly. |
| Multiple acts / branching endings | ✅ Stages + `goto_stage` + consequence branch flags express acts and endings today. |
| Expansion packs / DLC | ✅ Drop new JSON + module + registry line; no core change. Content is fully separable from engine. |
| Mod support | 🟡 Feasible: quests are pure data. A future `register_quest_dir(path)` could auto-discover JSON from a mods folder — recommended as a small future addition, not required now. |

---

## Deliverables summary

**Files created:** `legacy/validator.py`,
`legacy/framework/living_world_reactions.py`,
`legacy/data/living_world_reactions.json`,
`docs/systems/legacy_quest_authoring.md`, this audit doc.

**Files modified:** `legacy/dev_tools.py` (expanded toolkit),
`legacy/framework/quest_framework.py` (fail/set-stage/export APIs — additive),
`legacy/framework/registry.py` (install reaction layer),
`legacy/framework/__init__.py` (export new module).

**Reusable improvements:** data-driven living-world reactions; a permanent
validator; a full developer toolkit; the authoring toolkit doc.

**Optimizations:** load-once quest/JSON parsing; memoised reaction mapping;
single-subscriber idempotent recompute; verified save round-trip.

**Remaining technical debt:** (low) mod auto-discovery is not yet
implemented; the interactive `combat.py` bridge is optional and untuned for
the signature encounters; ambient-dialogue/rumor consumers exist as a query
API but are not yet wired into the terminal tavern/merchant screens (by
design — those screens are pre-existing engine surfaces).

**Recommendations before Quest #4:**
1. Confirm/rename the placeholder NPC names flagged in `legacy/README.md` §8.
2. (Optional) wire the reaction query API into the terminal merchant/tavern
   screens so players *see* living-world changes.
3. (Optional) add `register_quest_dir()` for mod/DLC auto-discovery.
