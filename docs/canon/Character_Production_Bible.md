# Character Production Bible — Elyndor

The **minimum production standard** for every major character in Elyndor. This is
the studio standard: no primary character is considered production-complete until
every deliverable below exists and is recorded in canon. **Talos** and
**Eleanor** are the reference implementations — measure new work against them.

> Additive rule: this Bible governs *process and deliverables*. It does not
> author lore. Narrative truth lives in `docs/heroes/`, `docs/characters/`,
> `docs/companions/`, `docs/npcs/`. Unknown fields use `_TBD_`.

---

## Required deliverables (and why each exists)

| # | Deliverable | Why it exists |
|---|---|---|
| 1 | **Hero reference sheet** | The single master identity image — the one canonical picture everything else is checked against. |
| 2 | **Full-body render** | Clean, unobstructed full figure for proportion/silhouette reference and promo crops. |
| 3 | **Turnaround sheet** | Front/¾/side/back so 3D artists can model without guessing hidden geometry. |
| 4 | **Tripo reference** | A generation-ready view set + export spec so the 3D pipeline (Tripo) starts from canon, not interpretation. |
| 5 | **Colour palette** | Locks the exact hues so every downstream material/UI/marketing asset stays on-model. |
| 6 | **Equipment reference** | Defines armour/gear pieces as separable layers for paper-doll, swaps, and consistent modelling. |
| 7 | **Weapon reference** | Canonical weapon form so it reads identically in-hand, in UI, and in marketing. |
| 8 | **Facial expression sheet** | Emotional range for animation/portraits so the character *acts* consistently. |
| 9 | **Animation notes** | Movement identity (weight, tells, combat feel) so rigging/animation express character, not just motion. |
| 10 | **Modeling notes** | Production targets (topology, UVs, PBR, scale, polycount, pivots) so models are engine-ready and uniform. |
| 11 | **UI portrait guide** | How to crop/frame the portrait so identity survives at small sizes. |
| 12 | **Canonical documentation** | The character's entry in `docs/canon/Characters.md` tying assets + rules + revision together. |
| 13 | **Design rules** | The short "do-not-change" list that protects the silhouette/identity across contributors. |
| 14 | **Revision history** | Versioned record; canon evolves by supersession, never silent edits. |

A character is **Reference Complete** when 1–3, 5–8, and 12–14 exist; **Production
Complete** when 4, 9–11 and the full 3D→Godot→animation chain are delivered (see
`Character_Production_Status.md`).

## Reference implementations
- **Talos** — `assets/reference/characters/talos_cloak.png`, `talos_no_cloak.png`;
  canon entry in [`Characters.md`](Characters.md#talos).
- **Eleanor** — `eleanor_reference_v1.png` (+ model sheet, turnaround, full-body);
  canon entry in [`Characters.md`](Characters.md#eleanor). Eleanor's sheets also
  demonstrate the deliverables 4–8, 10–11 in a single package.

## Companion Standards (Task 6)
Every **major companion** must eventually receive the same package as a hero:
canon character sheet · canon visual identity · hero render · turnaround ·
equipment reference · weapon reference · expression sheet · production (modeling/
animation) notes · revision history. Companions are **not** a lower tier — they
share the party's screen time and must hold up to the same scrutiny. Talos and
Eleanor are the reference implementation; track companion progress in
[`Character_Production_Status.md`](Character_Production_Status.md).

## Process
1. Follow [`Pipeline.md`](Pipeline.md): Concept → Lore → Design → Canonical
   Reference Sheet → Hero Render → Turnaround → Tripo → Blender → Rigging →
   Godot → Animation → UI → Marketing → Playable Character.
2. Every stage derives from the previous canonical stage.
3. Use the reusable [`checklists/Character_Checklist.md`](checklists/Character_Checklist.md).
4. Obey [`Asset_Standards.md`](Asset_Standards.md) (immutability, naming,
   revisions) and [`Visual_Language.md`](Visual_Language.md) (art direction).
