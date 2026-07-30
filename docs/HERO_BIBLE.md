# Hero Bible

> **Document Status:** Canonical design philosophy as of July 2026.  
> **Authority:** This document governs the design standard for every companion in the game. All future companions must follow these principles.  
> **Cross-references:** [`docs/CHARACTER_DESIGN_GUIDE.md`](CHARACTER_DESIGN_GUIDE.md) · [`docs/HERO_TEMPLATE.md`](HERO_TEMPLATE.md) · [`docs/heroes/`](heroes/) · [`docs/GAME_BIBLE.md`](GAME_BIBLE.md)

---

## Philosophy

Every companion in this game should feel **handcrafted**.

A companion should never simply be "a tank" or "a mage." Their gameplay, abilities, dialogue, personality, equipment, animations, and story should all reinforce who they are as a **person**.

> Mechanics should grow naturally from the character rather than being assigned arbitrarily.

The player's emotional connection to a companion should be just as important as their combat effectiveness.

---

## Design Requirements

Every companion must have all of the following:

| Requirement | Description |
|---|---|
| **Distinct personality** | Public and private faces; consistent under pressure |
| **Unique gameplay identity** | Combat role grows from who they are, not from slot filling |
| **Memorable visual design** | Instantly recognizable silhouette; meaningful personal details |
| **Meaningful emotional journey** | A story arc that changes them — or challenges them to change |
| **Distinct dialogue** | Should sound uniquely like themselves without a portrait |
| **Personal relationships** | Dynamic with each other companion; evolves over time |
| **Personal quest** | An arc that resolves their Core Wound |

> No companion should ever feel interchangeable.

---

## Core Wound Philosophy

Every companion possesses one defining **Core Wound** — an emotional scar that shapes everything about them.

The Core Wound must directly influence:

- **Personality** — how they present themselves and guard their inner life
- **Dialogue** — what they say and what they avoid saying
- **Gameplay** — their combat role and how their abilities express their wound
- **Personal quest** — the story that challenges and potentially heals the wound
- **Character growth** — how they change (or resist changing) over time

The wound is not the character. It is the lens through which they see the world.

---

## Confirmed Companions & Core Wounds

| Hero | Core Wound |
|---|---|
| **Talos** | Lost faith in authority after years of watching ordinary people suffer while those in power pursued their own agendas |
| **Eleanor** | Naive optimism that leaves her vulnerable to betrayal — she believes the best of everyone, sometimes to her own cost |
| **Ragash** | Rejected by her own people; found belonging with her hounds instead of other people |
| **Ronan** | Believes he is a danger to everyone around him because of his curse; carries constant guilt for what he might become |
| **Steven** | His identity and mysterious past define his emotional journey — what he knows about himself that others do not |

---

## Hero Bible Entries

Full Hero Bible entries live in [`docs/heroes/`](heroes/):

| Hero | Entry | Status |
|---|---|---|
| Talos | [`docs/heroes/TALOS.md`](heroes/TALOS.md) | ✅ Complete |
| Eleanor | `docs/heroes/ELEANOR.md` | ⚠️ Not yet written |
| Ragash | `docs/heroes/RAGASH.md` | ⚠️ Not yet written |
| Ronan | `docs/heroes/RONAN.md` | ⚠️ Not yet written |
| Steven | `docs/heroes/STEVEN.md` | ⚠️ Not yet written |

---

## Creating a New Hero Bible Entry

1. Copy [`docs/HERO_TEMPLATE.md`](HERO_TEMPLATE.md)
2. Name it `docs/heroes/<HERONAME>.md`
3. Fill in every section — do not leave sections blank or marked TBD
4. Confirm that the Core Wound connects to every other section
5. Add the entry to the index table above
6. Cross-reference from `docs/characters/<heroname>.md` and `docs/GAME_BIBLE.md`

---

## Document History

| Date | Change |
|---|---|
| July 2026 | Created — established Hero Bible philosophy, Core Wound system, design requirements |
