# Canonical Character Reference — Elyndor

This document is the **visual canon** for Elyndor characters: which reference
sheets are authoritative and how all future art must derive from them. The
linked reference sheets are the single source of truth for a character's
appearance. All future art (3D models, portraits, concept art, animation,
equipment layers, marketing renders, UI images) must derive from these sheets
and must not reinterpret them unless a future canonical design revision
explicitly supersedes them (see [`Asset_Standards.md`](Asset_Standards.md)).

Reference assets live under `assets/reference/characters/` and are **reference
material only** — not gameplay sprites or production textures. They are stored
at original resolution, uncompressed and unaltered.

> Narrative lore (backstory, dialogue, relationships) is **not** authored here.
> It lives in `docs/characters/`, `docs/heroes/`, `docs/companions/`,
> `docs/npcs/`. Unknown fields below use clearly-labelled `_TBD_` placeholders —
> do not invent lore.

Use [`_character_template.md`](_character_template.md) when adding a new
character.

---

## Talos

### Status
**Canonical** — primary visual reference for all future Talos art and modeling.

### Reference Assets
| Version | File | Resolution | Notes |
|---|---|---|---|
| Talos (Cloak) | [`assets/reference/characters/talos_cloak.png`](../../assets/reference/characters/talos_cloak.png) | 1672 × 941 | Full turnaround sheet — front/side/back rotations, head studies, weapon + shield callouts, material/colour swatches. Navy hooded cloak over shoulders/back. |
| Talos (No Cloak) | [`assets/reference/characters/talos_no_cloak.png`](../../assets/reference/characters/talos_no_cloak.png) | 1024 × 1536 | Full-body hero portrait, no cloak — armour, navy tabard, longsword, sun-sigil shield. |

### Visual Identity
- **Primary colours:** gunmetal / dark steel plate, brass–gold trim, navy cloth
  (tabard + cloak), brown leather strapping.
- **Silhouette:** broad, heavily-armoured frame in a grounded sword-and-shield
  stance; (cloak version) flowing hooded cloak reads strongly from behind.
- **Iconography:** radiant **sun sigil** on the shield face and tabard trim.
- **Face:** pointed (elven) ears, short dark hair, trimmed beard, facial scar.

### Design Intent (preserve unless a canonical revision changes it)
- Maintain **silhouette & proportions** — bulky guardian frame, board-and-sword.
- Maintain **costume details** — layered dark plate with brass/gold trim and
  leather straps; navy tabard and (cloak variant) navy hooded cloak; segmented
  pauldrons, belt, greaves.
- Maintain the **colour palette** (see the swatch strip on the cloak sheet).
- Maintain the **sun sigil** iconography and the **elven ears / scar** identity.

### Equipment (as depicted in the reference sheets)
- Longsword (one-handed), large round/heater shield bearing the sun sigil,
  full plate cuirass + pauldrons + greaves, navy tabard, (cloak variant) hooded
  cloak, belt and leather harness. _Gameplay stat mapping: TBD._

### Personality
_TBD — see `docs/characters/` / `docs/heroes/` once authored. Do not invent._

### Animation Notes
_TBD — deliberate, weighty guardian movement is implied by the armour and
stance; formal reference to be captured during rigging/animation. Placeholder._

### Combat Notes
_TBD — visually a Guardian archetype (sword-and-shield, defensive). Confirm
against `docs/COMBAT_SYSTEM.md` / `tactical/data/classes.json` before binding to
mechanics. Placeholder._

### Voice & Dialogue Notes
_TBD — no canonical voice direction yet. Placeholder._

### Modeling Notes
- Derive the 3D model from `talos_cloak.png` (turnaround) as the primary
  topology reference; use `talos_no_cloak.png` for undersuit/armour detail.
- Model the cloak as a separable layer so both canonical states (cloak /
  no-cloak) are supported from one base mesh.
- Preserve the swatch palette for material authoring.

### UI Portrait Notes
- Derive portrait crops from `talos_no_cloak.png` (clean hero framing).
- Keep the sun sigil and face identity legible at small sizes.

### Revision History
| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-06 | Canonical reference sheets imported (cloak 1672×941, no-cloak 1024×1536), unaltered. Established as visual source of truth. |

---

## Eleanor

