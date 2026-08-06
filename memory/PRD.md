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

## Next-Action Batch — Compass Sheet, Party Key-Art, Torren Field-Forge Slice (2026-06)
### Art (generated + documented)
- `assets/reference/props/founders_compass_interior_v1.png` (1264×848) — compass
  interior: Baelor's First Lesson + engraved Master lineage. Documented in props
  README + Characters.md Founder's Compass.
- `assets/reference/marketing/party_lineup_keyart_v1.png` (1264×848) — all five
  heroes at true relative scale (Talos 188 / Ragash 170 / Eleanor 167 / Ronan 167
  / Torren 135). Documented in marketing README as a canon-derived derivative
  (per-character sheets remain source of truth).

### Torren Field-Forge Slice — "The Forge Stand" (playable, verified)
- New: `tactical/showcase_forge.py`, `scripts/forge_showcase_report.py`,
  `backend/tests/test_forge_showcase.py`, `docs/design/encounters/forge_stand_torren.md`.
- Data (additive): `smith` class (sturdy, weak-hitting: 46 HP, armor 4, 4 dmg) +
  6 Field-Forge abilities in `ability_library.json` (field_barricade,
  reinforced_wall, spike_barrier, forge_beacon, reinforce_armor, battle_repairs);
  new `chasm` terrain type; small additive `creates_object` option on the terrain
  effect handler in `abilities_engine.py` (lets terrain abilities place cover
  objects). No existing gameplay/data changed destructively.
- **Proof (ablation):** same party + enemies; only Torren's behaviour differs.
  Torren BUILDS → ~87% win / ~5% loss; Torren BRAWLS → ~22% win / ~42% loss
  (40 seeds). The ~65-pt gap proves his identity is constructs, not stats.
- Verification: harness 62/62 (0 WARN); full suite **227 passed** (11 new); all
  Forge Stand ability/mechanic + design-proof tests green.

## Ronan Companion Quest — "The Lost Howl" (2026-06, additive docs-only)
Files changed: docs/quests/the_lost_howl.md (new), docs/world/hidden_pack.md,
docs/canon/Characters.md (Ronan + Eleanor). No gameplay/asset/engine files touched.
- Canonical title **The Lost Howl**; theme *"what makes a family?"* (belonging /
  chosen family) — completing the flagship triangle: Talos=duty, Torren=honour,
  Ronan=belonging.
- Hidden Pack **Warden tradition** added additively (rescue newly-awakened wolves;
  *"No wolf is left alone"*, *"Know the beast"*) and reconciled with the existing
  isolated-community canon (Sera stays Elder; Alpha = Warden lead; existing
  members/debate preserved unchanged).
- 3-act structure; the **Lost Wolf** twist (awakened utterly alone = Ronan's
  mirror); **save-don't-slay** final encounter (objective flips to *Protect the
  Lost Wolf*) as a defining design goal.
- **Alpha** recurring NPC + preserved lines ("Every wolf deserves a pack." /
  "Because someone once did the same for me.").
- Ending *"I already found my pack." / "Then our work is done."*; **Pack Token**
  (carved wolf, nonmagical) tied beside the seed pouch (hope + belonging).
- Full **Eleanor integration** as Ronan's emotional counterpart (she says "you",
  never "the wolf"; campfire scene; "Look at his eyes"; empty-handed rescue; "I've
  only ever met people"; "compassion is a choice, not a certainty"; braided-cord
  final moment) — documented in Characters.md#eleanor.
- Validation: 1200 links checked, 0 broken; existing Ronan/Hidden Pack/Eleanor
  canon preserved.
- Open `_TBD_`: Alpha named identity/appearance (and whether Alpha == Sera); Lost
  Wolf name/details; final-encounter mechanics + objective-swap implementation;
  roster reconciliation for "Corwin" and "the healer".

