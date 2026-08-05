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

## Enemy AI Personalities + Behavior Memory — COMPLETE (2026-06)
Priority 1/5 of the Engine→Game directive. Reusable, data-driven AI library.
- **`tactical/data/ai_profiles.json`** — 20 archetypes; the 4 missing referenced
  profiles (caster/ambusher/defender/aggressive) added → missing-profile WARN cleared.
- **`tactical/ai.py`** — honours profile flags (charges/kites/hold_position/
  prefers_flank/fearless/avoids/flee) via one code path; sticky targeting +
  `_update_memory` + `_retreat`. No enemy-specific AI.
- **`enemies.resolve`** fail-loud (warn + fallback) on undefined profile.
- **`Combatant.ai_memory`** — target_id/turns_chasing/morale/commander_nearby/
  currently_flanking, each influencing decisions.
- **Verified:** `backend/tests/test_ai_personalities.py` 25/25; full suite 116/116;
  harness 47 checks 46 PASS/0 FAIL/1 WARN; `test_reports/iteration_7.json`;
  report `docs/verification/ai_personalities.md`; system doc `docs/systems/tactical_ai.md`.
- **Remaining WARN = Skill/Item ability wiring** (next). Archetype aliases
  (defender≈defensive, ambusher≈assassin) fully differentiate once abilities land.
- **Next: Ability/Item usage → Phase B (Downed/Death) → combat feedback → vertical slice.**

## Combat Phase C — Canonical Ability Pipeline — COMPLETE (2026-06)
The tactical combat engine is now **feature-complete**: Move, Attack, Prepare,
Opportunity, Facing/Flanking, Cover/Elevation, AI personalities, and now
Ability preview + execution + cooldowns + AI ability usage all run on ONE
canonical pipeline with zero duplicate implementations.
- **`tactical/abilities_engine.py`** — single authoritative `ability_preview()`
  (name/AP/cooldown/range/LOS/legal-target/AoE/friendly-fire/expected
  damage&healing/buffs/debuffs/status/tactical_value/usable/failure_reason).
  `use_skill()` is gated by that preview (what the player sees is enforced).
- **Data-driven cooldowns** — per-ability `cooldown` field; tracked in
  `unit.cooldowns`; ticked once in `start_of_turn`; block reuse; save/load via
  `export_state`/`import_state`. No hardcoded ability-specific cooldown logic.
- **AI (`ai.py` `take_turn`)** — evaluates a worthwhile ability BEFORE movement,
  then move, then attack-ability/basic-attack. `choose_ability` reads the same
  preview the player UI does; profile flags (`coordinates`/`buffs_allies`/
  `summons`/`kites`) give gentle role multipliers — no enemy-specific code.
- **Effects** — attack/movement_attack/summon(+heal_zone)/heal/buff/zone/
  control/debuff/terrain/movement handlers; status lifecycle (rooted, poison
  DoT, shielded, emboldened/marked/hexed/cursed); `raise_skeleton` added; class
  abilities capped to AP≤2 to fit the 2-AP economy.
- **Verified:** harness `python -m tactical.verify` **62/62 PASS, 0 WARN**
  (last Skill/Item WARN eliminated); full backend suite **175 passed**;
  independent testing-agent `test_reports/iteration_8.json` 100%, 0 issues.
  Docs: `docs/systems/tactical_abilities.md`,
  `docs/verification/phaseC_ability_pipeline.md`. New suite
  `backend/tests/test_ability_pipeline.py` (31 tests).
- **Next (per user direction):** ONE polished **vertical-slice showcase
  encounter** (elevation + cover + flanking + hazards + distinct AI +
  companion) — NOT Phase B (Downed/Death) yet.

## Gold-Standard Vertical-Slice Encounter — "The Sundered Span" — COMPLETE (2026-06)
The single hand-built reference battle that demonstrates EVERY canonical combat
pillar at once — the benchmark for all future encounter design (not a template
to mass-produce).
- **`tactical/showcase.py`** — a 12×7 ravine-bridge ambush: 4-hero party
  (Guardian/Ranger/Mage/Rogue, healing potions) vs 5 distinct goblin AI
  archetypes (Warlord commander/buffs, Shaman support/heals, Bridge Warden
  defender, Ridge Sniper skirmisher, Corrupted Raider brute). Impassable ravine
  with a bridge chokepoint + slow ford; player & enemy high ground; half/full
  cover; oil + explosive barrel hazard. `pillar_manifest()` maps all 15 pillars
  to a feature + the decision it creates; `tactician_controller()` is the
  reference good-play oracle.
