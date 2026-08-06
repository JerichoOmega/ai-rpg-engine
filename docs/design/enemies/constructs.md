# Constructs

> Bestiary family doc — [`index`](README.md). Documentation of existing data units
> in [`enemies.json`](../../../tactical/data/enemies.json). No data changed.

**Teaches:** durability and sustained problem-solving — patient fights.

## Lore summary
Ancient guardians of First Age ruins and vaults — stone sentinels and crystalline
watchers still executing orders long after their makers vanished. They guard, they
do not hunt.

## Visual identity
Carved stone and glowing crystal, geometric and inhuman; runic seams that pulse when
active; slow, deliberate, monumental.

## Combat philosophy
Constructs teach **attrition and priority under low pressure**: high durability,
few numbers, and elite casters/summoners (`arcane_pulse`, `bone_shield`, spawns)
that reward patient, correct target order over frantic damage. The anti-swarm
lesson — a couple of tough bodies instead of a mob.

## Strengths
High armor/HP, area magic (`arcane_pulse`), self-protection (`bone_shield`), and
summons (`arcane_construct`) — they grind you down if you dawdle.

## Weaknesses
Slow, predictable, no morale, and often stationary guardians that can be avoided or
kited; vulnerable to sustained focus fire.

## AI profiles (reused)
`defender` (stone_sentinel), `caster` (crystal_guardian), `skirmisher`
(ancient_watcher), `summoner` (arcane_construct).

## Recommended encounter usage
Ruins/Dungeon vaults and Story set-pieces; a strong "puzzle-fight" contrast to
morale-driven humanoid encounters.

## Roster (4)
| Unit | Role | Tier | Threat | AI | One lesson | Tags |
|---|---|---|---|---|---|---|
| `stone_sentinel` | tank | veteran | moderate | defender | **A durable wall** — patience beats panic | Ruins, Cave/Dungeon |
| `crystal_guardian` | caster | veteran | moderate | caster | A durable caster — reach or endure it | Ruins, Story |
| `ancient_watcher` | ranged | veteran | moderate | skirmisher | Stationary ranged — break line of sight | Ruins |
| `arcane_construct` | summoner | elite | high | summoner | **Kill the summoner** (`arcane_pulse`) | Ruins, Story |

## Future upgrade path (documented)
Veteran (sentinel/guardian/watcher) → Elite (arcane_construct) → **Champion** `_TBD_`
(a vault-keeper) → **Boss** `_TBD_` (a First Age colossus set-piece).

## Future elite/boss variants (`_TBD_`)
A colossal vault-guardian boss and a "Skeletal/Ancient Guardian" undead-construct
crossover are **reserved placeholders** (`corrupted_ancient_guardian` is the
corrupted line — see [`corrupted.md`](corrupted.md)).
