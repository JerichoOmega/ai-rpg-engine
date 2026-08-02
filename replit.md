# Project Dungeon Keeper

## Overview
A terminal-based Python fantasy RPG with an AI Dungeon Master, backed by an extensive documentation-first lore and design repository. Most work in this project is docs/lore/design authoring under `docs/`, `elyndor/`, and the root canon pillar files. GitHub remote: `JerichoOmega/ai-rpg-engine` (origin).

## Canon authority hierarchy
1. `FINAL_CANON_DECISIONS.md` (Canon Lock ledger — rulings D-xx, V-x, P-01, A1–A8)
2. Root pillar docs: `WORLD_BIBLE_1.0.md`, `DIVINE_CHORUS.md`, `GOBLIN_CULTURE.md`, `VAMPIRE_CANON_AUDIT.md`, `LIVING_WORLD_DESIGN_PILLAR.md`, `PRESERVING_WONDER.md`
3. `docs/` tree (operational canon and content production)
4. Governance docs: `PROJECT_CONSTITUTION.md`, `AI_START_HERE.md`, `GAME_BIBLE.md`

`CONSOLIDATION_LOG.md` (root) records synchronization changes and reasons.

## User preferences
- **Lore Impact Report rule (established 2026-08-02):** every authored quest/questline document must end with a "Lore Impact Report" section answering: Does this quest establish new canon? Does it reference existing canon? Which civilizations are involved? Which companions react? Which Divine Voices are reflected? Which philosophical pillars are reinforced? Does it create any future quest hooks? Are there any continuity concerns?
- If implementing content requires *creating or changing* canon (rather than applying existing canon), stop and request approval before proceeding.
- Major questlines must follow the Quest Integration Standard in `docs/systems/quests.md` (outcome-tier tables incl. inaction/escalation).
- The user reviews and approves scoped phases before work proceeds; deliver summaries and wait for explicit approval on scope changes.
