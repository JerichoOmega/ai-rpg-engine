# `core/` — RESERVED (engine-agnostic game logic)

> **RESERVED — documented destination, not yet populated.** This directory holds
> **no code today** and is **not an importable package** (intentionally no
> `__init__.py`). Do not import from it. The live codebase is unchanged.

**Purpose (future).** The engine-agnostic game *rules* — pure logic with no
rendering, UI, scenes, animation, camera, audio, or input. Presentation depends on
`core/`; `core/` depends on nothing above it.

**Planned contents (see the plan):** `combat/` (promoted from `tactical/`),
`characters/`, `ai/`, `systems/` (status, abilities, inventory, economy),
`quests/`, `world/` (world state, regions, factions, relationships, events),
`save/`.

**Rules & migration path:**
- Laws: [`../docs/architecture/LAYER_RULES.md`](../docs/architecture/LAYER_RULES.md)
- Contracts: [`../docs/architecture/ENGINE_INTERFACES.md`](../docs/architecture/ENGINE_INTERFACES.md)
- Roadmap: [`../docs/architecture/GODOT_MIGRATION_PLAN.md`](../docs/architecture/GODOT_MIGRATION_PLAN.md)

Population happens **incrementally**, with the full test suite green after each
step and old import paths preserved via re-export shims. No files are moved yet.
