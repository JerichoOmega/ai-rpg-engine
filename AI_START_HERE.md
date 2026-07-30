# AI_START_HERE.md

> **This is the first file every AI assistant and developer reads before touching this repository.**  
> Follow this guide from top to bottom at the start of every session.  
> Follow the shutdown checklist at the end of every session.  
> Last updated: July 2026.

---

## What Is This Project?

A terminal-based AI RPG written in Python. The player types commands; an AI Director shapes the narrative. The engine covers combat, quests, factions, economy, companions, and exploration — all in a single Python process with no external dependencies.

**Entry point:** `main.py` → `game_loop.py`  
**Central state:** `world_state.py` (one dict, always the truth)  
**Cross-module communication:** `event_bus.py` (publish/subscribe)

---

## Step 1 — Read These Documents in Order

Do not skip steps. Do not start coding until Step 6 is complete.

### 1. Latest Handoff
```
docs/handoffs/   ← open the file with the most recent date
```
Read: **Completed Work**, **Warnings**, and **Recommended Next Task** first.  
This tells you exactly what happened last session and what to watch out for.

### 2. Project Memory
```
PROJECT_MEMORY.md
```
Five-minute full-project overview: architecture, rules, common mistakes, file map.

### 3. Project State
```
PROJECT_STATE.md
```
Current completion percentages, all active bugs, priorities, and blocked work.  
**Do not build on a broken system without understanding its known issues first.**

### 4. Project Constitution
```
PROJECT_CONSTITUTION.md
```
The governing rules. Defines how decisions are made, what requires human approval, and what is never permitted.

### 5. Game Bible
```
docs/GAME_BIBLE.md
```
What the game is — every confirmed mechanic, design pillar, and canon rule. Read before touching any gameplay system.

### 6. AI Continuation Guide
```
docs/AI_CONTINUATION_GUIDE.md
```
Coding standards, module ownership map, established patterns, and anti-patterns. Read before writing any code.

### 7. Relevant System Documentation
```
docs/systems/<relevant-system>.md
```
Only the specific system(s) you will be working in. Do not skip this step.

---

## Step 2 — Pre-Development Checklist

Complete this before writing a single line of code.

- [ ] Read the latest handoff document
- [ ] Read `PROJECT_STATE.md` — know what is broken and what is in progress
- [ ] Confirm exactly what work has been requested
- [ ] Identify every system that will be affected
- [ ] Read the `docs/systems/` doc for each affected system
- [ ] Check `docs/known_issues.md` — does your work touch a known bug?
- [ ] Check `docs/AI_CONTINUATION_GUIDE.md` module ownership table — does a module for this already exist?
- [ ] Check `DESIGN_DECISIONS.md` — has a related architectural decision already been made?
- [ ] Determine which documentation files will need updating when the work is done

---

## Step 3 — Development Rules

Follow these during every session, without exception.

| Rule | Detail |
|---|---|
| **Understand before editing** | Read any file you will modify before touching it |
| **Preserve existing architecture** | Extend the existing patterns; do not invent new ones |
| **Reuse existing systems** | Check the module ownership table before creating anything new |
| **No duplicate implementations** | If it exists, use it |
| **Use the event bus for side effects** | Never import a module to trigger a side effect — use `event_bus.emit()` |
| **All state goes in `world_state`** | Never store mutable game state in module-level variables |
| **Follow coding standards** | See `docs/coding_standards.md` for formatting, naming, and structure rules |
| **Never invent lore** | If it is not in the codebase or Game Bible, it does not exist — mark it ⚠️ NOT YET DEFINED |
| **Never invent mechanics** | If a mechanic is not implemented, it is not a mechanic — it is a proposal |
| **New `world_state` keys need migration** | Every new key must be added to `ensure_world_state_defaults()` in `world_state.py` |
| **New events need documentation** | Every new event must be added to `docs/systems/event_bus.md` |
| **Keep documentation synchronized** | Update docs in the same session as the code change — never defer |

---

## Step 4 — When to Stop and Ask for Human Approval

**Pause immediately and ask** before making any of the following changes:

- Major gameplay redesign or removal of a confirmed mechanic
- Changes to established canon (characters, world rules, game systems)
- Removal of a major system or module
- Breaking architectural changes (restructuring how modules communicate)
- Large-scale refactors not explicitly requested
- Save format changes (anything that breaks existing save files)
- Security-sensitive changes
- Any decision where reasonable alternatives exist and you are unsure which to choose

**When uncertain:**
1. Stop working.
2. Document the issue and both sides of the decision.
3. State your recommended option with reasoning.
4. Ask for clarification.

Do not silently choose. Do not guess.

---

## Step 5 — Conflict Resolution

If documentation and code disagree:

1. **Do not immediately change either.**
2. Identify which is more recent (check `CHANGELOG.md` and `docs/handoffs/`).
3. Write a clear description of the conflict.
4. Add it to `docs/known_issues.md` if not already there.
5. Ask for clarification before resolving it.

The code is the ground truth for what currently works.  
The Game Bible is the ground truth for what the game is meant to be.  
If they conflict, document the discrepancy — do not quietly patch one to match the other.

---

## Step 6 — Post-Development Shutdown Checklist

