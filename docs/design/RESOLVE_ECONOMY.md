# Resolve Economy

> **Canon Status:** CONFIRMED — 2026-06. Gameplay Canon (design authority); **Planned Additive**.
> **Authority:** The full design of the shared **Resolve** resource — how it is earned, spent,
> and balanced so it **rewards tactical play, never passive waiting.** All numbers here are
> **balancing targets/illustrations (`_TBD_`)**, not committed values.
> **Cross-references:** [`REACTIVE_COMBAT.md`](REACTIVE_COMBAT.md) ·
> [`OPPORTUNITY_CATALOGUE.md`](OPPORTUNITY_CATALOGUE.md) ·
> [`PARTNER_TECHNIQUE_MATRIX.md`](PARTNER_TECHNIQUE_MATRIX.md) ·
> [`REACTIVE_ENCOUNTER_DESIGN.md`](REACTIVE_ENCOUNTER_DESIGN.md)

---

## What Resolve is
One **shared party pool** representing confidence, coordination, trust, and tactical momentum.
It is **always earned, never passive** — there is no per-turn trickle, no regen-while-idle. If the
party stops making good plays, Resolve stops growing. This is the core anti-"turtle" guarantee.

## Earning Resolve
Resolve is granted by **actions the design wants to reward** (from
[`OPPORTUNITY_CATALOGUE.md`](OPPORTUNITY_CATALOGUE.md)). Illustrative gains (`_TBD_`):

| Source | Band | Notes |
|---|---|---|
| Exploiting an opening (capitalizing a Minor opportunity) | +Small | The bread-and-butter generator |
| Flanking / smart positioning | +Small | Rewards movement and setup |
| Perfect block / guard break | +Small–Medium | Rewards defensive skill (Talos) |
| Critical hit / precision execution | +Small–Medium | Rewards precision (Corwin) |
| Environmental interaction (explosive, collapse, hazard) | +Medium | Rewards using the map (Torren/Eleanor) |
| Successful authorized reaction | +Small | The loop feeds itself |
| Saving/reviving an ally, holding a surrounded ally | +Medium | Rewards teamwork (Talos/Maeve) |
| Coordinated teamwork (Partner setup) | +Medium | Rewards intentional combos |

**Every gain fires visual + audio + a UI pulse** ([`REACTIVE_COMBAT.md`](REACTIVE_COMBAT.md)) so
the player always knows they earned it. Diminishing returns on spammed identical sources prevent
degenerate farming (`_TBD_`).

## Expected gain per encounter (targets)
| Encounter type | Expected Resolve generated | Design intent |
|---|---|---|
| Trivial skirmish | Low | A couple of Minor reactions; not enough to bank big |
| Standard encounter | Moderate | Enough for several Minor reactions + one Major (a Partner Technique) |
| Elite / set-piece | High | Multiple Majors; banking toward a Legendary |
| Boss | Highest, but gated | Flows in bursts tied to the boss's opportunity phases (below) |

## Spending Resolve
| Spend | Cost band | Notes |
|---|---|---|
| **Minor reaction** (Command Decision) | Low | Quick capitalize; the common spend |
| **Signature reaction** | Moderate | A companion's hero-defining reaction |
| **Partner Technique (Major)** | Moderate–High | Two-companion cinematic combo |
| **Legendary Technique** | High | Rare, often multi-character, boss-phase payoff |

**Declining costs nothing.** The player should frequently decline Minor opportunities to bank
Resolve for a Major/Legendary window — that tension *is* the economy.

## Balancing principles
- **Minors fund Majors:** a fight generates many cheap opportunities; the player chooses which to
  spend on now vs. bank. Roughly, several Minor gains should equal one Major spend (`_TBD_`).
- **Partner Techniques** priced so a well-played standard encounter affords ~one; a set-piece
  affords a few. They must feel *earned*, not spammable.
- **Legendary Techniques** priced above what a single normal encounter yields — they require
  **banking across the fight** or a boss's high-Resolve phase, guaranteeing a "big moment" cadence
  rather than constant fireworks.
- **No passive floor:** there is no minimum trickle; a passive party runs dry. Aggression *and*
  smart defence both pay — but *waiting* does not.
- **Party-composition texture:** different companions generate Resolve differently
  ([`companions/COMPANION_OPPORTUNITY_PROFILES.md`](companions/COMPANION_OPPORTUNITY_PROFILES.md)),
  so the *rate and flavour* of the economy shifts with the roster — a replayability lever.

## Bosses & Resolve flow
Boss fights shape the economy deliberately ([`REACTIVE_ENCOUNTER_DESIGN.md`](REACTIVE_ENCOUNTER_DESIGN.md)):
- Bosses **Resist/Ignore** many opportunities, so the steady Minor drip is *lower* early — the
  party must generate Resolve off adds, positioning, and defence.
- A boss's **Threshold/exposed phase** opens a **high-Resolve, high-spend window**: the banked
  pool pays off in Major/Legendary techniques during the opening the party worked to create.
- This produces the intended rhythm: **survive & bank → boss opens → spend big → repeat.**

## Anti-patterns (explicitly avoided)
- Resolve that regenerates while idle (rewards turtling).
- A single dominant generator (collapses build diversity).
- Techniques cheap enough to spam (kills the "earned moment" feel).
- Costs so high the resource is never spent (kills the loop).

## Document History
| Date | Change |
|---|---|
| 2026-06 | Created — full Resolve economy: earning sources & bands, per-encounter targets, spend costs, Minor-funds-Major balancing, boss Resolve-flow rhythm, and explicit anti-patterns. All values `_TBD_`; Planned Additive. |
