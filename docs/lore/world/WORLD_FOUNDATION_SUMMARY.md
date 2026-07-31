# World Foundation Summary

> **Canon Status:** Reference document — read-only compilation. No new lore established here.  
> **Purpose:** Consolidates all world canon from across the repository into a single indexed reference for writers and designers. Organized into three tiers: what is established, what is partially established, and what has not yet been defined.  
> **Authority:** This document reflects the sources listed below. It does not override them. In any conflict between this summary and a source document, the source document is authoritative.  
> **No lore invented here.** Every entry traces to an existing canonical source. Items without a source citation are not included.

---

## Source Documents Reviewed

| File | Content Area |
|---|---|
| `docs/lore/HISTORY_BIBLE.md` | Seven Ages narrative framework |
| `docs/lore/TIMELINE.md` | Concise developer chronology |
| `docs/lore/ARCHITECTS.md` | Pre-Chorus builders |
| `docs/lore/DIVINE_CHORUS.md` | Chorus philosophy and structure |
| `docs/lore/DIVINE_CHORUS_PHILOSOPHY.md` | Expanded Chorus philosophy, Five Tensions |
| `docs/lore/CANON_RULES.md` | Immutable design principles |
| `docs/lore/IMPERIAL_CAPITAL.md` | Capital city, institutions, districts |
| `docs/lore/GREAT_LIBRARY.md` | Archive collections, Order of Archivists |
| `docs/lore/FIRST_TEMPLE.md` | Oldest temple, sealed sub-structure |
| `docs/world/WORLD_BIBLE.md` | Six canonical regions, factions overview |
| `docs/world/RACES.md` | Six playable races |
| `docs/world/vampire_houses.md` | Three vampire houses |
| `docs/world/religions.md` | Four religious traditions and three cults |
| `docs/world/goblin_tribes.md` | Three goblin tribes |
| `docs/world/cults.md` | Three named cults |
| `docs/world/covenant_inquisitors.md` | Inquisitor faction |
| `docs/systems/world_regions.md` | Technical region system |
| `docs/GAME_BIBLE.md` | Overall design reference |
| `docs/CAMPAIGN_DESIGN.md` | Campaign structure and core premise |
| `elyndor/world/world_overview.md` | World name, geographic scope |
| `elyndor/magic/MAGIC_BIBLE.md` | Primordial Magic, full Chorus profiles |
| `elyndor/history/HISTORY_BIBLE.md` | Four-Age historical framework |
| `elyndor/history/the_eighth.md` | The Forgotten Eighth's full account |
| `elyndor/history/the_corruption.md` | Corruption mechanics and faction effects |
| `elyndor/ancient_legends/aurelia_sunstrider.md` | Ancient legend: Aurelia |
| `elyndor/ancient_legends/valen_ashfall.md` | Ancient legend: Valen |
| `docs/world/GEOGRAPHY_LANDMARKS.md` | All named geographic landmarks — lakes, mountains, swamps, plains, coastlines, caves, ruins |

---

## ⚠️ Designer Flag: Dual Historical Frameworks

Two documents describe the history of Elyndor using different frameworks and terminology. Both are marked as canonical. They are reconcilable — the periods map onto each other — but they use different names, different period boundaries, and different counts.

| Framework | Source | Ages |
|---|---|---|
| **Seven Ages** | `docs/lore/HISTORY_BIBLE.md` | Awakening · Discovery · Unity · Long Decline · Sundering · Restoration · Present |
| **Four Ages** | `elyndor/history/HISTORY_BIBLE.md` | Creation · Kingdoms · Wars · Shadows |

Rough correspondence: The Four-Age model's Age of Creation spans roughly the Seven-Age model's first four ages (Awakening through Long Decline plus the Sundering). The Age of Kingdoms corresponds to the Age of Restoration. The Ages of Wars and Shadows correspond to the Second and Third Ages of the campaign-facing framework.

**Neither framework should be treated as wrong.** Content using either model is valid. **A designer decision is needed** on whether to consolidate these into a single canonical numbering system, adopt one as the "public-facing" framework and one as the "scholarly" framework, or explicitly canonize both as co-existing scholarly traditions. Until that decision is made, both are confirmed canon.

---

---

# SECTION I — CONFIRMED CANON

Everything in this section is established in at least one canonical source document. These facts may be used freely in all content.

---

## World Identity

