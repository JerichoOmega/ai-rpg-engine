# Elyndor Canon & Reference Index

This folder is the **visual-canon and asset-reference index** for Elyndor. It is
the single entry point that ties together:

- the immutable **reference assets** under `assets/reference/`, and
- the authoritative **narrative lore** already maintained under `docs/lore/`,
  `docs/world/`, `docs/world/factions/`, `docs/characters/`, etc.

> These canon files do **not** duplicate or replace existing lore. Narrative
> truth continues to live in its established homes; the files here are
> lightweight **indexes + visual-canon + asset-pipeline records** that point to
> those sources and govern how art/models/UI/marketing derive from canon.

## Contents
| File | Purpose | Narrative source of truth |
|---|---|---|
| [`Characters.md`](Characters.md) | Character visual canon + reference sheets | `docs/characters/`, `docs/heroes/`, `docs/companions/`, `docs/npcs/` |
| [`_character_template.md`](_character_template.md) | Reusable per-character metadata template | — |
| [`Factions.md`](Factions.md) | Faction visual canon index | `docs/world/factions/` |
| [`Settlements.md`](Settlements.md) | Settlement visual canon index | `docs/world/`, `docs/lore/IMPERIAL_CAPITAL.md` |
| [`Equipment.md`](Equipment.md) | Equipment/weapon/armour visual canon | `tactical/data/`, gear docs |
| [`Creatures.md`](Creatures.md) | Creature/enemy visual canon index | `tactical/data/enemies.json`, bestiary docs |
| [`World.md`](World.md) | World/biome/geography visual canon | `docs/world/GEOGRAPHY_LANDMARKS.md`, `docs/lore/world/` |
| [`Timeline.md`](Timeline.md) | Canonical timeline index | `docs/lore/TIMELINE.md` |
| [`Magic.md`](Magic.md) | Magic system visual canon index | `docs/lore/DIVINE_CHORUS*.md` |
| [`Architecture.md`](Architecture.md) | Architecture/structures visual canon | `docs/lore/GREAT_LIBRARY.md`, `docs/lore/FIRST_TEMPLE.md` |
| [`Asset_Standards.md`](Asset_Standards.md) | Naming, formats, revision system, future-proofing | — |
| [`Pipeline.md`](Pipeline.md) | Concept → reference → model → game asset pipeline | — |

## Golden rules
1. **Canonical reference assets are immutable.** Never modify, resize, crop,
   recolour, compress, or overwrite them. New versions *supersede* old ones and
   the old ones are archived, never deleted.
2. **Every downstream asset derives from the canonical reference sheet.**
3. **Do not invent lore here.** If a field is unknown, leave a clearly-labelled
   `_TBD_` placeholder and link to where the truth will live.
4. **Expand, never fragment.** Cross-reference existing lore rather than
   re-authoring it.

See [`Asset_Standards.md`](Asset_Standards.md) for the full rules.
