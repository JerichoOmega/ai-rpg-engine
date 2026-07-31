---
name: Name collision checks for lore NPCs
description: Grep all docs for an existing character's name before authoring content around them — the same name may already denote a different person elsewhere.
---

Rule: before writing new content **around an existing named character** (not just when inventing new names), grep the whole repo for the name. Pre-existing docs can contain two different characters with the same name.

**Why:** A quest doc had a deceased Archivist "Carros" while `docs/lore/GREAT_LIBRARY.md` had a living researcher "Carros" with downstream dependencies (vampire houses, Soleth trigger). Building handout content on the quest's Carros got rejected in completion review. Resolution: renamed the *dependency-free* character (quest Archivist → Hollen) and added a disambiguation note in the quest text.

**How to apply:** `grep -rn "<Name>" docs/ elyndor/` before authoring; if two distinct people share a name, rename the one with fewer dependencies and log the rename in Document History.
