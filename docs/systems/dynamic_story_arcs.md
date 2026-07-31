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

**Torren**, if present, observes The Fractured Circle's corrupted scholars with the particular grief of a craftsman watching something that required years to build become something that destroys. He does not engage with the theological or institutional dimensions of the crisis. He engages with what is being lost — the discipline, the precision, the accumulated knowledge that corrupted mages are discarding or weaponizing. He is reliably useful in the aftermath of encounters, repairing what can be repaired, and he does not comment on what cannot.

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

### The Broken Crown

**Summary:** The Corruption spreads through the institutions of power that govern the continent — not through obvious villains, but through the slow amplification of ambition, fear, and desire for control that already existed inside them. Military commanders make decisions that sacrifice civilians to protect strategic position. Officials cover up crises to avoid accountability. Governors suspend rights in the name of security. None of them believe they are doing wrong. The Corruption does not need them to. Talos has spent years believing that all governments eventually rot — and in this arc, he watches that belief come true at scale, in the specific institutions he once served.

**Primary affected faction:** The Capital's military and governing apparatus

**Corruption type:** Political

---

#### Campaign-Exclusive Enemies

These enemy types exist only during The Broken Crown:

| Enemy Type | Description |
|---|---|
| **Corrupted enforcers** | Military personnel carrying out orders they would once have refused; trained, disciplined, and wrong |
| **Political inquisitors** | Officials who have weaponized institutional authority to silence threats, real or perceived |
| **Loyalist officers** | Former commanders whose protective instincts have curdled into authoritarianism; they believe they are doing what is necessary |
| **Informant networks** | Civilian collaborators — not monsters, but frightened people who have chosen security over conscience |
| **Institutional cultists** | Individuals inside the power structure who have crossed from complicity into active service of the Corruption's agenda |

#### Campaign-Exclusive Locations

| Location | Description |
|---|---|
| **Sealed government archives** | Records that were officially destroyed; what remains reveals decisions that powerful people need to remain hidden |
| **Military detention sites** | Facilities that exist outside the official command structure, where people are held without process |
| **Abandoned command posts** | Forward positions that were quietly withdrawn from, leaving the civilians they were meant to protect |
| **Compromised garrison towns** | Settlements where the institutions meant to protect have become the source of fear |

---

#### Talos's Personal Story

This campaign arc forces a confrontation Talos has spent years avoiding.

He does not dislike institutions because he never understood them. He distrusts them because he understood them too well — he walked their halls, followed their orders, and watched what those orders became. His core wound is the accumulated experience of seeing good soldiers die for politics, of following commands he later regretted, of realizing that the people at the top of a command structure are not the people at the bottom of it.

The Broken Crown puts that wound directly against the present. These are not abstract institutions — they are specific commands, specific officials, specific operations that may involve people Talos knew, served alongside, or once respected.

His arc in The Broken Crown is not radicalization. He already drew his conclusion long ago. It is something harder: being forced to act against a system he once belonged to, while knowing that the ordinary soldiers carrying out those orders are not the source of the rot. He cannot hate them. He cannot let them continue. He has to find a way to do what must be done without losing the distinction between the institution and the people caught inside it.

See [`docs/heroes/TALOS.md`](../heroes/TALOS.md)

---

#### Companion Dynamics During This Arc

**Eleanor** brings a genuine disagreement with Talos that this arc makes unavoidable. She believes institutions can be reformed — that the rot is not inherent but situational, and that abandoning them entirely abandons the people who depend on them. Talos does not share this belief, and in The Broken Crown, he has evidence. This is not a fight between cynicism and naïveté — both positions have real weight, and the arc does not adjudicate between them. It forces the party to keep working together despite the disagreement.

**Ragash** has no particular attachment to any government and will say so clearly. She is not ideologically engaged with the arc's political content — she is practically engaged with its consequences. When civilians are in danger, she responds to that. When the party needs someone who will not hesitate because of former loyalties, she is it.

