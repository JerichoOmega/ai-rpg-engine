# Elyndor Universe Bible

> **Elyndor is a standalone fantasy universe, independent of any single game.**  
> Future games, books, comics, or other media may all take place within Elyndor.  
> This document system contains only reusable world-building.  
> Gameplay systems, playable characters, and game-specific content are intentionally excluded.

---

## Canon Rules

- The world is called **Elyndor**.
- Geography is intentionally open-ended — no fixed number of continents, kingdoms, or nations has been established.
- Future projects may define geography as needed, growing outward from what has been previously established.
- **Ancient Legends** are historical or mythical figures from a forgotten age. They are not playable characters unless a future story specifically establishes them as such.
- Modern protagonists and companions belong to their own game's documentation, not here.
- Do not rewrite or redesign established lore unless explicitly instructed.

---

## Lore Writing Style

All lore in this bible should read as though it were discovered by historians, explorers, librarians, or scholars living in Elyndor. Avoid:

- Developer notes or meta commentary
- Gameplay terminology (damage, stats, cooldowns)
- RPG mechanics language
- Modern references

The world should feel **believable and timeless**.

---

## Structure

```
elyndor/
├── README.md                        ← this file (canon rules + index)
├── world/
│   └── world_overview.md            ← high-level setting description
├── ancient_legends/
│   ├── README.md                    ← what Ancient Legends are
│   ├── _legend_template.md          ← canonical template for all legend entries
│   ├── aurelia_sunstrider.md        ← Aurelia Sunstrider — confirmed legend
│   └── valen_ashfall.md             ← Valen Ashfall — confirmed legend
├── bestiary/
│   ├── README.md                    ← bestiary index and filing rules
│   └── _creature_template.md        ← canonical template for all creature entries
├── history/
│   └── README.md                    ← historical timelines and ages
├── magic/
│   └── README.md                    ← magic systems and arcane knowledge
└── organizations/
    └── README.md                    ← guilds, factions, religions, cults
```

---

## Expansion Rules

- Adding a new Ancient Legend: copy `ancient_legends/_legend_template.md`, name it `<character_name>.md`, fill in known sections only.
- Adding a new creature: copy `bestiary/_creature_template.md`, name it `<creature_name>.md`, place it in `bestiary/`.
- Adding a new civilization or region: create a new file in `world/`, referencing only what has been established. Do not invent geography that contradicts existing canon.
- **Never mix Universe Bible content with game-specific content.**

---

## What Does NOT Belong Here

- Playable character sheets → `docs/characters/`
- Game mechanics, classes, combat systems → `docs/`
- Quest design, chapters, story beats → `docs/`
- Any content specific to one game's story

---

## Index of Confirmed Canon

| Category | Confirmed Entries |
|---|---|
| Ancient Legends | Aurelia Sunstrider, Valen Ashfall |
| World Name | Elyndor |
| Setting Tone | Ancient fantasy; oldest civilizations have vanished into myth |
| Geography | Intentionally open-ended |
| Creatures | *(none yet confirmed; template ready)* |
| Organizations | *(none yet confirmed)* |
| Magic System | *(not yet defined)* |
| Pronunciation | See [`docs/PRONUNCIATION_GUIDE.md`](../docs/PRONUNCIATION_GUIDE.md) for all canonical name pronunciations |
