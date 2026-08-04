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
| Version | File | Resolution | Notes |
|---|---|---|---|
| Eleanor (primary) | _TBD — no canonical reference sheet imported yet_ | — | Until a sheet exists, the **written visual direction in this document is the authoritative reference.** Produce sheets as `assets/reference/characters/eleanor_*.png` (lossless, original resolution) per [`Asset_Standards.md`](Asset_Standards.md), then link them here. |

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
| Reference Images | _TBD_ (written direction authoritative for now) |
| Primary Colours | Ivory / cream / white |
| Secondary Colours | Sky blue / soft teal |
| Accents | Gold embroidery, emerald gemstones, light-brown leather, light-gold metal |
| Silhouette | Young, lighter build; loose flowing golden hair; layered mage robes, travel-ready |
| Race | Human |
| Height | _TBD_ |
| Body Type | Young, lighter build (carries herself with confidence beyond her age) |
| Weapons | Magical focus — staff / wand / orb / crystal (an *active* extension of her, not a tool) |
| Armour | Light armoured mage robes (reinforced cloth + light leather) |
| Accessories | **The Hearthstone Pendant** (new canon); **the family ribbon** tied to her focus (established canon) |
| Personality Summary | Optimistic, warm, compassionate, family-oriented, hopeful, curious |
| Combat Style | Rare multi-element casting — high power, self-managed instability |
| Voice Notes | _TBD_ |
| Important Story Notes | Harmonic Soul; Mages Guild arc — see `docs/heroes/ELEANOR.md` |

### Physical Description
- **Age/build:** young, lighter build; more confident than her age suggests
  (established canon — `docs/heroes/ELEANOR.md`).
- **Hair (canonical):** bright **golden blonde**, long, with slight natural
  waves, worn **loose**, a few strands framing her face — elegant but practical.
  Inspired by the *overall style* of Jaina Proudmoore's long hair without copying
  it. **Her hair is a defining visual feature.**
- **Eyes (canonical):** bright **emerald green**, expressive, full of curiosity
  and hope.
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
  travel-ready. Elegant layered cloth with reinforced light-leather protection;
  small shoulder guards acceptable. **No oversized fantasy armour.**
- **Focus:** staff / wand / orb / crystal — active, expressive, a natural
  extension of her (established canon).
- **Signature accessory:** The Hearthstone Pendant (see below).
- See also [`Equipment.md`](Equipment.md).

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
- Derive the 3D model from the canonical visual direction here (and the future
  Eleanor reference sheet once produced).
- Keep the **loose flowing golden hair** as a hero silhouette element (plan for
  hair sim / well-authored cards).
- Model robes as **layered cloth + light leather**; keep it travel-ready, not
  bulky. Small shoulder guards optional.
- Author the **Hearthstone Pendant** as a distinct, simple prop (see spec).
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
