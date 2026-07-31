# Faction Reputation — Principles

> **Canon Status:** Confirmed — established July 2026.
> **Authority:** Principles only. **[`docs/systems/reputation.md`](../../systems/reputation.md) is the authoritative reputation system** — scale, tracked factions, tier tables, and cross-faction effects. This file restates the design commitments for faction authors; where the two differ, the systems document wins.
> **Cross-references:** [`FACTION_BIBLE.md`](FACTION_BIBLE.md) · [`FACTION_RELATIONSHIPS.md`](FACTION_RELATIONSHIPS.md)

---

## Core Commitments (Canon)

1. **Every major faction maintains its own reputation with the player.** There is **no single universal reputation meter**, and never will be.
2. **Different factions react differently to the same choice.** An act that earns Stonefang respect may cost Mossroot trust; sharing knowledge that delights the Library may alarm the Veiled Order.
3. Reputation is tracked on the standard **-100 to +100** scale with faction-specific tier models (see the tier tables in [`docs/systems/reputation.md`](../../systems/reputation.md)).

## What Reputation Buys

Standing with a faction governs, per its tier model:

- **Trust** — who will deal with the player at all
- **Political influence** — the ability to sway faction decisions at the margin
- **Access to services** — vendors, healing, information, safe passage
- **Discounts** — economic reflection of standing
- **Special quests** — content gated by demonstrated relationship
- **Unique dialogue** — NPCs acknowledge the player's record
- **Story branching** — high- and low-standing routes through major arcs

## Implementation Status

| Faction group | Status |
|---|---|
| Kingdoms, Adventurers Guild, Mages Guild | Tracked ([`docs/systems/reputation.md`](../../systems/reputation.md)) |
| Goblin Tribes (3), Religious Orders (4), Vampire Great Houses (3) | Tracked, with full tier tables |
| Vampire Founding Houses (7) | Narrative standing only, until tables are authored |
| The great guilds, noble houses, military & civil orders, Imperial Council | ⚠️ Tier tables not yet authored — use narrative standing consistent with this folder until the systems document is extended |
| Mercenary companies | ⚠️ NOT YET DEFINED (per systems doc) |

**Rule for writers:** never assume a system-tracked reputation exists for a faction unless [`docs/systems/reputation.md`](../../systems/reputation.md) lists it. Narrative standing (the AI Director's judgment, consistent with faction philosophy) covers the gap — flag any faction that needs a real track as a follow-up task rather than improvising numbers.

## Authoring Checklist

When adding or extending a faction's reputation:

- [ ] Define what the faction *measures* (Drakmor measures capability; Mossroot measures care; Corvath would measure lawfulness)
- [ ] Define gain/loss events tied to the faction's philosophy
- [ ] Define cross-faction effects with allies and rivals ([`FACTION_RELATIONSHIPS.md`](FACTION_RELATIONSHIPS.md))
- [ ] Add tier table to [`docs/systems/reputation.md`](../../systems/reputation.md)
- [ ] Never let reputation reduce to good/evil — factions judge by their own values
