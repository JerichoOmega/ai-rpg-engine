# Lore Consistency Audit

> **Audit Date:** July 2026  
> **Auditor:** Replit Agent  
> **Canonical Authority:** `docs/lore/` — all nine files  
> **Scope:** Full repository — source code, documentation, design documents, quest content, companion content, world-building documents, history documents, magic system, NPC descriptions, AI continuation guide, code comments  
> **Method:** Read-only review. No files were modified.

---

## How to Read This Report

- **✔ Fully Consistent** — aligned with the Lore Bible; no action required
- **⚠ Minor Inconsistency** — small wording, terminology, or framing issues worth correcting eventually
- **❌ Major Conflict** — direct contradiction with the Lore Bible's immutable principles; review before any further content work that touches these files
- **💡 Suggestion** — environmental storytelling opportunity that would better reinforce established world philosophy; recommendations only

---

## ✔ Fully Consistent

The following files were reviewed and found to be fully aligned with the Lore Bible:

| File | What Was Checked | Finding |
|---|---|---|
| `docs/lore/` (all 9 files) | Internal consistency | All files consistent with each other |
| `elyndor/history/the_corruption.md` | Corruption as amplified virtue; Stage IV justification mechanism; Chorus not credited with causing it | Clean |
| `elyndor/history/the_eighth.md` | Naming conventions; Five Stages; Sundering canonical term; mysteries preserved | Clean (one minor issue — see ⚠ #9) |
| `docs/world/WORLD_BIBLE.md` | Chosen races; divine bloodlines; Chorus political involvement; race descriptions | Clean |
| `docs/world/religions.md` | Chorus framed as steward not ruler; cult theology framed as mortal belief not canonical fact; no chosen-hero claims | Clean |
| `docs/world/cults.md` | "Chosen" language correctly framed as false cult belief; imprisoned god's whispers framed as manipulation | Clean |
| `docs/world/goblin_tribes.md` | Goblins as intelligent peoples; no chosen-race language | Clean |
| `docs/world/vampire_houses.md` | Houses as mortal political actors; no Chorus involvement in their rise | Clean |
| `docs/world/covenant_inquisitors.md` | Inquisitors shown as Corruption-amplified, not divinely endorsed | Clean |
| `docs/CAMPAIGN_DESIGN.md` | Player not chosen; Corruption as amplified virtue; Chorus's impossible choice framed correctly | Clean |
| `docs/GAME_BIBLE.md` (Lore Design Philosophy) | Five rules compatible with Lore Bible | Clean |
| `docs/GAME_BIBLE.md` (Race descriptions) | "Not every dwarf enjoys mining" — explicitly states personality not determined by ancestry | Clean |
| `docs/GAME_BIBLE.md` (Lore Bible ToC #47–56) | New lore files correctly listed | Clean |
| `docs/heroes/ELEANOR.md` (Harmonic Soul framing) | Explicitly states "it does not make Eleanor the chosen one"; gods "cannot grant or revoke" her nature | Conditionally clean — see ❌ #4 |
| `elyndor/magic/MAGIC_BIBLE.md` (Seven Elemental Aspects) | Seven stewards and their domains consistent with Chorus as stewards, not creators | Clean |
| `elyndor/magic/MAGIC_BIBLE.md` (Two Approaches section) | Guild vs. religious tension correctly framed | Clean |
| `elyndor/magic/MAGIC_BIBLE.md` (Corruption section) | Consistent with the_corruption.md | Clean |
| `docs/heroes/TALOS.md` | Military background; institutional disillusionment; no chosen-one framing | Clean |
| `docs/heroes/RAGASH.md` | No divine bloodline or chosen-race framing | Clean |
| `docs/heroes/RONAN.md` | Curse framed as natural phenomenon, not divine selection | Clean |
| `docs/heroes/TORREN.md` | No divine framing; ordinary background | Clean |
| `docs/quests/religious_order_quests.md` | Quest hooks compatible with canon; Chorus not directing players | Clean |
| `docs/quests/goblin_tribe_quests.md` | No canon violations found | Clean |
| `docs/encounters/religious_encounters.md` | Pilgrimage and shrine content compatible with Chorus philosophy | Clean |
| `docs/systems/dynamic_story_arcs.md` | Arc framework respects handcrafted-first; Corruption as amplifier | Clean |
| `docs/systems/journey_system.md` | Companion bonds as Corruption resistance is thematically consistent | Clean |
| `docs/HERO_BIBLE.md` | Core Wound system compatible with "heroes made through choices" | Clean |
| `docs/PLAYER_SYSTEM.md` | Hero selection; no chosen-one language | Clean |
| `docs/world/RACES.md` | Race philosophy compatible with "no chosen races" | Clean |

---

## ❌ Major Conflicts

These are direct contradictions with the Lore Bible's immutable principles. Review before any further content work that touches these files.

---

### ❌ 1 — Historical Framework Mismatch

**File:** `elyndor/history/HISTORY_BIBLE.md`  
**Location:** Line 12 (header statement); entire document structure  

**What it says:**
> "The history of Elyndor is divided into **four ages**, each with a distinct identity, defining events, and long-term consequences."

The document is structured entirely around:
- First Age — The Age of Creation
- Second Age — The Age of Kingdoms
- Third Age — The Age of Wars
- Fourth Age — The Age of Shadows (present)

**What the Lore Bible says:**  
`docs/lore/HISTORY_BIBLE.md` (confirmed July 2026, revised to Seven Ages) and `docs/lore/TIMELINE.md` establish the canonical framework as:
1. Age of Awakening
2. Age of Discovery
3. Age of Unity
4. The Long Decline
5. The Sundering
6. Age of Restoration
7. Present Age

**Why this matters:**  
`elyndor/history/HISTORY_BIBLE.md` is the primary technical history document cross-referenced by `docs/world/WORLD_BIBLE.md`, `elyndor/magic/MAGIC_BIBLE.md`, `docs/heroes/TALOS.md`, `docs/world/vampire_houses.md`, and `docs/world/religions.md`. Any content created using this document as reference will use an obsolete framework structurally incompatible with the canonical seven ages.

**Context:**  
`docs/lore/HISTORY_BIBLE.md` includes a revision note: "Major revision — Seven-Age framework replaces Four-Age framework." The intent to supersede exists. The `elyndor/history/HISTORY_BIBLE.md` file was never updated to reflect this.

**Recommended correction:**  
Update `elyndor/history/HISTORY_BIBLE.md` to align with the Seven Ages framework established in `docs/lore/HISTORY_BIBLE.md`. The existing document contains valuable content (the Talos military connection, vampire house Third Age expansion, specific regional histories) that should be preserved and mapped to the correct age. This is a substantive revision requiring deliberate authoring, not a find-and-replace.

---

### ❌ 2 — AI Continuation Guide Lists Obsolete Framework as Current

**File:** `docs/AI_CONTINUATION_GUIDE.md`  
**Location:** Line 38 (file reference table)

**What it says:**
> `elyndor/history/HISTORY_BIBLE.md` | "Four Ages framework: Age of Creation, Age of Kingdoms, Age of Wars (Talos served here; Vampire Houses expanded here), Age of Shadows (present)"

**What the Lore Bible says:**  
The canonical framework is Seven Ages. The Four Ages framework has been explicitly superseded.

**Why this matters:**  
The AI Continuation Guide is the primary bootstrapping document for every future development session. Any AI session that follows this guide will be told the Four Ages framework is the current canonical framework and will use obsolete age names in quest content, NPC dialogue, codex entries, and historical references. This affects every piece of lore content created in every future session until corrected.

**Recommended correction:**  
1. Update line 38 to reference `elyndor/history/HISTORY_BIBLE.md` as needing reconciliation with the Seven Ages framework.
2. Add `docs/lore/` and `docs/lore/CANON_RULES.md` to the "Read These Files First" table at the top of the guide, with the note that the Lore Bible supersedes earlier historical documents.
3. Add `docs/lore/TIMELINE.md` as the concise canonical chronological reference.

---

### ❌ 3 — GAME_BIBLE ToC Describes History File as "Four Ages Framework"

**File:** `docs/GAME_BIBLE.md`  
**Location:** Line 52 (Table of Contents entry #42)

**What it says:**
> `42. [History Bible](../elyndor/history/HISTORY_BIBLE.md)` *(separate file — Four Ages framework)*

**What the Lore Bible says:**  
The canonical framework is Seven Ages.

**Why this matters:**  
The GAME_BIBLE ToC is a navigation document used by both human developers and AI sessions. Describing the history file as "Four Ages framework" will direct readers to use the obsolete document as authoritative.

**Recommended correction:**  
Update the ToC description to note that `elyndor/history/HISTORY_BIBLE.md` is pending reconciliation with the Seven Ages framework, and add a note directing readers to `docs/lore/HISTORY_BIBLE.md` and `docs/lore/TIMELINE.md` for the current canonical framework.

---

### ❌ 4 — A God Appears and Speaks Directly to Eleanor

**File:** `docs/heroes/ELEANOR.md`  
**Location:** Lines 159–188 (The Harmonic Soul Revelation section)

**What it says:**
> "Inside the sanctuary, **Eleanor encounters one of the gods**."  
> "The god does not tell Eleanor what to do with this. The god tells her the truth about what she is, because she asked, and because she was ready to hear it."  
> "Most mages learn one note. You can hear the entire symphony. What you do with that hearing is yours to decide."

**What the Lore Bible says:**  
`docs/lore/DIVINE_CHORUS.md`:
> "If a piece of content requires the Chorus to act, speak, appear, or select someone — it almost certainly violates the principles."

`docs/lore/CANON_RULES.md`:
> "They do not communicate personal divine instructions to individuals."

**Why this matters:**  
A member of the Divine Chorus appears physically, speaks directly to Eleanor, and communicates knowledge about her nature. Even though the scene is carefully written to avoid chosen-one language and the god gives no instructions, the act of appearing and speaking in person conflicts with the Lore Bible's core principle that the Chorus is a presence felt through the world, not a being players or companions can encounter directly.

**Mitigating factors:**  
- The scene explicitly denies Eleanor is chosen: "The gods chose no one; the universe simply produced someone unusual."
- The god does not select Eleanor for a purpose, does not give instructions, and cannot grant or revoke her Harmonic Soul nature.
- The encounter happens at a sealed First Age sanctuary, which `docs/world/religions.md` establishes as existing.
- The information conveyed could be discoverable through other means (the magic of the sanctuary itself revealing truth to those ready to hear it, rather than a god in person).

**This was written before the Lore Bible was established.** The core content of the revelation (Harmonic Soul, what it means, what it does not mean) is fully canon-compatible. Only the delivery mechanism — a god appearing in person and speaking — conflicts.

**Recommended correction:**  
Revisit the delivery mechanism of the Harmonic Soul revelation during Eleanor's companion quest design. Options include:
- The sanctuary itself communicates truth through its magic, without a god appearing personally
- Eleanor experiences an overwhelming impression or vision rather than a direct conversation
- The knowledge arrives through ancient records discovered within the sanctuary — the god's ancient words preserved in inscription or crystallized memory, not a living encounter

The revelation's content does not need to change. The god appearing in person does.

---

## ⚠ Minor Inconsistencies

These are small wording, terminology, or framing issues that do not fundamentally break the canon but should be corrected over time.

---

### ⚠ 1 — "Ancient God" Is Not a Canonical Designation

**Files:** `elyndor/history/HISTORY_BIBLE.md` (lines 31, 71, 88, 100, and others); `elyndor/magic/MAGIC_BIBLE.md` (lines 11, 13); `docs/CAMPAIGN_DESIGN.md` (line 35)  

**Issue:**  
The Eighth is referred to as "the Ancient God" throughout these documents — used both as an in-world term and as a factual descriptor in the magic system.

**What the Lore Bible says:**  
`CANON_RULES.md`: She is referred to as "the Forgotten Eighth," "the Absent One," or "the goddess of a specific domain only in contexts where that domain is relevant."

`elyndor/history/the_eighth.md` lists "The Ancient One" (imprecise, in-world label) as one of several references used by those who don't know the truth. "Ancient God" is close to this but not identical — and when used in the magic system lore (`MAGIC_BIBLE.md` line 11), it reads as a factual designation rather than an in-world misconception.

**Recommended correction:**  
- In-world references (what characters believe) can use "the Ancient God" as an in-world label for those without access to the truth.
- Lore documents written from a developer/writer perspective should use "the Forgotten Eighth" when speaking factually.
- `MAGIC_BIBLE.md` line 11 is a developer-facing document; it should use the canonical name.

---

### ⚠ 2 — Primordial Magic Attributed to the Eighth Alone

**File:** `elyndor/magic/MAGIC_BIBLE.md`  
**Location:** Line 11

**What it says:**
> "Primordial Magic is the original magical force woven into creation by the Ancient God during the First Age."

**Issue:**  
This attributes the creation/weaving of Primordial Magic to the Eighth ("the Ancient God") alone. The canonical account in `docs/lore/TIMELINE.md` says:

> "The Divine Chorus comes into being — eight members. The First Song is sung; Primordial Energy flows; physical reality takes its current form."

The First Song is an act of all eight Chorus members collectively. Primordial Magic is not the Eighth's individual creation.

**Recommended correction:**  
Attribute Primordial Magic's existence to the full Chorus and the First Song, not to the Eighth alone. The Eighth's imprisonment *changed* Primordial Magic (fracturing it into elemental aspects) — this is correctly documented — but she did not singularly create it.

---

### ⚠ 3 — "Shaped the First Races" May Contradict Chorus Non-Creator Status

**File:** `elyndor/history/HISTORY_BIBLE.md`  
**Location:** Line 31

**What it says:**
> "The Ancient God was active in the world; its influence directly shaped the physical world and the first races."

**Issue:**  
This claims the Eighth "directly shaped…the first races." The Lore Bible (`docs/lore/DIVINE_CHORUS.md`) establishes: "They did not create mortal life. They did not design civilization."

If the Eighth shaped the first races, this attributes the creation of mortal life to a Chorus member — contradicting the principle that the Chorus did not create mortal life.

**Recommended correction:**  
Revise to clarify that the Eighth was active in the world during the First Age without attributing the creation or shaping of mortal life to her. Her influence on the physical world (geography, natural forces) is potentially compatible with her role as a Chorus member; her influence on "the first races" implies creation and should be reframed.

---

### ⚠ 4 — "Gods Walked Among Mortals" Implies Past Direct Chorus Involvement

**File:** `elyndor/history/HISTORY_BIBLE.md`  
**Location:** Line 35

**What it says:**
> "The gods walked among mortals directly, before their withdrawal."

**Issue:**  
This implies the Chorus was historically more directly present in mortal affairs, and that the Sundering caused their withdrawal. The Lore Bible does not explicitly address whether the Chorus was ever more directly present — it describes their relationship to mortals in perpetual-tense terms that don't allow for a historical period of greater intervention.

**Mitigating factors:**  
The Eighth specifically is documented as spending extended time among mortals — this is canonical. The claim may be an overgeneralization from her specific behavior to all members of the Chorus.

**Recommended correction:**  
Reframe to make clear that the Eighth's presence among mortals was unusual and not characteristic of the full Chorus. The withdrawal after the Sundering may refer to the Chorus becoming more careful and reserved following the trauma of the Sundering — a change in emotional posture, not a change from political intervention to non-intervention.

---

### ⚠ 5 — "Third Age" Terminology in the_eighth.md

**File:** `elyndor/history/the_eighth.md`  
**Location:** Line 221

**What it says:**
> "The Third Age's wars destroyed libraries and archives that might have preserved more."

**Issue:**  
This uses Four Ages terminology ("Third Age") in a document that otherwise aligns with Seven Ages-compatible language. Under the Seven Ages framework, the "Third Age" maps approximately to "The Long Decline" and "The Sundering" period, not a distinct "Third Age of Wars."

**Recommended correction:**  
Update to Seven Ages terminology when `elyndor/history/HISTORY_BIBLE.md` is revised. Replace "The Third Age's wars" with a reference to the conflicts of The Long Decline or the period following the Sundering, depending on the intended historical reference.

---

### ⚠ 6 — AI Continuation Guide Does Not Reference the Lore Bible

**File:** `docs/AI_CONTINUATION_GUIDE.md`  
**Location:** "Read These Files First" table (lines 11–56)

**Issue:**  
The Lore Bible (`docs/lore/`) does not appear anywhere in the AI Continuation Guide's priority reading list. This document is the primary bootstrapping resource for future AI development sessions. Without a reference to the Lore Bible, any future AI session will proceed without knowing that `docs/lore/CANON_RULES.md` establishes immutable design principles that supersede earlier documents.

**Recommended correction:**  
Add the following entries to the "Read These Files First" table, near the top:
- `docs/lore/README.md` — Lore Bible index; establishes the canonical source of truth for all worldbuilding
- `docs/lore/CANON_RULES.md` — Immutable design principles; read before any lore, quest, NPC, or companion work
- `docs/lore/TIMELINE.md` — Canonical Seven Ages chronological reference (supersedes Four Ages framework)

This is independently logged as a proposed task (#85 in the task list).

---

### ⚠ 7 — "Divine Cleric" Role in UI Mockup

**File:** `preview.py`  
**Location:** Line 895

**What it says:**
> `{ name:'Seraphina', role:'Divine Cleric', ... }`

**Issue:**  
"Divine Cleric" as a role title implies direct divine selection or empowerment, which is in mild tension with the Lore Bible's principle that the Chorus does not select individuals for divine purposes. The Lore Bible does not prohibit religious practitioners from existing; it prohibits the framing of individuals as divinely chosen.

**Context:**  
This is a UI mockup with placeholder characters. "Seraphina" and companions "Dregan" and "Zyx the Woven" are not canonical heroes. This is a demonstration interface, not authored story content. Very low priority.

**Recommended correction:**  
When placeholder content in `preview.py` is eventually replaced with canonical hero data, ensure role titles do not use "Divine" as a prefix implying selection (e.g., "Chorus Cleric," "Temple Cleric," "Sacred Healer," or the character's actual class name). No urgent action required for placeholder UI content.

---

### ⚠ 8 — "Great Libraries" (Plural) in Capital Province Description

**File:** `docs/world/WORLD_BIBLE.md`  
**Location:** Line 246

**What it says:**
> "Institutions | Royal Government, Military High Command, Mages Guild Headquarters, Major Temples, Universities, **Great Libraries**"

**Issue:**  
"Great Libraries" (plural) contradicts `docs/lore/GREAT_LIBRARY.md`, which establishes the Great Library as a singular institution — the continent's primary archive.

**Recommended correction:**  
Change "Great Libraries" to "the Great Library" in the Capital Province institution table.

---

### ⚠ 9 — Eleanor's Harmonic Soul Implies a Connection to the Eighth's Work

**Files:** `elyndor/magic/MAGIC_BIBLE.md` (line 11); `docs/heroes/ELEANOR.md`  

**Issue:**  
`MAGIC_BIBLE.md` states Primordial Magic was "woven into creation by the Ancient God." Eleanor's Harmonic Soul connects her to pre-fracture Primordial Magic — the unified source as it existed before the Eighth's imprisonment. The architecture therefore implies Eleanor has an unusual relationship to the Eighth's work specifically.

This is not stated anywhere as a chosen-one connection, and the documents explicitly deny it. However, the underlying structure creates a latent implication that future writers could accidentally reinforce: "Eleanor is special because she's connected to what the Eighth made."

**Recommended correction:**  
When the attribution of Primordial Magic to "the Ancient God" alone is corrected (see ⚠ #2) — attributing the First Song to the full Chorus — Eleanor's Harmonic Soul becomes a connection to the collective Chorus's work rather than to the Eighth specifically. This resolves the latent implication at the structural level without requiring any change to Eleanor's documented arc.

---

## 💡 Suggestions

Environmental storytelling opportunities that would deepen the Lore Bible's world philosophy without requiring system changes. These are recommendations only. Do not implement without review.

---

### 💡 1 — Sol Kareth's Buried Civilizations as Architect Evidence

**Existing setup:** `docs/world/WORLD_BIBLE.md` describes Sol Kareth as having "countless ruins beneath the sands" and "buried civilizations." The Corruption is "waking what was buried."

**Opportunity:** Some of these ruins could be Architect-adjacent — structures whose age, materials, or geometry resist explanation by any known civilization. Sol Kareth's scholars and merchants would have encountered these ruins for generations and developed entirely secular theories about them. An archivist from the Great Library visiting Sol Kareth could recognize, with unsettling certainty, that one particular structure belongs in the same category as the anomaly beneath the First Temple — without being able to say more. History discovered, not explained.

---

### 💡 2 — Frozen Highlands Oral Traditions and the Great Forgetting

**Existing setup:** `elyndor/history/the_eighth.md` notes that "certain practices and references in The Old Ways and The Ancestors' Path…do not quite fit seven-member theology, because they were established before the Forgetting."

**Opportunity:** Frozen Highlands oral tradition — passed through generations without a written record — could contain grief rites or ancestor-veneration practices with an eighth invocation that no living practitioner can explain. The rite would be performed because "it has always been done this way." A scholar who studies it would find one more reference, in a liturgy no one understands, to a mourned figure who has no name. Discovery without resolution.

---

### 💡 3 — Gnome Archive Communities and the Gap

**Existing setup:** Gnome communities in the Iron Peaks lower settlements are "among the oldest on the continent" and function as record-keepers for the dwarven kingdoms.

**Opportunity:** The oldest gnome archive catalogs would pre-date the Age of Restoration's reconstruction. A player or companion with access could find that the gnome records for the Age of Unity are mysteriously incomplete — not lost through disaster, but containing systematic gaps that gnomish archivists have catalogued as "administrative loss, cause unknown." The gaps follow a pattern that a sufficiently informed player would recognize as the shape of a removal, not a loss.

---

### 💡 4 — Age of Unity Trade Routes as Visible History

**Existing setup:** `docs/lore/HISTORY_BIBLE.md` notes that "the trade routes that still exist in the [present] trace back to Age of Unity construction."

**Opportunity:** Road milestones, bridge keystones, and waymarker inscriptions along these ancient routes could bear construction dates or dedication texts that, when translated, reference a civilization larger than anything in the current political map. A gnome scholar who studies old roads for structural engineering purposes would find architecture that assumes a continent-scale coordinated infrastructure — impossible to build without political unity that no current kingdom can claim. The scale of what was lost, made visible in stone.

---

### 💡 5 — House Soleth Archives and the Eighth's Absence

**Existing setup:** House Soleth's power is "ancient knowledge and survival of vampire society — power through accumulated history and secrets." Their Archivist holds "personal name unused for centuries."

**Opportunity:** House Soleth's archive is old enough to pre-date the complete Great Forgetting. Somewhere in their holdings is a document — a temple inventory, a scholar's correspondence, a merchant's contract — that references an eighth elemental domain in passing, as if it were common knowledge. The Archivist knows this document exists. The Archivist does not know what the eighth domain was, or why the reference appears nowhere else. It is filed as a historical curiosity. It is one of the things that could lead a thorough player directly to the campaign's central truth — if they earn enough access to ask about it.

---

### 💡 6 — Theologically Anomalous Grief Rites

**Existing setup:** The Veiled Order's theology centers on Morvel (Shadow — death, transition, memory, the threshold). The Order treats death as transition, not ending.

**Opportunity:** The Veiled Order's most ancient grief rites — those pre-dating their institutional organization — include a mourning practice that senior members call "the Unresolved Grief." It is used specifically when a death is deemed impossible to fully grieve — when the loss is so fundamental that standard transition theology does not quite reach it. No one in the living Order knows what this practice was originally designed for. It has been used, rarely, for monarchs and catastrophes. A thorough player who reaches the Order's innermost scholarship might find that the rite's oldest form includes language about a mourned figure beyond the Final Verse — beyond even the Veiled Order's understanding of what follows death. The eighth grief that even death cannot contain.

---

## Summary

| Category | Count |
|---|---|
| ✔ Fully consistent files/systems | 28+ |
| ❌ Major conflicts requiring review | 4 |
| ⚠ Minor inconsistencies to correct over time | 9 |
| 💡 Environmental storytelling suggestions | 6 |

### Priority Order for Corrections

1. **`docs/AI_CONTINUATION_GUIDE.md`** — Add Lore Bible references. Until this is corrected, every future AI session starts without knowing the canonical framework exists. (See ❌ #2 and ⚠ #6)

2. **`elyndor/history/HISTORY_BIBLE.md`** — Reconcile with Seven Ages framework. This is the largest revision required and should be planned as a deliberate authoring session. (See ❌ #1)

3. **`docs/GAME_BIBLE.md` ToC entry #42** — Update description from "Four Ages framework" to reflect canonical Seven Ages. (See ❌ #3)

4. **`docs/heroes/ELEANOR.md` — Harmonic Soul delivery mechanism** — Review whether a god appearing in person and speaking directly is compatible with the Lore Bible, or whether the revelation can be delivered through the sanctuary's magic itself rather than a direct divine encounter. The revelation's content is canon-compatible; the delivery mechanism requires deliberate design review. (See ❌ #4)

5. **Terminology cleanup** — "Ancient God" designations and Primordial Magic attribution to the Eighth alone are spread across several documents and can be addressed during the `elyndor/history/HISTORY_BIBLE.md` revision. (See ⚠ #1, ⚠ #2, ⚠ #3)

6. **`docs/world/WORLD_BIBLE.md`** — "Great Libraries" to "the Great Library." (See ⚠ #8)

---

## What Is Not a Problem

The following are sometimes flagged in lore audits and are **not** issues in this repository:

- **Cults believing they are divinely chosen** — Correctly framed as false cult belief, not canonical truth. The imprisoned god's manipulation is the source.
- **Religious traditions claiming the Chorus created civilization** — Correctly framed as theology vs. canonical fact. The Solari Covenant's belief that "the Radiant One holds civilization together" is a mortal theological claim, not endorsed by the Lore Bible.
- **Eleanor's Harmonic Soul making her special** — Her uniqueness is explicitly distinguished from being chosen. The documents handle this carefully. (The delivery mechanism of the revelation is the issue, not the Harmonic Soul concept itself.)
- **The Corruption amplifying real virtues** — This is exactly as the Lore Bible describes. No issue.
- **Characters believing in prophecy or fate** — As long as this is presented as a character's belief rather than canonical truth, this is fine. No such cases were found in the reviewed documents.
- **The Eighth having loved a mortal** — Explicitly documented as not a chosen mortal. Intentionally ordinary. No issue.

---

*This audit is a read-only report. No files were modified.*  
*Review this document together before making corrections.*  
*All corrections should be documented in the relevant file's Document History section.*
