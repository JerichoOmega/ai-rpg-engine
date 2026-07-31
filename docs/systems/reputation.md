# Reputation System

**Purpose:** Documents the per-faction reputation design philosophy and its consequences for gameplay.

**Design inspiration:** Fallout: New Vegas

---

## Overview

The reputation system does **not** use a universal morality score.

Players are not rated as "good" or "evil." Instead, reputation is tracked **separately for each major faction** in the world. A player can be a hero to the Adventurers Guild, despised by the Mages Guild, and respected by one goblin tribe while being hunted by another — simultaneously.

This creates a world that feels politically real rather than morally simplified.

---

## Design Principles

### No Universal Score

There is no single slider from "good" to "evil." Reputation is relational — it describes the player's standing with a specific group based on their actual history with that group.

### Actions Have Consequences

Player decisions — completing quests, breaking alliances, siding with one faction against another, attacking groups, protecting settlements — create lasting changes to specific faction standings.

### Factions Remember

High or low reputation is not easily reset. Factions that have been wronged do not forget. Factions that have been helped will call on that history.

### Reputation Is Asymmetric

Actions that help one faction may harm another. Siding with the Adventurers Guild against a vampire coven will improve one standing and destroy the other. Players must manage a web of relationships, not a single meter.

---

## Factions with Reputation Tracking

The following factions are confirmed to have separate reputation tracking:

| Faction | Notes |
|---|---|
| **Kingdoms** | The ruling authorities; political standing with government |
| **Adventurers Guild** | The neutral trade organization; quest access and information |
| **Mages Guild** | The arcane institution; magical services and Eleanor's faction |
| **Vampire Houses** | Three Great Houses, each tracked independently with formal tier tables; seven Founding Houses use narrative standing only — see below |
| **Goblin Tribes** | Three separate tribes, each tracked independently — see below |
| **Religious Orders** | Four orders, each tracked independently — see below |
| **Mercenary Companies** | ⚠️ NOT YET DEFINED — specific companies to be established |

### Goblin Tribes (detail)

Three tribes are tracked independently. Standing with one does not transfer to others — tribal interests frequently conflict, and helping one tribe may actively harm standing with another.

| Tribe | Leader | Reputation Character |
|---|---|---|
| **Stonefang Tribe** | Warchief Grakkor Stonefang | Strength-based; affected by demonstrated combat capability, honoring the Debt of Steel, outcomes of leadership challenges, and willingness to deal directly rather than through intermediaries |
| **Mossroot Tribe** | Elder Speaker Vess | Trust-based and slow-building; affected by how the party treats Mossroot territory, wildlife, and secrets — notably the Deep Warren; council consensus means reputation shifts are gradual in both directions |
| **Ashfire Tribe** | Warchief Skarra Ashfire | Politically sensitive; affected by consistency and follow-through on commitments (Ash Oaths are taken seriously), treatment of the unification's legitimacy, and whether the party is perceived as a long-term political partner or short-term opportunist |

**Cross-tribal reputation dynamics:**
- Helping the Stonefang against the Mossroot in a territorial dispute creates a significant Mossroot penalty and a moderate Stonefang gain
- Helping the Mossroot defend against Stonefang incursion creates the reverse
- Recognizing Ashfire territorial claims (e.g., in negotiating safe passage through their zone) creates an Ashfire gain with no automatic effect on the other two — but the Stonefang will note it
- Brokering peace or a territorial agreement between any two tribes creates a smaller gain with the third (they observe that the party can operate as a neutral political actor)

> Full tribal definitions: [`docs/world/goblin_tribes.md`](../world/goblin_tribes.md)

### Religious Orders (detail)

Four orders are tracked independently, one per major religion:

| Order | Parent Religion | Reputation Character |
|---|---|---|
| **The Covenant Clergy** | The Solari Covenant | Institutional and political; affected by civic decisions, treatment of Covenant property, and alliances with nobility |
| **The Grove Keepers** | The Old Ways | Decentralized; affected by environmental choices, treatment of sacred groves, and relations with elven communities |
| **The Ancestor Speakers** | The Ancestors' Path | Clan-linked; clan-specific sub-reputation feeds into tradition-wide standing; dwarven and Highlands communities treated separately |
| **The Veiled Archivists** | The Veiled Order | Information-sensitive; affected by what the player does with knowledge the Order shares, and whether they expose or protect Order members |