> Eleanor is Elyndor's **second fully-documented canonical reference character**,
> standing beside Talos as a deliberate visual counterpoint: Talos is discipline
> and steel; **Eleanor is hope and light**. Both must read as belonging to the
> same world.
>
> **Narrative canon is established** in [`docs/heroes/ELEANOR.md`](../heroes/ELEANOR.md)
> and [`docs/characters/eleanor.md`](../characters/eleanor.md) — this entry does
> **not** rewrite it. The sections below add the approved **visual direction**
> and consolidate her production reference. Personality/story fields cite the
> existing bible; unknown fields use `_TBD_`.

### Status
**Canonical** — approved visual direction below is the authoritative reference
for all future Eleanor art, modeling, UI, and marketing.

### Reference Assets
**Canonical concept reference — imported 2026-08-04, unaltered (no resize/crop/compress/recolor).**
These are the authoritative visual source for Eleanor until a future canonical
revision supersedes them (see [`Asset_Standards.md`](Asset_Standards.md)).

| Role | File | Resolution | SHA-256 |
|---|---|---|---|
| **Primary** — master character sheet ("The Light of the Elements": turnaround, face/hair, expressions, pendant, palette, combat, animation, relationships, UI) | [`assets/reference/characters/eleanor_reference_v1.png`](../../assets/reference/characters/eleanor_reference_v1.png) | 1024 × 1536 | `af60208a805367b8ab021254dd8bf2d7b836ef0162458bb5ede5d6183a425ebc` |
| Model sheet (close-up, colour palette, PBR texture set, Tripo export info, model notes) | [`assets/reference/characters/eleanor_model_sheet_v1.png`](../../assets/reference/characters/eleanor_model_sheet_v1.png) | 1024 × 1536 | `a6ebbb6038f3ad05fde2e37f2ba033a1ade96f8674cf7ba8046a185b4e4dd791` |
| 3D turnaround (front/¾/side/back, T-pose, wireframe, PBR set) | [`assets/reference/characters/eleanor_turnaround_v1.png`](../../assets/reference/characters/eleanor_turnaround_v1.png) | 1536 × 1024 | `cda925d0cc074239623d5db4e5250488526adaa3418f2c74fa193076aaf7567e` |
| Full-body hero figure (clean pose with staff) | [`assets/reference/characters/eleanor_fullbody_v1.png`](../../assets/reference/characters/eleanor_fullbody_v1.png) | 1122 × 1402 | `ef7ee0bfdf1fb5bcce8e206fd9af94ce0a752f49119810c7aa778b1e726763fe` |

**Status:** Canonical (v1). All Eleanor derivatives must trace back to these files.

### Overview
A young **Human Mage** and **elemental specialist** — the party's warmth and its
force multiplier. Born with an exceptionally rare affinity for **multiple
elements at once**, a gift the Mages Guild has no framework for. She should look
**approachable, not intimidating**: the person you instinctively trust.
(Full character: [`docs/heroes/ELEANOR.md`](../heroes/ELEANOR.md).)

### Metadata (reserved fields)
| Field | Value |
|---|---|
| Character Name | Eleanor |
| Status | Canonical |
| Reference Images | `eleanor_reference_v1.png` (+ model sheet, turnaround, full-body) — canonical v1 |
| Primary Colours | Ivory / cream / white |
| Secondary Colours | Sky blue / soft teal |
| Accents | Gold embroidery, emerald gemstones, light-brown leather, light-gold metal |
| Silhouette | Young, graceful build; long flowing golden hair; layered flowing robes, travel-ready |
| Race | Human (female) |
| Height | 5'6" (167 cm) — per approved reference sheet |
| Body Type | Early 20s; realistic human, graceful build |
| Weapons | Magical focus — staff / wand / orb / crystal (an *active* extension of her, not a tool) |
| Armour | Light armoured mage robes (reinforced cloth + light leather) |
| Accessories | **The Hearthstone Pendant** (new canon); **the family ribbon** tied to her focus (established canon) |
| Personality Summary | Optimistic, warm, compassionate, family-oriented, hopeful, curious |
| Combat Style | Rare multi-element casting — high power, self-managed instability |
| Voice Notes | _TBD_ |
| Important Story Notes | Harmonic Soul; Mages Guild arc — see `docs/heroes/ELEANOR.md` |

### Physical Description
- **Age/build:** early 20s; graceful, realistic human build; carries herself
  with more confidence than her age suggests (established canon —
  `docs/heroes/ELEANOR.md`). **Height 5'6" (167 cm)** per the approved sheet.
