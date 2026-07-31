# Living Chronicle — Journal System

> **Canon Status:** CONFIRMED — established 2026-07-31.  
> **Authority:** This document defines the canonical Journal system: its design philosophy, section structure, and how it serves both the player and the World State system. All future UI, content, and AI Director work involving player-facing information must align with these principles.  
> **Cross-references:** [`docs/GAME_BIBLE.md`](../GAME_BIBLE.md) · [`docs/systems/world_state.md`](world_state.md) · [`docs/lore/GREAT_LIBRARY.md`](../lore/GREAT_LIBRARY.md)

---

## Design Philosophy

The Journal is a **living archive** inspired by the Great Library.

It does not display information the player already knows. It expands naturally as the player discovers the world — entries that are empty at the start of the campaign grow denser, more nuanced, and more cross-referenced as the player learns more. The Journal is not a menu. It is a record of a journey.

> The goal is for players to open the Journal in the final act of the campaign and be able to read the record of who they were at the beginning — and see how far they have come.

The Journal answers the question: **"What do I know about this world?"**

It is intentionally separated from the Character Menu (which answers "Who am I?") and the Statistics screen (which answers "What have I accomplished?").

---

## World State

The Journal's most significant section. It tracks the overall condition of civilization as the player progresses through the campaign.

### Design Principle: Not a Morality System

The World State is not a moral ledger. It does not track whether the player is good or evil. It tracks whether civilization is stronger or weaker for the player having been in it.

Helping people, protecting knowledge, resolving conflicts, and preserving communities all contribute toward slowing the Long Decline. The Corruption cannot be permanently stopped — but the player can strengthen civilization's ability to endure it, buying the world time.

Ignoring suffering allows the Decline to advance. The World State records what the player actually did, not what they intended.

### Display Philosophy

World State is **not displayed constantly**. There is no persistent meter, no percentage, no alignment indicator. Players must intentionally open the Journal to view it.

The World State is expressed through **descriptive assessments**, not numbers:

| Assessment | Meaning |
|---|---|
| **Flourishing** | Civilization is stronger than at the campaign's start; communities are supported, knowledge is preserved, conflicts are resolved |
| **Stable** | No significant regression; the player is holding the line |
| **Holding** | The Decline is advancing, but slowly; the player's actions are buying time |
| **Strained** | Civilization is under visible pressure; communities are struggling |
| **Declining** | The Decline is measurably advancing; the player's impact has not been sufficient to hold it |
| **Fading** | Significant civilizational loss; institutions are failing; communities are isolated |
| **On the Brink** | The Decline is near-critical; what the player does next will determine what survives |

These assessments should feel **observational rather than mechanical** — like a scholar's assessment of current conditions, not a game score.

### World State Journal Contents

The World State section of the Journal includes:

- **Current overall assessment** — the descriptive tier
- **Regional observations** — how specific regions are faring; which communities the player has helped or ignored
- **Scholar assessments** — brief entries from in-world scholars and Keepers who have observed the player's actions from the outside; these feel like primary source documents, not UI text
- **Communities helped** — a record of specific communities the player has strengthened or preserved
- **Knowledge preserved** — documentation of lore, archives, traditions, and wisdom the player protected from loss
- **Major historical developments** — significant world events the player witnessed or caused, framed as historical record rather than quest completion

> **Writing guidance:** World State entries should be written in the voice of a knowledgeable in-world observer — a Keeper of Ancestors reflecting on the Iron Peaks, a Great Library archivist cataloguing what was preserved, a frontier settler describing what the party did for a community. Never write these as game feedback. Write them as documents.

---

## Bestiary

Creature entries that expand over time as the player encounters, studies, and survives different enemies.

### Entry Progression

**Before encounter:**
> *Unknown creature. No observations recorded.*

**After first encounter (survived):**
> Basic physical description. Combat behavior observed. Region noted.

**After multiple encounters or scholarly research:**
> Habitat. Behavioral patterns. Weaknesses discovered. Known subspecies. Historical notes. Relationship to the Corruption (where applicable).

The Bestiary rewards players who pay attention — both in combat and in finding in-world documents about creatures. Some entries can only be completed by finding specific texts, not just by fighting the creature repeatedly.

---

## Flora & Fauna

A reference section that expands as the player explores different regions.