## Hidden Pack Alpha art + Lost Wolf (Bram) playable slice + Ronan–Eleanor banters (2026-06)
Latest 3-item request delivered & self-validated (agent-tested; not yet user-playtested).
Files (committed HEAD): assets/reference/characters/hidden_pack_alpha_reference_v1.png (new),
assets/reference/characters/README.md, docs/canon/Characters.md (Alpha entry),
docs/quests/the_lost_howl.md, docs/world/hidden_pack.md,
docs/design/encounters/the_lost_wolf_bram.md (new),
docs/design/companions/ronan_eleanor_banter.md (new),
tactical/showcase_lost_howl.py (new), scripts/lost_howl_report.py (new),
backend/tests/test_lost_howl_encounter.py (new). Plus this session:
docs/canon/Character_Production_Status.md (Alpha secondary-NPC row/note).
- **Alpha reference art** imported byte-for-byte: `hidden_pack_alpha_reference_v1.png`
  1264×848, sha256 `943bbcad…fde2e` (matches Characters.md). Canonical, immutable.
  (Note: file bytes are JPEG-encoded content under a .png name — preserved as-is, not
  re-encoded.) Named Alpha identity still `_TBD_`.
- **Lost Wolf named Bram** — "save, don't slay" climax as a headless playable slice:
  objective flips from *Defeat the Beast* → *Protect the Lost Wolf* when the Alpha
  arrives (round 4). No shared gameplay systems modified (design/validation only).
  Proof: compassion play → rescued 100% / murder-hobo → slain 100% over 30 seeds
  (deterministic). Alpha begins offset and arrives later; rescue requires a LIVING wolf.
- **Ronan–Eleanor banters** — travel barks (early/mid/late) + campfire beats; canonical
  exchanges preserved verbatim; Eleanor always says "you", never "the wolf".
- **Production tracker** — Hidden Pack Alpha added as a Secondary/Supporting NPC
  (Reference Complete; 3D→marketing pending). Additive only; no hero rows changed.
- Verification (all agent-tested, PASS): targeted Lost Howl tests 6/6; tactical.verify
  62/62, 0 WARN, FOUNDATION STABLE; full pytest **233 passed** (15.5s); markdown links
  1222/0 broken; Alpha PNG integrity OK; scope audit clean (only intended files; no
  canonical art/gameplay/engine modified; save_data.json + verification_report.json
  test side-effects restored).

## Ronan Canon v1.2 — Character Polish & Hidden Pack Expansion (2026-06, additive docs-only)
Files changed (6, docs only — no gameplay/combat/AI/engine/asset changes):
docs/heroes/RONAN.md, docs/world/hidden_pack.md, docs/canon/Characters.md,
docs/quests/the_lost_howl.md, docs/design/encounters/the_lost_wolf_bram.md,
docs/characters/ronan.md.
- **Ronan finalized** (matches Talos/Eleanor/Torren completeness). Added to the
  hero bible: Central Philosophy *"No one should have to survive alone,"*
  expanded surface/hidden personality, canonical **Daily Behaviours** (Last Watch,
  Eats Last, Counts the Party, Walks the Outside, Never Wastes Food, Anonymous
  Kindness), Relationship With Nature (woodsman first), Animals trust him, the
  Oversized Cloak, the **deeper fear** (afraid of no longer *needing* people —
  additive to the existing werewolf-control fear), Greatest Strength (never leaves
  anyone behind), v1.2 companion beats (Talos takes the watch; Torren makes him
  laugh; Ragash judges by actions; Party Healer names his real fear), Design Intent.
- **Alpha named — Alden Graymane** (distinct character from Sera; prior `_TBD_`
  resolved across hidden_pack.md, Characters.md, the_lost_howl.md). Sera stays
  Elder; Alden leads the Warden/rescue tradition. Traits: patient, compassionate,
  calm, quietly exhausted, wise, soft-spoken; treats Ronan as *"someone who has
  finally come home."*
- **Hidden Pack culture** added: First Law *"No wolf is left alone,"* greeting
  *"Who walks beside you?"*, homecoming howl (not moon-howling), emblem = wolf paw
  growing into tree roots (*"strength through belonging"*).
- **Bram future role**: returns later; the Pack comes to Ronan's aid because of the
  compassion shown in *The Lost Howl* (documented in quest + Bram encounter doc).
- **Legacy sheet reconciled**: docs/characters/ronan.md synchronized to current
  canon (reddish-brown hair, current personality/equipment/Hidden-Pack lore/
  relationships), stale details preserved under a labeled *Legacy Development
  Notes* section, with an authority note (RONAN.md + Characters.md are canonical).