Standing with one order does not transfer to others. The Solari Covenant and the Old Ways have significant historical tension — high standing with one creates a small baseline penalty with the other unless the player actively manages both relationships.

> Full religion definitions: [`docs/world/religions.md`](../world/religions.md)

### Vampire Houses (detail)

Three houses are tracked independently. Standing with one does not transfer to the others — and because the houses are in permanent, low-intensity competition, gaining significant standing with one may create minor penalties with the others who notice the relationship. Each house tracks reputation on the standard -100 to +100 scale, but each uses a distinct tier model that reflects its internal culture. Standing with a house is not just a number; it determines which personnel will deal with you, which information they share, and what they can offer.

> Full house definitions: [`docs/world/vampire_houses.md`](../world/vampire_houses.md)

**Founding Houses:** the seven Founding Houses (Noctis, Valenor, Draven, Seraphe, Morcant, Kaelor, Vesper — see [`docs/world/factions/vampire_houses/HOUSE_PROFILES.md`](../world/factions/vampire_houses/HOUSE_PROFILES.md)) do **not** have implemented reputation tracks. They use narrative standing bands managed by the AI Director until individual tier tables are authored. Writers must not assume system-tracked reputation exists for them.

---

#### House Vetharis — Reputation Tiers

*Cassiel's philosophy: information is the only real power. Reputation with Vetharis reflects how much of that power the house is willing to share — and how much risk Cassiel is willing to accept by continuing the relationship.*

**Negative tiers:**

| Tier | Range | Character |
|---|---|---|
| **Marked** | -100 to -51 | Vetharis considers the player an active liability. Agents work through entirely legitimate channels — institutional complaints, quiet discrediting, doors closed without explanation — to limit the player's access and credibility. No open confrontation. The player will not know they are being managed. |
| **Suspect** | -50 to -21 | Vetharis will not work with this player. Information that would otherwise be available through institutional contacts goes quiet. Vetharis-placed assets who would normally be accessible decline meetings or become suddenly unavailable. |

**Neutral tier:**

| Tier | Range | Character |
|---|---|---|
| **Unregistered** | -20 to +20 | The player has not entered Vetharis's meaningful awareness. No active relationship; no active hostility. |

**Positive tiers:**

| Tier | Range | What it unlocks |
|---|---|---|
| **Operative Tier** | +21 to +40 | Established by completing *The Aldric Hourne Problem*. The player is a known quantity — capable, not yet proven fully reliable. **Unlocks:** access to a Vetharis information broker in the Capital Province; one piece of non-public intelligence per campaign arc (current events, institutional movements, faction activities not visible through other channels). |
| **House Tier** | +41 to +65 | Established by completing *The Impatient Ones* and demonstrating continued discretion. The house considers the player a reliable operational asset. **Unlocks:** Vetharis agents provide light field assistance on request (a contact opened, a record retrieved, a name confirmed); access to Vetharis-placed assets in institutional positions for information that would require weeks to obtain through other means; awareness of Impatient Faction operations in the player's region (useful for conflict avoidance). |
| **Cassiel Tier** | +66 to +100 | The rarest Vetharis standing. Cassiel engages with the player personally rather than through intermediaries. This tier reflects trust in the most specific Vetharis sense: Cassiel believes the player's judgment about information can be relied upon. **Unlocks:** Cassiel's direct read of the political landscape — his analysis of which institutions are Corruption-affected, which are salvageable, and which are already lost; access to Vetharis's assessment of the other two houses' current positions; Cassiel's personal intelligence on a named subject of the player's choice per arc. |

**The Impatient Faction sub-track:**

Interactions with Sera Vaine and the Impatient Faction create a parallel track that can diverge from the Cassiel Tier without fully collapsing house standing. High Impatient Faction standing opens access to Sera's independent operational network; high Cassiel standing may restrict this. The AI Director uses this divergence to create situations where the player must choose which tier of Vetharis relationship to prioritize.