Entries include:
- Plant and animal names and descriptions
- Crafting material uses (which flora yields which reagents)
- Medicinal properties (especially relevant to Cooking and Alchemy systems)
- Regional distribution — where to find specific ingredients
- Cultural significance — how different peoples use or regard the plant or animal

Regional cuisine entries reference Flora & Fauna for ingredient origin context. Eleanor's passive skill (preserving rare magical reagents) creates rarer Flora & Fauna entries that would otherwise be unrecoverable.

---

## People

Records of significant NPCs the player has met, with entries that update throughout the story.

Each People entry includes:
- Name and role
- Biographical notes (builds as the player learns more)
- Current relationship / trust level
- Quest progression associated with this person
- Notes on what the player has done with or for this person — written as record rather than stat

People entries are not complete at first meeting. They grow as the player spends time with, questions, or investigates the person. An NPC the player encounters once has a brief entry. An NPC who becomes central to a questline has an entry that evolves across the campaign.

---

## Locations

Entries for cities, ruins, temples, dungeons, and landmarks discovered during the campaign.

Historical discoveries gradually expand each entry. A ruin the player visits early in the campaign may have a sparse entry; after the player has investigated it thoroughly, found its texts, and understood its historical significance, the entry becomes a miniature historical document.

Entry categories:
- Physical description
- Known history (grows as the player learns more)
- Current state (occupied, abandoned, contested, Corruption-affected)
- Notable figures associated with the location
- Player's recorded actions there

---

## History

The player's developing understanding of Elyndor's history, organized by the Four Ages framework.

Sections:
- **The Four Ages** — Age of Awakening, Age of Harmony, Age of Sundering, Age of Restoration; entries expand as the player discovers historical records
- **The First Empire** — what the player knows about the Empire and First Council; incomplete at the start
- **The Great Library** — the Library's history and the player's relationship with it
- **The Divine Chorus** — what the player has learned about the Chorus and its limits
- **The Forgotten Eighth** — this section begins locked; entries appear as the player uncovers evidence

> **Design principle:** Historical discoveries should **expand existing entries** rather than overwrite previous understanding. The player's developing comprehension is part of the record. An early entry might reflect incomplete or incorrect understanding; a later annotation corrects or deepens it. The history the player carries is the history they earned.

---

## Recipes

Cooking recipes the player has learned through the campaign.

Recipes unlock through:
- Exploration (found in kitchens, libraries, travelers' packs)
- Merchants (some regional cooks sell recipes)
- Quests (completing a questline for a community may unlock their traditional recipes)
- Companions (companions may share recipes that reflect their backgrounds)

Each recipe entry includes:
- Name
- Ingredients required
- Prepared effect (healing amount, stat bonus duration and magnitude)
- Regional origin — which culture or community this recipe comes from
- Brief cultural note — why this dish matters where it comes from

Regional recipes reinforce worldbuilding. A dwarven clan's winter stew has a different entry flavor than a halfling river-town's trading feast.

---

## Alchemy

Potion formulas the player has learned.

Formula entries include:
- Potion name and appearance
- Required reagents
- Effect (mechanical) and duration
- Source of the formula (who or what the player learned it from)
- Crafting notes — any relevant observations about preparation

---

## Relationship to Other Menus

The Journal is one of four player-facing information systems. Each answers a different question:

| Menu | Question Answered |
|---|---|
| **Journal** | What do I know about this world? |
| **Character Menu** | Who am I? |
| **Party Menu** | Who is traveling with me? |
| **Statistics** | What have I accomplished? |

**The Journal and Statistics are explicitly separated.** Statistics track player performance metrics (enemies defeated, quests completed, distance traveled). The World State tracks what happened to the world. These systems should **never overlap** — a player who has defeated a thousand enemies may still find the world Declining if they ignored the suffering around them.

---

## UI Integration

The Journal is accessible via the **Quick Access Wheel** during gameplay — it is one of the seven most frequently needed menus and should be reachable without interrupting the experience. See [`docs/GAME_BIBLE.md`](../GAME_BIBLE.md) — UI Philosophy section.

---

## Document History

| Date | Change |
|---|---|
| 2026-07-31 | Created — Living Chronicle system defined: design philosophy, World State section (descriptive tiers, not morality), Bestiary, Flora & Fauna, People, Locations, History, Recipes, Alchemy; relationship to Character Menu, Party Menu, Statistics documented |
