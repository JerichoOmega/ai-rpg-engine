# Reactive Encounter Design — Factions & Opportunities

> **Canon Status:** CONFIRMED — 2026-06. Gameplay Canon (design authority); **Planned Additive**.
> **Authority:** How enemies and factions contribute to Reactive Combat — the openings they
> *offer*, the threats they *pose*, and the reactions they *invite*. Enemy families here map to
> the data roster in [`enemies/README.md`](enemies/README.md); opportunities to
> [`OPPORTUNITY_CATALOGUE.md`](OPPORTUNITY_CATALOGUE.md).
> **Cross-references:** [`REACTIVE_COMBAT.md`](REACTIVE_COMBAT.md) ·
> [`RESOLVE_ECONOMY.md`](RESOLVE_ECONOMY.md) · [`../systems/tactical_ai.md`](../systems/tactical_ai.md)

---

## Principle — enemies exist to create and deny opportunities
Every enemy is a **source of opportunities** for the party and a **denier** of others. Good enemy
design gives the player openings worth recognizing and punishes sloppy positioning. The tactical
texture of a fight comes from the *mix* of opportunities its enemies create — not from any single
overloaded unit. Each faction below defines: **Typical openings · Typical reactions · Weaknesses ·
Behavior patterns · Signature opportunity.**

---

## Bandits
- **Typical openings:** Off Balance, Distracted, Disarmed, Cornered (they break and flee).
- **Typical reactions:** punish overextension, cut off fleeing routes, backstab the distracted.
- **Weaknesses:** morale — fear and losing their leader scatters them (Enraged/Terrified cascades).
- **Behavior:** opportunistic, cowardly under pressure, target the weak, use ambush and numbers.
- **Signature opportunity:** *Fleeing/Distracted* clusters — ideal for Ragash flushes and Ronan
  pursuit; killing the leader creates a *Terrified* rout.

## Knights / Soldiers
- **Typical openings:** Guard Broken, Staggered, Off Balance (heavy, committed swings).
- **Typical reactions:** guard-break punishes (Talos), precision into the exposed gap (Corwin).
- **Weaknesses:** poise/stamina — sustained pressure shatters their guard; slow to reposition.
- **Behavior:** disciplined, hold formation and choke points, protect their line, punish rushes.
- **Signature opportunity:** *Guard Broken* after a whiffed heavy attack — the classic Talos+Corwin
  window; formations create *Cornered* if flanked.

## Undead
- **Typical openings:** Staggered, Knocked Down, Shattered (vs Frozen/Petrified), Scorched.
- **Typical reactions:** shatter frozen skeletons, area burn hordes, control chokes.
- **Weaknesses:** fire and holy; brittle to physical shatter; **Ignore** poison/fear/mental states.
- **Behavior:** relentless, fearless, no self-preservation, swarm in numbers, slow but tireless.
- **Signature opportunity:** *Frozen → Shatter* and *Burning* horde clears — Eleanor's element
  chains shine; mental/fear openings are wasted here (teach the player this).

## Beasts
- **Typical openings:** Off Balance, Airborne, Enraged, Terrified, Isolated.
- **Typical reactions:** bait the charge and counter, launch/juggle, herd the pack.
- **Weaknesses:** instinct-driven — baitable, provokable, and scared by a bigger predator (Ronan).
- **Behavior:** aggressive charges, pack tactics, wounded-animal recklessness, territorial.
- **Signature opportunity:** *Enraged charge* (bait → counter) and *Terrified* when Ronan asserts
  dominance — a natural Ronan/Ragash playground.

## Cultists
- **Typical openings:** Exposed (mid-ritual/channel), Confused, Vulnerable, Distracted.
- **Typical reactions:** interrupt the channel (huge value), execute exposed casters, disrupt buffs.
- **Weaknesses:** fragile bodies, dependent on rituals/summons and a leader; punished by interrupts.
- **Behavior:** support/summon from the back, buff and debuff, sacrifice fodder, protect the ritual.
- **Signature opportunity:** *Exposed while channeling* — a high-value interrupt window (Corwin's
  called shot); denying the ritual is the whole fight's tactical spine.

## Demons
- **Typical openings:** Threshold/Exposed (phase windows), Enraged, Scorched.
- **Typical reactions:** capitalize hard during exposed phases, bank Resolve between them.
- **Weaknesses:** bespoke, telegraphed vulnerabilities; often a specific counter-element or object.
- **Behavior:** powerful, phase-based, area threats, punish greed, warp the battlefield.
- **Signature opportunity:** **Legendary** exposed phases (see Tiers) — the party survives the
  onslaught, then unloads banked Resolve in a multi-character payoff.

## Constructs
- **Typical openings:** Guard Broken, Scorched, Exposed (weak points/cores), Pinned.
- **Typical reactions:** target exposed cores, melt armor (Scorched), immobilize and dismantle.
- **Weaknesses:** exposed cores/joints, heat/overload, immobile or slow; **Ignore** poison/fear.
- **Behavior:** methodical, area-denial, hold objectives, high armor, low adaptability.
- **Signature opportunity:** *Exposed core / Scorched armor* — Torren and Eleanor pry them open;
  the Corruption **Anchors** are a construct-style objective
  ([`encounters/the_corruption_avatar.md`](encounters/the_corruption_avatar.md)).

---

## Faction contrast table
| Faction | Offers most | Denies (Resist/Ignore) | Best answered by |
|---|---|---|---|
| Bandits | Fleeing/Distracted | — | Ragash, Ronan |
| Knights | Guard Broken | mobility openings | Talos, Corwin |
| Undead | Shatter/Burning | poison, fear, mental | Eleanor, area control |
| Beasts | Enraged/Terrified | — | Ronan, Ragash |
| Cultists | Exposed (channel) | — | Corwin, interrupts |
| Demons | Legendary phases | most CC between phases | banked Resolve, whole party |
| Constructs | Exposed core/Scorched | poison, fear, sometimes CC | Torren, Eleanor |

> **Design intent:** mixing factions mixes opportunity types, forcing the player to switch reads
> mid-fight (e.g. undead front line + cultist backline = *shatter the horde while interrupting the
> ritual*). Encounters escalate toward larger opportunities per the Tiers model
> ([`OPPORTUNITY_CATALOGUE.md`](OPPORTUNITY_CATALOGUE.md#opportunity-tiers-part-4--canonical-escalation-model)).

## Encounter checklist (Reactive Combat)
Every designed encounter must answer:
1. What opportunities does this enemy mix **offer** the party?
2. What does it **deny**, and is that denial telegraphed?
3. Which companions' reads does it reward — and does it punish a passive party?
4. How does it feed the **Resolve economy** ([`RESOLVE_ECONOMY.md`](RESOLVE_ECONOMY.md))?
5. Does it escalate toward at least one **Major/Legendary** moment?

## Document History
| Date | Change |
|---|---|
| 2026-06 | Created — Reactive Combat encounter design: per-faction opportunity/reaction/weakness/behavior/signature profiles (bandits, knights, undead, beasts, cultists, demons, constructs), faction contrast table, and an encounter design checklist. Documentation-only; Planned Additive. |