**Ronan** understands what it is to watch something you cannot stop happen inside a system you are part of. He does not have strong opinions about the Capital specifically, but he understands complicity — the fear of acting that enables the thing you fear to continue. He is not positioned to lecture Talos; he is positioned to quietly be present in a way that Talos recognizes as genuine.

**Torren**, if present, has little investment in the political content of The Broken Crown. What he responds to is the damage — what institutional corruption does to the actual infrastructure of people's lives, the structures and supply lines and maintainable systems that a functioning government is supposed to keep running. He is not positioned to adjudicate the Talos/Eleanor disagreement about reform versus abandonment. He is already thinking about what comes next.

See [`docs/heroes/`](../heroes/)

---

---

## Campaign-Specific Companion Interactions — The Broken Crown

### The Broken Crown — Talos and Eleanor

**Condition:** Both Talos and Eleanor must be active companions during this campaign.

**What becomes available:** Dialogue, camp scenes, and relationship moments built around a genuine ideological disagreement that neither character abandons.

---

**The dynamic:**

Talos believes institutions cannot be saved — they can only be survived, resisted, or outlasted. Eleanor believes that institutions, even broken ones, can be reformed by people with enough courage and enough patience. Neither of them is playing a role. Both positions are real.

The Broken Crown puts this disagreement in direct contact with evidence. Talos watches the rot spread exactly as he always believed it would. Eleanor watches the same events and finds examples — small ones, hard ones — of people inside the system trying to hold a line. They are both right about different things, and the arc does not resolve this.

What the arc produces instead:

- Scenes where they argue, actually argue, without the argument being resolved for the player
- A moment where Eleanor's belief enables something Talos's would have foreclosed — and Talos has to acknowledge this
- A moment where Talos's lack of illusions prevents a mistake that Eleanor's hope would have made — and Eleanor has to acknowledge this
- By the end of the arc: not agreement, but a harder kind of respect; the recognition that the other person's position is not weakness or blindness, but a different way of bearing the same weight

**What this demonstrates:** Talos's capacity for intellectual honesty under pressure. He does not modify his conclusion, but he does not dismiss what does not fit it. Eleanor's growth is visible in the same measure — she does not lose her belief in reform, but she holds it with more precision. The Broken Crown is the arc where their relationship becomes something more durable than warmth.

See [`docs/heroes/TALOS.md`](../heroes/TALOS.md) · [`docs/heroes/ELEANOR.md`](../heroes/ELEANOR.md)

---

---

### The Hungry Dark

**Summary:** The Great Forest is failing. The Corruption spreads from something beneath its roots — not a single source, but a pattern of contamination moving outward through the ecosystem. Corrupted wildlife presses into goblin tribal territory, then into the Frontier settlements, then beyond. The goblin tribes face a choice between fighting something they cannot see clearly, retreating from ancestral land, or attempting to understand what is happening before it is too late. The forest's own logic is turning against everything living in it. Ragash's hounds can smell something wrong before any of this is visible — and as the arc develops, that sensitivity becomes central to what the party can and cannot know.

**Primary affected faction:** The Great Forest ecosystem and the goblin tribes whose existence is tied to it

**Corruption type:** Natural

---

#### Campaign-Exclusive Enemies

These enemy types exist only during The Hungry Dark:

| Enemy Type | Description |
|---|---|
| **Corrupted predators** | Apex animals whose territorial and hunting behavior has been amplified into something organized and relentless |
| **Hollow-eyed scavengers** | Animals that once cleaned up after the forest; now spreading contamination through what they consume |
| **Root-bound constructs** | Manifestations of the Corruption that have taken on organic form — not undead, not quite alive; something the forest's own material has become |
| **Feral tribal outcasts** | Goblins driven from their tribes by the spreading crisis, not corrupted but desperate enough to be dangerous |
| **Despoiled wardens** | Creatures that once held territorial balance in the forest; their corruption breaks the ecological logic that kept everything stable |

#### Campaign-Exclusive Locations

