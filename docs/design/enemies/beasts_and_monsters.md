# Beasts & Monsters

> Bestiary family doc — [`index`](README.md). Documentation of existing data units
> in [`enemies.json`](../../../tactical/data/enemies.json). No data changed.

**Teaches:** aggressive melee pressure and ambush — big bodies and lurking threats.

## Lore summary
The larger predators and monstrosities of Elyndor's dangerous places: trolls of the
forests and mountains, swamp horrors, and the crawling things of deep caves. This
family covers the **trolls**, **swamp**, and **cave** data groups.

## Visual identity
Trolls: hulking, regenerating, grey-green or stone-hued. Swamp: slick, bloated,
leech- and spider-like. Cave: pale, chitinous, crystal-encrusted lurkers.

## Combat philosophy
This family teaches **respecting the big body and the unseen threat**. Trolls are
elite `brute` walls that demand sustained focus (and, later, answers to regeneration
`_TBD_`). Swamp/cave units teach **ambush and terrain** — `cave_lurker` and
`bog_spider` strike from concealment; `swamp_leech`/`rot_hound` swarm and harry.

## Strengths
Trolls: huge HP, heavy hits, elite threat. Swamp/cave: ambush, poison/web, swarm
pressure, terrain synergy.

## Weaknesses
Trolls: slow, low numbers, no ranged — kiteable and crowd-controllable. Swamp/cave:
fragile once revealed; rely on surprise and terrain.

## AI profiles (reused)
`brute` (trolls, mire_beast), `ambusher` (cave_lurker), `skirmisher`
(bog_spider/crystal_beetle), `pack_hunter` (rot_hound), `aggressive` (swamp_leech),
`defender` (rock_crawler).

## Recommended encounter usage
Set-piece bruisers and ambushes in Forest/Mountains/Swamp/Cave. A single troll makes
a strong mini-boss-feel encounter without being a scripted boss.

## Roster (10)
| Unit | Role | Tier | Threat | AI | One lesson | Tags |
|---|---|---|---|---|---|---|
| `troll` | elite | elite | high | brute | **A big body needs a plan** (CC + focus) | Forest, Mountains, Story |
| `forest_troll` | elite | elite | high | brute | Terrain-flavored elite bruiser | Forest, Story |
| `mountain_troll` | elite | elite | high | brute | Highland elite bruiser | Mountains, Story |
| `mire_beast` | bruiser | basic | moderate | brute | Swamp pressure — don't get bogged down | Swamp |
| `bog_spider` | ambusher | basic | moderate | skirmisher | **Ambush + web** — terrain is lethal | Swamp, Cave/Dungeon |
| `swamp_leech` | swarm | basic | trivial | aggressive | Swarm chip in bad footing | Swamp |
| `rot_hound` | skirmisher | basic | low | pack_hunter | Pack flanking in the mire | Swamp, Night |
| `cave_lurker` | ambusher | basic | moderate | ambusher | **Ambush** from the dark — scout ahead | Cave/Dungeon |
| `rock_crawler` | frontline | basic | low | defender | A slow wall in tight tunnels | Cave/Dungeon |
| `crystal_beetle` | skirmisher | basic | low | skirmisher | Fast harasser in cramped space | Cave/Dungeon, Mountains |

## Future upgrade path (documented)
Basic (swamp/cave units) → Veteran `_TBD_` → Elite (trolls) → **Champion** `_TBD_`
(a regenerating great-troll) → **Boss** `_TBD_` (an apex monstrosity set-piece).

## Future elite/boss variants (`_TBD_`)
Dire Bear, Mountain Lion, Giant Warg, and Marsh Crocodile (requested "Beasts") are
**reserved placeholders** — the Dire/Warg roles are partially served by
`cave_bear`/`rot_hound` today; add dedicated units when needed.
