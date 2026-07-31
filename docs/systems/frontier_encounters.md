# Frontier Travel Encounter Table

> **Canon Status:** CONFIRMED — 2026-07-31.  
> **Authority:** This document defines the canonical encounter table for Frontier travel. The AI DM must use these entries when placing encounters during Frontier travel sequences. Named goblin contact entries supersede improvised placement — if the party is in a goblin tribe's zone, use the authored entries here rather than a generic encounter. Encounter philosophy from [`docs/world/WORLD_BIBLE.md`](../world/WORLD_BIBLE.md) applies to every entry.  
> **Cross-references:** [`docs/world/WORLD_BIBLE.md`](../world/WORLD_BIBLE.md) · [`docs/world/goblin_tribes.md`](../world/goblin_tribes.md) · [`docs/quests/goblin_tribe_quests.md`](../quests/goblin_tribe_quests.md) · [`docs/systems/reputation.md`](reputation.md) · [`docs/encounters/mossroot_first_contact.md`](../encounters/mossroot_first_contact.md)

---

## How to Use This Document

The Frontier is divided into three tribal zones plus neutral travel corridors. Before placing an encounter:

1. **Identify the zone** — which tribal territory is the party traveling through?
2. **Check the party's reputation** — existing standing with a tribe changes what contact looks like
3. **Select encounter type** — use the authored entries for goblin contacts; use the frequency table for other encounter types
4. **Apply encounter philosophy** — present choices; do not default to combat; let ignored threats persist

> **Rule:** Goblin contacts in their home zone are never procedurally generated. Use the named entries in this document. A Stonefang encounter in Stonefang territory is a specific authored contact, not a random ambush, unless the party's prior reputation makes combat the only remaining option.

---

## Frontier Zone Map

The Frontier's goblin tribal territories define the encounter context for most travel.

```
NORTH ─────────────────────────────────────────────────────────
                    [NEUTRAL CORRIDOR]
       Frontier Northern Edge · Iron Peaks border zone
────────────────────────────────────────────────────────────────
  [STONEFANG ZONE]           │        [NEUTRAL/CONTESTED]
  Eastern Frontier           │        Great Forest margins
  Fang-Hold & trade roads    │        
  · High contact frequency   │  [MOSSROOT ZONE]
  · Caravan route runs here  │  Forest margin camps
  · Varkk patrols active     │  Seasonal movement
                             │  · Low contact if avoided
────────────────────────────────────────────────────────────────
  [CONTESTED BORDER]         │  [MOSSROOT / ASHFIRE OVERLAP]
  Stonefang/Ashfire tension  │  Cautious coexistence zone
────────────────────────────────────────────────────────────────
  [ASHFIRE ZONE]             
  Central and southern Frontier · Cinderhold
  Sol Kareth trade route (northern spur)
  · Politically active; emissary contacts common
  · Caravan escort opportunities
SOUTH ─────────────────────────────────────────────────────────
```

**Neutral corridors** — areas not currently claimed by any tribe — still generate encounter activity but primarily from bandits, wildlife, refugees, and the Corruption. The AI DM may seed goblin contacts in neutral corridors if tribal logic warrants it (a Mossroot runner avoiding the main trails, a Stonefang raiding party in transit).

---

## Encounter Frequency — Frontier Travel Leg

