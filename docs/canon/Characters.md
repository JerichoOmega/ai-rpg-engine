# Canonical Character Reference — Elyndor

This document is the **visual canon** for Elyndor characters: which reference
sheets are authoritative and how all future art must derive from them. The
linked reference sheets are the single source of truth for a character's
appearance. All future art (3D models, portraits, concept art, animation,
equipment layers, marketing renders, UI images) must derive from these sheets
and must not reinterpret them unless a future canonical design revision
explicitly supersedes them (see [`Asset_Standards.md`](Asset_Standards.md)).

Reference assets live under `assets/reference/characters/` and are **reference
material only** — not gameplay sprites or production textures. They are stored
at original resolution, uncompressed and unaltered.

> Narrative lore (backstory, dialogue, relationships) is **not** authored here.
> It lives in `docs/characters/`, `docs/heroes/`, `docs/companions/`,
> `docs/npcs/`. Unknown fields below use clearly-labelled `_TBD_` placeholders —
> do not invent lore.

Use [`_character_template.md`](_character_template.md) when adding a new
character.

---

## Talos

### Status
**Canonical** — primary visual reference for all future Talos art and modeling.

### Reference Assets
| Version | File | Resolution | Notes |
|---|---|---|---|
| Talos (Cloak) | [`assets/reference/characters/talos_cloak.png`](../../assets/reference/characters/talos_cloak.png) | 1672 × 941 | Full turnaround sheet — front/side/back rotations, head studies, weapon + shield callouts, material/colour swatches. Navy hooded cloak over shoulders/back. |
| Talos (No Cloak) | [`assets/reference/characters/talos_no_cloak.png`](../../assets/reference/characters/talos_no_cloak.png) | 1024 × 1536 | Full-body hero portrait, no cloak — armour, navy tabard, longsword, sun-sigil shield. |

### Visual Identity
- **Primary colours:** gunmetal / dark steel plate, brass–gold trim, navy cloth
  (tabard + cloak), brown leather strapping.
- **Silhouette:** broad, heavily-armoured frame in a grounded sword-and-shield
  stance; (cloak version) flowing hooded cloak reads strongly from behind.
- **Iconography:** radiant **sun sigil** on the shield face and tabard trim.
- **Face:** pointed (elven) ears, short dark hair, trimmed beard, facial scar.

### Design Intent (preserve unless a canonical revision changes it)
- Maintain **silhouette & proportions** — bulky guardian frame, board-and-sword.
- Maintain **costume details** — layered dark plate with brass/gold trim and
  leather straps; navy tabard and (cloak variant) navy hooded cloak; segmented
  pauldrons, belt, greaves.
- Maintain the **colour palette** (see the swatch strip on the cloak sheet).
- Maintain the **sun sigil** iconography and the **elven ears / scar** identity.

### Equipment (as depicted in the reference sheets)
- Longsword (one-handed), large round/heater shield bearing the sun sigil,
  full plate cuirass + pauldrons + greaves, navy tabard, (cloak variant) hooded
  cloak, belt and leather harness. _Gameplay stat mapping: TBD._

### Personality
_TBD — see `docs/characters/` / `docs/heroes/` once authored. Do not invent._

### Animation Notes
_TBD — deliberate, weighty guardian movement is implied by the armour and
stance; formal reference to be captured during rigging/animation. Placeholder._

### Combat Notes
_TBD — visually a Guardian archetype (sword-and-shield, defensive). Confirm
against `docs/COMBAT_SYSTEM.md` / `tactical/data/classes.json` before binding to
mechanics. Placeholder._

### Voice & Dialogue Notes
_TBD — no canonical voice direction yet. Placeholder._

### Modeling Notes
- Derive the 3D model from `talos_cloak.png` (turnaround) as the primary
  topology reference; use `talos_no_cloak.png` for undersuit/armour detail.
- Model the cloak as a separable layer so both canonical states (cloak /
  no-cloak) are supported from one base mesh.
- Preserve the swatch palette for material authoring.

### UI Portrait Notes
- Derive portrait crops from `talos_no_cloak.png` (clean hero framing).
- Keep the sun sigil and face identity legible at small sizes.

### Revision History
| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-06 | Canonical reference sheets imported (cloak 1672×941, no-cloak 1024×1536), unaltered. Established as visual source of truth. |

---

## Future Character-Reference Pipeline
All character production assets must **derive from** the canonical reference
sheets above rather than creating new interpretations. This applies to Tripo /
photogrammetry-style 3D generation, Blender sculpts & retopo, Godot models &
rigs, promotional/marketing artwork, equipment previews & paper-doll layers,
portraits and UI character images, and animation reference. See
[`Pipeline.md`](Pipeline.md).

**Rule of thumb:** the reference sheet is the contract. Any deviation must first
be recorded here as a *new canonical revision* before any derivative asset is
produced.
