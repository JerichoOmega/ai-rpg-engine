# Dynamic Campaign Story Arcs

> **Canon Status:** CONFIRMED — established July 2026
> **Authority:** This document defines what Dynamic Story Arcs are, how the AI Dungeon Master selects and executes them, and how they interact with the fixed main narrative. All future campaign arc design must align with these principles.
> **Cross-references:** [`docs/CAMPAIGN_DESIGN.md`](../CAMPAIGN_DESIGN.md) · [`docs/systems/ai_director.md`](ai_director.md) · [`docs/GAME_BIBLE.md`](../GAME_BIBLE.md) · [`docs/heroes/ELEANOR.md`](../heroes/ELEANOR.md)

---

## What Dynamic Story Arcs Are

Project Dungeon Keeper features **one handcrafted main story** shared across every campaign.

Each campaign also features one or more **Dynamic Story Arcs** — large-scale world events that are unique to that particular playthrough.

The AI Dungeon Master selects these arcs during campaign generation. They are not procedurally generated stories — they are **authored scenarios** that the AI activates and orchestrates based on campaign parameters.

---

## What Arcs Influence

A Dynamic Story Arc shapes the entire campaign through which it runs:

| Element | How arcs shape it |
|---|---|
| **Regions** | Which areas fall into crisis; what changes in regional tone |
| **Major factions** | Which factions are affected; how their internal politics shift |
| **Companion stories** | Which companions have personal stakes in the arc's events |
| **Questlines** | Campaign-exclusive quests that only exist when this arc is active |
| **Enemy types** | Campaign-exclusive enemies introduced by the arc |
| **World events** | Unique events that occur as the arc develops |
| **Politics** | Inter-faction relationships modified by arc events |
| **Exploration** | Sites, dungeons, or locations that only appear during this arc |

The main story **never changes**. The world's response to the Corruption does.

---

## Campaign Philosophy

The goal is **not** procedural storytelling.

The goal is **handcrafted storytelling with dynamic world variation**.

Players should finish different campaigns with dramatically different experiences while still sharing the same central narrative. Each campaign should feel like another telling of the same legend.

> One player may remember a campaign where the Mages Guild slowly fell into corruption and magic-using cultists became one of the game's defining enemies. Another player may never encounter this storyline because their campaign focused on an entirely different regional crisis.

These differences should encourage replayability while preserving the handcrafted central narrative.

---

## AI Dungeon Master Arc Selection

The AI Dungeon Master selects one or more Dynamic Story Arcs during campaign generation.

Selected arcs should:

- Influence world events throughout the campaign
- Affect companion storylines where appropriate companions are present
- Introduce unique encounters tied to the arc's events
- Create campaign-exclusive enemies
- Modify faction relationships in ways that persist
- Shape questlines and available content

Not every campaign should contain every arc. Campaign identity emerges from the arcs selected. The arcs in play during a campaign are a major part of what makes that campaign distinct from others.

---

## Dynamic Enemy Design

Each Dynamic Story Arc introduces **enemies unique to that campaign**.

These enemy types exist **only** while the arc is active. They should not automatically appear in other campaigns.

This makes each campaign feel mechanically and narratively distinct — the enemies a player faces in one run may simply not exist in another.

> Full design principle: campaign-exclusive enemies are an authorial tool, not a resource pool. When a player faces a Corrupted Battle Mage, they are in a campaign shaped by the Fractured Circle. That enemy is part of the story they are in.

---

## Confirmed Arcs

### The Fractured Circle

**Summary:** The Corruption quietly spreads throughout portions of the Mages Guild. Rather than beginning with obvious villains, respected scholars and researchers slowly become obsessed with understanding the Corruption. Some begin secretly communicating with cultists. Others believe the ancient god's power can be studied or controlled. Eventually portions of the Mages Guild become intertwined with one of the world's cults.

**Primary affected faction:** The Mages Guild

**Corruption type:** Arcane

---

#### Campaign-Exclusive Enemies

These enemy types exist only during The Fractured Circle:

| Enemy Type | Description |
|---|---|
| **Magic-using cultists** | Practitioners who have crossed from scholarly curiosity into active service |
| **Corrupted battle mages** | Former Guild combat specialists whose training is now turned against civilization |
| **Ritualists** | Scholars whose research has become ritual; dangerous in controlled environments |
| **Arcane priests** | Blending religious cult practice with forbidden magical knowledge |
| **Corrupted scholars** | Non-combat figures who have become sources of dangerous information and dangerous acts |
| **Arcane summoners** | Guild members who have discovered summoning applications of the Corruption's energy |

#### Campaign-Exclusive Locations

| Location | Description |
|---|---|
| **Secret magical laboratories** | Hidden research sites where forbidden Corruption study continues |
| **Corrupted magical archives** | Guild repositories where documents have been altered or replaced with cult material |
| **Forbidden research sites** | Locations outside Guild infrastructure where more extreme work is conducted |

---

#### Eleanor's Personal Story

This campaign arc becomes **deeply personal for Eleanor**.

Many of the corrupted individuals are people she knew before the campaign began:

- Former teachers
- Fellow students
- Friends
- Mentors
- Researchers she admired

Her story in this arc is one of **heartbreak rather than hatred**. She must confront the realization that good intentions do not protect people from the Corruption — that being scholarly, curious, and well-meaning is not a defense against it.

