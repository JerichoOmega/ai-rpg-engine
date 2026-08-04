# Reference Assets (CANON)

Immutable **reference material** — the single source of truth for Elyndor's
visual identity. Not gameplay sprites, not production/runtime textures. Every
production asset (3D models, UI, marketing, animation) **derives from** the
files here (see [`docs/canon/Pipeline.md`](../../docs/canon/Pipeline.md)).

## Rules (see `docs/canon/Asset_Standards.md`)
- Lossless PNG, **original resolution**, `snake_case` names.
- **Never** modify, resize, crop, recolour, compress, overwrite, or delete a
  reference asset. New versions supersede old ones; old ones are archived under
  `<category>/_archive/`, never deleted.

## Categories
| Folder | Purpose | Canon doc |
|---|---|---|
| `characters/` | Playable heroes, companions, NPCs | `docs/canon/Characters.md` |
| `equipment/` | Weapons, armour, shields, gear, paper-doll layers | `docs/canon/Equipment.md` |
| `creatures/` | Enemies, beasts, monsters, bosses | `docs/canon/Creatures.md` |
| `factions/` | Heraldry, sigils, uniforms | `docs/canon/Factions.md` |
| `settlements/` | Towns, capitals, outposts | `docs/canon/Settlements.md` |
| `architecture/` | Buildings, structures, ruins | `docs/canon/Architecture.md` |
| `props/` | Objects, items in world, VFX/sigils | `docs/canon/Magic.md` (VFX) |
| `environments/` | Biomes, regions, landscapes | `docs/canon/World.md` |
| `ui/` | UI-facing derived reference (portrait crops, icons) | `docs/canon/Characters.md` |
| `marketing/` | Promotional/marketing render references | `docs/canon/Pipeline.md` |

Each category folder has its own `README.md`. Add new subjects as
`<subject>_<variant>.png` and record them in the matching canon doc.
