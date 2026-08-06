# Undead

> Bestiary family doc — [`index`](README.md). Documentation of existing data units
> in [`enemies.json`](../../../tactical/data/enemies.json). No data changed.

**Teaches:** status effects and target priority.

## Lore summary
The restless dead of Elyndor — bound skeletons in ruined garrisons, spirits tied to
grief, and the necromancers who raise them. Undead cluster where The Corruption and
old battlefields overlap; ruins are their home.

## Visual identity
Bleached bone in rusted armour, tattered banners, cold blue grave-light; spirits as
translucent, drifting figures; necromancers in dark robes wreathed in sickly energy.

## Combat philosophy
Undead teach **priority**: a `skeleton_shieldbearer` wall you must break, a
`skeleton_archer` you must reach, a `skeleton_captain`/`necromancer` you must kill
*first* or the fight never ends. They introduce **status effects** — `curse`,
`bone_shield`, and reanimation — so players learn to read buffs/debuffs and answer
the source, not the symptom.

## Strengths
Formations (shield walls), reinforcement (`raise_skeleton`/`raise_dead`), debuffs
(`curse`), and elite bodies that ignore morale — undead never flee.

## Weaknesses
No morale to break (a double edge — predictable), slow without a commander, and
hard-countered by killing the summoner/leader. Spirits are fragile if cornered.

## AI profiles (reused)
`aggressive_melee` (warriors/captains), `defensive` (shieldbearers/spearmen),
`skirmisher` (archers), `ambusher` (spirits/wraiths), `summoner` (necromancer).

## Recommended encounter usage
Ruins and Story dungeons: `ruins_undead`. Ideal for teaching "kill the caster" and
for tense night set-pieces.

## Roster (9)
| Unit | Role | Tier | Threat | AI | One lesson | Tags |
|---|---|---|---|---|---|---|
| `skeleton_warrior` | frontline | basic | low | aggressive_melee | The baseline body — reliable to read | Tutorial, Ruins |
| `skeleton_archer` | ranged | basic | low | skirmisher | Close the gap on shooters | Ruins, Night |
| `skeleton_spearman` | frontline | basic | low | defensive | Reach weapons punish the approach | Ruins |
| `skeleton_shieldbearer` | tank | basic | moderate | defensive | **Shield wall** — break the line or go around | Ruins |
| `skeleton_captain` | frontline | elite | high | aggressive_melee | Kill the `rally` source first | Ruins, Story |
| `ancient_skeleton` | frontline | elite | high | aggressive_melee | Elite bodies need focus, not chip | Ruins, Story |
| `restless_spirit` | skirmisher | basic | moderate | ambusher | **Ambush** — watch your flanks | Ruins, Night |
| `wraith` | skirmisher | elite | high | ambusher | A `curse`-caster that ambushes — priority | Ruins, Night, Story |
| `necromancer` | summoner | elite | high | summoner | **Kill the caster** or fight forever | Ruins, Story |

## Future upgrade path (documented)
Basic (warrior/archer/spearman) → Veteran `_TBD_` (armored/wight variants) → Elite
(captain/ancient/wraith/necromancer) → **Champion** `_TBD_` (a death-knight lieutenant)
→ **Boss** `_TBD_` (a lich / grave-lord set-piece).

## Future elite/boss variants (`_TBD_`)
Skeletal Guardian (elite shield anchor), Zombie (slow/tanky attrition), Grave Warden
(undead defender-commander), and a named lich boss are **reserved placeholders**.