- **World name:** Elyndor
- **Setting scope:** A single unnamed continent. The game takes place entirely on this continent.
- **Total number of continents:** NOT YET DEFINED (see Section III). The world overview explicitly marks this as intentionally open.
- **Core premise:** An ancient god remains imprisoned beneath the world. Its prison has been weakening for a thousand years. As its influence spreads, the world falls into chaos through a force known as the Corruption. The player gradually uncovers the truth behind this ancient threat while exploring the continent.

---

## Geography — Regions

Six canonical regions exist. Their lore descriptions are established in `docs/world/WORLD_BIBLE.md`. Their in-engine technical definitions are in `docs/systems/world_regions.md`, which notes that detailed in-code region lore is **not yet defined** at the systems layer — the descriptions below come from lore documents only.

| Region | Summary |
|---|---|
| **The Frontier** | Open wilderness and contested territory. Primary goblin tribe territory. Most dangerous travel. Cinderhold (Ashfire tribe) is in the central/southern Frontier. Fang-Hold (Stonefang tribe) is on an eastern rocky promontory. |
| **The Great Forest** | Ancient woodland. Mossroot goblin tribe maintains the Deep Warren (underground forest refuge) here. The First Grove — sacred to the Old Ways — exists somewhere in the Great Forest, location known only to senior practitioners. |
| **The Iron Peaks** | Mountain range. Dwarven civilization concentrated here from the Second Age onward. Hall of First Forging (Tharok's ancient temple) is deep within the Iron Peaks. House Soleth has an archive in the deep passes — one site has gone silent. |
| **The Frozen Highlands** | Cold northern territory. Ice caves and ancient fortresses exist here. No specific sites named in canon. |
| **Sol Kareth** | Desert/arid region that emerged as a trade and learning center in the Second Age. Contains oasis cities (number and names not yet established). House Soleth has two excavation sites sealed in Sol Kareth. |
| **The Capital Province** | Political center of the continent since the Second Age. Contains the Imperial Capital, the dominant city on the continent. |

---

## Geography — Named Settlements

| Settlement | Location | Notes |
|---|---|---|
| **The Imperial Capital** | Capital Province | Largest city on the continent. Founded in the Second Age. Never given a proper name — referred to only as "the Imperial Capital" or "the Capital." |
| **Fang-Hold** | Eastern Frontier, rocky promontory | Stonefang goblin tribe settlement |
| **Deep Warren** | Underground, Great Forest | Mossroot goblin tribe settlement |
| **Cinderhold** | Central/southern Frontier | Ashfire goblin tribe settlement; built in a former ruin |

No other named settlements are established in canon. All other inhabited locations are described by region or by type only.

---

## Geography — Named Landmarks

Full lore entries (2–4 sentences each) are in `docs/world/GEOGRAPHY_LANDMARKS.md`. The table below is the index. ⚠️ See that document for two naming disambiguations: **The Deep Warrens** (Iron Peaks cave) ≠ **Deep Warren** (Mossroot goblin settlement); **Temple of the First Dawn** (Solaryn ruin) ≠ **First Temple** (oldest Chorus temple).

### Lakes

| Name | Region |
|---|---|
| **Serenity Lake** | Great Forest / Frontier border |
| **Frostmere** | Frozen Highlands |
| **Stonewater Lake** | Iron Peaks |

### Iron Peaks — Named Features

| Name | Type |
|---|---|
| **Mount Ironheart** | Highest peak; navigational landmark; oral tradition anchor |
| **Skyspire** | Northeastern peak; anomalous geometry; dwarves avoid it |
| **Black Anvil Range** | Western sub-range; dark stone; location of the oldest dwarven forges |
| **Thundercrest Range** | Northern sub-range; extreme lightning activity |
| **Iron Gate Pass** | Primary cross-continental mountain pass |

### Swamps

| Name | Region |
|---|---|
| **Blackfen** | Frontier (southwestern) |
| **Mistfen** | Great Forest / Frontier border |

### Plains

| Name | Region |
|---|---|
| **Golden Plains** | Capital Province / Frontier border |
| **King's Meadow** | Capital Province (formal Crown-maintained grassland) |
| **Wind Plains** | Frontier (northern) |
| **Sunfields** | Capital Province (primary agricultural land) |

### Sol Kareth — Named Landmarks

| Name | Type |
|---|---|
| **Sea of Glass** | Vast fused-silica desert expanse; origin unknown |
| **Scorpion Dunes** | Highest dune field; seasonally shifting; conceals ruins |
| **Whispering Sands** | Acoustic basin; traditional neutral ground for negotiations |
| **Oasis of Kings** | Largest oasis; neutral council site; oldest recorded meeting place |
| **The Broken Obelisk** | Partially translated boundary marker; top section fallen |

### Frozen Highlands — Named Locations

| Name | Type |
|---|---|
| **Icewind Valley** | Wind-channeling valley; partial ice preservation |
| **Crystal Icefields** | Geometric ice formations; non-random pattern |
| **White Fang Ridge** | Territorial boundary ridge; navigational landmark |
| **Frozen Crown** | Far-northern circular stone/ice formation; pre-settlement origin |

### Coastlines

| Name | Location |
|---|---|
| **Sapphire Coast** | Southern coast (near Capital Province and Great Forest) |
| **Storm Coast** | Northern coast (near Frozen Highlands and Frontier) |
| **The Shattered Coast** | Western coast (fragmented geology; remote) |
| **Emerald Bay** | Southern coast (near Great Forest; primary maritime trade entry) |

### Caves & Dungeons

| Name | Region |
|---|---|
| **Hollow Deep** | Great Forest |
| **Forgotten Halls** | Iron Peaks (lost dwarven complex) |
| **Iron Delve** | Iron Peaks (former mining operation) |
| **The Deep Warrens** | Iron Peaks (natural, pre-dwarven cave network) |
| **Shadow Cavern** | Frontier (eastern) |
| **Ember Hollow** | Sol Kareth (geothermal cave complex) |
| **Whispering Caves** | Sol Kareth (near Whispering Sands) |
| **Titan's Tomb** | Sol Kareth (oversized burial complex) |

### Ruins

| Name | Region |
|---|---|
| **The Fallen City** | Frontier (unnamed ancient city) |
| **Old Aranor** | Great Forest (pre-existing elvish settlement) |
| **Sunken Temple** | Sapphire Coast (partially submerged; pre-dates four religions) |
| **Kingsfall** | Frontier (northern; battlefield and fortification) |
| **Ashwatch Keep** | Frontier (near Cinderhold / Ashfire territory) |
| **Grey Fortress** | Frozen Highlands (southern approach) |
| **Temple of the First Dawn** | Frontier / Capital Province border (ancient Solaryn temple) |
| **The Forgotten Citadel** | Frozen Highlands (far north; pre-dates Grey Fortress) |

---

## Geography — The Imperial Capital (Districts)

| District | Notable Institutions |
|---|---|
| **Crown District** | Seat of political power |
| **Academic Quarter** | Great Library; Mages Guild headquarters; universities; museums; translation halls; observatory; Scholar's District |
| **Temple District** | Radiant Spire (Solaryn's temple, dominant presence) |
| **Merchant Quarter** | House Vetharis surface operations |
| **Lower City** | General population; Corruption manifests most visibly here |

---

## Geography — Ancient Temple Sites (Divine Chorus)

Five of the seven Chorus members have named or located ancient temple sites. Two do not.

| God | Temple Name | Location |
|---|---|---|
| **Solaryn** | Radiant Spire | Capital Province (within the Imperial Capital's Temple District) |
| **Neressa** | Sanctuary of Returning Tides | Rocky coast, half-submerged at high tide |
| **Tharok** | Hall of First Forging | Deep within the Iron Peaks |
| **Zephyros** | The High Crossing | Windswept mountain pass, open to sky |
| **Sylvara** | The First Grove | Somewhere in the Great Forest; precise location known only to senior Old Ways practitioners |
| **Morvel** | ⚠️ NOT YET NAMED | — |
| **Eldris** | ⚠️ NOT YET NAMED | — |

---

## The Divine Chorus

### Identity and Role

The Divine Chorus are seven primordial stewards of Creation — not a conventional pantheon competing for worship, but cosmic beings whose purpose is the maintenance of reality itself. They maintain Primordial Energy, cosmic balance, the Final Verse, and the stability of existence. They intervene directly only when reality itself is threatened.

### The Seven Members

| God | Title | Element | Domain |
|---|---|---|---|
| **Solaryn** | The First Flame | Fire | Civilization, order, light, ambition, the courage to build |
| **Neressa** | The Endless Tide | Water | Healing, compassion, life, grief, the patience to endure |
| **Tharok** | The Unbroken Foundation | Earth | Craft, endurance, legacy, the obligation to build well |
| **Zephyros** | The Wandering Wind | Wind | Travel, freedom, change, possibility, the courage to leave |
| **Sylvara** | The Deep Root | Nature | Growth, seasons, cycles, the living world, balance |
| **Morvel** | The Patient Witness | Shadow | Death, transition, memory, the threshold, clarity |
| **Eldris** | The Long Thread | Fate | Lineage, continuity, obligation, time's thread |

### What the Chorus Does Not Do (Immutable Rules)

No canonical content may feature the Chorus doing any of the following:
- Governing kingdoms or building political structures
- Choosing rulers, dynasties, or leaders
- Manipulating wars or political outcomes
- Selecting individuals for divine purposes
- Issuing prophecies naming heroes
- Communicating personal divine instructions to individuals
- Intervening in mortal governance of any kind

> **For content creators:** No NPC, quest, or codex entry may credibly claim that the Chorus sent a vision with specific instructions, chose a character for a purpose, or intervened in a political outcome. Any such claim in content is either the character's mistaken belief, deliberate manipulation by another party, or a Corruption-adjacent phenomenon — never literal truth.

### The Teaching of Balance

The central teaching shared across all four major religious traditions:

> *"No flame burns without air. No river flows without stone. No mountain stands without time. No life exists without balance."*

No member of the Chorus is more important than another. Each represents something Creation cannot function without.

### The Final Verse

The world's term for death is **the Final Verse**. It is not a location and not an afterlife — it is the moment a soul passes beyond the stewardship of the Divine Chorus. No one knows what follows. Not mortals, not scholars, not mages, and not even the Chorus themselves. The Final Verse is **never answered in canonical content**. Its mystery is intentional and load-bearing.

Morvel's domain includes the Final Verse, but even Morvel does not claim knowledge of what lies beyond it.

### The Five Tensions

The mythology is structured around five unresolved tensions that must never be resolved in canonical content:

| Tension | Meaning |
|---|---|
| **Balance vs. Obsession** | The Eighth's story; the Chorus's restraint after her fall |
| **Acceptance vs. Attachment** | The inability to let go as the source of the world's greatest wound |
| **Wisdom vs. Knowledge** | Understanding that knows its limits vs. knowing that has forgotten why limits exist |
| **Duty vs. Compassion** | The Chorus's impossible choice |
| **Cosmic Perspective vs. Mortal Perspective** | What is lost and gained at each scale; neither is simply right |

---

## The Forgotten Eighth

- There was an eighth member of the Divine Chorus.
- **Her true name has been erased** — not from the world's memory only but from the Chorus's oldest surviving records. It is not to be invented or recovered in canonical content.
- She is referred to as: the Forgotten Eighth, the Absent One, the Fallen Sister, or the goddess of her specific domain in contexts where that domain is relevant.
- She was not older than the rest of the Chorus. She was one of them: a member of the same primordial family, a steward of some elemental aspect.
- Her elemental stewardship is **NOT YET DEFINED** (intentional mystery — see Section III).
- **Her fall:** She spent more time among mortals than any of her siblings. She fell in love with an ordinary mortal. The mortal sang their Final Verse. She could not accept it.
- **Her prison:** "Beneath the world." No specific location given.
- **Her story is a tragedy, not a villain's origin.** She began as the most compassionate member of the Chorus. Her fall resulted from countless small compromises, each justified to herself across centuries.

### The Five Stages of the Fall (Immutable Canon)

1. **Love**
2. **Grief**
3. **Obsession**
4. **Justification** *(the true root — "It had to be done" is when corruption takes hold)*
5. **Hatred** *(she believes the Chorus betrayed her first: "They chose law over love")*

Stage IV is the most important design principle of her arc: Corruption did not overwrite her from outside. It grew from the compromises she chose and then justified.

### The Great Forgetting

- The Chorus erased the Eighth from collective memory as part of the imprisonment.
- The Great Forgetting is the historical period corresponding to this erasure.
- Evidence survives: ancient First Age ruins sometimes depict eight figures rather than seven; sealed or collapsed pre-Forgetting sanctuaries exist; the Chorus's own oldest traditions "whisper" of the Eighth when read carefully.
- The Great Library's Sealed Archive contains restricted materials from before the Forgetting.

### The Chorus's Ongoing Grief

The Chorus did not stop loving the Eighth when they sealed her away. The most ancient records say this clearly. They built the prison with grief, not hatred. Whether the imprisonment was justified — whether the Great Forgetting was mercy or self-protection — is a question the campaign leaves permanently open.

---

## The Architects

- The Architects predate the Divine Chorus. Even the Chorus does not fully understand them.
- **Immutable rules (from `docs/lore/CANON_RULES.md`):**
  - They never appear in canonical content.
  - They never speak.
  - They never become enemies.
  - Their origin is never confirmed.
  - Their existence is intentionally and permanently mysterious.
- Evidence exists as archaeological curiosities: structures that match no known civilization, materials that cannot be explained by known craft, geometries implying an understanding of existence that predates mortal thought.
- **Greatest concentration of evidence:** Beneath the First Temple. The sub-temple Architect structure is permanently sealed and is never resolved in canonical content.
- Architect sites exist "around the world" beyond the First Temple — none named or located in current canon.

---

## The First Temple

- Oldest temple to the Divine Chorus on the continent.
- A sealed Architect structure lies beneath it.
- The sub-structure is **permanently sealed**. There is no canonical path to entering it. This is an immutable design principle — the mystery of what lies beneath is never resolved.

---

## The Great Library

- Located in the Academic Quarter of the Imperial Capital.
- The largest archive on the continent.
- Staffed in part by gnomish archivists (one of the most prominent gnomish populations outside the Iron Peaks).
- Administered by the **Order of Archivists**.

### Collections

| Collection | Access | Contents |
|---|---|---|
| **Open Stacks** | Public | General history, philosophy, geography, natural history |
| **Restricted Archive** | Scholar credentials required | Pre-Forgetting fragments, sensitive political records, documented Corruption cases |
| **Sealed Archive** | Order of Archivists only | Materials from before the Great Forgetting; access almost never granted |

---

## The Corruption

The Corruption does not control minds. It **amplifies existing flaws** — within individuals, societies, and nature. Every virtue, taken beyond its own limits, becomes its corruption.

### Virtue-to-Corruption Mappings (established in canon)

| Virtue | Corruption Expression |
|---|---|
| Love | Possessiveness, obsession |
| Protection | Imprisonment, paranoia |
| Justice | Cruelty, persecution |
| Knowledge | Obsession, recklessness |
| Faith | Fanaticism, zealotry |
| Ambition | Tyranny, exploitation |
| Duty | Rigid inhumanity |

### Campaign Expression Types

| Type | Manifestations |
|---|---|
| **Political** | Civil war; oppressive rulers; assassinations; betrayals |
| **Natural** | Cursed forests; crop failures; wildlife mutation; ecosystem collapse |
| **Religious** | Cult spread; fractured holy orders; ancient temples awakening; religious war |
| **Arcane** | Unstable magic; relic activations; mages losing control; magical disasters |
| **Universal** | Ancient monsters awakening; increasing faction hostility |

Multiple types may appear in a single campaign.

---

## Primordial Magic

- Magic in Elyndor draws on Primordial Energy — the underlying force that the Divine Chorus stewards.
- Seven elemental aspects: **Fire · Water · Earth · Wind · Nature · Shadow · Fate**
- Each aspect is stewarded by one Chorus member (see table above).
- The Eighth's elemental aspect is not defined and not maintained — **NOT YET DEFINED** (see Section III).
- The Sundering reshaped the availability and behavior of Primordial Magic across the world.

---

## Playable Races

Six races are confirmed canonical. All are available as player character options.

| Race | Regional Concentration | Cultural Notes |
|---|---|---|
| **Human** | All regions | Politically dominant across the continent; most diverse in culture |
| **Dwarf** | Iron Peaks (primary) | Civilization centered in Iron Peaks since Second Age |
| **Elf** | Great Forest (primary) | Deep connection to the Old Ways tradition |
| **Halfling** | Central river corridor | **No homeland.** Concentrated along the continent's central river trade network; most integrated into mixed-race urban communities |
| **Gnome** | Iron Peaks + Capital (Academic Quarter) | Iron Peaks is primary cultural homeland; significant presence as archivists in the Capital |
| **Goblin** | Frontier (primarily) | Three distinct canonical tribes; not monolithic |

**Immutable design rules (from `docs/lore/CANON_RULES.md`):**
- No race is inherently superior, divinely favored, or cosmically significant.
- No race rises or falls through any quality of birth — only through its own decisions.

---

## Factions

### Religious Traditions

Four major traditions. All are legitimate paths of worship — none is canonically "correct."

| Tradition | Focus | Primary God(s) |
|---|---|---|
| **Solari Covenant** | Organized institutional religion, law, order | Solaryn (primary) with Chorus acknowledgment |
| **The Old Ways** | Ancient tradition; nature, seasons, cycles | Sylvara (primary); all Chorus honored |
| **The Veiled Order** | Death, transition, acceptance of the Final Verse | Morvel |
| **The Ancestors' Path** | Lineage, obligation to those who came before | Eldris |

**The Solari Covenant's institutional claim** that Solaryn represents the whole of right religion is a theological overreach that every other tradition views with skepticism — established as a setting tension, not an authorial endorsement.

### Cults

Three named cults. These are distinguished from religious traditions by their distortion of legitimate belief into harmful ideology. They are not secret societies — they operate with varying degrees of concealment.

| Cult | Ideology | Notable |
|---|---|---|
| **The Ashen Tribunal** | Purification through destruction of the "unworthy" | Corruption of Solari Covenant's justice emphasis |
| **The Severance** | Severing all ties — to people, place, history — as the path to enlightenment | Corruption of freedom/detachment values |
| **The Threshold Circle** | Obsessive pursuit of what lies beyond the Final Verse | Corruption of the Veiled Order's acceptance of death |

### Vampire Houses

Three canonical houses. Not monolithic — each has internal factions and political complexity.

| House | Territory | Leader | Character |
|---|---|---|---|
| **House Vetharis** | Imperial Capital (primary), surface political operations | Lord Commander Serath Vetharis | Political operators; most integrated into mortal society |
| **House Drakmor** | Frontier and wilderness regions | Warlord Kira Drakmor | Military and territorial; most openly aggressive |
| **House Soleth** | Sol Kareth, Iron Peaks deep passes | Archivist-Queen Mira Soleth | Knowledge-focused; excavation sites in Sol Kareth (two sealed) and Iron Peaks (one gone silent) |

### Goblin Tribes

Three canonical tribes. Not monolithic.

| Tribe | Territory | Settlement | Leader |
|---|---|---|---|
| **Stonefang** | Eastern Frontier, rocky terrain | Fang-Hold | Chieftain Grak Stonefang |
| **Mossroot** | Great Forest | Deep Warren (underground) | Elder Thorn |
| **Ashfire** | Central/southern Frontier | Cinderhold (rebuilt ruin) | Warchief Ember |

### Covenant Inquisitors

The militant enforcement branch of the Solari Covenant.

| Name | Role |
|---|---|
| **Inquisitor-General Coss** | Overall leadership |
| **Senior Examiner Lysa Venn** | Administrative and operational coordinator |
| **Brother Verath** | Active field inquisitor (Frontier reach) |

### Other Named Factions

- **The Adventurers Guild** — continent-spanning organization; serves as a structural hub for player quest intake
- **The Mages Guild** — academic magic institution; headquarters in the Capital's Academic Quarter
- **The Order of Archivists** — administers the Great Library; independent scholarly body
- **The Hidden Pack** — werewolf/lycanthrope faction; members and internal structure not yet established in canon

---

## Ancient Legends

Two figures from the Age of Legends are confirmed canonical. Their names and defining traits are established; all other details are explicitly **NOT YET DEFINED**.

| Figure | Era | Defining Trait | Status |
|---|---|---|---|
| **Aurelia Sunstrider** | Age of Legends | Compassion, hope, courage | Confirmed canon — name and traits only |
| **Valen Ashfall** | Age of Legends | Resolve; facing impossible odds to protect others | Confirmed canon — name and traits only |

Both figures appear in independent sources separated by geography and tradition, suggesting historical reality. Whether they are single historical persons or composite figures built around archetypes remains a matter of scholarly debate within the setting.

---

## Immutable Design Rules (World-Level)

These are established in `docs/lore/CANON_RULES.md` and cannot be overridden by any content:

- **There is no chosen one.** No character is selected by fate, prophecy, or divine will to save the world.
- **There are no chosen races.** No race is inherently superior, divinely favored, or cosmically significant.
- **There are no divine bloodlines.** Power and leadership are not inherited through divine ancestry.
- **Heroes are created through their choices.** A character becomes significant through what they decide, sacrifice, and refuse to compromise — not through who they are at the start.
- **History belongs to mortals.** The gods do not write history. Mortals do.
- **The Architects are never explained.** Their mystery is a permanent feature of the world, not a puzzle to be solved.
- **The Eighth is not named.** Her true name has been erased and must not be invented or recovered.
- **The Final Verse is never answered.** What lies beyond death is permanently unknown, including to the Chorus.

---

---

# SECTION II — PARTIAL CANON

Everything in this section has been mentioned or implied in canonical sources but is **incomplete**. These elements exist — they are not to be denied — but their full details have not been established. Content using these elements should treat them as background texture rather than foreground specifics, unless and until a designer decision completes them.

---

## Geography — Unnamed or Underspecified

| Element | What Is Confirmed | What Is Missing |
|---|---|---|
| **The continent** | The game takes place on a single continent | The continent has no canonical name |
| **Central river corridor** | A significant river (or river network) runs through the center of the continent and forms the backbone of Halfling trade culture | The river is not named; its course, tributaries, and termini are not described |
| **Oceans / seas** | Implied by the half-submerged coastal location of Neressa's temple and by general world geography | None named |
| **Islands** | Implied by standard world geography | None confirmed or named |
| **Mountain ranges** | The Iron Peaks is named; ranges shifted during the Sundering | Black Anvil Range and Thundercrest Range are now named (both are sub-ranges of the Iron Peaks). No other mountain ranges outside the Iron Peaks are named. |
| **Coastlines** | Referenced indirectly (Neressa's temple on a "rocky coast") | Sapphire Coast, Storm Coast, The Shattered Coast, and Emerald Bay are now named. No specific bays, headlands, or sea names are established beyond these four. |

---

## Settlements — Described but Unnamed

| Type | Region | Status |
|---|---|---|
| Oasis cities | Sol Kareth | "Oasis cities" referenced as a settlement type; number and names not established |
| Ice cave complexes | Frozen Highlands | Referenced as existing features; none named |
| Ancient fortresses | Frozen Highlands | Referenced as existing features; none named |
| Forest settlements | Great Forest | No named settlements beyond Deep Warren (goblin) |
| Dwarven settlements | Iron Peaks | No named settlements established beyond the Hall of First Forging (temple) |

---

## The Divine Chorus — Incomplete Details

| Element | Status |
|---|---|
| Sacred animals | Established for each member in `elyndor/magic/MAGIC_BIBLE.md` — not repeated here as they exceed world geography scope |
| Sacred plants | Same |
| Festivals | Established per member in `elyndor/magic/MAGIC_BIBLE.md` |
| Relics | Named per member but not located geographically |
| Ancient temple sites — Morvel | Temple exists; not named or located |
| Ancient temple sites — Eldris | Temple exists; not named or located |

---

## Architect Sites Beyond the First Temple

The Architects' evidence exists "around the world" — this is confirmed. However:
- No specific site outside the First Temple has been named
- No location has been given for any secondary Architect site
- The First Temple sub-structure is the only Architect site described in any detail

---

## The Age of Legends

The Age of Legends is referenced as the era of Aurelia Sunstrider and Valen Ashfall. It is described as "a period of the world's history whose details have grown difficult to separate from myth." Its relationship to the Four-Age or Seven-Age historical frameworks is not specified.

---

## Celestial Bodies

The world has a sun and moon implied by normal day/night cycle references. Stars are referenced in the context of navigation and cosmology. None are named in any canonical source.

---

## Calendar and Dating System

No canonical calendar exists. Years are referenced in relation to the Ages (e.g., "founded in the Second Age," "a thousand years of weakening prison") but no specific year numbering, month names, or dating system has been established.

---

## Trade Routes

The Age of Unity's trade routes "still exist" in the present age — this is confirmed. No specific route has been named, mapped, or given a proper noun.

---

---

# SECTION III — UNDEFINED

Everything in this section has **not been established** in any canonical source. These are genuine gaps — not oversights but open questions awaiting designer decisions. Content must not fill these gaps speculatively.

Items marked ⚠️ **NOT YET DEFINED** in the source documents are listed here.

---

## World Scale and Cosmology

| Gap | Notes |
|---|---|
| Total number of continents | `elyndor/world/world_overview.md` explicitly marks this as intentionally open |
| Whether other landmasses exist beyond the campaign continent | Implied open; no canonical answer |
| The name of the campaign continent (if it has one) | Not established |
| Celestial body names (sun, moon, stars) | None given in any source |
| Whether the world has a canonical "below" (deeper cosmology below the prison) | Implied but not described |

---

## Geography — Unnamed Elements

| Gap |
|---|
| Names of any ocean or sea |
| Names of any island or island group |
| Names of rivers (including the central corridor river) |
| Names of any road or trade route |
| Named oasis cities in Sol Kareth (Oasis of Kings is a named landmark/meeting site, but the oasis *cities* as settlements remain unnamed) |
| Named settlements in the Great Forest (beyond Deep Warren) |
| Named settlements in the Iron Peaks |
| Named settlements in the Frozen Highlands |
| Named settlements in Sol Kareth |
| The First Grove's precise location within the Great Forest |
| The location of Neressa's Sanctuary of Returning Tides (four coastlines now named — which one, or is it on an unnamed stretch?) |
| The location of The High Crossing (mountain pass — Iron Peaks implied but which range is unconfirmed) |

---

## Divine Chorus — Undefined

| Gap | Notes |
|---|---|
| The Eighth's true name | Erased from history; must not be invented |
| The Eighth's elemental aspect | Intentionally undefined |
| The Eighth's domain title (equivalent of "The First Flame," etc.) | Not established |
| What elemental aspect the Eighth stewarded | Intentionally unresolved |
| Ancient temple site name for Morvel | Not established |
| Ancient temple site location for Morvel | Not established |
| Ancient temple site name for Eldris | Not established |
| Ancient temple site location for Eldris | Not established |
| What lies beyond the Final Verse | Permanently undefined by design |

---

## History — Undefined

| Gap | Notes |
|---|---|
| The Age of Legends' relationship to the Four-Age / Seven-Age frameworks | Not specified |
| Named events within the Age of Unity | Referenced as a period; no specific events named |
| Named events within the Age of Long Decline | Referenced; no specific events named |
| Named battles from the Third Age | Referenced as "common ruined fortresses" but none named |
| A canonical year numbering system | Not established |
| A calendar system (months, seasons formally named) | Not established |

---

## Factions — Undefined Details

| Faction | Undefined Elements |
|---|---|
| **The Hidden Pack** | Named members; internal factions; territory; leadership structure |
| **House Vetharis** | Internal factions beyond surface operations description |
| **House Drakmor** | Internal factions; named sub-commanders |
| **House Soleth** | Internal factions; fate of the silent Iron Peaks archive |
| **Stonefang tribe** | Named sub-chieftains; full political structure |
| **Mossroot tribe** | Named sub-leaders; full political structure |
| **Ashfire tribe** | Named sub-commanders; full political structure |
| **The Ashen Tribunal** | Named leadership; specific territory; membership structure |
| **The Severance** | Named leadership; specific territory; membership structure |
| **The Threshold Circle** | Named leadership; specific territory; membership structure |
| **The Hidden Pack** | Everything beyond its existence as a concept |

---

## Ancient Legends — Undefined Details

Both Aurelia Sunstrider and Valen Ashfall have the following explicitly marked as NOT YET DEFINED in their source files:
- Titles
- Physical appearance
- Combat style
- Weapons
- Known abilities
- Specific deeds, opponents, or outcomes of their legendary acts
- Present-day cultural legacy
- Whether either figure is connected to the playable cast

---

## Architect Sites

| Gap |
|---|
| Any named Architect site beyond the First Temple |
| The location of any secondary Architect site |
| The purpose or function of any Architect structure |
| Whether Architect sites correlate to Chorus temple sites or operate independently |

---

## Other World Elements

| Gap |
|---|
| Named roads or named trade routes |
| The continent's own proper name (if it has one) |
| Named celestial events or astronomical phenomena |
| Flora or fauna with proper nouns beyond Chorus sacred species |
| Currency names |
| A canonical measurement system (distance, weight) |
| Any named ocean or sea (four coastlines are now named; the waters themselves are not) |
| Any named river (the central river corridor remains unnamed) |

---

---

## Document History

| Date | Change |
|---|---|
| July 2026 | Created — compiled from full repository review. All 26 source documents reviewed. No new lore established. |
| July 2026 | Updated — added Geography — Named Landmarks section reflecting `docs/world/GEOGRAPHY_LANDMARKS.md`. Updated Partial Canon and Undefined sections to reflect newly named mountain ranges (Black Anvil Range, Thundercrest Range), four named coastlines, three named lakes, and all landmark names. Source documents table updated. |
