# Opportunity Catalogue — Master Battlefield Reference

> **Canon Status:** CONFIRMED — 2026-06. **CORE COMBAT REFERENCE.**
> **Authority:** The authoritative master list of every battlefield **opportunity** the
> Reactive Combat pillar is built on. Gameplay Canon (design authority); **Planned Additive** —
> nothing here is implemented. Exact durations/values are balancing targets (`_TBD_`).
> **Guiding principle:** *"Every action creates opportunities."*
> **Cross-references:** [`REACTIVE_COMBAT.md`](REACTIVE_COMBAT.md) (pillar) ·
> [`companions/COMPANION_OPPORTUNITY_PROFILES.md`](companions/COMPANION_OPPORTUNITY_PROFILES.md) ·
> [`PARTNER_TECHNIQUE_MATRIX.md`](PARTNER_TECHNIQUE_MATRIX.md) ·
> [`RESOLVE_ECONOMY.md`](RESOLVE_ECONOMY.md) ·
> [`REACTIVE_ENCOUNTER_DESIGN.md`](REACTIVE_ENCOUNTER_DESIGN.md)

---

## How to read this catalogue

An **opportunity** is a temporary battlefield condition that makes a specific reaction
*worth doing right now*. When one appears, the owning companion may **recognize** it (a bark),
and the player-commander may authorize a **reaction** or **Partner Technique** for **Resolve**
([`REACTIVE_COMBAT.md`](REACTIVE_COMBAT.md)). Declining is always free.

Every entry defines: **Description · How it's created · Duration · Recognized by · Example
reactions · Stacks? · Boss handling.** Companion keys: **T** Talos · **C** Corwin · **R** Ragash ·
**E** Eleanor · **Ro** Ronan · **To** Torren · **M** Maeve.

**Duration bands** (exact = `_TBD_`): *Instant* (this authorization window only) · *Short*
(~1 round) · *Medium* (~2–3 rounds) · *Positional* (lasts while the spatial condition holds).

