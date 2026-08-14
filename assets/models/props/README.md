# Props — Production 3D Models

Canonical 3D assets for world objects, interactables, and containers. GLB
(binary glTF 2.0) is the source format; preserve as delivered (mesh, UVs,
materials, embedded textures). See [`../README.md`](../README.md) and
[`docs/canon/Asset_Standards.md`](../../../docs/canon/Asset_Standards.md).

## Asset registry

| ID | Name | File | Type | Category | Source Format | Reference Image | Description |
|---|---|---|---|---|---|---|---|
| `treasure_chest` | Treasure Chest | `treasure_chest.glb` | 3D Model | Props | GLB | [`assets/reference/props/treasure_chest_reference_v1.png`](../../reference/props/treasure_chest_reference_v1.png) | Stylized fantasy treasure chest for the tactical RPG. |

## `treasure_chest`

- **Logical identifier:** `treasure_chest`
- **Canonical 3D asset:** `assets/models/props/treasure_chest.glb`
- **2D design reference:** `assets/reference/props/treasure_chest_reference_v1.png`
- **Source format:** GLB (binary glTF 2.0)
- **Design direction (from the 2D reference):** domed-lid wooden chest with dark
  iron reinforcement banding, gold/brass diamond studs along the frame, a
  brass shield-shaped keyhole lock plate, and a side ring handle — stylized
  fantasy game-art silhouette.

### GLB contents (inspected)
| Property | Value |
|---|---|
| Exporter / version | Khronos glTF Blender I/O v4.1.63 · glTF 2.0 |
| Scenes / nodes / meshes | 1 / 1 / 1 |
| Mesh | `output_unwrapped`, 1 primitive, triangles |
| Geometry | 2,592 vertices · 2,643 triangles |
| Vertex attributes | POSITION, NORMAL, TANGENT, TEXCOORD_0 (UVs present) |
| Material | `BakedPBR` — metallic-roughness, double-sided, OPAQUE |
| Textures (embedded PNG, 2048×2048) | base_color · normal · metallic-roughness · ambient-occlusion |
| Animations / skins / cameras | none |
| Bounding box (local units) | ~0.823 × 0.657 × 0.678 |
| Self-contained | Yes — all textures embedded in the binary buffer (no external files) |

> The GLB is **authoritative** for the actual 3D implementation. The 2D reference
> is the visual/design source. No significant discrepancy was found between the
> model and the reference; if one is discovered later, record a new canonical
> revision rather than silently altering the model (Asset_Standards §4).
