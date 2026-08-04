# Elyndor — Full Production Audit

> Author: Creative Director / Senior RPG + Systems Design review
> Scope: the whole game as a **player** experiences it, not the docs.
> Date: 2026-06 · Basis: direct codebase analysis (root modules, `tactical/`,
> `legacy/`, `docs/GAME_BIBLE.md`, `known_issues.md`, `roadmap.md`).
> Rule honoured: evolve existing systems, never rewrite what content can fill.

---

## 0. Executive Summary — the one thing that matters

**Elyndor is engine-rich and wiring-poor.** Under the hood it has more capability
than most indie prototypes: a verified data-driven **tactical grid engine**
(`tactical/`, 74 enemy blueprints, LOS/cover/elevation/fire), a branching
**Legacy quest framework** (`legacy/`), a genuine background **living-world
simulation** (`faction_manager`, `economy_manager`, `relationship_manager`,
`world_event_manager`, `dm_brain`), deep **dialogue** (persuasion/intimidation/
memory/rumors), and a **AAA-depth lore bible** (`GAME_BIBLE.md`, religions,
history, magic).

But the **moment-to-moment game the player actually touches is a slot machine.**
The main loop (`game_loop.py`) is: press **Explore** → a `random.randint`
decides combat (60%) / quest (20%) / world event (20%) → maybe a boss (10%) →
tick the world. **Travel** and **Rest** print flavour text and tick — they do
not let you choose a destination even though `travel_manager.travel_to_region()`
fully exists. Everything else on the menu (Quests, Party, Regions, Settlements,
Story, World Events, Director) is a **read-only viewer**.

So the player sees a rich world *described to them* while their actual agency is
"press 1 repeatedly." The gap between vision and felt experience is almost
entirely a **wiring + agency** problem, not a missing-systems problem.

**The single highest-leverage move is not to build more systems — it is to
connect the systems that already exist into the player's hands, and to unify the
three combat/enemy stacks into one.** That alone converts this from "promising
prototype" to "a real RPG loop."

---

## 1. The Three-Systems Problem (CRITICAL — read first)

The project contains **three disconnected combat/enemy stacks**:

| Stack | Files | State | Used by player? |
|-------|-------|-------|-----------------|
| **Legacy prototype combat** | `combat.py` (918 ln), `enemy_manager.py` (`enemy_database`), `bosses.py`, `status_effects.py` | Menu combat: Attack / Heavy Attack; companions auto-attack; no grid, no positioning | **Yes** — this is what `explore()`→`quick_encounter()` runs |
| **Tactical grid engine** | `tactical/` (verified Phase 1) | Full grid: move+AP, LOS, cover, elevation, fire, 74 blueprints, shared AI | **No** — not reachable from the main loop |
| **Legacy branching quests** | `legacy/` | Dialogue trees, speech checks, consequences, living-world reactions | Only via menu **11** |

And a **combat-canon conflict** on top: `Combat_Gameplay_Architecture.md` (what
`tactical/` implements: move+AP, Prepare-reactions, N-unit party, 0 HP =
removed) vs `docs/COMBAT_SYSTEM.md` + `GAME_BIBLE.md` "Combat Overview" (MP + AP
+ Support Action, one Reaction/round, **Facing/flanking**, **Shield Stance**,
**Downed→revive/Death**, **Initiative**, **4-hero party**). These are Level-1
canon and they disagree.

**Why this is the #1 production risk:** every piece of future content
(enemies, bosses, encounters, companion combat, balance) must target *one*
combat model. Building the enemy ecosystem before this is resolved means
building it twice. **Resolution is a decision, not a guess** — see §16 R-01.

---

## 2. Combat (playable `combat.py`)

* **Current State:** Turn-based menu. Player options: Attack, Heavy Attack,
  (skill/item limited). Companions auto-attack via `companion_manager`. Enemies
  via `enemy_manager`. Status effects exist. No grid/positioning/AP.
* **Strengths:** Readable; status-effect + loot + XP wiring works; companions
  participate; boss phase checks exist (`enemy_manager.boss_phase_check`).
* **Weaknesses:** Zero positional tactics; "Heavy Attack" is the only real
  decision; companion auto-attack removes player agency over the party;
  `skill_tree.py` (504 ln) is essentially disconnected from `combat.py`.
