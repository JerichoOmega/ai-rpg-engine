# PRD — Legacy Questline Architecture (Elyndor RPG)

## Original Problem Statement
Implement three approved Legacy Questlines (The Debt Comes Due, What the
Forest Carries, Eternal Forge) into the existing terminal Python RPG **as
reusable systems** that establish the foundation for all future questlines.
Preserve design pillars (Living World, companions never mandatory, natural
speech checks, tactical combat that serves story). Do not redesign, simplify,
or invent canon. Mark gaps `CANON_PENDING`.

## User Choices (confirmed)
- Full playable integration wired into `game_loop` + a runnable demo harness.
- Both automated harness AND permanent developer debugging tools.
- Canon: use "Captain Thomas Rourke" (package authority) over prompt's "Hawthorne".
- Clean, standard, well-documented Python for new modules; preserve legacy style elsewhere.
- Documentation-first: full framework docs, PROJECT_STATE/CHANGELOG/handoff updates.

## Architecture
Terminal Python RPG. `world_state.py` = single source of truth;
`event_bus.py` = cross-module side effects; modular managers.
New: `legacy/` package layered strictly on top of those two, with all quest
content authored as JSON data executed by a generic step-runner.

## Core Requirements (static)
Reusable frameworks: Quest, Companion Affinity + Banter, Dialogue Trees,
Speech Checks (5 skills), Split Party, Timed Objectives, Multi-Stage
Encounters, Environmental Puzzles, Living World State, Reputation,
Civilization Relationships, Quest Consequences. Companions optional; speech
checks never hard-fail the main quest; combat serves story with one signature
encounter per quest; lasting Living-World consequences.

## What's Been Implemented (2026-06-15)
- 13 reusable framework modules (`legacy/framework/`).
- 3 data-driven quests (`legacy/data/*.json` + `legacy/quests/*.py`) — verbatim from approved packages.
- Signature encounters: Debt multi-stage "Corruption Breaks the Truce"; Forest 8-round ritual defence (ends on ritual success); Forge corrupted constructs + engineering puzzles.
- `world_state["legacy"]` namespace + save migration; `game_loop` menu option 11.
- Permanent dev tools (`legacy/dev_tools.py`) and automated harness (`legacy/harness.py`, 6/6 pass).
- Full docs: `docs/systems/legacy_quest_framework.md`, `legacy/README.md`, handoff.

## Production Hardening (2026-06-16)
- Architecture audit (`docs/systems/legacy_framework_audit.md`): all frameworks reusable/quest-type agnostic.
- Expanded developer toolkit (stage jump, objective/quest fail, reputation, force world update, spawn NPC, skip cinematic, export state, simulate speech).
- Authoring toolkit (`docs/systems/legacy_quest_authoring.md`): full JSON schema + examples.
- Reusable Living-World reaction layer (`legacy/framework/living_world_reactions.py` + JSON): flags → merchants/pricing/NPC schedules/patrols/refugees/ambient dialogue/rumors/prosperity/road safety/regional reputation.
- Quest-flow validator (`legacy/validator.py`): 0 errors / 0 warnings across all three quests.
- Verified: harness 6/6, validator clean, independent testing-agent pass (100%).

## Canon Assumptions Pending Approval
- Supporting NPC names not in packages: `Skarn`/`Halden` (grieving veterans), `Master Builder Durga`. JSON-only; renameable without code changes.

## Prioritized Backlog
- P0: Canon approval/rename of placeholder NPC names.
- P1: Additional engine reactions to `living_world_changed` (merchants, patrols, NPC schedules).
- P1: Author the next Legacy Questline using the established JSON + 2-line registration pattern.
- P2: Optional full turn-based combat integration for signature encounters (`encounters.launch_interactive`).
- P2: Persist companion banter cooldowns; expand speech-check aptitude data.

## How to Run / Test
- Play: `python main.py` → menu → 11. Legacy Questlines.
- Regression: `python legacy/harness.py` (report: `legacy/harness_report.json`).
- Dev tools: `from legacy import dev_tools`.

---

## Tactical Combat Foundation — Phase 1 verified (2026-06)
- `tactical/` grid engine independently verified STABLE against
  `Combat_Gameplay_Architecture.md`: 32/32 harness PASS + 21/21 testing-agent
  tests (`/app/test_reports/iteration_3.json`). Harness: `python -m tactical.verify`.
  Report + checklist: `docs/verification/phase1_combat_foundation.md`.
- Tracked debt (Phase 2/6): Skill/Item actions unwired (abilities decorative),
  Mage Spell Focus no-op, 4 AI-profile names missing from `ai_profiles.json`.
- **OPEN DECISION R-01 (blocks combat unification):** combat-canon conflict
  between `Combat_Gameplay_Architecture.md` (move+AP, Prepare, N-party) and
  `docs/GAME_BIBLE.md`/`docs/COMBAT_SYSTEM.md` (MP+AP+Support, Facing, Shield
  Stance, Downed/Death, Initiative, 4-hero party). Not to be resolved by guess.

