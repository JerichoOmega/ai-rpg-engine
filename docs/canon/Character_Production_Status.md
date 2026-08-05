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
| **Ronan**   | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | **Lore Complete** |
| **Ragash**  | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ◻ | ⬜ | ⬜ | **Reference Complete** |
| **Torren**  | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | **Lore Complete** |

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
- **Ronan / Torren** — narrative bibles exist in `docs/heroes/` and
  `docs/characters/`; no canon visual entry or reference art produced yet.
- **Ragash** — canon visual entry ([`Characters.md#ragash`](Characters.md#ragash))
  + **imported reference art** (`ragash_reference_v1.png` master, `ragash_turnaround_v1.png`,
  `ragash_fullbody_v1.png`, `ragash_character_sheet_v1.png`) from the approved
  package. Culture: [`Bloodhorn Clan`](../world/factions/bloodhorn_clan.md);
  quest: [`The Broken Oath`](../quests/the_broken_oath.md). Now **Reference
  Complete** (3D/rig/Godot/animation/marketing still pending).
- Also present in `docs/heroes/`: **Steven** (not in this tracker's requested
  roster; add a row if promoted to a tracked production character).

_Last updated: 2026-08-04. Update this table whenever a deliverable ships._