- **Design thesis (verified):** button-mashing LOSES (naive both-AI 0/30),
  competent tactics WIN (~23/30, ~77%), decisive in ~13 rounds. Armoured foes
  make flanking/high-ground/abilities/focus-fire the correct answers, not
  optional flavour.
- **Play:** `python scripts/play_showcase.py` (interactive) /
  `python scripts/showcase_report.py` (headless demo + win-rate).
- **Verified:** `backend/tests/test_showcase_encounter.py` 19/19; full backend
  216/216; harness 62/62/0; independent testing-agent
  `test_reports/iteration_9.json` 100%, 0 issues. Reference doc:
  `docs/design/encounters/gold_standard_sundered_span.md` (seeds the Encounter
  Design Bible).
- **Next:** Encounter Design Bible (archetypes/terrain/composition rules derived
  from this encounter) → combat readability pass → Phase B (Downed/Death).

## Canonical Art Pipeline — Ronan + Torren Imported (2026-06)
Additive art-canon + documentation work; NO gameplay/engine/combat/source files
touched (verified via git status: only docs/ + assets/ changed).

### Ronan — Reference Complete
- Imported 3 approved sheets byte-for-byte into `assets/reference/characters/`:
  `ronan_reference_v1.png` (1024×1536 master), `ronan_character_sheet_v1.png`
  (1536×1024 multi-panel), `ronan_fullbody_v1.png` (1024×1536). SHA-256 recorded;
  source==project==recorded verified.
- Full visual-canon entry added to `docs/canon/Characters.md#ronan` (Human
  Rogue/Duelist, 5'6"/167, reddish-brown copper-undertoned wavy hair + scruff,
  amber eyes, oversized hooded cloak, twin short swords, symbolic nonmagical seed
  pouch; werewolf-form production notes). Narrative canon preserved; art-blurb
  "born into a pack" reconciled as art-context only (Hidden Pack stays a later
  discovery per `docs/heroes/RONAN.md`). Eyes = amber-yellow (per master sheet).

### Torren Ironhall — Reference Complete
- Imported 4 approved sheets byte-for-byte: `torren_reference_v1.png` (1536×1024
  master), `torren_turnaround_v1.png` (1536×1024 poses), `torren_fullbody_v1.png`
  + `torren_fullbody_alt_v1.png` (1122×1402). SHA-256 recorded & verified.
- Full visual-canon entry `docs/canon/Characters.md#torren`: **Dwarf** Master
  Blacksmith, ~85 / 4'5" (135cm), reddish-brown/ginger hair + full forge-braided
  beard (one singed braid), warm amber eyes, charcoal/deep-brown/burgundy +
  copper/bronze palette, repaired travelling smith gear, the **Forge Hammer**,
  the **Founder's Compass** (lineage Durin→Barag→Thorek→Borin→Hadrin→Orin→Durgan
  → blank for Torren) and retired **Ironhall Master's Seal**.
- Authored **Clan Ironhall** (`docs/world/factions/clan_ironhall.md`) — first
  named dwarven clan (Iron Peaks craft-honour clan); key figures (Borik
  Stoneheart, Hilda Forgekeeper, Garrik Ironvein, Brynja Emberforge, Odrin
  Runehammer, Durgan); locations (Hall of Names, Hall of Echoes, Silent Forge,
  Empty Pedestal, Ancestral Forge).
