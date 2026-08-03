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
