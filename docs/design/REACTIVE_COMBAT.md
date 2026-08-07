# Reactive Combat, Resolve & Partner Techniques

> **Canon Status:** CONFIRMED — established 2026-06. **CORE COMBAT PILLAR.**
> **Authority:** This document is the **single source of truth** for the game's
> defining combat philosophy — *Reactive Combat*, the shared **Resolve** resource,
> **Command Decisions**, and **Partner Techniques**. It is **Gameplay Canon (design
> authority)** under [R-01](../design_decisions/R-01-combat-canon.md): it defines how
> combat should *feel*. It is **Planned Additive** — none of it is implemented yet;
> no gameplay code exists for it. The implementation authority remains the
> `tactical/` runtime + [`Combat_Gameplay_Architecture.md`](../../Combat_Gameplay_Architecture.md).
> **Cross-references:** [`GAME_BIBLE.md`](../GAME_BIBLE.md) · [`COMBAT_SYSTEM.md`](../COMBAT_SYSTEM.md) ·
> [`CORE_DESIGN_PILLARS.md`](CORE_DESIGN_PILLARS.md) (Pillar 3) ·
> [`companions/COMPANION_PROGRESSIONS.md`](companions/COMPANION_PROGRESSIONS.md) ·
> [`../companions/COMPANION_REACTIVITY_STANDARD.md`](../companions/COMPANION_REACTIVITY_STANDARD.md) ·
> [`architecture/ENGINE_INTERFACES.md`](../architecture/ENGINE_INTERFACES.md) ·
> [`architecture/LAYER_RULES.md`](../architecture/LAYER_RULES.md)

---

## 1. The Core Philosophy

> **"Every action creates opportunities."**

Reactive Combat is one of the **defining features** of the game. Combat should feel
like **leading an elite adventuring party that constantly recognizes openings on the
battlefield**.

Players are **not memorizing rotations**. They are:

- **Evaluating** situations
- **Creating** opportunities
- **Recognizing** opportunities
- **Deciding** whether they are worth capitalizing on

The player should constantly ask **"How can I create another opportunity?"** — never
**"Which attack does the most damage?"**

This pillar influences **all** future combat systems, companions, enemies, encounters,
bosses, UI, progression, tutorials, and ability design.

---

## 2. Resolve — the shared party resource

**Resolve** replaces the earlier placeholder notion of "team synergy"/"Synergy Points."
It is the party's fuel for coordinated techniques.

Resolve represents:

- Team **confidence**
- **Coordination**
- **Trust**
- **Tactical momentum**
- The party's ability to execute coordinated techniques **under pressure**

**Resolve is SHARED across the entire party. It is NOT individual.** One pool, spent by
the commander (the player) to authorize coordinated actions.

### Gaining Resolve — always earned, never passive

Players should **never passively gain Resolve.** It is earned by playing well. Sources
include:

- Exploiting enemy openings
- Flanking
- Saving allies
- Perfect blocks
- Guard breaks
- Critical hits
- Environmental interactions
- Successful reactions
- Smart positioning
- Coordinated teamwork

Every companion eventually has **unique, identity-reinforcing** ways to generate Resolve
(see §7 and the per-companion tables).

### Feedback — every gain is felt

Every Resolve gain **must** include:

- **Visual feedback**
- **Audio cue**
- **UI pulse**

> The player should always know they **earned** it. Resolve gain should feel satisfying.

---

## 3. Reactive Combat — decision support, not a QTE

Reactive Combat is **NOT a quick-time event.** The slowdown exists **only** to give the
player enough time to make a tactical decision. It is an **accessibility and
decision-support feature**, not a cinematic flourish.

When an opportunity appears:

1. **Time slows significantly.**
2. The player is shown the **available reactions**.
3. The player **chooses** whether to authorize one.

**If they decline, combat simply continues. Nothing is wasted. No penalty.** Declining is
always a valid, cost-free choice.

---

## 4. Command Decisions — the commander fantasy

Companions **identify** opportunities. The player **authorizes** them.

> **"Corwin has a clear shot."**
> Authorize *Skyhunter's Gambit*? — Cost: **2 Resolve**

The fantasy: the companions are **intelligent**; they recognize openings. The player is
the **commander making the final decision.** Companions **never remove player agency** —
they surface options; the player decides.

---

## 5. Partner Techniques — intentionally created opportunities

Partner Techniques are **separate from Reactive Combat**:

| System | Who creates the opportunity |
|---|---|
| **Reactive Combat** | The **battlefield** creates the opportunity (the player reacts) |
| **Partner Techniques** | The **player intentionally** creates the opportunity |

Partner Techniques require:

