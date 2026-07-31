# Journey System — Companion Relationships & Camp Evolution

> **Canon Status:** [CONFIRMED — established July 2026]  
> **Authority:** This document defines the canonical framework for how travel, camp, companion relationships, and dialogue scheduling work. All future companion content, camp events, relationship mechanics, and travel narrative design must align with these principles.  
> **Cross-references:** [`docs/CAMPAIGN_DESIGN.md`](../CAMPAIGN_DESIGN.md) · [`docs/systems/ai_director.md`](ai_director.md) · [`docs/systems/dynamic_story_arcs.md`](dynamic_story_arcs.md) · [`docs/CHARACTER_DESIGN_GUIDE.md`](../CHARACTER_DESIGN_GUIDE.md) · [`docs/heroes/`](../heroes/)

---

## Journey Conversations — Canonical Design

> **Design update — 2026-07-31:** The primary storytelling mechanism during travel is **Journey Conversations**, not a traditional camp system. There is no mandatory camp hub similar to Baldur's Gate 3 or Solasta. Companions converse while the player continues moving — leaving towns, entering new regions, traveling between destinations, completing quests. The camp philosophy below documents the rest and recovery layer that coexists with Journey Conversations; it is not the primary relationship-building mechanism.

Journey Conversations occur naturally during:
- Travel between destinations
- Exploration of wilderness and ruins
- Departing towns and settlements
- Arriving in new regions
- Quest completion moments

**Travel itself is the primary storytelling space.** The scheduler, priority tiers, relationship network, and companion interventions documented below apply to Journey Conversations throughout the journey — not only at camp stops.

---

## Design Philosophy

Project Dungeon Keeper is not a game where companions simply accompany the player.

It is a game where strangers gradually become a family.

The player's journey is not only about saving the world. It is about helping five specific people grow together — and through that growth, becoming capable of facing a darkness that none of them could face alone.

The Journey System is how this happens mechanically. It exists to ensure that the transformation from strangers to family feels **earned**, not declared; **gradual**, not sudden; and **specific**, not generic.

> *"The greatest battle is not against darkness… but against forgetting who you are."*

The Journey System reinforces this theme at every level: the Corruption isolates; companionship preserves. As the party's bonds deepen, those bonds become the thing the Corruption cannot take.

---

## The Journey System — Core Concept

**Replace the traditional "hub between missions" philosophy.**

In most games, the hub is where relationships develop — a home base the player returns to between adventures. In Project Dungeon Keeper, the journey itself is what builds relationships.

**Travel is no longer downtime. Travel is one of the primary methods of storytelling.**

Companion development happens during movement — on the road, at camp, in the moments between destinations. The player should gradually feel that weeks and months are passing as the companions travel together, and should be able to look back at where the relationships started and recognize the distance they have traveled.

---

## Overworld Travel

The world uses the Solasta-inspired overworld travel system. Travel between destinations occurs in segments. Each segment may include:

- Travel through a region (encounter opportunities)
- Camp establishment (rest, character management, crafting, companion interactions)
- Weather and world events
- Ambient storytelling moments

**Travel structure per journey:**

```
Origin → Travel Segment → Camp → Travel → [Weather/World Event] → Camp → Travel → Destination
```

Each journey between two destinations contains multiple camps. Not every camp is eventful. Not every eventful camp is heavy. The pacing of what happens between destinations is itself a narrative tool.

---

## Camp Philosophy

Camp serves two parallel purposes that must both be present:

### Mechanical Purpose
- Rest and recovery
- Character and equipment management
- Crafting (Torren's domain, but available to all)
- Consumable restocking

### Narrative Purpose
- Conversations and character development
- Companion bonding and relationship evolution
- Reflection on recent events
- Humor, disagreement, and resolution
- Personal growth moments

**Camp is emotional safety.**

Outside camp, the Corruption whispers. Inside camp, companions remind one another who they truly are. This distinction should be felt in the game's tone and visual design — camp should read as a protected space, not because it is magically shielded, but because the people in it choose to keep it that way.

> Camp is not where the party rests from the adventure. Camp is where the party remembers why the adventure is worth it.

---

## Companion Interactions

### Core Rule: No Interaction Is Random

Every companion interaction at camp has **prerequisites**. The prerequisite system ensures that every conversation feels earned — that it emerges from things that have actually happened in this specific campaign.

**Possible prerequisites include:**

| Category | Examples |
|---|---|
| **Story progression** | A specific act or quest milestone reached |
| **Companion quests** | A related personal quest beat completed |
| **Previous conversations** | A specific earlier interaction has occurred |
| **Relationship levels** | A minimum bond level between two specific companions |
| **Player choices** | A decision with emotional weight was made |
| **Combat outcomes** | A companion was downed, or performed a specific action |
| **Recent injuries** | A companion is recovering from something |
| **Lore discovery** | The party learned something significant |
| **Region completion** | A specific area was explored or resolved |
| **Time elapsed** | Sufficient time has passed since the last conversation on this thread |

This system means two things: players who engage deeply with the world will unlock interactions that other players never see, and players will never feel that conversations are appearing at arbitrary moments disconnected from what just happened.

---

## Interaction Scheduling

### The Problem Without a Scheduler

Multiple interactions may become available at the same time — after a major quest, after a dynamic story arc beat, after a relationship threshold is crossed. Without scheduling, these stack up and deliver multiple heavy conversations at the same camp, which undermines pacing and emotional impact.

### The Solution: Invisible Interaction Scheduler

The Journey System maintains an invisible scheduler that distributes available interactions across future camps. The scheduler determines:

1. Which interaction is most appropriate for **this specific camp** (given what just happened, the emotional weight already carried, what other companions need space for)
2. How to **distribute interactions across the journey** so that heavy and light scenes alternate naturally
3. Which interactions remain **queued for later** if this camp is not the right moment

**Example distribution — journey from The Capital to The Frontier:**

```
Capital (depart)
  ↓
Camp 1 — Torren speaks with Ronan [queued; prerequisites met after Capital quest]
  ↓
Camp 2 — Quiet camp. Ambient only. [emotional breathing room after heavy scene]
  ↓
Camp 3 — Eleanor and Talos discuss recent events [queued]
  ↓
Weather event (storm during travel)
  ↓
Camp 4 — Ragash and Torren [relationship scene unlocked by storm event]
  ↓
Frontier (arrive)
```

This creates natural pacing — the journey feels lived-in rather than event-saturated.

### Scheduler Metadata

Every interaction in the system carries metadata the scheduler reads:

| Field | Description |
|---|---|
| **Prerequisites** | What must have happened for this interaction to be available |
| **Priority** | Tier determining urgency (see below) |
| **Cooldown** | Minimum camps before this companion can be the focus again |
| **Emotional weight** | How heavy this scene is; used to alternate with lighter content |
| **Companion participation** | Which companions are involved |
| **Story dependencies** | Whether this interaction references or unlocks other content |

Unused interactions do not expire. They remain queued and become available in future journeys when circumstances are appropriate.

---

## Conversation Priority Tiers

When multiple interactions are available, the scheduler selects based on priority:

| Priority | Category | Examples |
|---|---|---|
| **Highest** | Main story events | Major revelations; campaign-defining moments |
| **Very High** | Companion quest progression | Personal arc beats; romance progression |
| **High** | Significant emotional moments | Response to trauma; major world event reactions |
| **Medium** | Character development | Values conversations; growing understanding between companions |
| **Low** | Casual conversation; humor | Campfire stories; friendly teasing; quiet reflection |
| **Ambient** | Background life moments | Non-interactive texture; atmosphere without dialogue |

**The scheduler should naturally alternate between heavy and light scenes** — a High-priority emotional scene should typically be followed by a Low or Ambient camp before another High-priority scene runs. This prevents the campaign from feeling relentlessly intense, and makes genuinely heavy moments land harder because they have been given space.

---

## Companion Cooldowns

After a companion has been the focus of an emotionally significant interaction, that companion receives an invisible **cooldown** before they can be the focus again.

**Purpose:** Naturally distributes narrative attention across the full cast. No single companion should dominate camp conversations unless the story specifically requires it (during that companion's personal arc, for example).

**Effect:** The scheduler deprioritizes recently-focused companions when selecting which queued interaction to run at the next camp. This prevents players from feeling that they are watching one companion's story while others stand in the background doing nothing.

---

## Ambient Camp Events

Not every camp requires dialogue. Many camps should simply reinforce that the companions are becoming a family through **atmosphere rather than conversation**.

**Ambient camp moments (non-interactive texture):**

| Companion | Ambient activity |
|---|---|
| **Torren** | Repairing damaged armor and weapons before anyone asks; working by firelight late into the night |
| **Talos** | Sharpening his blade with practiced economy; sitting apart but watching the camp |
| **Ronan** | Quietly disappearing into the woods before returning without explanation |
| **Eleanor** | Studying ancient texts by firelight; occasionally asking a question aloud that nobody expected |
| **Ragash** | Preparing dinner or tending to her hounds; occupied and at ease |

**Group ambient moments:**
- Companions laugh together about something that happened during travel
- Someone tells a story the player half-hears from across camp
- A quiet evening passes without incident; the fire burns low
- Companions share a meal in comfortable silence

These moments build the sense that time is passing and relationships are deepening, without demanding the player's full attention. A campaign that contains too many quiet ambient camps feels slow; a campaign that contains none feels like a series of events without a life between them.

---

## Types of Camp Events

The scheduler draws from six event categories:

### 1. Companion Conversation
Two or more companions — with or without the player as active participant — have a scene that develops their relationship or reveals character. The most common high-weight camp event type.

### 2. Group Conversation
The entire party participates. Used for major shared reactions, world events the whole group must respond to, or rare moments of collective levity. Should occur less frequently than individual companion conversations — group scenes carry more weight when they are not constant.

### 3. Player Activity
The player chooses how to spend the evening. This is an active choice with mechanical and relational consequences:

| Activity | Effect |
|---|---|
| Train with Talos | Relationship growth; possible combat bonus |
| Study with Eleanor | Relationship growth; possible lore unlock |
| Hunt with Ronan | Relationship growth; possible regional knowledge |
| Help Torren forge equipment | Relationship growth; possible item improvement |
| Explore nearby ruins with Ragash | Relationship growth; possible discovery |
| Cook for the party | Minor relationship growth with all companions |
| Play games around the fire | Ambient relationship growth; levity |

Player activities are not mandatory. Players who decline an activity miss a relationship moment; this is intentional. The relationship system should reward consistent engagement without punishing absence.

### 4. Story Event
A narrative-heavy camp event tied to main story or Dynamic Story Arc progression. Typically the highest-priority item in the scheduler queue when available. These events may introduce new information, shift world state, or change companion dynamics in lasting ways.

### 5. World Event
Something arrives at or near camp from the outside world:

- Travelers seeking rest or assistance
- Merchants with unusual inventory
- Weather phenomena that force camp decisions
- Ruins visible from camp that can be investigated
- Wildlife (including Corruption-affected wildlife)
- Corruption manifestations at the edge of the firelight
- Unexpected visitors with their own agendas

World events may cascade into Story Events or Companion Conversations depending on what occurs.

### 6. Quiet Camp
No major interaction occurs. The camp is simply a place to rest. Ambient character texture may be present. **Quiet camps are important for pacing** — they give players space to process what has happened, and they make the eventful camps feel meaningful by contrast.

---

## Relationship System

### Full Network, Not Just Player ↔ Companion

Relationships in this game are not only between the player and each companion. Every companion pair has an independent relationship that evolves based on what they have been through together.

**The complete relationship network (10 pairs plus player-companion relationships):**

| Pair | Current Status |
|---|---|
| Talos ↔ Eleanor | Documented: protective recognition; she is goodness worth preserving |
| Talos ↔ Ragash | To be developed |
| Talos ↔ Ronan | Documented: cautious → earned respect as Ronan demonstrates control |
| Talos ↔ Torren | Documented: mutual respect through discipline and craft |
| Eleanor ↔ Ragash | Documented: Ragash becomes fiercely protective of Eleanor |
| Eleanor ↔ Ronan | Documented: can develop into romance; dynamic inverts during The Fractured Circle |
| Eleanor ↔ Torren | Documented: magic/restoration comparison; productive disagreements |
| Ragash ↔ Ronan | Documented: one of the strongest friendships; unconditional acceptance |
| Ragash ↔ Torren | Documented: imperfect beauty vs patience through craft |
| Ronan ↔ Torren | Documented: "Broken steel can be reforged" |

Every pair's relationship evolves independently. Some companions will naturally become closer to each other than others — not every relationship reaches the same depth, and that is realistic and correct. The player's choices influence which relationships are given space to develop.

### Relationship Growth

Relationships improve through accumulated shared experience:

- Travel together (accumulated over time)
- Shared combat (surviving together builds something)
- Camp interactions (direct relationship investment)
- Personal quests (witnessing each other's vulnerabilities)
- Helping one another in moments of need
- Shared victories (especially unlikely ones)
- Resolving genuine disagreements (not avoiding them)
- Acts of sacrifice for each other
- Humor shared (trust enough to be genuinely funny)
- Demonstrated trust (relying on someone and being right to)
- Time elapsed together (the accumulation of ordinary moments)

**Not every relationship grows equally.** Some companions are naturally more compatible than others. Some relationships will remain cordial but not deep. This variety is intentional — it reflects how real relationships work, and it means that when two companions do develop a deep bond, it feels specific rather than universal.

---

## Corruption Resistance Through Relationships

**This is one of the Journey System's most significant mechanical and thematic pillars.**

The Corruption isolates people. It amplifies existing fears, doubts, and drives for control — turning individuals inward and cutting them off from genuine connection. The Corruption's strongest foothold in a person is the belief that they face what they face alone.

Companionship directly counters this.

As trust deepens between companions:
- Companions become **more resistant to the Corruption's influence** — not immune, but slower to fall
- The Corruption's amplification effect finds less purchase in a mind that knows it is not alone
- **Emotional resilience** is the mechanical expression of this: relationship depth extends the time companions can resist Corruption-influenced choices before something breaks

**This is never framed as immunity.** The Corruption is not defeated by being liked. The strongest bonds provide the longest runway before a companion — or the player — starts making choices that reflect the Corruption rather than themselves. What they do with that runway is still a choice.

> The stronger the bonds, the longer companions can resist. The longer they resist, the more choices remain their own.

---

## Companion Intervention System

During critical Corruption moments, companions with strong enough relationships may **intervene** — stepping into a moment that might otherwise go a different way.

**Examples:**
- Torren pulls Ronan back from losing himself during a near-transformation
- Eleanor reminds Talos why he fights when he is about to make the choice his past self would recognize as wrong
- Ragash comforts Eleanor after a betrayal that would otherwise close her off
- Ronan, understanding the fear of losing yourself, reaches Eleanor during The Fractured Circle in ways no other companion can

**What interventions are NOT:**
- Magical powers or combat abilities
- Guaranteed outcomes that remove player agency
- Dramatic speeches that explain the theme

**What interventions ARE:**
- Narrative moments where a specific relationship, at a specific depth, changes what is possible in a specific scene
- Supported entirely by the relationship progression that preceded them — they are not available if the relationship is not there
- Expressions of trust rather than declarations of it

An intervention that has not been earned by the relationship feels like a plot convenience. An intervention that has been earned feels like the culmination of everything that came before it.

---

## Dynamic Dialogue Memory

Every meaningful interaction becomes a **remembered event** — a specific fact about this campaign that future dialogue can reference.

**Examples of remembered events:**
- "Torren encouraged Ronan after the Wolf Den"
- "Talos apologized to Eleanor after what happened in the Iron Peaks"
- "Ragash taught Torren wilderness survival during the Frontier crossing"
- "Eleanor helped Talos understand the First Age history of the ruin they explored"

Future dialogue naturally references these shared memories. Companions speak to each other as people who have been through specific things together — not as characters running generic relationship dialogue.

**Purpose:** This creates **continuity throughout the adventure**. A player should be able to hear a throwaway reference in a late-game camp conversation and remember exactly when that thing happened. The party's history accumulates.

**Design rule:** Do not write companion dialogue that could be said by any companion at any point in the campaign. Write dialogue that requires something to have already happened, and that references what that was.

---

## Camp Evolution

Camp should visually and emotionally evolve across the campaign. The change should be observable — a player who looks at an early-game camp and a late-game camp should be able to see the difference.

### Early Game — Strangers

- Companions maintain distance; separate tents, separate spaces
- Minimal unsolicited conversation
- Formal or guarded interactions when they do occur
- Everyone is present, but not yet together
- The fire feels smaller

### Mid Game — Building Trust

- Shared meals; companions eating together without it being an event
- Friendly teasing that would not have been possible earlier
- Training together; teaching each other things
- Shared responsibilities emerging naturally (Torren handles repairs; Ragash handles hunting)
- Trust visible in the things companions do without being asked

### Late Game — Family

- Camp feels like home
- Companions freely interact with each other without player involvement
- They joke, argue, comfort, and support each other as a matter of course
- The player realizes: they are no longer a group of adventurers who share a fire
- They have become something that does not need a word for it, but which every player will recognize

**The design target:** A player who reaches the late game should be able to sit at camp and watch companions interact with each other — independent of the player's presence — and feel that they are watching something that developed. Not something that was always there.

---

## Gameplay Philosophy — What Relationships Unlock

Relationship progression should not primarily reward **raw statistics**.

Attack bonuses and critical chance are not the language of connection. They are the language of optimization. This game is not about optimization.

**Relationship depth should unlock:**

| Reward Type | Description |
|---|---|
| **Corruption resistance** | Deeper bonds = longer runway before Corruption finds purchase |
| **Companion interventions** | High-relationship companions can change outcomes during critical moments |
| **Unique conversations** | Interactions only available at certain relationship depths |
| **Cooperative combat abilities** | Abilities that require specific companions to have built specific trust (not solo abilities; genuinely two-person) |
| **Companion quest progression** | Some personal quest beats require relationship thresholds to unlock |
| **Alternative story outcomes** | Some endings or resolutions require specific companion relationships to be at the required depth |
| **New camp activities** | Deeper relationships open additional Player Activity options |
| **Emotional payoffs** | The most important reward: the moment a player realizes what these specific companions have become to each other |

**Mechanical bonuses should support the narrative rather than replace it.** A small stat improvement from a relationship is acceptable as a secondary benefit. It should never be why a player invests in a relationship.

---

## Core Philosophy

The Journey System exists because the world is not saved by a lone hero.

It is saved by people who refuse to let one another face darkness alone.

Every road traveled. Every campfire. Every shared hardship. Every laugh. Every disagreement resolved. Every memory created.

These things make the party stronger — not because they accumulate experience, but because they build the bonds that allow five very different people to resist, together, what none of them could resist alone.

The goal is for players to finish Project Dungeon Keeper feeling that they did not merely command a party of heroes. They watched five strangers gradually become a family. And that transformation was as important to saving the world as any battle they fought.

---

## Connection to Other Systems

| System | Connection |
|---|---|
| **AI Director** | The interaction scheduler is a subsystem the AI Director coordinates; the DM Brain's story pressure tracking should inform which camp event tiers are appropriate at any point |
| **Dynamic Story Arcs** | Arcs define which companion relationships are spotlighted and which interactions become available; the scheduler must be arc-aware |
| **Reputation System** | Faction reputation can serve as a prerequisite for certain camp interactions |
| **Corruption System** | Relationship depth is the primary mechanical counter to Corruption's escalating influence |
| **Personal Quests** | Major personal quest beats generate high-priority interactions; some beats are only available after relationship prerequisites are met |

---

## Document History

| Date | Change |
|---|---|
| July 2026 | Created — Journey System, Camp Philosophy, Interaction Scheduling, Conversation Queue, Relationship Network, Corruption Resistance, Companion Interventions, Dialogue Memory, Camp Evolution, Gameplay Rewards Philosophy |
| 2026-07-31 | Design update — Journey Conversations established as the canonical primary storytelling mechanism; camp system reframed as the rest/recovery layer; conversations now occur during travel, not only at camp stops; companion approval system (principle-based, not morality-based) documented |
