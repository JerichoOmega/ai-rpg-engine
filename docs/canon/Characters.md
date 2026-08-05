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

## Ragash

> Elyndor's **third fully-documented canonical companion**, after Talos and
> Eleanor. **Narrative canon is established** in
> [`docs/heroes/RAGASH.md`](../heroes/RAGASH.md) and
> [`docs/characters/ragash.md`](../characters/ragash.md) — this entry does **not**
> rewrite it. It adds the approved **visual identity**, her **Bloodhorn** origin,
> and consolidates her production reference. Culture: [`Bloodhorn Clan`](../world/factions/bloodhorn_clan.md);
> companion quest: [`The Broken Oath`](../quests/the_broken_oath.md).
>
> **Source:** approved *Ragash Canonical Package* (docs only — no artwork
> included). Personality/story fields cite the hero bible; unknowns use `_TBD_`.

### Status
**Canonical** — visual identity below, and the reference sheets, are
authoritative for all future Ragash art.

### Reference Assets
**Canonical reference — imported 2026-08-05, unaltered (no resize/crop/compress/recolor).**

| Role | File | Resolution | SHA-256 |
|---|---|---|---|
| **Primary** — master hero sheet ("Houndmaster of the Wild": portrait, full body, signature item, back view, design notes, silhouette) | [`assets/reference/characters/ragash_reference_v1.png`](../../assets/reference/characters/ragash_reference_v1.png) | 1536 × 1024 | `c57abeb34c14035cf29f56d9fe90813f28316e0dcc9318e6b41aa30697524ac5` |
| Turnaround / poses (multiple full-body poses, head & expressions ×4, silhouettes, hounds, equipment) | [`assets/reference/characters/ragash_turnaround_v1.png`](../../assets/reference/characters/ragash_turnaround_v1.png) | 1536 × 1024 | `20d911c7d9cb770d61a7a03c911eeeff49b71ceb393d0efdf5b7a3c5dd9d45a3` |
| Full-body character sheet | [`assets/reference/characters/ragash_fullbody_v1.png`](../../assets/reference/characters/ragash_fullbody_v1.png) | 1024 × 1536 | `fef5e4126b7b35538f4cbe2cf7fa4495a1d58c8d16c632ea29f6772f999b6cea` |
| Character sheet (portrait, overview + equipment + palette) | [`assets/reference/characters/ragash_character_sheet_v1.png`](../../assets/reference/characters/ragash_character_sheet_v1.png) | 1086 × 1448 | `b04403c92fd225dda17df580375dfb7f213228034f85b707b785ee1bf6c3b610` |

**Status:** Canonical (v1). All Ragash derivatives must trace back to these files.

