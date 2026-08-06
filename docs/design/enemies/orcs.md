# Orcs

> Bestiary family doc — [`index`](README.md). Documentation of existing data units
> in [`enemies.json`](../../../tactical/data/enemies.json). No data changed.

**Teaches:** raw aggression, durability, and commander-driven morale.

## Lore summary
Warbands of the Frontier's harsher edges — orcs organized around strength, honour in
battle, and chieftains who lead from the front. Heavier and more disciplined than
goblins, they push rather than skirmish.

## Visual identity
Large, muscular, tusked; heavy scavenged plate and cleavers; war-paint and trophies;
chieftains marked by scale and scars.

## Combat philosophy
Orcs teach **absorbing and answering pressure**: `brute` frontliners that walk
through chip damage, a `berserker` that hits harder as it drops, an `orc_guardian`
tank, and an `orc_chieftain`/`orc_champion` using `war_cry`/`rally` to amplify the
line. The lesson is crowd control and focus fire under sustained aggression.

## Strengths
High durability, heavy hits, escalating damage (berserker), morale buffs, and elite
bodies that anchor a warband.

## Weaknesses
Low mobility and few ranged options (only `orc_hunter`); commander-reliant morale;
vulnerable to kiting and terrain that blunts the charge.

## AI profiles (reused)
`brute` (warrior/berserker/champion/chieftain), `defensive` (guardian),
`skirmisher` (hunter).

## Recommended encounter usage
Frontier/Mountains: `orc_warband`. Use for "hold the line, control the crowd, kill
the commander" set-pieces.

## Roster (6)
| Unit | Role | Tier | Threat | AI | One lesson | Tags |
|---|---|---|---|---|---|---|
| `orc_warrior` | frontline | basic | moderate | brute | Walks through chip — needs focus | Frontier, Mountains |
| `orc_guardian` | tank | basic | moderate | defensive | **A wall** — reposition around it | Frontier, Mountains |
| `orc_hunter` | ranged | basic | moderate | skirmisher | The warband's only reach — deny it | Mountains, Forest |
| `orc_berserker` | frontline | veteran | high | brute | **Hits harder as it dies** — burst it | Mountains, Story |
| `orc_champion` | frontline | elite | high | brute | `war_cry` elite — crowd-control priority | Mountains, Story |
| `orc_chieftain` | commander | elite | high | brute | **Break the `rally`/`war_cry` commander** | Frontier, Story |

## Future upgrade path (documented)
Basic (warrior/guardian/hunter) → Veteran (berserker) → Elite (champion/chieftain) →
**Champion** `_TBD_` (a warlord) → **Boss** `_TBD_` (a warchief set-piece).

## Future elite/boss variants (`_TBD_`)
A named orc warchief boss and a shaman/support slot are **reserved placeholders**.
