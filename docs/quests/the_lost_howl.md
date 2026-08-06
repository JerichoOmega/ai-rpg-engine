# The Lost Howl — Ronan Companion Quest (Canonical)

> **Status:** Canonical design (2026-06). Ronan's flagship companion quest.
> **Canonical title:** **The Lost Howl** (supersedes any prior working titles;
> earlier notes are internal development history only).
> Character: [`docs/heroes/RONAN.md`](../heroes/RONAN.md) ·
> [`docs/canon/Characters.md#ronan`](../canon/Characters.md#ronan).
> World: [`The Hidden Pack`](../world/hidden_pack.md). Emotional counterpart:
> [`Eleanor`](../canon/Characters.md#eleanor).
> Design/narrative documentation only — **no gameplay systems, combat, or save
> formats are changed by this document.** Reserved details use `_TBD_`.

---

## Core Theme — *What makes a family?*
Where Torren's quest ([`The Empty Pedestal`](the_empty_pedestal.md)) is about
**honour** and Talos's is about **duty**, Ronan's is about **belonging,
acceptance, and chosen family.** The Lost Howl asks a single question and answers
it through the people around him: *what makes a family?*

## The Hidden Pack — Warden tradition (expanded canon)
> **Additive refinement — reconciled with [`hidden_pack.md`](../world/hidden_pack.md).**
> The Hidden Pack remains **hidden from the wider world** (their existence is not
> common knowledge; the isolation-vs-coexistence debate about engaging *human*
> communities is preserved intact). What The Lost Howl **adds** is their purpose
> toward *their own kind*: the Pack is **not merely a tribe hiding from humanity —
> it is a quiet network of Wardens who locate and protect newly awakened
> werewolves** before fear, hunters, or isolation destroy them. **Their mission is
> rescue, not conquest.** Rescuing lone wolves is fully compatible with staying
> hidden — they extract and shelter quietly.

**Highest law:** *"No wolf is left alone."*

**Philosophy — "Know the beast."** The Pack does **not** teach members to suppress
the wolf, nor to surrender to it. The wolf is **neither curse nor blessing — it is
simply part of who they are.** The path to control is **understanding, not fear.**

## Structure
### Act I — The Accusation
Reports spread of a dangerous beast attacking frontier settlements. Evidence
initially points toward **Ronan** — and even Ronan begins to fear he has
unknowingly lost control.

### Act II — The Inconsistencies
The investigation reveals the story doesn't hold: **disappearing victims,
conflicting tracks, unusually intelligent attacks, and signs of multiple wolves.**
The party gradually realizes the truth is more complicated than "Ronan did it."

### Act III — The Wardens
The **Hidden Pack** is discovered. Contrary to the rumours, they have been
**protecting** the settlements, not threatening them — and they have been
**pursuing the true source** of the attacks themselves.

## Major Twist — The Lost Wolf
The "monster" is **not an evil werewolf.** It is **Bram** — a **solitary werewolf
who awakened completely alone** — no mentor, no guidance, no family, no one to
teach control — and has become increasingly desperate simply trying to survive.
The story **intentionally refuses to portray him as inherently evil.** The Lost
Wolf is a mirror: **exactly what Ronan himself might have become** had he never
found the party. Full design (name/look/mechanics + **playable slice**):
[`The Lost Wolf (Bram)`](../design/encounters/the_lost_wolf_bram.md).

## Final Encounter — save, don't slay *(defining design goal)*
The climax **deliberately subverts** the expected boss fight:
- **Initial objective:** *Defeat the Beast.*
- **Mid-encounter:** the **Hidden Pack Alpha arrives**, and the objective changes
  to **Protect the Lost Wolf until the Pack reaches them.**
- **The climax focuses on saving rather than killing.** This inversion is a
  **defining design goal** of the quest and must be preserved. (Any combat beats
  should follow the readability principles of
  [`the gold-standard encounter`](../design/encounters/gold_standard_sundered_span.md);
  mechanics/objective-swap implementation: `_TBD_`.) **This objective swap is
  implemented and proven as a playable slice** — `tactical/showcase_lost_howl.py`
  (compassion → rescued; murder-hobo → slain); design:
  [`The Lost Wolf (Bram)`](../design/encounters/the_lost_wolf_bram.md).

## The Hidden Pack Alpha *(major recurring NPC)*
A senior Warden — **calm, compassionate, wise, quietly exhausted; respected rather
than feared.** For decades the Alpha has found newly awakened werewolves before the
rest of the world finds them.

**Preserve these lines:**
- *"Every wolf deserves a pack."*
- When asked why they keep risking their life for dangerous werewolves:
  *"Because someone once did the same for me."*

> **Reconciliation with [`hidden_pack.md`](../world/hidden_pack.md):** Sera remains
> the Pack **Elder** (consensus leader who does not cast deciding votes). The
> **Alpha** is the leader of the Pack's **Warden/rescue tradition** — the one who
> goes out to find the lost. Whether the Alpha is Sera in another aspect, or a
> distinct senior Warden, is `_TBD_`; treat the Alpha as a distinct recurring
> figure unless a future revision merges the roles. Named identity/appearance:
> `_TBD_`.

## Ronan's Arc
Across the quest Ronan slowly realizes that **if he had never met the party, he
might have become exactly like the Lost Wolf.** His understanding of family shifts
**from survival to belonging.**

## Ending — "I already found my pack."
The Alpha offers Ronan a **permanent place among the Hidden Pack.** Ronan looks
toward **Talos, Eleanor, Corwin, Torren, Ragash, and the healer**, and answers:

> **Ronan:** *"I already found my pack."*
> **Alpha** *(smiling):* *"Then our work is done."*

This is **not a rejection** of the Hidden Pack — it is the **culmination of
Ronan's emotional journey.** (Party roster names above are as given; `Corwin` and
`the healer` cross-reference the current companion roster — reconcile with
[`docs/canon/Characters.md`](../canon/Characters.md) as the roster finalizes; any
not-yet-canon member is `_TBD_`.)

## Symbolic Reward — the Pack Token
The Hidden Pack presents Ronan with a **carved wooden wolf token.** It is **not a
rank and not a magical artifact.** It signifies one thing: *"You will always have
a home here."* Ronan **ties it beside his seed pouch.** The two items become
permanent paired symbols:
- **Seed Pouch → hope and the future.**
- **Pack Token → belonging and chosen family.**

---

## Eleanor Integration — Ronan's emotional counterpart
Eleanor's role runs throughout the quest. She is **Ronan's emotional counterpart,**
and her defining choice is language: **she never separates Ronan from the wolf.**
She always speaks of him simply as **"you"** — never **"the wolf."** This
distinction is intentional and should be preserved in all dialogue. Ambient
travel/campfire lines that build this bond across the journey:
[`Ronan–Eleanor Banter`](../design/companions/ronan_eleanor_banter.md).

### Campfire Conversation *(defining scene)*
> **Ronan:** *"Have you ever wished you weren't born different?"*
> **Eleanor:** *"No."* *(a pause)* *"I've wished the world was kinder."*

### The Lost Wolf — "Look at his eyes"
During the final confrontation Eleanor notices what everyone else misses:
> **Eleanor** *(quietly):* *"Look at his eyes."*
> *"He's begging someone to stop hurting him."*
Her compassion helps change the course of the encounter.

### The Rescue
Rather than attacking, **Eleanor walks toward the frightened werewolf with empty
hands:**
> **Eleanor:** *"You don't have to be afraid anymore."*
She succeeds **not through magic but through compassion** — and her courage gives
Ronan the courage to step forward himself.

### Hidden Pack Dialogue *(preserve)*
> **Alpha:** *"You don't fear wolves."*
> **Eleanor:** *"I've only ever met people."*
This line summarizes Eleanor's entire worldview.

### Final Conversation *(defining Eleanor moment)*
> **Ronan:** *"How did you know he wouldn't hurt you?"*
> **Eleanor** *(smiling):* *"I didn't."*
> *"Sometimes compassion is a choice, not a certainty."*

### Final Symbolic Moment
After Ronan receives the Pack Token, Eleanor takes a **braided green cord** she has
woven over the journey and, without fanfare, **threads the token beside Ronan's
seed pouch:**
> **Eleanor:** *"Now they travel together."*
The Seed Pouch is hope; the Pack Token is belonging — **Eleanor simply helps Ronan
carry both.**

---

## Integration with the companion narratives
- **Theme triangle:** Talos = **duty**, Torren = **honour**, Ronan = **belonging**.
  The three flagship companion quests deliberately explore different faces of what
  a person owes and is owed.
- **Hidden Pack reuse:** The Lost Howl uses the established Hidden Pack cast (Sera,
  Horath, Lyss, Davan, Tae) and their isolation/coexistence debate as the social
  backdrop; it **adds** the Warden/rescue tradition, the Alpha, and the Lost Wolf
  without overwriting that material.
- **Eleanor pairing:** formalizes Eleanor as Ronan's emotional counterpart,
  consistent with her hope/compassion identity in
  [`Characters.md#eleanor`](../canon/Characters.md#eleanor).
- **Seed Pouch continuity:** the Pack Token joins — never replaces — the existing
  symbolic, nonmagical seed pouch.

## Revision History
| Date | Change |
|---|---|
| 2026-06 | Authored *The Lost Howl* (canonical title): theme (*what makes a family?*), three-act structure, the Lost Wolf twist, the save-don't-slay final encounter, the Hidden Pack **Alpha** NPC + preserved lines, Ronan's arc, the *"I already found my pack"* ending, the carved-wolf **Pack Token** reward, and full **Eleanor integration** (campfire, "look at his eyes", the empty-handed rescue, "I've only ever met people", "compassion is a choice", the braided-cord final moment). Additively expanded the Hidden Pack's **Warden/rescue tradition** and philosophy (*"No wolf is left alone" / "Know the beast"*), reconciled with existing `hidden_pack.md`. Design-only; no systems changed. |
