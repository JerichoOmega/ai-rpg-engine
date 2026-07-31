# Combat System

> **Document Status:** Canonical design direction as of July 2026.  
> **Authority:** This document defines the target combat design for the Stylized 3D Tactical RPG. It supersedes any earlier combat design notes not explicitly preserved here.  
> **Relationship to terminal prototype:** The current Python terminal implementation (`combat.py`) is the active prototype. It does not yet implement the grid, AP economy, facing, or downed system described here. The terminal prototype remains authoritative for *what exists now*; this document is authoritative for *where combat is going*.  
> **Cross-references:** [`docs/GAME_BIBLE.md`](GAME_BIBLE.md) · [`docs/systems/combat.md`](systems/combat.md) · [`docs/PLAYER_SYSTEM.md`](PLAYER_SYSTEM.md)

---

## Combat Philosophy

Combat is a **turn-based tactical system** fought on **square grids** within fully **3D isometric environments**.

The design emphasizes:

- **Tactical positioning** — where you stand matters as much as what you do
- **Meaningful decision making** — every turn should present real choices
- **Environmental awareness** — the battlefield is a tool, not a backdrop
- **Team synergy** — heroes should complement each other through positioning and ability combinations
- **Readable combat** — what is happening should always be clear to the player
- **Flexible player choice** — multiple valid approaches to any situation

> Combat should reward planning rather than speed.

---

## Battlefield

### Grid

Combat takes place on **square tile grids** rendered in a 3D isometric environment.

- Movement occurs tile to tile
- Tile position determines facing, adjacency, flanking, and attack range
- Environmental features (cover, elevation, hazards) are expressed through the tile grid

---

## Movement

Heroes have a pool of **Movement Points (MP)** each turn.

Movement is intentionally **flexible**:

| Option | Rule |
|---|---|
| Move then act | Standard |
| Act then move | Allowed — remaining MP can be spent after an action |
| Split movement | Allowed — move some tiles, act, move remaining tiles |

Movement should never feel like a punishment for acting.

---

## Action Economy

Every hero receives the following resources each turn:

### Movement Points (MP)
Used to move across tiles. Flexible in order (see Movement above).

---

### Action Point Pool (AP)
Used for offensive and tactical abilities.

Examples of AP-cost actions:

| Action type | Examples |
|---|---|
| Weapon attacks | Standard attack, multi-hit, charged strike |
| Offensive spells | Direct damage, AoE, debuffs |
| Combat abilities | Class-specific active skills |
| Dash | Spend AP for bonus movement |
| Combat interactions | Pushing enemies, interacting with environment |
| Special class abilities | Hero-unique powerful actions |

Different abilities cost different amounts of AP. AP is the primary offensive resource.

---

### Support Action

Each hero receives **one dedicated Support Action** every turn.

Support Actions are **entirely separate from AP** and cannot be converted into Action Points.

Examples of Support Actions:

- Drinking potions
- Applying buffs to allies
- Healing injured allies
- Reviving a Downed ally
- Using support-focused abilities
- Other utility-first actions

> Support Actions exist to encourage strategic utility alongside pure offense. A hero who spends all AP on attacks can still contribute healing or a buff without sacrificing combat output.

---

### Reactions

Each hero may use **one Reaction per round**.

Reactions trigger in response to events — typically enemy actions or ally positioning.

Examples:

- **Opportunity attack** — strike an enemy moving out of range
- **Shield block** — intercept an incoming attack
- **Counter attack** — return a blow after being hit
- **Ally protection** — intercept an attack targeting a nearby ally
- Class-specific reaction abilities (to be defined per hero)

Reactions **refresh each round**.

---

## Initiative

Combat uses an **initiative system** with a player-friendly flexibility rule:

- Each combatant has an **Initiative value** determining turn order
- **Heroes whose turns occur consecutively** in the initiative order may be activated in **any order the player chooses** before initiative passes to the opposing side

This means if Talos and Eleanor are both scheduled before the next enemy, the player decides which acts first — enabling setup plays, combos, and tactical sequencing.

This system preserves initiative-based pacing while rewarding party coordination.

---

## Facing

Combat includes **directional facing** for all combatants.

| Direction | Notes |
|---|---|
| **Front** | Full defensive coverage; shields active |
| **Side** | Reduced defensive coverage |
| **Rear** | Minimal coverage; back attacks land for increased effect |

Facing influences:

- **Shield protection** — shields only block frontal attacks (and potentially side, to be balanced)
- **Defensive bonuses** — armor may apply differently by direction
- **Flanking** — attacking from the side or rear bypasses some defenses
- **Back attacks** — rear strikes deal bonus damage or apply special conditions

Positioning relative to enemies is a core tactical consideration, not a bonus mechanic.

---

## Shield Stance System

Shield-bearing heroes gain access to the **Shield Stance** mechanic — an active defensive choice rather than a passive armor bonus.

### Entering Shield Stance

- A shield-bearing hero spends their **Support Action** to raise their shield and enter Shield Stance
- Entering Shield Stance **does not consume any AP**
- The shield remains active until the player chooses to lower it

### Benefits While Active

All bonuses apply to attacks originating from the **front**:

| Benefit | Notes |
|---|---|
| Increased frontal defense | Exact values TBD during balancing |
| Increased block chance | Exact values TBD during balancing |
| Reduced ranged damage from the front | Exact values TBD during balancing |
| Improved melee resistance from the front | Exact values TBD during balancing |
| Access to shield-specific Reaction abilities | Defined per class |

### Maintaining the Stance

Shield Stance **persists between turns** at no additional cost. The player does not spend another Support Action each round — the stance remains until voluntarily dropped or removed by a game mechanic.

### Lowering the Shield

- May be done at the beginning of the hero's turn
- **Costs no AP and no Support Action**
- Removes all Shield Stance bonuses immediately
- Does **not** refund the Support Action originally spent to enter the stance
- The hero's current turn Support Action becomes available for other uses (healing, buffs, revive, consumables)

### Tactical Purpose

Shield Stance creates a meaningful decision every battle:

> Raise the shield for powerful frontal defense — or lower it to use the Support Action for healing, reviving a downed ally, applying a buff, or using a consumable.

This reinforces shield-bearing heroes as **active front-line protectors**, not simply high-armor damage dealers. The system rewards anticipating enemy actions and planning around the tradeoff.

### Design Philosophy

Shields are an active tactical choice, not passive stat bonuses. The system is intentionally simple to understand while rewarding planning and positioning.

Future skills, equipment, talents, and class abilities may expand upon the Shield Stance system.

---

## Downed System

When a hero reaches **zero HP**:

1. They become **Downed** — they fall and cannot act
2. They **do not immediately die**
3. Allies may revive them using a Support Action during combat

### If Combat Ends While a Hero Is Downed

The downed hero:
- Automatically survives
- Stands after combat ends
- Recovers with **very low HP** (~1 HP or a low value determined during balancing)
- Enters **Critical Condition** — they must be healed before the next battle

> Downed is a warning state, not a failure state. It creates urgency without ending the run.

---

## Death

**Death is separate from being Downed.**

A hero only dies through special circumstances:

- **Execution** — struck while Downed by certain enemies or abilities
- **Special enemy abilities** — specific boss or elite mechanics
- **Story events** — narrative-driven death (always intentional)
- **Other intentional gameplay mechanics** — to be defined

Dead heroes **cannot be revived through normal healing**.

They must be restored using the world's **resurrection mechanics** (exact mechanics ⚠️ **NOT YET DEFINED**).

> Death should remain uncommon and meaningful. When a hero dies, it is an event — not a routine outcome.

---

## Party System

### Active Party

The player controls **four active heroes** during combat.

- All four act each round according to initiative
- Party composition (which four heroes are active) is managed outside combat

### Party Management

| Context | Rule |
|---|---|
| Outside combat | Players may freely swap heroes in and out of the active party |
| During combat | Party swapping is **disabled** — the active party is locked |

### Party Bench

Heroes not in the active party remain available for future deployment. They do not participate in the current combat encounter.

---

## Recruitment Philosophy

**Not every hero is guaranteed to appear in every campaign.**

- Recruitment opportunities may vary between playthroughs
- Some heroes may be missable or locked behind specific decisions
- Different campaigns should feel meaningfully different based on who joined the party

> Replayability is a design goal. A party of Talos, Ragash, and Ronan should feel different from one built around Eleanor and Torren.

---

## Design Goals Summary

| Goal | Description |
|---|---|
| Tactical positioning | Where you stand shapes what you can do |
| Team synergy | Heroes should combine — set up, follow up, protect |
| Strategic flexibility | Multiple valid solutions to each encounter |
| Readability | Intent should always be legible on the battlefield |
| Player creativity | Systems should enable surprise and expression |
| Replayability | Different parties and decisions should produce different challenges |

> The system should remain **approachable** for players new to tactical RPGs while offering **meaningful depth** for experienced ones.

---

## Relationship to Current Terminal Prototype

The Python terminal prototype in `combat.py` implements a simplified version of turn-based combat:

- Single-player control, no grid
- Simple Attack / Skill / Item / Flee action menu
- No AP economy, Support Actions, or Reactions
- No facing or positioning
- No Downed state (defeat = combat ends)
- Companions auto-attack

The terminal system is the **active implementation** and should not be broken. The systems documented here are the **design target** for the 3D game. When implementing the 3D engine, the terminal prototype's combat logic (status effects, loot, XP, event bus wiring) provides reference for the underlying data model; the turn structure and UI will be replaced entirely.

Full technical documentation of the terminal prototype: [`docs/systems/combat.md`](systems/combat.md)

---

## Future Definition Required

These areas are confirmed as part of the system but not yet fully designed:

| Area | Status |
|---|---|
| MP values per hero | ⚠️ NOT YET DEFINED — to be balanced per class |
| AP values per hero | ⚠️ NOT YET DEFINED — to be balanced per class |
| Reaction abilities per hero class | ⚠️ NOT YET DEFINED |
| Resurrection mechanics | ⚠️ NOT YET DEFINED |
| Environmental tile types and effects | ⚠️ NOT YET DEFINED |
| Full boss roster | ⚠️ NOT YET DEFINED (Ashen Guardian confirmed only) |
| Initiative stat derivation | ⚠️ NOT YET DEFINED |
| Exact Downed revival HP value | ⚠️ NOT YET DEFINED — approximately 1 HP, to be balanced |

---

## Document History

| Date | Change |
|---|---|
| July 2026 | Created — established canonical combat design direction for 3D Tactical RPG |
