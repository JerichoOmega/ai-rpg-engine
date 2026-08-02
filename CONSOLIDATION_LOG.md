# Consolidation Log

> **Purpose:** Records every repository synchronization change made after the Foundation Sync passes, with the reason for each. Companion to `V5_V6_RECONCILIATION_REPORT.md` and `CONSOLIDATION_REPORT.md`.
> **Scope discipline:** No new lore introduced. No canon redesigned. No files moved, renamed, or deleted. No gameplay/quest/implementation code touched.

---

## Phase A — Safe Synchronization (2026-08-02)

Approved scope: stale terminology and age names; retired placeholder names; broken links; superseded/reference banners; navigation cross-references.

### A1. Stale age terminology (Canon Lock ruling D-01: Awakening · Harmony · Sundering · Restoration)

| File | Change | Reason |
|---|---|---|
| `docs/world/vampire_houses.md` | "Third Age — the Age of Wars" → "centuries of war in the Age of Restoration"; removed "Second Age" ordinal; added Talos cross-link | Deprecated age name. Placement in the Age of Restoration follows existing canon: `docs/heroes/TALOS.md` places Talos's service in the middle centuries of the Age of Restoration, and `docs/AI_CONTINUATION_GUIDE.md` states the Vampire Houses expanded during the same wars. |
| `docs/world/factions/vampire_houses/VAMPIRE_HISTORY.md` §4 | "wars of the Third Age" → "wars of the Age of Restoration" | Same mapping as above. (§2 "The Age of Wars Between" untouched — it is an in-universe vampire era name, deliberately distinct.) |
| `docs/world/GEOGRAPHY_LANDMARKS.md` (Old Fortress entry) | "during the Age of Wars" → "during the wars of the Age of Restoration" | Deprecated age name; same mapping. |
| `docs/heroes/ELEANOR.md` (sanctuary paragraph) | "sealed since the Age of Creation" → "sealed since the Age of Awakening" | Deprecated First Age name. |
| `elyndor/history/README.md` | Four Ages table renamed to canonical names/themes; D-01 note added; Confirmed Historical Events table age labels updated (imprisonment → Age of Sundering; wars, vampire expansion, Guild founding, seal weakening → Age of Restoration; Corruption → Sundering onset / Restoration acceleration) | Table used the fully deprecated Creation/Kingdoms/Wars/Shadows framework. Event placements follow `docs/lore/HISTORY_BIBLE.md` (imprisonment in the Sundering; Guild functioning in the stabilized Restoration) and `docs/heroes/TALOS.md`. |
| `docs/AI_CONTINUATION_GUIDE.md` | HISTORY_BIBLE row updated to canonical age names with D-01 citation | Guide row still taught the deprecated names to future sessions. |
| `docs/roadmap.md` | Changelog line annotated: age names superseded by D-01 | Historical entry preserved; annotation prevents it being read as current canon. |
| `elyndor/history/HISTORY_BIBLE.md` (Document History) | History row reworded to note the original names were renamed per D-01 | Same rationale — changelog kept, stale names no longer restated. |
| `docs/lore/DEVELOPMENT_REFERENCE.md` | Stale note replaced: both history bibles now use the canonical Four Ages; Seven Ages framework noted as superseded | The old note wrongly directed readers to a "Seven Ages canon" and called the (already corrected) elyndor bible obsolete. |

### A2. Retired placeholder names (Legacy Character Reserve, ruling P-01)

| File | Change | Reason |
|---|---|---|
| `docs/characters/talos.md` | "**Steven** — (relationship not yet defined)" → Torren entry summarizing the authored dynamic, pointing to `docs/heroes/TALOS.md`; Steven retirement noted | Steven is non-canonical (retired to `LEGACY_CHARACTER_RESERVE.md`); Torren is his replacement and the Talos–Torren dynamic is already authored. |
| `docs/characters/eleanor.md` | Same pattern → pointer to `docs/heroes/ELEANOR.md` | Same. |
| `docs/characters/ragash.md` | Same pattern → pointer to `docs/heroes/RAGASH.md` | Same. |
| `docs/characters/ronan.md` | Same pattern → pointer to `docs/heroes/RONAN.md` | Same. |
| `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md` (vampire houses table) | Leader names updated: Serath Vetharis → Lord Cassiel Vetharis; Kira Drakmor → Lady Morreth Drakmor; Archivist-Queen Mira Soleth → The Archivist; provenance footnote added | The old names are reserved legacy names (P-01), not active leaders; current leaders per `docs/world/vampire_houses.md`. |

