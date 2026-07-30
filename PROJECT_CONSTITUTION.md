# PROJECT_CONSTITUTION.md

> **The governing document for this repository.**  
> This is not a Game Bible. It is not technical documentation. It is not a roadmap.  
> It is the permanent set of principles, rules, and decision-making processes that govern how this project evolves — regardless of who is working on it.  
>  
> Every future contributor — human or AI — must read and follow this document.  
> Last updated: July 2026.

---

## Article I — Mission Statement

This project is an **AI-driven terminal RPG** with a long-term vision: to create a deeply narrative, systems-rich single-player game where an intelligent AI Director shapes every session into a unique, reactive story.

The mission is not simply to ship features. It is to build a game that:

- **Puts the player first.** Every system exists to serve the player's experience — immersion, agency, narrative weight, and the feeling that the world responds to their choices.
- **Sustains itself over time.** Code, architecture, and documentation must remain legible and maintainable years after any single contributor has moved on.
- **Documents its own knowledge.** This project treats documentation as a first-class product, not an afterthought. A contributor who reads the documentation should be able to understand, extend, and preserve the project without access to any prior conversation.
- **Scales without breaking.** New systems and content must integrate cleanly into the existing architecture rather than around it. Growth compounds value; it does not compound complexity.
- **Preserves its identity.** The creative vision, design philosophy, and tone of the game are as important as any line of code. Technical decisions serve the game — not the other way around.

---

## Article II — Core Principles

These principles are permanent. They govern every decision made in this project. When in doubt, return to them.

### 1. Preserve the Game's Identity
Every technical and design decision must serve the game's vision. Before implementing anything, ask: *does this serve the player experience?* If not, reconsider.

### 2. Understand Before Editing
No contributor — human or AI — should modify code or documentation without first understanding what it does, why it exists, and what depends on it. Read before writing.

### 3. Favor Clarity Over Cleverness
Code should be written to be understood by the next person who reads it. Clever solutions that are difficult to follow are worse than simple solutions that are easy to maintain. Readability is not optional.

### 4. Build Modular, Decoupled Systems
Systems communicate through defined interfaces (the event bus). Direct cross-module coupling is avoided except where necessary for return values. Each module owns exactly one domain.

### 5. Document Before Redesigning
If a system needs to be redesigned, document the current behavior and the reasons for the change before touching any code. Never redesign silently.

### 6. Never Remove Working Functionality Without Justification
Deleting a working feature, module, or system requires explicit justification and documentation of the removal in `CHANGELOG.md`. Silent removal is prohibited.

### 7. Preserve Backward Compatibility Whenever Practical
Save files, APIs, and data formats should remain compatible with older versions unless a breaking change is explicitly necessary, justified, documented, and migrated via `ensure_world_state_defaults()`.

### 8. Avoid Unnecessary Complexity
The simplest solution that correctly solves the problem is preferred. Premature generalization, unnecessary abstraction, and over-engineering are considered defects.

### 9. Documentation Evolves With the Code
Documentation that does not reflect the current codebase is worse than no documentation — it actively misleads. Every significant code change must be followed by a documentation update.

### 10. Prioritize Sustainability Over Speed
A shortcut that creates technical debt, breaks a system, or leaves documentation stale is not faster — it is slower, because it will have to be undone. Do the work correctly the first time.

---

## Article III — Sources of Truth

Each document in this project has a defined authority. No document overrides another within its domain.

| Document | Authority | Location |
|---|---|---|
| **`PROJECT_MEMORY.md`** | AI and developer quick-start onboarding summary | Root |
| **`PROJECT_STATE.md`** | Current implementation status, active bugs, priorities | Root |
| **`DESIGN_DECISIONS.md`** | Historical reasoning behind major architectural choices | Root |
| **`CHANGELOG.md`** | Record of all significant changes, by milestone | Root |
| **`PROJECT_CONSTITUTION.md`** | Permanent governance — how the project evolves | Root |
| **`docs/GAME_BIBLE.md`** | **Authoritative source for gameplay, mechanics, vision, and all canon** | `docs/` |
| **`docs/AI_CONTINUATION_GUIDE.md`** | Rules and patterns for future AI contributors | `docs/` |
| **`docs/architecture.md`** | Technical architecture, module relationships, data flow | `docs/` |
| **`docs/coding_standards.md`** | Code style, naming conventions, formatting rules | `docs/` |
| **`docs/roadmap.md`** | **Future plans only** — nothing in this file is implemented | `docs/` |
| **`docs/known_issues.md`** | Current confirmed bugs and technical debt | `docs/` |
| **`docs/systems/`** | Deep-dive documentation for each major system | `docs/systems/` |
| **The codebase itself** | Authoritative source for current technical behavior and implementation | Root `.py` files |