- Validation (agent-tested, PASS): markdown link validator — 0 broken links in all
  6 edited files (recreated a GitHub-accurate validator; 12 remaining broken links
  are all pre-existing and out-of-scope: goblin_tribes exports, PRD, LORE_AUDIT);
  full pytest **233 passed** (engine/gameplay/AI/combat untouched); git scope clean
  (docs only; no code, no canonical assets modified); existing Ronan canon
  preserved and internally consistent.

## Engine-Agnostic Core — Godot Migration Architecture (2026-06, additive docs + reserved dirs)
Non-breaking architecture refactor prep. **No code, gameplay, combat, AI, quest, save, or canon changes.**
Files created (9): docs/architecture/{GODOT_MIGRATION_PLAN, LAYER_RULES, ENGINE_INTERFACES,
GODOT_SCENE_MAPPING, ARCHITECTURE_DECISIONS}.md + reserved README markers in
core/, engine/, engine/godot/, tools/ (no __init__.py → not importable, no code).
- **Audit finding:** `tactical/` combat core is already ~90% engine-agnostic (pure
  logic; presentation isolated to render.py/session.py; showcases run headless with
  0 I/O). No curses/pygame/tkinter lock-in anywhere. Coupling lives in the legacy
  root runtime (world_actions/game_loop) and stray print()s in combat_bridge +
  event_bus. Save = JSON (portable). Canon docs = 100% engine-neutral.
- **Doc set:** migration plan (audit/roadmap/risks/effort/readiness index), layer
  rules + presentation-assumption audit, engine data contracts (CharacterState,
  BattlefieldState, Quest/Dialogue/World/SaveState, Combat/Animation/Reward events,
  intents — field names mirror real code), Godot scene/node/signal mapping, and an
  ADR log (ADR-0001…0009).
- **Godot Readiness: ~55% overall** (combat core ~90%, data/canon ~100%, save ~85%,
  overworld runtime ~40%). Top blocker: engine.log/event_bus are human-string/print
  based, not a structured event stream → highest-value next step (plan P1, additive).
  Migration complexity: Medium (favourable — no graphics-engine lock-in).
- Validation (agent-tested): full pytest **233 passed** (no behavior/save/AI change);
  git scope = only new files, **no .py modified**; reserved dirs not importable;
  markdown links — 0 broken across the 9 new files (11 remaining broken links are
  all pre-existing/out-of-scope: LORE_AUDIT, PRD, goblin_tribes exports). Sundered
  Span / Forge Stand / Lost Howl slices remain valid & headless.

## Corwin & Maeve Ashwood — Companion Polish Pass (2026-06, additive docs-only)
Brings the final two core companions to parity with Talos/Eleanor/Ragash/Ronan/Torren.
Completes the 7-companion philosophy set: Talos=Duty, Eleanor=Justice&Hope, Ragash=Loyalty,
Ronan=Belonging, Torren=Honour&Legacy, **Corwin=Truth&Discovery**, **Maeve=Compassion&Hope Through Service**.
Files (11; docs only — no gameplay/combat/AI/recruitment/save/asset changes):
NEW: docs/heroes/CORWIN.md, docs/heroes/MAEVE.md, docs/characters/corwin.md,
docs/characters/maeve.md, docs/quests/the_silent_witness.md,
docs/quests/a_light_in_the_ashes.md, docs/design/companions/corwin_maeve_relationships.md.
EDITED: docs/canon/Characters.md (+Corwin & +Maeve Ashwood entries, art `_TBD_`),
docs/canon/Character_Production_Status.md (+2 party rows "Docs Complete — Art Pending"),
docs/quests/the_lost_howl.md (roster: "the healer" → Maeve Ashwood),
docs/design/companions/ronan_eleanor_banter.md (roster note).
- **Corwin** (Gnome Ranger / Corruption Investigator): theme "the truth is a kindness,
  even when it hurts"; core wound (buried/ignored corruption evidence, self-blame);
  surface/hidden personality; signature habits; Surveyor's Lens + Green Journal;
  exploration & knowledge-first combat identity; companion quest **The Buried Evidence**
  (NEW provisional title, revisable — climax reinforces philosophy, not a boss fight);
  relationships/camp/exploration/banter. Preserved prior Gnome/Ranger/Investigator +
  affinity/roster refs.