- **Hair (canonical):** bright **golden blonde**, long, high-volume with soft
  natural waves, worn **loose**, a few strands framing her face — elegant but
  practical. Inspired by the *overall style* of Jaina Proudmoore's long hair
  without copying it. **Her hair is a defining visual feature.**
- **Eyes (canonical):** bright **emerald green**, expressive, full of curiosity
  and hope.
- **Expression:** warm, kind, gentle; approachable. The approved sheet gives an
  expression range: *happy · curious · concerned · determined.*
- **Read on first sight:** *hope · warmth · kindness · magic.*

### Visual Identity
Eleanor is the **visual opposite of Talos** — light, warmth, and openness against
his steel and discipline — while clearly belonging to the same world. Bright,
clean fabrics and soft metals; an approachable, luminous presence rather than an
armoured or arcane-menacing one.

### Colour Palette
| Role | Colours |
|---|---|
| Primary | Ivory, cream, white |
| Secondary | Sky blue, soft teal |
| Accents | Gold embroidery, emerald gemstones |
| Leather | Light brown |
| Metal | Light gold |

> Replaces any *generic* mage-clothing colour direction with this brighter
> palette. Does not alter established narrative canon.

### Equipment
- **Armour:** light armoured mage robes — **not** fragile, **not** heavy;
  travel-ready. Elegant layered cloth (ivory/cream with blue underlayers and
  gold embroidered trim) with reinforced light-leather protection: bracers,
  belt with utility pouch/satchel, and knee-high leather travel boots with small
  emerald-set guards. Small shoulder guards present. **No oversized fantasy
  armour.**
- **Focus:** staff / wand / orb / crystal — active, expressive, a natural
  extension of her (established canon). Primary depicted focus is the staff
  (below); secondary options (wand/orb/crystal) shown on the sheet's Weapon
  Focus panel.
- **Utility:** spellbook, backup wand, potion pouch, component satchel (model
  sheet).
- **Signature accessory:** The Hearthstone Pendant (see below).
- See also [`Equipment.md`](Equipment.md).

### Weapon — Elegant Mage Staff *(canonical appearance)*
As depicted in the approved artwork:
- A tall, slender **golden staff** with an elegant twisted/interwoven headpiece
  cradling a faceted **pale-blue crystalline gem**, and a matching pointed
  crystal ferrule at the base.
- Warm gold metal, refined and graceful (not blunt or martial) — reads as a
  channeling focus, matching her light-and-gold visual language.
- _No magical lore is asserted for the staff beyond "a focus for channeling
  elemental magic" (existing canon). Deeper properties: `_TBD_` — do not invent._

### Personality
Preserve all existing personality canon (`docs/heroes/ELEANOR.md`). Visually
reinforce: **optimistic, warm, compassionate, family-oriented, hopeful,
curious** — approachable rather than intimidating. Her optimism is genuine, not
naive.

### Combat Style
Elemental specialist and the party's **force multiplier**: her Rare Elemental
Casting lets her combine multiple elements for results single-element mages
cannot reach, at the cost of instability she manages in real time. She is
escalation, not a safety net. (Mechanics/design: `docs/heroes/ELEANOR.md`,
`docs/COMBAT_SYSTEM.md`.)

### Animation Notes
- In combat she should look like someone **in conversation with something**, not
  wielding a tool (established canon).
- Physical tell: when homesick/frightened/after family news she **touches the
  knot of the ribbon** on her focus without noticing.
- Further formal animation reference: _TBD_ (capture during rigging).

### Modeling Notes
- **Derive the 3D model from the canonical reference set above** —
  `eleanor_turnaround_v1.png` for topology (front/¾/side/back + T-pose +
  wireframe), `eleanor_reference_v1.png` for identity, `eleanor_model_sheet_v1.png`
  for materials.
- **Production targets (from the model sheet):** OBJ/FBX export · clean
  quad-based topology · non-overlapping UVs · 4096×4096 PBR set (base colour,
  normal, roughness, metallic, AO, emissive) · real-world scale (metres) ·
  A-pose · **target polycount 35k–45k** · keep pivots centred at the feet.
- Keep the **long, high-volume flowing golden hair** as a hero silhouette
  element (plan hair sim / well-authored cards).
- Model robes as **layered cloth + light leather**; travel-ready, not bulky;
  small shoulder guards included.
- Author the **Hearthstone Pendant** as a distinct, simple prop, seated centred
  above the sternum (see spec).
- Preserve the ivory/cream + sky-blue/teal + gold/emerald palette in materials.

### UI Portrait Notes
- Lead with **face + hair + emerald eyes**; the portrait should immediately read
  *warm and hopeful*.
