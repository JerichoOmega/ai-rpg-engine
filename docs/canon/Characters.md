# Canonical Character Reference — Elyndor

This document tracks the **canonical visual references** for Elyndor characters.
The linked reference sheets are the single source of truth for a character's
appearance. All future art (models, portraits, concept art, animation,
equipment, marketing renders, UI images) must derive from these sheets and must
not reinterpret them unless a future canonical design revision explicitly
supersedes them.

Reference assets live under `assets/reference/characters/` and are **reference
material only** — not gameplay sprites or production textures. They are stored
at original resolution, uncompressed and unaltered.

---

## Talos

**Status:** Canonical — primary visual reference for all future Talos art and
modeling.

**Role:** Player character (Guardian archetype — heavy plate, sword-and-shield;
sun sigil on shield/tabard).

### Reference Assets

| Version | File | Resolution | Notes |
|---|---|---|---|
| Talos (Cloak) | [`assets/reference/characters/talos_cloak.png`](../../assets/reference/characters/talos_cloak.png) | 1672 × 941 | Full turnaround sheet — front/side/back rotations, head studies, weapon + shield callouts, material/colour swatches. Navy hooded cloak over the shoulders/back. |
| Talos (No Cloak) | [`assets/reference/characters/talos_no_cloak.png`](../../assets/reference/characters/talos_no_cloak.png) | 1024 × 1536 | Full-body hero portrait, no cloak — armour, navy tabard, longsword, sun-sigil shield. |

**Purpose:** Primary visual reference for all future character art and modeling.

### Design intent to preserve
Unless changed through a future canonical design revision, all derivative work
must maintain:
- **Silhouette & proportions** — broad, heavily-armoured frame; sword-and-board stance.
- **Costume details** — layered dark plate with brass/gold trim and brown leather
  strapping; navy tabard and (cloak version) navy hooded cloak; segmented pauldrons,
  belt, and greaves.
- **Colour palette** — gunmetal/dark steel + brass-gold accents + navy cloth +
  brown leather (see the swatch strip on the cloak sheet).
- **Iconography** — the radiant **sun sigil** (shield face and tabard trim).
- **Facial features** — pointed (elven) ears, short dark hair, trimmed beard,
  facial scar.

---

## Future Character-Reference Pipeline

All character production assets must **derive from** the canonical reference
sheets above rather than creating new interpretations. This applies to:

- Tripo / photogrammetry-style 3D generation
- Blender sculpts and retopo
- Godot character models and rigs
- Promotional / marketing artwork
- Equipment previews and paper-doll layers
- Portraits and UI character images
- Animation reference

Rule of thumb: **the reference sheet is the contract.** If a production asset
needs to deviate (new armour set, alternate costume, aged appearance, etc.),
that change must first be captured as a *new canonical revision* recorded in
this document before any derivative asset is produced.

### Recommended organization for future character references
```
assets/
  reference/
    characters/
      talos_cloak.png
      talos_no_cloak.png
      <character>_<variant>.png        # one folder-flat set per character
    equipment/                         # (future) canonical gear reference
    environments/                      # (future) canonical location reference
```
Suggested conventions for new entries:
- `snake_case`, `<character>_<variant>.png`, original resolution, lossless.
- Add a row to this document under a per-character heading with resolution,
  a one-line description, and the design-intent notes to preserve.
- Keep reference material separate from production/runtime assets; never
  overwrite an existing canonical file — supersede it with a dated revision note.

---

## Revision History
| Date | Change |
|---|---|
| 2026-06 | Established canon doc; imported Talos reference sheets (cloak 1672×941, no-cloak 1024×1536) unaltered into `assets/reference/characters/`. |
