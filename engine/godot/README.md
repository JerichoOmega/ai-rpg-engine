# `engine/godot/` — RESERVED (future Godot presentation layer)

> **RESERVED — empty on purpose.** No Godot project, scenes, or scripts exist here
> yet. This is the **documented destination** for the eventual Godot presentation
> layer. The current game (terminal) is unaffected.

**Purpose (future).** The Godot project that renders the engine-agnostic `core/`:
scenes, nodes, UI, input, animation, audio, VFX, camera, navigation. Godot reads
**state**, plays **events**, and emits **intents** — it computes **no game rules**.

**When work starts here, follow:**
- Scene/node/signal mapping: [`../../docs/architecture/GODOT_SCENE_MAPPING.md`](../../docs/architecture/GODOT_SCENE_MAPPING.md)
- Data contracts: [`../../docs/architecture/ENGINE_INTERFACES.md`](../../docs/architecture/ENGINE_INTERFACES.md)
- Layer laws: [`../../docs/architecture/LAYER_RULES.md`](../../docs/architecture/LAYER_RULES.md)
- Roadmap (phase P5): [`../../docs/architecture/GODOT_MIGRATION_PLAN.md`](../../docs/architecture/GODOT_MIGRATION_PLAN.md)

The Python core remains the source of truth for rules during Godot bring-up; the
headless showcase harness is the parity oracle (core owns RNG; Godot replays).
