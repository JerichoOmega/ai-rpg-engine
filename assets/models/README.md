# Production 3D Models

Canonical **production/runtime 3D game assets** (meshes + materials + textures),
kept **separate** from reference/canon art. Every model here **derives from** a
canonical reference sheet under [`assets/reference/`](../reference/README.md)
(see the pipeline in [`docs/canon/Pipeline.md`](../../docs/canon/Pipeline.md) and
the standards in [`docs/canon/Asset_Standards.md`](../../docs/canon/Asset_Standards.md)).

> **Reference vs. model.** `assets/reference/` holds immutable 2D design source
> art (the visual contract). `assets/models/` holds the actual 3D assets the game
> loads. The reference is **not** a substitute for the model, and the model does
> not replace the reference — they are related project assets.

## Source format
- **GLB** (binary glTF 2.0) is the canonical 3D source/interchange format for this
  project. Preserve GLBs as delivered — mesh, UVs, materials, and embedded
  textures. Do **not** convert to FBX/OBJ, regenerate, remodel, retopologize, or
  swap textures without recording a new canonical revision first (Asset_Standards §4).

## Naming
- `snake_case`, `<asset_id>.glb`, matching the logical asset identifier, e.g.
  `treasure_chest.glb`, `wooden_barrel.glb`, `stone_well.glb`.
- The paired 2D reference uses `<asset_id>_reference_v<N>.png` under
  `assets/reference/<category>/` (repo reference-versioning convention).

## Categories
Mirrors the reference category layout; folders are added as assets arrive.

| Folder | Purpose | Reference source |
|---|---|---|
| `props/` | World objects, interactables, containers | `assets/reference/props/` |

Each category folder has its own `README.md` acting as the asset registry (one
row per asset), following the same table-registry convention used across
`assets/reference/`.

## Godot readiness
Godot is the eventual target engine, but **no Godot project exists yet** (see
[`engine/godot/README.md`](../../engine/godot/README.md), reserved/empty by
design). These GLBs are organized and documented so a future Godot import
(`docs/architecture/GODOT_SCENE_MAPPING.md`) can consume them directly. Do not
build a stand-in rendering system to preview them.