- Authored **The Empty Pedestal** companion quest
  (`docs/quests/the_empty_pedestal.md`) — truth-vs-oath; Durgan's impossible
  choice; the sealed High-King letter twist; "no villain" rule; canonical ending
  (disgrace mark removed, Silent Forge relit with the Master's Seal, Torren's
  name engraved in the Founder's Compass).
- Reconciliations: race corrected Human→Dwarf in `docs/characters/torren.md`
  (approved); companion quest is complementary to — not a replacement for — the
  reserved personal Core Wound (the **Cold Clasp**, `docs/heroes/TORREN.md`),
  which is preserved.
- Updated `assets/reference/characters/README.md`, `docs/canon/
  Character_Production_Status.md` (Ronan+Torren now Reference Complete;
  3D/rig/Godot/animation/UI/marketing still Not Started), `docs/world/RACES.md`
  (dwarf-culture cross-ref).

### Validation (agent-tested)
- All 7 imported assets: project == recorded SHA-256 == source (PASS).
- Talos/Eleanor/Ragash assets unchanged (10/10 PASS).
- 1169 markdown links checked; ALL links in new/edited files resolve.
  12 pre-existing broken links remain in UNTOUCHED files (`docs/GAME_BIBLE.md`,
  `docs/encounters/religious_encounters.md`) — not introduced by this work.
- Talos/Eleanor/Ragash/Ronan/Torren are now the five fully-canonical production
  characters (Reference Complete).

## Torren Ironhall — Canon Revision v1.2 (2026-06)
Additive refinement; only 3 docs changed (Characters.md, clan_ironhall.md,
the_empty_pedestal.md). No assets/source touched.
- **Founder replaced:** placeholder Durin → **Baelor Ironhall** (*The First
  Builder / The Stonewright / The First Master*) — original, non-franchise name.
  Baelor canon: greatest builder (Great Halls/Bridges/Fortress Gates/Mountain
  Roads/Aqueducts/Foundries/Public Forges); belief *"A kingdom's strength is
  measured by what remains when the fighting ends."*
- **Clan motto:** **"Truth is the first measurement."** (now in clan doc, compass
  description, quest doc, clan history).
- **Founder's Compass expanded:** personally forged by Baelor; explicitly NOT
  magical; each Clan Master adds name + personal maker's mark + one lesson →
  documented as a **living historical record**. **Baelor's First Lesson**
  (founding inscription, before any name): *"Measure the stone before you shape
  it. Measure yourself before you judge another."* — philosophical origin of the
  quest.
- **Ending refined (The Empty Pedestal):** Borik restores the name in the Hall of
  Names; Torren completes ordinary craftsmanship at the Silent Forge and stamps
  it with the Master's Seal; opens the Compass and engraves **Torren Ironhall**
  beneath every prior Master, adding his lesson **"Truth is the strongest
  foundation."** — beginning the next generation.
- **Design intent:** Compass = truth/craftsmanship/patience/legacy/generational
  wisdom; Seal = earned honour/responsibility/stewardship/carrying the name.
  Together: the Compass seeks truth; the Seal accepts responsibility.
- Validation: no residual placeholder-founder lore refs (only revision-history
  notes documenting the change); Baelor + motto present in all 3 files; 1172
  links checked, all links in edited files resolve (12 pre-existing broken links
  remain only in untouched GAME_BIBLE.md / religious_encounters.md).

## Canon Maintenance — Doc-Link Repair + Ironhall Timeline (2026-06)
Documentation-only, additive. 3 files changed: docs/GAME_BIBLE.md,
docs/encounters/religious_encounters.md, docs/lore/TIMELINE.md.
- **Repaired 8 genuinely broken links:** GAME_BIBLE.md `../game_tone.md`→`game_tone.md`
  and 6× `../characters/…`→`characters/…`; religious_encounters.md fixed a
  malformed nested link → `[**The Acceptable Risk**](../quests/threshold_circle_questline.md)`.
  (The 4 GAME_BIBLE `#…--…` TOC anchors were never actually broken — valid `&`
  headings; earlier report was a validator false-positive, now corrected.)
- **Ironhall timeline integration** in `docs/lore/TIMELINE.md`: new
  "Clan Ironhall — Historical Anchors" section + Key Dates rows — Baelor founding
  (deep past, era `_TBD_`), Durgan's Broken Oath (Age of Restoration, generations
  back, date `_TBD_`; explicitly a *separate* catastrophe from the Sundering),
  and Torren's restoration (campaign present). Cross-referenced clan_ironhall.md +
  the_empty_pedestal.md; no dwarf-only isolated history; no existing entries changed.
- **Validation:** full link scan = **1179 links, 0 broken**. No gameplay/engine/
  asset files modified; no duplicate lore. Intentional new `_TBD_`: exact
  founding era, Durgan's exact date.
