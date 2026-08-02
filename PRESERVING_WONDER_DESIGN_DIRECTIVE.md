# PRESERVING_WONDER_DESIGN_DIRECTIVE.md

> **Canon Status:** [CONFIRMED — established January 2026]
> **Authority:** Project-wide design directive addressing the three legitimate risks identified in third-party design review (lore overload, invisible consequences, administrative Legacy Questlines). Governs how every existing and future system serves the player's felt experience.
> **Rule:** No system, questline, doc, or scene may violate the principles below without an explicit design exception.
> **Integration target (Phase 2):** `GDD/01_Foundation/02_Design_Pillars.md`.

---

## Five New Design Principles (added to project philosophy)

These join the existing pillars (Handcrafted-First, Difficulty by Choice, Offline-First, Origin Characters, Living World). They are not replacements — they are the *how* that makes the others playable.

1. **Complexity is earned through discovery, not delivered through exposition.**
2. **Every major player decision should create visible consequences whenever possible.**
3. **Players should feel like they are shaping history, not managing civilizations.**
4. **History should often be discovered before it is explained.**
5. **Living World systems should create emotional immersion — not simulation for its own sake.**

---

## Risk 1 · Avoid Lore Overload

### The problem

The repository contains an enormous amount of worldbuilding — Four Ages of history, seven-member Divine Chorus, Forgotten Eighth, seven elemental aspects, three vampire houses, three goblin tribes, four religious traditions, six playable races, six regions, First Empire history, the Great Library, the First Temple, the Architects, and more. A player who receives all of this in the opening hours will bounce.

### The rule

**Complexity is earned through discovery.**

The player should encounter names, factions, and historical events **only when those concepts become relevant to the moment they are in**. The Forgotten Eighth is not introduced by name in an opening cinematic. The Architects are never explained. The Four Ages are named in-world by scholars only when a scholar has reason to name them.

### Existing systems that could violate this principle

| System | Risk | Recommended revision |
|---|---|---|
| Opening cinematic / new-game intro | Temptation to dump world history to establish stakes | Open with a specific *place* and a specific *problem* — not a history lesson. World context accrues over the first act. |
| Character sheets and codex | Temptation to make codex entries readable from the main menu | Codex entries unlock only when the player has encountered the subject in-world. Reading a codex entry should feel like *closing a loop*, not opening one. |
| Companion dialogue during recruitment | Temptation to have companions monologue their backstory | Recruit through action, not narration. Backstory unfolds across camp conversations tied to Journey System progression. |
| The Fractured Circle arc (Eleanor) | Sanctuary scene risks over-explaining Primordial Magic | Per D-02 ruling, Eleanor pieces the truth together herself across three stages. Extend this pattern: no NPC ever explicitly explains "what a Harmonic Soul is" before Stage 2. |
| The Forgotten Eighth | Temptation to name her early | Follow the two-tier naming rule (pending D-05). Early game: "the Ancient God" is a rumor. Only late-game investigation reveals she was one of the Chorus. |
| Divine Chorus | Temptation to enumerate the seven gods in a single conversation | Introduce one god at a time, tied to the regions and situations where their element matters. The full seven-member structure is not shown to the player until they've encountered several individually. |

### Delivery-timing rubric (new discipline for every doc)

Every named canonical concept should carry a `first-encounter-window` annotation during Phase 2 consolidation:

- **Act 1** — race names, region names, one god, one faction per region, the Corruption as a felt threat.
- **Act 2** — the Four Ages (by name), inter-tribal politics, more of the Chorus, individual companion Core Wounds.
- **Act 3** — the Sundering, the Forgotten Eighth (as concept), the Living World's largest political shifts.
- **Legacy Questlines / late-game** — the Architects (glimpsed, never explained), the true depth of First-Age history, the Great Forgetting.

Content that violates its window is either delayed or repositioned. Nothing is deleted.

---

## Risk 2 · Visible Consequences

### The problem

A Living World that changes but doesn't *show* the change might as well be static. The player must be able to see the world respond.

### The rule

**Every major decision creates visible consequences. Show, don't tell.**

### Cross-catalog of visible-consequence mechanisms

Extending the environmental storytelling checklist in `LIVING_WORLD_DESIGN_PILLAR.md`, the following are the vocabulary the world uses to *speak back* to the player:

**Immediate visible signals (within one settlement visit):**
- New patrols on roads the player has recently cleared.
- Repaired walls where combat damaged them.
- New banners at settlements the player helped defend.
- Altered marketplace stock (safer trade routes → more variety; danger → scarcity).
- NPCs who now greet the player by name or reference a past action.
- Children playing at recent events ("You be the traveler who came here! I'll be the shadow-beast!").

**Medium-term signals (across regional revisits):**
- New buildings (a new smithy after the Frontier's trade routes reopened; a new refugee house after the player secured aid).
- New caravans stopping at settlements they previously avoided.
- New council representatives seated (goblin representative at the Capital, per Council of Embers success).
- Statues, memorials, or planted trees.
- Festivals held or postponed.

**Long-term signals (across acts):**
- New books in the Great Library referencing the player's era.
- Old road inscriptions re-carved in mixed script styles.
- Companion Evolution states visibly shifting how they occupy settlements.
- NPCs in later acts referencing the player's early-act actions unprompted.

### Additional visible-consequence ideas (per your request)

- **The Great Library's card catalog visibly grows.** Every completed major action produces an archived record. A player can literally read the world's memory of them.
- **The Capital's diplomatic hall.** A single hall in the Capital contains a seat for every civilization that has formally recognized the Kingdom. If the Council of Embers succeeds, a new empty chair is added — then filled at a visible ceremony.
- **The world's night sky.** After the completion of certain Legacy Questlines, subtle visual changes to the horizon at that region (e.g., a new watchfire pattern visible tower-to-tower after The Council of Embers's mixed patrols begin).
- **Companion small-story feedback.** Companions notice consequences the player might miss. Talos: *"The road guard nodded to you. He was hostile the last time we passed."* Eleanor: *"The archive shelf you had me research now includes your name in the acknowledgments."*
- **Ambient art in Living World spaces.** Murals painted over time by settlement children; new frescoes added to religious spaces after the tradition's questline; new songs sung at evening fires that reference recent events by phrasing rather than by name.

### Rule for authoring

Every quest with a completion state must specify at minimum **three visible-consequence signals** (immediate / medium-term / long-term) before it is considered content-complete. This is a hard authoring gate, not a suggestion.

---

## Risk 3 · Legacy Questlines Must Feel Like Adventures

### The problem

A Legacy Questline that resolves through diplomacy, reputation math, and formal ceremony is at risk of feeling like an administrative arc. Politics is *not* the reward — politics is the *consequence* of adventure.

### The rule

**Every Legacy Questline must be an adventure first. Political outcomes emerge from adventure — never the other way.**

### Required adventure elements (per Legacy Questline)

Adding this to the Legacy Questlines framework as a mandatory checklist:

- [ ] At least one memorable dungeon or expedition.
- [ ] At least one dangerous journey between locations (Journey System engaged).
- [ ] At least one character moment per involved companion (personal beat during the arc, not merely presence).
- [ ] At least one difficult moral decision that has no clean answer.
- [ ] At least one emotional payoff scene — a scene that lands even for a player uninterested in the arc's political consequence.
- [ ] At least one exciting combat encounter with a memorable enemy (not a filler mob).
- [ ] At least one act of discovery — an ancient site, a hidden truth, a forgotten relic.