Eleanor's personal arc during the Fractured Circle is one of the clearest expressions of the game's core Corruption principle: it amplifies existing flaws, it does not manufacture evil from nothing.

See [`docs/heroes/ELEANOR.md`](../heroes/ELEANOR.md)

---

#### Companion Dynamics During This Arc

**Talos** views the situation pragmatically at first. Those serving the cult must be stopped. His military background makes him prioritize protecting innocent lives over relitigating the moral complexity of how individuals arrived at their current position. If the party pushes him on this, his views are more nuanced than his initial assessment — but he leads with function.

**Ragash** understands Eleanor's emotional conflict from personal experience. Having experienced rejection by her own people, she recognizes what it looks like to watch someone you respected lose themselves. She becomes Eleanor's primary emotional support throughout this arc. This is not a dramatic shift in Ragash's character — it is a natural expression of who she already is.

**Ronan** brings the most complicated perspective: because he constantly fears losing himself to his werewolf curse, he understands that corruption is not always a conscious choice. He is positioned to remind Eleanor that some victims may still be worth saving — that not every corrupted person has fully crossed the line. This dynamic directly engages Ronan's core wound.

Steven's involvement depends on when he is recruited and what the party has uncovered about his past. He says nothing, but he watches the corrupted scholars with unusual attention.

See [`docs/heroes/`](../heroes/)

---

---

## Campaign-Specific Companion Interactions

Dynamic Story Arcs unlock **unique companion interactions** that only occur during that campaign — conversations, camp scenes, and relationship moments that reinforce the emotional impact of the arc's central conflict.

These interactions are not available in campaigns where the arc is not active. They are part of what makes each campaign emotionally distinct, not just narratively distinct.

---

### The Fractured Circle — Eleanor and Ronan

**Condition:** Both Eleanor and Ronan must be active companions during this campaign.

**What becomes available:** Additional dialogue, camp conversations, and story scenes that would not exist in other campaign runs.

---

**The dynamic:**

Throughout most of the game, Eleanor is positioned to help Ronan. She sees him clearly — the guilt, the isolation — and does not find any of it disqualifying. She is one of the primary reasons he does not collapse inward.

The Fractured Circle **inverts this dynamic**.

As Eleanor watches respected members of the Mages Guild — former teachers, friends, mentors, researchers she admired — fall to the Corruption, Ronan recognizes what she is going through. Because he lives with the daily fear of losing himself to his curse, he understands this experience in a way no other companion does.

Ronan becomes one of Eleanor's strongest emotional supports during this arc. He:

- Encourages her not to lose hope
- Reminds her that those who have fallen were once good people — and that this matters, even when it does not change what must be done
- Helps her carry the emotional burden of making impossible decisions about people she cares about

**What this demonstrates:** Ronan's own growth. He is no longer only someone who needs saving. He has become someone capable of helping others — and doing so in the specific way that only his experience enables. The Fractured Circle is one of the clearest moments where his arc pays off in a way that serves another character.

This interaction should feel like a **natural consequence of who both characters are**, not a scripted reversal. Eleanor helped Ronan because she is the kind of person who does that. Ronan helps Eleanor because he has grown, and because he understands something about her situation that she cannot fully explain to anyone else.

See [`docs/heroes/ELEANOR.md`](../heroes/ELEANOR.md) · [`docs/heroes/RONAN.md`](../heroes/RONAN.md)

---

## Companion Growth Philosophy

Companion relationships **continue evolving throughout the game**. They are never static.

Major campaign events should:

- Strengthen friendships through shared crisis
- Surface disagreements that would not arise under normal conditions
- Reveal new perspectives that companions could not access without specific experiences
- Unlock campaign-exclusive dialogue, scenes, and relationship moments

Different Dynamic Story Arcs naturally highlight different relationships between companions. The Fractured Circle centers Eleanor and Ronan. Future arcs should identify, at design time, which companion relationships they are designed to illuminate — and ensure those relationships have something to say about the arc's central conflict.

**The design goal:** Replaying the game provides not only different world events, but different emotional experiences within the party. Two players who both completed a campaign with Eleanor and Ronan may have experienced completely different moments between them, depending on which arc was active.

---

## Design Notes for Future Arcs

Each future Dynamic Story Arc should define:

1. **Summary** — what is happening in the world during this arc
2. **Primary affected faction** — which major faction or institution is most shaped by the arc
3. **Corruption type** — which of the four Corruption expressions (Political, Natural, Religious, Arcane) drives the arc
4. **Campaign-exclusive enemies** — what new enemy types this arc introduces
5. **Campaign-exclusive locations** — what sites only exist during this arc
6. **Companion stakes** — which companions have personal connection to this arc's events
7. **Companion dynamics** — how all party companions respond to the arc's events
8. **Campaign-specific companion interactions** — which companion relationships the arc is designed to illuminate; what interactions become available and under what conditions

Arcs should be designed to **intersect with the companion roster** — they are most powerful when they put a companion's core wound in direct contact with the arc's events, and when they allow a companion's growth to manifest in service of another companion.

---

## Document History

| Date | Change |
|---|---|
| July 2026 | Created — Dynamic Story Arc framework established; The Fractured Circle documented as the first confirmed arc |