* **Player Experience:** Fights feel like a coin-flip you watch, not a puzzle
  you solve. This is the biggest felt-quality gap vs the "tactical RPG" pitch.
* **Production Risk:** The pitch is a *tactical* RPG; the playable combat is not
  tactical. The tactical engine that fixes this already exists but isn't wired.
* **Missed Opportunities:** The verified `tactical/` engine + the party model +
  the status/loot data model could be fused into the real combat.

| # | Recommendation | Class | Prio | Effort | Deps | Risk | Player impact |
|---|----------------|-------|------|--------|------|------|---------------|
| C1 | **Route real encounters through the `tactical/` engine** (bridge: build a `Battlefield` + `Combatant` party from `world_state["player"]` + `active_companions` + `enemy_manager` group, run `CombatEngine`, map results back to XP/loot/status) | Engine | CRITICAL | L | R-01 resolved; §3 party model | High | Turns the core loop tactical |
| C2 | Wire `skill_tree` learned skills into the tactical **Skill action** (currently unimplemented in `actions.py`) | Hybrid | HIGH | M | C1, tactical Skill action | Med | Class fantasy finally usable |
| C3 | Player-controlled companions in tactical combat (they already have stats) instead of auto-attack | Engine | HIGH | M | C1 | Med | Party = tactics, not spectators |
| C4 | Downed/Death + Facing per the canon decision (R-01) | Engine | HIGH | M–L | R-01 | Med | Adds the "one bad position = consequence" tension |

---

## 3. Party, Progression & Skills

* **Current State:** `progression_manager` is surprisingly mature (roster XP,
  hero level-ups, world-tier scaling, `scale_enemy_power`). `player.py` and
  `world_state["player"]` are **dual sources of truth** (known 🟠 bug). Class
  selection doesn't exist (defaults Warrior). `skill_tree.py` unlock/apply/
  legendary exists but combat barely uses it. `skills.py` = 3 functions.
* **Strengths:** Shared-XP roster, world-tier scaling, level-up scaffolding.
* **Weaknesses:** No class choice at start; skills not usable in combat;
  dual player state can desync gear/level from combat.
* **Player Experience:** Progression numbers go up but change little you *feel*.
* **Missed Opportunities:** Skill loadouts already conceptually match the
  tactical engine's equip-slots + loadout-lock model.

| # | Recommendation | Class | Prio | Effort | Deps | Risk | Impact |
|---|----------------|-------|------|--------|------|------|--------|
| P1 | **Unify player state** (make `Player` read/write `world_state["player"]`) | Engine | CRITICAL | M | — | Med (save) | Fixes silent stat desync |
| P2 | **Class selection at new game** (Guardian/Ranger/Mage/Rogue already defined in `tactical/data/classes.json`) | Hybrid | HIGH | S–M | C1 | Low | Identity from minute one |
| P3 | Level-up grants a **skill point + stat growth you notice** (tie to `skill_tree`) | Content | HIGH | S | P1 | Low | Meaningful progression |
| P4 | Ability loadout screen at camp/settlement (reuse tactical loadout-lock) | Engine | MED | M | C2 | Low | Build expression |

---

## 4. Enemies

* **Current State:** **Two rosters.** `enemy_manager.enemy_database` (old,
  playable) and `tactical/data/enemies.json` (74 blueprints, families:
  wildlife, goblinoid, orcish, undead, bandit, corrupted, monster, forest,
  ancient_construct, cave, swamp, cult, mercenary; tiers basic→elite; variants;
  inheritance). The rich one isn't played.
* **Strengths:** The blueprint system is genuinely good: data-driven,
  inheriting, tagged by faction/role/tier/threat with loot/audio/visual hooks.
* **Weaknesses:** 4 AI-profile names referenced but undefined (`caster`,
  `ambusher`, `defender`, `aggressive`) → silent empty AI. Abilities are
  decorative (no Skill action). No morale, no faction tactics, no regional
  night/corruption variants at spawn time. No enemy leaders affecting a group.
* **Missed Opportunities:** Difficulty from *composition/behaviour* (the stated
  pillar) is one AI layer away.

