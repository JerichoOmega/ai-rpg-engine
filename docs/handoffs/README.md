# Handoff System

> **Purpose:** A standardized communication layer between development sessions.  
> Every time meaningful work is completed, a dated handoff document is created here.  
> The newest handoff is the first thing any future contributor should read.

---

## What Is This System?

The handoff system is a **session-level record** — a concise brief written at the end of every significant development session that answers the question: *"What happened last time, and where should we go next?"*

It is not a changelog (that's `CHANGELOG.md`).  
It is not project status (that's `PROJECT_STATE.md`).  
It is not architecture documentation (that's `docs/architecture.md`).  

It is the **context layer** — the human- and AI-readable record of exactly what was done, what was decided, what was left incomplete, and what to do next.

---

## When to Create a Handoff

Create a new handoff document at the end of any session that includes:

- A new feature or system being implemented
- A significant bug fix or integration pass
- An architectural change
- A major documentation effort
- Any work that took more than a few minutes and changed the project state

**Rule:** If the next contributor would benefit from knowing what happened, write a handoff.

---

## How to Create a Handoff

1. Copy `HANDOFF_TEMPLATE.md` from this directory.
2. Name the new file: `YYYY-MM-DD-short-description.md`  
   Example: `2026-08-15-combat-system-refactor.md`
3. Fill in every section. Use `N/A` for sections that do not apply.
4. Never overwrite a previous handoff. They are a permanent historical record.
5. Update `PROJECT_STATE.md` to reference this handoff in the "Recently Completed Work" section.

---

## How to Read a Handoff

1. Open the most recent handoff (sort by filename date, take the last).
2. Read **Completed Work**, **Warnings**, and **Recommended Next Task** first.
3. Follow any links to deeper documentation for full context.
4. Then read `PROJECT_MEMORY.md` and `PROJECT_STATE.md` for current project status.

---

## Relationship to Other Documents

| Document | Role | Relationship to Handoffs |
|---|---|---|
| `docs/handoffs/*.md` | Session-level record | **Read this first** — most recent context |
| `PROJECT_MEMORY.md` | AI quick-start summary | Stable overview; updated only when onboarding info changes |
| `PROJECT_STATE.md` | Current project health | Updated after every session; tracks bugs, completion, priorities |
| `CHANGELOG.md` | Development history by milestone | Coarser grain than handoffs; grouped by version milestone |
| `PROJECT_CONSTITUTION.md` | Permanent governance | Does not change session-to-session |
| `docs/GAME_BIBLE.md` | Game design canon | Updated only when gameplay changes |
| `docs/AI_CONTINUATION_GUIDE.md` | AI contributor rules | Updated when architecture or conventions change |

### The Reading Order for a New Contributor

```
1. docs/handoffs/<latest>.md      ← what happened last session
2. PROJECT_MEMORY.md              ← full project quick-start
3. PROJECT_STATE.md               ← current health and priorities
4. PROJECT_CONSTITUTION.md        ← governing rules
5. docs/GAME_BIBLE.md             ← what the game is
6. docs/AI_CONTINUATION_GUIDE.md  ← how to work here
```

---

## Handoff Index

| Date | File | Summary |
|---|---|---|
| 2026-07-30 | [`2026-07-30-documentation-session.md`](2026-07-30-documentation-session.md) | Full documentation suite created; integration pass completed |
| 2026-07-31 | [`2026-07-31-lore-design-session.md`](2026-07-31-lore-design-session.md) | Engine stabilization (dual player-state eliminated); lore Bible expansion (Four Ages framework, First Empire, Great Library Director, Soleth Archive, Capital dynasty, hero arcs) |
| 2026-06-15 | [`2026-06-15-legacy-questline-integration.md`](2026-06-15-legacy-questline-integration.md) | Legacy Questline Architecture: 13 reusable frameworks + 3 approved quests (data-driven), dev tools, automated harness (6/6), wired into game loop |

*Add new rows here (oldest → newest) each time a handoff is created.*

---

## Rules

- **Never delete a handoff.** They are a permanent historical record.
- **Never edit a completed handoff.** If corrections are needed, note them in the next handoff.
- **One handoff per session.** If multiple sessions happen in a day, append a suffix: `2026-08-15-a-...md`, `2026-08-15-b-...md`.
- **Cross-reference, don't duplicate.** Link to existing docs rather than restating them in full.
