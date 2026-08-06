# `engine/` — RESERVED (presentation adapters)

> **RESERVED — documented destination, not yet populated.** This directory holds
> **no code today** and is **not an importable package** (intentionally no
> `__init__.py`). Do not import from it. The live codebase is unchanged.

**Purpose (future).** Thin **presentation adapters** that consume the engine-agnostic
`core/` via **state + events** and send **intents** back. An adapter may be replaced
without touching game rules.

**Planned contents:**
- `terminal/` — today's ASCII driver (`tactical/render.py` + `tactical/session.py`
  would move here).
- `godot/` — the future Godot presentation layer (see `godot/README.md`).

**Rules & mapping:**
- Laws: [`../docs/architecture/LAYER_RULES.md`](../docs/architecture/LAYER_RULES.md)
- Godot mapping: [`../docs/architecture/GODOT_SCENE_MAPPING.md`](../docs/architecture/GODOT_SCENE_MAPPING.md)
- Roadmap: [`../docs/architecture/GODOT_MIGRATION_PLAN.md`](../docs/architecture/GODOT_MIGRATION_PLAN.md)

No files are moved yet; extraction happens incrementally with tests green.
