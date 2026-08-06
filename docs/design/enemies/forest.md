# Forest

> Bestiary family doc — [`index`](README.md). Documentation of existing data units
> in [`enemies.json`](../../../tactical/data/enemies.json). No data changed.

**Teaches:** terrain control and zoning — enemies that shape the battlefield.

## Lore summary
The awakened and animate life of Elyndor's deep woods — treants, thorn-things,
living vines, and forest spirits. Often **neutral unless provoked**; they defend
their groves rather than hunt, tied to the Old Ways ([`religions.md`](../../world/religions.md)).

## Visual identity
Bark-skinned giants, tangled thorn masses, creeping vines, and luminous drifting
spirits — nature made watchful and hostile.

## Combat philosophy
This family teaches **zoning and control**: `entangle` roots and denies tiles,
`living_vines` block lanes, `forest_spirit` sustains allies with `healing_totem`.
Players learn to fight *around* control effects and to kill the enabler
(spirit/treant) rather than hacking the terrain.

## Strengths
Root/immobilize (`entangle`), area denial, sustain (`healing_totem`/`spirit_ward`),
and durable elite treants.

## Weaknesses
Slow and rooted themselves; few ranged threats; fire/burst answers control quickly;
non-aggressive until provoked (can be avoided).

## AI profiles (reused)
`defender` (treant/thornling/living_vines), `support` (forest_spirit).

## Recommended encounter usage
Forest/Story set-pieces emphasizing terrain; excellent contrast fights after
aggression-heavy families to force a tempo change.

## Roster (4)
| Unit | Role | Tier | Threat | AI | One lesson | Tags |
|---|---|---|---|---|---|---|
| `treant` | elite | elite | high | defender | **`entangle` zoning** — don't stand in roots | Forest, Story |
| `thornling` | elite | basic | low | defender | Small zoner — chip that denies space | Forest |
| `living_vines` | defender | basic | low | defender | **Lane control** — block, reroute your line | Forest, Ruins |
| `forest_spirit` | support | basic | moderate | support | **Kill the sustain** (`healing_totem`) | Forest, Story, Night |

## Future upgrade path (documented)
Basic (thornling/vines/spirit) → Veteran `_TBD_` → Elite (treant) → **Champion**
`_TBD_` (an elder treant) → **Boss** `_TBD_` (a grove-guardian set-piece).

## Future elite/boss variants (`_TBD_`)
Forest Stag (neutral herd animal, provoke-only) and an elder grove-guardian boss are
**reserved placeholders**. Corrupted forms: see [`corrupted.md`](corrupted.md).
