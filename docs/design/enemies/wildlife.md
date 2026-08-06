# Wildlife

> Bestiary family doc — [`index`](README.md). Documentation of existing data units
> in [`enemies.json`](../../../tactical/data/enemies.json). No data changed.

**Teaches:** positioning and environmental awareness — the game's "first teachers."

## Lore summary
The ordinary and not-so-ordinary creatures of Elyndor's wilds: vermin, wolf packs,
boars, bears, and spiders. They are **not evil** — they are hungry, territorial, or
defending young. Most early Frontier travel encounters are wildlife.

## Visual identity
Naturalistic real-world animals scaled to threat: mangy rats, lean grey wolves,
tusked boars, hulking brown/cave bears, chitinous spiders. Earthy, believable,
never cartoonish.

## Combat philosophy
Wildlife teaches the fundamentals before humanoids arrive: **wolves punish poor
spacing** (pack flanking), **boars punish standing in a lane** (charge), **spiders
punish ignoring terrain** (web/zoning), **rats punish tunnel vision** (swarm chip
damage). Individually weak; dangerous through numbers, positioning, or a single
big body.

## Strengths
Speed and flanking (wolves), a heavy single hit (boars/bears), zoning and poison
(spiders), action economy (rat/spiderling swarms).

## Weaknesses
Low individual durability (except bears), no ranged answer, no morale/command — they
do not adapt; the player who fixes their positioning wins.

## AI profiles (reused)
`pack_hunter` (wolves/rot-adjacent), `brute` (boars/bears), `skirmisher`
(spiders/rats).

## Recommended encounter usage
Tutorial and early Frontier: `forest_wolf_pack`, `cave_swarm`. Use as the opening
teacher and as filler pressure that reads instantly.

## Roster (13)
| Unit | Role | Tier | Threat | AI | One lesson | Tags |
|---|---|---|---|---|---|---|
| `giant_rat` | swarm | basic | trivial | skirmisher | Swarms chip you if ignored | Tutorial, Cave/Dungeon |
| `diseased_rat` | swarm | basic | low | skirmisher | Kill swarms before they stack | Cave/Dungeon, Ruins |
| `wolf` | skirmisher | basic | low | pack_hunter | **Pack flanking** — don't get surrounded | Tutorial, Forest, Night |
| `dire_wolf` | skirmisher | veteran | moderate | pack_hunter | Faster flankers punish slow spacing | Forest, Mountains, Night |
| `alpha_wolf` | skirmisher | elite | moderate | pack_hunter | Kill the `howl` buffer first | Forest, Night, Story |
| `wild_boar` | bruiser | basic | low | brute | **Charge** — don't stand in its lane | Tutorial, Forest |
| `armored_boar` | bruiser | veteran | moderate | brute | Armor rewards focus fire | Forest, Mountains |
| `great_boar` | bruiser | veteran | moderate | brute | A big body needs a plan, not a trade | Forest |
| `bear` | bruiser | basic | moderate | brute | One heavy body demands crowd control | Forest, Cave/Dungeon |
| `cave_bear` | bruiser | veteran | high | brute | Bait the charge, then commit | Cave/Dungeon, Mountains |
| `giant_spider` | ambusher | basic | moderate | skirmisher | **Web/zoning** — terrain is a weapon | Forest, Cave/Dungeon |
| `brood_spider` | ambusher | elite | high | summoner | Kill the spawner, not the spawns | Cave/Dungeon, Swamp |
| `spiderling` | swarm | basic | trivial | skirmisher | Spawns exist to waste your AP | Cave/Dungeon |

## Future upgrade path (documented)
Basic (wolf/boar/bear) → Veteran (dire/armored/cave) → Elite (alpha/brood) →
**Champion** `_TBD_` (e.g. a scarred pack alpha with a lieutenant) → **Boss**
`_TBD_` (e.g. an apex predator set-piece). Corrupted variants: see
[`corrupted.md`](corrupted.md).

## Future elite/boss variants (`_TBD_`)
Forest Stag (neutral unless provoked), Mountain Lion (ambush), Giant Warg (pack
bruiser), and a named apex-predator boss are **reserved placeholders** — not yet in
data.
