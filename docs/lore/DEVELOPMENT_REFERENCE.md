# Development Reference — Canon Constitution

> **Authority:** This document defines how every future AI agent and developer should think when expanding Project Dungeon Keeper. It is the constitution for all future development.
>
> The Lore Bible (`docs/lore/`) defines what the world **is**.  
> This document defines how to **work within it**.

---

## Phase Declaration

The project has entered a new phase of development.

The Lore Bible located in `docs/lore/` is now the canonical foundation of the entire project. It supersedes any older documentation, design notes, historical timelines, or legacy worldbuilding that may still exist elsewhere in the repository.

**When making future changes, use the Lore Bible as the primary source of truth.**

---

## Canonical Principles

The following principles are immutable unless explicitly revised by the project owner.

### World Philosophy

- There is no chosen one.
- There are no chosen races.
- There are no divine bloodlines.
- Heroes become heroes through their choices.
- History belongs to mortals.
- Civilization is inherited and shaped by each generation.

### The Divine Chorus

The Divine Chorus preserves existence — not history.

They do **not**:
- choose rulers
- manipulate politics
- determine wars
- create destiny
- interfere with mortal affairs except when reality itself is threatened

They care deeply for Creation while respecting mortal free will.

### The Architects

The Architects exist only as an ancient mystery.

- They should never be fully explained.
- They should never become active characters, enemies, or quest-givers.
- Mystery is intentional and should always be preserved.

### The Great Library

The Great Library is the world's foremost institution of knowledge.

- Its purpose is preserving civilization's collective memory for future generations.
- The Order of Archivists is politically neutral and serves truth rather than governments.

---

## Narrative Philosophy

When creating content:

- **Show history instead of explaining it.**
- **Prefer environmental storytelling over exposition.**
- Allow cultures to interpret history differently.
- Preserve ambiguity where appropriate.
- Maintain a sense of an ancient, lived-in world.

---

## Development Guidelines

Before introducing new lore, verify that it does not contradict the Lore Bible.

If a contradiction exists:

1. Treat the Lore Bible as canonical.
2. Adapt the new content to fit the established canon.
3. If the conflict cannot be resolved without changing canon, **request designer approval before proceeding.**

---

## Design Goal

Every quest, companion, city, faction, book, ruin, artifact, and line of dialogue should feel like it belongs to a world with thousands of years of believable history.

- **Consistency is more important than novelty.**
- **Historical depth is more important than spectacle.**
- **Mystery is more powerful than complete explanation.**

The player should always feel that they are exploring a living world that existed long before their arrival and will continue long after their story ends.

---

## Final Principle

> When uncertain, favor **consistency**, **subtlety**, **historical depth**, and **respect for established canon** over introducing new ideas that could weaken the world's internal logic.

---

## Reading Order for New Sessions

If you are an AI agent bootstrapping a new development session, read these files in this order before doing any lore, quest, NPC, or companion work:

| Priority | File | Purpose |
|---|---|---|
| 1 | `docs/lore/CANON_RULES.md` | Immutable design principles |
| 2 | `docs/lore/README.md` | Lore Bible index |
| 3 | `docs/lore/TIMELINE.md` | Canonical Seven Ages chronological reference |
| 4 | `docs/lore/DIVINE_CHORUS.md` | How to handle the Chorus |
| 5 | `docs/lore/ARCHITECTS.md` | What can and cannot be said about them |
| 6 | `docs/lore/HISTORY_BIBLE.md` | Narrative companion to the Seven Ages |
| 7 | `docs/lore/FIRST_TEMPLE.md` | The boundary that must never be crossed |
| 8 | `docs/AI_CONTINUATION_GUIDE.md` | Full session bootstrap context |

> **Note:** `elyndor/history/HISTORY_BIBLE.md` uses the obsolete Four Ages framework and is pending reconciliation with the Seven Ages canon. Until updated, defer to `docs/lore/HISTORY_BIBLE.md` and `docs/lore/TIMELINE.md` for historical structure.