Roll or select encounter type per travel leg (one leg = a half-day's travel between significant points).

| Roll / Frequency | Encounter Category |
|---|---|
| Very common (≥1 per leg in active zones) | Goblin tribal activity — contact, tracks, patrol |
| Common (most legs) | Bandit ambush or merchant encounter |
| Occasional (some legs) | Corrupted wildlife, refugees, Adventurers Guild contract runner |
| Rare (notable when it occurs) | Orc warband, ancient ruin discovery, Ancient monster sign |
| Uncommon (not every journey) | Companion event, hidden shrine, world boss approach |

> **AI DM note:** Do not place two significant encounters on the same travel leg without narrative justification. One meaningful contact is better than three diluted ones. A leg with no encounter is valid — not every journey needs an event.

---

## Goblin Tribe Contact Encounters

Each tribe has four authored contact types, graded by prior reputation and campaign stage. The AI DM selects the type that matches the current relationship state.

---

### Stonefang Tribe — Eastern Frontier

**Territory:** Eastern contested zones, trade road to Fang-Hold  
**Contact frequency:** Common to Very Common in zone  
**Quest this leads to:** *"The Debt Comes Due"* — [`docs/quests/goblin_tribe_quests.md`](../quests/goblin_tribe_quests.md)

---

#### SF-C1 — Patrol Contact (No Prior Reputation)

**When to use:** Party has no established Stonefang reputation; first or early encounter in zone

**What the party sees:**  
A group of four to six Stonefang warriors moving along the trade road, spread wide enough to suggest they are looking for something rather than traveling. They carry trophies — armor pieces, a human shield with an axe buried in it — that establish their identity immediately. They have spotted the party before the party has options.

**How the contact goes:**  
The patrol leader moves forward, hand not on their weapon. This is assessment, not immediate aggression. They want to know who the party is and whether they are worth fighting, taxing, or ignoring. They will ask — directly, without pleasantries — where the party is going and what they are carrying. They will not attack unless provoked or the party attempts to flee.

**Resolution options:**

| Approach | Outcome | Reputation effect |
|---|---|---|
| Comply, show goods, pay informal toll | Patrol moves on; the party is marked in Stonefang memory as compliant travelers | Neutral to slight positive; no debt |
| Demonstrate capability without combat (intimidation, visible equipment quality) | Patrol reassesses; the leader gives a short nod and withdraws | Mild positive; the party is noted as "worth watching" |
| Negotiate — offer information or a small bribe | Patrol accepts; party passes freely | Neutral |
| Attempt to flee | Patrol pursues; combat likely | Slight negative |
| Combat | Direct resolution; patrol may retreat if clearly losing | −10 Stonefang if patrol is killed; Varkk learns of it |

**What this plants:**  
If the party paid, negotiated, or impressed the patrol, the patrol leader files an informal report with the tribe's scout network. Within one session, Grakkor's organization knows the party exists and something about what they are. This sets up the Debt of Steel contact (SF-C3) as a natural next step.

---

#### SF-C2 — Varkk's Patrol (Neutral or Negative Reputation)

**When to use:** Party has negative Stonefang standing, OR has demonstrated combat capability against the tribe but has not been formally identified as an enemy

**What the party sees:**  
A larger patrol — eight to twelve warriors — moving with coordinated purpose. Varkk himself may be present, or a lieutenant who reports directly to him. The formation is aggressive-defensive: they are not hiding, but they have chosen a position that makes retreat difficult.

**How the contact goes:**  
Varkk (or his lieutenant) is direct and hostile. He believes the party has either done something against the tribe or represents a future problem. He will offer combat or demand something specific — the return of goods taken from a patrol, information about what the party is doing in Stonefang territory, a demonstration of subservience.

**Resolution options:**

| Approach | Outcome | Reputation effect |
|---|---|---|
| Comply with demands | Varkk lets them through; his contempt is visible | Slight positive with Varkk; negative with Grakkor's faction (who sees this as the party treating Varkk as the authority) |
| Challenge Varkk's authority — appeal to Grakkor's standing | Varkk backs down, angry; the party has correctly identified the political structure | Significant positive with Grakkor's faction; Varkk remembers the party |
| Combat | Varkk is a capable fighter; this is a real engagement | −20 Stonefang if Varkk is killed or badly wounded; opens a vendetta |
| Escape or stealth exit | The party avoids the encounter; Varkk's patrol loses them in terrain | No change; Varkk is frustrated |

**What this plants:**  
This encounter clarifies for the party that there is a political division in the Stonefang between Grakkor's strategic faction and Varkk's aggressive one. This knowledge is directly useful in *"The Debt Comes Due."*

---

#### SF-C3 — The Debt Runner (Quest Entry Point)

**When to use:** Party has neutral or positive Stonefang reputation; Grakkor has identified them as potentially useful; campaign stage is appropriate for the Stonefang quest

**What the party sees:**  
A single Stonefang goblin moving quickly but openly — not trying to hide, which is notable. The runner carries a sealed message marked with Grakkor's personal sigil (a stone fang design recognizable to anyone with any Stonefang knowledge). The runner is looking for the party specifically, or looking for someone and finds the party.

**Two versions:**

*Version A — Direct summons:*  
If the party was previously spared by a Stonefang patrol (has a Debt of Steel owed to them), the runner addresses them by name or description: "You owe. Warchief Grakkor calls it now." The runner hands the message — time, location, truce terms. He will not discuss the details; his job is delivery.

*Version B — Intercepted summons:*  
The runner is looking for someone else — a Frontier settlement contact or another party. The player party encounters the runner at a road junction. They can intercept (overhear the name being called, or the runner bumps into them), follow him to find out where he is going, let him pass, or question him. The runner will not reveal the message contents but will admit it carries Grakkor's mark if pressed honestly. The party can follow to discover the context — and decide whether to let events unfold or insert themselves.

**The message:**  
Brief, written in Trade Common (Grakkor is literate, a fact Varkk resents). It states: a debt is owed, payment is requested in the form of a specific service, come to [location] under a temporary truce marked by this message, arrive within three days.

**Resolution options:**

| Approach | Outcome |
|---|---|
| Accept the summons and go | *"The Debt Comes Due"* begins at Stage 1 |
| Ignore the message | Varkk's alternative (raiding the caravan) proceeds within two days; world state effect occurs; party has lost an opportunity |
| Intercept and investigate before deciding | Party gains advance information about what Grakkor wants; can prepare accordingly; quest still begins at Stage 1 |
| Send word declining | −20 Stonefang immediately; party is treated as having refused a lawful Debt of Steel |

**Ragash note:** If Ragash is in the party, her hounds may pick up the runner's trail before visual contact — the runner's approach is detectable a few minutes before he reaches the road junction. The party has a moment to prepare or observe before being addressed.

---

#### SF-C4 — Established Alliance Contact (Positive Reputation 20+)

**When to use:** Party has completed *"The Debt Comes Due"* with positive outcome, OR has built Stonefang reputation above 20 through other means

**What the party sees:**  
A Stonefang warrior at a known road junction — not aggressive, not hiding. He wears a trophy item that marks him as a member of Grakkor's personal command (not Varkk's raiders). He waits for the party to approach.