### A3. Superseded/reference banners

| File | Change | Reason |
|---|---|---|
| `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md` | "PARTIALLY SUPERSEDED" banner added at top identifying the stale framework discussion and legacy leader names, deferring to `FINAL_CANON_DECISIONS.md` | Both reconciliation reports identify this file as the primary source of stale data. |
| `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md` | Dual Seven-Age/Four-Age framework section replaced with the single canonical Four Ages row and a D-01 resolution note; source-table row corrected | The "designer decision is needed / both are confirmed canon" text was resolved by D-01; leaving it invited new content on a dead framework. |

### A4. Navigation cross-references

| File | Change | Reason |
|---|---|---|
| `docs/world/goblin_tribes.md` (header) | "See also" link to root `GOBLIN_CULTURE.md` summarizing what only that pillar defines (rites, Council of Elders, Corrupted-goblins-not-a-fourth-tribe ruling) | Operational doc and cultural pillar were not linked; writers starting from either file could miss the other. |
| `docs/world/vampire_houses.md` (header) | "Foundation rulings" link to root `VAMPIRE_CANON_AUDIT.md` (V-1–V-6) with a note that its "Three Houses" framing predates the ten-house roster | Connects operational canon to the locked pillar rulings and pre-empts the three-vs-ten confusion. |
| `docs/lore/DIVINE_CHORUS.md` (header) | "See also" banner to root `DIVINE_CHORUS.md` (eight named Voices, seven Heralds, D-04c/D-05) | The docs/lore file predates the named-Voices/Heralds pillar; without the pointer it reads as a complete theology. |

### A5. Broken links

| Finding | Resolution |
|---|---|
| Reported dead link to `docs/lore/GREAT_LIBRARY.md` (from `HOUSE_PROFILES.md`, `FACTION_BIBLE.md`, `SECRET_ORGANIZATIONS.md`, `journal_system.md`) | **False positive — no change.** The file exists at `docs/lore/GREAT_LIBRARY.md`; all links resolve. |

### Post-review corrections (same pass)

| File | Change | Reason |
|---|---|---|
| `elyndor/history/README.md` | Mages Guild event row reworded: precursors in the Age of Harmony, current institutional form in the Age of Restoration, founding date not canonically fixed | Review caught that my first wording asserted a settled Restoration founding date, which no canonical source fixes. |
| `docs/world/vampire_houses.md` | "Third Age section" pointer → "Age of Restoration section" | The linked history bible no longer uses that section label. |

### Remaining inconsistencies deliberately NOT touched (need a canon ruling or belong to later phases)

1. `VAMPIRE_HISTORY.md` §2 "The Age of Wars Between" — in-universe vampire era name; kept as deliberate canon.
1b. `docs/world/vampire_houses.md` body text (Soleth section, Theranel scenes) uses ordinal "Second Age"/"Third Age" in in-universe scholarly dialogue and catalogue labels. Under D-01 these ordinals now denote Harmony/Sundering; whether each usage still points where the author intended requires a content-level ruling — flagged for the existing old-vocabulary sweep (task #113 per the 2026-07-31 handoff) rather than mechanically remapped here.
2. `CONSOLIDATION_REPORT.md`'s proposed `/GDD/` restructure — Phase C, deferred per approval scope.
3. `exports/goblin_tribes_brainstorm.zip` duplicates its unpacked .md siblings — deletion is out of Phase A scope.
4. Root pillar docs (`GOBLIN_CULTURE.md`, `WORLD_BIBLE_1.0.md`, etc.) received no back-links to the docs/ tree — the reconciliation reports schedule their banner pass for Phase 2; left to that phase to avoid editing locked pillars.

---

## Log History

| Date | Entry |
|---|---|
| 2026-08-02 | Phase A safe synchronization executed and logged |
