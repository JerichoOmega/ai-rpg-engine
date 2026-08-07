# Tactical AI Framework (reusable behavior library + memory)

> Status: Implemented · Technical Canon: `tactical/ai.py`, `tactical/data/ai_profiles.json`
> Verified: harness `python -m tactical.verify` (AI Personalities checks) +
> `backend/tests/test_ai_personalities.py` (25) · report
> `docs/verification/ai_personalities.md`

> **Reactive Combat pillar:** companion AI must eventually **recognize opportunities** and
> surface them to the player-commander (the barks in [`../design/REACTIVE_COMBAT.md`](../design/REACTIVE_COMBAT.md) §6),
> who authorizes a reaction/Partner Technique for **Resolve**. Enemy AI likewise **creates and
> denies** opportunities (openings the party can exploit; punishing sloppy positioning).
> Companion intelligence identifies; it never auto-acts — the player always decides. Planned
> Additive on this one AI pipeline.

## Principle

Enemy behaviour is **data-driven and reusable**. A blueprint sets stats,
abilities, equipment and a **profile name**; the profile decides tactical
priorities. There is **no enemy-specific AI** — one code path (`ai.take_turn` /
`ai._score_tile`) serves every enemy, driven only by profile flags. Adding a new
archetype is a JSON entry that can be assigned to dozens of enemies. *Whenever
two blueprints share behaviour, extend/assign a profile — never add special-case
logic. The library grows by archetype, not by enemy.*

The AI reads the **same** functions the player's UI uses (`compute_hit_chance`,
`threat_map`, `reachable`, `line_of_sight`, `relative_arc`) — no hidden state,
no bonuses.

## Profile flags honoured today

`target_selection` (nearest | lowest_health | lowest_armor) · `preferred_range`
(melee | ranged) · `charges` · `kites` · `hold_position` · `prefers_flank` ·
`fearless` · `uses_cover` · `avoids` (hazards) · `will_retreat` /
`flees_when_low` (+ `flee_threshold`).

Descriptive flags reserved for the ability phase (not yet executed):
`coordinates`, `buffs_allies`, `summons`, `pack_tactics`, `high_value_target`,
`reckless`.

## Archetype library

| Profile | Feel | Key flags |
|---------|------|-----------|
| aggressive / brute / beast | charge in, ignore cover | charges, (fearless) |
| berserker | reckless charge, never retreats, braves fire | charges, fearless, avoids:[] |
| aggressive_melee | close, but use cover | uses_cover |
| defender / defensive | hold ground, prefer cover | hold_position, uses_cover |
| commander | focus-fire weak targets, steady allies | lowest_health, coordinates |
| skirmisher / hunter | ranged, keep distance, pick off wounded | kites, will_retreat, (prefers_flank) |
| ambusher / assassin | seek flanks, disengage when hurt | prefers_flank, flees_when_low |
| caster / necromancer / summoner | stay back, avoid melee, reposition | ranged, kites, will_retreat |
| support | hang back near allies, avoid melee | ranged, buffs_allies, kites |
| pack_hunter | surround and flank | pack_tactics, prefers_flank |
| cowardly | break and run when wounded | flees_when_low, flee_threshold .5 |
| elite / boss | disciplined, never break | fearless, uses_cover |

**Authored aliases (intentional):** `defensive`≈`defender`, `assassin`≈`ambusher`
today. Their *finer* distinctions from the Gameplay Canon — "defender uses
defensive abilities first," "ambusher waits for favorable attacks," "caster uses
crowd control," "commander buffs allies" — depend on the **ability system**
(next phase) and will differentiate the aliases then.

## Behavior memory (`Combatant.ai_memory`)

A short per-unit tactical context so enemies act intentionally, not randomly:

* `target_id` — **sticky targeting**: keep chasing the committed target while it
  lives (lowest-health seekers still switch to a target under 50% of the current
  target's HP).
* `turns_chasing` — increments while out of range, resets on engagement.
* `morale` — `low` when half+ the team is dead → raises flee threshold;
  `high`/`normal` otherwise.
* `commander_nearby` — a living `coordinates` ally within 4 tiles halves the
  flee threshold (troops stand firm while led).
* `currently_flanking` — recorded when attacking from a side/rear arc.

`fearless` profiles never flee regardless of memory.
