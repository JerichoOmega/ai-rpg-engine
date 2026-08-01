# FINAL_CANON_DECISIONS.md

> **Purpose:** Consolidate every unresolved architectural, canon, and design decision identified in `CONSOLIDATION_REPORT.md` into a single ruling-ready document.
> **Instruction:** Read each decision, rule on one option per decision, then return the ruled document. No repository changes will be made until every ruling is received.
> **Status:** Canon Lock phase — sequential rulings in progress.
> **Author:** E1 (Project Consolidation Phase — decision-authoring pass).
> **Date:** January 2026.
> **Source of every decision below:** `CONSOLIDATION_REPORT.md` Part I §3 (contradictions), §4.C (new canon), §7 (R1–R10 high-risk), and Part II VS-3–VS-6 (VS-1 blockers).

---

## Running Approved Rulings

| # | ID | Status | Ruling Summary | Approved |
|---|---|---|---|---|
| 1 | D-01 | ✅ CANONICAL | **Four Ages framework adopted:** Age of Awakening → Age of Harmony → Age of Sundering → Age of Restoration. Long Decline is the final era of the Age of Harmony (not a separate Age). Full age names in canonical docs; "First Age / Third Age" shorthand allowed in in-world dialogue or scholarly references only; "Age I / II / III / IV" reserved for internal notes. Prior frameworks (Version A and Version B) archived for development-history reference only; obsolete framework names removed from canonical docs. | Jan 2026 |
| 2 | D-02 | ✅ CANONICAL | **Three-stage sanctuary revelation for Eleanor's Harmonic Soul:** (1) **Resonance** — Eleanor senses Primordial resonance approaching the sanctuary; no voice, no vision, no deity. (2) **Discovery** — Eleanor reads preserved First Age scholarship on Harmonic Souls inside the sanctuary; realizes it describes her. She reaches the conclusion herself. (3) **Confirmation** — At the sanctuary's heart, an ancient chamber saturated with Primordial resonance responds naturally to her presence — not because she is chosen, but because she possesses the qualities the sanctuary was designed to recognize. **No god ever appears, speaks, or reveals Eleanor's identity.** Occurs during The Fractured Circle questline. Present companions witness resonance but experience nothing themselves; reactions vary by personality. Reinforces the theme *"history belongs to mortals."* | Jan 2026 |
| 3 | D-03 | ✅ CANONICAL (revised) | **Roster of seven canonical companions:** Talos, Eleanor, Ragash, Ronan, Torren, **Corwin** (Gnome male Ranger — Truth/Observation/Curiosity; long-time Corruption investigator; Marksman + Skirmisher combat trees; expertise in tracking, foraging, corruption investigation, environmental observation), **Community Healer** (female; community healer / battlefield physician; skilled in medicine, herbal remedies, restorative magic; tied to a refugee settlement; recruited via "A Light in the Ashes" — refuses to leave until player secures long-term aid through the Imperial Council; theme: Service, Compassion, Preservation; full Hero Bible + final name + race + combat specialization still to be authored). **Every companion** requires a Hero Bible, Core Wound, personal questline, Companion Expertise, Companion Evolution, Settlement behaviors, and Origin playthrough support. **Party: 7 recruitable / 4 active.** Safe settlements always contain every recruited companion. All companion systems assume the final roster of seven. **VS-1 still focuses on Talos as the primary Origin;** the remaining six companions arrive in later milestones per the roadmap. | Jan 2026 |

*(3 of 30 approved — running total.)*

---

## How to Rule

For each decision, mark the option you approve (write "APPROVED" next to it) or provide an alternative. If a Recommendation is acceptable as-is, write "APPROVED per recommendation." If you need more information before ruling, write "HOLD — need X." Nothing is applied to the repository until every decision has a ruling.

---

## Section A — Canon & Lore Decisions

### D-01 · Historical Framework — Four Ages canonical

**Decision ID:** D-01
**Title:** Confirm the Four-Age historical framework as canon; retire the Seven-Age and original Four-Age names.
**Current Conflict:**
Three overlapping historical frameworks exist across the repository:
- **Version A (obsolete):** Age of Creation → Kingdoms → Wars → Shadows.
- **Version B (superseded):** Seven Ages — Awakening / Discovery / Unity / Long Decline / Sundering / Restoration / Present.
- **Version C (current per the latest prompt + lore-bible body):** Awakening → Harmony → Sundering → Restoration; Long Decline is the tragic final chapter of the Age of Harmony.

The *body content* of `docs/lore/HISTORY_BIBLE.md`, `docs/lore/TIMELINE.md`, `elyndor/history/HISTORY_BIBLE.md`, and `docs/lore/civilization/*` already reflects Version C. Stale references remain in seven other files.

