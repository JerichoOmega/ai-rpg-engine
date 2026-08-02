# CONSOLIDATION_REPORT.md

> **Audit-only report — no repository changes made.**
> **Scope:** Complete read-only review of every documentation source in the repository, including `/app/docs/`, `/app/elyndor/`, root-level governance documents, code-adjacent memory files, `attached_assets/`, and the three ZIP archives.
> **Purpose:** Provide a full, decision-grade snapshot of the project's documentation health so the owner can approve the consolidation plan before any file is created, moved, edited, or archived.
> **Method:** Every document listed under §1 was read; contradictions were cross-checked against the Lore Bible (`docs/lore/`), governance documents, and the most recent canonical prompts in `attached_assets/`. Where a contradiction significantly affects gameplay, story, lore, worldbuilding, core mechanics, character canon, or progression, it is flagged for review rather than auto-resolved.
> **Author:** E1 (Project Consolidation Phase — audit pass).
> **Date:** January 2026.

---

## 0. Executive Summary

- **Project identity:** *Project Dungeon Keeper* — an AI-driven, offline-first tactical RPG set in the world of **Elyndor**. A Python terminal prototype (~55 modules) is the current implementation; the long-term target is a Stylized 3D Tactical RPG intended for a Godot prototype next.
- **Documentation volume:** ~90 markdown documents across four overlapping documentation systems (root governance, `docs/`, `elyndor/`, and the newer `docs/lore/` Lore Bible), plus 40+ prompt snapshots in `attached_assets/` and three ZIP archives that are older repository snapshots.
- **Overall documentation health:** 🟡 **Strong content, fragmented structure.** The individual documents are unusually high-quality — carefully written, canon-aware, and philosophically consistent within themselves. The fragmentation problem is structural: the same topic (history, magic, companions, world regions) is authored across two or three parallel folders with overlapping authority, and canon has shifted twice (Four Ages → Seven Ages → back to a *new* Four Ages) without every downstream document being updated.
- **Ready for prototype in Godot?** Not yet. Foundation is 90% ready. What blocks prototype is not writing — it is **structural consolidation** (one canonical index, one canonical history, one canonical companion roster) and **five newly-canonized philosophies from the current session** (Living World, Difficulty by Choice, Offline-First, AI-Optional, Origin Characters + Companion Expertise + Companion Evolution + Settlement Dispersal) that are not yet reflected in any existing document.
- **Recommended path:** Follow the plan in §6. **Do not begin consolidation until this report is reviewed.**

---

## 1. Repository Documentation Inventory

### 1.1 Root-level governance documents (`/app/`)

