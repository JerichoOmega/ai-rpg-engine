# Goblins

> Bestiary family doc — [`index`](README.md). Documentation of existing data units
> in [`enemies.json`](../../../tactical/data/enemies.json). No data changed.

**Teaches:** coordinated enemy tactics — the first foes that fight as a *team*.

## Lore summary
Frontier goblin tribes (see [`goblin_tribes.md`](../../world/goblin_tribes.md)) —
Stonefang, Mossroot, Ashfire and others. Not mindless: they raid, scout, ambush,
and follow chiefs and beastmasters. Whole questlines already build on them
([`goblin_tribe_quests.md`](../../quests/goblin_tribe_quests.md)).

## Visual identity
Small, wiry, opportunistic; mismatched scavenged armour, tribe-coloured warpaint
(Stonefang grey, Mossroot green, Ashfire red), crude but effective weapons; shamans
in bone-and-feather fetishes.

## Combat philosophy
Goblins teach **coordination**: archers kite while spearmen hold, scouts flank,
shamans buff/heal/`hex`, and a `goblin_chief`/`goblin_beastmaster` ties it together
with `rally`, `war_cry`, and `beast_call`. Kill order and pressure on the commander
matter more than raw damage. This is the family that punishes fighting "one enemy at
a time."

## Strengths
Numbers, role synergy (front line + ranged + support + commander), summons/beasts,
and buffs that multiply an otherwise weak roster.

## Weaknesses
Individually fragile; **morale-dependent** — break the chief and the coordination
collapses; shamans and beastmasters are soft priority targets.

## AI profiles (reused)
`aggressive_melee` (warriors/raiders/chief), `skirmisher` (scouts/archers),
`defensive` (spearmen), `support` (shaman), `summoner` (beastmaster).

## Recommended encounter usage
Frontier set-pieces: `goblin_camp`, plus the authored tribe quests. The precedent
gold-standard encounter [`The Sundered Span`](../encounters/gold_standard_sundered_span.md)
is goblin-centric — use it as the readability benchmark.

## Roster (10)
| Unit | Role | Tier | Threat | AI | One lesson | Tags |
|---|---|---|---|---|---|---|
| `goblin_warrior` | frontline | basic | low | aggressive_melee | The baseline body — but it never comes alone | Tutorial, Frontier |
| `goblin_scout` | scout | basic | low | skirmisher | Scouts flank — cover your sides | Frontier, Forest |
| `goblin_archer` | ranged | basic | low | skirmisher | **Kiting** — shooters bleed you at range | Frontier, Forest |
| `goblin_spearman` | frontline | basic | low | defensive | A held line buys the archers time | Frontier |
| `mossroot_scout` | skirmisher | basic | low | skirmisher | Tribe flankers exploit terrain | Forest, Story |
| `ashfire_raider` | frontline | basic | moderate | aggressive_melee | Aggressive raiders force your tempo | Frontier, Roads |
| `stonefang_warrior` | frontline | veteran | moderate | aggressive_melee | Veteran bodies anchor a warband | Mountains, Story |
| `goblin_shaman` | support | basic | moderate | support | **Kill the support** — `hex`/heal/ward | Frontier, Story |
| `goblin_beastmaster` | commander | veteran | moderate | summoner | Remove the `beast_call` handler | Forest, Story |
| `goblin_chief` | commander | elite | high | aggressive_melee | **Break the commander, break the tribe** | Frontier, Story |

## Future upgrade path (documented)
Basic (warrior/archer/spearman/scout) → Veteran (stonefang/beastmaster) → Elite
(chief) → **Champion** `_TBD_` (a warlord uniting tribes) → **Boss** `_TBD_` (a
tribal-alliance set-piece).

## Future elite/boss variants (`_TBD_`)
A "Raider", dedicated "Defender", and "Commander" beyond the current chief are the
requested role-slots — largely covered by `ashfire_raider`, `goblin_spearman`, and
`goblin_chief`/`goblin_beastmaster`; a named warlord boss is a **reserved placeholder.**
