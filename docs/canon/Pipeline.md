# Production Pipeline — from Canon to Game Asset

Every downstream asset traces back to the **canonical reference sheet**. The
reference sheet is the contract; each stage below consumes the previous stage's
output and must not silently deviate from canon (see
[`Asset_Standards.md`](Asset_Standards.md)).

```
Concept Art
    ↓
Canonical Reference Sheet        ← the single source of truth (assets/reference/)
    ↓
3D Model (Tripo)                 ← generated from the reference turnaround
    ↓
Blender Cleanup                  ← retopo, UVs, material authoring from swatches
    ↓
Rigging
    ↓
Godot Import                     ← runtime model + materials
    ↓
Animation
    ↓
UI Portrait                      ← cropped/derived, identity preserved
    ↓
Marketing Render
    ↓
Final Game Asset
```

## Stage notes
| Stage | Input | Must preserve | Output location (suggested) |
|---|---|---|---|
| Concept Art | Brief | — | working/concept (not canon until approved) |
| **Canonical Reference Sheet** | Approved concept | Immutable original | `assets/reference/<category>/` |
| 3D Model (Tripo) | Reference turnaround | Silhouette, proportions | production model source |
| Blender Cleanup | Raw model | Palette, costume details | production model source |
| Rigging | Clean model | Proportions | production |
| Godot Import | Rigged model | Materials/colour | runtime assets |
| Animation | Rigged model | Weight/identity | runtime assets |
| UI Portrait | Reference / model | Face + iconography | UI assets |
| Marketing Render | Model / reference | Full identity | `assets/reference/marketing/` derivatives |

## Rules
1. If a stage needs to change canon, stop and record a **new canonical revision**
   first (see the revision system in `Asset_Standards.md`), then continue.
2. Downstream production/runtime assets are **not** stored in
   `assets/reference/` — that folder holds reference/canon only.
3. Each character's per-stage notes live under **Modeling Notes / UI Portrait
   Notes / Animation Notes** in `Characters.md`.

---

## Expanded Character Production Pipeline (Concept → Playable Character)

The full studio pipeline for a major character. **Every stage derives from the
previous canonical stage** — nothing downstream reinterprets canon.

```
Concept
   ↓
Lore                     ← docs/heroes/, docs/characters/ (narrative truth)
   ↓
Character Design
   ↓
Canonical Reference Sheet ← the contract (assets/reference/characters/)
   ↓
Hero Render
   ↓
Turnaround
   ↓
Tripo                    ← 3D model generated from the turnaround
   ↓
Blender                  ← retopo, UVs, materials from the palette/PBR set
   ↓
Rigging
   ↓
Godot                    ← runtime model + materials
   ↓
Animation                ← idle + combat, expressing the character's identity
   ↓
UI                       ← portraits derived from canon
   ↓
Marketing                ← promo renders, identity preserved
   ↓
Playable Character
```

Governance:
- Track each character's position in this pipeline in
  [`Character_Production_Status.md`](Character_Production_Status.md).
- The required deliverables and their rationale are in
  [`Character_Production_Bible.md`](Character_Production_Bible.md).
- If any stage must change canon, record a **new canonical revision first**
  (see `Asset_Standards.md`) before producing the derivative.
