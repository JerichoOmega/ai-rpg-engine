# Asset & Canon Standards — Elyndor

Project-wide rules for reference assets and canon documentation. These follow
professional game-studio asset-management practice and are designed to scale to
hundreds of characters, multiple artists, multiple AI tools, and outsourced work.

---

## 1. File & naming standards
- **Naming:** `snake_case`, descriptive of subject + variant, e.g.
  `talos_cloak.png`, `talos_no_cloak.png`, `mossroot_goblin_chief.png`.
  Pattern: `<subject>_<variant>[_<state>].png`.
- **Format:** reference art is **lossless PNG** (or the artist's original layered
  source when available, stored alongside).
- **Resolution:** preserve **original resolution**. Never resize, crop, or
  compress a reference asset.
- **Colour:** never recolour. The reference is the colour contract.
- **Location:** all reference material lives under `assets/reference/<category>/`
  (see `assets/reference/README.md`). Keep reference separate from any
  production/runtime assets.

## 2. Immutability of canon
- Canonical reference assets are **immutable source assets**. Never modify,
  overwrite, or delete them.
- **Maintain source assets forever.** Superseded versions are archived, not
  deleted (see the revision system below).
- Every downstream asset — renders, 3D models, UI, marketing — **derives from
  canon**, never the other way around.

## 3. Revision system
Canon evolves through explicit, numbered revisions. Older versions remain
archived permanently; canonical history is never deleted.

```
Talos v1.0   (Canonical — original reference sheets)
   ↓
Talos v1.1   (Minor equipment updates)
   ↓
Talos v2.0   (New official redesign — supersedes v1.x)
```

Rules:
- **Minor revision (vX.y):** small, compatible changes (accessory, trim, palette
  tweak). Add a row to the character's Revision History; keep prior files.
- **Major revision (vX.0):** a redesign that changes silhouette/identity. Create
  new reference files (do not overwrite), archive the previous set under
  `assets/reference/<category>/_archive/<subject>/vX/`, and record the
  supersession in the Revision History with the reason.
- A superseded version's Status becomes `Deprecated` with a pointer to the
  version that replaces it. Downstream assets should migrate to the newest
  canonical version.

## 4. Derivation rule (the contract)
Unless a canonical revision explicitly changes it, all derivative work must
maintain the reference's **silhouette, proportions, costume details, and colour
palette**. If a production asset must deviate, capture that change as a new
canonical revision **first**, then produce the derivative.

Derivation applies to (non-exhaustive):
- Future renders derive from canon
- Future 3D models derive from canon
- Future UI derives from canon
- Future marketing derives from canon
- Future animation & rigging reference derives from canon

## 5. Do-not / do
| Do NOT | DO |
|---|---|
| Modify / overwrite / delete canon | Add new files; supersede via revision |
| Resize, crop, compress, recolour references | Preserve original, lossless, full-res |
| Invent lore in canon index files | Cross-reference existing lore; use `_TBD_` |
| Fragment canon into competing copies | Expand and link to the single source |

## 6. Future-proofing
The system is intentionally modular so the project can scale to:
hundreds of characters · multiple artists · multiple AI tools (Tripo, Blender,
Godot, image gen) · outsourced artwork · version tracking · marketing assets ·
alternative costumes · equipment variants · seasonal skins · NPC variants.

Scaling conventions:
- One flat file set per subject inside its category folder; use `_variant`
  suffixes for costumes/skins (e.g. `talos_winter.png`).
- One documentation row/section per subject; reserve the metadata fields in
  `_character_template.md` for every character.
- Archive superseded revisions under `_archive/`; never delete.
