# Elyndor Bestiary — Enemy Design Library

> **Status:** Canonical enemy **design documentation** (2026-06). This is the
> long-term bestiary for Elyndor, documenting the **74 data-driven enemy units**
> that already exist in [`tactical/data/enemies.json`](../../../tactical/data/enemies.json).
> **Documentation only — no gameplay, combat, AI, balance, or data was changed to
> create these docs.** Reserved/future content uses `_TBD_`.

## Design philosophy
Quality over quantity. Every enemy has a **distinct tactical identity** and
teaches **one lesson** — positioning, target priority, teamwork, terrain, morale,
or battlefield awareness. Basic enemies demonstrate **one mechanic**; complexity
comes from **combinations**, not from any single overloaded unit.

> **Reactive Combat pillar:** enemies exist to **create and deny opportunities** — flanks,
> exposed casters, guard breaks, environmental setups — the openings the party's *Reactive
> Combat* loop turns into **Resolve** and reactions ([`../REACTIVE_COMBAT.md`](../REACTIVE_COMBAT.md)).
> Good enemy design gives the player openings worth recognizing and punishes sloppy positioning;
> bosses (e.g. the Corruption Avatar) build set-piece opportunity/denial into their mechanics. Precedent
encounters: [`The Sundered Span`](../encounters/gold_standard_sundered_span.md),
[`The Forge Stand`](../encounters/forge_stand_torren.md),
[`The Lost Wolf (Bram)`](../encounters/the_lost_wolf_bram.md).

## Family docs (one per family)
| Family | Units | Teaches | Doc |
|---|---|---|---|
| Wildlife | 13 | Positioning & environmental awareness | [`wildlife.md`](wildlife.md) |
| Undead | 9 | Status effects & target priority | [`undead.md`](undead.md) |
| Goblins | 10 | Coordinated enemy tactics | [`goblins.md`](goblins.md) |
| Bandits & Mercenaries | 6 | Human tactical encounters | [`bandits.md`](bandits.md) |
| Cultists | 3 | Magic-heavy encounters | [`cultists.md`](cultists.md) |
| Orcs | 6 | Raw aggression & morale/commanders | [`orcs.md`](orcs.md) |
| Beasts & Monsters | 10 | Aggressive melee pressure & ambush | [`beasts_and_monsters.md`](beasts_and_monsters.md) |
| Forest | 4 | Terrain control & zoning | [`forest.md`](forest.md) |
| Constructs | 4 | Durability & sustained problems | [`constructs.md`](constructs.md) |
| Corrupted (variant line) | 11 | Escalation of the familiar + the family **boss** | [`corrupted.md`](corrupted.md) |

**Total: 76 spawnable units** (74 base roster + the `corruption_avatar` boss and
its `corruption_anchor` wardstone — the region's finale set-piece).

## How to read a family doc
Each family doc has: **visual identity · lore summary · combat philosophy ·
strengths · weaknesses · AI profile(s) · recommended encounter usage · future
upgrade path (Basic→Veteran→Elite→Champion→Boss) · a roster table · future
elite/boss variants (`_TBD_`)**. The roster table lists each unit's **role, tier,
threat, AI profile, the one lesson it teaches, and encounter tags.**

## Combat-role glossary (canonical `role` values in data)
`frontline` · `bruiser` · `tank` · `defender` · `skirmisher` · `ranged` ·
`ambusher` · `swarm` · `scout` · `support` · `caster` · `summoner` · `commander` ·
`elite`. Every unit belongs to exactly one role — there is **no generic AI**.

## AI-profile glossary (reused from `tactical/data/ai_profiles.json`)
`aggressive` / `aggressive_melee` · `brute` · `berserker` · `defender` /
`defensive` · `skirmisher` · `ambusher` · `pack_hunter` · `caster` · `summoner` ·
`support` · `commander` · `cowardly` · `elite` / `boss`. New enemies **reuse**
these; do not author duplicate behaviours.

## Progression ladder (documented, not all implemented)
```
Basic → Veteran → Elite → Champion → Boss
```
`tier` values in data today are **basic · veteran · elite · boss**. The first
**Boss** tier unit now exists — the **Corruption Avatar** finale set-piece
([`the_corruption_avatar.md`](../encounters/the_corruption_avatar.md)). A
**Champion** tier between elite and boss remains a documented target (`_TBD_`).

## Encounter-tag legend
`Tutorial` · `Frontier` · `Forest` · `Roads` · `Ruins` · `Mountains` ·
`Cave/Dungeon` · `Swamp` · `Night` · `Story`. Tags are documented per unit in each
family's roster table to simplify future encounter generation. *(Tags live in the
docs for now; a `tags` field in `enemies.json` is a future additive option.)*

## Existing encounter definitions (data)
The following encounters in [`tactical/data/encounters.json`](../../../tactical/data/encounters.json)
already compose these families: `forest_wolf_pack`, `roadside_ambush`,
`ruins_undead`, `goblin_camp`, `cave_swarm`, `orc_warband`, `corrupted_incursion`.

## Document History
| Date | Change |
|---|---|
| 2026-06 | Created the bestiary design library: index + 10 family docs covering all 74 existing data-driven units, with roles, AI mapping, one-lesson-per-basic, encounter tags, and Basic→Boss progression targets. Documentation-only; no data/gameplay changed. |
| 2026-06 | Added the family's **boss tier**: the Corruption Avatar + Corruption Anchor (roster 74→76). Documented in [`corrupted.md`](corrupted.md) and [`the_corruption_avatar.md`](../encounters/the_corruption_avatar.md); backed by 2 additive `enemies.json` blueprints. |
