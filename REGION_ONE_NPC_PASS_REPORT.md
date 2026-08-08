# Region One — NPC & Settlement Population Pass — Final Report

> Makes Region One (the Frontier) feel **inhabited by real people** and
> establishes the game's reusable NPC content model. Additive · non-breaking ·
> engine-agnostic · Godot-compatible · canon-safe. **Date:** 2026-06.

---

## 1. Outcome

The Frontier is no longer a sequence of interchangeable quest-givers: it is a
place inhabited by 14 characterized NPCs who **remember what the player did**,
**know only what they plausibly could**, **react to the region changing**, and
draw out companion reactions — all through the *existing* deed / regional-memory
/ region-state systems (no meter, no morality, no simulation, no new save path).

## 2. Existing NPC audit & canon reconciliation

| Source | Verdict | Action |
|---|---|---|
| `docs/characters/*`, `docs/canon/*` — companion & key-character canon (Maeve, Corwin, Ronan, Torren, Eleanor, Ragash, Talos), **locked** | Authoritative | **Preserved.** Companions are referenced/reacted-to, never redefined as NPCs. |
| `docs/npcs/warden_solis.md`, `religious_travelers.md` — existing named canon NPCs | Authoritative (their arcs) | Untouched; new names chosen to avoid collision. |
| `npc_manager.py` (`NPCS`) — **legacy overworld**, numeric relationship **meter** | Not Region One; uses forbidden pattern | Left as-is; not extended. |
| `dialogue_manager.py` — legacy dialogue/relationship helpers | Partial | Not required; data-driven `dialogue` block covers Region One without omniscient state. |
| Living World content (deeds/region-state/memory/events) | Authoritative & modern | **Reused** as the NPC substrate. |

**No canon was rewritten.** New Frontier NPC names were cross-checked against
existing docs and chosen net-new. Maeve's and Corwin's locked canon
(personalities, wounds, philosophies, relationships) is untouched.

## 3. NPCs added (14) & locations populated

Ashen Camp (refugee settlement): **Camp-Mother Alna** (major), **Sergeant Oda**
(guard), **Pell** (child/civilian), **Hetty** (cook/ambient).
Greenhollow (village): **Elder Fenn** (major), **Merra** (merchant).
Old Forge: **Garrick** (smith/quest). Frontier Road: **Coll** (trader/merchant),
**Roadwarden Hulde** (faction), **Caravan-Leader Tamsin** (event), **Old
Perrin** (storyteller/ambient). Old Wolf Shrine: **Huntsman Ordo** (quest). Sunk
Hall ruins: **Scholar Nain** (quest). Sundered Span: **Ferryman Joss**
(service). Blight Heart (boss arena): intentionally uninhabited.

Category mix spans major / quest / settlement / merchant / service / guard /
civilian / faction / event / ambient. Every named NPC has a reason to exist.

## 4. NPC content model (smallest reusable contract)

Static NPC data = `data/<region>_npcs.json` (optional `content.npcs` manifest
ref; regions without NPCs still validate). Rules = `tactical/living_world/npcs.py`.
Fields: identity, placement, characterization (depth scales with importance),
`companion_hooks`, `knows` (with knowledge sources), `relationships`, `events`,
`presence` (status-gated), `dialogue` (`default`/`by_status`/`by_deed`/`by_flag`).
`RegionContent` extended with an optional `npcs` list — fully backward-compatible.

## 5. Memory, knowledge & contextual dialogue

- **Memory = remembered deeds.** `remembered_deeds()` = the recorded deeds an NPC
  plausibly knows. No meter.
- **Knowledge is bounded.** `knows_deed()` requires a declared source
  (`involved`/`witnessed`/`public`/`companion_told`/`faction_tracks`/
  `found_evidence`/`word_of_mouth`). NPCs are not omniscient.
- **Dialogue reacts.** `contextual_dialogue()` priority: known deed → set flag →
  region status → default. Proven: Camp-Mother Alna is *fearful* with a
  threatened-camp line on a fresh game, and *present* thanking the player by name
  once the camp is secured and the Avatar broken.

## 6. Living World / restoration / Corruption aftermath

- NPC **presence** and **dialogue** shift with region state: Elder Fenn is
  fearful while Greenhollow is corrupted and welcoming once it is restored;
  Merra's shop reopens; Roadwarden Hulde's ledger turns to good news.
- **Corruption mystery preserved:** Old Perrin spreads only the public version;
  Scholar Nain — the sole investigator — states the Avatar was a *symptom, not
  the source*, leaving the true origin deliberately unresolved (canon-safe).

## 7. Companion interactions

`companion_hooks` + `companion_reactions()` surface the right companion by
situation (medical→Maeve, evidence→Corwin, military→Talos, craft→Torren,
faith→Eleanor, beast→Ragash, belonging→Ronan), gated on party presence — e.g.
Huntsman Ordo draws out Ragash/Ronan only when they are present.

## 8. Save & Godot compatibility

- **Save:** zero new persisted NPC state — NPC memory is derived from the
  already-persisted `living_world` deeds/region-states. Existing/legacy saves
  unaffected; round-trip verified.
- **Godot:** `npcs.py` is pure data + rules (audited: no `print`/`input`/
  `open`/Godot/UI). The Godot layer consumes the same state and `describe()`
  outputs.

## 9. Tests added & validation

- `backend/tests/test_frontier_npcs.py` — **19 tests** covering the 21 required
  checks (load, unique ids, all references resolve, dialogue in fresh &
  completed states, determinism, deed memory, Corruption-mystery preservation,
  fresh/restored state changes, save-load memory survival, companion gating,
  companions-not-redefined, no orphans, no Region Two leakage, category mix,
  settlement inhabitation vs. wilderness sparsity).
- Region Review gained an **NPC Population** check (→ 16 checks).

| Gate | Result |
|---|---|
| `python -m pytest` | **334 passed** (was 315 → +19; 0 regressions) |
| `python -m tactical.verify` | **62/62 — FOUNDATION STABLE** |
| `python -m tactical.living_world.region_review` | **16/16 — REGION READY** |
| `python scripts/ci_quality_gate.py` / `make ci` | **QUALITY GATE: PASS** |
| git scope | only intended files; `save_data.json` restored |

## 10. Files changed

New: `tactical/living_world/npcs.py`, `data/frontier_npcs.json`,
`backend/tests/test_frontier_npcs.py`, `docs/systems/frontier_npcs.md`, this
report. Edited (additive): `region.py` (optional `npcs`), `data/frontier_region.json`
(npcs ref), `__init__.py` (export), `region_review.py` (NPC check + guard list).

## 11. Remaining gaps & Region Two recommendations

- NPC-owned quests currently reuse the existing beats/events + deeds; a future
  pass could add explicit NPC quest objects if the quest architecture warrants.
- The reference NPC contract is region-agnostic: **Region Two ships a
  `<region>_npcs.json`** and inherits every rule (memory, presence, dialogue,
  companion hooks, validation) — content, not systems.
- Scholar Nain's unresolved thread is the deliberate hook into the deeper
  Corruption arc for later regions.

**Region One is populated, reactive, tested, canon-safe, and ready.**