**Cross-house effects:**
- Gaining House Tier or Cassiel Tier standing with Vetharis creates a -5 to -10 penalty with Drakmor (they observe the player working in Cassiel's orbit and adjust their assessment accordingly)
- High Vetharis standing does not automatically affect Soleth — the Archivist tracks the player's handling of information, not their political associations — but Cassiel may use high Vetharis standing players as intermediaries in the rare moments he communicates with Soleth

---

#### House Drakmor — Reputation Tiers

*Morreth's philosophy: the world respects strength. Reputation with Drakmor reflects demonstrated capability and operational value. There is no social navigation here — only the record.*

**Negative tiers:**

| Tier | Range | Character |
|---|---|---|
| **Hunted** | -100 to -51 | The player has directly damaged Drakmor operations, territory, or military interests in a way Morreth considers requiring a response. Drakmor forces in the Frontier are actively hostile; Expansionist-controlled checkpoints will not allow passage; the player's name circulates in the Frontier mercenary circuit as someone Drakmor wants found. |
| **Avoided** | -50 to -21 | Drakmor will not contract the player. Frontier passage through Drakmor-adjacent territory is subject to increased scrutiny. Old Guard operators who encounter the player are professionally cold. No active pursuit; no cooperation. |

**Neutral tier:**

| Tier | Range | Character |
|---|---|---|
| **Unregistered** | -20 to +20 | The player has not crossed into Drakmor's territory in a meaningful way, or has been present but performed below the threshold that earns registration. |

**Positive tiers:**

| Tier | Range | What it unlocks |
|---|---|---|
| **Contractor Tier** | +21 to +40 | Established by completing *The Fang-Hold Ultimatum*. The player is a known operational asset — competent, useful for specific jobs. **Unlocks:** access to Drakmor supply caches in the Frontier (consumables, basic equipment, reliable resupply along supply corridors); one piece of military intelligence per arc (territorial threats, Corruption-influenced incursions in the region, Expansionist operations the player should be aware of); basic safe passage through Drakmor-recognized Frontier territory. |
| **Field Rank Tier** | +41 to +65 | Established by sustained operational value — multiple completed jobs, or one job with unusually clean results. Morreth considers the player a reliable long-term asset rather than a one-contract hire. **Unlocks:** Old Guard operators are willing to work alongside the player on joint operations; Expansionist-held checkpoints are non-hostile and provide information about what is moving through their territory; Morreth's command structure treats the player as a party with standing in Frontier disputes — their word carries weight in the mercenary circuit. |
| **Morreth Tier** | +66 to +100 | Morreth deals with the player directly. This is not warmth; it is professional recognition that the player is operating at a level that warrants her personal attention. **Unlocks:** direct consultation with Morreth on territorial matters; the ability to influence Drakmor territorial decisions at the margin (where a road is consolidated, which settlement is prioritized, whether an Expansionist advance is officially sanctioned); Morreth's read on the current Corruption threat in the Frontier — where it is advancing, what it is disrupting, what Drakmor cannot yet handle. |

**The Hallec personal loyalty sub-track:**

Sergeant Hallec's standing with the player operates as a parallel personal loyalty track independent of formal house reputation. Completing *The Soldier Who Remembered* privately creates Hallec standing without necessarily creating Morreth Tier standing. High Hallec standing unlocks his four centuries of institutional memory — specific knowledge about Drakmor's political history, vulnerabilities, and the reasoning behind decisions that official Drakmor channels would not document. This track can coexist with any positive Drakmor tier or can exist in tension with it (a player who told Morreth about Hallec's private request has higher formal Morreth standing and lower personal Hallec standing simultaneously).

**Cross-house effects:**
- Gaining Field Rank or Morreth Tier standing creates a -5 penalty with Vetharis (Cassiel tracks who works with Morreth's military apparatus and adjusts his information-sharing accordingly)
- High Drakmor standing has no automatic Soleth effect, but Drakmor's territorial presence in the Frontier and Iron Peaks creates friction with Soleth archive sites — the player may face situations where advancing Drakmor interests damages Soleth assets

---

#### House Soleth — Reputation Tiers

*The Archivist's philosophy: knowledge is the only power that compounds. Reputation with Soleth reflects how deeply the player can be trusted with what the house knows — and how much of the archive the Archivist judges them ready to hold.*

**Negative tiers:**

| Tier | Range | Character |
|---|---|---|
| **Closed** | -100 to -51 | The player has handled Soleth-adjacent historical information in a way the Archivist considers irreversible — broadcasting it publicly, selling it to a rival faction, or giving it to the Mages Guild without authorization. All Soleth paths are permanently unavailable. Preservationist operatives will work to limit the player's access to historical sources through other channels. This is not punishment; it is the Archivist concluding the player cannot be trusted to hold what they know. |
| **Information Risk** | -50 to -21 | The player has been careless — not catastrophically, but enough that Soleth treats them as a managed risk. Operatives decline missions. The scholar contact who made initial introductions is no longer available to facilitate meetings. The Archivist is watching but not engaging. |

**Neutral tier:**

| Tier | Range | Character |
|---|---|---|
| **Unregistered** | -20 to +20 | The player has not crossed the knowledge threshold that triggers Soleth's observation. They do not exist to Soleth in any meaningful operational sense. |

**Positive tiers:**

| Tier | Range | What it unlocks |
|---|---|---|
| **Operative Tier** | +21 to +40 | Established by completing *What the Desert Remembers*. The player has demonstrated sufficient discretion that Mira Deln is willing to continue working with them. **Unlocks:** Mira Deln as an ongoing contact; one piece of historical intelligence per arc drawn from Soleth's operational archive — specifically, information that answers a current campaign question with documented historical precedent; awareness of which Sol Kareth sites are currently under Soleth interest (useful for avoiding complications). |
| **Archive Tier** | +41 to +65 | The Archivist has reviewed the player's handling of the *What the Desert Remembers* outcome and determined that deeper collaboration is warranted. **Unlocks:** access to specific secondary archive materials — not the deepest holdings, but documents that confirm or extend what the player already knows about the Corruption or the pre-Forgetting world; Preservationist cooperation on specific research questions; access to Soleth-known site locations in the Iron Peaks and Sol Kareth for investigation; the Archivist communicates through Mira Deln with deliberate regularity — information the player receives is no longer incidental, it is considered. |
| **Archivist Tier** | +66 to +100 | The highest Soleth standing. The Archivist engages personally. This tier is achieved only through *The Fraying Edge* with full disclosure — and requires the player to have handled the Keth-Dural complex in a way the Archivist considers the correct outcome. **Unlocks:** direct contact with the Archivist; access to primary archive materials on the god's prison and the mechanics of the seal; one piece of direct knowledge from the Remnant's account — specific, verifiable, and not available through any other source; the Great Library arrangement path — the Archivist authorizes the player to access the Sealed Archive through the standing research arrangement, opening the Soleth Accounting and related materials to the player for the first time. |

**The Weaponizer sub-track:**

Players who deal with Weaponizer-aligned operatives (including Voss Theranel) build a parallel Weaponizer sub-track. High Weaponizer sub-track standing opens different access than formal house standing: the Weaponizers will share materials the Preservationists would withhold, but their information comes with the Weaponizer's interpretation already attached, and sharing it further creates the internal political consequences described in *vampire_houses.md*. The Archivist is aware of who has Weaponizer sub-track standing and factors this into his assessment of the player — high Weaponizer sub-track standing alongside high formal Soleth standing is the combination he finds most interesting and most worth watching.

**Cross-house effects:**
- High Soleth standing has no automatic effect on Vetharis, but players with Archivist Tier standing who share specific categories of information with Vetharis will find Cassiel's interest in maintaining the relationship increases significantly
- High Soleth standing and high Drakmor standing are mechanically compatible but narratively in tension — the player who works for both must manage situations where Drakmor's territorial presence threatens Soleth archive sites

---

### Cross-House Reputation Dynamics

The three houses track each other's relationships with outside parties. A player who has achieved standing with two houses simultaneously is a player that all three houses are watching carefully.

| Combination | Effect |
|---|---|
| High Vetharis + High Drakmor | Cassiel reads this as the player working both sides of the military-political divide. He becomes more guarded. Morreth reads it as the player being a political operator. She becomes more transactional. Neither house terminates the relationship — the player's multi-house access is itself valuable — but both provide less than they would to an exclusive partner. |
| High Vetharis + High Soleth | The most stable combination. Cassiel values Soleth's knowledge; the Archivist values Cassiel's institutional reach. A player trusted by both is occasionally used as a channel between them for things neither house wants to communicate directly. This is the most significant political position a player can occupy in vampire politics. |
| High Drakmor + High Soleth | The most fraught combination. Drakmor's Frontier operations and Iron Peaks presence are in direct physical conflict with Soleth archive sites. A player maintaining both relationships will face situations where one house's interests directly damage the other's. How they navigate this determines which house considers them ultimately reliable. |
| All Three Houses | Theoretically possible. Practically, achieving Morreth Tier, Cassiel Tier, and Archivist Tier simultaneously requires the player to have navigated multiple direct conflicts between house interests. This is the campaign's most politically consequential player position. All three lords are aware of this player. None of them fully trust them. All of them consider the relationship worth maintaining. |

Additional factions may be added as the world is developed. Each new faction with meaningful player interaction should have its own reputation track.

---

## Reputation Consequences

### High Reputation

| Benefit | Description |
|---|---|
| **Unique quests** | Questlines only available to those trusted by the faction |
| **Discounts** | Reduced prices at faction-affiliated merchants |
| **Allies** | Faction members may provide active assistance |
| **Special dialogue** | New conversation options reflecting established trust |
| **Political influence** | Ability to affect faction decisions and policies |
| **Safe passage** | Movement through faction territory without hostility |

### Poor Reputation

| Consequence | Description |
|---|---|
| **Increased prices** | Faction-affiliated merchants charge more or refuse service |
| **Denied services** | Certain services, training, or information unavailable |
| **Assassination attempts** | Faction sends agents after the player |
| **Hostile settlements** | Faction-controlled towns become dangerous to enter |
| **Lost questlines** | Questlines become permanently unavailable |
| **Pursuit** | Rival factions actively hunt the player across the campaign |

---

## Design Notes

### Reputation Should Feel Meaningful

Reputation changes must be large enough that players feel them. A reputation system where standing never visibly shifts is not a reputation system — it is a hidden score.

### Diplomacy as Gameplay

High reputation with a faction should open doors that violence would permanently close. Some questlines, information, and alliances only become available through sustained positive standing.

### Campaign Variation

Different campaigns may start with different baseline reputations depending on how the AI Director seeds the campaign. A campaign with heavy vampire activity may begin with vampire houses already suspicious of the player based on world events before the campaign started.

---

## Technical Notes

The existing `world_state["factions"]` dict tracks four factions (`kingdom`, `shadow_cult`, `mages_guild`, `rebels`) with reputation values from -100 to 100.

**Design target:** Expand this to track all confirmed reputation factions individually. Each new faction entry follows the same -100 to 100 model with `hostile`, `neutral`, `friendly`, and `allied` tiers.

See [`docs/GAME_BIBLE.md — Factions`](../GAME_BIBLE.md) for current technical implementation.

⚠️ **NOT YET IMPLEMENTED** — The expanded reputation system (goblin tribes, vampire houses, Adventurers Guild, Religious Orders, Mercenary Companies) is a design target. Only the four factions in `world_state["factions"]` are currently tracked.

---

## Related Systems

- `faction_manager.py` — current faction data and evolution
- `world_state.py` — `world_state["factions"]` for current reputation values
- [`docs/world/WORLD_BIBLE.md`](../../docs/world/WORLD_BIBLE.md) — faction design philosophy
- [`docs/GAME_BIBLE.md`](../GAME_BIBLE.md) — Factions section

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Created — reputation system design philosophy established |
| 2026-07-31 | Added vampire house reputation tracks — three houses with named tiers, per-tier unlocks, contact sub-tracks (Cassiel Tier / Hallec personal loyalty / Weaponizer), and cross-house reputation dynamics table |