### Conflict Resolution Hierarchy

When documents disagree with each other or with the code:

1. **The code is the ground truth for what currently works.**
2. **The Game Bible is the ground truth for what the game is meant to be.**
3. **If code and Game Bible conflict:** document the discrepancy in `docs/known_issues.md`. Do not silently resolve it. Request clarification before making changes.
4. **Roadmap items are not implemented features.** A feature listed in the roadmap does not exist in the game.

---

## Article IV — Canon Policy

Canon is the established truth of this project. It must be protected.

### What Is Canon

- Gameplay mechanics that exist in the codebase — **[CONFIRMED]**
- Design decisions documented in `DESIGN_DECISIONS.md` — **[CONFIRMED]**
- Game mechanics described in `docs/GAME_BIBLE.md` that are also in the code — **[CONFIRMED]**

### What Is Not Canon

- Roadmap items — these are **[PLANNED]**, not implemented
- Code patterns that appear consistent but are undocumented — these are **[INFERRED]** until confirmed
- Lore, characters, factions, history, or world details not present in the codebase or Game Bible — **⚠️ NOT YET DEFINED**
- Ideas discussed but not committed — not canon until implemented and documented

### Canon Rules — Absolute Prohibitions

- **Never invent lore.** If world history, mythology, faction backstory, or character origins are not in the codebase or Game Bible, they do not exist. Mark them ⚠️ NOT YET DEFINED.
- **Never invent gameplay mechanics.** If a mechanic is not implemented, it is not a mechanic — it is a proposal.
- **Never silently redefine an established system.** Changing how a system works without documenting the change corrupts the canon.
- **Never present planned features as existing features.** Roadmap items are clearly distinguished from implemented ones.

### Status Markers (Required in All Documentation)

| Marker | Meaning |
|---|---|
| **[CONFIRMED]** | Verified in code; definitively implemented |
| **[INFERRED]** | Derived from code patterns; likely intent but not explicitly stated |
| **[PLANNED]** | On the roadmap; not yet implemented |
| **⚠️ NOT YET DEFINED** | No decision made; no implementation exists; do not treat as real |

---

## Article V — Change Management

Every change to this project — code or documentation — must follow these rules.

### Minor Changes
*Bug fixes, small corrections, adding content within an existing system.*
- Make the change.
- If the change affects a documented behavior, update the relevant doc.
- Update `PROJECT_STATE.md` if a known issue is resolved.

### Major Changes
*New systems, architectural changes, changes to existing system behavior, removing features.*

**Before writing code:**
1. Read the relevant system documentation in `docs/systems/`.
2. Read `docs/known_issues.md` — does the change interact with a known bug?
3. Consult `DESIGN_DECISIONS.md` — has a related decision already been made?
4. If proposing a new architectural decision, document it in `DESIGN_DECISIONS.md` first.

**After completing the change:**
1. Update the relevant `docs/systems/` document.
2. Update `docs/architecture.md` if module relationships changed.
3. Update `docs/GAME_BIBLE.md` if gameplay behavior changed.
4. Update `PROJECT_STATE.md` (completion %, bug list, priorities).
5. Update `CHANGELOG.md` with a milestone entry.
6. Update `PROJECT_MEMORY.md` if onboarding information has changed.

### Breaking Changes
- A breaking change is any change that makes existing save files incompatible, removes a public function, or changes an event payload.
- Breaking changes **must** be documented in `CHANGELOG.md` before or simultaneously with implementation.
- Breaking save format changes **must** be handled by `ensure_world_state_defaults()` in `world_state.py`.

### Deprecation
- Systems or functions being retired must be marked as deprecated in their source file with a comment explaining what replaces them.
- Deprecated systems must be listed in `docs/known_issues.md`.
- Deprecated systems are **never silently removed** — the removal itself is a documented milestone.

---

## Article VI — AI Development Rules

This project is developed with the assistance of AI contributors. The following rules govern AI behavior at all times.

### Before Making Any Change

