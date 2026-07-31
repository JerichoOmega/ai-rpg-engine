# Krath the Unyielding — Boss Encounter

> **Document Status:** Canonical as of July 2026.
> **Authority:** This document defines the stat block, combat behavior, non-combat handling, and campaign-stage progression for Krath the Unyielding, the Corrupted champion of the Stonefang Tribe. All encounters involving Krath must align with this document and with the Stonefang Corruption Manifestation in [`docs/world/goblin_tribes.md`](../world/goblin_tribes.md).
> **Cross-references:** [`docs/world/goblin_tribes.md`](../world/goblin_tribes.md) · [`docs/world/WORLD_BIBLE.md`](../world/WORLD_BIBLE.md) · [`docs/systems/combat.md`](../systems/combat.md) · [`docs/quests/goblin_tribe_quests_tier2.md`](../quests/goblin_tribe_quests_tier2.md)

---

## Who Krath Is When the Party Meets Him

Krath was the Stonefang's greatest fighter before the Corruption touched him, and everything the Corruption has done to him runs through that fact. He is not a monster wearing a goblin's shape — he is a champion whose defining virtue (he does not stop) has been amplified into his destruction (he *cannot* stop). Per canon: he wins every confrontation, kills more than the tribe can use, has twice ignored Grakkor's direct orders citing enemies no one else could see, and radiates something that elevates aggression in warriors who spend time near him. Hounds refuse to approach his tent. His trophy wall has grown grotesque, with pieces no acknowledged raid explains.

**The tragedy the AI DM must preserve:** Krath is not evil. He is lost. Every version of this encounter — combat, containment, or diplomacy — should carry the weight that destroying him is a loss the tribe will feel, and that by his own culture's framework he has done nothing wrong: a warrior who wins is a warrior who is right.

---

## Stat Block

Krath is a boss-tier enemy following the standard enemy structure ([`docs/systems/combat.md`](../systems/combat.md)). His numbers scale by **Corruption Stage** (see Progression below). Stage II is the default if the campaign state gives no strong signal.

| Field | Stage I — The Champion | Stage II — The Unyielding | Stage III — The Hollow Champion |
|---|---|---|---|
| `name` | "Krath the Unyielding" | "Krath the Unyielding" | "Krath the Unyielding" |
| `hp` / `max_hp` | 140 | 190 | 240 |
| `damage` | 22 | 28 | 34 |
| `crit_chance` | 15 | 20 | 25 |
| `elite` | `True` | `True` | `True` |
| `boss` | `True` | `True` | `True` |
| `status_effects` | `[]` | `[]` | `[]` |

*(For scale: a standard goblin runs ~35 hp / 8 damage; the ancient dragon, the game's top boss, runs 250 / 35. Stage III Krath is deliberately near dragon-tier — a Corrupted champion is a campaign-significant threat, not a strong goblin. `crit_chance` is a percentage checked against a 1–100 roll, per the engine's convention.)*

### Corruption-Enhanced Traits

These express the three canonical Corruption effects — uncontrollable aggression, strength beyond normal goblin limits, and pain that no longer registers — as combat behavior. Like the phase behaviors below, Unyielding Focus and Aggression Bleed require engine support (per-attacker damage tallies; ally stat modification) before `combat.py` can enforce them; until then the AI DM applies them as narrative-overlay rules:

| Trait | Effect |
|---|---|
| **Ignores Pain** | Krath shows no reaction to damage and never behaves as if wounded. The AI DM should narrate hits landing *without* narrating him weakening — the party gets no visual feedback on his hp until a phase transition. This is deliberately unnerving: the usual signal that a fight is being won is absent. |
| **Cannot Disengage** | Krath never flees, never accepts surrender mid-combat, and never stops when a fight is "won." If a party member goes down, he continues attacking the downed target unless another combatant forces his attention (see Unyielding Focus). Enemies who flee are pursued. |
| **Unyielding Focus** | Krath locks onto whichever combatant last dealt him the most damage in a round and attacks that target until someone exceeds it. A coordinated party can use this — his aggression is total but *predictable*, and rotating his focus is the intended tactical solution for parties that cannot out-tank him. |
| **Aggression Bleed** | Any Stonefang warriors fighting alongside Krath fight at elite intensity (+10 hp, +3 damage — the standard elite modifier) from proximity exposure. They also will not retreat while Krath stands. Defeating or removing Krath first breaks this: surviving warriors revert to normal goblin behavior, including withdrawal. |

### Phase Behavior

