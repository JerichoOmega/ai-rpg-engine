# The Forge Stand — Torren Field-Forge Showcase Encounter

> **Status:** Canonical design + playable showcase (2026-06). Companion piece to
> [`The Sundered Span`](gold_standard_sundered_span.md). Where the Span proves the
> general combat pillars, **The Forge Stand exists to prove one thing: Torren
> Ironhall's identity as the party's battlefield *shaper* and craftsman-support
> is real in play, not just on paper.**
>
> Runtime: `tactical/showcase_forge.py` · Proof: `scripts/forge_showcase_report.py`
> · Tests: `backend/tests/test_forge_showcase.py` · Character:
> [`docs/canon/Characters.md#torren`](../../canon/Characters.md#torren).
> Design-only doc; no gameplay data is described here that isn't in the runtime.

## The question the encounter asks
*Can a hero whose kit is **building, not hitting** actually carry a fight?*
Torren is deliberately built as a **sturdy but weak-hitting** front-liner (high
HP + armour, low attack damage). He cannot out-duel anything. If he matters, it
must be because he **reshapes the battlefield** — and the encounter is designed
so that this is the only thing that works.

## Setup
- **Map (12×7):** mostly open ground; two boulders at (5,1) and (5,5) frame a
  natural gap near the party's line — a partial choke Torren reinforces.
- **Party (3):** Torren (`smith`) fronting a glass-cannon backline — a ranger and
  a mage. Each carries one healing potion.
- **Raiders (4):** three goblin brutes that **charge**, plus one archer that
  softens the line. Left unchecked they reach the fragile heroes in ~2 turns and
  overwhelm them.

## Torren's Field-Forge kit (the `smith` class)
Six data-driven abilities in `tactical/data/ability_library.json`, all routed
through the canonical ability pipeline (`ability_preview` → `use_skill`):

| Ability | Type | What it shapes | The decision it creates |
|---|---|---|---|
| **Spike Barrier** | terrain (rubble) | Half cover that does **not** block LOS, and difficult ground | Lay it in front of a fragile hero for cover, or in a charger's path to slow it — rarely AP for both |
| **Reinforced Wall** | terrain (wall segment) | Full cover, blocks LOS, impassable | Hard-cut a lane without walling off your own shots |
| **Field Barricade** | terrain (crate) | Half-cover screen that also blocks LOS (1 AP) | A quick screen now vs saving for a 2-AP wall |
| **Forge Beacon** | buff (morale) | Emboldens allies (+hit) in range | Group up for the beacon vs spread to spread risk |
| **Reinforce Armor** | buff (shield) | Shields Torren + adjacent allies (halves one hit) | Time it for the alpha strike, not the chip |
| **Battle Repairs** | heal | Restores a wounded ally in reach | Repair now, or shape the field first |

The signature play is **rubble one tile toward the enemy from a fragile ally**:
it gives that hero directional half cover (−25% enemy hit) *without* blocking the
hero's own shots — pure survivability that keeps the glass cannons firing.

## The proof (reproducible)
`scripts/forge_showcase_report.py` runs the **same party against the same
raiders** under two controllers that differ **only in Torren's behaviour**:

- **Torren BUILDS** (`forge_tactician_controller`): slows the charge, covers the
  backline, beacons, shields, repairs, body-blocks the choke, and only mops up a
  lone survivor once the backline is safe.
- **Torren BRAWLS** (`no_forge_controller`): advances and swings his (weak)
  hammer; **never uses a construct.**

Representative result (40 seeds each; competent backline identical in both):

| Controller | Wins | Losses |
|---|---|---|
| **Torren BUILDS** | **~87%** | **~5%** |
| **Torren BRAWLS** | ~22% | ~42% |

**The ~65-point win-rate gap — and the fact that building almost never *loses* the
party while brawling loses it ~40% of the time — is the proof that Torren's value
is his constructs, not his stats.** (Mirrors the Span's "tactics win / mindless
loses" evidence; win-rates are agent-run simulation, not a player-set bar.)

## Why brute force fails here (by design)
1. Torren's low damage means he can't delete the swarm himself.
2. The brutes charge the fragile backline; unscreened, a 20-HP mage dies in ~2
   hits.
3. Only *shaping* — slowing the charge, covering and shielding the backline,
   repairing, and holding the choke — buys the glass cannons the turns they need
   to win the trade.

## Design lessons (for the Encounter Design Bible)
- **Give a support identity a fight only that identity can win.** Weak-hitting
  Torren forces the player to value shaping over swinging.
- **Fragile allies + an aggressive swarm** make protection the win condition.
- **A partial natural choke** invites (but doesn't hand over) fortification.
- **Prove the identity by ablation:** run the same fight with the identity's kit
  turned off and show the outcome collapse.

## Revision History
| Date | Change |
|---|---|
| 2026-06 | Authored The Forge Stand showcase (runtime `tactical/showcase_forge.py`, report, tests). Added the `smith` class + six Field-Forge abilities (data), and a small additive `creates_object` option on the terrain effect handler so terrain abilities can place cover objects. Verified: building wins ~87% vs brawling ~22% over 40 seeds; harness 62/62; full suite green. No existing gameplay/data changed destructively. |
