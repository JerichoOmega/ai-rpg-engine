# Bandits & Mercenaries

> Bestiary family doc — [`index`](README.md). Documentation of existing data units
> in [`enemies.json`](../../../tactical/data/enemies.json). No data changed.

**Teaches:** human tactical encounters — foes that fight the way the player does.

## Lore summary
Desperate or greedy people on the Frontier roads: highway bandits preying on
travellers, and organized mercenary companies for hire. The morally grey humanoid
family — some are villains, many are just hungry.

## Visual identity
Practical leathers and mismatched steel, hooded cloaks, road-worn gear; mercenaries
more uniform and disciplined, with matching tabards and better arms.

## Combat philosophy
Bandits teach **symmetry** — they use cover, ranged fire, flanking, and leaders with
`rally`, so the player faces their own tools turned against them. Mercenaries add
discipline (`shield_wall`) and a hard-hitting `mercenary_captain`. Morale matters:
break the leader and lesser bandits waver.

## Strengths
Balanced composition (melee + ranged + leader), cover use, buffs (`rally`,
`shield_wall`), veteran/elite anchors.

## Weaknesses
**Morale-dependent** (target the leader), no summons or magic, and archers are soft
in melee.

## AI profiles (reused)
`aggressive_melee` (bandit/leader/mercenary/captain), `skirmisher`
(bandit_archer/highwayman).

## Recommended encounter usage
Roads/Frontier: `roadside_ambush`. Great for "use cover, kill the leader" lessons
and mixed melee/ranged reads.

## Roster (6)
| Unit | Role | Tier | Threat | AI | One lesson | Tags |
|---|---|---|---|---|---|---|
| `bandit` | frontline | basic | low | aggressive_melee | The human baseline — fights like you | Tutorial, Roads |
| `bandit_archer` | ranged | basic | low | skirmisher | Ranged threat from cover | Roads, Forest |
| `highwayman` | frontline | basic | moderate | skirmisher | **Flanker** — mobile, hits the soft targets | Roads, Night |
| `bandit_leader` | frontline | veteran | moderate | aggressive_melee | **Kill the `rally` leader** to break morale | Roads, Story |
| `mercenary` | frontline | basic | low | aggressive_melee | Disciplined line, not a mob | Roads, Frontier |
| `mercenary_captain` | commander | elite | high | aggressive_melee | `shield_wall` + `rally` — priority commander | Roads, Story |

## Future upgrade path (documented)
Basic (bandit/archer/mercenary) → Veteran (leader/highwayman) → Elite (captain) →
**Champion** `_TBD_` (a crime-lord lieutenant) → **Boss** `_TBD_` (a mercenary-company
commander set-piece).

## Future elite/boss variants (`_TBD_`)
Cutthroat (assassin/flanker), Crossbowman (heavy ranged), Veteran Mercenary, and a
named Captain boss are **reserved placeholders** — highwayman/mercenary_captain
partially cover these role-slots.
