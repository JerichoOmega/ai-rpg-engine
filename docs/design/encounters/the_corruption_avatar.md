# The Corruption Avatar — Regional Finale (Design)

> **Status:** Encounter **design + implemented headless set-piece** (2026-06).
> Additive. Implemented in [`tactical/showcase_corruption_avatar.py`](../../../tactical/showcase_corruption_avatar.py),
> proven by [`backend/tests/test_corruption_avatar.py`](../../../backend/tests/test_corruption_avatar.py)
> and reported by [`scripts/corruption_avatar_report.py`](../../../scripts/corruption_avatar_report.py).
> Two additive data blueprints were added to
> [`enemies.json`](../../../tactical/data/enemies.json) (`corruption_avatar`,
> `corruption_anchor`); **no existing data, combat, or AI was changed.**

## Role in the region
The **climactic finale the entire Frontier chapter builds toward**. It comes
**after** [The Lost Howl](the_lost_wolf_bram.md) — Ronan's *emotional* climax
(Bram's rescue and the Hidden Pack's acceptance is the final *character* beat).
Once that resolves, **Corwin's investigation** exposes the true source of the
corruption, and the whole party converges on the heart of the blight for the
region's *tactical* climax. The companion quests feed **into** the finale rather
than competing with it.

## Identity — canonically reserved (`_TBD_`)
The Avatar's **true name, origin, and deeper lore are intentionally unresolved.**
Throughout the region it is treated as **an ancient force / a manifestation of
The Corruption**, not a named individual. Subtle foreshadowing (Corwin's
"something old wearing the corruption like a mask") points toward a larger
mystery **without answering it**. The player defeats *this manifestation* and
**cleanses the region**, but the underlying source may extend beyond this single
encounter. This preserves flexibility for future acts — no permanent lore is
invented that could constrain later world-building.

## The tactical lesson (new to the slice)
**Don't tunnel the boss — dismantle what sustains it first.** This is a distinct
lesson from the earlier set-pieces:

| Set-piece | Lesson |
|---|---|
| The Sundered Span | Terrain, elevation, readability |
| The Forge Stand | Use the environment (build vs brawl) |
| The Lost Howl | Save, don't slay |
| **The Corruption Avatar** | **Break the boss's supports before you can hurt it** |

## Mechanic — WARDED + phases
* **Corruption Anchors (wardstones) ×3** ring the Avatar. While **any** anchor
  stands, damage to the Avatar is **nullified** — its blight knits shut as fast
  as you cut it. Anchors are immobile ranged pressure (`defender` AI).
* **Phase 1 — Break the wards.** The Avatar is effectively invulnerable; the
  party must destroy the three anchors while surviving the Avatar's melee and
  the anchors' Blight Pulse.
* **Phase 2 — Exposed & enraged.** The instant the last anchor falls, the wards
  shatter: the Avatar becomes vulnerable and **enrages** (+1 AP, +4 damage) for
  the true fight.

## Cast & numbers (data-driven, reference party)
Validated with the canonical engine and the reference tactician party
([`showcase.build_party`](../../../tactical/showcase.py)). Numbers are scaled to
that party; a full-companion loadout is the in-fiction framing.

| Unit | HP | Armor | Move | AP | Attack | Range | AI |
|---|---|---|---|---|---|---|---|
| `corruption_avatar` | 120 | 3 | 3 | 2 (→3 enraged) | 8–12 (→12–16) corruption | 1 | `boss` |
| `corruption_anchor` ×3 | 22 | 2 | 0 | 1 | 4–7 corruption | 4 | `defender` |

## Interactive hooks (Frontier flow)
Wired into [`tactical/frontier.py`](../../../tactical/frontier.py) as the 9th
beat. Player choices earlier in the region feed the finale:
- **Corwin's careful investigation** (`knows_source`) **telegraphs** the wardstone
  mechanic in the finale's prompt.
- **`preparedness`** (earned from good recruitment/investigation choices) grants
  extra sustain; poor choices harden the wardstones. The **golden read (break the
  anchors) stays winnable at every preparedness level** — no unwinnable states.
- The finale choice itself branches: **break the wards** (golden) → *cleansed*;
  **strike the heart** (naive) → *held / overwhelmed*. This is a clearly
  telegraphed climactic decision, the appropriate place for a real branch.

## Design evidence (agent-tested, not user-confirmed)
From [`scripts/corruption_avatar_report.py`](../../../scripts/corruption_avatar_report.py), 40 seeds:
- **Break the wards (right read): ~95% cleansed** (97.5% well-prepared, 80% rushed).
- **Tunnel the Avatar (naive read): 0% cleansed** (100% fail).
- **Strategic gap: +95 percentage points** — the lesson lands decisively.

## Outcomes
- `cleansed` — the manifestation is destroyed; the Frontier is freed (win).
- `held` — time runs out with the Avatar still warded (the naive read).
- `overwhelmed` — the party falls.

## What's `_TBD_`
The Avatar's name/origin/deeper lore; a bespoke hand-built battlefield and
multi-avatar/second-phase mechanics for a full presentation-layer build; the
narrative thread that carries the unresolved source into future acts.

## Document History
| Date | Change |
|---|---|
| 2026-06 | Designed + implemented the regional finale: the Corruption Avatar (identity `_TBD_`) with the WARDED wardstone mechanic and a two-phase exposed/enrage structure. Added 2 additive data blueprints, a headless set-piece, tests, and a design report; wired it as the Frontier's 9th beat with preparedness/telegraph hooks. Agent-tested; not user-confirmed. |
