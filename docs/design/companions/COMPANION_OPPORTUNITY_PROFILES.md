# Companion Opportunity Profiles

> **Canon Status:** CONFIRMED — 2026-06. Gameplay Canon (design authority); **Planned Additive**.
> **Authority:** Defines each companion's **battlefield identity** within Reactive Combat — the
> opportunities they specialize in recognizing, so the player learns *"Corwin noticed
> something,"* not *"a generic reaction appeared."* Opportunities are defined in
> [`OPPORTUNITY_CATALOGUE.md`](../OPPORTUNITY_CATALOGUE.md); pairings in
> [`PARTNER_TECHNIQUE_MATRIX.md`](../PARTNER_TECHNIQUE_MATRIX.md).
> **Cross-references:** [`REACTIVE_COMBAT.md`](../REACTIVE_COMBAT.md) ·
> [`companions/COMPANION_PROGRESSIONS.md`](COMPANION_PROGRESSIONS.md) · the Hero Bibles
> in [`../heroes/`](../../heroes/). Values `_TBD_` (balancing).

---

## Principle — specialization, not omniscience
Companions do **not** react to everything equally. Each has **Primary** opportunities they
recognize instantly and reliably, and **Secondary** ones they notice situationally. This makes
each companion's "voice" on the battlefield legible: the player learns to associate a bark and a
reaction style with a specific hero. Reacting to *fewer* things, *better*, is the goal.

For each companion: **Primary Opportunities · Secondary Opportunities · Preferred Battlefield
Role · Natural Reaction Style · Unique Resolve Generation.**

---

## Talos — the Wall
- **Primary:** Guard Broken · Ally Downed · Ally Surrounded · Ally Grabbed · Cornered · Near Wall
- **Secondary:** Airborne · Staggered · Enraged (baits it onto himself) · Near Cliff
- **Preferred role:** Frontline anchor; protector; choke-point holder.
- **Reaction style:** Defensive and interceptive — steps *in front of* danger, punishes broken
  guards, converts threats-to-allies into threats-to-himself. Bark: *"Get behind me."*
- **Unique Resolve:** Protecting allies · shield blocks · holding choke points. Talos is the
  party's **Resolve engine of last resort** — even a losing fight generates Resolve while he
  keeps people standing.

## Corwin — the Eye
- **Primary:** Exposed · Marked · Airborne · High Ground · Distracted · Near Explosive Object
- **Secondary:** Vulnerable · Pinned · Disarmed · Low Ground (enemy)
- **Preferred role:** Precision ranged executioner; spotter; opening-finisher.
- **Reaction style:** Patient and surgical — waits for a clean line and takes the shot that
  *ends* something. Bark: *"I've got a shot."*
- **Unique Resolve:** Precision attacks · critical hits · long-range executions. Corwin converts
  Major openings into kills, freeing Resolve for the next setup.

## Ragash — the Pack
- **Primary:** Isolated/flanking routes · Ally Flanking · Distracted · Grappled (her hounds) ·
  Ally Surrounded
- **Secondary:** Knocked Down · Marked · Cornered · Poisoned (bleed synergy)
- **Preferred role:** Flanker; encircler; mobile disruptor with the hound pack.
- **Reaction style:** Opportunistic and coordinated — reads the *space* and closes escape routes.
  Bark: *"They're surrounded."*
- **Unique Resolve:** Hound coordination · flanking · pack tactics. Every surround/combined
  strike banks Resolve.

## Eleanor — the Weaver
- **Primary:** Wet · Standing In Water · Standing On Ice · Rooted · Near Fire · Chilled/Frozen
  setups · Confused
- **Secondary:** Burning · Electrified · Scorched · Ally Protected (her wards)
- **Preferred role:** Battlefield-control mage; opportunity *creator* more than capitalizer.
- **Reaction style:** Systemic and combinatorial — sees the elemental/terrain reaction two steps
  ahead. Bark: *"I can use the terrain."*
- **Unique Resolve:** Elemental interactions · battlefield manipulation · supporting allies.
  Eleanor's chains (Wet→Frozen, etc.) *manufacture* the openings others cash in.

## Ronan — the Predator
- **Primary:** Terrified · Knocked Down · Airborne · Off Balance · Isolated prey · Cornered
- **Secondary:** Staggered · Distracted · Near Cliff · Enraged (matches it)
- **Preferred role:** Aggressive mobile bruiser; pursuer; finisher of the weak and fleeing.
- **Reaction style:** Explosive and instinctive — the moment prey is exposed, he wants to close.
  Bark: *"Now!"*
- **Unique Resolve:** Fear · pounces · predator gameplay · aggressive follow-ups — the strongest
  Resolve generators, but they push **Ferality** ([`../heroes/RONAN.md`](../../heroes/RONAN.md)), a
  built-in risk/reward tension.

## Torren — the Builder
- **Primary:** Near Destructible/Explosive Object · Under Hanging Structure · Near Wall ·
  Scorched · Pinned (his restraints)
- **Secondary:** Guard Broken · Petrified/Frozen (shatter) · Cornered · High Ground (emplacements)
- **Preferred role:** Engineer; area-denial and terrain-weaponizer; controls *where* fights happen.
- **Reaction style:** Deliberate and structural — turns the environment and his constructs into
  the opening. Bark direction: *"Bring it down."* (`_TBD_`)
- **Unique Resolve:** `_TBD_` — reinforce forge/engineering identity: **detonations/collapses,
  successful area-denial, and holding an engineered position.**

## Maeve Ashwood — the Anchor
- **Primary:** Ally Downed · Ally Surrounded · Ally Grabbed · Inspired/Ally Protected windows ·
  Terrified allies
- **Secondary:** Poisoned (cleanse) · Vulnerable (debuff read) · Confused
- **Preferred role:** Battlefield physician; keeps the party standing; sustains momentum.
- **Reaction style:** Protective and timely — reacts to *ally* states first, converting near-
  disasters into held lines. Bark direction: *"Stay with me."* (`_TBD_`)
- **Unique Resolve:** `_TBD_` — reinforce healing/keeping-people-standing identity: **clutch
  revives, timely saves, and sustaining an Inspired/Protected window.** Maeve's presence keeps
  Resolve *flowing* when the party is under pressure.

---

## Reading the battlefield (design intent)
Because profiles overlap only partially, a given opportunity usually has **one obvious owner**
and a couple of situational ones. This produces distinct "voices": Ally Downed → Talos/Maeve;
Exposed → Corwin; Wet → Eleanor; Terrified → Ronan; Destructibles → Torren; Surrounds → Ragash.
Party composition therefore changes *which opportunities the party can see and take* — a core
replayability lever.

## Document History
| Date | Change |
|---|---|
| 2026-06 | Created — battlefield-identity profiles for all seven companions (primary/secondary opportunities, role, reaction style, unique Resolve). Torren/Maeve Resolve specifics `_TBD_`. Documentation-only; Planned Additive. |