**How the contact goes:**  
Grakkor sends intelligence or a request through trusted runners now that the party has proven useful. Examples of what the contact may carry:
- Information about a threat Grakkor's scouts have identified that he cannot address directly (politically useful to share with the party)
- A request for a specific service with named terms and offered payment
- Warning that Varkk has learned something about the party's activities and is moving to act
- Trade goods available at Fang-Hold that Grakkor knows the party may want

This contact type establishes that the relationship with Grakkor now has ongoing operational texture — he uses the party as a resource in his political calculations the same way he uses his own officers.

---

### Mossroot Tribe — Great Forest Margins

**Territory:** Southern and western Great Forest margins, forest-adjacent Frontier travel routes  
**Contact frequency:** Low unless the party enters forest-margin terrain; increases with time in zone  
**Quest this leads to:** *"What the Forest Carries"* — [`docs/quests/goblin_tribe_quests.md`](../quests/goblin_tribe_quests.md)  
**First contact scene:** [`docs/encounters/mossroot_first_contact.md`](../encounters/mossroot_first_contact.md)

---

#### MR-C1 — Hound Alert (Companion Trigger)

**When to use:** Ragash is in the active party; party is traveling along or through forest-margin terrain; no prior Mossroot contact has occurred

**What the party sees:**  
Nothing immediately. Ragash's hounds go still — not defensive alert, but the focused stillness of tracking. Ragash reads them and reports: goblin trail, recent (within hours), moving parallel to the party's path before cutting off the road toward the forest. At least two individuals, probably more. The trail does not circle back.

**How the contact goes:**  
This is information, not a contact — yet. The party can:

| Approach | Outcome |
|---|---|
| Follow the trail | Leads to a Mossroot scout observation post; the scouts were already watching the party; they are neither hidden nor aggressive — they retreat when approached but leave a single marker at the post (a carved stick that an Old Ways practitioner or Mossroot-knowledgeable character can identify as "we have seen you; we choose not to engage") |
| Ignore it and continue | The Mossroot scout reports back to Vess; next encounter is MR-C2 |
| Leave a non-threatening gesture at the trail (offer, placed without pursuit) | A scout retrieves it; not acknowledged yet but noted; accelerates trust-building in future contacts |
| Set a trap | Scouts detect the trap and disappear completely; Mossroot contact is harder to initiate for the next several sessions |

**What this plants:**  
The Mossroot know the party is in the zone and know Ragash is with them. Her species and the behavior of her hounds (tracking vs. aggressive) form their initial assessment. The carved marker, if examined, is the beginning of a communication thread.

---

#### MR-C2 — The Runner in the Open (Quest Entry Point, Version A)

**When to use:** Party has neutral or slightly positive Mossroot reputation from prior animal behavior (no trap-setting, no aggressive pursuit); no prior Mossroot quest entry