- **Maeve Ashwood** (name CANONIZED; "Community Healer" kept as in-world title): theme
  "hope is something you practice"; philosophy "people remember the person who stayed";
  core wound (two war patients, one saved/one lost, both names in her journal); Lantern
  of Ashes + Field Journal; settlement exploration + protect/rescue combat identity;
  expanded **A Light in the Ashes** (recruitment + refuse-to-leave requirement PRESERVED,
  restoration-not-vengeance climax); Elyra (The Living Hearth) faith. **Disambiguated from
  the unrelated cult figure Sister Maeve Thornwell (cults.md).**
- Both entered production tracker as core party (Lore✅ / Canon Doc✅; art & downstream ⬜).
- Remaining `_TBD_`: reference art for both; Corwin quest final title + specifics; Maeve's
  physical description, settlement name/location, the two remembered patient names; combat
  mechanics for both (no new mechanics defined).
- Validation (agent-tested): git scope = docs only, **no .py/asset/save changed** →
  no combat/recruitment regression possible; full pytest **233 passed**; markdown links
  0 broken across all 11 files (11 remaining broken are pre-existing/out-of-scope:
  LORE_AUDIT, PRD, goblin_tribes exports).

## Corwin & Maeve reference art + Corwin quest title finalized (2026-06, additive)
- **Reference art imported** (byte-for-byte, unaltered): `corwin_reference_v1.png`
  (1264×848, sha b213885d…) and `maeve_reference_v1.png` (1264×848, sha 2c851a39…).
  Both promoted to **Reference Complete** in Characters.md + production tracker;
  hero/character bibles + characters README updated; visual identities established.
- **Corwin quest title FINALIZED: "The Silent Witness"** (replaces provisional
  "The Buried Evidence"). Quest file renamed the_buried_evidence.md → the_silent_witness.md;
  documented the title's multivalent design intent (Corwin, the forest, the Green
  Journal, the buried evidence, the quiet consequences, the observer). All canonical
  references synced (CORWIN.md, Characters.md, Character_Production_Status.md,
  corwin.md, the quest doc). Provisional title kept only in historical revision notes.
  Title-only change — narrative/objectives/mechanics/progression unchanged.
- Validation: docs + 2 new image assets only; no .py/save/quest-logic changes.

## Enemy Bestiary + Quest Index + First-Region Slice (2026-06, additive docs-only)
No gameplay/combat/AI/data/save changes. 13 new docs.
- **Bestiary** (`docs/design/enemies/`): index + 10 family docs (wildlife, undead,
  goblins, bandits, cultists, orcs, beasts_and_monsters, forest, constructs,
  corrupted) documenting all **74 existing data units** with role/tier/threat/AI,
  one-lesson-per-basic, encounter tags, and Basic→Veteran→Elite→Champion→Boss
  progression targets (Champion/Boss = `_TBD_`). Doc-only; enemies.json untouched.
- **Companion Quest Index** (`docs/quests/companion_quests_index.md`): links all 7
  companions/quests + philosophy set + naming philosophy. Ragash=The Broken Oath,
  Ronan=The Lost Howl, Torren=The Empty Pedestal, Corwin=The Silent Witness,
  Maeve=A Light in the Ashes, Eleanor="The Weight of What We Build", Talos title `_TBD_`.
- **First-Region Slice** (`docs/design/first_region_vertical_slice.md`): 8-beat
  Frontier pacing stitching existing encounters (forest_wolf_pack, roadside_ambush,
  corrupted_incursion, etc.) + the 3 playable showcases (Sundered Span, Forge Stand,
  Lost Wolf) + companion recruitment/philosophy beats, with readability curve and an
  explicit exists-vs-`_TBD_` scope split (interactive region build = follow-up).
- Validation: git = docs only, no .py/json/save changed; markdown links 0 broken
  across all 13 new files (11 remaining broken = pre-existing/out-of-scope).
