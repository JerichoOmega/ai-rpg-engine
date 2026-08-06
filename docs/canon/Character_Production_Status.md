# Character Production Status — Elyndor

Live production tracker against the [`Character_Production_Bible.md`](Character_Production_Bible.md)
standard. **Only known-completed work is marked Complete.** Everything else is
`Not Started`, `Planned`, or `In Progress` — do not mark work done that has not
been produced.

**Legend:** ✅ Complete · 🟡 In Progress · ◻ Planned · ⬜ Not Started

**Column definitions:**
- *Lore* — narrative bible exists (`docs/heroes/`, `docs/characters/`).
- *Canon Doc* — visual-canon entry in `docs/canon/Characters.md`.
- *Hero Sheet / Full Body / Turnaround* — the corresponding reference image exists.
- *Tripo Ready* — a Tripo 3D **model** has been generated (a reference/export
  spec alone does **not** count).
- *Blender / Rigged / Godot / Animation / UI Portrait / Marketing* — the produced
  asset exists (not merely a reference panel).
- *Voice* — recorded/authored voice **direction or VO** exists.
- *Status* — overall stage.

## Party / Heroes

| Character | Lore | Canon Doc | Hero Sheet | Full Body | Turnaround | Tripo Ready | Blender | Rigged | Godot | Animation | UI Portrait | Marketing | Voice | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Talos**   | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | **Reference Complete** |
| **Eleanor** | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ◻ | ⬜ | 🟡 | **Reference Complete** |
| **Ronan**   | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | **Reference Complete** |
| **Ragash**  | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ◻ | ⬜ | ⬜ | **Reference Complete** |
| **Torren**  | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | **Reference Complete** |
| **Corwin**  | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | **Reference Complete** |
| **Maeve Ashwood** | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | **Reference Complete** |

## Notes (evidence, not claims)
- **Talos** — art: `talos_cloak.png` (turnaround), `talos_no_cloak.png` (hero/full
  body). Canon: [`Characters.md#talos`](Characters.md#talos).
- **Eleanor** — art: `eleanor_reference_v1.png`, `eleanor_model_sheet_v1.png`,
  `eleanor_turnaround_v1.png`, `eleanor_fullbody_v1.png`. Canon:
  [`Characters.md#eleanor`](Characters.md#eleanor). *Tripo:* the model sheet
  includes an export **spec** (OBJ/FBX, 4096² PBR, A-pose, 35k–45k) but no model
  has been generated → Tripo Ready = ⬜. *UI Portrait:* a portrait **panel**
  exists on the sheet (reference), but no exported UI asset → ◻ Planned. *Voice:*
  written voice **direction** exists on the reference sheet / hero bible → 🟡.
- **Ronan** — canon visual entry ([`Characters.md#ronan`](Characters.md#ronan))
  + **imported reference art** (`ronan_reference_v1.png` master,
  `ronan_character_sheet_v1.png`, `ronan_fullbody_v1.png`) from the approved
  *Ronan Character Sheet* set. Now **Reference Complete** (3D/rig/Godot/animation/
  UI/marketing still pending).
- **Corwin** — canon visual entry ([`Characters.md#corwin`](Characters.md#corwin))
  + **imported reference art** (`corwin_reference_v1.png`, 1264×848) + hero/character
  bibles ([`CORWIN.md`](../heroes/CORWIN.md), [`corwin.md`](../characters/corwin.md))
  + companion quest [`The Buried Evidence`](../quests/the_buried_evidence.md). Now
  **Reference Complete** (3D/rig/Godot/animation/UI/marketing still pending).
- **Maeve Ashwood** — canon visual entry
  ([`Characters.md#maeve-ashwood`](Characters.md#maeve-ashwood)) + **imported
  reference art** (`maeve_reference_v1.png`, 1264×848) + hero/character bibles
  ([`MAEVE.md`](../heroes/MAEVE.md), [`maeve.md`](../characters/maeve.md)) +
  recruitment quest [`A Light in the Ashes`](../quests/a_light_in_the_ashes.md).
  Name canonized (Community Healer kept as title). Now **Reference Complete**
  (3D/rig/Godot/animation/UI/marketing still pending).
- **Torren** — canon visual entry ([`Characters.md#torren`](Characters.md#torren))
  + **imported reference art** (`torren_reference_v1.png` master,
  `torren_turnaround_v1.png`, `torren_fullbody_v1.png`, `torren_fullbody_alt_v1.png`)
  from the approved *Torren Ironhall* set. Clan:
  [`Clan Ironhall`](../world/factions/clan_ironhall.md); quest:
  [`The Empty Pedestal`](../quests/the_empty_pedestal.md). Now **Reference
  Complete** (3D/rig/Godot/animation/UI/marketing still pending).
- **Ragash** — canon visual entry ([`Characters.md#ragash`](Characters.md#ragash))
  + **imported reference art** (`ragash_reference_v1.png` master, `ragash_turnaround_v1.png`,
  `ragash_fullbody_v1.png`, `ragash_character_sheet_v1.png`) from the approved
  package. Culture: [`Bloodhorn Clan`](../world/factions/bloodhorn_clan.md);
  quest: [`The Broken Oath`](../quests/the_broken_oath.md). Now **Reference
  Complete** (3D/rig/Godot/animation/marketing still pending).
- Also present in `docs/heroes/`: **Steven** (not in this tracker's requested
  roster; add a row if promoted to a tracked production character).
- **Party marketing key-art** (all five heroes at true relative scale):
  `assets/reference/marketing/party_lineup_keyart_v1.png` (canon-derived derivative).
  **Founder's Compass** interior prop reference:
  `assets/reference/props/founders_compass_interior_v1.png`.
- **Torren combat identity** proven in-engine by **The Forge Stand** showcase
  (`tactical/showcase_forge.py` · [`design doc`](../design/encounters/forge_stand_torren.md)):
  building wins ~87% vs brawling ~22% over 40 seeds.

## Secondary / Supporting NPCs

| Character | Lore | Canon Doc | Reference Art | Tripo Ready | Downstream (Blender→UI→Marketing) | Status |
|---|---|---|---|---|---|---|
| **Hidden Pack Alpha** | ✅ | ✅ | ✅ | ⬜ | ⬜ | **Reference Complete** |

- **Hidden Pack Alpha** — senior Warden of the [`Hidden Pack`](../world/hidden_pack.md)
  who arrives at the climax of [`The Lost Howl`](../quests/the_lost_howl.md) to bring
  the Lost Wolf home. Canon visual entry: [`Characters.md#the-hidden-pack-alpha`](Characters.md#the-hidden-pack-alpha).
  Reference art: `assets/reference/characters/hidden_pack_alpha_reference_v1.png`
  (1264×848). **Supporting production evidence:** the Alpha's mid-encounter arrival
  and objective-swap are proven in-engine by the **Lost Wolf (Bram)** playable slice
  (`tactical/showcase_lost_howl.py` · [`design doc`](../design/encounters/the_lost_wolf_bram.md)):
  compassion play rescues the wolf, murder-hobo play triggers the tragic slain state.
  3D/rig/Godot/animation/UI/marketing still pending.

_Last updated: 2026-06 (Hidden Pack Alpha reference art + Lost Wolf/Bram combat showcase; Ronan + Torren reference art; party key-art + Founder's Compass prop; Torren combat showcase). Update this table whenever a deliverable ships._
