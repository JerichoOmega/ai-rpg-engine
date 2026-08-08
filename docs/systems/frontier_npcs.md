# Region One (Frontier) NPCs — Architecture, Contract & Roster

> **Status:** CONFIRMED — implemented 2026-06 as the *Region One NPC & Settlement
> Population Pass*. Additive, non-breaking, engine-agnostic.
> **Home:** `tactical/living_world/npcs.py` (rules) + `data/frontier_npcs.json`
> (content), consumed via `RegionContent`. **Laws:**
> [`LAYER_RULES.md`](../architecture/LAYER_RULES.md) ·
> [`ENGINE_INTERFACES.md`](../architecture/ENGINE_INTERFACES.md).

## Why this lives in the Living World layer

Region One's inhabitants are built on the **existing** engine-agnostic Living
World foundation (region states, remembered deeds, regional memory,
`LivingWorld` persistence, `RegionContent` manifests) rather than the legacy
`npc_manager.py`. See the audit below for the rationale.

## Design philosophy

- **No approval meter, no morality score.** An NPC's stance is expressed through
  concrete **remembered deeds** and the **region state** around them —
  *"this person remembers what happened"*, never *"+17 friendship"*.
- **No omniscient NPCs.** An NPC only knows a deed if it has a plausible
  knowledge source (`involved`, `witnessed`, `public`, `companion_told`,
  `faction_tracks`, `found_evidence`, `word_of_mouth`). Memory is **derived from
  the deeds the world already persists** — no new persisted NPC state.
- **No simulation.** Presence, role changes and dialogue variants are *derived*
  from region state + deeds at query time, deterministically.
- **Depth scales with importance.** Major NPCs are fully characterized; ambient
  NPCs are a line and a location.

## The NPC content contract (smallest reusable model)

`data/<region>_npcs.json` is a list of NPC records; the manifest references it as
`content.npcs` (optional — a region without NPCs still validates). Fields:

| Field | Purpose |
|---|---|
| `id`, `name`, `role`, `category` | identity (category ∈ `major, quest, settlement, merchant, service, guard, civilian, faction, event, ambient`) |
| `location_id`, `region_id` | placement (must resolve to a region location) |
| `personality`, `motivation`, `concern` | characterization (short) |
| `history`, `values`, `secret` | deeper characterization (major NPCs) |
| `companion_hooks` | which companion the NPC's situation draws out (`medical`→Maeve, `evidence`→Corwin, `military`→Talos, `craft`→Torren, `faith`→Eleanor, `beast`→Ragash, `belonging`→Ronan) |
| `knows` | `[{deed, source}]` plausible knowledge (`deed:"*"`+`source:"public"` = keeps up with public news) |
| `relationships` | `[{with, kind, note}]` (`with` = another NPC id or a companion) |
| `events` | dynamic-world-event ids the NPC is associated with |
| `presence` | `{default, fearful_if_status:[...], absent_if_status:[...]}` |
| `dialogue` | `{default, by_status:{status:line}, by_deed:{deed:line}, by_flag:{flag:line}}` |

### Selection rules (`npcs.py`)
`contextual_dialogue()` chooses the most specific line: **known deed → set flag →
region status → default**, so an NPC never repeats the same line across a major
event they know about. `presence()` derives present/fearful/absent from the
location's status. `knows_deed()`/`remembered_deeds()` gate memory by knowledge
source. `companion_reactions()` returns the present companions the scene draws
out. `resolve_references()` validates every reference resolves (used by the CI
gate + Region Review "NPC Population" check).

## Region One NPC roster (14)

