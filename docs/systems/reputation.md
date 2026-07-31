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
| **Vampire Houses** | Three separate houses, each tracked independently |
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