| File | Lines | Role | Health |
|---|---|---|---|
| `README.md` | 87 | Repo overview + entry-point map | ✔ Consistent |
| `AI_START_HERE.md` | 280 | Session startup + shutdown checklist | ⚠ References obsolete age names via known-issues section (stale) |
| `PROJECT_CONSTITUTION.md` | 372 | Permanent governance (Articles I–XI) | ✔ Consistent |
| `PROJECT_MEMORY.md` | 265 | AI 5-minute quick-start | ⚠ Decision #22 uses obsolete Four-Age names ("Creation/Kingdoms/Wars/Shadows"); Decisions numbered non-sequentially (skips, duplicates 18) |
| `PROJECT_STATE.md` | 264 | Completion %, active bugs, priorities | ⚠ Reflects July 2026 snapshot; does not include the current session's canon additions |
| `DESIGN_DECISIONS.md` | 342 | Architectural decisions 001–016 | ✔ Consistent internally |
| `CHANGELOG.md` | 145 | Milestone history v0.1–v0.4 | ✔ Consistent |
| `architecture.md` | 6 | Redirect stub → `docs/architecture.md` | ✔ Retained as intentional stub |
| `LORE_CONSISTENCY_AUDIT.md` | 437 | Prior lore audit (July 2026) | ⚠ **Itself outdated** — was written when the Seven-Age framework was canonical; several "❌ Major Conflicts" it lists (❌ #1, ❌ #3, ⚠ #5) have since been partially resolved by the owner's directive to restore a new Four-Age framework. Audit remains authoritative for its still-open findings. |

### 1.2 Game documentation (`/app/docs/`)

**Core (13 files):**
`README.md`, `GAME_BIBLE.md` (1053 lines, 56 ToC entries), `AI_CONTINUATION_GUIDE.md`, `architecture.md`, `coding_standards.md`, `known_issues.md`, `roadmap.md`, `dependencies.md`, `CAMPAIGN_DESIGN.md`, `COMBAT_SYSTEM.md`, `PLAYER_SYSTEM.md`, `HERO_BIBLE.md`, `HERO_TEMPLATE.md`, `CHARACTER_DESIGN_GUIDE.md`, `PRONUNCIATION_GUIDE.md`, `game_tone.md`.

**Systems deep-dives (`docs/systems/` — 12 files):**
`world_state.md`, `combat.md`, `ai_director.md`, `save_system.md`, `event_bus.md`, `quests.md`, `factions_economy.md`, `progression_skills.md`, `inventory_equipment.md`, `npcs_companions.md`, `world_regions.md`, `reputation.md`, `dynamic_story_arcs.md`, `journey_system.md`.

**Characters (`docs/characters/` — 8 files + template):**
`README.md`, `_character_template.md`, `talos.md`, `eleanor.md`, `ragash.md`, `ronan.md`, `steven.md` (retired), `torren.md`.

**Heroes (`docs/heroes/` — 7 files):**
`RONAN.md`, `TORREN.md`, `RAGASH.md`, `STEVEN.md` (retired), `TALOS.md`, `ELEANOR.md`, plus the `HERO_TEMPLATE.md` reference.

**World (`docs/world/` — 7 files):**
`WORLD_BIBLE.md`, `RACES.md`, `GEOGRAPHY_LANDMARKS.md`, `vampire_houses.md`, `religions.md`, `cults.md`, `goblin_tribes.md`, `covenant_inquisitors.md`.

**Content authoring (`docs/quests/`, `docs/encounters/`):**
`goblin_tribe_quests.md`, `religious_order_quests.md`, `religious_encounters.md`, `mossroot_first_contact.md`.

**Lore Bible (`docs/lore/` — 11 files + sub-folders):**
`README.md`, `CANON_RULES.md`, `DEVELOPMENT_REFERENCE.md`, `HISTORY_BIBLE.md`, `TIMELINE.md`, `DIVINE_CHORUS.md`, `DIVINE_CHORUS_PHILOSOPHY.md`, `ARCHITECTS.md`, `FIRST_TEMPLE.md`, `IMPERIAL_CAPITAL.md`, `GREAT_LIBRARY.md`. Plus `docs/lore/civilization/` (5 files: `README.md`, `FIRST_EMPIRE.md`, `FIRST_COUNCIL.md`, `FALL_OF_THE_FIRST_EMPIRE.md`, `LEGACY_OF_THE_FIRST_EMPIRE.md`) and `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md`.

**Handoffs (`docs/handoffs/`):**
`README.md`, `HANDOFF_TEMPLATE.md`, `2026-07-30-documentation-session.md`.

### 1.3 Elyndor Universe Bible (`/app/elyndor/`)

| Path | Files | Purpose |
|---|---|---|
| `elyndor/README.md` | 1 | Universe canon rules + index |
| `elyndor/world/` | 1 (`world_overview.md`) | High-level setting |
| `elyndor/ancient_legends/` | 4 (`README.md`, template, `aurelia_sunstrider.md`, `valen_ashfall.md`) | Two confirmed legends |
| `elyndor/bestiary/` | 2 (`README.md`, template) | **Empty — no creatures authored yet** |
| `elyndor/history/` | 4 (`README.md`, `HISTORY_BIBLE.md`, `the_corruption.md`, `the_eighth.md`) | The canonical Forgotten Eighth + Corruption docs live here |
| `elyndor/magic/` | 2 (`README.md`, `MAGIC_BIBLE.md`) | Primordial Magic + Divine Chorus (magic-facing) |
| `elyndor/organizations/` | 1 (`README.md`) | **Empty scaffold — no organizations authored yet** |

### 1.4 Code-adjacent memory (`.agents/memory/`)

| File | Purpose | Health |
|---|---|---|
| `MEMORY.md` | Two-line index | ✔ |
| `integration-pass.md` | Task 3 fix log | ✔ |
| `lore-bible-canon.md` | Lore Bible pinned reference | ⚠ **Still describes the framework as "Seven Ages"** — obsolete since the owner restored a new Four-Age framework. |

### 1.5 Attached prompt archive (`/app/attached_assets/`)

45 files: 44 pasted prompts (`.txt`) spanning the full development history, plus one merge summary and one uploaded `.docx`. The three most recent prompts (by timestamp) are the *most authoritative* recent canon:

1. `Pasted-We-have-finalized-the-historical-structure-of-the-world_1785513288461.txt` — **Establishes the current canonical Four-Age framework** (Awakening → Harmony → Sundering → Restoration). This supersedes every prior history document.
2. `Pasted-Project-Evolution-Plan-Transition-to-a-Living-World-Sim_1785509840763.txt` — **Establishes Living World simulation direction**: AI becomes one subsystem, not the engine; world state is consulted before generation.
3. `Pasted-Flesh-Out-the-False-Ancestor-Cult-Objective-Expand-the-_1785508697949.txt` — Cult expansion prompt.

### 1.6 ZIP archives — status determined

| Archive | Contents | Verdict |
|---|---|---|
| `/app/ai-rpg-engine.zip` (14 MB) | An older `workspace/` snapshot containing `.py` files + a smaller `docs/` tree + duplicates of prompts in `attached_assets/` | **No unique documentation.** `/app` is a strict superset. |
| `/app/ai_rpg_update.zip` (8.8 MB) | Older Python source snapshot with `.pythonlibs/`, `.cache/`, `.git/` — code-only | **No unique documentation.** |
| `/app/project-dungeon-keeper-docs.zip` (297 KB) | Older `docs/` + `elyndor/` snapshot | **No unique documentation.** `/app` is a strict superset — includes everything in the ZIP plus `docs/characters/torren.md`, `docs/heroes/TORREN.md`, `docs/systems/journey_system.md`, `docs/world/GEOGRAPHY_LANDMARKS.md`, `docs/world/covenant_inquisitors.md`, `docs/encounters/mossroot_first_contact.md`, `docs/lore/`, `elyndor/history/HISTORY_BIBLE.md`, `elyndor/history/the_eighth.md`, `elyndor/magic/MAGIC_BIBLE.md`. |

**Verified with `diff -rq`**. The ZIPs contribute no candidate canon that is not already present in `/app`. Recommendation: after consolidation, move all three ZIPs into `/app/docs/archive/snapshots/` with an accompanying `README.md` explaining they are pre-consolidation repository snapshots retained for historical reference only.

---

## 2. Documentation Health — Complete / Partial / Missing

### 2.1 Complete documents (author-ready; can be lifted into the GDD as-is with cross-reference updates)

| Document | Confidence | Notes |
|---|---|---|
| `docs/lore/CANON_RULES.md` | ✅ High | The **immutable core** — every other canon claim must defer to it. |
| `docs/lore/DIVINE_CHORUS.md` | ✅ High | Definitive Chorus doc. |
| `docs/lore/ARCHITECTS.md` | ✅ High | Perfect example of "mystery preserved by design". |
| `docs/lore/FIRST_TEMPLE.md` | ✅ High | Complete + short. |
| `docs/lore/IMPERIAL_CAPITAL.md` | ✅ High | Substantial and self-contained. |
| `docs/lore/GREAT_LIBRARY.md` | ✅ High | Longest lore doc (~50 KB); no gaps. |
| `docs/lore/HISTORY_BIBLE.md` | ✅ High | Narrative history; **matches** the current Four-Age canon. |
| `docs/lore/TIMELINE.md` | ✅ High | Developer chronology; matches Four-Age canon. |
| `docs/lore/DEVELOPMENT_REFERENCE.md` | ✅ High | Canon constitution for developers. |
| `docs/lore/civilization/*.md` | ✅ High | First Empire + Council + Fall + Legacy: all four are cohesive. |
| `elyndor/history/the_corruption.md` | ✅ High | Corruption-as-amplified-virtue canon. |
| `elyndor/history/the_eighth.md` | ✅ High | Five Stages canon, one minor terminology issue (see §3). |
| `elyndor/magic/MAGIC_BIBLE.md` | ✅ High | 490 lines; complete. Minor issues (attribution, terminology) noted in §3. |
| `elyndor/history/HISTORY_BIBLE.md` | ✅ High | Body content matches Four-Age canon; only revision log shows the churn. |
| `docs/world/WORLD_BIBLE.md` | ✅ High | Six regions, factions, choice philosophy — comprehensive. |
| `docs/world/RACES.md` | ✅ High | Six playable races. |
| `docs/world/vampire_houses.md` | ✅ High | Three houses (Vetharis, Drakmor, Soleth). |
| `docs/world/religions.md` | ✅ High | Four traditions (Solari Covenant, Old Ways, Ancestors' Path, Veiled Order). |
| `docs/world/goblin_tribes.md` | ✅ High | Three tribes (Stonefang, Mossroot, Ashfire). |
| `docs/world/cults.md` | ✅ High | Named cults. |
| `docs/world/covenant_inquisitors.md` | ✅ High | Corruption-adjacent framing preserved. |
| `docs/world/GEOGRAPHY_LANDMARKS.md` | ✅ High | Named landmarks. |
| `docs/heroes/TALOS.md`, `ELEANOR.md`, `RAGASH.md`, `RONAN.md`, `TORREN.md` | ✅ High | Full Hero Bibles for all five confirmed companions. |
| `docs/characters/{talos,eleanor,ragash,ronan,torren}.md` | ✅ High | Character sheets. |
| `docs/HERO_BIBLE.md` | ✅ High | Core Wound design philosophy. |
| `docs/CHARACTER_DESIGN_GUIDE.md` | ✅ High | Design checklist for future companions. |
| `docs/CAMPAIGN_DESIGN.md` | ✅ High | Handcrafted-first + dynamic variation. |
| `docs/COMBAT_SYSTEM.md` | ✅ High | Grid + AP + facing + downed rules. |
| `docs/PLAYER_SYSTEM.md` | ✅ High | Phase 1 predefined roster; Phase 2 custom deferred. |
| `docs/systems/journey_system.md` | ✅ High | Travel-as-storytelling + camp evolution. |
| `docs/systems/dynamic_story_arcs.md` | ✅ High | First arc: *The Fractured Circle*. |
| `docs/game_tone.md` | ✅ High | Dark-fantasy + adventure balance. |
| `docs/systems/reputation.md` | ✅ High | Fallout-NV per-faction model. |
| `docs/systems/world_state.md` | ✅ High | Full schema + helpers + migration guard. |
| `docs/systems/event_bus.md` | ✅ High | Every registered event + payload. |
| `docs/systems/save_system.md` | ✅ High | Both systems + migration. |
| `docs/systems/combat.md` (terminal prototype) | ✅ High | Current combat impl vs. canonical target both documented. |
| `docs/systems/quests.md` | ✅ High | CRUD + faction bonus. |
| `docs/systems/factions_economy.md` | ✅ High | |
| `docs/systems/progression_skills.md` | ✅ High | Level 25 cap + shared XP + companion scaling. |
| `docs/systems/inventory_equipment.md` | ✅ High | |
| `docs/systems/world_regions.md` | ✅ High | |
| `docs/systems/npcs_companions.md` | ✅ High | |
| `docs/systems/ai_director.md` | ✅ High | DM Brain pressure + focus map. |
| `docs/coding_standards.md` | ✅ High | |
| `docs/dependencies.md` | ✅ High | |
| `docs/architecture.md` | ✅ High | Module map. |
| `docs/quests/goblin_tribe_quests.md`, `religious_order_quests.md` | ✅ High | One authored quest per tribe/order. |
| `docs/encounters/religious_encounters.md`, `mossroot_first_contact.md` | ✅ High | |
| `elyndor/README.md` | ✅ High | Universe canon rules. |
| `elyndor/ancient_legends/{aurelia_sunstrider,valen_ashfall}.md` | ✅ High | Two legends complete. |
| `docs/PRONUNCIATION_GUIDE.md` | ✅ High | Names + phonemes. |

### 2.2 Partial documents (need reconciliation before use)

| Document | What's Missing / Broken |
|---|---|
| `PROJECT_MEMORY.md` (root) | Decision #22 still uses obsolete age names ("Creation/Kingdoms/Wars/Shadows"); Decisions numbered non-sequentially (skips 17, duplicates 18 twice); missing the current session's canon additions (Living World, Difficulty by Choice, Origin Characters, Companion Expertise, Companion Evolution, Settlement Dispersal). |
| `PROJECT_STATE.md` (root) | Snapshot from July 2026; does not track the new philosophies from the current session; also does not reflect the Four-Age → Seven-Age → new Four-Age churn. |
| `AI_START_HERE.md` (root) | Includes stale bug list; "Full Documentation Map" section omits `docs/lore/`, `docs/lore/civilization/`, `docs/heroes/`, `docs/world/`, `docs/encounters/`, `docs/quests/`. |
| `docs/AI_CONTINUATION_GUIDE.md` | **Line 38** still describes `elyndor/history/HISTORY_BIBLE.md` as "Age of Creation, Age of Kingdoms, Age of Wars, Age of Shadows" — those age names are obsolete per the owner's most recent directive; the file's *body* already uses the new canon. Also missing entries for `docs/lore/CANON_RULES.md`, `docs/lore/DEVELOPMENT_REFERENCE.md`, `docs/lore/civilization/*`. |
| `docs/roadmap.md` | Line 105 references "Four Ages framework established: Age of Creation, Age of Kingdoms, Age of Wars, Age of Shadows" — obsolete age names. Priorities list is unchanged since July 2026. |
| `docs/GAME_BIBLE.md` | 1053 lines, 56 ToC entries. Consistent within itself, but: (a) does not yet document the new Living World / Difficulty by Choice / Offline-First / AI-Optional / Origin Characters / Companion Expertise / Companion Evolution / Settlement Dispersal canon; (b) ToC duplicates entry 5 (Genre + Target Audience both numbered 5); (c) ToC entries 34–56 are cross-file references rather than in-file sections — fine, but should be moved to a "Related documents" appendix. |
| `docs/systems/npcs_companions.md` | Companion roster is complete for the five confirmed companions; missing entries for Corwin (mentioned in current problem statement) and the Future Healer (mentioned in current problem statement). |
| `docs/PLAYER_SYSTEM.md` | Excellent for Phase-1 hero selection; **does not describe Origin Characters** (every companion is also a playable protagonist). This is a substantive new canon layer that reshapes the file. |
| `docs/CAMPAIGN_DESIGN.md` | Complete for handcrafted-first + dynamic variation; missing an explicit "no difficulty setting" clause, missing the "Living World simulation" framing from the latest prompt. |
| `docs/systems/journey_system.md` | Excellent for travel-and-camp; **does not describe Settlement Dispersal** — the new canon that when the party enters a safe settlement, every recruited companion appears somewhere appropriate and can be found there. |
| `docs/HERO_BIBLE.md`, `docs/CHARACTER_DESIGN_GUIDE.md` | Complete for combat identity and Core Wound design; missing sections on **Companion Expertise** (out-of-combat contribution roles: Talos-morale/leadership/children, Torren-engineering/repair, Eleanor-research/arcane-study/teaching, Corwin-tracking/foraging/corruption-investigation, Ragash-hunter-prep/animal-care/survival, Ronan-security/patrols/defense, Future Healer-medicine/community-health/refugee-care) and **Companion Evolution** (permanent behavioral changes after personal quests). |
| `elyndor/history/HISTORY_BIBLE.md` | Body content is fully aligned with the new Four-Age canon; the *revision log entry from the "Four Ages: Creation/Kingdoms/Wars/Shadows" era is still visible* — misleading if read out of context. Also cross-referenced by AI_CONTINUATION_GUIDE with the obsolete names. |
| `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md` | 724 lines. **Header explicitly labels the framework as "Seven Ages narrative framework"** — obsolete since the owner restored a new Four-Age canon. Body content is otherwise a valuable index; must be re-headed with Four-Age labels. |
| `.agents/memory/lore-bible-canon.md` | Refers to the framework as "Seven Ages" — obsolete. |
| `LORE_CONSISTENCY_AUDIT.md` (root) | Written when the Seven-Age framework was canonical. Findings ❌ #1, ❌ #3, ⚠ #5 have been partially resolved by the owner's restoration of the new Four-Age canon. Findings ❌ #2 (AI_CONTINUATION_GUIDE missing Lore Bible references), ❌ #4 (Eleanor + Chorus encounter), ⚠ #1–#4, ⚠ #6–#9 remain **fully open**. |

### 2.3 Missing documents (required for the new canon from this session and for Godot prototype readiness)

**Required by the canon rules the owner just re-stated in the current problem statement:**

| Missing document | Why needed | Suggested target location |
|---|---|---|
| **`GDD/03_Core_Gameplay/DIFFICULTY_PHILOSOPHY.md`** | The owner explicitly states there is no traditional Easy/Normal/Hard; difficulty evolves through choices. No file documents this today. | New |
| **`GDD/08_AI/OFFLINE_FIRST.md`** | The game must be fully playable offline. AI enhances, never replaces. No dedicated file exists (references are scattered across `GAME_BIBLE.md`, `llm_bridge.py` design decisions, and the "Project Evolution Plan" prompt). | New |
| **`GDD/08_AI/AI_PHILOSOPHY.md`** | Defines which AI enhancements are optional (tavern gossip, ambient NPC talk, dynamic rumors, campaign variation) and which content is *never* AI-generated (main quests, companions, endings). No dedicated file exists. | New |
| **`GDD/05_Companions/ORIGIN_CHARACTERS.md`** | Every companion is also a playable Origin character. Existing docs (`PLAYER_SYSTEM.md`, `HERO_BIBLE.md`) name predefined heroes but do not spell out the NPC-vs-PC dual mode: NPC = behavior evolves automatically, PC = additional roleplay choices unlock but personality is never forced. | New |
| **`GDD/05_Companions/COMPANION_EXPERTISE.md`** | Out-of-combat expertise roles per companion (morale/engineering/research/tracking/hunter-prep/security/medicine). Currently a paragraph in the problem statement only. | New |
| **`GDD/05_Companions/COMPANION_EVOLUTION.md`** | Permanent behavioral change after personal quests (Ronan more social, Talos becomes mentor, Corwin more trusting, etc.). Currently a paragraph in the problem statement only. | New |
| **`GDD/05_Companions/SETTLEMENT_DISPERSAL.md`** | On entering a safe settlement the active party disperses; every recruited companion appears somewhere appropriate; each remains available for conversation, party-swap, personal quest, story progression. Never idle. No file today. | New |
| **`GDD/04_World/LIVING_WORLD_SIMULATION.md`** | The "Living World" pillar and the "Project Evolution Plan" prompt define the world as a persistent simulation; the AI reads the world state before generating anything. No consolidated doc today — the concept is scattered across `world_state.py`, `dm_brain.py`, and prompt files. | New |

**Documents for characters mentioned in the new canon but not yet authored:**

| Missing document | Why needed | Notes |
|---|---|---|
| **`GDD/05_Companions/heroes/CORWIN.md`** | Corwin is named in the current problem statement's *Companion Expertise* section ("tracking, foraging, corruption investigation") but does not exist as a companion in the confirmed roster of five. **This is a canon addition and must be reviewed before authoring.** See §4.C1. | ⚠ Requires owner ruling first |
| **`GDD/05_Companions/heroes/FUTURE_HEALER.md`** | Similarly named in the same section ("medicine, community health, refugee care"). Currently only a placeholder concept. | ⚠ Requires owner ruling first |

**Documents for planned systems still absent (per `docs/roadmap.md`):**

| Missing document | Roadmap status | Notes |
|---|---|---|
| `elyndor/bestiary/BESTIARY_BIBLE.md` | [FUTURE] | Scaffolding exists (`_creature_template.md`) but zero creatures authored |
| `elyndor/organizations/*` | [PLANNED] | Only `README.md` exists (7 lines-ish) |
| `elyndor/cultures/CULTURE_BIBLE.md` | [FUTURE] | Halflings + Gnomes are ⚠ NOT YET DEFINED |
| `elyndor/economy/ECONOMY_BIBLE.md` | [FUTURE] | Continent-scale trade + currency + regional economies |
| **`GDD/02_Prototype/GODOT_PROTOTYPE_PLAN.md`** | Not on the roadmap yet | Required to prepare for the next phase per the current problem statement |
| `docs/systems/dialogue.md` | Missing | Dialogue engine referenced but has no dedicated doc |
| `docs/systems/relationship.md` | Missing | Relationship manager exists in code, no doc |
| `docs/systems/settlement.md` | Missing | Settlement manager exists in code, no doc |
| `docs/systems/world_event.md` | Missing | World event manager exists in code, no doc |
| `docs/systems/campaign_manager.md` | Missing | Campaign manager exists in code, no doc |
| `docs/systems/corruption.md` | Missing | Corruption is the central antagonist; canon exists in `elyndor/history/the_corruption.md` (lore side) but no *system* doc for how Corruption is tracked, propagated, and expressed mechanically |

### 2.4 Duplicate documents

| Duplicate pair / group | Recommendation |
|---|---|
| `elyndor/history/HISTORY_BIBLE.md` **and** `docs/lore/HISTORY_BIBLE.md` | These are intentional companions (technical + narrative) and *not* strict duplicates. Both are now consistent with the current Four-Age canon. **Keep both** but add a header banner to each explicitly identifying which is technical and which is narrative and cross-linking. |
| `docs/lore/DIVINE_CHORUS.md` **and** `docs/lore/DIVINE_CHORUS_PHILOSOPHY.md` | Deliberate primary + extended companion. **Keep both** with clear headers. |
| `PROJECT_STATE.md` **and** `PROJECT_MEMORY.md` | Different purposes (state snapshot vs. onboarding) but overlap heavily on completion percentages and rules. **Keep both**; move overlapping content into single canonical sub-sections and cross-link. |
| `save_manager.py` **and** `state_manager.py` (code, not docs) | DECISION-004 flags this as ✅ [CONFIRMED] intentional dual-save; deferred cleanup. Not a doc issue, but the docs should link this decision from `docs/systems/save_system.md` more prominently. |
| Root `architecture.md` (6-line stub) **and** `docs/architecture.md` (full) | Intentional stub. Retain as-is. |
| `docs/heroes/STEVEN.md` **and** `docs/characters/steven.md` | Explicitly retired with redirect notices. Retain as retirement stubs (do not archive). |
| `factions.py`, `regions.py`, `loot.py`, `memory.py` (code, not docs) | Superseded legacy modules. Not a doc issue but referenced throughout docs; recommend an explicit "Deprecation Notice" appendix in `docs/architecture.md`. |
| `ai-rpg-engine.zip`, `ai_rpg_update.zip`, `project-dungeon-keeper-docs.zip` | Older repository snapshots. **Move to `docs/archive/snapshots/`** with a README explaining they are pre-consolidation snapshots — see §5. |
| `attached_assets/*.txt` (44 pasted prompts) | Full history of design prompts. Retain in place; add `attached_assets/INDEX.md` timeline that maps each prompt to the canon layer it introduced. |

---

## 3. Contradictions and Canon Conflicts

Every contradiction below is presented with **both sides** and a **preferred resolution**. Only items marked **[MINOR — will auto-resolve]** will be handled without a ruling; the rest are **[FLAGGED — awaits your approval]**.

### 3.1 Historical framework (THREE overlapping versions in circulation)

**[FLAGGED — awaits your approval, but the current canon is clear]**

- **Version A (obsolete):** Age of Creation → Age of Kingdoms → Age of Wars → Age of Shadows.
  Still cited in: `PROJECT_MEMORY.md` Decision #22, `docs/AI_CONTINUATION_GUIDE.md` line 38, `docs/roadmap.md` line 105, `elyndor/history/HISTORY_BIBLE.md` revision-log entry 1.
- **Version B (superseded):** Seven Ages — Awakening / Discovery / Unity / Long Decline / Sundering / Restoration / Present.
  Still cited in: `.agents/memory/lore-bible-canon.md`, `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md` (header + source table), earlier revision-log entries in `docs/lore/HISTORY_BIBLE.md` and `elyndor/history/HISTORY_BIBLE.md`.
- **Version C (current canonical, most recent prompt + Lore Bible + owner directive):** Four Ages — **Awakening → Harmony → Sundering → Restoration**. The Long Decline is the tragic final chapter of the Age of Harmony, not a fifth age. The game begins near the end of the Age of Restoration.
  Body content of `docs/lore/HISTORY_BIBLE.md`, `docs/lore/TIMELINE.md`, `elyndor/history/HISTORY_BIBLE.md`, `docs/lore/civilization/*.md`, `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md` (body).

**Preferred resolution:** Version C is canonical. Retire Version A and Version B references. Every remaining reference to obsolete age names (§2.2 files) is updated to Version C during consolidation. No content is lost — the *events* attributed to obsolete ages simply map to the new age names.

**Awaits your approval:** confirm Version C is final.

### 3.2 Eleanor's Harmonic Soul — a Chorus member appears in person

**[FLAGGED — awaits your approval]**

- **`docs/heroes/ELEANOR.md` (lines 159–188):** During Eleanor's companion quest at a sealed First-Age sanctuary, *"Eleanor encounters one of the gods"* who explains her Harmonic Soul to her directly.
- **`docs/lore/CANON_RULES.md`:** *"They do not communicate personal divine instructions to individuals."*
- **`docs/lore/DIVINE_CHORUS.md`:** *"If a piece of content requires the Chorus to act, speak, appear, or select someone — it almost certainly violates the principles."*

The scene is written carefully — no chosen-one language, no divine instruction, no ability granted — but a Chorus member is still shown appearing in person and speaking. `LORE_CONSISTENCY_AUDIT.md` already flagged this as ❌ #4 and it remains unresolved.

**Preferred resolution:** Change the delivery mechanism only. The revelation's *content* (Harmonic Soul, what it means, what it does not mean) is fully canon-compatible. Suggested alternatives (from the prior audit):
- The sanctuary itself communicates truth through its magic (no god appears);
- Eleanor experiences an overwhelming impression or vision, not a direct conversation;
- The knowledge arrives through preserved ancient records within the sanctuary (crystallized memory, inscription, etc.).

**Awaits your approval:** pick one delivery mechanism (or offer a fourth).

### 3.3 Companion roster — five vs seven

**[FLAGGED — awaits your approval]**

- **All existing docs:** The confirmed roster is exactly five — Talos, Eleanor, Ragash, Ronan, Torren. See `docs/PLAYER_SYSTEM.md`, `docs/characters/README.md`, `docs/HERO_BIBLE.md`, `DESIGN_DECISIONS.md` #016.
- **Current session's problem statement (Companion Expertise section):** Names *Corwin* ("tracking, foraging, corruption investigation") and *Future Healer* ("medicine, community health, refugee care") *in addition to* the confirmed five. This implies a roster of seven.

**Preferred resolution options:**
1. **Add Corwin and Future Healer as canonical companions #6 and #7.** Requires new Hero Bible entries for each, Core Wound authorship, personal-quest sketches, gameplay identity sentences, and roster-count updates across ~15 files.
2. **Interpret Corwin and Future Healer as *concept placeholders* — companions the world contains but the player may or may not recruit.** Compatible with the "recruitment is not guaranteed per playthrough" rule in `DESIGN_DECISIONS.md` #7 (Combat Direction).
3. **Interpret Corwin as a rename or reidentification of an existing companion.** Would require your explicit ruling on which one.

**Awaits your approval:** pick 1, 2, or 3 (or specify differently). Until this is ruled, no docs for Corwin/Future Healer will be authored.

### 3.4 Primordial Magic attribution

**[MINOR — will auto-resolve during consolidation]**

- `elyndor/magic/MAGIC_BIBLE.md` line 11: *"Primordial Magic is the original magical force woven into creation by the Ancient God during the First Age."*
- `docs/lore/TIMELINE.md`: The First Song is sung by the *full* Divine Chorus. Primordial Magic is not a single member's creation.

**Auto-resolution:** Reword to *"woven into creation by the Divine Chorus during the Age of Awakening; later fractured by the Eighth's fall into seven elemental aspects."* Preserves both facts (the Chorus authored Primordial Magic; the Eighth's imprisonment fractured it). No lore removed.

### 3.5 "Ancient God" vs "the Forgotten Eighth" — terminology

**[MINOR — will auto-resolve during consolidation]**

Both terms are used interchangeably in developer-facing documents. The Lore Bible states the canonical developer-facing name is *the Forgotten Eighth*; *the Ancient God* is an in-world label used by characters who lack access to the truth.

**Auto-resolution:** In documents written from a *developer/writer* perspective, standardize on "the Forgotten Eighth." In *in-world* content (character dialogue, cult texts, common knowledge), the in-world label may continue. Every conversion will be logged.

### 3.6 "Great Libraries" (plural) in one file

**[MINOR — will auto-resolve during consolidation]**

`docs/world/WORLD_BIBLE.md` line 246 lists Capital Province institutions as *"…Universities, Great Libraries."* Every other reference — including the entire `docs/lore/GREAT_LIBRARY.md` — treats the Great Library as one singular institution.

**Auto-resolution:** Change to *"the Great Library."*

### 3.7 "The gods walked among mortals" — implied historical Chorus presence

**[FLAGGED — awaits your approval]**

`elyndor/history/HISTORY_BIBLE.md` line 35 states *"The gods walked among mortals directly, before their withdrawal."* The Lore Bible does not authorize any historical period of direct Chorus presence; only the Eighth is documented as having spent extended time among mortals.

**Preferred resolution:** Rephrase to make clear that the Eighth's presence was unusual and not characteristic of the full Chorus — after the Sundering the Chorus became more careful (a change in emotional posture, not a change from political intervention to non-intervention).

**Awaits your approval:** confirm this framing (or offer an alternative).

### 3.8 "Shaped the first races" — implies Chorus created mortal life

**[FLAGGED — awaits your approval]**

`elyndor/history/HISTORY_BIBLE.md` line 31 states the Eighth *"directly shaped … the first races."* The Lore Bible states the Chorus did not create mortal life.

**Preferred resolution:** Reword to describe the Eighth's influence on the *physical world* (geography, natural forces) — compatible with her role as a Chorus steward — without attributing the creation of mortal life to her.

**Awaits your approval:** confirm this reframe.

### 3.9 Difficulty philosophy — no explicit clause in any doc today

**[MINOR — will auto-resolve during consolidation]**

The problem statement establishes: *no traditional Easy/Normal/Hard; difficulty evolves through choices.* No existing document contradicts this — but no existing document *states* it either. Because it is stated by the owner in the current session, it becomes canon and needs a dedicated doc (see §2.3).

**Auto-resolution:** Create `GDD/03_Core_Gameplay/DIFFICULTY_PHILOSOPHY.md` with the owner's exact framing.

### 3.10 AI Continuation Guide missing Lore Bible references

**[MINOR — will auto-resolve during consolidation]**

`LORE_CONSISTENCY_AUDIT.md` ❌ #2 and ⚠ #6 both flag this. The Lore Bible (`docs/lore/`) does not appear in the AI Continuation Guide's priority reading list.

**Auto-resolution:** Add `docs/lore/README.md`, `docs/lore/CANON_RULES.md`, `docs/lore/DEVELOPMENT_REFERENCE.md`, `docs/lore/HISTORY_BIBLE.md`, `docs/lore/TIMELINE.md` to the top of the reading list.

### 3.11 Player state canonicality — `player.py` singleton vs `world_state["player"]`

**[FLAGGED — awaits your approval; existing project-critical known issue BUG-002]**

`DESIGN_DECISIONS.md` #007 explicitly labels this as unresolved. Not a documentation-only issue — has gameplay impact (stats can desync after combat). No new resolution proposed here; this is preserved as-is in the GDD until you rule.

### 3.12 Legacy code modules retained at root

**[FLAGGED — awaits your approval; existing project-critical known issue]**

`factions.py`, `regions.py`, `loot.py`, `memory.py` remain in the root directory alongside their `*_manager.py` successors. `DESIGN_DECISIONS.md` #009 defers deletion. No new resolution proposed here.

---

## 4. Broken References, Naming Inconsistencies, and Structural Debt

### 4.A Broken cross-references (documentation)

| Location | Issue |
|---|---|
| `docs/AI_CONTINUATION_GUIDE.md` line 38 | Describes `elyndor/history/HISTORY_BIBLE.md` using obsolete age names. |
| `docs/roadmap.md` line 105 | Same obsolete age names in the [CONFIRMED] History Bible bullet. |
| `docs/GAME_BIBLE.md` ToC entry #5 | Duplicate ordinal number: "5. Genre" and "5. Target Audience". |
| `docs/GAME_BIBLE.md` line 52 | ToC entry #42 correctly describes the new Four-Age framework — but *some* readers may still be led to the obsolete revision-log entry in the linked file. |
| `.agents/memory/lore-bible-canon.md` | Framework labeled "Seven Ages"; obsolete. |
| `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md` header + source-table | Labeled "Seven Ages"; obsolete. |
| `PROJECT_MEMORY.md` Decision #22 | Uses obsolete age names. |
| `PROJECT_MEMORY.md` decisions list | Decision numbering: 1–16 sequential, then 26 → 25 → 24 → 23 → 22 → 21 → 18 (dup) → 18 (dup) → 18 (dup) → 17 → 16 → … Non-sequential; will confuse future readers. |
| `PROJECT_STATE.md` "Highest Priority Tasks" | Numbered 1–5 then "Short term" 4–7 then "Medium term" 8–11 (duplicate 11); numbering restarts. |
| `LORE_CONSISTENCY_AUDIT.md` (root) | Own findings ❌ #1 and ❌ #3 partially outdated by the new Four-Age framework restoration, but no revision note has been added to the file. |

### 4.B Naming standardization (terminology drift)

| Term A | Term B | Term C | Canonical choice (recommended) |
|---|---|---|---|
| "The Ancient God" | "The Ancient One" | "The Forgotten Eighth" | *The Forgotten Eighth* (developer docs); *The Ancient God / The Absent One* (in-world) |
| "The Imprisonment" | "The Sundering" | — | *The Sundering* (canonical); *The Imprisonment* (acceptable as descriptive phrase in scholarly writing) |
| "Age of Creation" | "Age of Awakening" | — | *Age of Awakening* |
| "Age of Kingdoms" | "Age of Discovery" + "Age of Unity" | "Age of Harmony" | *Age of Harmony* |
| "Age of Wars" | "The Long Decline" | (final chapter of Age of Harmony) | Long Decline is *not* an age; it is the tragic final chapter of Age II |
| "Age of Shadows" | "Present Age" | "Age of Restoration" | *Age of Restoration* |
| "Steven" | "Torren" | — | *Torren* (Steven retired; retain redirect stubs) |
| "Divine Cleric" (preview.py placeholder) | — | — | Placeholder in a UI mockup; rename to a non-"Divine" role title when replaced |
| "Great Libraries" (plural, WORLD_BIBLE) | "the Great Library" | — | *the Great Library* (singular) |
| "Companion" (party member) | "Origin Character" (playable version of same companion) | "Hero" (generic) | *Companion* (party role); *Origin Character* (when spec'ing PC mode); *Hero* is the umbrella |

### 4.C Newly-introduced canon that has no home yet

**C1. Corwin (companion) — mentioned in the current problem statement but not in any doc.**
See §3.3. Needs owner ruling before authoring.

**C2. Future Healer (companion) — mentioned in the current problem statement but not in any doc.**
See §3.3. Needs owner ruling before authoring.

**C3. Origin Characters framework — mentioned as canon in the current problem statement, has no doc.**
Distinct from Custom Hero (Phase 2, deferred). Origin = every existing companion is also a playable protagonist. Rules: NPC mode = automatic evolution; PC mode = unlock roleplay choices, never force personality changes.

**C4. Companion Expertise (out-of-combat contribution matrix) — canon-fresh, no doc.**
Talos: morale, leadership, helping children. Torren: engineering, construction, repairs. Eleanor: research, arcane study, teaching. Corwin: tracking, foraging, corruption investigation. Ragash: preparing hunters, animal care, survival training. Ronan: security, patrols, settlement defense. Future Healer: medicine, community health, refugee care.

**C5. Companion Evolution (post-personal-quest permanent behavior shift) — canon-fresh, no doc.**
Examples: Ronan more socially engaged after accepting his curse; Talos grows into a mentor; Corwin more willing to trust others.

**C6. Settlement Dispersal (party disperses in safe settlements; companions occupy appropriate locations; never idle) — canon-fresh, no doc.**
Related but distinct from the Journey / Camp system which is about *travel*. Settlement Dispersal is about *hubs*.

**C7. Difficulty by Choice (no traditional Easy/Normal/Hard; difficulty evolves) — canon-fresh, no doc.**
Compatible with existing "Living World" and "player agency" language but never explicitly ruled.

**C8. Offline-First requirement (whole RPG must run offline; all critical content local; online is optional) — canon-fresh at the design-pillar level.**
Currently implied by `DESIGN_DECISIONS.md` #010 (No External Dependencies) and by the LLM mocking pattern, but not documented as a *player-experience* rule.

**C9. AI Philosophy (AI enhances, never replaces handcrafted; no critical quest, companion, or ending should require AI) — canon-fresh at this framing.**
Adjacent to `docs/lore/CANON_RULES.md` and the "Project Evolution Plan" prompt, but not consolidated.

**C10. Living World simulation direction — canon-fresh at this framing.**
The most recent authoritative prompt establishes: *"The player should never feel like they are chatting with an AI. They should feel like they are exploring a world that continues to exist whether they are present or not."* Priority order for AI narrative: (1) World State (2) Rules (3) Existing Lore (4) NPC Memory. No consolidated doc.

### 4.D Structural debt (files, not folders)

- Root-level top-level markdown files (`AI_START_HERE.md`, `PROJECT_MEMORY.md`, `PROJECT_STATE.md`, `PROJECT_CONSTITUTION.md`, `DESIGN_DECISIONS.md`, `CHANGELOG.md`, `LORE_CONSISTENCY_AUDIT.md`) sit alongside code files in `/app/`. This is legible but inconsistent with the GDD structure the owner has requested. Recommendation: **retain in place** (they are session-entry documents referenced from many places) and cross-link from the new `GDD/00_Index.md`.
- The `docs/lore/` sub-folder is technically inside `docs/` (game-specific) but its content (Chorus, Architects, First Empire, Great Library, Imperial Capital, First Temple) is universe-level and would fit better inside `elyndor/`. This is a legacy of the Lore Bible being authored in July 2026 before the two-system split hardened. Recommendation for the *GDD phase*: **leave `docs/lore/` in place** and simply link both folders into `GDD/04_World/` — the physical relocation is a bigger surgery than the consolidation phase should attempt.

---

## 5. Recommended Folder Structure for `/app/GDD/`

This structure implements the numbered sections from the problem statement and reserves slots for the missing docs identified in §2.3.

```
/app/GDD/
├── 00_Index.md                              ← master ToC + reading order
├── 00_Rationale_Log.md                      ← every consolidation change + rationale
├── 01_Foundation/
│   ├── 01_Vision.md                         ← from GAME_BIBLE §Executive Summary + Vision
│   ├── 02_Design_Pillars.md                 ← Living World, Difficulty by Choice,
│   │                                          Offline-First, AI-Optional, Origin Characters,
│   │                                          Handcrafted-First, Party as Family
│   ├── 03_Tone_and_Aesthetic.md             ← docs/game_tone.md content
│   ├── 04_Project_Constitution.md           ← link → /app/PROJECT_CONSTITUTION.md
│   ├── 05_Canon_Rules.md                    ← link → docs/lore/CANON_RULES.md
│   └── 06_Design_Decisions.md               ← link → /app/DESIGN_DECISIONS.md
├── 02_Prototype/
│   ├── 01_Current_Terminal_Prototype.md     ← what runs today (v0.4)
│   ├── 02_Godot_Prototype_Plan.md           ← NEW: what to build first in Godot
│   ├── 03_Bridging_Terminal_to_3D.md        ← systems that carry forward
│   └── 04_Prototype_Milestones.md           ← measurable milestones
├── 03_Core_Gameplay/
│   ├── 01_Core_Loop.md                      ← from GAME_BIBLE §Core Gameplay Loop
│   ├── 02_Combat_System.md                  ← link → docs/COMBAT_SYSTEM.md
│   ├── 03_Progression.md                    ← link → docs/systems/progression_skills.md
│   ├── 04_Equipment_and_Inventory.md        ← link → docs/systems/inventory_equipment.md
│   ├── 05_Economy.md                        ← link → docs/systems/factions_economy.md
│   ├── 06_Save_System.md                    ← link → docs/systems/save_system.md
│   ├── 07_Difficulty_Philosophy.md          ← NEW (see §2.3)
│   └── 08_Player_Choice.md                  ← link → docs/world/WORLD_BIBLE.md §Player Choice
├── 04_World/
│   ├── 01_World_Overview.md                 ← link → elyndor/world/world_overview.md
│   ├── 02_History.md                        ← link → docs/lore/HISTORY_BIBLE.md
│   │                                          + elyndor/history/HISTORY_BIBLE.md
│   ├── 03_Timeline.md                       ← link → docs/lore/TIMELINE.md
│   ├── 04_Regions.md                        ← link → docs/world/WORLD_BIBLE.md +
│   │                                          docs/world/GEOGRAPHY_LANDMARKS.md
│   ├── 05_Races.md                          ← link → docs/world/RACES.md
│   ├── 06_Factions.md                       ← link → docs/world/vampire_houses.md +
│   │                                          docs/world/goblin_tribes.md +
│   │                                          docs/world/covenant_inquisitors.md
│   ├── 07_Religions_and_Cults.md            ← link → docs/world/religions.md + cults.md
│   ├── 08_Divine_Chorus.md                  ← link → docs/lore/DIVINE_CHORUS.md +
│   │                                          docs/lore/DIVINE_CHORUS_PHILOSOPHY.md
│   ├── 09_Architects.md                     ← link → docs/lore/ARCHITECTS.md
│   ├── 10_Imperial_Capital.md               ← link → docs/lore/IMPERIAL_CAPITAL.md
│   ├── 11_Great_Library.md                  ← link → docs/lore/GREAT_LIBRARY.md
│   ├── 12_First_Temple.md                   ← link → docs/lore/FIRST_TEMPLE.md
│   ├── 13_First_Empire.md                   ← link → docs/lore/civilization/*
│   ├── 14_Magic_and_Elements.md             ← link → elyndor/magic/MAGIC_BIBLE.md
│   ├── 15_The_Forgotten_Eighth.md           ← link → elyndor/history/the_eighth.md
│   ├── 16_The_Corruption.md                 ← link → elyndor/history/the_corruption.md
│   ├── 17_Ancient_Legends.md                ← link → elyndor/ancient_legends/*
│   ├── 18_Living_World_Simulation.md        ← NEW (see §2.3)
│   └── 19_Pronunciation_Guide.md            ← link → docs/PRONUNCIATION_GUIDE.md
├── 05_Companions/
│   ├── 01_Hero_Bible.md                     ← link → docs/HERO_BIBLE.md
│   ├── 02_Character_Design_Guide.md         ← link → docs/CHARACTER_DESIGN_GUIDE.md
│   ├── 03_Player_System_and_Origin.md       ← link → docs/PLAYER_SYSTEM.md + NEW Origin section
│   ├── 04_Companion_Expertise.md            ← NEW (see §2.3)
│   ├── 05_Companion_Evolution.md            ← NEW (see §2.3)
│   ├── 06_Settlement_Dispersal.md           ← NEW (see §2.3)
│   ├── 07_Journey_and_Camp.md               ← link → docs/systems/journey_system.md
│   ├── heroes/
│   │   ├── TALOS.md                         ← link → docs/heroes/TALOS.md
│   │   ├── ELEANOR.md                       ← link → docs/heroes/ELEANOR.md
│   │   ├── RAGASH.md                        ← link → docs/heroes/RAGASH.md
│   │   ├── RONAN.md                         ← link → docs/heroes/RONAN.md
│   │   ├── TORREN.md                        ← link → docs/heroes/TORREN.md
│   │   ├── CORWIN.md                        ← PLACEHOLDER (owner ruling required — §3.3)
│   │   └── FUTURE_HEALER.md                 ← PLACEHOLDER (owner ruling required — §3.3)
│   └── retired/
│       └── STEVEN.md                        ← link → docs/heroes/STEVEN.md
├── 06_Story/
│   ├── 01_Main_Story.md                     ← from GAME_BIBLE §Main Story
│   ├── 02_Campaign_Design.md                ← link → docs/CAMPAIGN_DESIGN.md
│   ├── 03_Dynamic_Story_Arcs.md             ← link → docs/systems/dynamic_story_arcs.md
│   ├── 04_Quests.md                         ← link → docs/systems/quests.md +
│   │                                          docs/quests/*
│   ├── 05_Encounters.md                     ← link → docs/encounters/*
│   ├── 06_AI_Director.md                    ← link → docs/systems/ai_director.md
│   └── 07_Reputation.md                     ← link → docs/systems/reputation.md
├── 07_Systems/
│   ├── 01_Architecture.md                   ← link → docs/architecture.md
│   ├── 02_World_State.md                    ← link → docs/systems/world_state.md
│   ├── 03_Event_Bus.md                      ← link → docs/systems/event_bus.md
│   ├── 04_NPCs_and_Companions.md            ← link → docs/systems/npcs_companions.md
│   ├── 05_Combat_Implementation.md          ← link → docs/systems/combat.md
│   ├── 06_Quests_Implementation.md          ← link → docs/systems/quests.md
│   ├── 07_Regions_and_Travel.md             ← link → docs/systems/world_regions.md
│   ├── 08_Save_and_State.md                 ← link → docs/systems/save_system.md
│   ├── 09_Dialogue.md                       ← NEW (see §2.3)
│   ├── 10_Relationship.md                   ← NEW (see §2.3)
│   ├── 11_Settlement.md                     ← NEW (see §2.3)
│   ├── 12_World_Events.md                   ← NEW (see §2.3)
│   ├── 13_Campaign_Manager.md               ← NEW (see §2.3)
│   ├── 14_Corruption_System.md              ← NEW (see §2.3 — mechanical, complements the lore doc)
│   ├── 15_Coding_Standards.md               ← link → docs/coding_standards.md
│   ├── 16_Dependencies.md                   ← link → docs/dependencies.md
│   └── 17_Known_Issues_and_Debt.md          ← link → docs/known_issues.md
├── 08_AI/
│   ├── 01_AI_Philosophy.md                  ← NEW (see §2.3)
│   ├── 02_Offline_First.md                  ← NEW (see §2.3)
│   ├── 03_LLM_Bridge.md                     ← from docs/systems/ai_director.md §LLM Bridge
│   ├── 04_Dynamic_Rumors_and_Gossip.md      ← optional AI enhancement layer
│   └── 05_Campaign_Variation.md             ← optional AI enhancement layer
├── 09_Early_Access/
│   ├── 01_Roadmap.md                        ← link → docs/roadmap.md
│   ├── 02_Prototype_Readiness_Checklist.md  ← from PROJECT_STATE.md
│   ├── 03_Development_History.md            ← link → CHANGELOG.md + docs/handoffs/*
│   └── 04_Handoff_Template.md               ← link → docs/handoffs/HANDOFF_TEMPLATE.md
├── 10_Post_Launch/
│   ├── 01_Custom_Hero_Phase_2.md            ← from PLAYER_SYSTEM.md §Phase 2
│   ├── 02_Bestiary_Bible.md                 ← [FUTURE] roadmap item
│   ├── 03_Culture_Bible.md                  ← [FUTURE] roadmap item
│   ├── 04_Economy_Bible.md                  ← [FUTURE] roadmap item
│   ├── 05_Organizations_Expansion.md        ← [FUTURE] roadmap item
│   └── 06_Multi_Act_Campaign.md             ← [FUTURE] roadmap item
└── ARCHIVE_INDEX.md                          ← lists everything moved to docs/archive/ with why
```

**Source-of-truth policy:**
- Each `GDD/*` file **either** contains authored content **or** cross-links to a canonical source that remains in `docs/`, `elyndor/`, or root. **No duplication.** The GDD serves as the master index and organized reading order; the underlying documents remain the ground truth.
- Every archived file will be moved to `docs/archive/<subpath>/` and its removal noted in `ARCHIVE_INDEX.md` with: (a) why it was archived, (b) which document replaced it, (c) date archived, (d) whether unique information was preserved.

---

## 6. Recommended Implementation Order

Only start after this report is approved. Steps 1–4 are non-controversial cleanup that mostly reorganizes and cross-links. Steps 5–9 depend on your rulings in §3.

**Step 1 — Baseline + backup.** Snapshot the current `/app/docs/`, `/app/elyndor/`, and root docs into `docs/archive/pre-consolidation-2026-01/` before any edit. Move the three ZIPs into `docs/archive/snapshots/`. Add `ARCHIVE_INDEX.md`.

**Step 2 — Create `/app/GDD/` scaffold with `00_Index.md` and section READMEs.** No content moved yet. This gives a navigable frame.

**Step 3 — Fix broken references in place.** Update the *obsolete-age-name* citations in `PROJECT_MEMORY.md` (Decision #22), `docs/AI_CONTINUATION_GUIDE.md` line 38, `docs/roadmap.md` line 105, `.agents/memory/lore-bible-canon.md`, `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md`. Every change logged in `00_Rationale_Log.md`. Also fix: numbering in `PROJECT_MEMORY.md` decisions; duplicate ordinal in `docs/GAME_BIBLE.md` ToC entry 5.

**Step 4 — Populate GDD cross-references.** Each `GDD/*` file (except the *NEW* files) becomes a short link-doc pointing to the canonical source in `docs/`, `elyndor/`, or root.

**Step 5 — Author the missing docs listed in §2.3 that do not require your ruling.**
- `GDD/03_Core_Gameplay/07_Difficulty_Philosophy.md` — from the owner's statement.
- `GDD/04_World/18_Living_World_Simulation.md` — from the "Project Evolution Plan" prompt.
- `GDD/08_AI/01_AI_Philosophy.md` — from the owner's statement + existing canon.
- `GDD/08_AI/02_Offline_First.md` — from the owner's statement + `DESIGN_DECISIONS.md` #010.
- `GDD/05_Companions/06_Settlement_Dispersal.md` — from the owner's statement.
- `GDD/05_Companions/04_Companion_Expertise.md` — from the owner's statement (roster of 5 known + placeholders for Corwin + Future Healer clearly labeled ⚠ pending §3.3 ruling).
- `GDD/05_Companions/05_Companion_Evolution.md` — from the owner's statement.
- `GDD/05_Companions/03_Player_System_and_Origin.md` — extension of `docs/PLAYER_SYSTEM.md`.
- `GDD/02_Prototype/02_Godot_Prototype_Plan.md` — first-milestone plan for the Godot pass.

**Step 6 — Apply the minor auto-resolutions (§3.4, §3.5, §3.6, §3.9, §3.10).** Log each change in `00_Rationale_Log.md`.

**Step 7 — Wait for your rulings on the flagged contradictions (§3.1, §3.2, §3.3, §3.7, §3.8, §3.11, §3.12).** No action taken on these until each is approved.

**Step 8 — Author the [MISSING] system docs (§2.3):** `dialogue.md`, `relationship.md`, `settlement.md`, `world_event.md`, `campaign_manager.md`, `corruption.md`. Each is derived from reading the corresponding `.py` module — no invention.

**Step 9 — Regenerate `PROJECT_STATUS.md`** at repo root with the fields you listed (completion %, per-system %, prototype readiness checklist, missing docs, high-priority tasks, dependencies, next milestone, blockers, next-session work).

---

## 7. High-Risk Design Decisions Requiring Review

Presented in decreasing order of urgency. Every one of these blocks or shapes the Godot prototype.

**R1. Companion count — five, six, or seven?**
Corwin + Future Healer must be ruled canonical, deferred, or removed (§3.3). Every companion-facing doc, roster count, save schema, and combat balance target depends on this.

**R2. Eleanor's Harmonic Soul revelation — how is it delivered?**
Currently a canon violation (§3.2). Blocks Eleanor's personal-quest scripting for the Godot prototype.

**R3. Historical framework — confirm Version C (Four Ages: Awakening → Harmony → Sundering → Restoration) is final.**
The body content of all lore docs already reflects this. Only revision-log entries + a handful of stale references (§4.A) remain. Once confirmed, we standardize and stop revising this.

**R4. Player state canonicality (`player.py` vs `world_state["player"]`).**
DECISION-007 defers this. It has been deferred since Task 3. The prototype cannot safely add new stat sources until it is picked.

**R5. Legacy modules (`factions.py`, `regions.py`, `loot.py`, `memory.py`).**
DECISION-009 defers this. Godot port is a natural boundary at which to archive them.

**R6. Custom Hero — Phase 2 timing.**
`PLAYER_SYSTEM.md` says Phase 2. If Godot prototype scope includes a Custom Hero path, this decision changes. Recommend: **defer Custom Hero out of the prototype** (as documented).

**R7. Origin Character path parity.**
Every existing companion becoming a playable protagonist expands scope significantly. Prototype could ship with a single Origin Character (Talos is the safest choice — already-authored, canon-safe, no romance branches) and add the others incrementally.

**R8. AI enhancement scope in the Godot prototype.**
The prototype may ship with LLM calls remaining fully mocked (as the current terminal build does). Confirm this.

**R9. World Simulation persistence semantics.**
The "Project Evolution Plan" prompt says the world should feel like it continues to exist whether the player is present or not. That implies simulation ticks during travel *and* during time skips. Confirm the desired granularity (daily tick? hourly? event-driven?) before we scope the AI-Director rework.

**R10. Godot prototype's first playable slice.**
Recommend: a single settlement + one region + one companion (Talos) + one combat encounter + one dialogue scene + save/load. This scopes the port narrowly enough to validate the architecture without over-investing.

---

## 8. Overall Documentation Health Assessment

**Strengths (unusually strong for this stage of a project):**
- The Lore Bible (`docs/lore/`) is a masterclass in canon governance: `CANON_RULES.md`, `DIVINE_CHORUS.md`, and `ARCHITECTS.md` set immutable design principles that every downstream document *actually respects*.
- The Hero Bibles for the five confirmed companions are complete, philosophically consistent, and internally cross-referenced.
- The world material (regions, races, religions, cults, vampire houses, goblin tribes) is comprehensive.
- The governance layer (`PROJECT_CONSTITUTION.md`, `AI_START_HERE.md`, `DESIGN_DECISIONS.md`, `docs/handoffs/`) is exceptional — sessions across contributors are actually preserved.
- The prior `LORE_CONSISTENCY_AUDIT.md` is itself a valuable artifact — it demonstrates the project already has a rigorous internal-audit culture.

**Weaknesses (all fixable in the consolidation phase):**
- **Fragmentation.** Four parallel documentation systems (root / `docs/` / `docs/lore/` / `elyndor/`) with overlapping authority. New readers do not know where to start; the current entry points (`AI_START_HERE.md` → `PROJECT_MEMORY.md` → `docs/GAME_BIBLE.md` → `docs/lore/README.md`) work but require ~30 minutes before a contributor understands the map.
- **Canon churn debris.** Framework revisions (Four Ages → Seven Ages → new Four Ages) left behind ~7 stale references + one entire outdated summary file (`docs/lore/world/WORLD_FOUNDATION_SUMMARY.md`) + one outdated audit report (`LORE_CONSISTENCY_AUDIT.md`). None of this affects the *content* of the current canon; it affects readability.
- **New canon from the current session has no home.** Living World, Difficulty by Choice, Offline-First, AI-Optional, Origin Characters, Companion Expertise, Companion Evolution, Settlement Dispersal — these are all *stated* in the problem statement but not yet in *documents*.
- **Missing system docs for code that exists.** Dialogue, relationship, settlement, world-event, campaign-manager, and (mechanical) corruption systems all have code but no dedicated system docs.
- **Structural debt at code level** (dual player state, legacy modules, dual save systems) is well-documented but persistent. Should be resolved at the Godot boundary.

**Overall grade:** 🟡 **B+ / Ready for consolidation.** Once the fragmentation is resolved and the flagged contradictions are ruled, this project has a substantially better documentation foundation than most projects that have shipped a prototype.

**Godot prototype readiness (as of this audit):**
- Foundation Systems documentation: 90% (main gap: Origin Characters, difficulty philosophy, offline-first, AI philosophy).
- Prototype Systems documentation: 40% (main gap: Godot Prototype Plan, migration-from-terminal doc).
- Core Gameplay documentation: 85% (main gap: mechanical corruption doc, difficulty philosophy).
- World documentation: 95% (main gap: living-world simulation framing consolidated in one place).
- Companion documentation: 75% (main gap: Origin, Expertise, Evolution, Settlement Dispersal; +Corwin/Future Healer pending).
- Story & Quest documentation: 80% (main gap: full quest content still sparse, but that is a content task not a doc task).
- Polish & Early Access documentation: 60% (main gap: prototype readiness checklist, real handoff cadence).
- Post-Launch documentation: 20% (fine — this is intentional; nothing here should be over-designed).

---

## 9. What Happens Next

**This report ends the audit-only pass.** No files have been modified.

**Action required from you:**

1. **Confirm the folder structure in §5** (or specify changes).
2. **Rule on the flagged contradictions in §3:**
   - §3.1 Historical framework (Version C is Four Ages — confirm)
   - §3.2 Eleanor's Harmonic Soul revelation (pick delivery mechanism)
   - §3.3 Companion roster (five / seven / other)
   - §3.7 "Gods walked among mortals" reframe (approve)
   - §3.8 "Shaped the first races" reframe (approve)
   - §3.11 Player state canonicality (pick canonical source or defer explicitly)
   - §3.12 Legacy modules (archive at Godot boundary or now)
3. **Confirm the high-risk decisions in §7** (R1–R10) or specify how to proceed.
4. **Approve the implementation order in §6.**

Once approved, consolidation will proceed in the order given, with every automatic resolution and every manual edit logged in `GDD/00_Rationale_Log.md`.

---

## Appendix A — Files Read for This Audit

**Root-level (9):** `README.md`, `AI_START_HERE.md`, `PROJECT_CONSTITUTION.md`, `PROJECT_MEMORY.md`, `PROJECT_STATE.md`, `DESIGN_DECISIONS.md`, `CHANGELOG.md`, `architecture.md`, `LORE_CONSISTENCY_AUDIT.md`.

**`docs/` core (13):** Every file listed in §1.2 core section.

**`docs/systems/` (14):** All system deep-dives.

**`docs/characters/` (8), `docs/heroes/` (7), `docs/world/` (7):** All files, both retired and active.

**`docs/quests/` (2), `docs/encounters/` (2):** All authored content.

**`docs/lore/` (11) + `docs/lore/civilization/` (5) + `docs/lore/world/` (1):** All Lore Bible files.

**`docs/handoffs/` (3):** All handoff records.

**`elyndor/` (14):** Every file under README + world + ancient_legends + bestiary + history + magic + organizations.

**`.agents/memory/` (3):** `MEMORY.md`, `integration-pass.md`, `lore-bible-canon.md`.

**`attached_assets/`:** All 44 pasted-prompt files were catalogued; the three most recent (by timestamp) were read in full to identify the current canon layer.

**ZIP archives:** All three extracted and compared with `diff -rq` against `/app`; verified as older snapshots with no unique content.

## Appendix B — Rationale for Every Auto-Resolution Proposed

Each entry below explains why an auto-resolution (§3.4, §3.5, §3.6, §3.9, §3.10) is safe.

- **§3.4** (Primordial Magic attribution) — Reword only. No lore removed. Both facts (Chorus authored Primordial Magic; Eighth's imprisonment fractured it) preserved. Rationale: aligns `MAGIC_BIBLE.md` line 11 with the Lore Bible's foundational claim that the *full* Chorus performed the First Song.
- **§3.5** (Ancient God vs Forgotten Eighth terminology) — Distinguish developer-facing vs in-world contexts. Rationale: the Lore Bible already codified this dual usage; some earlier docs simply predate the rule.
- **§3.6** (Great Libraries vs the Great Library) — Cosmetic singular correction. Rationale: `docs/lore/GREAT_LIBRARY.md` unambiguously establishes one Library.
- **§3.9** (Difficulty philosophy) — New doc created from the owner's exact framing in the current problem statement. Rationale: no existing document contradicts this; owner explicitly states it.
- **§3.10** (AI Continuation Guide missing Lore Bible references) — Additive change to a table. Rationale: `LORE_CONSISTENCY_AUDIT.md` already flagged this as ❌ #2 and ⚠ #6.

---

---

# Part II — Vertical Slice Readiness Assessment

> **Purpose:** Determine whether this project is ready to begin a **Vertical Slice** — a small but *complete-feeling* playable segment that demonstrates the target experience end-to-end (one region + one settlement + one dungeon + one questline + one companion recruit + one companion quest + one boss + one loop).
>
> **Method:** Every system and content area is scored against three criteria:
> - **Design (Doc):** is the system canonically documented?
> - **Prototype (Code):** does a functional terminal-prototype implementation exist?
> - **Godot-ready:** is there enough information to reimplement in Godot without inventing new canon?
>
> **Verdict format:** ✅ Ready · 🟡 Partial · ❌ Missing.

---

## VS-1. Core Gameplay System Readiness

| System | Design (Doc) | Prototype (Code) | Godot-Ready | Notes / Gaps |
|---|---|---|---|---|
| **Exploration** | ✅ Two-layer model documented (strategic continent map + handcrafted regions) — `docs/world/WORLD_BIBLE.md`, `docs/systems/world_regions.md` | 🟡 Region travel + `world_map.py` static display + `travel_manager.py` inter-region movement all present; no strategic-continent-map layer | 🟡 | Godot scene layout for the two-layer exploration is undefined. Dual region-discovery state is a known bug (BUG-004). |
| **Combat** | ✅ Canonical `docs/COMBAT_SYSTEM.md` (grid, AP economy, facing, downed, shield stance, initiative, party of four) | 🟡 Terminal turn-based combat is functional (`combat.py`, `enemy_manager.py`, `bosses.py`, `status_effects.py`) but is a *placeholder* — no grid, no AP, no facing, no downed system | ❌ | The target combat system (3D tactical grid) has **zero** implementation yet. The terminal loop is not a stepping stone — it will be rewritten in Godot. Complete design however means no invention needed. |
| **Dialogue** | 🟡 `dialogue_manager.py` + skill checks + rumor generation covered in `docs/GAME_BIBLE.md` and `docs/systems/npcs_companions.md`. **No dedicated `docs/systems/dialogue.md`.** | ✅ Terminal dialogue with persuasion/intimidation checks working | 🟡 | Dialogue framework doc for Godot (branching format, condition system, LLM-optional layer) is missing. |
| **Companion System** | ✅ Hero Bibles complete for all five confirmed companions; `docs/HERO_BIBLE.md`, `docs/CHARACTER_DESIGN_GUIDE.md`, `docs/systems/npcs_companions.md`, `docs/systems/journey_system.md` | 🟡 `companion_manager.py` supports recruit/remove/loyalty/attack/ability; recruitment *conditions* per companion are not scripted; abilities are placeholder | 🟡 | Companion Expertise, Companion Evolution, Origin Character, and Settlement Dispersal are new canon with no docs (§2.3). Also blocks a decision on the roster (Corwin + Future Healer). |
| **Progression** | ✅ Level 25 cap, shared XP across roster, new-companion auto-scaling documented in `docs/systems/progression_skills.md` | 🟡 XP and level counter working; per-level stat growth not applied; skill tree scaffold not wired to combat | 🟡 | Level-up stat curves per class (Talos/Eleanor/Ragash/Ronan/Torren) are undefined. Skill trees per companion (Torren has three named paths: Forge Master, Engineer, War Smith) are named but not filled with individual skill nodes. |
| **Inventory** | ✅ Canonical path (`world_state["player"]["inventory"]`) documented in `docs/systems/inventory_equipment.md` | ✅ Functional (add/remove/has_item helpers) | ✅ | Ready as-is; port to Godot is straightforward. |
| **Equipment** | ✅ Slots (weapon, armor, accessory) and stat application documented | ✅ Functional | ✅ | Ready. |
| **Crafting** | ❌ ⚠ **NOT YET DEFINED** anywhere in the repo. `docs/roadmap.md` [FUTURE] entry only. Torren is thematically tied to crafting but there is no recipe database, no component-gathering system, no crafted-item catalog. | ❌ | ❌ | This is the largest single gap that could block the Torren companion quest if it depends on crafting mechanics. |
| **Saving/Loading** | ✅ Both save systems + migration guard documented in `docs/systems/save_system.md` | ✅ Both functional; `ensure_world_state_defaults()` in place | 🟡 | Godot port will not use JSON+manager-dicts as-is — the save schema must be redefined against the new `world_state` shape, but the *strategy* is documented. |

**Core Gameplay overall:** 🟡 **Design is 90% ready. Implementation is terminal-only.** The Godot Vertical Slice will build fresh code against the existing canon — no design invention needed except for crafting and skill-tree fill.

---

## VS-2. Vertical Slice Content Requirements

Concrete assessment of the eight required VS deliverables against current documentation and content.

### VS-2.1 One complete playable region

**Status: 🟡 Design ready; Godot scene definition missing.**

| Requirement | Status |
|---|---|
| Region designed? | ✅ Six canonical regions exist (`docs/world/WORLD_BIBLE.md`). **The Frontier** is the strongest candidate for VS-1 — the Corruption arrives there first, the goblin tribes are located there, and the region has the most authored content (`docs/quests/goblin_tribe_quests.md`, `docs/encounters/mossroot_first_contact.md`). |
| Biome + danger + factions specified? | ✅ Every region has biome, danger level, faction control. |
| Explorable content authored? | 🟡 Frontier has one first-contact encounter authored + three tribe questlines. Not enough content for a *full* region — needs 3–5 more location vignettes. |
| Scene layout / map / traversal? | ❌ No Godot scene layout, no map graph, no traversal grid or nav mesh definition. |
| Environmental storytelling beats? | 🟡 `docs/world/GEOGRAPHY_LANDMARKS.md` lists named landmarks; specific in-region storytelling beats not yet authored. |

**Recommendation:** Ship VS-1 with **The Frontier** as the playable region. Design gap = Godot scene/map layout only.

### VS-2.2 One settlement

**Status: 🟡 Data exists; playable settlement scene undefined.**

| Requirement | Status |
|---|---|
| Settlement data model? | ✅ `settlement_manager.py` has 12+ functions (prosperity, security, events, rumors, services). Serialized via save_manager. |
| Named settlement content? | 🟡 Terminal prototype includes multiple settlements as data; none has an *authored* location doc (people, buildings, quest hooks, environmental beats). |
| Settlement Dispersal spec? | ❌ New canon from current session. See §2.3 and §4.C6. |
| Godot scene? | ❌ Undefined. |

**Recommendation:** Author one full settlement (recommend: **a Frontier trading post/outpost** — thematically the ideal VS-1 hub). Includes NPC roster, dispersal layout for the five companions, service buildings, one merchant, at least one quest hook.

### VS-2.3 One dungeon

**Status: ❌ Dungeon design not authored; code stub only.**

| Requirement | Status |
|---|---|
| Dungeon system design doc? | ❌ Missing (`docs/roadmap.md` #8 is the only reference). |
| Dungeon data model? | 🟡 `dungeon_manager.py` has only `run_dungeon(dungeon_id)` — no floor/room/trap/loot-table sub-systems. |
| Authored dungeon content? | ❌ Zero authored dungeons in the repo. |
| Dungeon layout / architecture? | ❌ No canonical dungeon-layout system. |

**Recommendation:** Author **one small dungeon (3–5 rooms)** tied to the Frontier questline (e.g., a corrupted watchtower or a Mossroot-territory ruin). Design gap is real here: dungeon-layout system needs a short design doc before authoring content.

### VS-2.4 One major questline

**Status: ✅ Fully authored; ready to script.**

Three complete questlines authored:
- `docs/quests/goblin_tribe_quests.md`: **The Debt Comes Due** (Stonefang, 5 stages), **What the Forest Carries** (Mossroot, 5 stages), **Smoke and Terms** (Ashfire, 5 stages).
- `docs/quests/religious_order_quests.md`: four authored quests (Inquisitor's Commission, Turning Grove, What the Ancestors Say, Archivist's Last Record).
- `docs/systems/dynamic_story_arcs.md`: **The Fractured Circle** (Eleanor's arc + Mages Guild corruption).

**Recommendation:** Ship VS-1 with **What the Forest Carries** (Mossroot) — this quest already has a first-contact encounter authored (`docs/encounters/mossroot_first_contact.md`) and matches the Frontier setting.

### VS-2.5 One companion recruitment

**Status: 🟡 Companion is documented; recruitment scene is not.**

Every one of the five confirmed companions is fully authored (Hero Bible + Character Sheet). Recruitment mechanics exist in code (`recruit_companion()`). What is missing:
- The *narrative recruitment scenes* per companion — when, where, why the player first meets them, and what conditions unlock their recruitment.
- The Torren Hero Bible refers to introductory scenes conceptually; no authored recruitment dialogue exists yet.

**Recommendation:** Author **Talos's recruitment scene** for VS-1. Talos is the safest choice: earliest in the tone canon (mentor archetype), lowest romance/narrative risk, easiest to test.

### VS-2.6 One companion quest

**Status: ✅ Two authored, ready.**

- **Eleanor's personal story** (The Fractured Circle) — fully authored in `docs/systems/dynamic_story_arcs.md` lines 116–170.
- **Ronan's Hidden Pack** — key story beat authored in `docs/heroes/RONAN.md` Personal Quest section.
- **Torren's Core Wound arc** — outlined but full quest not yet authored.

**Recommendation:** Author **Eleanor's Fractured Circle arc** (already the most-developed) *or* pick a smaller companion quest suitable for VS-1 (recommend an earlier beat from Talos's arc since he's the recommended VS-1 recruit).

### VS-2.7 One boss encounter

**Status: 🟡 Boss system + several bosses in code; VS-1 boss not authored in canonical detail.**

`bosses.py` has boss phase logic; `enemy_manager.py` has boss_phase_check. `docs/systems/combat.md` documents boss combat structure. Zero *named* bosses have been designed with narrative, mechanical, and thematic canon (name, backstory, phase transitions, dialogue, arena, defeat consequences).

**Recommendation:** Design **one named Frontier boss** tied to the Mossroot questline (candidate: a Corruption-tainted alpha of the "hollow game" already referenced in `docs/world/goblin_tribes.md`). Needs a 1-page design doc.

### VS-2.8 One fully playable gameplay loop

**Status: 🟡 Terminal loop is complete; Godot loop requires all above + integration.**

The terminal prototype demonstrates the full loop today: enter region → travel → explore → encounter → combat → loot → progression → quest update → save. This *proves the design is loop-complete*.

**Recommendation:** VS-1 loop = **arrive at Frontier trading post → meet Talos → recruit Talos → accept Mossroot questline → travel to Mossroot territory → resolve first-contact encounter → explore a small corrupted ruin (dungeon) → boss fight → return to settlement → save/load → progress to next stage of quest.**

---

## VS-3. Technical Readiness

### VS-3.1 Documentation availability by technical area

| Area | Doc Present | Godot-Ready | Gap |
|---|---|---|---|
| **Scene Architecture** | ❌ | ❌ | No Godot scene tree design. No definition of scene granularity (per-region? per-settlement? per-encounter?). No scene transition rules. |
| **Save System** | ✅ `docs/systems/save_system.md` + `world_state.py` migration guard | 🟡 | Strategy documented; Godot-side schema (Resource? JSON? Custom?) undefined. |
| **Data Structures** | 🟡 `docs/systems/world_state.md` documents the 11 world_state sections. Companion, quest, region, enemy, item schemas exist as terminal-prototype dicts. | 🟡 | Godot equivalents (Resources, GDScript classes) undefined. No canonical mapping table from `world_state` sections to Godot resources. |
| **Quest Framework** | ✅ `docs/systems/quests.md` + `docs/systems/dynamic_story_arcs.md` | 🟡 | Terminal quest DB structure ready; Godot quest-runner (node? Resource?) undefined. Branching quest state graph undefined. |
| **Dialogue Framework** | 🟡 Scattered across `docs/systems/npcs_companions.md` + `docs/systems/journey_system.md` | ❌ | No dedicated framework doc. Godot dialogue engine (Dialogic? custom?) and format not chosen. |
| **Combat Framework** | ✅ `docs/COMBAT_SYSTEM.md` (canonical target) + `docs/systems/combat.md` (terminal impl) | 🟡 | Grid resolution, action-point costs per skill, and skill-list-per-companion undefined at the numeric level. Turn order handling in Godot undefined. |
| **AI Framework** | 🟡 `docs/systems/ai_director.md` + `dm_brain.py` + `llm_bridge.py` | 🟡 | DM Brain pacing works. LLM integration is mocked. Offline-First and AI Philosophy docs missing (§2.3). No decision on which LLM (or none) for VS-1. |
| **UI Framework** | ❌ | ❌ | Terminal is text I/O. `ui_mockup/index.html` and `preview.py` exist as a *separate* Flask prototype — not the target UI. Godot UI framework (Control nodes, theme, HUD hierarchy) undefined. |
| **Animation Pipeline** | ❌ | ❌ | ⚠ NOT YET DEFINED — no doc, no assets, no rig standard. |
| **Audio Pipeline** | ❌ | ❌ | ⚠ NOT YET DEFINED — no doc, no assets. |

### VS-3.2 Missing implementation documentation

Ranked by priority for VS-1 start:

**Critical (blocks Godot prototype start):**
- `GDD/02_Prototype/01_Godot_Scene_Architecture.md` — how the target project is organized (main scene, region scene, combat scene, dialogue overlay, UI overlay).
- `GDD/02_Prototype/02_Godot_Data_Model.md` — mapping from `world_state` sections to Godot Resources / autoload singletons.
- `GDD/02_Prototype/03_Save_Schema_for_Godot.md` — how the JSON save format is loaded into Godot Resources.
- `GDD/07_Systems/09_Dialogue.md` — dedicated dialogue framework spec (branching, conditions, LLM-optional layer).
- `GDD/07_Systems/14_Corruption_System.md` — mechanical spec (currently only lore-side).

**Important (needed before VS-1 completion):**
- `GDD/07_Systems/11_Settlement.md` — companion dispersal, service nodes, rumor generation format.
- `GDD/07_Systems/12_World_Events.md` — event triggers, tick cadence, world_state effects.
- `GDD/07_Systems/13_Campaign_Manager.md` — act progression, arc selection.
- `GDD/07_Systems/10_Relationship.md` — social-state + npc-relationship dual system.
- `GDD/03_Core_Gameplay/09_Dungeon_System.md` — floor/room/trap/loot subsystem.
- Numeric balance tables — per-class level-up stat curves, per-skill AP costs, per-enemy stat block templates.

**Optional (can lean on placeholder decisions initially):**
- UI theme and HUD hierarchy — a placeholder theme can carry VS-1.
- Animation state machine spec — placeholder animations acceptable in VS-1.
- Full audio pipeline — placeholder audio acceptable in VS-1.

---

## VS-4. Art Requirements — Placeholder Asset Plan

**Guiding principle:** Vertical Slice validates the *loop and feel*, not final visual fidelity. Every asset below can be a placeholder unless explicitly noted.

### VS-4.1 Characters

| Companion | VS-1 Asset Need | Placeholder Recommendation |
|---|---|---|
| Talos | 3D model + idle + walk + attack (sword) + hit-react + one dialogue portrait | **Kenney Adventurers Pack** or a Mixamo-rigged free asset. Portrait: AI-generated or commissioned. |
| Eleanor | (Not in VS-1 — deferred) | Skip for VS-1. |
| Ragash | (Not in VS-1) | Skip. |
| Ronan | (Not in VS-1) | Skip. |
| Torren | (Not in VS-1) | Skip. |
| Player (Origin: Talos) | Shares Talos rig with alternate outfit or none | Same asset as Talos, distinct highlight/marker. |

### VS-4.2 Enemies

| Enemy type | VS-1 Need | Placeholder |
|---|---|---|
| Goblin (Mossroot) — 2 variants | Non-hostile in first-contact then hostile in dungeon | Kenney goblin pack or Mixamo. |
| Corrupted wildlife ("hollow game") | 1 variant | Recolored wolf/wildlife rig. |
| VS-1 Boss (Corruption-tainted alpha) | 1 unique model | Larger recolored wolf with particle effect for corruption. |

### VS-4.3 Environment

| Location | VS-1 Need | Placeholder |
|---|---|---|
| Frontier trading post (settlement) | 1 hub scene with buildings, NPC spawn points, dispersal spots | Kenney low-poly medieval pack. |
| Overworld (region layer) | 1 explorable area with paths, terrain, encounter zones | Godot terrain with Kenney nature pack. |
| Small corrupted ruin (dungeon) | 3–5 rooms with lighting for corruption effect | Kenney dungeon pack + emissive/glow shader. |

### VS-4.4 UI

| Element | VS-1 Need | Placeholder |
|---|---|---|
| Main menu | Start / Load / Quit | Godot default theme + custom title. |
| HUD (health / party / minimap) | Basic overlay | Rectangle-and-text placeholders. |
| Dialogue overlay | Portrait + text + choices | Godot Panel + RichTextLabel. |
| Inventory panel | Grid + tooltip | Godot GridContainer + Kenney UI icons. |
| Combat UI (AP tracker, initiative order, action buttons) | Turn readable | Godot buttons + custom icons. |

### VS-4.5 Icons

| Category | VS-1 Need | Placeholder |
|---|---|---|
| Item icons (weapons, armor, potions) | ~20 icons | Kenney RPG icons pack (free CC0). |
| Skill/ability icons | ~10 icons | Kenney or Game-icons.net (CC BY 3.0). |
| Faction/reputation icons | ~5 icons | Custom simple SVG. |
| Status effect icons | ~6 icons | Kenney or custom. |

### VS-4.6 Animations

| Type | VS-1 Need | Placeholder |
|---|---|---|
| Character base (idle/walk/run/attack/hit/death) | 6 clips per rig | Mixamo (free) — retargeted to placeholder rigs. |
| Combat feedback (block, dodge, downed) | 3 clips | Mixamo or hand-authored. |
| UI transitions | Fade, slide, pop | Godot Tween — no assets needed. |

### VS-4.7 Sound

| Type | VS-1 Need | Placeholder |
|---|---|---|
| Footsteps (grass/stone/wood) | 3 variants | freesound.org CC0. |
| Combat SFX (sword swing, hit, block, dodge, downed) | ~8 clips | Kenney audio pack (CC0). |
| UI SFX (button, dialogue tick, menu open/close) | ~5 clips | Kenney audio pack. |
| Ambient (forest, settlement, dungeon) | 3 loops | freesound.org CC0. |

### VS-4.8 Music

| Track | VS-1 Need | Placeholder |
|---|---|---|
| Settlement ambient | 1 loop (~2 min) | AI-generated (Suno/Udio) *or* royalty-free (Kevin MacLeod / free-stock-music). |
| Exploration | 1 loop | Royalty-free. |
| Combat | 1 loop | Royalty-free. |
| Boss | 1 loop | Royalty-free. |
| Main menu | 1 loop | Royalty-free. |

### VS-4.9 VFX

| Effect | VS-1 Need | Placeholder |
|---|---|---|
| Corruption glow | Emissive particle system | GPUParticles3D + shader. |
| Attack impact / hit flash | Simple particle burst | GPUParticles3D. |
| Dialogue-hint highlight | Ring / arrow | Simple mesh + tween. |
| Boss transition | Camera shake + fade | Godot camera + tween. |
| Save/load indicator | UI-only | Godot Tween. |

**Summary:** Every art requirement for VS-1 can be met with **free/CC0 asset packs (Kenney, Mixamo, freesound.org) + Godot-native shaders/particles + one commissioned or AI-generated dialogue portrait for Talos**. No custom-3D-modeling pipeline is required for VS-1.

---

## VS-5. Missing Design Documentation — Ranked

**Critical (blocks VS-1 start):**
- **Godot Scene Architecture** — how the project is organized in Godot.
- **Godot Data Model** — `world_state` → Resources / autoload mapping.
- **Save Schema for Godot** — how JSON save loads into Godot resources.
- **Dialogue Framework** — dedicated system doc; branching + conditions + optional-AI layer.
- **Difficulty Philosophy** — the "no Easy/Normal/Hard" rule the owner just canonized (§2.3).
- **Offline-First** — the fundamental design pillar the owner just canonized (§2.3).
- **AI Philosophy** — which optional AI enhancements are allowed, and where they are prohibited (§2.3).
- **Living World Simulation** — priority order for world-state → rules → lore → NPC memory (§2.3).
- **Origin Character** — NPC vs PC mode rules (§2.3).
- **Companion Expertise** — out-of-combat contribution matrix per companion (§2.3).
- **Companion Evolution** — post-personal-quest permanent behavior changes (§2.3).
- **Settlement Dispersal** — companion appears somewhere appropriate in the hub (§2.3).
- **Corruption Mechanical System** — how Corruption is tracked/propagated/expressed in gameplay (lore side exists; mechanical side does not).
- **Ruling on the flagged contradictions (§3, §7)** — historical framework, Eleanor's revelation, companion roster (Corwin/Future Healer), player-state canonicality.

**Important (blocks VS-1 completion but not start):**
- **Dungeon System** — floor/room/trap/loot subsystem design.
- **Settlement System** — service nodes, NPC spawn logic, rumor generation format.
- **Relationship System** — dual social-state + npc-relationship spec unified.
- **World Events System** — tick cadence, triggers, world_state effects.
- **Campaign Manager** — act progression, arc selection.
- **Numeric Balance Tables** — per-class level curves, AP costs, enemy stat blocks.
- **VS-1 Settlement authored** — Frontier trading post: buildings, NPCs, dispersal points, quest hooks.
- **VS-1 Dungeon authored** — 3–5 rooms tied to Mossroot questline.
- **VS-1 Boss authored** — Corruption-tainted alpha with name, backstory, phase transitions.
- **VS-1 Recruitment scene authored** — Talos's first-meeting sequence.
- **Godot Prototype Plan** — scope and milestone plan for the VS-1 build.

**Optional (can be added after VS-1):**
- Bestiary Bible.
- Culture Bible (especially Halflings + Gnomes still ⚠ NOT YET DEFINED).
- Economy Bible.
- Organizations expansion.
- Multi-act campaign scripting.
- Crafting system (**unless** VS-1 depends on Torren; Talos is recommended precisely to avoid this).
- Full UI theme and HUD polish.
- Full animation state machine.
- Full audio pipeline and adaptive music mixer.

---

## VS-6. Development Risks

Ranked by severity.

**RISK-1 — Undefined Godot scene architecture (Critical).**
No document exists describing how the target project is organized in Godot. Every implementation decision from day one is currently a guess. **Mitigation:** author `GDD/02_Prototype/01_Godot_Scene_Architecture.md` before any Godot code.

**RISK-2 — Combat is a green-field rewrite (Critical).**
The canonical grid+AP+facing+downed system has no implementation anywhere. The terminal loop is not a stepping stone. This is the single largest engineering investment for VS-1. **Mitigation:** write a small combat-only Godot spike (single tile, single hero, single enemy) before committing to the full VS-1 scope.

**RISK-3 — Companion roster still unresolved (High).**
Corwin and Future Healer canon-status blocks VS-1 companion-related decisions. If Corwin becomes canonical, expertise/evolution docs need a sixth entry each and combat balance shifts. **Mitigation:** rule §3.3 before VS-1 begins.

**RISK-4 — Difficulty and AI philosophy not documented (High).**
The owner has re-stated these as canon in the current session. Any Godot-side design decision made before those documents are authored risks contradicting the newly-canonized philosophies. **Mitigation:** author the Critical docs in §VS-5 before Godot work starts.

**RISK-5 — Dialogue framework choice pending (High).**
Godot has multiple dialogue plugins (Dialogic, custom) and mixing them is expensive. Deciding late will require re-authoring content. **Mitigation:** pick a dialogue tool in the Godot Prototype Plan doc.

**RISK-6 — Crafting undefined (Medium; only relevant if Torren is in VS-1).**
Torren is the fifth companion whose thematic identity is *restoration/crafting*. Any Torren VS-1 slice depends on crafting mechanics that do not exist yet. **Mitigation:** VS-1 uses Talos (recommended), which does not require crafting. Defer Torren-related content to VS-2 or later.

**RISK-7 — Player-state divergence (Medium).**
`player.py` vs `world_state["player"]` is unresolved (BUG-002, DECISION-007). Any new Godot implementation must pick one path. **Mitigation:** rule §3.11 before Godot save-schema is authored.

**RISK-8 — Living World simulation cadence undefined (Medium).**
The "world continues without the player" pillar needs a tick cadence and event-trigger model. Building the AI Director in Godot without these decisions produces the wrong pacing. **Mitigation:** rule §7 R9 (World Simulation persistence semantics) in the same session as Difficulty/Offline-First/AI-Philosophy docs.

**RISK-9 — Scope creep from Origin Characters (Medium).**
"Every companion is also a playable protagonist" is a permanent design pillar but a scope multiplier. **Mitigation:** VS-1 ships with **one** Origin (Talos). All authored content assumes Talos-POV. Other Origins are Phase-2 (not VS-1).

**RISK-10 — Terminal engine may distract from Godot investment (Medium).**
The terminal prototype is 90%+ complete on many systems. It may be tempting to add features to the terminal instead of committing to the Godot rewrite. **Mitigation:** Freeze the terminal engine at v0.4. Every new feature goes to Godot.

**RISK-11 — Documentation churn resurgence (Low).**
The Four→Seven→Four Ages history and Steven→Torren migration show canon has been rewritten mid-project. If it happens again during VS-1 (e.g., a companion is retired), work is invalidated. **Mitigation:** the Constitution's escalation clauses (Article VI, VII) already cover this — enforce them.

**RISK-12 — Legacy code modules (Low).**
`factions.py`, `regions.py`, `loot.py`, `memory.py` do not affect Godot but pollute the reference. **Mitigation:** at Godot boundary, do not port them; archive them under `docs/archive/legacy/`.

---

## VS-7. Recommended Next Steps — Roadmap to Vertical Slice

This roadmap covers **only** the work required to reach a playable VS-1 in Godot. Nothing extra.

### Phase 1 — Immediate Work Required (blocks VS-1 kick-off)

Estimated: 1–2 weeks of design work, no Godot code yet.

**P1.1 — Consolidation approval.**
Owner reviews CONSOLIDATION_REPORT.md and rules on §3, §7. Consolidation proceeds per §6.

**P1.2 — Canon-fresh docs (author the ten identified in §2.3 that don't need rulings):**
- `GDD/03_Core_Gameplay/07_Difficulty_Philosophy.md`
- `GDD/04_World/18_Living_World_Simulation.md`
- `GDD/08_AI/01_AI_Philosophy.md`
- `GDD/08_AI/02_Offline_First.md`
- `GDD/05_Companions/03_Player_System_and_Origin.md`
- `GDD/05_Companions/04_Companion_Expertise.md`
- `GDD/05_Companions/05_Companion_Evolution.md`
- `GDD/05_Companions/06_Settlement_Dispersal.md`

**P1.3 — Ruling-dependent docs (author after §3 / §7 rulings):**
- Companion roster resolution (Corwin, Future Healer).
- Eleanor's Harmonic Soul delivery mechanism.
- Player-state canonicality.
- Historical-framework final confirmation + stale-reference cleanup.

**P1.4 — Godot pre-flight (Critical missing implementation docs):**
- `GDD/02_Prototype/01_Godot_Scene_Architecture.md`
- `GDD/02_Prototype/02_Godot_Data_Model.md`
- `GDD/02_Prototype/03_Save_Schema_for_Godot.md`
- `GDD/07_Systems/09_Dialogue.md`
- `GDD/07_Systems/14_Corruption_System.md`

**Exit criteria for Phase 1:** All Critical docs in §VS-5 exist; all §3 rulings received; Godot Prototype Plan finalized.

### Phase 2 — Prototype-Ready Work (VS-1 kick-off)

Estimated: 3–6 weeks. First Godot code lands.

**P2.1 — Godot project scaffolding.** Init the project; import the placeholder asset packs listed in §VS-4; set up the scene tree per `GDD/02_Prototype/01_Godot_Scene_Architecture.md`.

**P2.2 — Data-model port.** Implement world_state as Godot autoload; port the 11 sections; port the save/load system per `GDD/02_Prototype/03_Save_Schema_for_Godot.md`.

**P2.3 — Combat spike.** Single-hero, single-enemy, single-tile combat with movement points and one action point. **This spike alone tests RISK-2.**

**P2.4 — Dialogue spike.** Load one branching conversation with skill-check nodes.

**P2.5 — VS-1 content authoring (parallel):**
- Frontier trading post (settlement) design doc.
- Small corrupted ruin (dungeon) design doc.
- Talos's recruitment scene authored.
- VS-1 boss (Corruption-tainted alpha) design doc.
- Mossroot questline scripted format.

**Exit criteria for Phase 2:** Godot project builds and runs an empty scene; combat spike is playable; dialogue spike is playable; VS-1 content docs are complete.

### Phase 3 — Vertical Slice Completion

Estimated: 6–10 weeks. VS-1 becomes playable end-to-end.

**P3.1 — Frontier region playable.** Overworld scene loads; player traverses; encounter zones function.

**P3.2 — Trading-post settlement playable.** Player enters hub; companion dispersal system spawns Talos in appropriate location; Talos is recruitable; other NPCs interact.

**P3.3 — Mossroot questline scripted.** Quest triggers, stages, and rewards implemented per `docs/quests/goblin_tribe_quests.md` and `docs/encounters/mossroot_first_contact.md`.

**P3.4 — Small ruin dungeon playable.** 3–5 rooms; corruption VFX; loot; boss room.

**P3.5 — Boss encounter functional.** Full phase logic per `docs/systems/combat.md` and `docs/COMBAT_SYSTEM.md`.

**P3.6 — Save/load full-loop verified.** Player can save mid-quest, quit, reload, and complete.

**P3.7 — HUD + Inventory + Basic UI.** Placeholder theme; readable in all scenes.

**P3.8 — AI Director layer (mocked).** Pacing system runs; LLM calls remain mocked to preserve Offline-First.

**Exit criteria for Phase 3:** Player can start the game, recruit Talos, complete the Mossroot questline, defeat the boss, save, reload, and continue — all in Godot, no missing systems.

### Phase 4 — Early Access Preparation

Estimated: 8–12 weeks after Phase 3.

**P4.1 — VS-1 polish.** Replace placeholder art with a first pass of custom art in the VS-1 region.

**P4.2 — Optional AI layer.** Wire real LLM to `llm_bridge.py` Godot equivalent; enable ambient rumors and tavern gossip *behind an opt-in flag*.

**P4.3 — Companion Expertise beats.** Implement one Companion Expertise interaction per companion (out-of-combat contribution vignettes).

**P4.4 — Second region prototype.** Iterate on the Godot architecture with a second region (Great Forest recommended) to validate the pattern.

**P4.5 — Recruitment for a second companion.** Author Eleanor's recruitment scene + first Fractured Circle beat.

**P4.6 — Playtest + iteration.** Structured playtests of VS-1 → VS-2 flow; iterate on difficulty (per Difficulty by Choice canon), pacing, and companion relationships.

**P4.7 — Early Access candidate build.** Steam page, trailer, and packaged demo built from the VS-1 / VS-2 slice.

**Exit criteria for Phase 4:** A playable, publishable Early Access candidate demonstrating the target experience with one full campaign region, two companions, and one story arc.

---

## VS-8. Vertical Slice Readiness — Bottom Line

**Can VS-1 development begin today?** ❌ **Not today.** Design is 85% ready but the Critical documents in §VS-5 must be authored first (Phase 1) before Godot code lands.

**Can VS-1 development begin in 1–2 weeks?** ✅ **Yes** — provided:
1. Consolidation approval per Part I §9.
2. §3 and §7 rulings received.
3. Phase 1 documents authored per §VS-7.

**Is the design foundation strong enough?** ✅ **Yes.** After Phase 1, the design is complete enough that no gameplay invention is required during Godot implementation. Every VS-1 requirement can be served by existing canon (regions, companions, questlines, boss framework, combat model, save system) plus the new documents this report identifies.

**Is the scope realistic?** ✅ **Yes, with discipline.** VS-1 as scoped (Frontier + Talos + Mossroot + one dungeon + one boss + one loop) is achievable in 12–18 weeks *if* scope creep from Origin Characters, Custom Hero, real LLM integration, and Corwin/Future Healer is deferred to VS-2 or later.

**Recommendation:** Approve consolidation, rule the flagged items, author Phase 1 docs, then start the Godot project. **The project is closer to VS-1-ready than it looks — the gap is small, well-defined, and non-inventive.**

---

*End of report — including Vertical Slice Readiness Assessment.*
*Awaiting review and rulings before any repository modification.*