| # | Recommendation | Class | Prio | Effort | Deps | Impact |
|---|----------------|-------|------|--------|------|--------|
| E1 | **Consolidate to the blueprint roster** (retire `enemy_database` or make it a thin adapter) | Engine | CRITICAL | M | C1 | Removes duplicate debt |
| E2 | **Complete the AI-profile library** (add caster/ambusher/defender/commander/brute/fanatical + tactical personalities) + **fail loud** on missing profile | Engine | HIGH | M | tactical AI | Composition-driven difficulty |
| E3 | **Morale system** (leader/elite death, half-group loss → flee/regroup/rally) | Engine | HIGH | M | E2 | Fights feel alive |
| E4 | **Wire enemy abilities** via the Skill action + shared ability library | Engine | HIGH | M | C2 | Signature enemy moments |
| E5 | Named mini-bosses & elite modifiers (one passive + one ability + better loot/AI) as reusable modifier, not new enemies | Hybrid | MED | M | E2 | Memorable encounters |
| E6 | Regional/night/corruption **variants at spawn** (override-only) | Content | MED | S | E1 | Regional identity |

---

## 5. Bosses & Signature Encounters

* **Current State:** `bosses.py` (70 ln) + `enemy_manager.boss_phase_check`;
  one confirmed boss (Ashen Guardian) triggered by a 10% roll after Explore.
* **Weaknesses:** Bosses are stat-check phases, not arenas; random trigger robs
  them of narrative weight; `legacy/` has richer signature encounters that don't
  share the boss framework.
* **Recommendations:**
  * B1 — **Bosses inherit from the enemy blueprint** + phases + arena abilities +
    dialogue (Engine, HIGH, M, deps C1/E2). No separate combat engine.
  * B2 — **Story-placed bosses**, not random rolls (Content, HIGH, S).
  * B3 — Arena hazards/interactables per boss reusing terrain data (Content, MED).

---

## 6. Exploration, Travel & Encounters

* **Current State:** `explore()` = pure RNG slot machine. `travel()` = flavour +
  tick (**does not call** the fully-built `travel_manager.travel_to_region()`
  with neighbours/difficulty/weather). `world_map.py` is a static display (known
  🟡). `encounter_manager` has narrative/ambush encounters that the loop mostly
  ignores. `dungeon_manager` exists (147 ln) but no crawl.
* **Player Experience:** No sense of *place* or *journey*; you don't go anywhere,
  the world just ticks past you.
* **Recommendations:**