| Location | Description |
|---|---|
| **The Greyline** | The advancing edge of the corruption — a shifting boundary where normal forest transitions into something wrong; moves over the course of the campaign |
| **Abandoned Mossroot warrens** | Sections of the Hidden Pack's territory evacuated as the corruption pressed in; what was left behind tells a story |
| **Contaminated watersheds** | Water sources that have become vectors for the spread; anything downstream is at risk |
| **Deep root sites** | Ancient forest locations that predate the goblin tribes' memory; the Corruption appears to have originated at or near them |

---

#### Ragash's Personal Story

Ragash's hounds are the most sensitive instrument the party has during The Hungry Dark — and that means Ragash is on the front line of understanding what is happening before anyone else.

This is not straightforward.

Her hounds begin to show stress responses that she cannot fully interpret. They are reacting to something real. She knows that absolutely. But they have never encountered anything like this before, which means she cannot read them with the precision she normally relies on. The arc places her in the unfamiliar position of having her most trusted relationship be a source of information she cannot fully decode.

Her greatest fear — losing a hound — becomes structurally present. As the arc develops, one of her hounds may be exposed. Whether the outcome is loss, close call, or something else depends on the arc's events, but the possibility is authored into the arc's design. Ragash's emotional armor, which she maintains with considerable effort around people, is not built for this.

The Hungry Dark also puts her in sustained contact with the goblin tribes — specifically Mossroot — in ways that are not comfortable and not simple. They are losing the same thing she fears losing. They are losing it differently. Whether this becomes a point of connection or simply a parallel wound is shaped by the party's choices.

See [`docs/heroes/RAGASH.md`](../heroes/RAGASH.md)

---

#### Companion Dynamics During This Arc

**Ronan** is positioned to understand Ragash in this arc more clearly than anyone else in the party. He has spent years fearing something inside himself that he cannot fully control — something with its own logic that is not entirely his. He does not have a solution for Ragash, and he does not pretend to. What he has is genuine recognition: the experience of watching something you love and trust become something you cannot entirely read. This dynamic does not make them close in a sudden or dramatic way. It gives them a specific kind of understanding that the arc makes possible.

**Talos** responds to the practical dimensions of the crisis with full engagement, but the ecosystem's suffering reaches him through its human consequences — the settlements at risk, the tribes being displaced, the breakdown of order. He and Ragash do not approach The Hungry Dark from the same direction, but they are both, in the end, protecting what can be protected.

**Eleanor** is drawn toward the deep root sites and the question of what the Corruption is doing to something as old and complex as the Great Forest's underlying systems. Her academic instincts are useful here — she can sometimes identify patterns that Ragash's tracking and Talos's tactical read miss. She is careful not to make Ragash's situation about her curiosity, and usually succeeds.

**Torren**, if present, approaches the Corruption-damaged sites of The Hungry Dark with the attention of a craftsman assessing structural loss. He does not have Ragash's ecological knowledge, but he reads what the Corruption is doing to ancient wood and stone in his own register — as destruction of things that took centuries to build. He finds materials others overlook. He grieves the waste in a way that does not require explanation.

See [`docs/heroes/`](../heroes/)

---

---

## Campaign-Specific Companion Interactions — The Hungry Dark

### The Hungry Dark — Ragash and Ronan

**Condition:** Both Ragash and Ronan must be active companions during this campaign.

**What becomes available:** Quiet, parallel scenes between two companions who understand each other's specific fear without requiring explanation.

---

**The dynamic:**

Ragash does not ask for help. She does not want to be witnessed being uncertain, and she is not going to explain why. Ronan does not offer help directly. He understands not wanting to.

What The Hungry Dark produces is something smaller and more accurate than support: the experience of being around someone who is not alarmed by your situation, who is not trying to solve it, and who is still there.

Ronan has spent years managing something inside him that could, on a bad day, harm someone he wanted to protect. The specific fear underneath Ragash's hound anxiety — *what if I cannot keep the thing I love most safe?* — is not foreign to him. He does not say this. She does not ask. The arc creates space for them to exist alongside each other in their parallel fears without the conversation that would make it smaller.

