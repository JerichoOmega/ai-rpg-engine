# CONTENT_PRODUCTION_ROADMAP.md — Post-Foundation Development Plan

> **Status:** ✅ Established February 2026 — the map for Phases 2–7.
> **Purpose:** The remaining Elyndor development plan, phased by dependency. Foundation Phase 1 is complete; this document governs what comes after.

---

## Phasing Principle

Each phase's work should not begin until its predecessor's outputs are stable enough to build upon without redesign. Parallel tracks are allowed where their outputs do not collide.

---

## Phase 2 — Character & Civilization Depth (Recommended Start)

**Goal:** bring characters and civilizations to the same authoring depth as goblins and vampires already have.

- **P2.1 — Hero Bibles (7 companions)**
  - Talos ← start here; VS-1 dependency
  - Eleanor ← Harmonic Soul complexity; second because arcs shape magic doc later
  - Ragash ← orc-cultural texture emerges here
  - Ronan ← curse/Choice-vs-Nature exemplar
  - Corwin ← gnome-cultural texture emerges here
  - Torren ← per prior seed
  - Community Healer ← last; needs refugee settlement context first
- **P2.2 — Civilization Deep-Passes**
  - Dwarves (highest existing foothold: forge canon, Iron Peaks, Kaelos)
  - Orcs (via Ragash arc completion)
  - Elves (parallel with elven region work)
  - Gnomes (Great Library scaffolding exists)
  - Beastfolk & Halflings (later — canonized as existing but low foothold)
- **P2.3 — Repository Consolidation (deferred sync)**
  - Execute the 15-edit Phase 2 task list from `PHASE_1_CONSISTENCY_AUDIT.md`
  - Directory restructure into `/app/GDD/`
  - Archive superseded fragments

**Exit criteria:** all 7 Hero Bibles complete; 5+ civilizations at goblin/vampire depth; repository restructured.

---

## Phase 3 — Regional & Faction Layer

**Goal:** the world's geography and non-civilization factions receive depth passes.

- **P3.1 — Region Deep-Passes** (6 canonical regions)
  - Capital Province · The Frontier · Sol Kareth · Iron Peaks · Great Forest · Frozen Highlands
- **P3.2 — Major Cities**
  - The Capital · regional hubs · goblin settlements' outsider-facing districts (per V-6)
- **P3.3 — Named Kingdoms & Provinces**
  - Human political geography; standing conflicts
- **P3.4 — Landmarks & Sites**
  - Complete authoring per `docs/world/GEOGRAPHY_LANDMARKS.md` seed
- **P3.5 — Non-civilization Factions**
  - Mages Guild depth · Adventurers Guild depth · Solari Covenant political wing · Cults (Ashen Tribunal, Severance, Threshold Circle)

**Exit criteria:** every region has enough depth to host questlines; every named faction has motivations, methods, internal factions.

---

## Phase 4 — Main Campaign Authoring

**Goal:** the primary player narrative.

- **P4.1 — Campaign Structure** (act count; through-line; tone)
- **P4.2 — Acts** (3–5 acts; each with premise and stakes)
- **P4.3 — Chapters** (per-act chapter breakdown)
- **P4.4 — Legacy Questlines Woven In**
  - Goblin Legacy Questline
  - Vampire Legacy Questline
  - Other civilization Legacy Questlines as authored
- **P4.5 — Major Antagonists & Bosses**
  - Corruption-linked; specific per act
- **P4.6 — Endings & Player-Choice Consequences**
  - Multiple; per Choice-vs-Nature pillar

**Exit criteria:** playable main campaign narrative structure end-to-end; every act ties into at least one Legacy Questline.

---

## Phase 5 — Side Content & Living World

**Goal:** the world *fills in*.

- **P5.1 — Side Quests** (per region; per faction)
- **P5.2 — Faction Quests** (deep faction arcs beyond the main campaign)
- **P5.3 — Random Encounters** (regional; travel-oriented; ambient life)
- **P5.4 — World Events** (dynamic — Corruption spread, faction moves, seasonal changes)
- **P5.5 — Ambient Storytelling** (NPCs living their lives independent of the player)

**Exit criteria:** the world feels lived-in regardless of what the player chooses to pursue.

---

## Phase 6 — Gameplay Integration

**Goal:** systems meet the lore.

- **P6.1 — Combat Systems** (character-level; per-companion; per-Origin)
- **P6.2 — Progression** (skill trees per companion; Origin-specific)
- **P6.3 — Equipment & Crafting** (forge canon → gameplay; craftsmanship-honors-Lyssara)
- **P6.4 — Magic System Implementation** (elemental study per D-04)
- **P6.5 — Exploration & Travel** (Journey System per prior canon)
- **P6.6 — Reputation & Faction Standing** (per systems/reputation.md; deep integration with civilizations)

**Exit criteria:** all mechanical systems are lore-grounded; no system contradicts a pillar.

---

## Phase 7 — Polish & Narrative Cohesion

**Goal:** the world speaks with one voice.

- **P7.1 — Dialogue Pass** (companion voice consistency; NPC memorability; proverb/prayer integration)
- **P7.2 — Environmental Storytelling** (lore placed in objects, ruins, journals per Preserving Wonder)
- **P7.3 — Narrative Review** (consistency across acts; foreshadowing; Chorus themes reinforced)
- **P7.4 — Balance & Pacing** (playtest; adjustment; final questline polish)
- **P7.5 — Continuity Audit** (final canon consistency sweep before content lock)

**Exit criteria:** the world is ready for external eyes.

---

## Recommended Development Order (User Preference Endorsed)

The user's preferred order — **Companions → Civilizations → Legacy Questlines → Regions → Main Campaign → Side Content → Gameplay Integration** — is **optimal given the current repository state**, with one refinement:

**Refinement:** Run **P2.3 (Repository Consolidation)** as an early sub-task within Phase 2. This unblocks all subsequent work by giving the repository a clean, predictable structure before the volume of authoring increases substantially.

**Alternative consideration:** Some **Regional work** (Phase 3.1) can run in parallel with **Civilization deep-passes** (Phase 2.2) where the region-culture pairing is tight (e.g., Iron Peaks + Dwarves; Great Forest + Elves + Mossroot goblins). This parallelization can save cycles without compromising quality.

---

## Guiding Principles Throughout All Phases

1. **Consult before invent** — check `LEGACY_CHARACTER_RESERVE.md` before creating new named characters.
2. **Preserve before overwrite** — apply the D-04c reframing pattern to reconcile contradictions.
3. **Rule before write** — major decisions go through `FINAL_CANON_DECISIONS.md`.
4. **Discover, don't explain** — Preserving Wonder governs all content.
5. **Cross-reference generously** — every new doc cites at least three existing docs.
6. **Respect the Silence** — the Forgotten Eighth, the Final Verse, the Schism — permanent mysteries.
7. **Foundation is locked** — the ten Foundation-Locked systems are not to be redesigned without an explicit new Canon Lock ruling.

---

## Document History

| Date | Change |
|---|---|
| Feb 2026 | Created — seven-phase content production roadmap. Governs post-Foundation Phase 1 development. User's preferred development order endorsed with one refinement (early Phase 2.3 consolidation sub-task) and one parallelization option (regional work alongside civilization deep-passes). |