> **Implementation status:** the current engine's boss handling applies generic damage boosts at fixed hp thresholds and named `special_attack` values only for existing bosses (`bosses.py`). The phase behaviors below — the named specials, the once-per-phase rule, the double attack, and the crit doubling — are **authored design that requires engine support before they are runnable in `combat.py`**. Until that support exists, the AI DM treats this table as narrative-overlay guidance layered on the engine's generic boss escalation: narrate the phase beats, and let the engine's standard boss damage boosts stand in for the mechanical escalation.

| Phase | Trigger | Special behavior |
|---|---|---|
| **Phase 1 — The Champion** | Combat start | Standard attacks with Unyielding Focus. Krath fights with visible skill — this is still the greatest warrior the Stonefang ever produced, and the AI DM should narrate technique, not frenzy. |
| **Phase 2 — The Slip** | hp ≤ 50% | Special attack: **"unseen enemies"** — once per phase, Krath attacks a point where no one is standing, striking at the enemies only he can see. The round's damage is wasted, but his *next* attack gains +50% damage as he redirects the frenzy. This is the canonical madness made mechanical: the party watches him fight something that is not there, and learns his openings come at his worst moments. |
| **Phase 3 — The Break** | hp ≤ 25% | Special attack: **"the unyielding"** — Krath attacks twice per round and his crit chance doubles (to 30 / 40 / 50 by stage). He is no longer defending at all. Narratively, whatever was left of the champion's technique is gone; this phase should read as pure Corruption, and it is the point where merciful parties get their last, best opening (see Stopping Krath Without Killing Him). |

---

## Encounter Notes

### When Krath Appears

Krath is **not** a random encounter. He appears only through authored triggers, in rough order of likelihood:

1. **The disproportionate raid** (canonical first sign): the party investigates or interrupts a Stonefang raid that burned rather than looted and killed rather than captured — and Krath is leading it, still fighting after the fight is over.
2. **Grakkor's quiet request**: Grakkor, as the canonical reluctant quest source, cannot publicly name his champion a problem without triggering a leadership challenge. He can point the party at Krath obliquely — a hunting party that "needs observing," a raid that "exceeded its orders."
3. **The Proving aftermath** ([`docs/quests/goblin_tribe_quests_tier2.md`](../quests/goblin_tribe_quests_tier2.md)): any resolution of Varkk's challenge that openly names Krath's taint makes Krath himself the tribe's next acknowledged problem — and the party the people who understand it.
4. **His own trajectory**: if the party ignores every thread, Krath's canonical endpoint arrives on its own — a Corrupted champion at the head of a raiding force that no longer calculates risk, encountered as a regional crisis rather than a tribal one.

### What Triggers Him

In any face-to-face situation, the AI DM should track what pushes Krath from unsettling to violent:

- **Being blocked** — any physical obstruction of where he is going or what he is doing. He does not route around obstacles anymore; he goes through them.
- **Being challenged** — anything a Stonefang would read as a challenge (a drawn weapon, a raised voice, stepping between him and a kill) is accepted instantly and totally. There is no posturing phase. Stonefang confrontation culture normally has structure — announcements, three days' notice, submission rules. Krath has lost all of it.
- **Being denied** — refusing him something he has decided is his (a trophy, a target, passage) reads to him as an enemy revealing itself.
- **The invisible enemies** — unpredictably, Krath reacts to things that are not there. A conversation can end because something over the party's shoulder, visible only to him, moved.

### Combat vs. Diplomacy

**In combat**, Krath is the encounter this document's stat block defines. The AI DM should play him as relentless, focused, and — critically — *not cruel*. He does not taunt, does not savor, does not monologue. He fights the way a landslide moves.

**In diplomacy**, the window is narrow but real, and it is not persuasion in any normal sense:

- Krath can still be *reached* through the Stonefang's own forms. He responds to strength-language: a party that has visible standing with the tribe, carries trophies he can read, or has Grakkor's explicit backing gets more sentences out of him than one that leads with reason.
- He cannot be talked out of what he is doing, because from inside his frame nothing is wrong. Arguments that he is sick, cursed, or dangerous are processed as challenges (see above).
- What *can* work: redirecting him. Krath still accepts targets. A party that gives his aggression somewhere to go — a genuine threat, a Proving-sanctioned bout, a hunt — can move him without fighting him. This is containment, not cure, and each redirection buys days, not weeks.
- **The Debt of Steel does not function.** If Krath spared anyone before his corruption, the debt still binds culturally — but invoking it now buys only hesitation, a single round of stillness while something old surfaces, before the Corruption closes over it again. The AI DM can use that round; the party only gets it once.

### Stopping Krath Without Killing Him

Killing Krath is the straightforward resolution and a genuine loss. The alternatives, in ascending difficulty:

| Approach | What it looks like | What it requires |
|---|---|---|
| **Redirection** (temporary) | Aim him at something else — a Corrupted threat, a sanctioned bout, a distant hunt | A credible target and Stonefang-fluent framing; buys days |
| **Containment** (medium-term) | Incapacitation in combat (the game's submission-not-death convention) plus tribal restraint — Grakkor's champion-care orders, a warded holding, warriors rotated to limit proximity exposure | Winning the fight *without* killing him, and Grakkor's active cooperation; the Aggression Bleed makes guarding him costly |
| **Severance** (true resolution) | Cutting Krath off from whatever sustains the Corruption in him | **Deliberately not fully authored.** Whether a Corruption-touched individual can be restored is a campaign-level question tied to shrine anchor points and the Mages Guild's incomplete research ([`docs/world/WORLD_BIBLE.md`](../world/WORLD_BIBLE.md)); the AI DM may run a party's genuine attempt using established Corruption-shrine mechanics, but no guaranteed cure exists in canon. A party that tries should learn something true about the Corruption whether or not Krath survives it. |

**If Krath dies:** the Stonefang feel it. Grakkor loses his best warrior and, privately, a problem — the mixture makes him more dangerous to negotiate with, not less. How the party killed him matters: a clean kill in an acknowledged confrontation is read as strength (+Stonefang standing among warriors, complicated standing with Grakkor); an ambush or poisoning of the tribe's champion is read as an act of war regardless of why it was necessary.

---

## Progression by Campaign Stage

Krath's state advances with the campaign. The AI DM should select the stage from world state — how far the Corruption arc has progressed and how long Krath has been left unaddressed — and apply the matching stat column, plus the following:

### Stage I — The Champion (early campaign)

Krath is still recognizable. He speaks in short, coherent sentences; he still sleeps in the camp; Grakkor's orders still slow him even when they no longer stop him. His hunting parties over-kill, but they come home. **Diplomacy is at its widest here** — redirection works for a week at a time, and the single Debt-of-Steel round is closest to the surface. A party that meets Stage I Krath and does nothing should remember him later.

### Stage II — The Unyielding (mid campaign, default)

The state described in [`docs/world/goblin_tribes.md`](../world/goblin_tribes.md): orders ignored twice, invisible enemies cited, trophies unexplained, hounds refusing his tent, proximity effects measurable in other warriors. He speaks rarely and mostly in the present tense — the past has stopped mattering to him. Redirection buys days. Varkk's interest is active (see Tier 2 quests). Containment is viable but expensive.

### Stage III — The Hollow Champion (late campaign, if unaddressed)

The canonical endpoint arriving: Krath no longer distinguishes raid from hunt from challenge. He is at the head of whatever warriors the Aggression Bleed has bound to him — functionally a warband inside the tribe, no longer answering to Grakkor at all. Diplomacy is a single option wide: redirection at something genuinely dangerous enough to occupy him, once. At this stage the encounter is regional: settlements are being hit, the Guild is drafting a contract, and the Stonefang leadership crisis (and the Ashfire opportunism it invites — see Cross-Tribe Corruption Dynamics in [`docs/world/goblin_tribes.md`](../world/goblin_tribes.md)) is in motion whether the party engages or not.

**Stages do not rewind.** A party that saw Stage I and returns later finds Stage II or III. The AI DM should let returning parties see the difference — the sentences shorter, the camp emptier around his tent, one more thing on the trophy wall.

---

## AI DM Guardrails

- **Krath never becomes a generic boss.** Every appearance must carry at least one signal of what he was: a moment of technique, a Stonefang form half-remembered, the one round the Debt of Steel buys.
- **Do not resolve Varkk here.** Varkk's ambitions around Krath belong to the Proving questline ([`docs/quests/goblin_tribe_quests_tier2.md`](../quests/goblin_tribe_quests_tier2.md)) and his longer arc. Krath encounters may *feed* that arc (Varkk observing, Varkk's pledged warriors present) but must not conclude it.
- **The source of Krath's corruption stays unauthored.** What specifically touched him — which shrine, which moment — is not established in canon and must not be improvised as fact. NPCs may speculate; the narrator may not confirm.
- **No cure promises.** See Severance above. The AI DM must never present a guaranteed restoration path.

---

## Document History

| Date | Change |
|---|---|
| 2026-07-31 | Initial document: stage-scaled stat block (Stage I/II/III), Corruption-enhanced combat traits (Ignores Pain, Cannot Disengage, Unyielding Focus, Aggression Bleed), three-phase boss behavior, encounter triggers, combat vs. diplomacy handling, non-lethal resolution ladder, campaign-stage progression, AI DM guardrails |