1. **Read `PROJECT_MEMORY.md` first.** Understand the project in full before touching anything.
2. **Read `PROJECT_STATE.md`.** Know what is broken, what is in progress, and what the priorities are.
3. **Read the relevant system doc** in `docs/systems/` for any system being modified.
4. **Read `docs/known_issues.md`.** Do not accidentally fix a known issue as a side effect of unrelated work, and do not build on broken systems without acknowledging the breakage.
5. **Read `DESIGN_DECISIONS.md`** before any refactor or architectural change.

### While Working

- **Understand before editing.** Never modify code that you have not read and understood.
- **Reuse existing modules.** Before creating a new module or function, verify it does not already exist. The module ownership table in `docs/AI_CONTINUATION_GUIDE.md` is the reference.
- **Use the event bus for cross-module side effects.** Do not create direct imports between modules for the purpose of triggering behavior.
- **Store all mutable state in `world_state`.** Never store game state in module-level variables.
- **Preserve naming conventions.** Match the style of the file being edited. See `docs/coding_standards.md`.
- **Never assume missing information.** If something is unclear, mark it **[INFERRED]** and document the assumption. Do not silently invent answers.
- **Avoid unnecessary rewrites.** Refactoring working code solely for aesthetic preference is not permitted without explicit instruction.

### After Completing Work

- Update documentation as required by Article V.
- If a new `world_state` key was added, confirm it is in `ensure_world_state_defaults()`.
- If a new event was added, confirm it is documented in `docs/systems/event_bus.md`.
- If a design decision was made, add it to `DESIGN_DECISIONS.md`.

### When Uncertainty Exists

- Document alternatives considered.
- Recommend a preferred option with reasoning.
- Do not silently choose one path when multiple reasonable options exist.
- Use the status markers — **[CONFIRMED]**, **[INFERRED]**, **[PLANNED]**, **⚠️ NOT YET DEFINED** — to be explicit about confidence level.

---

## Article VII — Documentation Policy

Documentation is a first-class deliverable in this project. It is not optional and it is not done after the fact.

### The Documentation-First Rule

For any new system or significant feature, documentation is written **before or alongside** the code — not after. A feature without documentation is considered incomplete.

### Maintenance Obligations

| Trigger | Required Updates |
|---|---|
| New gameplay mechanic added | `docs/GAME_BIBLE.md`, relevant `docs/systems/` file |
| Existing mechanic changed | `docs/GAME_BIBLE.md`, relevant `docs/systems/` file, `CHANGELOG.md` |
| New module created | `docs/architecture.md`, `docs/systems/` (new file), `PROJECT_MEMORY.md` module table |
| Architecture changed | `docs/architecture.md`, `CHANGELOG.md`, `DESIGN_DECISIONS.md` |
| Bug fixed | `docs/known_issues.md` (mark resolved), `PROJECT_STATE.md`, `CHANGELOG.md` |
| New bug discovered | `docs/known_issues.md` (add entry with severity), `PROJECT_STATE.md` |
| New world_state key added | `docs/systems/world_state.md`, `ensure_world_state_defaults()` |
| New event added | `docs/systems/event_bus.md` |
| Significant design decision made | `DESIGN_DECISIONS.md` |
| Major milestone completed | `PROJECT_STATE.md`, `CHANGELOG.md`, `PROJECT_MEMORY.md` (if onboarding changed) |

### Documentation Quality Standards

Every documentation file must include, where applicable:
- **Purpose** — what this document covers and why it exists
- **Current Implementation** — what actually exists in code (not aspirational)
- **Design Rationale** — why it was built this way
- **Rules** — explicit rules that constrain this system
- **Related Systems** — links to related documentation
- **Future Expansion** — what could be added, clearly marked [PLANNED] or ⚠️ NOT YET DEFINED
- **Revision History** — when it was last meaningfully updated

---

## Article VIII — Code Quality Principles

These principles apply to all code written for this project.

| Principle | Rule |
|---|---|
| **Readability** | Code is written to be read by the next person, not optimized for the writer |
| **Modularity** | Each module has exactly one domain of responsibility |
| **Low coupling** | Modules depend on `world_state` and `event_bus`, not on each other directly |
| **High cohesion** | Functions within a module are tightly related to that module's domain |
| **Minimal duplication** | If the same logic appears twice, extract it. The third appearance demands extraction. |
| **Consistent naming** | Match the naming style of the surrounding file and codebase |
| **Explicit failure** | Code that fails must fail loudly — no silent fallbacks that mask errors |
| **No dead code** | Unused imports, unreachable functions, and commented-out blocks are removed |
| **Self-documenting** | Functions and variables are named to describe what they do, not how they do it |