## Production Audit (2026-06)
- Full audit: `docs/PRODUCTION_AUDIT.md`. Core finding: **engine-rich,
  wiring-poor**; three disconnected combat/enemy stacks; deep lore, thin loop.
- 5 gated phases, top-20/engine-10/content-10/risk-5 lists inside.

## Phase 1 Wiring Sprint — DONE (2026-06)
Goal: expose existing systems through gameplay (no new systems, no combat changes).
- **NEW glue:** `world_actions.py` (travel/settlement/explore/map orchestration).
- **Wired `game_loop.py`:** Explore → player-choice menu (reuses encounters/
  quests/events); Travel → `travel_manager.travel_to_region` (destination
  choice, region transition, road events, world tick); Regions → live
  `world_map`; Settlements → enter-scene (services→`shop`/`black_market`,
  faction presence, NPCs→`dialogue_manager.start_dialogue`, quest board).
- **Verified already-fixed:** save validation (`npcs` removed from required in
  `state_manager`); player-state sync (`player.sync_*` wired into save/load).
- Smoke tests: `scripts/smoke_phase1_wiring.py`, `scripts/smoke_phase1_deep.py`
  (region transition, dialogue, quest board — all pass, no exceptions).
- No combat code touched; compatible with either R-01 outcome.
- **Independently verified (2026-06):** `backend/tests/test_phase1_wiring_integration.py`
  23/23 pass; report `test_reports/iteration_4.json` +
  `docs/verification/phase1_wiring_integration.md`. Two seam bugs found & fixed:
  (1) CRITICAL `event_bus.emit` keyword collision crashing ~25% of travel days
  (fixed: event key made positional-only); (2) TD-001 region-discovery divergence
  (fixed: `complete_travel` syncs both stores). **PHASE 1 = COMPLETE.**
- **Next gate = R-01** (combat canon) before Phase 2 combat unification / any
  Phase 3 content.

## R-01 Combat Canon — APPROVED (2026-06)
Option (a) with a canon hierarchy (`docs/design_decisions/R-01-combat-canon.md`):
- **Gameplay Canon (Design Authority):** `GAME_BIBLE.md` + `COMBAT_SYSTEM.md`
  (how combat should feel; full feature set).
- **Technical Canon (Implementation Authority):** `tactical/` +
  `Combat_Gameplay_Architecture.md` (the single combat runtime).
- Rules: one engine / entry point / enemy framework / ability framework / AI
  framework. Evolve `tactical/` ADDITIVELY (never rewrite to match old docs,
  never remove verified features). Enemies→tactical blueprints; legacy
  `enemy_manager`/`combat.py` are Compatibility Layers (do not extend).
- Doc banners added to the three combat docs marking Gameplay/Technical canon.

### Migration order: A (facing/flanking/opportunity) → B (downed/death) →
C (shield stance/support actions) → D (initiative/party/polish).

## Phase A — Facing / Flanking / Opportunity — COMPLETE (2026-06)
- Additive: `tactical/facing.py` (new); `entities.Combatant.facing`;
  `inspection.compute_hit_chance` exposes facing/flanking; `movement_preview`
  exposes `provokes_opportunity_from`; `actions.move` sets facing + opportunity
  attacks; `actions._resolve_attack` applies rear ×1.25 flank damage + FLANK tag.
- Verified: harness `python -m tactical.verify` 40 checks 38 PASS/0 FAIL/2 WARN;
  independent `backend/tests/test_phase_a_facing_flanking.py` 29/29;
  `test_reports/iteration_5.json`; report `docs/verification/phaseA_facing_flanking.md`.
- No regressions; legacy `combat.py`/`enemy_manager.py` untouched.
- **Next: Phase B (Downed/Death/Recovery).**

## Combat Bridge (audit C1) — COMPLETE (2026-06)
Every STANDARD overworld encounter now runs on the canonical tactical engine.
- **New:** `combat_bridge.py` (overworld→tactical entry: party from world+companions,
  blueprint enemies via `tactical.encounters.build_group`, biome→group map, fairness
  cap, reward/HP write-back via `award_xp_to_roster`/gold/`generate_loot`);
  `tactical/session.py` (interactive terminal combat UI + headless mode).
- **Wired:** `world_actions.explore_menu` "Hunt" → `combat_bridge.start_encounter`.
  Legacy `combat.py`/`enemy_manager` = Compatibility Layers (not reachable from the
  standard path, not extended).
- **Verified:** `backend/tests/test_combat_bridge.py` 18/18; full backend suite 91/91;
  tactical harness STABLE; `test_reports/iteration_6.json`;
  report `docs/verification/combat_bridge.md`.
- Follow-ups (later phases): threat-budget scaling + real 4-hero party; city
  encounter groups (urban→roadside stopgap).
- **Approved sequence next:** enemy personality profiles → Phase B (Downed/Death)
  → combat feedback → one polished vertical slice before broad content.
