# Legacy Questline Architecture — Deliverables Report

This package is the production-quality, reusable quest architecture for
Elyndor, delivered as the vertical slice that implements the three approved
Legacy Questlines. It establishes the foundation every future questline
builds on: a new quest is a JSON data file plus a two-line registration, with
**no new engine code**.

Play it in-game: **main menu → 11. Legacy Questlines**.
Validate it: `python legacy/harness.py` (6/6 scenarios pass).
Full developer docs: [`docs/systems/legacy_quest_framework.md`](../docs/systems/legacy_quest_framework.md).

---

## 1. Every file created

**Reusable framework (`legacy/framework/`)**

| File | Reusable system |
|---|---|
| `io.py` | IOAdapter (Interactive / Scripted transports) |
| `world_flags.py` | Living World State Manager |
| `reputation.py` | Reputation hooks + Civilization Relationship Tracking |
| `companion_affinity.py` | Companion Affinity Hooks + Insight Gates + Banter |
| `speech_checks.py` | Speech Check Framework (5 skills) |
| `dialogue_trees.py` | Dialogue Tree Framework |
| `puzzles.py` | Environmental Puzzle Framework |
| `timed_objectives.py` | Timed Objective Framework |
| `encounters.py` | Multi-Stage Combat Encounters |
| `split_party.py` | Split Party Framework |
| `consequences.py` | Quest Consequence Framework |
| `quest_framework.py` | Quest Framework (Quest/Stage/step-runner/QuestManager) |
| `registry.py` | Content registration + world-state migration |
| `__init__.py` | Framework package exports |

**Quest content**

| File | Purpose |
|---|---|
| `legacy/data/debt_comes_due.json` | The Debt Comes Due (content = design authority) |
| `legacy/data/what_the_forest_carries.json` | What the Forest Carries |
| `legacy/data/eternal_forge.json` | Eternal Forge |
| `legacy/quests/debt_comes_due.py` | Loader + banter |
| `legacy/quests/what_the_forest_carries.py` | Loader + banter |
| `legacy/quests/eternal_forge.py` | Loader + banter |
| `legacy/quests/__init__.py` | JSON loader helper |

**Tooling, integration & docs**

| File | Purpose |
|---|---|
| `legacy/dev_tools.py` | Permanent developer utilities |
| `legacy/harness.py` | Automated regression harness |
| `legacy/menu.py` | In-game menu |
| `legacy/__init__.py` | Package entry (auto-registers quests) |
| `legacy/README.md` | This report |
| `docs/systems/legacy_quest_framework.md` | Developer-facing framework docs |
| `docs/handoffs/2026-06-15-legacy-questline-integration.md` | Session handoff |

## 2. Every file modified

| File | Change |
|---|---|
| `world_state.py` | Added the `world_state["legacy"]` namespace to the initial state and to `ensure_world_state_defaults()` (save migration). |
| `game_loop.py` | Added main-menu option **11. Legacy Questlines** (Exit moved to 12) wired to `legacy.menu.show_legacy_menu()`. |
| `CHANGELOG.md`, `PROJECT_STATE.md`, `docs/handoffs/README.md` | Documentation updates (documentation-first repo rule). |

## 3. Reusable systems added
Quest Framework · Companion Affinity Hooks · Companion Banter · Dialogue
Trees · Speech Check Framework · Split Party Framework · Timed Objective
Framework · Multi-Stage Combat Encounters · Environmental Puzzle Framework ·
Living World State Manager · Reputation Hooks · Civilization Relationship
Tracking · Quest Consequence Framework. (All requested systems delivered.)

## 4. Reusable frameworks expanded
* `faction_manager` reputation is now reached through `reputation.adjust_reputation`.
* `companion_manager` loyalty is complemented (not replaced) by the new affinity layer.
* `event_bus` gains ~20 new Legacy events (see the systems doc).
* `combat.py` remains available via `encounters.launch_interactive()`.

## 5. Living World integrations added
* **Debt:** frontier camp closes, Talos's town grows, refugees settled,
  Stonefang volunteers remain, safer frontier travel, Human⇄Stonefang
  relationship shifts (peace vs uneasy branch).
* **Forest:** forest restored, wildlife returns, Mossroot patrols expand,
  safer forest travel, restored Warden distant sightings (branch), sacred
  saplings grove (optional-objective branch).
* **Forge:** Eternal Forge active, dwarven trade resumes, better-crafted
  goods, roads/bridges improving, renewed hope, restored infrastructure
  counter, restored construct ally (branch), deep stair remains sealed.

## 6. Companion integrations added
Featured companions **Talos** (Forge; also present through Debt via his
hometown) and **Corwin** (Forest) with affinity-gated insight, optional
outcomes, and per-context banter. Every quest is completable with any party;
companions only *add* insight, dialogue, and optional rewards.

## 7. Placeholder values created
* `future_hook` consequences registered as inert flags only:
  `hook_prosperous_town_of_new_beginnings`,
  `hook_foundations_of_the_council_of_embers` (`CANON_PENDING`),
  `hook_restored_warden_recurring_presence` (`CANON_PENDING`),
  `hook_sealed_lower_chamber` (`CANON_PENDING`),
  `hook_ancient_guardian_of_the_deep` (`CANON_PENDING`).
  None are surfaced to the player.

## 8. Canon assumptions requiring approval
1. **Human captain name.** The implementation prompt said "Thomas
   Hawthorne"; the approved package (`Elyndor_Quest_Expansion_Package_v2`)
   says **"Captain Thomas Rourke."** Per Canon Protection we used the package
   (Rourke). *Confirmed with the requester.*
2. **Supporting NPC names not in the packages** were needed for playable
   dialogue and are marked as assumptions pending approval:
   `Skarn` / `Halden` (the two grieving veterans, described but unnamed in
   the design), and `Master Builder Durga` (a Master Builder spokesperson).
   These can be renamed in the JSON without code changes if canon differs.

## 9. Blockers encountered
None. All three quests are integrated, playable, and pass the automated
harness. Full turn-based combat integration is available but optional
(`encounters.launch_interactive`); the reusable data-driven resolver is the
default so encounters run headless in tests.