Specific scenes this arc makes available:

- A night watch scene where Ronan sits with Ragash while she monitors a stressed hound; almost nothing is said; the scene is about what presence costs and what it gives
- A moment after a close call with one of the hounds where Ronan does not say *I understand* — he does something instead, a small practical thing, and she lets him
- A camp scene late in the arc where Ragash, unprompted, tells Ronan something about one of the hounds — not emotional disclosure, but the kind of specific detail you share with someone you have decided to trust a little

**What this demonstrates:** Both characters' capacity for connection operating within the constraints they actually have. Ragash does not become open. Ronan does not become a caretaker. The relationship becomes something real within the bounds of who they are.

See [`docs/heroes/RAGASH.md`](../heroes/RAGASH.md) · [`docs/heroes/RONAN.md`](../heroes/RONAN.md)

---

---

### The Veiled Order

**Summary:** The Corruption spreads through the religious orders — not through disbelief, but through the opposite. Zealots arise who have become convinced that the ancient god should not be kept imprisoned, that its power is not destruction but transformation, and that those who serve it are not losing themselves but ascending. These are not skeptics or cynics. They are true believers who have reframed the Corruption as sacred. The Threshold Circle — a cult operating in proximity to legitimate religious institutions — becomes the visible face of something with deeper roots. As the arc develops, the party discovers that some of what they assumed were legitimate religious orders have been quietly infiltrated, and that the line between sincere faith and cult conviction is harder to see than it appeared.

**Primary affected faction:** The religious orders and the cult network operating within and adjacent to them

**Corruption type:** Religious

---

#### Campaign-Exclusive Enemies

These enemy types exist only during The Veiled Order:

| Enemy Type | Description |
|---|---|
| **Covenant inquisitors** | Officials of legitimate religious institutions who have been turned toward silencing anything that threatens the cult's cover |
| **Shrine wardens** | Figures who maintain corrupted sites while presenting themselves as servants of legitimate faith |
| **Converted pilgrims** | Ordinary believers who found meaning in the cult's message; not uniformly dangerous, but wholly committed |
| **The Surrendered** | Individuals who have given themselves over fully and willingly — not coerced, not deceived, but believing that losing themselves was the point |
| **Order militants** | Cult-aligned fighters drawn from religious military traditions; their training is real; their loyalty has shifted |

#### Campaign-Exclusive Locations

| Location | Description |
|---|---|
| **Compromised holy sites** | Temples and shrines whose surface observance remains intact while their purpose has fundamentally changed |
| **The Threshold Circle's inner sanctums** | Locations beneath or behind ordinary cult meeting places where the inner doctrine is practiced |
| **Converted waypoints** | Rest sites along pilgrim routes that have become points of recruitment and surveillance |
| **The Surrendered's gathering grounds** | Sites where those who have fully given themselves over congregate; deeply unsettling; not immediately violent |

---

#### Ronan's Personal Story

The Veiled Order confronts Ronan with something he has no framework for: people who chose to lose themselves.

His entire life is organized around preventing that from happening to him. He maintains distance, keeps moving, manages the transformation with constant vigilance — all of it in service of not becoming something that erases who he is. He has built his identity around the belief that losing control is the worst outcome, and that preventing it is worth the isolation it requires.

The Surrendered do not believe this. They encountered something vast and decided that the self they were protecting was not worth protecting. They were not deceived — the arc makes clear that many of them understood what they were choosing. They chose it anyway.

This forces Ronan to sit with a question he has never had to answer: what is he actually protecting when he protects his self? Is it the people around him — which is how he has framed it — or is it something more personal than that? And if someone else decided that self was worth surrendering, does that tell him something about his own conviction that it is not?

He does not convert. He does not sympathize with what the cult does. But The Veiled Order is the arc that makes Ronan's core wound a philosophical question rather than just a management problem. That distinction is what makes it his arc.

