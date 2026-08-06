# Cultists

> Bestiary family doc — [`index`](README.md). Documentation of existing data units
> in [`enemies.json`](../../../tactical/data/enemies.json). No data changed.

**Teaches:** magic-heavy encounters — debuffs, summons, and priority casters.

## Lore summary
Devotees of forbidden or corrupted faith (see [`cults.md`](../../world/cults.md))
who trade safety for power. They appear where The Corruption has taken root and
people have turned to dark bargains.

## Visual identity
Dark robes, ritual masks and brands, candlelit sigils; adepts marked by the power
they channel; leaders wreathed in visible dark energy.

## Combat philosophy
Cultists teach **magic priority**: fragile bodies backed by `curse` (debuff),
`dark_bolt` (ranged nuke), and `raise_dead` (summon) mean the player must **reach
and kill the casters** while managing debuffs and adds. The opposite lesson to
brute families — patience and target selection over trading blows.

## Strengths
Debuffs, ranged magic, summoning (action economy), and an elite `cult_leader` that
snowballs if ignored.

## Weaknesses
Physically frail, low mobility, and hard-countered by pressure on the casters;
without their magic they fold.

## AI profiles (reused)
`aggressive_melee` (fanatic cultists), `caster` (adept), `summoner` (leader).

## Recommended encounter usage
Story/Ruins with corruption themes; pairs naturally with `corrupted_incursion` and
undead adds from `raise_dead`.

## Roster (3)
| Unit | Role | Tier | Threat | AI | One lesson | Tags |
|---|---|---|---|---|---|---|
| `cultist` | frontline | basic | low | aggressive_melee | Fodder that screens the casters | Ruins, Story |
| `cult_adept` | caster | basic | low | caster | **Casters first** — `curse` + `dark_bolt` | Ruins, Story, Night |
| `cult_leader` | summoner | elite | high | summoner | `raise_dead` snowballs — end it fast | Story, Ruins |

## Future upgrade path (documented)
Basic (cultist/adept) → Veteran `_TBD_` (zealot/hex-adept) → Elite (leader) →
**Champion** `_TBD_` (a dark priest) → **Boss** `_TBD_` (a cult high-priest ritual
set-piece).

## Future elite/boss variants (`_TBD_`)
Fanatic (aggressive fodder), Ritualist (channel/summon support), Hex Adept
(debuff specialist), Zealot (berserk melee), Dark Priest (elite caster-commander)
are the requested role-slots — **reserved placeholders** beyond the current three.