**Affected Files:**
- `PROJECT_MEMORY.md` (Decision #22)
- `docs/AI_CONTINUATION_GUIDE.md` (line 38)
- `docs/roadmap.md` (line 105)
- `.agents/memory/lore-bible-canon.md`
- `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md` (header + source table)
- `LORE_CONSISTENCY_AUDIT.md` (partially outdated findings ❌ #1, ❌ #3, ⚠ #5)
- Revision-log entries in `elyndor/history/HISTORY_BIBLE.md` and `docs/lore/HISTORY_BIBLE.md`

**Options:**
1. **Adopt Version C as canon.** Retire A + B; sweep all remaining references.
2. Revert to Version A (Age of Creation/Kingdoms/Wars/Shadows).
3. Restore Version B (Seven Ages).
4. Author a fourth alternative framework.

**Pros:**
- **Option 1:** Matches the owner's most recent directive and the current Lore Bible body content. Zero content invention required — only cleanup.
- Option 2: Familiar names for early collaborators.
- Option 3: Adds granularity (Long Decline + Present Age as distinct periods).
- Option 4: Full creative freedom.

**Cons:**
- Option 1: None material — this is administrative cleanup.
- Option 2: Contradicts the latest prompt directly; reintroduces the framework the owner just retired.
- Option 3: Reintroduces the framework the owner explicitly restored back to Four Ages.
- Option 4: Requires re-authoring six major lore documents; massive scope increase.

**Your Recommendation:**
**Option 1 — Adopt Version C.** Every downstream doc will be updated to Awakening / Harmony / Sundering / Restoration. No lore is removed — events attributed to the obsolete age names simply remap to the new ages.

**Impact if Accepted:**
- ~15 discrete edits across the seven affected files.
- `LORE_CONSISTENCY_AUDIT.md` findings ❌ #1, ❌ #3, ⚠ #5 auto-close.
- `.agents/memory/lore-bible-canon.md` and `docs/lore/world/WORLD_FOUNDATION_SUMMARY.md` headers rewritten.
- `PROJECT_MEMORY.md` Decision #22 rewritten with new age names.
- The revision-log entries in the two HISTORY_BIBLE.md files retain their history (for provenance) but a new final entry marks the ruling.

**Priority:** Critical.

**✅ RULING — CANONICAL (January 2026):**

**Option 1 — APPROVED.** The canonical historical framework is:

1. **Age of Awakening** — birth of the world; emergence of first civilizations; foundations of magic, the Divine Chorus, and the world's earliest history.
2. **Age of Harmony** — the golden age of civilization; rise of kingdoms and empires; peace, prosperity, and unprecedented advancement. **The Long Decline is the final historical era of the Age of Harmony — during which corruption slowly erodes civilization — and is NOT a separate Age.**
3. **Age of Sundering** — collapse of the old world; great wars; the fall of kingdoms and empires; corruption spreads openly; ancient powers are lost or forgotten.
4. **Age of Restoration** — civilization struggles to rebuild; new kingdoms emerge; corruption remains an ever-present threat. **The game begins near the end of this Age**, when the fragile restoration is once again in danger.

Additional canonical rulings:
- The Long Decline remains a historical *period*, not an Age.
- Previous frameworks (Version A: Creation/Kingdoms/Wars/Shadows; Version B: Seven Ages) are archived for development history only. They are no longer canonical and must not appear in current documentation.
- Preserve revision history in archived development documents, but remove obsolete framework references from canonical Game Design Documents and Lore Bibles.
- Canonical documentation uses the **full age names**: *Age of Awakening, Age of Harmony, Age of Sundering, Age of Restoration.*
- Shorthand such as "First Age" or "Third Age" is permitted only in in-world dialogue or scholarly references.
- "Age I / II / III / IV" notation is reserved for internal development notes and must not appear in canonical player-facing content.

**Applied to consolidation plan.** Awaiting all remaining rulings before repository modification begins.

---

### D-02 · Eleanor's Harmonic Soul Revelation — Delivery Mechanism

**Decision ID:** D-02
**Title:** Change how Eleanor learns she is a Harmonic Soul; the revelation's content stays canonical.
**Current Conflict:**
`docs/heroes/ELEANOR.md` lines 159–188 depict *"Eleanor encounters one of the gods"* who explains her Harmonic Soul to her directly. `docs/lore/CANON_RULES.md` and `docs/lore/DIVINE_CHORUS.md` prohibit exactly this: *"They do not communicate personal divine instructions to individuals"* and *"If a piece of content requires the Chorus to act, speak, appear, or select someone — it almost certainly violates the principles."* Already flagged as ❌ #4 in `LORE_CONSISTENCY_AUDIT.md`.

**Affected Files:**
- `docs/heroes/ELEANOR.md`
- `docs/characters/eleanor.md` (may reference)
- `docs/systems/dynamic_story_arcs.md` (The Fractured Circle references Eleanor's revelation)
- `elyndor/magic/MAGIC_BIBLE.md` (Harmonic Soul concept anchored here)

**Options:**
1. **Sanctuary-Delivered Truth.** The sealed First-Age sanctuary itself communicates the truth through crystallized memory, resonance, or ancient inscription — no god appears.
2. **Vision / Overwhelming Impression.** Eleanor experiences a wordless, non-personal revelation as ambient Primordial resonance flows through her at the sanctuary — she *feels* it rather than being *told* it.
3. **Preserved Ancient Records.** The sanctuary contains a First-Age archivist's testimony or scholar's records that describe Harmonic Souls generally; Eleanor recognizes herself in the description.
4. Keep the god-in-person encounter (do not fix).

**Pros:**
- **Option 1:** Preserves mystique; sanctuary itself becomes a character. Compatible with Architects-adjacent aesthetic.
- Option 2: Cleanest match to the "Chorus is a presence, not a plot device" rule; wordless discovery is emotionally powerful.
- Option 3: Grounds the revelation in mortal-authored scholarship — extremely consistent with "history belongs to mortals."
- Option 4: No rewrite cost.

**Cons:**
- Option 1: Requires a small new lore element (what the sanctuary *is* mechanically) but nothing that contradicts existing canon.
- Option 2: Risk of feeling underwhelming without careful writing.
- Option 3: Slightly less emotionally direct; puts scholarship between Eleanor and her own truth.
- Option 4: Direct Canon Rules violation; every future Chorus-adjacent content invites the same violation.

**Your Recommendation:**
**Option 1 — Sanctuary-Delivered Truth.** It preserves the ambition of the original scene (Eleanor experiences the revelation as a *place-driven* discovery), lets the sanctuary itself carry the weight instead of a god, and integrates with existing First-Age / First-Temple canon. It leaves room in later content for Options 2 and 3 as *layered* delivery (Eleanor experiences resonance, discovers records, and pieces the truth together across the arc).

**Impact if Accepted:**
- Rewrite lines 159–188 of `docs/heroes/ELEANOR.md`.
- Update `docs/systems/dynamic_story_arcs.md` The Fractured Circle to reference the sanctuary rather than a Chorus member.
- Add ~1 paragraph to `elyndor/magic/MAGIC_BIBLE.md` describing pre-Sundering sanctuaries as places where Primordial resonance can still be sensed directly.
- `LORE_CONSISTENCY_AUDIT.md` ❌ #4 auto-closes.

**Priority:** Critical.

**✅ RULING — CANONICAL (January 2026):**

**Option 1 — APPROVED with layered stages.** The Harmonic Soul revelation occurs in three sequential stages during The Fractured Circle questline:

**Stage 1 — Resonance**
As Eleanor approaches the ancient sanctuary, she begins experiencing an overwhelming sense of Primordial resonance unlike anything she has ever felt before. This is not a vision. No voice speaks. No divine figure appears. She simply senses that the magic surrounding her is fundamentally different from anything she has studied. Something extraordinary is happening — but no answers are given yet.

**Stage 2 — Discovery**
Within the sanctuary, Eleanor discovers preserved First Age records, inscriptions, and magical research left behind by ancient scholars. These records describe the existence of Harmonic Souls and document observations about individuals capable of perceiving Primordial Magic as a unified whole rather than as isolated elements. Nothing explicitly identifies Eleanor. Instead, she gradually realizes that every description matches her own experiences throughout her life. **The sanctuary never tells her who she is. She reaches that conclusion herself.**

**Stage 3 — Confirmation**
At the sanctuary's heart lies an ancient chamber saturated with Primordial resonance. When Eleanor enters, the sanctuary responds naturally to her presence — not because it has chosen her, not because she is special to the gods, but because she possesses the qualities the sanctuary was originally designed to recognize. The response confirms the conclusion she has already reached. The sanctuary does not speak. No deity appears. No divine instruction is given. The place itself simply reacts in a way that no ordinary mage could trigger.

**Additional canonical rulings:**
- The Divine Chorus never appears, speaks directly to Eleanor, or gives personal guidance.
- The gods never reveal Eleanor's identity.
- Eleanor discovers the truth through observation, scholarship, and experience.
- The sanctuary confirms her conclusion through ancient magical resonance rather than dialogue.
- The revelation reinforces the world's central theme: *"History belongs to mortals."* Knowledge is preserved by civilizations, scholars, and sacred places — not by divine intervention.
- The revelation occurs **during The Fractured Circle questline**, so Eleanor's emotional and personal journey culminates alongside the larger narrative.
- Other companions present in the active party may witness the resonance but experience nothing themselves. Reactions vary by personality (Ronan senses nothing, Ragash's hounds may react to the resonance without understanding it, Talos observes with quiet respect, Torren treats the sanctuary as a work of craft worthy of study). This reinforces that the sanctuary responds specifically to a Harmonic Soul rather than creating a universal magical event.
- `LORE_CONSISTENCY_AUDIT.md` ❌ #4 auto-closes on ruling application.

**Applied to consolidation plan.** Awaiting all remaining rulings before repository modification begins.

---

### D-03 · Companion Roster Final Count

**Decision ID:** D-03
**Title:** Rule on Corwin and the Future Healer — are they canonical companions, deferred concepts, or removed?
**Current Conflict:**
Every existing doc (`docs/PLAYER_SYSTEM.md`, `docs/characters/README.md`, `docs/HERO_BIBLE.md`, `DESIGN_DECISIONS.md` #016) lists the roster as exactly **five**: Talos, Eleanor, Ragash, Ronan, Torren. The current project's problem statement introduces two additional names — **Corwin** (tracking, foraging, corruption investigation) and **Future Healer** (medicine, community health, refugee care) — implying a roster of seven. No Hero Bible or character sheet exists for either.

**Affected Files:**
- `docs/PLAYER_SYSTEM.md`
- `docs/HERO_BIBLE.md`
- `docs/CHARACTER_DESIGN_GUIDE.md`
- `docs/characters/README.md` + potentially two new sheets
- `docs/heroes/README.md` (if any) + potentially two new Hero Bibles
- `DESIGN_DECISIONS.md` (Decision #016)
- `PROJECT_MEMORY.md` roster references
- All future Companion Expertise / Evolution / Settlement Dispersal docs
- Combat balance targets (party of four; four out of seven vs four out of five)

**Options:**
1. **Canonize both.** Corwin and Future Healer become companions #6 and #7. Full Hero Bible + character sheet + Core Wound + personal-quest sketch authored for each.
2. **Canonize Corwin only.** Roster of six; Future Healer becomes a placeholder concept for later expansion.
3. **Canonize Future Healer only.** Roster of six; Corwin becomes a placeholder concept.
4. **Defer both as [PLANNED] concepts.** Roster stays at five; Expertise/Evolution docs reference the two names as [PLANNED] entries without authored content.
5. **Rename an existing companion.** Corwin becomes a re-identified version of one of the five (unlikely fit for any).
6. **Remove both.** Corwin and Future Healer excluded from canon; problem-statement mention treated as an error.

**Pros:**
- Option 1: Full canonical clarity; both concepts get proper design treatment; expertise matrix in the current problem statement lines up 1:1.
- Option 2: Corwin's expertise (tracking / foraging / corruption investigation) is a distinctive niche not covered by the five; healer role can be authored later.
- Option 3: Healer is the classical "missing role" from the current roster; expertise matrix identifies him/her as urgent.
- **Option 4:** Lowest scope risk; preserves the problem statement's mention as forward-looking canon; keeps VS-1 focused on the confirmed five.
- Option 5: Preserves the five-companion party balance.
- Option 6: Simplest, but contradicts a direct owner statement.

**Cons:**
- Option 1: Adds ~30–40 pages of authored content (2 × Hero Bibles + sheets + arcs + interventions); delays VS-1.
- Option 2/3: Asymmetric authoring; still adds content weight; makes the Expertise matrix awkward with one placeholder.
- Option 4: The Expertise / Evolution docs will contain placeholder rows for two unauthored companions.
- Option 5: Every candidate rename creates a canon violation elsewhere.
- Option 6: Directly contradicts the current problem statement (which explicitly names both).

**Your Recommendation:**
**Option 4 — Defer both as [PLANNED] concepts.** Roster stays at five for VS-1 and Phase-2. Companion Expertise and Companion Evolution documents will include Corwin and Future Healer rows *clearly marked [PLANNED]*, preserving the owner's stated intent without adding VS-1 authoring debt. When authored later (Phase-3 or beyond), both become companions #6 and #7 without breaking existing content.

**Impact if Accepted:**
- Roster count remains five in `docs/PLAYER_SYSTEM.md`, `docs/HERO_BIBLE.md`, `docs/characters/README.md`, `DESIGN_DECISIONS.md` #016.
- Companion Expertise doc (new) includes seven rows; two marked [PLANNED].
- Companion Evolution doc (new) includes seven rows; two marked [PLANNED].
- Settlement Dispersal doc (new) references the five confirmed companions for now.
- Two placeholder Hero Bible files created (`GDD/05_Companions/heroes/CORWIN.md`, `FUTURE_HEALER.md`) with only header + [PLANNED] markers.
- VS-1 companion (Talos) is unaffected.

**Priority:** Critical.

**✅ RULING — CANONICAL (January 2026, REVISED):**

**Prior ruling (Option 4 — defer) OVERRIDDEN. Option 1 — APPROVED.** The canonical companion roster consists of **seven companions**:

1. **Talos**
2. **Eleanor**
3. **Ragash**
4. **Ronan**
5. **Torren**
6. **Corwin**
7. **The Community Healer** (final name to be determined)

**Corwin — canonical identity locked:**
- Race: Gnome
- Gender: Male
- Role: Ranger
- Theme: Truth, Observation, and Curiosity
- Long-time investigator of the Corruption
- Expert tracker, forager, survivalist, and wilderness guide
- Believes seemingly unrelated events are connected; often dismissed as paranoid until proven correct
- Combat specialization branches:
  - Marksman (Longbow)
  - Skirmisher (Crossbow / Traps / Mobility)
- Companion Expertise: Tracking, Foraging, Corruption investigation, Environmental observation

**The Community Healer — canonical role locked; full identity to be authored:**
- Female
- Community healer rather than a traditional cleric
- Battlefield physician
- Skilled in medicine, herbal remedies, and restorative magic
- Closely tied to a refugee settlement
- Recruited through the questline **"A Light in the Ashes"**
- Refuses to leave her community until the player helps secure long-term aid through the Imperial Council
- Theme: Service, Compassion, and Preservation
- Final name, race, appearance, and combat specialization to be authored in a later phase

**Universal companion rules (apply to all seven):**
- Every companion is also a playable Origin Character.
- Every companion has:
  - A Hero Bible
  - A Core Wound
  - A personal questline
  - Companion Expertise
  - Companion Evolution
  - Settlement behaviors
  - Origin playthrough support
- **Party size:** 7 recruitable / 4 active.
- **Settlement Dispersal:** Safe settlements always contain every recruited companion, each occupying locations appropriate to their personality and expertise.
- The Companion Relationship matrix, Companion Expertise system, Companion Evolution system, and Settlement Dispersal system all assume the final roster of **seven** companions (21 companion pairs + player↔each = 28 relationship channels).

**Vertical Slice clarification:**
The Vertical Slice does NOT need to include every companion. **VS-1 focuses on Talos as the primary Origin Character.** The remaining six companions are introduced in later milestones according to the roadmap. Corwin and Community Healer Hero Bibles are authored ahead of their respective milestone content.

**Applied to consolidation plan.** Awaiting all remaining rulings before repository modification begins.

---

---

### D-04 · Primordial Magic Attribution

**Decision ID:** D-04
**Title:** Correct the Primordial Magic origin from "the Ancient God" to the collective Divine Chorus.
**Current Conflict:**
`elyndor/magic/MAGIC_BIBLE.md` line 11 attributes Primordial Magic to *"the Ancient God during the First Age."* `docs/lore/TIMELINE.md` (canonical) says the First Song was sung by the *full eight-member Chorus* and Primordial Energy stabilized from that collective act. The Eighth's role was to *fracture* Primordial Magic during her fall, not to create it.

**Affected Files:**
- `elyndor/magic/MAGIC_BIBLE.md` (line 11 primarily)
- `docs/heroes/ELEANOR.md` (Harmonic Soul framing implies pre-fracture Primordial Magic connection)

**Options:**
1. **Attribute Primordial Magic to the full Chorus / the First Song.**
2. Keep attribution to the Eighth alone.

**Pros:**
- Option 1: Consistent with `TIMELINE.md`, `DIVINE_CHORUS.md`, `CANON_RULES.md`. Preserves both facts (Chorus authored Primordial Magic; the Eighth's fall fractured it).
- Option 2: Simpler in isolation.

**Cons:**
- Option 1: None material — one-paragraph rewrite.
- Option 2: Direct contradiction with the Lore Bible; also creates an implicit chosen-one arc for Eleanor by tying her Harmonic Soul to the Eighth's individual creation.

**Your Recommendation:**
**Option 1.** Reword line 11 to: *"Primordial Magic is the original magical force that emerged from the First Song of the Divine Chorus during the Age of Awakening. The imprisonment of the Forgotten Eighth fractured it into seven elemental aspects — the form modern mages study today."*

**Impact if Accepted:**
- One paragraph rewrite in `MAGIC_BIBLE.md`.
- Eleanor's Harmonic Soul becomes a connection to the collective Chorus's work rather than the Eighth's individual work — resolves `LORE_CONSISTENCY_AUDIT.md` ⚠ #9 as a side effect.

**Priority:** High.

---

### D-05 · "The Ancient God" vs "The Forgotten Eighth" — Terminology

**Decision ID:** D-05
**Title:** Standardize developer-facing vs in-world terminology for the imprisoned Chorus member.
**Current Conflict:**
Both terms are used interchangeably across the repo. Lore Bible states the canonical developer-facing name is *the Forgotten Eighth*; *the Ancient God* / *the Absent One* are in-world labels used by characters who lack access to the truth.

**Affected Files:**
- `elyndor/history/HISTORY_BIBLE.md` (lines 31, 71, 88, 100)
- `elyndor/magic/MAGIC_BIBLE.md` (lines 11, 13)
- `docs/CAMPAIGN_DESIGN.md` (line 35)
- `elyndor/history/the_eighth.md`
- `docs/GAME_BIBLE.md`

**Options:**
1. **Two-tier terminology.** Developer/writer docs = "the Forgotten Eighth." In-world content (dialogue, cult texts, common knowledge) = "the Ancient God" / "the Absent One."
2. Standardize on "the Forgotten Eighth" everywhere.
3. Standardize on "the Ancient God" everywhere.

**Pros:**
- Option 1: Matches Lore Bible intent; preserves in-world flavor.
- Option 2: Absolute consistency.
- Option 3: Familiar; simpler.

**Cons:**
- Option 1: Requires contributors to distinguish contexts.
- Option 2: Robs the in-world content of dramatic irony (characters knowing less than the audience).
- Option 3: Reinforces the misconception the Lore Bible was designed to correct; damages the tragedy framing.

**Your Recommendation:**
**Option 1.** Every conversion will be logged in `GDD/00_Rationale_Log.md`.

**Impact if Accepted:**
- ~10 edits across the affected files.
- Style guide entry added to `docs/coding_standards.md` (or a new writing-style guide) documenting the two-tier rule.

**Priority:** High.

---

### D-06 · "Gods Walked Among Mortals" Reframe

**Decision ID:** D-06
**Title:** Clarify that only the Eighth spent extended time among mortals — not the full Chorus.
**Current Conflict:**
`elyndor/history/HISTORY_BIBLE.md` line 35 states *"The gods walked among mortals directly, before their withdrawal."* This implies the full Chorus was historically more directly present, which the Lore Bible does not authorize.

**Affected Files:**
- `elyndor/history/HISTORY_BIBLE.md`

**Options:**
1. **Reframe to Eighth-specific.** *"The Eighth spent extended time among mortals — a behavior unusual for the Chorus, whose members otherwise stayed distant from mortal affairs. After the Sundering, the Chorus became more careful in every interaction with the world."*
2. Delete the sentence.
3. Keep unchanged.

**Pros:**
- Option 1: Preserves the emotional weight of the Chorus's post-Sundering caution while making the Eighth's individual behavior clear.
- Option 2: Fastest cleanup.
- Option 3: No work.

**Cons:**
- Option 1: One paragraph rewrite.
- Option 2: Loses a valuable emotional beat.
- Option 3: Direct contradiction with `DIVINE_CHORUS.md`.

**Your Recommendation:**
**Option 1.**

**Impact if Accepted:**
- One sentence + surrounding paragraph rewritten in `elyndor/history/HISTORY_BIBLE.md`.
- Resolves `LORE_CONSISTENCY_AUDIT.md` ⚠ #4.

**Priority:** Medium.

---

### D-07 · "Shaped the First Races" Reframe

**Decision ID:** D-07
**Title:** Remove the implication that the Eighth created mortal life.
**Current Conflict:**
`elyndor/history/HISTORY_BIBLE.md` line 31 says the Eighth *"directly shaped … the first races."* The Lore Bible explicitly states the Chorus did not create mortal life. Attributing race-creation to the Eighth undermines both "no chosen races" and "the Chorus did not design civilization."

**Affected Files:**
- `elyndor/history/HISTORY_BIBLE.md`

**Options:**
1. **Reframe to physical-world influence only.** The Eighth's influence on Elyndor's landscape (rivers, forests, geographical formations) is compatible with her Chorus stewardship. Attribute *no* influence on mortal races or civilization.
2. Delete the reference entirely.
3. Keep unchanged.

**Pros:**
- Option 1: Preserves the Eighth's presence in the First Age without violating canon.
- Option 2: Fastest.
- Option 3: No work.

**Cons:**
- Option 1: Requires small rewrite.
- Option 2: Loses a First-Age worldbuilding beat.
- Option 3: Direct canon violation.

**Your Recommendation:**
**Option 1.**

**Impact if Accepted:**
- One sentence rewritten.
- Resolves `LORE_CONSISTENCY_AUDIT.md` ⚠ #3.

**Priority:** Medium.

---

### D-08 · The Great Library — Singular

**Decision ID:** D-08
**Title:** Fix the "Great Libraries" (plural) reference in the Capital institutions list.
**Current Conflict:**
`docs/world/WORLD_BIBLE.md` line 246 lists *"Universities, Great Libraries"* (plural). Every other reference — including all of `docs/lore/GREAT_LIBRARY.md` — treats the Great Library as a singular institution.

**Affected Files:**
- `docs/world/WORLD_BIBLE.md`

**Options:**
1. **Change to "the Great Library" (singular).**
2. Add lore establishing multiple Great Libraries (rejected by every other file).

**Pros:**
- Option 1: Trivial cleanup; matches every other doc.
- Option 2: None.

**Cons:**
- Option 1: None.
- Option 2: Contradicts `docs/lore/GREAT_LIBRARY.md`.

**Your Recommendation:**
**Option 1.**

**Impact if Accepted:**
- One-word edit in `docs/world/WORLD_BIBLE.md`.
- Resolves `LORE_CONSISTENCY_AUDIT.md` ⚠ #8.

**Priority:** Low.

---

## Section B — Design-Pillar Decisions (New Canon)

### D-09 · Difficulty by Choice — Canonical Adoption

**Decision ID:** D-09
**Title:** Codify "no traditional Easy/Normal/Hard; difficulty evolves through player choices" as a design pillar.
**Current Conflict:**
The current problem statement establishes this as canon: *"There is no traditional Easy / Normal / Hard difficulty. Difficulty naturally evolves through player choices."* No existing document contradicts this — but no existing document *states* it either.

**Affected Files:**
- New file: `GDD/03_Core_Gameplay/07_Difficulty_Philosophy.md`
- Reference edits in: `docs/GAME_BIBLE.md` (Design Pillars section), `PROJECT_MEMORY.md`, `docs/CAMPAIGN_DESIGN.md`
- Cross-reference from: `docs/systems/dynamic_story_arcs.md`, `docs/systems/journey_system.md`

**Options:**
1. **Adopt as canon; author a dedicated doc.** Difficulty is fully driven by choices (ignore a threat → world becomes harder; help a community → stability improves; corruption resistance depends on companion bonds).
2. Adopt as canon but hybrid — expose a hidden "world tension" slider as a tunable for playtesting only.
3. Do not adopt; keep design open.

**Pros:**
- **Option 1:** Cleanest match to the owner's directive; aligns with Living World and Companion Bonds systems.
- Option 2: Playtesting flexibility.
- Option 3: Maximum design freedom later.

**Cons:**
- Option 1: Requires numeric tuning per region/faction/companion state — non-trivial balance work.
- Option 2: Risk of the slider persisting into shipped product against the pillar's intent.
- Option 3: Contradicts the owner's stated canon.

**Your Recommendation:**
**Option 1.** Dedicated doc in `GDD/03_Core_Gameplay/07_Difficulty_Philosophy.md`. Includes concrete examples: ignoring the Frontier Corruption raises regional danger; completing Mossroot's questline reduces hollow-game encounters in later regions; deep companion bonds enable Corruption interventions.

**Impact if Accepted:**
- One new doc.
- Small additions to `docs/GAME_BIBLE.md` Design Pillars section.
- Numeric tuning framework becomes part of the balance work in Phase-3.

**Priority:** Critical.

---

### D-10 · Offline-First Scope

**Decision ID:** D-10
**Title:** Codify the offline-first requirement and define what "fully playable offline" means.
**Current Conflict:**
The owner's directive: *"The entire RPG must function completely offline. Everything required to finish the game is included locally. Online functionality is optional."* Implicit in `DESIGN_DECISIONS.md` #010 (No External Dependencies) and the LLM mocking pattern, but not documented as a *player-experience* rule.

**Affected Files:**
- New file: `GDD/08_AI/02_Offline_First.md`
- Reference edits in: `docs/GAME_BIBLE.md`, `PROJECT_CONSTITUTION.md`, `docs/systems/ai_director.md`, `llm_bridge.py` design notes

**Options:**
1. **Strict Offline-First.** All quests, companions, endings, and progression paths function 100% offline. Optional AI-enhanced text (rumors, ambient talk) may connect online but degrades gracefully to a canned local pool.
2. Offline-First with syncable optional cloud features (achievements, save-sharing) — LLM strictly local-or-none.
3. Hybrid: core game offline; optional AI features require online.

**Pros:**
- **Option 1:** Matches owner directive precisely; supports the pillar; simplest QA story.
- Option 2: Adds cloud features later without breaking the pillar.
- Option 3: Cheapest to implement AI features.

**Cons:**
- Option 1: Requires a comprehensive local content pool for every AI enhancement so degradation is invisible.
- Option 2: Adds infrastructure that must be built and maintained.
- Option 3: Contradicts the pillar — offline players get a degraded experience.

**Your Recommendation:**
**Option 1.** Every AI enhancement ships with a local fallback pool. No feature blocks progress when offline.

**Impact if Accepted:**
- New doc `GDD/08_AI/02_Offline_First.md`.
- All future AI-enhancement docs must declare their local-fallback pool.
- `llm_bridge.py` architecture (and Godot equivalent) must support an "AI disabled" mode as first-class.

**Priority:** Critical.

---

### D-11 · AI Philosophy — Allowed vs Prohibited Uses

**Decision ID:** D-11
**Title:** Enumerate exactly which content may use AI enhancement and which content is handcrafted-only.
**Current Conflict:**
The owner's directive: *"AI enhances the game. It never replaces handcrafted content. Offline players receive the complete experience. Examples of optional AI: tavern gossip, ambient NPC conversations, campaign variation, dynamic rumors. No critical quest, companion, or ending should require AI."* Adjacent to `docs/lore/CANON_RULES.md` and the Project Evolution Plan prompt but never consolidated.

**Affected Files:**
- New file: `GDD/08_AI/01_AI_Philosophy.md`
- Reference edits in: `docs/GAME_BIBLE.md` Design Pillars, `docs/systems/ai_director.md`

**Options:**
1. **Adopt as canon.** Explicit allowed/prohibited list per the owner's directive.
2. Broader AI scope — allow AI-generated side quests within canon constraints.
3. Narrower AI scope — no AI in-game at all; use it only in development tooling.

**Pros:**
- **Option 1:** Matches owner directive precisely; the enumerated list is already usable.
- Option 2: Extends replayability via novel side content.
- Option 3: Absolute canonical safety.

**Cons:**
- Option 1: Requires enforcement discipline in future content.
- Option 2: Contradicts "AI never replaces handcrafted content" — side quests are content.
- Option 3: Contradicts the owner's explicitly listed examples of allowed AI enhancement.

**Your Recommendation:**
**Option 1.** Allowed uses: tavern gossip, ambient NPC conversations, dynamic rumors, campaign variation flavor text. Prohibited: main quests, companion recruitment, companion personal quests, endings, boss content, worldbuilding lore. All allowed uses must have a local-fallback pool per D-10.

**Impact if Accepted:**
- New doc `GDD/08_AI/01_AI_Philosophy.md`.
- `docs/systems/ai_director.md` referenced from the new doc.
- `llm_bridge.py` mock functions become the reference implementation for the allowed uses.

**Priority:** Critical.

---

### D-12 · Living World Simulation — Persistence Semantics (R9)

**Decision ID:** D-12
**Title:** Define the tick cadence and event-trigger model for the Living World simulation.
**Current Conflict:**
The Project Evolution Plan prompt establishes: *"The player should never feel like they are chatting with an AI. They should feel like they are exploring a world that continues to exist whether they are present or not."* Priority order for narrative: (1) World State (2) Rules (3) Existing Lore (4) NPC Memory. But no doc specifies the cadence — daily tick? hourly? travel-event only? event-driven only?

**Affected Files:**
- New file: `GDD/04_World/18_Living_World_Simulation.md`
- Reference edits in: `docs/systems/ai_director.md`, `docs/systems/world_regions.md`, `docs/systems/factions_economy.md`, `docs/systems/campaign_manager.md` (new)

**Options:**
1. **Daily-tick simulation.** World state advances one in-world day per major player action or travel segment.
2. **Event-driven simulation.** No fixed cadence; world state advances only when triggers fire (quest completion, region entry, tick threshold).
3. **Hybrid cadence.** Daily tick during travel; event-driven at settlements and dungeons.
4. **Hourly / fine-grained.** Overkill for a tactical RPG.

**Pros:**
- Option 1: Predictable pacing; easy to script world events (e.g., "3 days after ignoring the Frontier corruption, Mossroot territory silences another zone").
- Option 2: Efficient; only computes when needed.
- **Option 3:** Combines predictable pacing during exploration with responsive event-triggered changes at hubs — matches the two-layer exploration system.
- Option 4: High compute for little narrative gain.

**Cons:**
- Option 1: Can feel arbitrary if travel time doesn't match narrative pacing.
- Option 2: Harder for writers to reason about — "when does world X evolve?"
- Option 3: Two cadence rules to maintain and document.
- Option 4: Overhead.

**Your Recommendation:**
**Option 3 — Hybrid cadence.** Daily tick advances during overworld travel (matches Journey System's camp cadence). At settlements and inside dungeons, only event-driven changes fire (matches Settlement Dispersal / Dungeon crawl expectations).

**Impact if Accepted:**
- New doc `GDD/04_World/18_Living_World_Simulation.md`.
- `game_loop.py` (terminal) and Godot equivalent gain a `tick_scale` state variable.
- World event, faction, and economy managers must respect the tick_scale.

**Priority:** Critical.

---

### D-13 · Origin Characters — Implementation Model (R7)

**Decision ID:** D-13
**Title:** Define how every companion also functions as a playable Origin protagonist.
**Current Conflict:**
The owner's directive: *"Every companion is a companion, a playable Origin character, and an independent individual. When NPC: behavior evolves automatically. When Player Character: never force personality changes; unlock additional roleplaying choices while preserving player agency."* Not documented anywhere.

**Affected Files:**
- New file: `GDD/05_Companions/03_Player_System_and_Origin.md`
- Reference edits in: `docs/PLAYER_SYSTEM.md`, `docs/HERO_BIBLE.md`, `docs/CHARACTER_DESIGN_GUIDE.md`, every Hero Bible file

**Options:**
1. **Full Origin parity from Phase-1.** Every companion is a playable Origin at launch; all Hero Bibles include a "Playing as X" section.
2. **Staged Origin rollout.** VS-1 ships with Talos as the single Origin; Eleanor Origin at VS-2; others follow. Others remain companions-only until authored.
3. **Origin as post-launch feature.** Ship with a single Origin (Talos); other Origins come as content updates.
4. Do not adopt Origin Characters — keep the roster as companions only.

**Pros:**
- Option 1: Consistent player experience; maximum replayability from launch.
- **Option 2:** Manageable VS-1 scope; validates the Origin architecture with one implementation before scaling.
- Option 3: Cheapest VS-1.
- Option 4: Simplest.

**Cons:**
- Option 1: Massive Phase-1 scope; each Origin requires its own "Playing as" content across every scene.
- Option 2: Requires the Hero Bible template to reserve an Origin section for future authoring.
- Option 3: Loses the pillar's power for VS-1.
- Option 4: Contradicts direct owner directive.

**Your Recommendation:**
**Option 2 — Staged rollout.** VS-1 = Talos Origin. Every Hero Bible gets a template Origin section (empty for four, filled for Talos). All authored content assumes Talos POV for VS-1 but references future Origin variance in [PLANNED] callouts.

**Impact if Accepted:**
- New doc `GDD/05_Companions/03_Player_System_and_Origin.md`.
- `docs/HERO_BIBLE.md` and `docs/CHARACTER_DESIGN_GUIDE.md` extended with Origin design section.
- Every Hero Bible gets a template "Playing as X" section (Talos filled; others [PLANNED]).
- `docs/PLAYER_SYSTEM.md` Phase-1 clarifies "predefined roster of five, one Origin at VS-1 (Talos)."

**Priority:** High.

---

### D-14 · Companion Expertise System

**Decision ID:** D-14
**Title:** Formalize the out-of-combat contribution matrix per companion.
**Current Conflict:**
The owner's directive lists specific expertise per companion. No system doc exists.

**Expertise matrix per owner directive:**
- Talos: morale, leadership, helping children
- Torren: engineering, construction, repairs
- Eleanor: research, arcane study, teaching
- Corwin: tracking, foraging, corruption investigation [PLANNED per D-03]
- Ragash: preparing hunters, animal care, survival training
- Ronan: security, patrols, settlement defense
- Future Healer: medicine, community health, refugee care [PLANNED per D-03]

**Affected Files:**
- New file: `GDD/05_Companions/04_Companion_Expertise.md`
- Reference edits in every Hero Bible

**Options:**
1. **World-interaction based (per owner directive).** Expertise unlocks unique interactions with settlements, quests, and regions — never combat passives. Talos improves settlement morale over time; Torren repairs specific broken things; Eleanor's presence enables unique research options; etc.
2. Combat passive bonuses.
3. Both — expertise is world-interaction *and* mild combat passive.

**Pros:**
- **Option 1:** Matches owner directive verbatim; distinguishes companions in narrative content, not combat balance.
- Option 2: Simple to implement.
- Option 3: Flexibility.

**Cons:**
- Option 1: Requires per-companion authored expertise interactions in each settlement/region.
- Option 2: Direct contradiction — owner explicitly says "world interactions rather than combat passives."
- Option 3: Same contradiction as Option 2.

**Your Recommendation:**
**Option 1.**

**Impact if Accepted:**
- New doc `GDD/05_Companions/04_Companion_Expertise.md` with the seven-row matrix (five confirmed + two [PLANNED]).
- Each Hero Bible extended with "Expertise Interactions" section.
- Settlement authoring template (see D-16) includes an "Expertise hooks" section for each companion.

**Priority:** High.

---

### D-15 · Companion Evolution System

**Decision ID:** D-15
**Title:** Formalize the permanent behavior changes that follow completed personal quests.
**Current Conflict:**
The owner's directive: *"Completing companion quests permanently changes how companions behave. Examples: Ronan becomes more socially engaged after accepting his curse. Talos grows into a mentor. Corwin becomes more willing to trust others."* No system doc exists.

**Affected Files:**
- New file: `GDD/05_Companions/05_Companion_Evolution.md`
- Reference edits in every Hero Bible (Growth section)

**Options:**
1. **Discrete Evolution States.** Each companion has 2–3 named evolution states, unlocked by personal-quest milestones. Dialogue pool, camp behavior, and settlement dispersal shift per state.
2. Continuous scalar (loyalty → warmth) that gradually shifts behavior.
3. Both — discrete milestones + continuous loyalty tone.

**Pros:**
- **Option 1:** Legible; writers can author dialogue variants clearly per state; save schema is simple.
- Option 2: Fine-grained; feels organic.
- Option 3: Best of both.

**Cons:**
- Option 1: Feels stepwise.
- Option 2: Hard to author dialogue that reads well across a continuous slider.
- Option 3: Two systems to maintain.

**Your Recommendation:**
**Option 1 — Discrete Evolution States.** Each companion: pre-quest state → mid-quest state (after key milestone) → post-quest state. Save schema stores current state per companion. Dialogue Manager selects lines from the current-state pool.

**Impact if Accepted:**
- New doc `GDD/05_Companions/05_Companion_Evolution.md`.
- Every Hero Bible extended with "Evolution States" section (two or three states each).
- Save schema gains `world_state["companions"][name]["evolution_state"]` field.

**Priority:** High.

---

### D-16 · Settlement Dispersal System

**Decision ID:** D-16
**Title:** Define how the party disperses across a settlement so companions are always doing something appropriate.
**Current Conflict:**
The owner's directive: *"When entering safe settlements: the active party disperses. Every recruited companion appears somewhere appropriate in the settlement. Companions remain available for: conversation, party swapping, personal quests, story progression. They are never simply standing idle."* No doc exists.

**Affected Files:**
- New file: `GDD/05_Companions/06_Settlement_Dispersal.md`
- Related: `GDD/07_Systems/11_Settlement.md`, `docs/systems/journey_system.md`

**Options:**
1. **Curated Dispersal.** Each settlement authors a set of "companion appearance spots" tagged by expertise/personality (Talos → training ground / orphanage, Torren → forge, Eleanor → library / rooftop / archive, Ragash → kennels / stable, Ronan → guard post / patrol route). Each companion picks the most appropriate available spot on settlement entry.
2. **Procedural Dispersal.** Settlement declares tagged spots; companion has tag preferences; runtime picks by best-match score.
3. **Random Dispersal.** No curation; companions spawn at random tagged spots.

**Pros:**
- **Option 1:** Authored quality; every dispersal feels like a specific choice.
- Option 2: Scalable across many settlements.
- Option 3: Cheapest.

**Cons:**
- Option 1: Per-settlement authoring overhead.
- Option 2: Requires a tag ontology and scoring rules; can produce weird pairings early.
- Option 3: Feels arbitrary; contradicts "somewhere appropriate."

**Your Recommendation:**
**Option 1 with Option 2 as fallback.** Every VS-1 and Phase-3 settlement gets curated dispersal spots per companion. Later settlements may use the procedural fallback if authoring bandwidth is limited. Establishing a shared tag ontology from the start makes migration to procedural trivial later.

**Impact if Accepted:**
- New docs `GDD/05_Companions/06_Settlement_Dispersal.md` + `GDD/07_Systems/11_Settlement.md`.
- Settlement authoring template includes per-companion dispersal spot fields.
- `docs/systems/journey_system.md` cross-references the new doc.
- VS-1 settlement (Frontier trading post) needs five dispersal spots authored.

**Priority:** High.

---

## Section C — Technical / Architecture Decisions

### D-17 · Player State Canonicality (R4 / BUG-002)

**Decision ID:** D-17
**Title:** Resolve the `player.py` singleton vs `world_state["player"]` divergence.
**Current Conflict:**
`DESIGN_DECISIONS.md` #007 marks this as UNRESOLVED. Combat reads from `player.py` singleton; save/load operates on `world_state["player"]`. Stats can silently desync after level-up or equipment change.

**Affected Files:**
- `player.py`, `world_state.py`, `combat.py`, `save_manager.py`, `state_manager.py`
- `DESIGN_DECISIONS.md` #007
- `docs/known_issues.md` BUG-002
- `docs/systems/world_state.md`

**Options:**
1. **`world_state["player"]` is canonical.** Retire `player.py` singleton. Combat reads/writes directly from world_state.
2. **`player.py` is canonical.** Retire the `world_state["player"]` section; save/load pulls from the singleton.
3. **Proxy pattern.** `player.py` becomes a thin view over `world_state["player"]` — same object, single storage.
4. Defer to the Godot rewrite (no fix in the terminal prototype).

**Pros:**
- Option 1: Aligns with the "world_state is single source of truth" pillar. Godot port becomes trivial.
- Option 2: Keeps combat code untouched.
- **Option 3:** Zero call-site changes; existing code keeps working; single storage.
- Option 4: No terminal work.

**Cons:**
- Option 1: Combat code refactor.
- Option 2: Violates the world_state single-source pillar.
- Option 3: Slight indirection.
- Option 4: Prolongs the divergence; contradicts the pillar.

**Your Recommendation:**
**Option 3 (near-term) + Option 1 (Godot).** In the terminal prototype, retrofit `player.py` as a proxy over `world_state["player"]` — closes BUG-002 without churn. In the Godot port, adopt Option 1 natively (no singleton; direct world_state access).

**Impact if Accepted:**
- Terminal: ~30-line refactor of `player.py` to a proxy.
- Godot: canonical player state = `world_state["player"]`.
- `DESIGN_DECISIONS.md` #007 status changes from UNRESOLVED → RESOLVED (Option 3 near-term / Option 1 Godot).
- BUG-002 closes.

**Priority:** High.

---

### D-18 · Legacy Modules Disposition (R5)

**Decision ID:** D-18
**Title:** Rule on the fate of `factions.py`, `regions.py`, `loot.py`, `memory.py`.
**Current Conflict:**
`DESIGN_DECISIONS.md` #009 flags these as retained-but-deprecated. They coexist with their manager successors (`faction_manager.py`, `region_manager.py`, `loot_manager.py`, `memory_engine.py`).

**Affected Files:**
- `factions.py`, `regions.py`, `loot.py`, `memory.py` (source)
- `DESIGN_DECISIONS.md` #009
- `docs/known_issues.md`
- `docs/architecture.md`

**Options:**
1. **Archive now.** Move to `docs/archive/legacy/` immediately (per prior report).
2. **Archive at the Godot boundary.** Leave in terminal; do not port to Godot.
3. Delete outright.
4. Keep indefinitely.

**Pros:**
- Option 1: Clean now; simplifies onboarding.
- **Option 2:** Zero terminal-side churn; natural cutover at the Godot rewrite.
- Option 3: Cleanest.
- Option 4: No work.

**Cons:**
- Option 1: Risk of missing an import (though `AI_START_HERE.md` states nothing imports them).
- Option 2: Continues confusion in terminal for a while longer.
- Option 3: Loses historical reference.
- Option 4: Continues to pollute.

**Your Recommendation:**
**Option 2 — Archive at the Godot boundary.** In terminal, add explicit deprecation notices to the top of each file. In Godot, they are simply not ported. Files move to `docs/archive/legacy/` when the terminal prototype is frozen.

**Impact if Accepted:**
- ~4 deprecation-notice edits in terminal.
- `docs/architecture.md` updates to include a "Deprecated modules" section.
- Godot port ignores these files.

**Priority:** Low.

---

### D-19 · Custom Hero Phase-2 — Hard Defer Confirmation (R6)

**Decision ID:** D-19
**Title:** Confirm that Custom Hero is deferred out of VS-1 and Phase-2.
**Current Conflict:**
`docs/PLAYER_SYSTEM.md` and `DESIGN_DECISIONS.md` #016 both defer Custom Hero to Phase-2 (no design yet). VS-1 planning must know whether this is still the case.

**Affected Files:**
- `docs/PLAYER_SYSTEM.md`
- `DESIGN_DECISIONS.md` #016

**Options:**
1. **Hard defer.** Custom Hero is out of VS-1 and Phase-2. Reconsidered only after Origin Characters (D-13) is complete.
2. Soft defer with early architecture work — build hero-identity data-driven so Custom Hero fits without rewrite.
3. Include Custom Hero in Phase-2 scope.

**Pros:**
- **Option 1:** Simplest scope. Origin Characters + five confirmed companions is already a large surface.
- Option 2: Keeps the door open architecturally.
- Option 3: Answers "I want to make my own hero" from day 1.

**Cons:**
- Option 1: Later Custom Hero implementation may still need a data-model retrofit.
- Option 2: Discipline required to keep hero identity data-driven.
- Option 3: Doubles the content authoring surface.

**Your Recommendation:**
**Option 1, with Option 2's discipline.** Custom Hero deferred; hero identity is data-driven from the start (this is *already* the discipline `DESIGN_DECISIONS.md` #016 mandates), so Custom Hero fits later without rewrite.

**Impact if Accepted:**
- `docs/PLAYER_SYSTEM.md` gets a "Phase-3+" annotation on Custom Hero (moved from Phase-2).
- `DESIGN_DECISIONS.md` #016 amended.

**Priority:** Medium.

---

### D-20 · AI Enhancement Scope in Godot Prototype (R8)

**Decision ID:** D-20
**Title:** Decide whether the Godot VS-1 ships with mocked LLM (like the terminal) or with a real optional LLM layer.
**Current Conflict:**
The terminal prototype has all LLM calls mocked. The problem statement establishes AI as optional. VS-1 could ship with either mocked LLM or a real one.

**Affected Files:**
- New `GDD/02_Prototype/02_Godot_Prototype_Plan.md`
- `docs/systems/ai_director.md`
- `llm_bridge.py` Godot equivalent

**Options:**
1. **VS-1 ships with mocked LLM only.** All AI-enhancement outputs come from the local fallback pool. Real LLM integration is a post-VS-1 opt-in feature.
2. VS-1 ships with mocked LLM + optional real LLM behind a hidden dev flag.
3. VS-1 ships with a real LLM as default; offline players get the mock.

**Pros:**
- **Option 1:** Zero external dependency risk for VS-1; validates the Offline-First pillar; simplest QA.
- Option 2: Devs can playtest real AI without shipping it.
- Option 3: Showcases the AI pillar.

**Cons:**
- Option 1: VS-1 does not exercise the real-LLM path.
- Option 2: Adds a dev-flag surface that must be maintained.
- Option 3: Introduces LLM cost + API keys + network latency into VS-1 QA.

**Your Recommendation:**
**Option 1.** VS-1 validates loop, feel, and architecture. Real LLM opt-in becomes a Phase-4 feature.

**Impact if Accepted:**
- Godot `llm_bridge` equivalent implemented as mock-only for VS-1.
- Real-LLM integration doc deferred to Phase-4.
- Offline-First pillar validated by construction.

**Priority:** Medium.

---

### D-21 · Dialogue Framework Tool Choice (RISK-5)

**Decision ID:** D-21
**Title:** Choose the dialogue authoring/runtime tool for Godot.
**Current Conflict:**
Godot has multiple mature dialogue tools. Picking late causes content rewrites. No decision documented.

**Affected Files:**
- New `GDD/07_Systems/09_Dialogue.md`
- All VS-1 dialogue authoring (Talos recruitment, Mossroot first-contact, boss dialogue)

**Options:**
1. **Dialogic (Godot addon).** Popular, mature, free, GDScript-native.
2. **Custom dialogue system built on Godot Resources.** Full control, matches project data-driven aesthetic.
3. **Ink (via inkgd).** Text-first branching narrative language.
4. **Yarn Spinner (via Godot port).** Familiar dialogue graph tooling.

**Pros:**
- Option 1: Fastest to author; visual editor.
- Option 2: Full control; deep integration with world_state / event_bus; no external addon churn.
- Option 3: Text-first; version-control friendly; excellent branching semantics.
- Option 4: Familiar to writers.

**Cons:**
- Option 1: External addon; may not deeply integrate with world_state.
- Option 2: More implementation work up front.
- Option 3: Requires an integration layer between Ink and world_state.
- Option 4: Godot port maturity varies; external tooling.

**Your Recommendation:**
**Option 2 — Custom system built on Godot Resources.** Rationale: (a) dialogue conditions must query world_state (companion presence, evolution state, faction reputation, quest flags), (b) the AI-optional layer per D-11 requires deep hooks, (c) Origin Character variants per D-13 require branching that responds to who the player is, (d) Companion Evolution states per D-15 must swap dialogue pools. All of this is fragile through an external addon. A custom Resource-based system is ~1 week of engineering and eliminates the addon dependency.

**Impact if Accepted:**
- New doc `GDD/07_Systems/09_Dialogue.md`.
- One custom Godot Resource type (`DialogueNode`) + one runtime (`DialogueRunner`).
- VS-1 dialogue authored in Godot Resource format from the start.

**Priority:** High.

---

## Section D — VS-1 Scope Decisions

### D-22 · VS-1 Region Selection

**Decision ID:** D-22
**Title:** Confirm The Frontier as the VS-1 region.
**Current Conflict:**
The audit recommends The Frontier as VS-1 region because: Corruption arrives there first, goblin tribes are located there, and it has the most authored content (three tribe quests + one first-contact encounter). No alternative has been formally considered.

**Affected Files:**
- `GDD/02_Prototype/02_Godot_Prototype_Plan.md` (new)
- All VS-1 content docs (settlement, dungeon, boss)

**Options:**
1. **The Frontier.**
2. The Great Forest.
3. The Iron Peaks.
4. The Frozen Highlands.
5. The Desert Kingdom (Sol Kareth).
6. The Capital Province.

**Pros/Cons:** The audit ranked all six; The Frontier scored highest for VS-1 (content depth, thematic alignment with Corruption pillar, tone match with Talos recruitment).

**Your Recommendation:**
**Option 1 — The Frontier.**

**Impact if Accepted:**
- VS-1 scoping documents lock The Frontier.
- Existing authored content (`docs/quests/goblin_tribe_quests.md`, `docs/encounters/mossroot_first_contact.md`) becomes VS-1 canonical.

**Priority:** Critical (blocks VS-1 authoring).

---

### D-23 · VS-1 Origin / Recruitment Choice

**Decision ID:** D-23
**Title:** Confirm Talos as the VS-1 Origin Character and first recruit.
**Current Conflict:**
Per D-13, VS-1 ships with one Origin. Talos is recommended: earliest tone canon (mentor), lowest romance/narrative risk, easiest to test, does not depend on Torren-related crafting (which D-14 defers).

**Affected Files:**
- `GDD/05_Companions/heroes/TALOS.md` (Origin section)
- VS-1 scripting content

**Options:**
1. **Talos.**
2. Eleanor (arc-heavy — Fractured Circle).
3. Ragash (partial arc authored).
4. Ronan (Hidden Pack authored).
5. Torren (crafting dependency).

**Pros/Cons:**
- Option 1: Lowest content debt; already-authored recruitment tone (`docs/game_tone.md`).
- Option 2: Fractured Circle is the most-developed arc, but expensive to fully script.
- Options 3–5: Each requires additional authoring.

**Your Recommendation:**
**Option 1 — Talos.**

**Impact if Accepted:**
- Talos Origin fully authored in Hero Bible.
- Other Origins remain [PLANNED] until Phase-3+.

**Priority:** Critical.

---

### D-24 · VS-1 Questline Choice

**Decision ID:** D-24
**Title:** Confirm the Mossroot questline (*What the Forest Carries*) as the VS-1 major questline.
**Current Conflict:**
The audit recommends this because: (a) an authored first-contact encounter exists (`docs/encounters/mossroot_first_contact.md`), (b) the full 5-stage quest is written (`docs/quests/goblin_tribe_quests.md`), (c) it thematically fits the Frontier + Corruption + hollow-game motif, (d) it does not require multi-companion narratives.

**Affected Files:**
- `GDD/06_Story/04_Quests.md` VS-1 reference
- Existing quest doc becomes VS-1 canonical script source

**Options:**
1. **Mossroot — *What the Forest Carries*.**
2. Stonefang — *The Debt Comes Due*.
3. Ashfire — *Smoke and Terms*.
4. Religious order quest (Covenant / Old Ways / Ancestors' Path / Veiled Order).
5. Eleanor's Fractured Circle arc.

**Pros:**
- Option 1: Most complete authored content; fits Talos recruit; matches Frontier region.
- Options 2 + 3: Also Frontier; less first-contact content pre-authored.
- Option 4: Religious quests are largely metropolis-based (Capital) — mismatched with Frontier.
- Option 5: Companion-heavy; requires Eleanor recruited first — conflicts with D-23.

**Your Recommendation:**
**Option 1 — Mossroot: *What the Forest Carries*.**

**Impact if Accepted:**
- VS-1 quest fully scripted from existing content.
- Other questlines remain authored-but-not-scripted content available for Phase-3.

**Priority:** Critical.

---

### D-25 · VS-1 Dungeon Design Approach

**Decision ID:** D-25
**Title:** Author a small (3–5 room) dungeon tied to the Mossroot questline.
**Current Conflict:**
No dungeon is authored in the repo. `dungeon_manager.py` has only `run_dungeon(id)`. VS-1 needs one dungeon that fits the Mossroot arc.

**Affected Files:**
- New: `GDD/06_Story/authored/mossroot_ruin.md` (or equivalent)
- New: `GDD/03_Core_Gameplay/09_Dungeon_System.md`

**Options:**
1. **Corrupted watchtower in Mossroot territory.** 3–5 rooms; corruption VFX; small mob encounters; one mini-boss room. Setting fits the "hollow game silence" motif.
2. Ancient buried ruin (First-Age adjacent) — feels too Architects-related.
3. Larger 6–10 room dungeon.

**Pros:**
- **Option 1:** Matches motif; scope realistic for VS-1.
- Option 2: Risk of over-explaining Architects (canon violation).
- Option 3: Scope creep.

**Your Recommendation:**
**Option 1 — Corrupted watchtower.** Also requires a small Dungeon System doc (§VS-5 Important item).

**Impact if Accepted:**
- New authored dungeon doc + new Dungeon System doc.
- VS-1 dungeon phase scoped.

**Priority:** Critical.

---

### D-26 · VS-1 Boss Design Approach

**Decision ID:** D-26
**Title:** Author one named boss for the VS-1 dungeon.
**Current Conflict:**
Zero named bosses are canonized. `bosses.py` provides only phase-check logic. VS-1 needs one.

**Affected Files:**
- New: `GDD/06_Story/authored/vs1_boss.md`

**Options:**
1. **Corruption-tainted alpha (of the "hollow game" already referenced in `docs/world/goblin_tribes.md`).** Larger corrupted wolf/predator. Two phases: aggressive → corrupted-final-form. Environmental storytelling: the beast was once ordinary. Dialogue: none (defeated by presence, not speech).
2. Corrupted goblin warlord.
3. Ancient Architect construct (canon-risky).
4. Vampire assassin (mismatch with Frontier / dungeon).

**Pros:**
- **Option 1:** Perfect motif match; already referenced in canon; no invention required.
- Option 2: Contradicts D-24 (Mossroot's arc is not about killing goblins).
- Option 3: Canon risk (Architects rules).
- Option 4: Faction mismatch.

**Your Recommendation:**
**Option 1 — Corruption-tainted alpha.**

**Impact if Accepted:**
- One authored boss doc.
- Boss combat implementation exercises the two-phase system in `bosses.py`.

**Priority:** Critical.

---

### D-27 · Godot Save Format

**Decision ID:** D-27
**Title:** Choose the Godot-side save format.
**Current Conflict:**
Terminal uses JSON + manager dicts. Godot has native Resource serialization (`.tres`, `.res`), plus JSON, plus binary options. Choice must be made before D-17's canonical player state is implemented in Godot.

**Affected Files:**
- New: `GDD/02_Prototype/03_Save_Schema_for_Godot.md`

**Options:**
1. **JSON (portable, human-readable, matches terminal).** Godot's `JSON.stringify` on a dictionary; easy migration from terminal.
2. Godot Resource files (`.tres`) — native, typed, editor-friendly.
3. Binary (`.res`) — smallest; opaque.
4. SQLite — overkill.

**Pros:**
- **Option 1:** Direct migration from terminal; save-inspection stays easy; version-control friendly.
- Option 2: Type safety; native editor integration.
- Option 3: Compact.

**Cons:**
- Option 1: No native typing.
- Option 2: Requires all game data as Resources — larger refactor.
- Option 3: Debug pain.
- Option 4: Massive dependency.

**Your Recommendation:**
**Option 1 — JSON.** Matches terminal, matches Offline-First simplicity, easy to migrate save files across versions with `ensure_world_state_defaults()`-equivalent Godot autoload logic.

**Impact if Accepted:**
- Godot `SaveManager` autoload writes/reads JSON.
- Terminal saves can be inspected as reference during Godot dev.
- Version migration in Godot mirrors the terminal pattern.

**Priority:** High.

---

## Section E — Documentation Cleanup Decisions

### D-28 · AI Continuation Guide — Add Lore Bible

**Decision ID:** D-28
**Title:** Update `docs/AI_CONTINUATION_GUIDE.md` to reference the Lore Bible as top-priority reading.
**Current Conflict:**
`LORE_CONSISTENCY_AUDIT.md` ❌ #2 and ⚠ #6 both flag this. The Lore Bible (`docs/lore/`) does not appear in the AI Continuation Guide's priority reading list, causing new AI sessions to miss immutable canon.

**Affected Files:**
- `docs/AI_CONTINUATION_GUIDE.md`

**Options:**
1. **Add Lore Bible top-of-list.** New entries: `docs/lore/README.md`, `docs/lore/CANON_RULES.md`, `docs/lore/DEVELOPMENT_REFERENCE.md`, `docs/lore/HISTORY_BIBLE.md`, `docs/lore/TIMELINE.md` — placed above `docs/GAME_BIBLE.md`.
2. Do nothing.

**Pros/Cons:** Option 1: Prevents future sessions from missing canon.

**Your Recommendation:**
**Option 1.**

**Impact if Accepted:**
- ~5-row table addition.
- `LORE_CONSISTENCY_AUDIT.md` ❌ #2 and ⚠ #6 close.

**Priority:** High.

---

### D-29 · LORE_CONSISTENCY_AUDIT.md — Retain or Supersede

**Decision ID:** D-29
**Title:** Decide what happens to the July-2026 lore audit now that its findings are being resolved.
**Current Conflict:**
The audit is a valuable artifact but partially outdated (§3.1's Version-C ruling closes multiple findings). Leaving it as-is is misleading; deleting it destroys history.

**Affected Files:**
- `LORE_CONSISTENCY_AUDIT.md`

**Options:**
1. **Retain with a resolution appendix.** Add a "Resolutions — January 2026" appendix at the end pointing each finding to its ruling (D-01 to D-08) or explaining why it remains open. Keep the audit body untouched.
2. Rewrite the audit against current canon.
3. Move to `docs/archive/` — retain but hide.

**Pros:**
- **Option 1:** Preserves history; makes the audit useful again immediately; zero content rewriting.
- Option 2: Cleanest end state but destroys historical provenance.
- Option 3: Historical retention but harder to find.

**Your Recommendation:**
**Option 1.**

**Impact if Accepted:**
- ~1-page appendix added to `LORE_CONSISTENCY_AUDIT.md`.
- Audit remains root-level and useful.

**Priority:** Low.

---

### D-30 · attached_assets/ — Retain in Place vs Archive

**Decision ID:** D-30
**Title:** Decide the fate of the 45 `attached_assets/*.txt` prompt snapshots.
**Current Conflict:**
These are historical prompts that authored the canon layer-by-layer. Some are still directly cited (the recent Four-Age directive, the Living World Simulation prompt). Others are superseded.

**Affected Files:**
- `attached_assets/*.txt` (45 files)
- New: `attached_assets/INDEX.md` (audit-recommended)

**Options:**
1. **Retain in place + add an `INDEX.md`** that maps each prompt to the canon layer it introduced (or "superseded by …").
2. Move all to `docs/archive/prompts/` with an index.
3. Delete superseded prompts.

**Pros:**
- **Option 1:** Preserves the trail; adds an index for navigation; nothing lost.
- Option 2: Cleaner root but breaks any existing cross-references.
- Option 3: Loses historical trail.

**Your Recommendation:**
**Option 1.**

**Impact if Accepted:**
- New `attached_assets/INDEX.md` authored.
- No file movement.

**Priority:** Low.

---

## Section F — Summary Table

Total decisions requiring ruling: **30**.

| # | ID | Priority | Category | Recommendation Shorthand |
|---|---|---|---|---|
| 1 | D-01 | Critical | Canon/Lore | Adopt Four-Age Version C |
| 2 | D-02 | Critical | Canon/Lore | Sanctuary-Delivered Truth |
| 3 | D-03 | Critical | Canon/Lore | Defer Corwin + Healer as [PLANNED] |
| 4 | D-04 | High | Canon/Lore | Attribute to full Chorus / First Song |
| 5 | D-05 | High | Canon/Lore | Two-tier terminology (dev vs in-world) |
| 6 | D-06 | Medium | Canon/Lore | Reframe as Eighth-specific |
| 7 | D-07 | Medium | Canon/Lore | Physical-world influence only |
| 8 | D-08 | Low | Canon/Lore | Singular Great Library |
| 9 | D-09 | Critical | Design Pillar | Difficulty by Choice canonized |
| 10 | D-10 | Critical | Design Pillar | Strict Offline-First |
| 11 | D-11 | Critical | Design Pillar | Allowed vs prohibited AI list |
| 12 | D-12 | Critical | Design Pillar | Hybrid cadence (daily-tick travel / event-driven hubs) |
| 13 | D-13 | High | Design Pillar | Staged Origin rollout (Talos VS-1) |
| 14 | D-14 | High | Companion Sys | World-interaction expertise (no combat passives) |
| 15 | D-15 | High | Companion Sys | Discrete evolution states |
| 16 | D-16 | High | Companion Sys | Curated dispersal (procedural fallback later) |
| 17 | D-17 | High | Tech/Arch | Proxy pattern near-term / world_state canonical in Godot |
| 18 | D-18 | Low | Tech/Arch | Archive at Godot boundary |
| 19 | D-19 | Medium | Tech/Arch | Hard defer Custom Hero |
| 20 | D-20 | Medium | Tech/Arch | Mocked LLM only in VS-1 |
| 21 | D-21 | High | Tech/Arch | Custom Resource-based dialogue |
| 22 | D-22 | Critical | VS-1 Scope | The Frontier |
| 23 | D-23 | Critical | VS-1 Scope | Talos |
| 24 | D-24 | Critical | VS-1 Scope | Mossroot questline |
| 25 | D-25 | Critical | VS-1 Scope | Corrupted watchtower dungeon |
| 26 | D-26 | Critical | VS-1 Scope | Corruption-tainted alpha boss |
| 27 | D-27 | High | Tech/Arch | JSON save format |
| 28 | D-28 | High | Doc Cleanup | Add Lore Bible to AI Continuation Guide |
| 29 | D-29 | Low | Doc Cleanup | Retain audit + add resolution appendix |
| 30 | D-30 | Low | Doc Cleanup | Retain attached_assets + add INDEX |

---

## Section G — Recommended Implementation Sequence

Once every decision above has a ruling, work proceeds in the following strict order. **No step begins until the previous step's exit criteria are met.**

### Phase 1 — Final Canon Decisions

**What:** Owner reviews this document and rules on all 30 decisions.
**Deliverable:** `FINAL_CANON_DECISIONS.md` returned with a ruling next to every decision.
**Exit criteria:** Zero open canon or architectural decisions remain.
**No repository modifications yet.**

### Phase 2 — Repository Consolidation

**What:** Apply every ruling to the repository per `CONSOLIDATION_REPORT.md` §5 (folder structure) + §6 (implementation order).

**Steps in order:**
1. Snapshot `/app/docs/`, `/app/elyndor/`, root docs to `docs/archive/pre-consolidation-2026-01/`.
2. Move the three ZIPs to `docs/archive/snapshots/` + write `ARCHIVE_INDEX.md`.
3. Create `/app/GDD/` scaffold with `00_Index.md` and `00_Rationale_Log.md`.
4. Fix in-place broken references (D-01, D-05, D-06, D-07, D-08, D-28).
5. Apply the Primordial Magic + terminology reworks (D-04, D-05).
6. Populate `GDD/*` link files (per §5 of the report).
7. Add the resolution appendix to `LORE_CONSISTENCY_AUDIT.md` (D-29).
8. Author `attached_assets/INDEX.md` (D-30).
9. Add deprecation notices to legacy modules (D-18).

**Exit criteria:** Every stale reference is corrected; every consolidation edit is logged in `GDD/00_Rationale_Log.md`; the `GDD/` folder is a navigable index of the entire repo.

### Phase 3 — Creation of Missing Critical Documents

**What:** Author every doc marked Critical in Part II §VS-5.

**Documents authored (in order):**
1. `GDD/03_Core_Gameplay/07_Difficulty_Philosophy.md` (D-09)
2. `GDD/08_AI/02_Offline_First.md` (D-10)
3. `GDD/08_AI/01_AI_Philosophy.md` (D-11)
4. `GDD/04_World/18_Living_World_Simulation.md` (D-12)
5. `GDD/05_Companions/03_Player_System_and_Origin.md` (D-13)
6. `GDD/05_Companions/04_Companion_Expertise.md` (D-14)
7. `GDD/05_Companions/05_Companion_Evolution.md` (D-15)
8. `GDD/05_Companions/06_Settlement_Dispersal.md` (D-16)
9. `GDD/07_Systems/09_Dialogue.md` (D-21)
10. `GDD/07_Systems/14_Corruption_System.md` (mechanical companion to lore doc)
11. `GDD/03_Core_Gameplay/09_Dungeon_System.md` (D-25 support)
12. `GDD/07_Systems/11_Settlement.md` (D-16 support)
13. `GDD/02_Prototype/01_Godot_Scene_Architecture.md`
14. `GDD/02_Prototype/02_Godot_Data_Model.md`
15. `GDD/02_Prototype/03_Save_Schema_for_Godot.md` (D-27)
16. `GDD/02_Prototype/04_Godot_Prototype_Plan.md` (D-20, D-22, D-23, D-24)

**Deliverable:** Every VS-1 pre-flight doc exists and cross-references the consolidated GDD structure.
**Exit criteria:** No blocking documentation gaps remain for the Godot phase.

### Phase 4 — Godot Project Architecture

**What:** Set up the Godot project and validate the architecture with two spikes.

**Steps in order:**
1. Init Godot project per `01_Godot_Scene_Architecture.md`.
2. Import placeholder asset packs per Part II §VS-4.
3. Implement `world_state` autoload per `02_Godot_Data_Model.md`.
4. Implement `SaveManager` autoload per `03_Save_Schema_for_Godot.md` (D-27).
5. Implement `event_bus` autoload.
6. Implement `player.py` proxy pattern → Godot-native world_state access (D-17).
7. **Combat Spike:** single hero, single enemy, single tile, one MP, one AP — validates the canonical combat model (RISK-2).
8. **Dialogue Spike:** one branching conversation using custom Resource-based dialogue (D-21).
9. Author the VS-1 content docs authored in Phase 3 or later:
   - Frontier trading post (settlement)
   - Corrupted watchtower (dungeon)
   - Talos Origin recruitment scene
   - Corruption-tainted alpha (boss)

**Exit criteria:** Godot project builds; combat + dialogue spikes are playable; VS-1 content docs complete; two spikes validate the architecture.

### Phase 5 — Vertical Slice Implementation

**What:** Assemble the full VS-1 playable loop in Godot.

**Steps in order (parallel work allowed within a step):**
1. Frontier region playable (traverse + encounter zones).
2. Trading-post settlement playable (dispersal system spawns Talos; NPCs interact; expertise hooks activate).
3. Talos recruitment scene functional.
4. Mossroot questline scripted (5 stages + first-contact encounter).
5. Corrupted watchtower dungeon playable (3–5 rooms + corruption VFX + boss room).
6. Boss encounter functional (Corruption-tainted alpha with two phases).
7. Save/load full-loop verified (mid-quest save + reload + resume).
8. HUD + Inventory + minimal UI functional.
9. AI Director layer active (mocked LLM per D-20).
10. Playtest pass 1 → fix regressions → playtest pass 2.

**Exit criteria:** A player can start the game, enter the Frontier, arrive at the trading post, recruit Talos, accept the Mossroot questline, travel to Mossroot territory, resolve first-contact, explore the corrupted watchtower, defeat the boss, save, reload, and continue — all in Godot, no missing systems, no scope debt.

---

## Section H — Awaiting Rulings

**No repository modifications made.** Every decision above waits for your ruling before consolidation begins. Reply with rulings inline, or provide alternatives per any decision.

**Recommended reply format:**

```
D-01: APPROVED per recommendation
D-02: APPROVED per recommendation
D-03: Alternative — canonize Corwin as companion #6; defer Future Healer as [PLANNED]
D-04: APPROVED per recommendation
...
```

Once every decision is ruled, consolidation will proceed exactly per Section G.

*End of decision document.*