Complete every applicable item before ending a session.

### Code Quality
- [ ] All modified Python files pass syntax check (`python -m py_compile <file>`)
- [ ] All modules import cleanly (no circular imports introduced)
- [ ] Modified systems tested manually for basic functionality

### Documentation
- [ ] `PROJECT_STATE.md` updated (completion %, bug list, priorities reflect current reality)
- [ ] `CHANGELOG.md` updated if this is a milestone-level change
- [ ] `DESIGN_DECISIONS.md` updated if a significant architectural decision was made
- [ ] `docs/GAME_BIBLE.md` updated if any gameplay mechanic was added or changed
- [ ] `docs/architecture.md` updated if module relationships changed
- [ ] Relevant `docs/systems/` file updated for any system modified
- [ ] `PROJECT_MEMORY.md` updated if onboarding information changed
- [ ] `docs/systems/event_bus.md` updated if new events were added
- [ ] `docs/systems/world_state.md` updated if new state keys were added

### Handoff
- [ ] New handoff document created in `docs/handoffs/` using `HANDOFF_TEMPLATE.md`
- [ ] Handoff index in `docs/handoffs/README.md` updated with the new entry
- [ ] `PROJECT_STATE.md` "Recently Completed Work" updated to reference the new handoff

---

## Quick Reference — Key Files

| File | One-Line Purpose |
|---|---|
| `main.py` | Entry point |
| `game_loop.py` | Command dispatcher — the hub of all gameplay |
| `world_state.py` | All mutable state + helper functions + migration guard |
| `event_bus.py` | Cross-module communication (always use this for side effects) |
| `dm_brain.py` | AI Director pacing and story pressure |
| `llm_bridge.py` | Only place for LLM calls (currently mocked) |
| `save_manager.py` | Manual player save/load |
| `state_manager.py` | Auto-save / state persistence |
| `combat.py` | Turn-based combat engine |
| `quests.py` | Quest CRUD and lifecycle |
| `faction_manager.py` | Faction reputation and events |

---

## Quick Reference — Critical Rules

```
1. world_state.py is the single source of truth for all game state.
2. event_bus.py is the only correct channel for cross-module side effects.
3. llm_bridge.py is the only place for LLM/AI text generation calls.
4. ensure_world_state_defaults() must include every world_state key.
5. Never import from legacy root modules: factions.py, regions.py, loot.py, memory.py
6. Never invent lore, mechanics, or characters not in the codebase.
7. Document before redesigning. Update docs in the same session as code.
```

---

## Quick Reference — Status Markers

Use these consistently across all documentation and code comments:

| Marker | Meaning |
|---|---|
| **[CONFIRMED]** | Implemented and verified in code |
| **[INFERRED]** | Derived from code patterns; likely intent |
| **[PLANNED]** | On the roadmap; not yet implemented |
| **⚠️ NOT YET DEFINED** | No decision made; no implementation exists |

---

## Quick Reference — Active Known Issues

As of July 2026. Full list: [`docs/known_issues.md`](docs/known_issues.md)

| Severity | Issue |
|---|---|
| 🔴 | `validate_world_state()` fails on new game — `npcs` key never initialized |
| 🟠 | `player.py` singleton vs `world_state["player"]` can desync after combat |
| 🟠 | `rebels` faction in state but absent from `faction_manager.FACTIONS` |
| 🟡 | Dual region discovery state (two separate trackers) |
| 🟡 | Quest `type` field absent — faction +10 bonus never fires |
| 🟡 | NPC changes not persisted in saves |

---

## Full Documentation Map

```
AI_START_HERE.md              ← you are here (session entry point)
PROJECT_CONSTITUTION.md       ← permanent governance
PROJECT_MEMORY.md             ← full project quick-start
PROJECT_STATE.md              ← current health and priorities
DESIGN_DECISIONS.md           ← architectural decision record
CHANGELOG.md                  ← development history
README.md                     ← repository overview

docs/
├── README.md                 ← documentation index
├── GAME_BIBLE.md             ← game design canon
├── AI_CONTINUATION_GUIDE.md  ← AI contributor rules
├── architecture.md           ← module map and data flow
├── coding_standards.md       ← code style guide
├── known_issues.md           ← bug and tech debt registry
├── roadmap.md                ← future development plan
├── dependencies.md           ← package inventory
├── systems/                  ← per-system deep dives (11 files)
│   ├── world_state.md
│   ├── combat.md
│   ├── ai_director.md
│   ├── save_system.md
│   ├── event_bus.md
│   ├── quests.md
│   ├── factions_economy.md
│   ├── progression_skills.md
│   ├── inventory_equipment.md
│   ├── npcs_companions.md
│   └── world_regions.md
└── handoffs/                 ← session records (read newest first)
    ├── README.md
    ├── HANDOFF_TEMPLATE.md
    └── 2026-07-30-documentation-session.md
```

---

## A Note on This Repository's Standards

This is a documentation-first project. A feature without documentation is considered incomplete. A code change without a documentation update is considered unfinished. Every session ends with a handoff document.

This is not bureaucracy — it is how a project survives across multiple AI assistants and development sessions without losing its identity, architecture, or accumulated knowledge.

**Leave this repository in a better state than you found it.**
