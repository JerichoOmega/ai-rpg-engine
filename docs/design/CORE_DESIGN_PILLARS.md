# Core Design Pillars

> **Canon Status:** CONFIRMED — established July 2026.
> **Authority:** These are the project's non-negotiable experience pillars. **Every future feature must support at least one pillar.** Features that support none are deferred (see [`SCOPE_PROTECTION.md`](SCOPE_PROTECTION.md)) and evaluated via [`FEATURE_EVALUATION.md`](FEATURE_EVALUATION.md).
> **Relationship to the Game Bible:** [`docs/GAME_BIBLE.md`](../GAME_BIBLE.md) § Core Design Pillars defines the *technical/architectural* pillars (reactive world, AI pacing, persistence, modularity, readability, no runtime dependencies). This document defines the *player-experience* pillars they exist to serve. The two lists are complementary; where they appear to conflict, experience pillars set the goal and technical pillars set the constraints.
> **Cross-references:** [`docs/GAME_BIBLE.md`](../GAME_BIBLE.md) · [`docs/world/WORLD_BIBLE.md`](../world/WORLD_BIBLE.md) · [`world_state/README.md`](world_state/README.md) · [`companions/COMPANION_BIBLE.md`](companions/COMPANION_BIBLE.md) · [`docs/systems/quests.md`](../systems/quests.md)

---

## 1. Living World
The world exists independently of the player and visibly changes — with them, without them, and because of them. Regions escalate or recover, factions act on their own agendas, shrines decay or draw pilgrims. Canonical model: [`world_state/LIVING_WORLD_SYSTEM.md`](world_state/LIVING_WORLD_SYSTEM.md).

**Test:** If the player leaves a region for a season, is it different when they return?

## 2. Meaningful Consequences
Choices change the world, not just the epilogue text. Outcomes come in tiers (Excellent → Disastrous), and a Mixed outcome is a *different world*, not a smaller reward ([`world_state/CONSEQUENCES.md`](world_state/CONSEQUENCES.md)). Consequences must be **visible** ([`VISIBLE_CONSEQUENCES.md`](VISIBLE_CONSEQUENCES.md)) and **communicated** ([`PLAYER_COMMUNICATION.md`](PLAYER_COMMUNICATION.md)).

**Test:** Can the player point at something in the world and say "that's like this because of what I did"?

## 3. Tactical Combat
Combat is a decision space, not a dice-rolling interlude. Positioning, resource management, enemy behavior, and party composition matter; readability beats spectacle ([`docs/systems/combat.md`](../systems/combat.md), [`docs/COMBAT_SYSTEM.md`](../COMBAT_SYSTEM.md)).

Its defining expression is **Reactive Combat** — *"Every action creates opportunities."* The player leads an elite party that recognizes openings, creates and capitalizes on them, and spends the shared, earned **Resolve** resource to authorize companion reactions and **Partner Techniques**. Players evaluate situations rather than memorize rotations. This is a **core combat pillar**; full canon: [`REACTIVE_COMBAT.md`](REACTIVE_COMBAT.md).

**Test:** Could a thoughtful player have won a lost fight by deciding differently, and can they tell why? — and: is the player asking *"how can I create another opportunity?"* rather than *"which attack does the most damage?"*

## 4. Handcrafted Storytelling
The AI DM improvises *within* authored canon — named NPCs, authored scenes, written handouts, established lore ([`docs/lore/CANON_RULES.md`](../lore/CANON_RULES.md)). Procedural generation fills gaps; it never replaces authored content for moments that matter. The quest philosophy test applies: if content could be removed without anyone noticing, it should not exist ([`docs/systems/quests.md`](../systems/quests.md)).

**Test:** Do memorable moments trace back to authored material rather than generic templates?

## 5. Companion-Driven Narrative
Companions are the emotional spine of the campaign. They have their own arcs, approval, disagreements, and reactions to the changing world ([`companions/COMPANION_BIBLE.md`](companions/COMPANION_BIBLE.md), [`../companions/COMPANION_REACTIVITY_STANDARD.md`](../companions/COMPANION_REACTIVITY_STANDARD.md)).

**Test:** Would the story feel meaningfully different with a different party?

## 6. Preservation of Civilization
The campaign's emotional register is the Long Decline: something worth saving is slipping, and effort spent holding it together matters. The stakes are settlements, traditions, archives, and roads — not abstract doom ([`docs/world/WORLD_BIBLE.md`](../world/WORLD_BIBLE.md), [`docs/game_tone.md`](../game_tone.md)).

**Test:** Does the feature give the player something concrete to protect, restore, or lose?

## 7. Player Choice Without Binary Morality
No good/evil meter. Choices trade real values against each other — the Consequences canon's "Mixed" tier is the most common honest result. Factions and NPCs judge the player by their own interests and beliefs, not a universal alignment.

**Test:** Do reasonable players disagree about which option was right?

## 8. World State Simulation
A persistent, inspectable world state underlies everything: regions, factions, settlements, shrines, reputation, story memory ([`world_state/WORLD_STATE_SYSTEM.md`](world_state/WORLD_STATE_SYSTEM.md), [`docs/systems/world_state.md`](../systems/world_state.md)). Systems read from and write to it; nothing important lives only in prose.

**Test:** When the world changes, did the state change — and do other systems see it?

## 9. Quality Over Quantity
Fewer, deeper: regions, factions, companions, quests, systems. A small number of deeply developed elements beats breadth every time ([`docs/world/WORLD_BIBLE.md`](../world/WORLD_BIBLE.md) World Philosophy). This pillar is enforced procedurally by [`SCOPE_PROTECTION.md`](SCOPE_PROTECTION.md) and [`FEATURE_EVALUATION.md`](FEATURE_EVALUATION.md).

**Test:** Would we rather ship this feature or deepen an existing one?

---

## Using the Pillars

- **Feature proposals** must name the pillar(s) they reinforce — see [`FEATURE_EVALUATION.md`](FEATURE_EVALUATION.md).
- **Conflicts between pillars** (e.g., a simulation idea that undermines handcrafted storytelling) are resolved in favor of the player-facing experience: what the player sees, understands, and remembers.
- **Pillar changes** are a canon-level decision requiring explicit user approval, like all changes under [`docs/lore/CANON_RULES.md`](../lore/CANON_RULES.md).

---

## Document History

| Date | Change |
|---|---|
| 2026-07-31 | Created — nine experience pillars with tests, reconciled with the Game Bible's technical pillars. |
