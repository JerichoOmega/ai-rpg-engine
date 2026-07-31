# The World State System (Design)

> **Canon Status:** Confirmed — established July 2026.
> **Authority:** Canonical design definition of the World State — what it measures, what it is not, and the categories every world system reads. The runtime schema is documented in [`docs/systems/world_state.md`](../../systems/world_state.md); see Implementation Status below for the current gap between design and code.
> **Cross-references:** [`LIVING_WORLD_SYSTEM.md`](LIVING_WORLD_SYSTEM.md) · [`WORLD_REACTIONS.md`](WORLD_REACTIONS.md) · [`CONSEQUENCES.md`](CONSEQUENCES.md)

---

## What the World State Is

The World State tracks **the overall health of civilization**.

It is **not**:

- morality
- alignment
- good vs. evil

It measures:

- stability
- prosperity
- security
- hope
- preservation of civilization

**Every major questline influences this system.** No major quest may be neutral to it ([`README.md`](README.md) — canonical design rules).

## The Ten Categories (Canon)

Track at minimum:

| Category | Measures | Example signals in play |
|---|---|---|
| **Security** | Safety of roads, settlements, and travel | Patrol density, encounter danger, escort demand |
| **Prosperity** | Economic health of communities | Market stock, settlement growth, NPC livelihoods |
| **Trade** | Flow of goods between regions | Caravan traffic, prices, route closures |
| **Hope** | Civilian morale and belief in the future | NPC dialogue tone, volunteerism, abandonment rates |
| **Infrastructure** | Roads, bridges, walls, waystations | Travel speed and safety, Builders' Guild activity |
| **Corruption** | Spread of The Corruption | Corruption zones, mutated wildlife, amplified vice |
| **Knowledge Preservation** | What civilization remembers | Library activity, lost archives, recovered lore |
| **Faith** | Health of religious life | Shrine conditions, pilgrim traffic, festival vitality |
| **Political Stability** | Institutional cohesion | Council deadlock, realm disputes, succession crises |
| **Environmental Health** | The land itself | Harvests, wildlife, water, blight |

These values influence **multiple systems simultaneously** — a drop in Security moves prices (Trade), patrols (faction behavior), encounter tables, journal entries, and companion dialogue together. Categories are interconnected by design; isolated movement of a single category should be rare and deliberate.

## Scope: Regional and Continental

World State is tracked at two grains:

- **Regional** — each of the six canonical regions has its own condition; the Frontier can burn while the Capital thrives.
- **Continental** — the aggregate trend the great institutions respond to ([`WORLD_REACTIONS.md`](WORLD_REACTIONS.md)).

Regional decline that goes unanswered escalates and spreads ([`REGIONAL_ESCALATION.md`](REGIONAL_ESCALATION.md)).

## Implementation Status

| Design element | Runtime status ([`docs/systems/world_state.md`](../../systems/world_state.md)) |
|---|---|
| Ten categories | ⚠️ Not yet implemented — the runtime tracks `world_conditions.world_chaos` (0–100+) as a single aggregate; treat it as the current proxy for overall decline |
| Regional conditions | Partial — `regions` section tracks discovery/control; per-region health values not yet implemented |
| Faction reputation | Implemented (`factions` section, -100..100) |
| Event/flag memory | Implemented (`story_memory`, `history`, `events`) |

**Rule for writers:** author content against the *design* categories (they define what the AI Director should narrate); **rule for engineers:** when implementing categories, extend the runtime schema via `ensure_world_state_defaults()` for save compatibility, and keep `world_chaos` as a derived aggregate rather than a parallel truth.
