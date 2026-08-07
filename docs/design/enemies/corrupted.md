# Corrupted (variant line)

> Bestiary family doc — [`index`](README.md). Documentation of existing data units
> in [`enemies.json`](../../../tactical/data/enemies.json). No data changed.

**Teaches:** escalation of the familiar — known foes made worse by The Corruption.

## Lore summary
The Corruption is Elyndor's central creeping threat (see
[`WORLD_BIBLE.md`](../../world/WORLD_BIBLE.md)); the Frontier suffers it first. It
does not create new creatures so much as **twist existing ones** — rats, wolves,
boars, goblins, orcs, bears, trolls, treants, and even ancient guardians. Each
`corrupted_*` unit **`extends` its base creature**, inheriting its identity and
adding menace. Corrupted units drive the `corrupted_incursion` encounter and the
mid/late-game threat curve.

## Visual identity
The base creature, wrong: blackened veins, weeping corruption, malformed growths,
sickly light in the eyes. Instantly readable as "that animal, but *turned*."

## Combat philosophy
This is a **cross-cutting variant family**, not a species. Its lesson: *the enemies
you learned to beat come back harder.* A `corrupted_wolf` still pack-flanks, a
`corrupted_boar` still charges — but tougher and more threatening. It rewards the
player's earlier learning while raising the stakes, and signals story escalation
without teaching a brand-new mechanic per unit.

## Strengths
Inherit their base creature's tactics plus higher threat/durability; thematically
signal danger; span every biome because they reuse every family.

## Weaknesses
Same **structural** weaknesses as their base forms (pack wolves still die to good
spacing; brutes still kite; casters/leaders still priority) — the counters you
already learned still apply.

## AI profiles (reused)
Inherited from base creatures: `pack_hunter`, `brute`, `aggressive_melee`,
`defender`, `skirmisher`. No new behaviours.

## Recommended encounter usage
`corrupted_incursion`, and as escalated re-skins of earlier encounters to show the
Corruption spreading. Ideal for the mid-slice "the woods you cleared aren't safe
anymore" beat.

## Roster (9)
| Unit | Base (`extends`) | Role | Tier | Threat | One lesson | Tags |
|---|---|---|---|---|---|---|
| `corrupted_rat` | `giant_rat` | swarm | basic | low | Familiar swarm, now a real threat | Ruins, Story |
| `corrupted_wolf` | `wolf` | skirmisher | basic | moderate | Pack tactics you know — nastier | Forest, Night, Story |
| `corrupted_boar` | `wild_boar` | bruiser | basic | moderate | The charge lesson, escalated | Forest, Story |
| `corrupted_goblin` | `goblin_warrior` | frontline | basic | moderate | Twisted tribes hit harder | Frontier, Story |
| `corrupted_bear` | `bear` | bruiser | basic | high | A big body, now genuinely scary | Forest, Cave/Dungeon, Story |
| `corrupted_orc` | `orc_warrior` | frontline | basic | high | Brute pressure, corrupted | Mountains, Story |
| `corrupted_troll` | `troll` | elite | elite | high | An elite wall, worsened | Story, Mountains |
| `corrupted_treant` | `treant` | elite | elite | high | `entangle` zoning, escalated | Forest, Story |
| `corrupted_ancient_guardian` | `stone_sentinel` | tank | elite | high | A vault-wall turned hostile | Ruins, Story |

## Future upgrade path (documented)
Corruption is itself the "veteran/elite" step for many base creatures. The
family's natural capstone — a **Corruption avatar / heart-of-the-blight
set-piece** — now exists (see below); a corruption-warped **Champion** apex
between elite and boss remains `_TBD_`.

## Boss tier — The Corruption Avatar (implemented)
The family's capstone boss is now defined in data and as a playable headless
set-piece. Two additive blueprints back it:

| Unit | Role | Tier | Threat | AI | One lesson | Tags |
|---|---|---|---|---|---|---|
| `corruption_avatar` | boss | boss | extreme | `boss` | Don't tunnel the boss — break its wards first | Story, Frontier, Ruins |
| `corruption_anchor` | objective | elite | moderate | `defender` | The thing sustaining the boss must die first | Story, Frontier, Ruins |

**Mechanic (WARDED):** while any `corruption_anchor` (wardstone) stands, damage
to the Avatar is nullified; destroy the anchors to **expose and enrage** it.
Full design, numbers, and evidence:
[`the_corruption_avatar.md`](../encounters/the_corruption_avatar.md).

**Identity is canonically `_TBD_`:** it is a *manifestation* of The Corruption —
an ancient force, not a named individual (trait `_TBD_identity`). The player
cleanses the region, but the true source is left unresolved for future acts.

## Future elite/boss variants (`_TBD_`)
Additional corrupted forms of any base creature, and a corruption-warped
**Champion** apex, remain **reserved placeholders** — the `extends` pattern makes
adding them a data-only value swap when needed.