| # | Recommendation | Class | Prio | Effort | Impact |
|---|----------------|-------|------|--------|--------|
| X1 | **Wire real travel**: destination choice via `travel_manager` + region graph; travel days roll road encounters | Engine | CRITICAL | M | Gives the world geography |
| X2 | **Live world map** bound to `world_state["regions"]["discovered_regions"]` | Engine | HIGH | S | Discovery matters |
| X3 | **Road/travel event tables** per biome (bandit toll, wounded pilgrim, hunter's camp, abandoned ruin, monster nest, merchant caravan, faction patrol, weather event) | Content | HIGH | M | World feels alive |
| X4 | **Hand-authored discoveries** (hidden caves, lore sites, optional bosses, treasure) seeded per region | Content | HIGH | M | Exploration reward |
| X5 | **Dungeon crawl** using `dungeon_manager` data (rooms, traps, floor boss, loot table) | Hybrid | MED | L | Long-session content |
| X6 | Explore should offer **choices** (investigate / avoid / set camp / scout) not a blind roll | Engine | HIGH | S | Restores agency |

---

## 7. Settlements, Villages & Cities

* **Current State:** `settlement_manager` (546 ln) + `location_manager` (547) +
  `hub.py` (unreached, known 🟢). Menu shows settlements **read-only**.
* **Player Experience:** Towns are entries in a list, not places you enter.
* **Recommendations (all evolve existing managers):**
  * S1 — **Enter a settlement** as a location scene: services menu (shop,
    tavern/rumors, jobs, temple, quest board) (Engine, CRITICAL, M).
  * S2 — **Named residents with schedules + companion reactions** per town
    (Content, HIGH, M) — e.g. *Rourke* the veteran captain, a suspicious
    reeve, a shrine-keeper (respect established canon; mark new names
    `CANON_PENDING`).
  * S3 — **Regional identity**: each settlement's economy/politics/festival/
    local conflict differs (Content, HIGH, M).
  * S4 — **Visible consequences**: quest/faction outcomes change a town's
    prosperity, guards, refugees (reuse `legacy` living-world reactions)
    (Hybrid, HIGH, M).
  * S5 — **Quest board / job board** per settlement feeding `quest_generator`
    (Content, HIGH, S).

---

## 8. Merchants & Economy

* **Current State:** `shop.py` = one generic `shop()` + `black_market()` +
  `sell_item`. `economy_manager` (507 ln) simulates prices/regional economy in
  the background but the player barely sees it.
* **Weaknesses:** One faceless shop everywhere; inventory static; economy sim is
  invisible to the player; no merchant identity, reputation, or scarcity.
* **Recommendations (leverage `economy_manager`):**

| # | Recommendation | Class | Prio | Effort | Impact |
|---|----------------|-------|------|--------|--------|
| M1 | **Merchant archetypes with identity + specialty stock**: reclaimed-Imperial-steel blacksmith, traveling herbalist (stock rotates on a timer), goblin scavenger fence, relic/reliquary dealer, corruption black-market dealer, caravan quartermaster | Content | HIGH | M | Every shop feels distinct |
| M2 | **Dynamic inventory** bound to `economy_manager` (regional surplus/shortage changes stock + price) | Engine | HIGH | M | Living economy the player *feels* |
| M3 | **Merchant reputation → discounts + rare stock unlocks**; tie to `faction_manager`/`reputation` | Hybrid | HIGH | M | Reason to be loyal |
| M4 | **Traveling merchants & seasonal festival vendors** appearing via world events | Content | MED | M | Surprise & timeliness |
| M5 | Merchant **questlines & rivalries** (supply a caravan, break a monopoly) | Content | MED | M | Depth |
| M6 | Player-visible **supply shortages** driven by world events/war (blocked road → prices spike) | Engine | MED | M | Consequence you can trade on |

---

## 9. Crafting, Loot & Equipment

* **Current State:** `loot_manager` (490 ln) + `equipment_system` (582 ln) are
  real. **Crafting does not exist in code** (only `docs/systems/crafting.md`).
* **Recommendations:**
  * L1 — **Crafting MVP** on existing inventory/economy: recipes, gather
    components from enemies/regions, crafted-item table (Engine, MED, L).
  * L2 — **Loot with identity**: named/regional/faction drops, set bonuses,
    rare collector items (Content, HIGH, M) — reuse blueprint `loot` tables.
  * L3 — **Equipment tactical modifiers** feeding the tactical engine (shield →
    cover-grant, bow → range, boots → move) so gear = tactics (Hybrid, HIGH, M).
  * L4 — Inventory **sort/filter/search** QoL (Engine, MED, S).

---

## 10. Quests

* **Current State:** Two systems. `quests.py` `quest_database` = mostly
  kill-count objectives triggered on enemy death; `quest_generator` procedural.
  `legacy/` = rich branching, speech checks, consequences (the good stuff),
  reachable only via menu 11. Faction-bonus never fires (missing `"type"`, known
  🟡).
* **Weaknesses:** Objective variety is thin in the main system; the *good* quest
  tech is siloed; no quest board; consequences don't reach settlements/world.
* **Recommendations:**
  * Q1 — **Promote the `legacy` framework to the primary quest system**; author
    main/side quests as data on it (Engine→mostly Content, HIGH, M).
  * Q2 — **Objective variety**: investigation, escort, defend, negotiate,
    infiltrate, moral-dilemma, time-sensitive, branching (Content, HIGH, M).
  * Q3 — **Quest consequences → living world** (prices, patrols, NPC fates,
    settlement prosperity) using existing `legacy` reactions (Hybrid, HIGH, M).
  * Q4 — Fix faction-bonus by tagging quests `"type":"faction"` (Content, LOW, S).

---

## 11. Companions

* **Current State:** `companion_manager` (722 ln) + `relationship_manager`
  (597) + `docs/systems/journey_system.md` (very deep design). Banter fires on a
  30% tick roll; companions auto-attack.
* **Strengths:** The *design* (camp-as-narrative-space, relationship network,
  corruption-resistance rewards) is a genuine differentiator.
* **Weaknesses:** Player doesn't control companions in combat; relationship
  changes from `npc_manager` aren't persisted (known 🟡); banter is random, not
  situational; personal quests/camp scenes not implemented.
* **Recommendations:**
  * K1 — **Camp scene** (rest → camp) exposing conversations, relationship
    events, personal-quest hooks (the journey_system made real) (Engine, HIGH, L).
  * K2 — **Situational banter** (region/quest/enemy-triggered) instead of pure
    RNG (Content, HIGH, M).
  * K3 — **Companion personal quests + inter-companion conflicts/friendships**
    (Content, HIGH, L).
  * K4 — Player-controlled companions in tactical combat (see C3).
  * K5 — Persist all companion/NPC relationship state (Engine, HIGH, S).

---

## 12. NPCs, Dialogue & Reputation/Factions

* **Current State:** `dialogue_manager` (569 ln) has persuasion/intimidation
  checks, relationships, rumors, world-state-aware lines — genuinely good.
  `faction_manager` (771) + `reputation` simulate standings; `rebels` faction
  missing from `FACTIONS` (known 🟠); dual NPC state (known 🟡).
* **Recommendations:**
  * N1 — **Reachable dialogue**: NPCs you can actually talk to inside
    settlements/quests (wire `dialogue_manager` into location scenes) (Engine,
    HIGH, M).
  * N2 — **Faction reactions the player feels**: patrols, greetings, prices,
    gate access, contracts scale with standing (Hybrid, HIGH, M).
  * N3 — Fix `rebels` faction + unify NPC relationship state (Engine, HIGH, S).
  * N4 — **Reputation tiers with tangible perks/penalties** per faction
    (Content, MED, M).

---

## 13. AI Director & Narrative

* **Current State:** `dm_brain` (268) + `narrative_ai` (375) + `story_manager`
  (520) + `llm_bridge` (**mock-only**) + `prompt_manager` (707). The Director
  ticks and adjusts pacing; narrative is mock text.
* **Strengths:** The scaffolding for AI-paced sessions is real and modular.
* **Recommendations:**
  * D1 — **Director drives encounters/events with intent** (respond to player
    state: low HP → respite; snowballing → escalation) rather than flat % rolls
    (Engine, HIGH, M).
  * D2 — **Optional real LLM** behind `llm_bridge` for flavour only, never
    gating mechanics ("AI-assisted, never AI-dependent") (Engine, MED, M).
  * D3 — **Narrative pacing beats** tied to travel/quests, not random ticks
    (Content, MED, M).

---

## 14. UI / UX / Tutorial / Accessibility

* **Current State:** Numeric terminal menus; heavy blank-line formatting; no
  tutorial; no difficulty options; no map readability; `ui_mockup/` + `app.py`
  (Flask, disconnected) + `preview.py` (mock) hint at a future GUI.
* **Recommendations:**
  * U1 — **Consistent command UI + context help** across menus (Engine, HIGH, S).
  * U2 — **First-session tutorial / guided first quest** (Content, HIGH, M).
  * U3 — **Combat readability**: the tactical engine already exposes
    inspection/threat/preview — surface it as the default combat UX (Engine,
    HIGH, M; deps C1).
  * U4 — **Difficulty options** (enemy scaling already exists via world tier)
    (Engine, MED, S).
  * U5 — Accessibility: screen-reader-friendly output, colourblind-safe glyphs in
    the tactical legend (Engine, MED, S).

---

## 15. Save/Persistence, Retention & Endgame

* **Current State:** `save_manager` (903) + `state_manager` (673) robust but
  carry known bugs (🔴 `npcs` validation; NPC/region dual-state). No
  achievements/bestiary/collections. No defined endgame beyond act tracking
  (`campaign_manager`).
* **Recommendations:**
  * V1 — Fix the 🔴 `validate_world_state` `npcs` bug (Engine, CRITICAL, S).
  * V2 — **Bestiary/codex auto-derived** from blueprint data (discovery, kills,
    strengths/weaknesses, drops) (Engine, HIGH, M) — strong retention hook.
  * V3 — **Achievements + regional completion + lore-book collection** (Content,
    MED, M).
  * V4 — **Endgame**: world-tier "post-campaign" threats, faction war
    conclusion, corruption climax reusing world-event + boss systems (Hybrid,
    MED, L).
  * V5 — Named save slots (Engine, LOW, S).

---

## 16. Engine Debt vs Content Debt (separated)

**Engine debt (must-build capability):** unify combat via `tactical/` (C1);
resolve combat canon (R-01); unify player state (P1); complete AI-profile lib +
fail-loud (E2); morale (E3); Skill/Item actions + ability wiring (C2/E4); real
travel + region graph (X1); live map (X2); enter-settlement scenes (S1);
dynamic merchant inventory (M2); reachable dialogue (N1); Director intent (D1);
bestiary (V2); fix 🔴 save bug (V1); fix rebels + relationship persistence
(N3/K5).

**Content debt (author on existing systems):** enemy variants/elites/named
mini-bosses (E5/E6); road/travel event tables (X3); discoveries (X4); named
merchants + questlines (M1/M4/M5); settlement residents/identity/consequences
(S2–S5); quest objective variety + consequences (Q1–Q3); companion camp scenes/
banter/personal quests (K1–K3); loot identity (L2); reputation perks (N4);
achievements/lore books (V3).

**Rule applied:** no rewrite is recommended. Every item evolves an existing
module. The heaviest engine items (C1, X1, S1) are *bridges/wiring*, not new
architecture.

---

## 17. Roadmap

### Phase 1 — Immediate High-Impact (make the loop a game)
Resolve combat canon (R-01); unify player state (P1); fix 🔴 save bug (V1); wire
**real travel + destination choice** (X1) and **live map** (X2); give **Explore
choices** (X6); **enter-settlement** services scene (S1).
*Time: ~2–3 wk · Complexity: Med · Risk: save-compat during P1 · Success: a new
player travels a chosen route, enters a town, uses services, and Explore offers
decisions — no blind rolls.*

### Phase 2 — Engine Expansion (unify combat & enemies)
Route encounters through `tactical/` (C1); consolidate to blueprint roster (E1);
complete AI profiles + fail-loud (E2); morale (E3); Skill/Item actions + ability
wiring (C2/E4); bosses inherit blueprint + phases (B1); dynamic merchant stock
(M2); reachable dialogue (N1); Director intent (D1).
*Time: ~4–6 wk · Complexity: High · Risk: the three-systems merge is the crux ·
Success: one combat engine, one enemy roster, composition-driven difficulty.*

### Phase 3 — Content Expansion (populate the living world)
Promote `legacy` as primary quests + objective variety + consequences (Q1–Q3);
road/travel event tables (X3); discoveries (X4); named merchants + questlines
(M1/M4/M5); settlement identity/residents/consequences (S2–S5); enemy variants/
elites/mini-bosses (E5/E6); companion camp scenes + situational banter + personal
quests (K1–K3); loot identity (L2); dungeon crawl (X5).
*Time: ~6–10 wk · Complexity: Med (content-heavy) · Risk: scope creep · Success:
each region feels distinct and reactive; no repeated-objective fatigue.*

### Phase 4 — Polish & Presentation
Combat readability via inspection UI (U3); consistent UI + tutorial (U1/U2);
difficulty + accessibility (U4/U5); bestiary/codex (V2); achievements/lore books
(V3); crafting MVP (L1); audio hooks (blueprints already carry audio ids).
*Time: ~3–5 wk · Complexity: Med · Success: legible, teachable, sticky.*

### Phase 5 — Launch Readiness (Early Access)
Endgame arc (V4); save slots (V5); balance pass using verify-style harnesses;
performance/stability sweep of the unified combat; clear the `known_issues.md`
🟠/🟡 backlog; optional GUI decision (`app.py`/`ui_mockup`).
*Time: ~4–6 wk · Complexity: Med–High · Success: a 5–10 hr vertical slice that
reviews as "a real tactical RPG," not a prototype.*

---

## 18. The Top 20 Highest-Impact Recommendations

1. **R-01 — Resolve the combat-canon conflict** (decision gate for everything).
2. **C1 — Route real encounters through the `tactical/` engine** (loop becomes tactical).
3. **X1 — Real travel with destination choice** (the world gets geography).
4. **S1 — Enter settlements as service scenes** (towns become places).
5. **P1 — Unify player state** (kills the silent stat-desync bug).
6. **E1 — Consolidate to the blueprint enemy roster** (one roster).
7. **E2 — Complete AI-profile library + fail-loud** (composition difficulty).
8. **Q1 — Promote `legacy` to the primary quest system** (use the good tech).
9. **X6 — Explore offers choices, not a blind roll** (agency).
10. **M2 — Dynamic merchant inventory bound to the economy sim** (living economy).
11. **E3 — Enemy morale** (fights feel alive).
12. **C2/E4 — Skill/Item actions + ability wiring** (class & enemy fantasy).
13. **B1/B2 — Blueprint bosses with phases, story-placed** (memorable set-pieces).
14. **X3 — Road/travel event tables** (world density between towns).
15. **K1 — Camp scene (journey_system made real)** (companion differentiator).
16. **V2 — Auto-derived bestiary/codex** (retention).
17. **N1/N2 — Reachable dialogue + felt faction reactions** (social world).
18. **X2 — Live world map** (discovery matters).
19. **V1 — Fix the 🔴 save-validation bug** (stability).
20. **U3/U2 — Combat readability + first-session tutorial** (accessibility & retention).

## 19. The 10 Biggest Engine Improvements
C1 combat bridge · X1 travel+region graph · S1 settlement scenes · E2 AI-profile
library+fail-loud · E3 morale · C2/E4 Skill-Item+ability wiring · M2 dynamic
merchant inventory · P1 unify player state · D1 Director-with-intent · V2
bestiary derivation.

## 20. The 10 Biggest Content Additions
Named merchants + questlines (M1/M5) · settlement residents & identity (S2/S3) ·
quest objective variety + consequences (Q2/Q3) · road/travel event tables (X3) ·
hand-authored discoveries & optional bosses (X4) · enemy variants/elites/mini-
bosses (E5/E6) · companion camp scenes + personal quests (K1/K3) · loot identity
& set bonuses (L2) · reputation tiers with perks (N4) · lore books + achievements
(V3).

## 21. The 5 Highest-Risk Production Issues
1. **Three-systems fragmentation + combat-canon conflict** (§1) — build-it-twice
   risk; blocks the enemy ecosystem. *Mitigation: R-01 decision → C1/E1 first.*
2. **Dual player state (`player.py` vs `world_state`)** — silent stat corruption
   across save/load. *Mitigation: P1 with a save-migration + regression harness.*
3. **Save/validation bug (🔴)** — can refuse valid new-game loads. *Mitigation:
   V1 immediately; add a save round-trip test.*
4. **Latent-capability trap** — the team keeps deepening background systems the
   player never touches, widening the vision↔play gap. *Mitigation: enforce a
   "player can touch it this phase" rule; Phase-1 is all wiring.*
5. **Scope creep in Phase 3** — the world is huge; content can sprawl.
   *Mitigation: depth-over-breadth; ship one exemplar region fully before scaling.*

---

## 22. Executive Conclusion

Elyndor does **not** need more systems to become compelling — it needs its
existing systems **connected to the player and unified into one combat/enemy
stack.** The verified `tactical/` engine, the `legacy/` quest framework, the
living-world simulation, and the deep lore bible are, together, more than enough
foundation for a strong indie tactical RPG. The prototype's weakness is entirely
in the **last mile**: the loop exposes RNG where it should expose *decisions*,
describes a world it should let you *enter*, and runs a menu-fight when a
verified tactical engine is sitting one bridge away.

**What must happen to evolve from prototype to commercial contender, in order:**
(1) decide the one combat canon; (2) unify combat/enemies through `tactical/`;
(3) put travel, settlements, dialogue, and merchants into the player's hands;
(4) promote `legacy` quests and author reactive, varied content on the systems
now unified; (5) polish for readability, teach the player, and add the retention
layer (bestiary, achievements, endgame). Do that, and the pitch — *a living,
consequence-driven, companion-led, tactical RPG with strong regional identity* —
stops being a document and becomes the thing the player feels.
