# Character Design Guide

> **Document Status:** Canonical design standard as of July 2026.  
> **Authority:** This guide governs how companions are designed in this project. Read it before creating any new companion.  
> **Cross-references:** [`docs/HERO_BIBLE.md`](HERO_BIBLE.md) · [`docs/HERO_TEMPLATE.md`](HERO_TEMPLATE.md) · [`docs/heroes/`](heroes/) · [`docs/GAME_BIBLE.md`](GAME_BIBLE.md)

---

## The Standard

Every companion in this game should feel **handcrafted**.

A companion is never just "a tank" or "a mage" or "a healer." Those are mechanical descriptions. They tell you what a companion does. They do not tell you who a companion *is*.

**Mechanics should grow naturally from the character — not be assigned arbitrarily.**

The player's emotional connection to a companion should matter as much as their combat effectiveness.

---

## The Core Wound System

Every companion is built on a **Core Wound** — one defining emotional experience that shaped who they became.

### What a Core Wound Is

A Core Wound is:
- Specific (not "she was hurt" — what exactly happened, and what did she decide to believe because of it)
- Formative (it happened or accumulated before the story begins)
- Active (it still shapes how they behave today)
- Challengeable (the personal quest can address it)

A Core Wound is **not** a plot event that happens during the game. It is the character's starting condition.

### How the Core Wound Connects to Everything

| Element | Connection to Core Wound |
|---|---|
| **Personality** | Their public face is often armor against the wound; their private face reveals what it cost them |
| **Dialogue** | What they say — and especially what they avoid saying — reflects the wound |
| **Combat role** | Their abilities should express who they are, and who they are comes from the wound |
| **Unique passive** | Should feel like it could only belong to this specific person |
| **Personal quest** | The narrative arc that directly challenges and potentially heals the wound |
| **Relationships** | Other companions either echo, challenge, or unknowingly provoke the wound; relationships evolve — never remain static |

### A Test

If you can swap a companion's Core Wound for a different companion's Core Wound and nothing else needs to change — the wound is not connected deeply enough.

---

## The Five Confirmed Companions & Their Wounds

| Hero | Core Wound | How It Manifests |
|---|---|---|
| **Talos** | Lost faith in authority after years of war | Distrusts institutions; protects people directly; slow to trust anyone with power |
| **Eleanor** | Naive optimism leaves her vulnerable to betrayal | Believes the best of everyone; this will cost her; her growth is learning to love without being blind |
| **Ragash** | Rejected by her own people; found belonging with her hounds | Pride as armor; blunt to the point of seeming cold; her hounds receive the openness she withholds from people |
| **Ronan** | Believes he is a danger to everyone around him | Keeps distance; his curse is a metaphor for the fear of losing control of what you are |
| **Torren** | He once refused to let go of something that could not be saved | His philosophy of restoration is the answer he built from that loss; he believes every person deserves an attempt before giving up on them |

Full Hero Bible entries: [`docs/heroes/`](heroes/)

---

## Design Checklist for New Companions

Before a new companion can be considered designed, every item on this list must be answered:

**Identity**
- [ ] Core Wound defined — specific, formative, active, challengeable
- [ ] Core Belief defined — what truth do they currently hold because of the wound?
- [ ] Gameplay identity flows from personality, not from slot-filling

**Character**
- [ ] Public personality distinct from private personality
- [ ] Greatest fear connected to Core Wound
- [ ] Driving goal specific and personal
- [ ] At least three concrete personal details (habits, preferences, rituals)

**Combat**
- [ ] Unique passive inspired directly by their life story
- [ ] No other companion shares this passive
- [ ] Signature ability is immediately associated with this companion
- [ ] One-sentence gameplay identity written

**Story**
- [ ] Personal quest challenges the Core Wound
- [ ] At least two player-influenced resolutions
- [ ] Relationship to each existing companion defined

**Presentation**
- [ ] Recognizable silhouette — identifiable at a glance
- [ ] One meaningful personal detail visible on the model
- [ ] Voice and dialogue feel distinct from every other companion

---

## Mechanics Growing From Character

The most important design rule in this project:

> **The ability should feel like it could only belong to this person.**

### How to Apply This

1. Write the character fully first — Core Wound, identity, personality, history
2. Ask: "Given who this person is, what do they do in a crisis?"
3. The answer to that question is the passive or signature ability

**Examples from the confirmed cast:**

- **Talos** protects people. His passive (Guardian's Resolve) makes allies near him safer. His signature ability (Battlecry) makes the whole party stronger. His kit is a person who fights so others survive.
- **Ragash** has bonded more deeply with her hounds than with people. Her signature ability (Hound Summon) is not a gameplay mechanic first — it is an expression of where her loyalty goes.
- **Ronan** fears losing control. His transformation into Werewolf Form is powerful and dangerous. The mechanic is the wound.

If you cannot explain why a companion has a specific ability in terms of who they are, the ability is wrong.

---

## The Gameplay Identity Sentence

Every companion must be summarized in one sentence:

> **"[Hero] is the reason the party _______________."**

This sentence becomes the design target. Every ability, passive, and mechanic should serve it.

- Talos: *"Talos is the reason the rest of the party survives."*
- Write the equivalent sentence before designing any other companion.

---

## Visual Identity Standards

Every companion must be **instantly recognizable** without text labels:

- A distinct silhouette readable at combat range
- A recognizable personal item or marking that tells a story
- Colors and equipment that reflect personality, not just class

Personal details visible on the model carry storytelling weight. Talos's bead bracelet is not decoration — it is the answer to "why does he fight?"

---

## Voice Standards

Every companion should sound unique **without a portrait visible**.

- Speaking pace and sentence length vary by character
- Vocabulary and idioms reflect background, not just class
- Humor (or lack of it) is consistent and specific
- What they do *not* say is as important as what they say

---

## Party as Family

The companions should gradually become a family over the course of a campaign.

This is not a design metaphor — it is a design requirement. Relationships must continuously evolve:

- Friendships deepen through shared crisis and revealed character
- Trust grows through demonstrated reliability, not declaration
- Disagreements emerge naturally when companions' values or experiences point in different directions
- Protectiveness develops as companions recognize what each person provides that cannot be replaced

**Eleanor** is the emotional heart of the party — the person who inspires hope and reminds everyone why they are still fighting. Other companions come to understand this and protect it, each in their own way.

**Ragash and Eleanor:** Ragash recognizes Eleanor's value to the group not sentimentally but practically — and becomes as protective of her as Talos is, for her own reasons.

**Ragash and Ronan:** One of the strongest friendships in the party. Built on mutual recognition of what it means to be an outsider, and Ragash's unperformed acceptance of Ronan's condition without judgment.

**Dynamic Campaign Story Arcs** should strengthen different relationships depending on which arc is active. Different campaigns produce different emotional experiences within the party — not only different world events.

> The target: a player who finishes a campaign should feel that these specific companions, in this specific campaign, became something to each other that could not have been scripted. The relationships should feel earned.

See [`docs/systems/dynamic_story_arcs.md`](systems/dynamic_story_arcs.md) for campaign-specific companion interactions.

See [`docs/systems/journey_system.md`](systems/journey_system.md) for how companion relationships develop during travel — the interaction scheduler, camp event types, relationship growth mechanics, Corruption resistance through bonds, and camp evolution from strangers to family.

---

## Document History

| Date | Change |
|---|---|
| July 2026 | Created — established Core Wound system, companion design checklist, mechanic-from-character principle |