See `docs/coding_standards.md` for concrete examples and enforcement rules.

---

## Article IX — Decision-Making Process

When multiple valid solutions exist, apply this decision framework:

### Selection Criteria (in order of priority)

1. **Preserves the existing architecture** — does it work within the established patterns?
2. **Minimizes technical debt** — does it reduce or at least not increase the debt in `docs/known_issues.md`?
3. **Maintains backward compatibility** — does it break existing save files, APIs, or documented behavior?
4. **Improves maintainability** — will the next contributor understand it more easily?
5. **Improves readability** — is the code clearer than the alternative?
6. **Improves scalability** — does it make future growth easier, not harder?

### When Uncertainty Remains

- Document the alternatives considered.
- State a recommended option with explicit reasoning.
- Do not silently choose — surface the decision.
- If the decision has architectural significance, add it to `DESIGN_DECISIONS.md`.

### Escalation

Some decisions should not be made unilaterally by an AI contributor:

- **Removing a confirmed gameplay feature** — requires explicit instruction
- **Choosing a real LLM model or API** — requires explicit instruction
- **Changing the canonical player state representation** (`player.py` vs `world_state["player"]`) — requires explicit instruction and a documented decision
- **Deleting legacy modules** (`factions.py`, `regions.py`, `loot.py`, `memory.py`) — requires explicit confirmation
- **Establishing new world lore** (world name, history, factions background) — requires creative direction from the project owner

---

## Article X — Future Expansion Protocol

When adding a new system to the project:

### Step 1 — Documentation First
Before writing code, create or update the relevant documentation:
- Write a brief design document (even one page) describing what the system does and how it fits into the architecture.
- Identify which existing systems it will interact with.
- Add it to the roadmap if it is planned; do not add it to the Game Bible until it is implemented.

### Step 2 — Integration Planning
- Identify all event bus events the new system will emit or subscribe to.
- Identify all `world_state` sections the system will read from or write to.
- Confirm that no existing module already owns this domain (check `docs/AI_CONTINUATION_GUIDE.md` module ownership table).

### Step 3 — Compatibility Review
- Confirm new `world_state` keys are added to `ensure_world_state_defaults()`.
- Confirm new events are documented in `docs/systems/event_bus.md`.
- Confirm existing save files will load correctly after the change.

### Step 4 — Architecture Review
- The new module must follow the single-domain ownership rule.
- Communication with other modules must go through `event_bus` for side effects.
- The new module must not import from legacy root modules (`factions.py`, `regions.py`, `loot.py`, `memory.py`).

### Step 5 — Implementation
- Write the code following `docs/coding_standards.md`.
- Keep functions small and named for their behavior.
- Write no logic inside `llm_bridge.py` — only text generation calls.

### Step 6 — Documentation Updates
After implementation is complete:
- Update `docs/architecture.md` to include the new module.
- Create or update the relevant `docs/systems/` file.
- Update `docs/GAME_BIBLE.md` if the system introduces new gameplay mechanics.
- Add a `CHANGELOG.md` entry.
- Update `PROJECT_STATE.md` completion percentages.
- Add any new design decisions to `DESIGN_DECISIONS.md`.

---

## Article XI — Final Declaration

This Constitution governs **how the project evolves.**

The **Game Bible** (`docs/GAME_BIBLE.md`) governs **what the game is.**

The **codebase** governs **how the game currently works.**

The **documentation** governs **what is known and preserved.**

These four authorities are complementary, not competing. When they align, the project is healthy. When they diverge, the project has identified its next most important task: resolving the divergence, not ignoring it.

Every future contributor — human or AI — who works on this project accepts the following obligations:

1. Read before writing.
2. Preserve what works.
3. Document what changes.
4. Never invent what is not real.
5. Surface uncertainty rather than silently resolve it.
6. Leave the project in a better state than you found it.

This project is a long-term endeavor. Its quality, consistency, and sustainability depend not on any single contributor, but on the collective discipline of everyone who works on it following these shared principles.

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial constitution created; cross-referenced against all existing documentation |