**What the party sees:**  
A young Mossroot goblin — visibly not a senior member — steps onto the road from the tree line approximately forty feet ahead. Hands visible. Not armed in an aggressive posture (tracking staff across the back, not in hand). The goblin waits for the party to close distance before speaking.

**How the contact goes:**  
The runner introduces himself as acting for the tribe without naming Vess or the council — he has been authorized to make contact but not to reveal the full structure behind the request. He says: *"A young hunter from our camps has been missing for three days near the forest edge. We have heard a party with a hound-orc is in the area. Have you seen a goblin traveling alone?"*

This is the Mossroot quest's *Runner Contact* entry point — the party has been identified as having Ragash and therefore as having potentially useful tracking capabilities. The runner is asking, not demanding. He expects the party to say no and leave. If they express genuine interest or ask follow-up questions, he becomes cautiously more forthcoming.

**Resolution options:**

| Approach | Outcome |
|---|---|
| Agree to help or investigate | *"What the Forest Carries"* begins; runner provides general area |
| Ask for payment first | Runner doesn't have authority to offer payment; the council would need to authorize it; he will say this honestly; the party can follow him to raise the question |
| Decline and move on | Runner thanks them briefly and disappears; Kett's situation worsens; the elven community's concern increases; the quest is still accessible via MR-C3 |
| Treat the runner with contempt | −10 Mossroot; no further contact from this runner; the tribe marks the party as "not people we work with" |

---

#### MR-C3 — Ferath's Edge Contact (Quest Entry Point, Version B)

**When to use:** Party enters the elven settlement of Ferath's Edge for any reason; this version runs if MR-C2 did not fire or was declined

**What the party sees:**  
At Ferath's Edge, an elven border guard stops the party at the settlement entrance with a specific question rather than a standard greeting: *"You have been through the forest margins recently. Have you seen any unusual tracks near the sacred grove — and did you encounter a young goblin in that area?"*

The guard is not hostile. She is gathering information. The settlement is currently holding Kett and trying to understand what happened, and they would appreciate outside confirmation or new information before deciding what to do with him.

**How the contact goes:**  
The elves explain the situation: they have detained a Mossroot goblin found moving away from the sacred grove, and they suspect he disturbed it. They ask the party to investigate before they act on the suspicion. If the party agrees, this is the *Elven Contact* entry for "What the Forest Carries."