See [`docs/heroes/RONAN.md`](../heroes/RONAN.md)

---

#### Companion Dynamics During This Arc

**Talos** has no patience for the arc's philosophical complexity at the outset. People are being harmed; the cult is expanding; those responsible should be stopped. His military background means he leads with function when the situation calls for action, and the Threshold Circle's activities frequently call for action. If the party pushes him on what he makes of The Surrendered — people who chose this — his views are more complicated than his initial assessment. He does not understand the choice. He does not dismiss the people who made it. He puts them in the category of things he has seen that he will not speak about casually.

**Eleanor** approaches the arc with analytical caution. The blending of legitimate religious practice and cult doctrine is exactly the kind of puzzle she cannot leave alone. She is useful here — she can identify the theological inconsistencies in the cult's messaging, trace the gradations between sincere faith and manipulated conviction. She is also at risk of spending more time understanding the system than acting against it, and the party may need to pull her out of that tendency.

**Ragash** trusts the hounds' response to compromised holy sites more than any institutional account of what those sites are. She does not engage with the theology. She engages with the evidence she can verify. If Ronan needs someone who will not turn his questions about The Surrendered into an event, she is nearby and she is not going to do that.

**Torren**, if present, engages with the physical evidence of the Threshold Circle's activity — the objects made or corrupted, the sacred spaces desecrated or deliberately remade. He has less patience for the cult's philosophical justifications than for the concrete record of what they have done. Sacred spaces that have been twisted register to him as both theological violation and craft destruction: these things were made carefully, and they have been deliberately broken.

See [`docs/heroes/`](../heroes/)

---

---

## Campaign-Specific Companion Interactions — The Veiled Order

### The Veiled Order — Ronan and Talos

**Condition:** Both Ronan and Talos must be active companions during this campaign.

**What becomes available:** Scenes built around a specific disagreement that reveals something genuine in both characters — and that does not end in resolution.

---

**The dynamic:**

Talos approaches The Surrendered the way he approaches most things: functionally. They have done harm or enabled it. They need to be stopped. Whatever led them to this position, that position is now wrong, and the consequence of wrong positions in a world this dangerous is suffering. He does not hate them. He cannot afford to care about them the way Ronan is caring about them. There is too much else to do.

Ronan cannot approach it this way.

He understands the fear that precedes surrender — the exhaustion of maintaining vigilance against something inside yourself, the appeal of simply letting go of the effort. He does not want to surrender. But he knows what it is to stand near the edge and look at it. The Surrendered stood near the same edge and took one more step. He needs to understand what they found there.

This disagreement is not a fight. Talos is not contemptuous of Ronan's position; he has learned, over the arc, that Ronan sees things he does not see. Ronan is not contemptuous of Talos's position; he knows that someone has to be the one who acts while others are still thinking. What the arc creates is a specific scene — late in the campaign, after the party has encountered The Surrendered multiple times — where the two of them finally put the disagreement into words.

The scene does not produce a winner. It produces mutual disclosure: Talos admits, plainly, that there is something in the cult's appeal he does not understand and suspects he never will. Ronan admits, plainly, that the reason he cannot stop thinking about it is closer to home than he has been willing to say aloud.

**What this demonstrates:** Talos's intellectual honesty and his capacity for relationship with people whose interior lives are different from his own. Ronan's ability to name his own situation to someone he trusts — partial disclosure, not full openness, but real. The Veiled Order is the arc where the distance Talos keeps and the distance Ronan keeps briefly become the same kind of thing.

See [`docs/heroes/RONAN.md`](../heroes/RONAN.md) · [`docs/heroes/TALOS.md`](../heroes/TALOS.md)

---

---

## Document History

| Date | Change |
|---|---|
| July 2026 | Created — Dynamic Story Arc framework established; The Fractured Circle documented as the first confirmed arc |
| July 2026 | Three additional arcs added: The Broken Crown (Political), The Hungry Dark (Natural), The Veiled Order (Religious) |