### Overview
A **female Orc Ranger / Houndmaster, hunter, and tracker** of the **Bloodhorn
Clan** (an Honor Clan; the reference sheets label her origin *"Bloodhorn Tribe
(Outcast)"* — synonymous). Alignment **Neutral Good**; now travelling with
**The Fellowship** (Talos's company). Motto: **"Blood makes you related. Loyalty
makes you family."** Blunt, proud, fiercely loyal; she believes *belonging is
earned* and found it first among her hounds. Excommunicated from the Bloodhorn
for choosing conscience over an Elder ruling (see
[`The Broken Oath`](../quests/the_broken_oath.md)). Full character:
[`docs/heroes/RAGASH.md`](../heroes/RAGASH.md).

### Metadata (reserved fields)
| Field | Value |
|---|---|
| Character Name | Ragash |
| Status | Canonical (documentation); art pending |
| Reference Images | _TBD_ (none in package) |
| Primary Colours | Rich reddish-brown leather, buckskin |
| Secondary Colours | Charcoal (weather cloak) |
| Accents | Weathered bronze hardware, fur, rope; amber eyes; braid beads |
| Silhouette | Lean, athletic; wild layered black hair with braids/beads; practical wilderness gear |
| Race | Orc (female) |
| Height | 5'7" (170 cm) — per reference sheet (lean; slightly shorter than most orcs) |
| Body Type | Late 20s – early 30s; lean, athletic |
| Weapons | Longbow + longsword + hunting knife (Ranger/Houndmaster); her three hounds extend her reach |
| Armour | Wilderness survival leather (not military/barbarian/ceremonial) |
| Accessories | **The First Paw** antler bead (signature); braided beads of bone/wood/antler/bronze; hunting/travel kit |
| Personality Summary | Blunt, proud, loyal (Neutral Good); warm underneath; earns and tests trust |
| Combat Style | Ranger/Houndmaster — versatile bow/melee, hounds as battlefield presence |
| Voice Notes | _TBD_ (see hero bible) |
| Important Story Notes | Bloodhorn exile; *The Broken Oath*; chosen-family arc |

### Physical Description
- **Build:** female Orc, **lean and athletic**, **slightly shorter than most
  orcs** — a tracker's frame, not a front-line bruiser.
- **Skin:** olive-green.
- **Hair:** thick, layered **black** hair in a wild silhouette; **several braided
  strands** with **handcrafted beads** woven throughout.
- **Eyes:** **amber / golden.**
- **Features:** a **scar crossing one eye**; **small tusks.**

### Visual Identity
Everything about Ragash says **she lives in the wilderness**: weathered,
repaired, practical, self-sufficient. She should read as a capable frontier
survivor and animal-handler — not a soldier, not a raider stereotype. Warm
earth tones against a cold charcoal cloak; handmade details over manufactured
uniformity.

### Design Philosophy
- **Earned, lived-in, self-reliant.** Gear shows practical repairs and personal
  craft (beads, rope, fur). Nothing issued; everything chosen or made.
- **Contrast within the party:** Talos = disciplined steel; Eleanor = light and
  hope; **Ragash = the wild, loyalty, and hard-won belonging.** Same world,
  distinct silhouette.
- Aligns with established orc canon (honour as accountability, wardens not
  raiders — [`NON_HUMAN_FACTIONS.md`](../world/factions/NON_HUMAN_FACTIONS.md)).

### Colour Palette
| Role | Colours |
|---|---|
| Primary | Rich reddish-brown leather, buckskin |
| Secondary | Charcoal (weather cloak) |
| Accents | Weathered bronze hardware, fur, natural rope |
| Skin / eyes | Olive-green skin; amber/golden eyes |

### Equipment
Canonical armour is **wilderness survival gear** — *not* military, *not*
barbarian, *not* ceremonial:
- Rich reddish-brown **leather** + **buckskin** cloth; a **charcoal weather
  cloak**; **weathered bronze** hardware; **fur** accents and **rope**.
- **Hunting equipment**, **travel gear**, and **medical supplies for her
  hounds.**
- **Practical repairs throughout** — patched, re-stitched, personalised.
- See also [`Equipment.md`](Equipment.md).

### Weapons
- **Longsword and bow** (versatile melee/ranged — established combat canon,
  `docs/heroes/RAGASH.md`).
- Hunting tools (knives, snares) consistent with a tracker.
- Her **hounds** are her signature battlefield extension (mechanics: hero bible /
  `docs/COMBAT_SYSTEM.md`). _No new mechanics defined here._

### Signature Item — The First Paw *(canonical)*
- **Status:** Canonical.
- **What:** a **hand-carved antler bead** worn in one of Ragash's braided
  strands, carved from the antler of **the first hound she ever raised.**
- **Meaning:** loyalty, trust, family, responsibility, **chosen family.**
- **Truth:** **no magical properties** — its importance is entirely emotional.
- **Rule:** **The First Paw must appear in every canonical depiction of Ragash.**

### Personality
Preserve all existing personality canon (`docs/heroes/RAGASH.md`): blunt to the
point of seeming cold, warm in ways that take time to see, proud, honest. Belief:
*"You earn belonging. It is not given."* Visually reinforce loyalty and quiet
warmth beneath a guarded exterior — capable and watchful, not hostile.

### Combat Style
Houndmaster — versatile between melee (longsword) and ranged (bow); her hounds
extend her presence and control space. Her power comes from what she has built
and who she has committed to (established canon).

### Companion Role
A **party companion** (chosen family, member of **The Fellowship**). Her three
hounds — **Tracker, Guardian, and Scout** ("more than animals — family") — are
central to her identity and presence. Core themes to guide dialogue, writing,
animation, and cinematics: **loyalty · conviction · belonging · chosen family ·
responsibility · strength through compassion.** Narrative hook (reference sheet):
she seeks the **mythical hounds** — ancient companions said to *choose* their
handler, not be tamed. _(Hook only; deeper lore `_TBD_`.)_

### Animation Notes
- Grounded, watchful, economical movement — a tracker's efficiency.
- Natural, protective body language toward hounds/companions.
- Physical tell: touches **The First Paw** in moments of grief or resolve.
- Formal reference: _TBD_ (capture during rigging).

### Modeling Notes
- Derive from the canonical visual direction here and the future Ragash
  reference sheet **once produced** (none in the package yet).
- Author **wild layered hair with distinct braids + beads** (incl. **The First
  Paw** antler bead) as a hero silhouette element.
- Model gear as **repaired, layered leather/buckskin + cloak + fur/rope**;
  weathered bronze hardware; visible practical repairs.
- Follow the studio production targets in
  [`Character_Production_Bible.md`](Character_Production_Bible.md) /
  [`Pipeline.md`](Pipeline.md).

### UI Portrait Notes
- Lead with **face + tusks + amber eyes + eye-scar + braids/beads**; The First
  Paw should be visible where framing allows.
- Read: capable, guarded warmth — never a snarling stereotype.

### Design Rules
1. Ragash must read as a **wilderness survivor / houndmaster**, not military,
   barbarian, or ceremonial.
2. **The First Paw appears in every canonical depiction.**
3. Keep signature identity consistent: olive skin, amber eyes, eye-scar, small
   tusks, wild braided/beaded black hair.
4. Warm earth tones + charcoal cloak + weathered bronze; handmade over uniform.
5. Do not portray the Bloodhorn (or Ragash) as villains or raider stereotypes.
6. Do not contradict established canon in `docs/heroes/RAGASH.md`.

### Revision History
| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-08-05 | Established Ragash's canonical visual identity (female Orc houndmaster; olive skin, amber eyes, eye-scar, small tusks, wild braided/beaded black hair), wilderness survival gear palette, and **The First Paw** signature item — from the approved *Ragash Canonical Package* (docs only). Added Bloodhorn origin + *The Broken Oath* cross-refs. Narrative canon preserved. **Reference artwork pending (none in package).** |
| v1.1 | 2026-08-05 | **Imported approved reference artwork** (unaltered): `ragash_reference_v1.png` (master hero sheet), `ragash_turnaround_v1.png` (poses/turnaround), `ragash_fullbody_v1.png`, `ragash_character_sheet_v1.png`. Art-confirmed canon: motto *"Blood makes you related. Loyalty makes you family."*, Ranger/Houndmaster role, Neutral Good, height 5'7" (170 cm), late-20s–early-30s, affiliation **The Fellowship**, the three named hounds **Tracker/Guardian/Scout**, bead materials (bone/wood/antler/bronze), and the mythical-hounds hook. Written direction superseded by the imported reference set. |

---

## Ronan

> Elyndor's **fourth fully-documented canonical companion**, after Talos,
> Eleanor, and Ragash. **Narrative canon is established** in
> [`docs/heroes/RONAN.md`](../heroes/RONAN.md) and
> [`docs/characters/ronan.md`](../characters/ronan.md) — this entry does **not**
> rewrite it. It adds the approved **visual identity** and consolidates his
> production reference. Personality/story fields cite the hero bible; unknowns use
> `_TBD_`.
>
> **Source:** approved *Ronan Character Sheet* set. Werewolf-form lore stays
> subordinate to [`RONAN.md`](../heroes/RONAN.md) and
> [`docs/world/hidden_pack.md`](../world/hidden_pack.md).

### Status
**Canonical** — approved visual direction below, and the reference sheets, are
authoritative for all future Ronan art, modeling, UI, and marketing.

### Reference Assets
**Canonical reference — imported 2026-06, unaltered (no resize/crop/compress/recolor).**

| Role | File | Resolution | SHA-256 |
|---|---|---|---|
| **Primary** — master character sheet ("Ronan — The Cursed Drifter": turnaround, expressions, action poses, equipment/materials, werewolf form, backstory, size comparison) | [`assets/reference/characters/ronan_reference_v1.png`](../../assets/reference/characters/ronan_reference_v1.png) | 1024 × 1536 | `46616f543d1365683c38df065bcf056c485ff32e4d22c7af9ea505d8730d1149` |
| Character sheet (landscape multi-panel: turnaround, expressions, action poses, equipment/details, werewolf form, palette, signature items) | [`assets/reference/characters/ronan_character_sheet_v1.png`](../../assets/reference/characters/ronan_character_sheet_v1.png) | 1536 × 1024 | `5bce38ada9cc88d894182445b32cdac8e987d34b0fce146c668d3b76e6fbba6f` |
| Full-body hero render (clean pose with twin short swords) | [`assets/reference/characters/ronan_fullbody_v1.png`](../../assets/reference/characters/ronan_fullbody_v1.png) | 1024 × 1536 | `d86ded00083b731005bbdc5f64959469ec1a592511901784a32e6bb5f952a66c` |

**Status:** Canonical (v1). All Ronan derivatives must trace back to these files.

### Overview
A **Human** drifter and **Rogue / Duelist** (Neutral Good) who carries a werewolf
curse he tries not to inflict on anyone he cares about. He should read as
**"a good man carrying a terrible burden"** — quiet, guarded, thoughtful,
compassionate, loyal — **not** an edgy antihero. Full character:
[`docs/heroes/RONAN.md`](../heroes/RONAN.md).

### Metadata (reserved fields)
| Field | Value |
|---|---|
| Character Name | Ronan |
| Status | Canonical |
| Reference Images | `ronan_reference_v1.png` (+ character sheet, full-body) — canonical v1 |
| Primary Colours | Dark browns — worn leather, rough cloth |
| Secondary Colours | Muted reddish-brown / dark green accents |
| Accents | Weathered steel (blades/buckles); reddish-brown werewolf-fur highlights |
| Silhouette | Lean, self-contained; oversized weathered hooded cloak; slightly separate from the group |
| Race | Human (male) |
| Height | 5'6" (167 cm) — per approved reference sheet |
| Body Type | Early–mid 20s; lean, athletic, travel-worn |
| Weapons | Matched practical **twin short swords** (minimally ornate) |
| Armour | Layered dark travel clothes + worn/repaired leather gear (bracers, belts, pouches, heavy boots) |
| Accessories | **Seed pouch** (symbolic, nonmagical); worn/frayed traveler's scarf |
| Personality Summary | Quiet, watchful, measured, empathetic, self-deprecating, darkly funny; burdened but loyal |
| Combat Style | Human form: fast paired short-swords; Werewolf Form: controlled escalation (mechanics: hero bible / `docs/COMBAT_SYSTEM.md`) |
| Voice Notes | _TBD_ (see hero bible: economical, precise, tired-but-not-hopeless) |
| Important Story Notes | Werewolf curse; cure-search arc; the Hidden Pack — see `docs/heroes/RONAN.md` |

### Physical Description
- **Build:** human, **lean / athletic / travel-worn**; early–mid 20s; **5'6"
  (167 cm)**; moves with the economy of someone always alert.
- **Hair:** **deep reddish-brown with copper undertones**, medium length,
  slightly messy with natural waves.
- **Facial hair:** short, matching **darker scruff**.
- **Eyes:** **amber-yellow** (per canonical sheet — see reconciliation note).
- **Read on first sight:** *quiet · guarded · thoughtful · burdened · kind
  underneath.*

### Visual Identity
Ronan is a **deliberate counterpoint** to Talos (discipline / heavy armour) and
Eleanor (hope / elegant light robes): where they read as steel and light, Ronan
reads as **shadow, distance, and restraint** — while clearly belonging to the same
world. Weathered, layered, self-repaired; nothing decorative.

### Colour Palette
| Role | Colours |
|---|---|
| Cloth / Leather | Dark browns |
| Accent (muted) | Reddish-brown, dark green |
| Metal | Weathered steel / greys |
| Werewolf fur | Dark brown with reddish-brown highlights |

### Equipment (as depicted in the reference sheets)
- **Oversized weathered hooded cloak** over **layered dark travel clothes**.
- **Worn / repaired leather gear:** bracers, belts, pouches, heavy travel boots;
  fingerless where shown.
- **Twin short swords** — matched, practical, minimally ornate (paired duelling).
- See also [`Equipment.md`](Equipment.md).

### Signature Item — The Seed Pouch *(symbolic, nonmagical)*
- **What:** a small belt pouch of **seeds from his childhood home** (a sprouting
  seedling is shown emerging from it on the sheet).
- **Meaning:** *"something beautiful can still grow, even in darkness"* — hope and
  origin carried by a man who keeps himself at a distance.
- **Truth:** **no magical properties**; its importance is entirely emotional.
  Do not depict it as an arcane object.

### Werewolf Form (production notes)
- **Silhouette:** dramatically **larger** than human form — strong shoulders, long
  arms, thick fur; a **visually distinct entity**, not the same figure re-statted
  (≈ 8+ ft per the sheet's size comparison).
- **Fur:** **dark brown with rich reddish-brown highlights**, especially along the
  **mane, shoulders, and back.**
- Model the transformation as a **separate hero silhouette** derived from the same
  identity; keep human-form palette echoes in the fur highlights.
- Silver weakness and form mechanics: hero bible / `docs/COMBAT_SYSTEM.md`.

### Personality
Preserve all existing personality canon (`docs/heroes/RONAN.md`): quiet, watchful,
measured, deeply empathetic, self-deprecating, darkly funny. Visually reinforce
**a burdened, loyal, compassionate man** — guarded exterior protecting real
warmth. **Not** a brooding edgelord.

### Combat Style
Human form: capable, careful paired short-swords. Werewolf Form: **controlled
escalation** — more powerful, harder to control, carrying real cost (established
canon). No new mechanics defined here.

### Animation Notes
- Grounded, economical, always-alert body language; keeps a margin from the group.
- The cloak reads strongly in motion and from behind.
- Formal reference: _TBD_ (capture during rigging).

### Modeling Notes
- Derive the 3D model from `ronan_reference_v1.png` (identity + turnaround) and
  `ronan_character_sheet_v1.png` (turnaround/details); use `ronan_fullbody_v1.png`
  for clean proportions.
- Author the **oversized hooded cloak** as a separable layer; model **twin short
  swords** as a matched pair.
- Build the **Werewolf Form** as a distinct hero mesh sharing identity cues.
- Preserve the dark-brown palette with reddish-brown accents.
- Follow the studio production targets in
  [`Character_Production_Bible.md`](Character_Production_Bible.md) /
  [`Pipeline.md`](Pipeline.md).

### UI Portrait Notes
- Lead with **face + amber eyes + reddish-brown wavy hair + hood**; read as
  *guarded, thoughtful, kind underneath.*
- Keep both human and werewolf portraits available for state changes.

### Design Rules
1. Ronan must read as **"a good man carrying a terrible burden"** — never an edgy
   antihero.
2. He must **contrast Talos and Eleanor** (shadow/restraint vs steel and light)
   while sharing the world's material language.
3. Keep signature identity consistent: reddish-brown copper-undertoned wavy hair,
   short scruff, amber eyes, oversized hooded cloak, twin short swords, seed pouch.
4. The **seed pouch appears** where framing allows; it is symbolic and nonmagical.
5. The **Werewolf Form is a distinct silhouette**, not a recoloured human.
6. Do not contradict established canon in `docs/heroes/RONAN.md`.

> **Reconciliation notes (art sheet vs narrative canon).**
> 1. **Eyes:** one sheet leaves eye colour *TBD*; the master sheet specifies
>    **amber-yellow** — adopted as canonical.
> 2. **Backstory blurb:** the sheet's short blurb says Ronan was *"born into a
>    nomadic werewolf pack."* **Established narrative canon is authoritative**
>    ([`RONAN.md`](../heroes/RONAN.md)): Ronan believed himself **alone** in the
>    curse for most of his life, and the **Hidden Pack**
>    ([`hidden_pack.md`](../world/hidden_pack.md)) is a later **discovery** and
>    turning point. Treat the sheet blurb as **art-context only** — do not import
>    it as narrative canon.

### Revision History
| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-06 | Established Ronan's canonical visual direction and **imported approved reference artwork** (unaltered): `ronan_reference_v1.png` (master sheet), `ronan_character_sheet_v1.png` (multi-panel), `ronan_fullbody_v1.png`. Canon: Human Rogue/Duelist, 5'6" (167 cm), reddish-brown copper-undertoned wavy hair + short scruff, amber eyes, oversized hooded cloak + layered travel leathers, twin short swords, symbolic nonmagical seed pouch; werewolf-form production notes (larger silhouette, dark-brown fur with reddish-brown highlights). Narrative canon preserved; art-blurb backstory reconciled as art-context only. |

---

## Torren

> Elyndor's **fifth fully-documented canonical companion**, completing the core
> party alongside Talos, Eleanor, Ragash, and Ronan. **Narrative canon is
> established** in [`docs/heroes/TORREN.md`](../heroes/TORREN.md) and
> [`docs/characters/torren.md`](../characters/torren.md) — this entry adds the
> approved **visual identity**, his **Clan Ironhall** heritage, his signature
> artifacts, and his companion quest, and consolidates his production reference.
>
> **Source:** approved *Torren Ironhall Character Sheet* set. Clan:
> [`Clan Ironhall`](../world/factions/clan_ironhall.md); companion quest:
> [`The Empty Pedestal`](../quests/the_empty_pedestal.md). Personality/story
> fields cite the hero bible; unknowns use `_TBD_`.

### Status
**Canonical** — approved visual direction below, and the reference sheets, are
authoritative for all future Torren art, modeling, UI, and marketing.

### Reference Assets
**Canonical reference — imported 2026-06, unaltered (no resize/crop/compress/recolor).**

| Role | File | Resolution | SHA-256 |
|---|---|---|---|
| **Primary** — master character sheet ("Torren Ironhall — Dwarf • Blacksmith • Companion": expressions, turnaround, details, clothing/gear, weapon, key items, palette, tools, scale reference) | [`assets/reference/characters/torren_reference_v1.png`](../../assets/reference/characters/torren_reference_v1.png) | 1536 × 1024 | `c57402d4258bdede6eff74cbac15eb5c9a44aa304753d147df62806fe0214de7` |
| Turnaround / action poses (8 poses, grey field) | [`assets/reference/characters/torren_turnaround_v1.png`](../../assets/reference/characters/torren_turnaround_v1.png) | 1536 × 1024 | `87bf7c852a9af789e4d32e2894eed366c7cb7da32fa64dc4e546b7bb6385b5b6` |
| Full-body hero render (hammer over shoulder, compass on belt) | [`assets/reference/characters/torren_fullbody_v1.png`](../../assets/reference/characters/torren_fullbody_v1.png) | 1122 × 1402 | `0b34c598920fa1dac6613391af7697d7a8b2dea6ba42c3739a0591787b063bd2` |
| Full-body hero render (alternate) | [`assets/reference/characters/torren_fullbody_alt_v1.png`](../../assets/reference/characters/torren_fullbody_alt_v1.png) | 1122 × 1402 | `649634e61c15e94f8d39fb92d09d21452342e7841c1475b3facb7e0baca65502` |

**Status:** Canonical (v1). All Torren derivatives must trace back to these files.

### Overview
**Torren Ironhall** — a **Dwarf Master Blacksmith, craftsman, and adventurer**
(Lawful Good) of **[Clan Ironhall](../world/factions/clan_ironhall.md)**. In the
party he is the **heavy frontline fighter, the craftsman, and the moral heart of
the group.** He is the comic relief — but his humour is a **coping mechanism**:
he jokes because **silence forces him to remember the burden his family has
carried for generations.** The humour disappears only when he speaks of Clan
Ironhall. Full character: [`docs/heroes/TORREN.md`](../heroes/TORREN.md).

### Metadata (reserved fields)
| Field | Value |
|---|---|
| Character Name | Torren Ironhall |
| Status | Canonical |
| Reference Images | `torren_reference_v1.png` (+ turnaround, 2× full-body) — canonical v1 |
| Primary Colours | Charcoal, deep brown |
| Secondary Colours | Burgundy (mountain cloak), worn tan |
| Accents | Copper / bronze hardware; steel (hammer, tools) |
| Silhouette | Compact, broad, barrel-chested; forge-braided beard; load-bearing, immovable |
| Race | **Dwarf** (male) |
| Age | ~85 (dwarf) — roughly a human's early/mid 30s |
| Height | 4'5" (135 cm) — per approved reference sheet |
| Body Type | Broad shoulders, massive forearms, thick hands, barrel chest; compact but immensely strong |
| Weapons | **Forge Hammer** — a blacksmith's hammer adapted for combat |
| Armour | Heavy leather work gear — reinforced smith's apron, tool belts, thick mountain boots; practical, repaired, not ornate |
| Accessories | **The Founder's Compass** (signature); **The Ironhall Master's Seal** (secondary, retired); tool belts, pouches, fingerless gloves; the **Cold Clasp** (reserved personal-arc detail — see hero bible) |
| Personality Summary | Warm, friendly, quick-witted, protective, dependable, humble, compassionate; humour as coping; grave only about Clan Ironhall |
| Combat Style | Heavy frontline / battlefield shaper; Support / Engineer (Field Forge constructs) — mechanics: hero bible / `docs/COMBAT_SYSTEM.md` |
| Voice Notes | _TBD_ (see hero bible: measured, dry, late-arriving humour; **terrible dwarven dad jokes**) |
| Important Story Notes | Clan Ironhall's disgrace; **The Empty Pedestal**; the Founder's Compass lineage — see `docs/heroes/TORREN.md` |

### Physical Description
- **Build:** dwarf, **broad shoulders, massive forearms, thick powerful hands,
  barrel chest** — compact but incredibly strong; **built like a lifelong
  blacksmith.** **4'5" (135 cm)**; ~85 years old (human early/mid-30s equivalent).
- **Face:** **square jaw, slightly crooked nose, heavy eyebrows, laugh lines,
  strong cheekbones, warm expression** — players should **immediately trust
  him.** Forge scars on face and hands.
- **Hair:** medium-length **deep reddish-brown / ginger**, slightly messy with
  natural waves; well-kept but practical.
- **Beard:** full to **mid-chest**, same reddish-brown/ginger, with several
  **forge braids** and **simple iron rings**; **one braid is singed shorter**
  from an old forge accident (left side).
- **Eyes:** **warm amber** — kind, expressive.

### Visual Identity
Read: **"a master craftsman who travels"** — **NOT** a royal dwarf. Everything is
**repaired, used, loved, practical**; nothing overly ornate. Within the party he
is the **grounded, load-bearing** silhouette — Talos is disciplined steel,
Eleanor is light and hope, Ragash is the wild, Ronan is shadow and restraint, and
**Torren is the anvil the party is built around.**

### Colour Palette
| Role | Colours |
|---|---|
| Primary | Charcoal, deep brown |
| Secondary | Burgundy (mountain cloak), worn tan |
| Metal | Copper, bronze (hardware); steel (hammer/tools) |

### Equipment (as depicted in the reference sheets)
- **Heavy charcoal travel / wool coat**; **deep burgundy mountain cloak** with
  hood.
- **Reinforced leather smith's apron** over heavy leather work gear.
- **Tool belts & pouches**, **thick mountain boots**, **fingerless gloves**, and
  **various blacksmith tools attached to his belt** (calipers, chisels, punches,
  whetstone, measuring ruler, small hammer, chalk, pencils, nails, tool roll —
  per the "Tools of the Trade" panel).
- Everything **repaired, used, loved, practical** — nothing ornate.
- See also [`Equipment.md`](Equipment.md).

### Weapon — The Forge Hammer *(canonical appearance)*
- A **practical blacksmith's hammer adapted for combat** — a heavy squared head
  with a maker's mark, a **long wooden handle**, well-maintained, showing
  **generations of repair.** It **doubles as tool and weapon.**
- **Avoid oversized fantasy proportions** — it must read as a real smith's hammer,
  not a cartoon warhammer.
- (Gameplay: his **Field Forge** constructs and skill trees — `docs/heroes/TORREN.md`.)

### Signature Item — The Founder's Compass *(canonical)*
- **What it is NOT:** a navigation compass.
- **What it is:** an ancient **master craftsman's measuring compass** — for
  precision, design, and discovery.
- **History:** forged by the **founder of Clan Ironhall**; passed from one Clan
  Master to the next. **Every generation used it, repaired it, and engraved their
  name inside** one arm.
- **Appearance:** **darkened steel with bronze accents**, hand-forged hinges,
  **one leg replaced centuries ago**, smooth from centuries of use; carried in an
  **old leather case.**
- **Engraved lineage inside (canonical, oldest → newest):** Durin · Barag ·
  Thorek · Borin · Hadrin · Orin · **Durgan** … *(final blank space reserved
  for)* **Torren Ironhall.**
- Full lineage/clan context:
  [`Clan Ironhall`](../world/factions/clan_ironhall.md#the-masters-lineage-and-the-founders-compass).

### Secondary Heirloom — The Ironhall Master's Seal *(canonical)*
- **Meaning:** the **right to place Clan Ironhall's mark** on completed works of
  true craftsmanship.
- **State:** **retired after the Broken Oath** — no official Ironhall work has
  carried its mark for generations.
- **Torren:** carries the seal **wrapped in cloth** and **refuses to use it**,
  believing he **has not yet earned that right.** (He finally uses it at the end
  of [`The Empty Pedestal`](../quests/the_empty_pedestal.md).)

### Companion Quest — The Empty Pedestal
His flagship companion quest is **not** about recovering a relic — it is about
**uncovering historical truth**, asking *what matters more: keeping an oath, or
saving lives?* Torren discovers that his disgraced ancestor **Durgan Ironhall**
chose to save the kingdom's people over the relic — and that the **High King had
secretly released Durgan from his oath** in a sealed letter revealed too late.
**No historical figure is a villain; the tragedy is incomplete history.** Full
design + cast + locations:
[`The Empty Pedestal`](../quests/the_empty_pedestal.md).

### Supporting Cast (companion quest)
| Character | Role |
|---|---|
| **High Thane Borik Stoneheart** | Current High Thane; honourable, initially skeptical; **restores Clan Ironhall's honour**. |
| **Elder Hilda Forgekeeper** | Clan historian; **believes history is missing**; quietly aids Torren. |
| **Garrik Ironvein** | Torren's lifelong best friend; grounded; **sees through his jokes**. |
| **Brynja Emberforge** | Friendly rival; **starts with the official history, becomes an ally**. |
| **Master Odrin Runehammer** | Torren's gruff old forge master; **proud of him despite rarely saying so**. |
| **Durgan Ironhall** | Ancestor; **tragic hero**, not a villain. |
Full profiles: [`Clan Ironhall — Key Figures`](../world/factions/clan_ironhall.md#key-figures).

### Personality (through design)
Preserve all existing personality canon (`docs/heroes/TORREN.md`). Visually and
tonally reinforce: **warm, friendly, quick wit, terrible dwarven dad jokes,
protective, extremely dependable, humble, compassionate** — a man who **jokes to
keep the weight at bay.** The **only** time the humour vanishes is when he speaks
of **Clan Ironhall**; that contrast is intentional and must be reflected
consistently in future dialogue.

### Animation Notes
- Grounded, deliberate, weighty — a load-bearing frame; always working (repairing
  gear at camp; see hero bible's Campfire Presence).
- Physical tells: reaching for tools first when something is wrong; the humour
  dropping when clan history comes up.
- Formal reference: _TBD_ (capture during rigging).

### Modeling Notes
- Derive the 3D model from `torren_reference_v1.png` (identity + turnaround) and
  `torren_turnaround_v1.png` (poses); use the two full-body renders for
  proportions.
- Author the **forge-braided beard with iron rings** (incl. the **one shorter,
  singed braid** on the left) as a hero silhouette element.
- Model gear as **repaired, layered leather + apron + burgundy cloak**, with
  belt-hung tools; **bronze/copper hardware.**
- Model the **Forge Hammer** at realistic smith proportions; the **Founder's
  Compass** as a distinct opening measuring-compass prop with a leather case; the
  **Master's Seal** as a small cloth-wrapped stamp.
- Preserve the charcoal / deep-brown / burgundy + copper/bronze/steel palette.
- Follow the studio production targets in
  [`Character_Production_Bible.md`](Character_Production_Bible.md) /
  [`Pipeline.md`](Pipeline.md).

### UI Portrait Notes
- Lead with **face + warm amber eyes + laugh lines + forge-braided beard**; read
  as *warm, trustworthy, quietly burdened.*
- The Founder's Compass on the belt should be visible where framing allows.

### Design Rules
1. Torren reads as a **travelling master craftsman**, **never a royal dwarf**.
2. Gear is **repaired, used, loved, practical** — nothing ornate.
3. The **Forge Hammer avoids oversized fantasy proportions** — it is a real
   smith's tool adapted for battle.
4. Keep signature identity consistent: reddish-brown/ginger hair + full braided
   beard (one singed braid), warm amber eyes, apron + tool belts, the **Founder's
   Compass** on the belt.
5. Humour is a coping mechanism — **grave only about Clan Ironhall.**
6. Do not contradict established canon in `docs/heroes/TORREN.md`.

> **Reconciliation notes (approved canon vs prior lore).**
> 1. **Race:** the finalized canon is **Dwarf**. This supersedes the earlier
>    "Human" value in [`docs/characters/torren.md`](../characters/torren.md),
>    which has been corrected. (The hero bible never specified a race.)
> 2. **Height:** the sheet's Scale Reference panel lists approximate figures for
>    the whole party; **Torren 4'5" (135 cm)** is canonical here. The panel's
>    numbers for other characters are illustrative and do **not** override their
>    own established heights (e.g. Eleanor's 5'6"/167 cm in her canon entry).
> 3. **Companion quest vs personal Core Wound:** *The Empty Pedestal* authors his
>    **clan-honour** companion arc. It is **complementary to** — not a replacement
>    for — his reserved personal Core Wound (the **Cold Clasp**,
>    [`TORREN.md`](../heroes/TORREN.md)). Both remain canon.

### Revision History
| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-06 | Established Torren's canonical visual identity and **imported approved reference artwork** (unaltered): `torren_reference_v1.png` (master sheet), `torren_turnaround_v1.png` (poses), `torren_fullbody_v1.png`, `torren_fullbody_alt_v1.png`. Canon: **Dwarf** Master Blacksmith, ~85 / 4'5" (135 cm), reddish-brown/ginger hair + full forge-braided beard (one singed braid), warm amber eyes, charcoal/deep-brown/burgundy + copper/bronze palette, repaired travelling smith gear, the **Forge Hammer**, the **Founder's Compass** (lineage Durin→…→Durgan→Torren) and retired **Ironhall Master's Seal**. Authored **Clan Ironhall** and the **The Empty Pedestal** companion quest with supporting cast + locations. Corrected prior race (Human→Dwarf); personal Core Wound (Cold Clasp) preserved. |

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