- Keep the pendant visible in bust framing where it fits naturally.
- Derive portraits from the canonical reference sheet once available; store under
  `assets/reference/ui/`.

### Design Rules
1. Eleanor must visually **contrast Talos** (light/hope vs steel/discipline) yet
   share the world's material language.
2. **Approachable, never intimidating.** Bright palette, soft metals, open
   posture.
3. Hair and emerald eyes are **defining features** — keep them prominent and
   consistent.
4. Do not depict the Hearthstone Pendant as an overtly magical object (see
   Hidden Truth). Do not conflate it with her mother's ribbon.
5. Do not contradict established canon in `docs/heroes/ELEANOR.md`.

**DO-NOT-CHANGE list (from the approved reference sheet):**
- Golden-blonde hair · emerald-green eyes.
- The Hearthstone Pendant (teardrop with emerald).
- Light-coloured mage attire (white / blue / gold).
- Long staff as the primary focus.
- Overall theme of **hope, warmth, and light.**

### Signature Accessory — The Hearthstone Pendant *(new canon)*
- **Name:** The Hearthstone Pendant.
- **Status:** Canonical family heirloom.
- **Material:** a rare **pale-gold metal** that naturally resists age, corrosion,
  and tarnish; warm, soft metallic sheen. **Never magical-looking by appearance
  alone.**
- **Appearance:** simple, elegant, **teardrop-shaped**, centred with a polished
  **emerald** gemstone, suspended from a chain of the same rare metal. No
  excessive ornamentation.
- **Family meaning:** passed through Eleanor's family for generations; represents
  **home, family, legacy, responsibility, and hope.** Given to the next
  generation because they are *ready to carry the family's legacy* — not for
  power.
- **Hidden Truth (handle carefully):** the pendant is **NOT** the source of
  Eleanor's elemental powers. Eleanor was **born** with an exceptionally rare
  multi-element affinity; the pendant **resonates with, stabilizes, and
  harmonizes** that innate gift. Without Eleanor it is simply a treasured
  heirloom; without the pendant Eleanor is still gifted, but wielding multiple
  elements at once becomes significantly more **exhausting, unstable, and
  dangerous**. It **complements** her gift — it does not create it. *(This is
  consistent with her established Harmonic-Soul canon in
  `docs/heroes/ELEANOR.md`.)*
- **Narrative intent:** at the story's start everyone — including Eleanor —
  believes it is simply a cherished heirloom. Its deeper significance unfolds
  **gradually**; do not reveal all mysteries immediately.

> **Canon note — two distinct heirlooms.** Eleanor's established canon already
> gives her **the ribbon** from her mother's dress, tied to her magical focus
> ("the most important thing she carries… not magical at all",
> `docs/heroes/ELEANOR.md`). The Hearthstone Pendant is a **separate, worn**
> heirloom and does **not** replace the ribbon. Keep both: the ribbon is her
> intimate sentimental token and emotional tell; the pendant is the generational
> family piece whose deeper resonance emerges over time.

### Revision History
| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-06 | Established Eleanor's canonical visual direction (golden blonde hair, emerald eyes, ivory/cream + sky-blue/teal + gold/emerald palette, light armoured travel robes) and the canonical **Hearthstone Pendant** heirloom (incl. its Hidden Truth). Narrative canon preserved; no reference sheet imported yet (written direction authoritative). |
| v1.1 | 2026-08-04 | **Imported approved concept art as canonical reference** (unaltered): `eleanor_reference_v1.png` (primary master sheet), `eleanor_model_sheet_v1.png`, `eleanor_turnaround_v1.png`, `eleanor_fullbody_v1.png`. Confirmed height 5'6" (167 cm), the elegant crystalline-gem staff, expression range, and production targets (OBJ/FBX, clean quads, 4096² PBR, A-pose, 35k–45k polys). Written direction superseded by the imported reference set. |

---

## Future Character-Reference Pipeline
All character production assets must **derive from** the canonical reference
sheets above rather than creating new interpretations. This applies to Tripo /
photogrammetry-style 3D generation, Blender sculpts & retopo, Godot models &
rigs, promotional/marketing artwork, equipment previews & paper-doll layers,
portraits and UI character images, and animation reference. See
[`Pipeline.md`](Pipeline.md).

**Rule of thumb:** the reference sheet is the contract. Any deviation must first
be recorded here as a *new canonical revision* before any derivative asset is
produced.