| NPC | Category | Location | Companion hook | Reacts to |
|---|---|---|---|---|
| Camp-Mother Alna | major | Ashen Camp | faith, military | helped_refugees, broke_the_avatar, camp status |
| Sergeant Oda | guard | Ashen Camp | military | helped_refugees, protected_travellers |
| Pell (child) | civilian | Ashen Camp | medical, beast | broke_the_avatar |
| Hetty (cook) | ambient | Ashen Camp | — | recovering status |
| Elder Fenn | major | Greenhollow | faith, evidence | cleansed_woods, broke_the_avatar, village status |
| Merra | merchant | Greenhollow | craft | protected_travellers, restored status |
| Garrick (smith) | quest | Old Forge | craft | restored_forge |
| Coll (trader) | merchant | Frontier Road | evidence | protected_travellers |
| Roadwarden Hulde | faction | Frontier Road | military, evidence | protected_travellers, road status |
| Huntsman Ordo | quest | Old Wolf Shrine | beast, belonging | saved_bram, cleansed_woods |
| Scholar Nain | quest | Sunk Hall (ruins) | evidence | broke_the_avatar (**keeps the mystery**) |
| Ferryman Joss | service | Sundered Span | craft | span status |
| Caravan-Leader Tamsin | event | Frontier Road | faith, medical | helped_refugees |
| Old Perrin | ambient | Frontier Road | faith | broke_the_avatar (public version only) |

Settlements (Ashen Camp, Greenhollow) are inhabited; the boss arena
(Blight Heart) has no residents — remote danger feels different from a home.

## Corruption Avatar aftermath (mystery preserved)

NPCs acknowledge the finale by knowledge tier: **Old Perrin** spreads the public
version but explicitly does not know the deep truth; **Scholar Nain** (the only
one studying the signature) states the Avatar was a *symptom, not the source* and
that something unexplained remains. This **preserves the deliberately unresolved
Corruption source** — consistent with the canon amplification rule
(`docs/canon/` / `frontier_encounters.md`).

## Region One NPC audit (existing inventory)

| Source | What it is | Authoritative for Region One NPCs? | Action |
|---|---|---|---|
| `docs/characters/*.md`, `docs/canon/` | Companion + key-character canon (Maeve, Corwin, Ronan, Torren, Eleanor, Ragash, Talos) — **locked** | Yes (companions) | **Preserved.** Companions are *referenced/reacted to*, never redefined as NPCs. |
| `docs/npcs/warden_solis.md`, `religious_travelers.md` | Existing named canon NPCs (Synod / pilgrimage) | Yes (their arcs) | Untouched; new Frontier names chosen to avoid collision. |
| `npc_manager.py` (`NPCS`) | **Legacy overworld** NPCs (kingdom_capital, shadow_marsh…) using a **numeric relationship meter** | No — not Region One, and its meter is the forbidden pattern | Left as-is; not extended. New NPCs use deeds/memory instead. |
| `dialogue_manager.py` | Legacy dialogue/relationship helpers | Partially | Not required; the data-driven `dialogue` block + `contextual_dialogue()` covers Region One needs without new omniscient state. |
| Living World content | presence/banter/landmarks/events/deeds/memory | Yes | Reused directly; NPCs plug into deeds + region states. |

**Canon reconciliation:** no existing canon was rewritten. New Frontier NPC
names were cross-checked against existing character/quest docs and chosen to be
net-new to avoid conflicts. Companion personalities/wounds/philosophies (esp.
Maeve and Corwin) are untouched — they only appear as `relationships`/
`companion_hooks` targets.

## Save & Godot

- **Save:** no new persisted NPC state. NPC static data is content; NPC dynamic
  reactions are derived from `world_state["living_world"]` (deeds + region
  states), which already persists via the existing SaveState contract. Existing
  and legacy saves are unaffected; unknown future fields are ignored.
- **Godot:** `npcs.py` is pure data + rules (no `print`/`input`/file/UI/Godot).
  The Godot layer owns scenes/sprites/animations/nav/dialogue presentation and
  consumes the same NPC state + `describe()`/`contextual_dialogue()` outputs.

## Validation

`python -m tactical.living_world.region_review` includes an **NPC Population**
check (references resolve, settlements inhabited, category mix, ≥8 NPCs with a
`major`). Full coverage in `backend/tests/test_frontier_npcs.py` (19 tests).

## Revision History

| Date | Change |
|---|---|
| 2026-06 | Created — Region One NPC content model + 14-NPC Frontier roster wired to deeds/region-state/memory/companions; NPC Population review check; audit + reconciliation. Additive/non-breaking. |