**What this plants:**  
The party now has both an elven contact (Ferath's Edge standing) and a Mossroot contact (through Kett, once they find and talk to him). Navigating between the two communities' interests becomes the core of the quest.

---

#### MR-C4 — Established Trust Contact (Positive Reputation 20+)

**When to use:** Party has completed *"What the Forest Carries"* positively, OR has Mossroot reputation above 20

**What the party sees:**  
Vess herself, or Thorn the war leader, at a trail junction the party is using. The meeting feels deliberate — the Mossroot knew the party's route. It is not an ambush; it is the Mossroot's way of showing they are paying attention.

**How the contact goes:**  
Vess offers information: something she has observed in the forest margins that she believes the party would want to know. What she shares depends on current campaign state — tribal movements, a corrupted animal sighting, intelligence about the treasure hunter faction or whoever hired them, or Ashfire expansion activity near Mossroot-adjacent zones. She does not ask for payment. She is operating within a now-established relationship and expects similar information flow in return.

**If the party shares what they know in return:**  
Mossroot standing increases by 5. If the shared information is genuinely useful (not just pleasantries), this can unlock the High Reputation track — Vess designating the party as "people worth finding" rather than just "people worth watching."

---

### Ashfire Tribe — Central and Southern Frontier

**Territory:** Central and southern Frontier, Cinderhold and surrounding area, Sol Kareth trade route northern spur  
**Contact frequency:** Common in zone; emissary contacts are particularly common near Frontier settlements  
**Quest this leads to:** *"Smoke and Terms"* — [`docs/quests/goblin_tribe_quests.md`](../quests/goblin_tribe_quests.md)

---

#### AF-C1 — Emissary in a Settlement (Quest Entry Point, Primary)

**When to use:** Party is in a Frontier settlement within or adjacent to Ashfire territory; no prior Ashfire contact; campaign stage is appropriate for the Ashfire quest

**What the party sees:**  
A well-dressed goblin — "well-dressed" meaning deliberate presentation rather than wealth, clean clothing, no visible weapons, nothing that reads as raider — sitting at a common room table or waiting near the settlement's main road. The goblin does not look out of place precisely because she is projecting the appearance of belonging. She has been here a few hours.

The emissary's name is **Senn** — one of Skarra's inner council members assigned to diplomatic contact work. She stands when the party approaches (or when she identifies them if the party has a prior reputation) and introduces herself by name and role without preamble: *"I represent Warchief Skarra Ashfire. I have been told you are capable people who operate across the Frontier. The Warchief has a proposal she would like you to hear."*

**How the contact goes:**  
Senn explains the basic shape of the caravan escort request without revealing the internal political context (Brenn's dissent). She offers standard compensation and specifies that the Warchief guarantees safe passage to Cinderhold for the initial meeting. She is professional, clear, and will answer direct questions honestly — Skarra has given her instructions to not lie to people Skarra wants to work with.

**Resolution options:**

| Approach | Outcome |
|---|---|
| Accept the meeting | *"Smoke and Terms"* begins at Stage 1 |
| Ask for more details before agreeing | Senn provides everything she is authorized to share; the party is invited to Cinderhold to hear the rest directly from Skarra |
| Decline | Senn thanks them for their time; the quest entry point closes for this session; the AI DM may re-seed via AF-C2 in a later session if the campaign context remains appropriate |
| Treat Senn poorly or dismissively | −10 Ashfire; Senn's report to Skarra affects the initial meeting atmosphere if the party later changes their mind |

**Ragash note:** Senn's assessment of Ragash is different from her assessment of the human party members. She addresses Ragash separately from the others — not more or less respectfully, but differently, acknowledging her as a distinct entity rather than a party component. This is deliberate Ashfire political behavior (recognizing that non-human parties to negotiations may have distinct interests), and Ragash notices it.

---

#### AF-C2 — Road Encounter with Ashfire Patrol (No Prior Reputation)

**When to use:** Party is traveling through Ashfire-claimed territory without prior contact; AF-C1 has not fired or was missed

**What the party sees:**  
A patrol of six Ashfire warriors crossing the road ahead — not blocking it, but moving across it in a way that makes passing without acknowledgment awkward. They carry the dual clan-marks (older warriors with both original clan and Ashfire marks visible). One holds up an open hand — stop, we want to talk.

**How the contact goes:**  
The patrol leader identifies the party as travelers in Ashfire territory and states this plainly: *"You are in Warchief Skarra's land. Tell us your business and your destination."* This is a border-check, not a robbery. The Ashfire under Skarra are trying to establish that their territory has legitimate authority — this patrol is an expression of that project.

**Resolution options:**

| Approach | Outcome | Reputation effect |
|---|---|---|
| State business honestly and ask about Ashfire territory | Patrol provides a brief orientation — what roads are safe, where Cinderhold is, what behavior is expected | Slight positive; party is noted as cooperative |
| Negotiate passage terms | Patrol may accept a small contribution or a commitment to report anything hostile they see | Neutral to slight positive |
| Dismiss or argue against the patrol's authority | Patrol leader is not offended but becomes formal and cold; passage is technically granted but the party is noted | Slight negative |
| Attempt to intimidate | Patrol holds position; the leader assesses the party's capability before deciding; if capability is clear, they let them pass and report both the party's capability and their behavior | Neutral, but the capability report reaches Cinderhold |
| Combat | This is exactly what Skarra does not want happening to the caravans she is trying to protect; if Skarra learns of it, significant penalty | −20 Ashfire; Brenn uses the incident politically |

---

#### AF-C3 — Brenn's People (Reputation-Modified Encounter)

**When to use:** Party has neutral-to-positive Ashfire reputation AND is traveling the Sol Kareth trade route northern spur; fires before or during *"Smoke and Terms"* Stage 2

**What the party sees:**  
A cluster of Ashfire goblins at the road's edge — not the full patrol posture of AF-C2, more like people who are waiting to be seen. They carry original clan-marks prominently displayed: former members of one of the two clans that resisted unification. They are not aggressive. They want to assess the party that Skarra has hired.

**How the contact goes:**  
A spokesperson (not Brenn himself — Brenn doesn't expose himself to parties he doesn't control) asks the party direct questions about their work for Skarra: what they were promised, whether they know what they are actually being used for, whether they are aware of the internal debate about the Sol Kareth approach. He frames this as giving the party information they deserve to have before committing to a politically complicated situation.

What he is actually doing: assessing whether the party is committed to Skarra's project or potentially persuadable to a neutral or indifferent position that would allow Brenn's alternative (controlled disruption) to proceed.

**Resolution options:**

| Approach | Outcome | Effect on "Smoke and Terms" |
|---|---|---|
| Listen and share nothing useful | Party gains intelligence about Brenn's position; Brenn's faction gains nothing | Party enters Stage 2 with advance knowledge of the road positioning |
| Share information about Skarra's arrangements | Brenn's people are better positioned to complicate the demonstration | Stage 2 is harder; Sural Vayne more likely to see the disruption |
| Report the encounter to Skarra before Stage 2 | Significant positive; Skarra has a tool to address Brenn directly | Additional +10 Ashfire |
| Drive Brenn's people away | They report the party as committed to Skarra's project; Brenn's positioning on the route becomes more aggressive | Stage 2 Brenn encounter is harder |

---

#### AF-C4 — Ash Oath Witness Invitation (Positive Reputation 25+)

**When to use:** Party has completed *"Smoke and Terms"* with positive outcome and the Ash Oath scene was reached; fires in a subsequent session

**What the party sees:**  
Fire-Speaker Durn — the Ashfire's ceremonial elder — sends a young clan member to find the party on the road. The message is simple: Durn wants to speak with them. This is not a request Skarra is behind, which the messenger will say if asked. Durn acts on his own spiritual authority.

**How the contact goes:**  
Durn wants to talk about what the party witnessed at the Ash Oath — not politically, but in terms of what it meant. He is interested in whether outside parties understand the weight of what Skarra has committed to. He will ask the party, directly, what they think Skarra is building. He is not testing them — he is genuinely asking.

This contact is purely narrative: it deepens the Ashfire thread, gives the party a window into the ideological tensions inside the tribe (Durn's spiritual continuity vs. Skarra's political survival), and establishes Durn as someone the party can bring genuine concerns to when the AI DM needs a Ashfire internal channel that bypasses Skarra.

---

## Reputation Thresholds — Goblin Encounter Modification

How existing reputation changes what encounter type fires:

| Stonefang Standing | Contact Type | Notes |
|---|---|---|
| Below −20 | SF-C2 (Varkk's patrol, hostile) | Combat likely |
| −20 to 0 | SF-C1 (assessment patrol) or SF-C2 | Tone is aggressive |
| 0 to 15 | SF-C1 (standard patrol) | Assessment, not hostile |
| 15 to 25 | SF-C3 (Debt Runner) becomes available | Quest entry opens |
| 25+ | SF-C4 (alliance contact) | Grakkor uses party as a resource |

| Mossroot Standing | Contact Type | Notes |
|---|---|---|
| Below −15 | No voluntary contact | Mossroot avoid the party entirely |
| −15 to 0 | No contact; Mossroot tracking observed if Ragash is present | Hound alert fires but no runner |
| 0 to 10 | MR-C1 (hound alert) + MR-C2 or MR-C3 available | Quest entry opens |
| 10 to 20 | MR-C2 or MR-C3 fires more readily | Trust threshold lowered |
| 20+ | MR-C4 (Vess direct contact) | Vess shares intelligence proactively |

| Ashfire Standing | Contact Type | Notes |
|---|---|---|
| Below −20 | AF-C2 (patrol, hostile tone) | Passage may be refused |
| −20 to 0 | AF-C2 (patrol, neutral) | Standard border check |
| 0 to 15 | AF-C1 (emissary) or AF-C2 | Quest entry available |
| 15 to 25 | AF-C3 (Brenn encounter) available during quest | Internal politics surface |
| 25+ | AF-C4 (Durn invitation) | Deep Ashfire access |

---

## Broader Frontier Encounter Table

Non-goblin encounters for Frontier travel legs. The AI DM selects these when a goblin contact is not appropriate (wrong zone, recent contact fatigue, campaign pacing).

---

### Combat Encounters

| Encounter | Zone | Frequency | Notes |
|---|---|---|---|
| **Bandit ambush** | Trade road, neutral corridor | Common | Motivation varies — economic desperation, hired contract, opportunism; see player choice options below |
| **Orc warband** | Northern and western Frontier | Occasional | Organized; may have specific territorial or political goals; not automatically hostile |
| **Corrupted wildlife** | All zones; increasing near Corruption-active areas | Occasional | Hollow animals, distorted behavior; see Corruption encounter files |
| **Necromancer ritual site** | Ruins, ancient battlefields | Rare | Risk of undead escalation if interrupted incorrectly |
| **Ancient monster (awakened)** | Deep Frontier, ruins | Rare | Corruption-adjacent; significant threat; never without warning signs first |
| **Troll territory** | River crossings, specific terrain features | Rare | Environmental hazard; highly territory-specific |

**Bandit resolution options (always offer):**

| Approach | Available when |
|---|---|
| Intimidate — demonstrate capability | Party has visible combat scars, quality equipment |
| Negotiate — discover motivation | Party asks rather than immediately defending |
| Bribe — offer passage payment | Party has coin and the bandits' goal is economic |
| Deceive — claim official authority | Party can back this up or create sufficient uncertainty |
| Investigate before engagement | Party scouts the ambush ahead of time (Ranger, Ragash hounds) |
| Combat | Always available; never the only option |

---

### Social Encounters

| Encounter | Frequency | What it offers |
|---|---|---|
| **Traveling merchant** | Common | Trade; rare inventory; information about road conditions and events ahead; may carry a rumor relevant to active quests |
| **Frontier settler family** | Occasional | World state indicator; may have been displaced, have a specific problem, or carry regional information; not a quest giver but a lore carrier |
| **Adventurers Guild contract runner** | Occasional | Carries open contracts relevant to the Frontier zone; may recognize a party with Guild reputation |
| **Covenant pilgrims** | Occasional (higher near Capital Province border) | Faction contact; may have information about religious activity in the region; escort opportunity |
| **Wandering musician** | Rare | Tone lightener; carries oral tradition and lore in song form; may know something specific if the party asks the right questions |
| **Mercenary company (passing)** | Rare | Identifiable by equipment and formation; may be traveling to or from a contract; information about who is hiring in the region |
| **Refugees (Corruption-displaced)** | Occasional to Common depending on campaign stage | World state indicator; Corruption has forced them out; carry first-hand accounts; may have seen something the party needs to know |

---

### Discovery Encounters

| Encounter | Frequency | Notes |
|---|---|---|
| **Ancient ruins** | Occasional | Environmental storytelling; may conceal dungeon entrance or named location from `docs/world/GEOGRAPHY_LANDMARKS.md` |
| **Forgotten watchtower** | Occasional | Structural information (who built it, how old, condition); may reveal map detail or serve as an observation point |
| **Hidden shrine** | Occasional | Covenant, Old Ways, or Ancestors' Path; see `docs/world/shrine_locations.md` for named shrines; generates small buff or quest hook |
| **Abandoned campsite** | Common | May indicate recent activity (who was here, how long ago, why they left); Ranger or Ragash can read more from this than others |
| **Battle site (old)** | Occasional | Historical content; Talos companion event site (see below); may contain salvageable material |
| **Ancient battlefield (First Empire)** | Rare | Significant discovery; Talos, Eleanor, and the AI DM all have specific responses; lore-dense |

---

## Companion Frontier Events

Frontier travel triggers specific companion-character moments. These layer over travel rather than replacing it — they occur while the party is moving.

### Talos — The Battlefield He Knows

**Trigger:** Party passes through any location tagged as a military engagement site, ancient battlefield, or fortified ruin in the Frontier. A second trigger fires near the Capital Province border specifically.

**What happens:** Talos goes quiet. He is reading the ground — sight lines, defensive positions, what the people who built this were afraid of. If the party asks, he explains what he sees. If they don't ask, he eventually says something anyway — something specific about the position, not a generic observation. What he says reveals something about how he thinks and, at higher trust, something about a specific battle he was part of.

**What this unlocks:** At trust 15+, the specific battle he references is one where he followed orders he knew were wrong. This is the entry point for his personal quest if it has not been seeded otherwise.

---

### Eleanor — Anomaly Recognition

**Trigger:** Party passes through a zone with unusual magical activity, a damaged shrine, Corruption wildlife signs, or any location tagged as having arcane significance.

**What happens:** Eleanor slows or stops. Her description of what she senses is specific — not "something feels wrong" but a technical assessment that tells the party something meaningful about what they are passing through. She will ask to stop and look if the party is willing.

**What this unlocks:** Her assessment is usable information. It may point toward a hidden encounter, explain a world state condition, or reveal something about the Corruption that the party did not have a name for. At trust 15+, she connects what she observes to her personal research thread.

---

### Ragash — Hound Intelligence

**Trigger:** Party travels through any zone with active goblin tribal presence, concealed threats, or hidden paths (applicable on most Frontier travel legs).

**What happens:** Ragash reads her hounds' behavior and reports what they are detecting — goblin activity, a creature watching from cover, a trail that the party's path crosses at an angle. This is information delivery, not flavor. What the hounds detect is specific and actionable.

**What this unlocks:** At trust 10+, Ragash may add personal commentary to her hound reports — observations about the Frontier that reveal her own history with it. At trust 20+, she begins sharing something specific about where her hounds came from and why she trains them the way she does.

---

### Ronan — The Distant Howl

**Trigger:** Party travels at dusk or night, or passes through wilderness far from settlements; fires in the Frontier when the party is more than a half-day from a settlement.

**What happens:** Ronan stops. He has heard something the others may not have — a howl in the distance, or the specific quality of silence that follows one. He will not explain immediately. If the party waits, he eventually says something — whether what he heard was wildlife, a turned werewolf pack, or something else entirely. At lower trust, he says it was nothing. At higher trust, he is honest that he is not sure.

**What this unlocks:** At trust 15+, he admits that he uses these moments to check whether the Frontier's packs respond to him. If they do, that means something he has not decided how to feel about. This is seeding for his personal quest if it has not opened otherwise.

---

### Torren — The Salvager's Eye

**Trigger:** Party passes through ruins, abandoned settlements, or post-conflict sites (very common in the Frontier).

**What happens:** Torren identifies usable materials and structural weaknesses others overlook. He may stop to retrieve something specific, or he may only comment on what he sees — what can be saved, what is beyond repair. At lower trust, his commentary is practical. At higher trust, it edges toward philosophical: what things are worth saving and why, and what it means that someone built this and it was destroyed.

**What this unlocks:** At trust 15+, he mentions something he once tried to save that he couldn't. This is not elaborated — it is planted. His personal quest builds from this.

---

## AI DM Guidance — Encounter Sequencing

### Seeding Goblin Contacts Organically

**Rule:** Do not make the party seek out goblin leadership. Let the contacts find them.

The goblin quest entry points are designed to arrive through normal travel behavior. The party does not need to know they should be looking for a Stonefang runner — the runner finds them. They do not need to know the Mossroot have a missing hunter — Ragash's hounds put them on the trail.

Use the encounter table entries above rather than requiring the party to make a quest-seeking decision. If the party is in Stonefang territory and the campaign stage is right, SF-C3 fires. The party's choice is what to do with the contact, not whether to find it.

### Escalating Ignored Threats

Per the Encounter Philosophy in `docs/world/WORLD_BIBLE.md`: threats that are ignored do not disappear.

| Ignored contact | What happens next |
|---|---|
| Party ignores SF-C3 (Debt Runner) | Varkk raids the caravan within two days; Frontier settlement militia capability is reduced; Stonefang internal politics shift toward Varkk's position |
| Party ignores MR-C2 (Mossroot runner) | Kett's situation worsens; elven community makes a decision without party input; Mossroot/elven territorial arrangement may be damaged; access to MR-C4 delayed |
| Party ignores AF-C1 (Ashfire emissary) | Senn reports the party as uninterested; Brenn's alternative gains internal momentum; the caravan demonstration happens without a neutral third party, reducing its effectiveness; Ashfire-Sol Kareth negotiation stalls |

### Contact Fatigue

Do not fire two significant goblin contacts in the same travel leg unless the party is actively pursuing goblin political engagement. Contacts should feel like the world's logic delivering them, not like a content queue being processed.

**Minimum spacing:**
- Two tribe contact encounters: at least one travel leg apart
- Same tribe contact encountered again: at least two travel legs apart
- Quest entry point fires: once per tribe per campaign phase

### After Quest Completion

Once a quest entry point has fired and the quest has resolved, goblin contacts in that tribe's zone shift from quest-seeding to relationship-operating. Use the positive reputation contact type (SF-C4, MR-C4, AF-C4) rather than repeating the entry point encounter. The relationship now has content; the entry point was the beginning, not the whole story.

---

## Document History

| Date | Change |
|---|---|
| 2026-07-31 | Created — Frontier encounter table including four authored contact types per goblin tribe (quest entry points, reputation-modified variants, first contacts, and established alliance contacts); reputation thresholds; broader Frontier encounter table (combat, social, discovery); companion frontier events for all five companions; AI DM sequencing guidance |