**Boss handling** uses a shared vocabulary (see [Boss Interaction Rules](#boss-interaction-rules)):
*Normal* · *Resist* (shorter/weaker) · *Threshold* (only during a stagger/exposed phase) ·
*Ignore* (immune) · *Special* (bespoke per boss).

---

## PHYSICAL opportunities

| Opportunity | Description | How created | Duration | Recognized by | Example reactions | Stacks? | Boss handling |
|---|---|---|---|---|---|---|---|
| **Airborne** | Enemy launched off the ground; cannot act or defend | Uppercuts, launch abilities, knockback into slopes | Short | T, C, Ro | Slam back down; aerial arrow; intercept juggle | No (re-launch refreshes) | Threshold (only when staggered) |
| **Knocked Down** | Prone; reduced defence, slow to rise | Heavy blows, trips, shield bash, pounce | Short | T, Ro, R | Ground execution; pin; stomp | No | Resist (rises faster) |
| **Guard Broken** | Defence shattered; open to a clean hit | Guard-break attacks, sustained pressure, heavy stagger damage | Short | T, To | Punish strike; guard-break Partner Technique | No | Threshold |
| **Staggered** | Reeling; interrupted and briefly slowed | Interrupts, big impacts, breaking poise | Short | T, To, Ro | Follow-up; reposition safely; combo opener | Yes (deepens toward Guard Broken) | Resist / Threshold |
| **Pinned** | Held in place by a weapon/force; cannot move | Pinning shots, spears, Torren restraints | Medium | C, To | Free hits; set up flank; area effect on the spot | No | Ignore (most bosses) |
| **Grappled** | Physically seized by an ally/hound; controlled | Ragash hounds, Talos hold, Ronan grab | Medium | R, T, Ro | Focus fire the held target; execute; throw | No | Ignore |
| **Off Balance** | Momentarily unsteady; next hit lands harder | Feints, shoves, terrain, missing a heavy swing | Instant | T, C, Ro | Quick capitalize strike; shove into hazard | Yes | Resist |
| **Disarmed** | Lost weapon; damage/threat sharply reduced | Disarm strikes, precision shots to weapon hand | Medium | C, T | Press advantage; ignore to pursue casters | No | Ignore |
| **Vulnerable** | Generic "defence down" window (armor/resist reduced) | Debuffs, marks, breaking cover, rear exposure | Medium | C, E, M | Any high-value hit; focus target | Yes (with other debuffs) | Resist |
| **Cornered** | No safe retreat; movement options denied | Pushing toward walls/cliffs, encirclement | Positional | T, R, Ro | Encircle; area denial; forced fight | No | Special |

---

## ELEMENTAL opportunities

| Opportunity | Description | How created | Duration | Recognized by | Example reactions | Stacks? | Boss handling |
|---|---|---|---|---|---|---|---|
| **Burning** | On fire; damage over time, may panic | Fire abilities, oil + spark, scorched terrain | Medium | E, C | Spread fire; push into more fire; ranged execute | Yes (intensity) | Resist (fire-immune bosses Ignore) |
| **Frozen** | Encased; cannot act; shatters under impact | Deep cold, water + frost combo | Short | E, T, Ro | Shatter strike (bonus vs frozen); free positioning | No | Ignore / Threshold |
| **Chilled** | Slowed and brittle; a step toward Frozen | Frost, cold terrain | Medium | E | Stack toward Frozen; kite; slow the charge | Yes (→ Frozen) | Resist |
| **Wet** | Soaked; amplifies lightning, enables freeze | Water terrain, rain, splash | Medium | E | Electrify; freeze; combo setup | Yes | Normal |
| **Electrified** | Conducting current; chains to nearby wet/metal | Lightning on wet/metal targets | Short | E, C | Chain lightning; stun follow-up | Yes | Resist |
| **Poisoned** | Damage over time; weakened | Poison weapons, spores, hazards | Medium | R, M, C | Let it tick + control; execute low targets | Yes (stacks) | Resist (undead/constructs Ignore) |
| **Rooted** | Anchored in place by vines/ice; can act, can't move | Entangle, frost, terrain control | Medium | E, C, R | Ranged focus; flank freely; area effect | No | Ignore |
| **Petrified** | Turned to stone; fully disabled, fragile | Rare petrify effects | Short | E, To | Shatter (like Frozen); reposition | No | Ignore |
| **Scorched** | Armor/resist burned away; takes more damage | Sustained fire, thermite, Torren heat | Medium | To, E, C | Focus fire; guard-break follow-up | Yes (with Vulnerable) | Resist |

---

## MENTAL opportunities

| Opportunity | Description | How created | Duration | Recognized by | Example reactions | Stacks? | Boss handling |
|---|---|---|---|---|---|---|---|
| **Terrified** | Fleeing or frozen in fear; won't fight well | Ronan's predator presence, horror abilities | Medium | Ro, M | Cut off escape; pounce; herd into hazards | No | Ignore (most bosses fearless) |
| **Distracted** | Attention elsewhere; open to a surprise hit | Feints, ally draws aggro, sudden noise | Short | C, R, Ro | Backstab; flank; sneak shot | Yes | Resist |
| **Confused** | Acts unpredictably / mis-targets | Illusions, disorientation, concussive hits | Medium | E, M | Let it hit its allies; reposition safely | No | Ignore |
| **Enraged** | Reckless; hits harder but drops defence | Taunts, provocation, pain thresholds | Medium | T, Ro | Bait + counter; guard for the party; punish overextension | No | Special (boss enrage = Legendary window) |
| **Inspired** *(ally)* | Buffed morale/coordination window | Talos Battlecry, Maeve support | Medium | T, M | Chain a Partner Technique; press the advantage | Yes | N/A (ally state) |
| **Marked** | Tagged as a priority target; easier to hit/track | Corwin's mark, hunter's mark, spotting | Medium | C, R | Focus fire; guaranteed-crit follow-up | Yes | Resist (short on bosses) |
| **Exposed** | A weak point/opening is briefly revealed | Breaking cover, rear arc, phase transitions | Short | C, To | Precision execute; called-shot Partner Technique | Yes (with Vulnerable) | Threshold |

---

## ENVIRONMENTAL opportunities

| Opportunity | Description | How created | Duration | Recognized by | Example reactions | Stacks? | Boss handling |
|---|---|---|---|---|---|---|---|
| **Near Cliff / Ledge** | An enemy stands beside a fatal drop | Positioning, pushing toward the edge | Positional | T, R, Ro | Shove off; knockback ring-out | No | Ignore (most bosses immovable) |
| **Near Wall** | Backed against a hard surface; can't retreat | Herding, corners | Positional | T, To | Slam into wall (bonus); pin; corner control | No | Special |
| **Standing In Water** | On/soaked terrain; enables freeze/shock | Terrain | Positional | E | Electrify; freeze the tile | Yes | Normal |
| **Standing On Ice** | Slippery; easy to knock/slide | Terrain / Eleanor frost | Positional | E, T | Shove for a slide; combo knockdown | No | Resist |
| **Near Explosive Object** | Barrel/cache that detonates when struck | Level design, Torren placement | Positional | To, C, E | Shoot/ignite it; area burst | No | Normal |
| **Near Destructible Object** | Cover/structure that can be collapsed | Level design | Positional | To, T | Collapse for damage/area denial | No | Normal |
| **Under Hanging Structure** | Chandelier/rockfall overhead | Level design | Positional | C, To | Drop it (heavy damage/CC) | No | Special |
| **Near Fire** | Adjacent to flame/hazard | Terrain / spread | Positional | E, Ro | Push into fire; spread; zone | Yes | Resist |
| **High Ground** *(ally)* | Elevation grants range/accuracy edge | Positioning | Positional | C, T | Take the shot; hold the line above | N/A | N/A |
| **Low Ground** *(enemy)* | Enemy below the party; disadvantaged | Positioning | Positional | C, R | Rain fire; charge downhill | N/A | Normal |

---

## ALLY-STATE opportunities

| Opportunity | Description | How created | Duration | Recognized by | Example reactions | Stacks? | Boss handling |
|---|---|---|---|---|---|---|---|
| **Ally Grabbed** | A companion is seized/held by an enemy | Enemy grapples/CC | Medium | T, Ro, R | Free them (guard break); focus the grabber | No | N/A |
| **Ally Downed** | A companion at 0 HP, needs revival | Combat damage ([`COMBAT_SYSTEM.md`](../COMBAT_SYSTEM.md) Downed) | Medium | T, M | Revive (Support Action); shield the spot; avenge | No | N/A |
| **Ally Surrounded** | A companion encircled by enemies | Enemy positioning | Positional | T, R, M | Break the ring; taunt-pull; area clear | No | N/A |
| **Ally Protected** *(state)* | An ally is under a guard/ward; safe to be bold | Talos guard, Eleanor ward, Maeve shield | Medium | T, E, M | Aggressive push while covered; overextend safely | Yes | N/A |
| **Ally Flanking** | An ally is in position for a coordinated hit | Positioning | Instant | R, C, Ro | Partner Technique; simultaneous strike | Yes | N/A |

---

## Opportunity Tiers *(Part 4 — canonical escalation model)*

Opportunities come in three tiers. Encounters should escalate naturally from Minor toward
Legendary, so the *feel* builds from quick capitalizations to a cinematic payoff.

| Tier | Rarity | Resolve | Presentation | What it is | Typical source |
|---|---|---|---|---|---|
| **Minor** | Common (many per fight) | Low | Quick reaction animation, light time-slow | A small opening — a single quick reaction | Off Balance, Distracted, Marked, most PHYSICAL/ELEMENTAL states |
| **Major** | Occasional | Moderate | Cinematic camera, signature animation | A **signature reaction** or a **Partner Technique** window | Guard Broken, Airborne, Exposed, Ally Downed, strong environmental setups |
| **Legendary** | Rare (often boss-driven) | High | Massive cinematic payoff; **multi-character** | A set-piece the whole party participates in | Boss enrage/exposed phase, collapsing structures, cliff ring-outs, chained combos |

### Escalation model
- **Early fight:** Minor opportunities teach the loop — create/recognize/capitalize cheaply.
- **Mid fight:** the party banks Resolve and sets up **Major** windows (deliberate Partner
  Techniques, environmental plays).
- **Climax / boss:** a **Legendary** opportunity opens (e.g. the Corruption Avatar's exposed
  phase — [`encounters/the_corruption_avatar.md`](encounters/the_corruption_avatar.md)); the
  banked Resolve pays off in a multi-character finisher.
- Rule of thumb: **Minor opportunities generate the Resolve that Major/Legendary ones spend**
  (see [`RESOLVE_ECONOMY.md`](RESOLVE_ECONOMY.md)).

---

## Boss Interaction Rules

Bosses must not be trivialized by opportunities, but must never feel *immune to tactics*.

- **Resist:** the opportunity applies but is shorter/weaker (e.g. a boss rises from Knocked
  Down almost immediately). Still worth creating; rarely worth building around.
- **Threshold:** the opportunity only lands during a designed **stagger/exposed phase** (poise
  bar, phase transition). This is the intended way to open bosses — the tactical lesson is
  *create the phase, then capitalize*. Ties directly to boss "phase" design.
- **Ignore:** the boss is immune (hard CC like Frozen/Pinned/Grappled on most bosses). Telegraph
  the immunity so the player learns to pursue other openings.
- **Special:** a bespoke, authored interaction (a boss that *can* be shoved off a ledge only
  after its legs are broken, etc.) — reserved for set-pieces.

> **Design guarantee:** every boss must offer **at least one reliable opportunity path** to
> capitalize on (usually a Threshold phase). A boss with no exploitable opening violates the
> pillar.

---

## Stacking & interaction principles
- Debuff-style states (Vulnerable, Marked, Scorched, poison) **stack** into bigger windows.
- Hard-disable states (Frozen, Petrified, Grappled, Pinned) **do not stack** — re-applying
  refreshes duration.
- **Chains are intended:** Wet → Electrified/Frozen; Chilled → Frozen; Staggered → Guard Broken;
  Airborne → Knocked Down. Chains are where Minor opportunities snowball into Major ones.

---

## Using this catalogue (mandatory reference)
When designing any ability, enemy, boss, status effect, equipment piece, map, or environmental
object, the designer must state **which catalogue opportunities it creates, recognizes, or
capitalizes on** (Reactive Combat Design Rule 1 — [`REACTIVE_COMBAT.md`](REACTIVE_COMBAT.md)).
New opportunities are added here first, with all seven fields, before being referenced elsewhere.

## Document History
| Date | Change |
|---|---|
| 2026-06 | Created — master opportunity catalogue (Physical, Elemental, Mental, Environmental, Ally-state), per-entry fields, three-tier escalation model, and boss interaction rules. Documentation-only; Planned Additive. |