The political outcome (Council of Embers formed; Khaz-Dur reclaimed; Elder Grove renewed; Crown's Reckoning delivered; Great Hunt gathered) is what remains *after* the adventure. Not what the adventure is *for*.

### Reference implementation — Council of Embers as adventure

Applying the checklist to Council of Embers to prove the framework:

- **Dungeon:** the abandoned First Convocation site itself functions as an exploration space. Beneath it — a sealed chamber that has never been opened, containing the true story of the First Convocation's failure. Combat-relevant if the failure summoned something the tribes could not later contain.
- **Dangerous journey:** transporting each tribe's sacred brazier across contested territory to the Convocation site. Multiple ambush points; Corrupted Goblins attempting to prevent the ceremony.
- **Character moments:** each companion has a natural personal beat during the arc (see the seven-companion resonance map in `LEGACY_CIVILIZATION_QUESTLINES.md`).
- **Difficult decision:** at least one moment where the player must choose which tribe's demand for satisfaction takes priority — with genuine cost to whichever tribe is chosen second.
- **Emotional payoff:** the moment when the elder from a specific tribe places their ember — the tribe that lost most in the First Convocation's collapse. That moment lands regardless of political context.
- **Exciting combat:** an authored boss encounter — recommended: a Corrupted former Council-hopeful from generations ago, still guarding the site, mistaking every visitor for the messengers who failed the First Convocation.
- **Discovery:** the truth of what happened at the First Convocation. Never fully explained until this arc.

The four remaining Legacy Questlines (Khaz-Dur, Elder Grove, Crown's Reckoning, Great Hunt) must each satisfy the checklist during their authoring pass. This is a **framework amendment** to `LEGACY_CIVILIZATION_QUESTLINES.md`.

---

## Risk 4 · Preserve Wonder

### The problem

Living World simulation is a *means*, not a goal. If the player consciously perceives the schedule, the mechanic has failed.

### The rule

**Wonder outranks simulation.** The invisible scheduler in `docs/systems/journey_system.md` already embodies this principle for companion conversations. Extend it universally.

### Design discipline

- NPCs never *state* their schedules. They are simply doing what they are doing when the player finds them.
- If a system's presence becomes visible as a system (e.g., "the tavern-keeper always goes to bed at 22:00, I can time-skip"), refactor toward variance. Real people are inconsistent.
- The player should never see a "simulation running" indicator, tick counter, or day-cycle debug element in shipped play.
- Systems exist to serve the felt sense of a place being alive. When the two conflict, cut the system.

### Existing systems to review through this lens

| System | Wonder risk | Recommended discipline |
|---|---|---|
| Living World tick cadence (pending D-12) | Fixed daily tick may feel gamey | Hybrid cadence (per my D-12 recommendation) already softens this. Layer variance into daily events so no two days feel identical. |
| Settlement Dispersal (pending D-16) | Companions predictably at the same spot every visit | Introduce small-story variance — Talos may be at the training ground three visits in a row, then teaching a specific child the fourth visit, then absent (in the archive) the fifth. |
| Journey System camp events | Priority queue may feel algorithmic if events fire in the same order | Existing scheduler already randomizes low-priority ambient events. Extend this discipline to mid-priority character moments so the *order* of relationship growth varies per playthrough. |

---

## Risk 5 · History Should Be Discoverable

### The rule

**The player discovers history before it is explained. Explanation is a reward for attention.**

This is already the working discipline of the Living World pillar. Formalizing it as a storytelling technique:

### The Discoverable-History Rubric

Every major piece of world history should exist in the world before it is named by any NPC:

1. **First encounter — physical.** The player sees a site, an object, or a marking.
2. **Second encounter — pattern.** The player sees the same site or motif elsewhere, in a different context.
3. **Third encounter — question.** A companion, an NPC, or an ambient piece of dialogue references the site indirectly. The player begins to suspect meaning.
4. **Fourth encounter — partial answer.** A codex entry, a book, or a scholar provides *some* context. Still not the full truth.
5. **Fifth encounter — reveal.** A Legacy Questline, a personal quest, or a late-game story beat reveals what was really there.

The First Convocation site (per `CANDIDATE_QUESTLINE_COUNCIL_OF_EMBERS.md`) is an ideal reference — the player passes through it before knowing what it is; only much later do they return with the knowledge to understand it.

**Extend this pattern to at least ten discoverable historical sites** across the world during Phase 2 authoring. Each site: cold, present, weathered, unnamed until the moment its name becomes earned.

---

## Risk 6 · Every Civilization Needs Its Own Identity

### The rule

**No civilization is a re-skin.** Each answers five identity questions distinctly.

### The Five Civilization Identity Questions

Every civilization in the game must have a documented answer to:

1. **What are they trying to become?**
2. **What do they fear losing?**
3. **What does everyday life look like?**
4. **What makes visitors immediately recognize this culture?**
5. **What historical burden do they carry?**

Legacy Questlines emerge naturally from the answers. Environmental storytelling emerges from the answers. Companion resonance emerges from the answers.

### Sample answers — Goblins (from `GOBLIN_CULTURE.md`)

1. *A civilization the world recognizes as such — not raiders, not vermin, but a people.*
2. *Their tribes' distinct identities under the pressure to merge or vanish.*
3. *Layered settlements built over centuries; hearth-tending; Contribution Feasts; Silence Watches.*
4. *Named tools; maker's-marks; First Hearths.*
5. *The First Convocation's failure and the goblins who died believing in it.*

### Required per civilization

Author or extract these five answers for every named civilization during Phase 2:

- Humans (Kingdom / Frontier — distinct answers)
- Goblins (done — `GOBLIN_CULTURE.md`)
- Elves
- Dwarves
- Gnomes (currently ⚠ NOT YET DEFINED — priority)
- Halflings (currently ⚠ NOT YET DEFINED — priority)
- Orcs
- Beastfolk (currently mostly ⚠ NOT YET DEFINED)
- Sol Kareth
- Vampire Houses (each house has distinct answers)
- Refugee settlements (as an emergent culture)

---

## Risk 7 · Marketing Perspective

### The rule

**Living World and Legacy Questlines are the reason players stay. Companions, combat, art, and exploration are the reason players buy.**

### Design implication

The complex worldbuilding systems this project has built must be *invisible entrance requirements* and *visible retention rewards*. A first-hour player should be captivated by:

- The look of Talos, and how he holds a sword.
- The feel of a first combat encounter — grid, MP, AP, facing, downed.
- The tone of the first settlement.
- The immediate warmth of the first companion recruitment.
- A memorable enemy silhouette.
- One striking piece of environmental art.

If the first hour requires the player to have understood Living World, Legacy Questlines, the Chorus, the Sundering, or the Four Ages, we have overloaded.

### Authoring implication

Every scene in the first hour has one job: **make the player feel this game is worth their time.** Nothing else. World depth *begins to matter* somewhere in hours 4–8. World depth *becomes the reason to stay* by hour 20. Full canonical depth *pays off* in the Legacy Questlines and endgame.

Every doc created during Phase 2 consolidation should specify: *"When does this content earn its place in the player's attention?"*

---

## Summary — What This Directive Changes

1. **Adds five new design principles** to the project philosophy.
2. **Adds a delivery-timing rubric** — every canonical concept gets a first-encounter-window annotation during Phase 2.
3. **Adds a visible-consequence gate** — every quest must specify at least three visible-consequence signals before being content-complete.
4. **Amends the Legacy Questlines framework** — every arc must satisfy the seven-item adventure checklist.
5. **Extends the wonder discipline** — variance in Settlement Dispersal, Journey scheduling, and Living World cadence.
6. **Formalizes the discoverable-history rubric** — five-encounter progression from physical → reveal.
7. **Requires per-civilization identity documentation** — the Five Civilization Identity Questions.
8. **Establishes the marketing-vs-retention distinction** — first-hour hooks are art, companions, combat, tone. World depth is the reason to stay.

---

## Existing Documents That Need Revision During Phase 2

- `CONSOLIDATION_REPORT.md` — add references to this directive as a Phase 3 requirement.
- `LIVING_WORLD_DESIGN_PILLAR.md` — cross-reference the wonder-preservation discipline.
- `LEGACY_CIVILIZATION_QUESTLINES.md` — add the seven-item adventure checklist to the framework.
- `GOBLIN_CULTURE.md` — Five Civilization Identity Questions worked into the intro.
- `docs/GAME_BIBLE.md` (Phase 2) — new pillar section referencing all five new principles.
- `docs/systems/journey_system.md` — reference the wonder-outranks-simulation discipline.
- `docs/CAMPAIGN_DESIGN.md` — reference the delivery-timing rubric.

---

## What Does NOT Change

- Established canon is intact. No lore is removed, altered, or reduced.
- The Council of Embers concept is unchanged; only its authored form must satisfy the adventure checklist.
- Every companion, race, faction, and questline previously canonized remains canonical.
- The final canonical roster of seven companions is unchanged.
- The Four Ages framework is unchanged.
- The Corruption as universal threat is unchanged.

**The world does not get smaller. It gets easier to enter.**

---

## Document History

| Date | Change |
|---|---|
| Jan 2026 | Created in response to third-party design review flagging lore overload, invisible consequences, and administrative-questline risks. Adds five new design principles + delivery-timing rubric + visible-consequence gate + adventure checklist + wonder discipline + discoverable-history rubric + per-civilization identity questions + marketing/retention distinction. Preserves every existing canonical decision. |