- Specific **companion combinations**
- **Positioning**
- **Resolve**
- **Availability** (cooldown / state)

They are **spectacular, cinematic** abilities — inspired by *Marvel: Ultimate Alliance* —
while remaining fully **integrated into tactical gameplay** (they still obey positioning,
targeting, and the Resolve economy; spectacle never overrides tactics).

---

## 6. Companion Intelligence — companions recognize openings

Companions should eventually **recognize opportunities automatically** and voice them, in
character:

| Companion | Bark |
|---|---|
| Corwin | *"I've got a shot."* |
| Talos | *"Get behind me."* |
| Ragash | *"They're surrounded."* |
| Eleanor | *"I can use the terrain."* |
| Ronan | *"Now!"* |

The player **still approves** the action. Companions identify; the commander decides.
Intelligence never becomes automation.

---

## 7. Companion Resolve Identity

Every combat companion generates Resolve in ways that **reinforce their class identity**.
Confirmed direction (exact values `_TBD_` during balancing):

| Companion | Identity | Resolve-generation focus |
|---|---|---|
| **Talos** | Frontline Defender | Protecting allies · shield blocks · holding choke points |
| **Corwin** | Ranger (precision) | Precision attacks · critical hits · long-range executions |
| **Ragash** | Houndmaster | Hound coordination · flanking · pack tactics |
| **Eleanor** | Elemental Mage | Elemental interactions · battlefield manipulation · supporting allies |
| **Ronan** | Werewolf Warrior | Fear · pounces · predator gameplay · aggressive follow-ups |
| **Torren** | Construct Engineer | `_TBD_` — reinforce forge/engineering identity |
| **Maeve Ashwood** | Battlefield Physician | `_TBD_` — reinforce healing/keeping-people-standing identity |

Each companion also gets **unique Partner Techniques** with specific partners (§5) — those
combinations are authored per relationship and are `_TBD_`.

---

## 8. Companion Relationships affect combat

Relationship progression (see [`journey_system.md`](../systems/journey_system.md)) **changes
combat.** As companions grow closer:

- Better **coordination**
- **Faster** animations
- New **Partner Techniques**
- Additional **reactions**
- Unique **dialogue**
- Improved **teamwork**

**Animations evolve over the campaign to show increasing trust** — early-game partners are
stiff and tentative; late-game partners move as one. This ties Reactive Combat directly to
Pillar 5 (Companion-Driven Narrative).

---

## 9. Ronan — Ferality integrates with Reactive Combat

Ronan retains the **Ferality system** — a long-term psychological mechanic unique to him.
Using werewolf abilities **increases Ferality**; higher Ferality grants **greater combat
power** while increasing **narrative and gameplay risk**. Ferality integrates naturally
with Reactive Combat and Resolve: predator openings (fear, pounces, aggressive follow-ups)
are strong Resolve generators, but leaning on them pushes Ferality upward. See
[`heroes/RONAN.md`](../heroes/RONAN.md).

---

## 10. Combat Goals

Combat should encourage: **smart positioning · creative thinking · environmental
interaction · teamwork · relationship building · spectacular cinematic moments.**

## 11. Design Philosophy — the four goals

Combat should feel like **directing an epic fantasy action film while preserving tactical
depth.** Every major ability must satisfy **all four**:

1. **Spectacular presentation**
2. **Tactical value**
3. **Character storytelling**
4. **Meaningful player choice**

---

## 12. Architecture note (engine-agnostic)

These systems must stay **engine-independent** ([`LAYER_RULES.md`](../architecture/LAYER_RULES.md)):

- **Core (rules):** the Resolve economy (a single shared party value), opportunity
  *detection*, the list of available reactions, Resolve costs, Partner-Technique
  eligibility, and applying an authorized action's effects. All headless & testable.
- **Presentation (terminal today / Godot later):** the **time-slow**, the reaction prompt,
  the authorize/decline input, and the visual/audio/UI-pulse feedback for Resolve gain.
- **Contract:** the core emits an *opportunity* event (with the candidate reactions and
  their Resolve costs) and exposes current Resolve; the presentation renders it and returns
  an *authorize(reaction_id)* or *decline*. Declining is a no-op. See
  [`ENGINE_INTERFACES.md`](../architecture/ENGINE_INTERFACES.md).

---

## Document History

| Date | Change |
|---|---|
| 2026-06 | Created — canonical Reactive Combat pillar: Resolve (shared, earned), Reactive Combat (decision-support slowdown, not a QTE), Command Decisions, Partner Techniques, Companion Intelligence, relationship-driven combat, Ronan Ferality integration, and the four ability goals. Gameplay Canon / Planned Additive; no code. |
