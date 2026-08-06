# The Lost Wolf (Bram) — Design & Playable Slice

> **Status:** Canonical design (2026-06). The antagonist-who-is-not-a-villain at
> the heart of Ronan's companion quest [`The Lost Howl`](../../quests/the_lost_howl.md).
> Runtime slice: `tactical/showcase_lost_howl.py` · report
> `scripts/lost_howl_report.py` · tests `backend/tests/test_lost_howl_encounter.py`.
> Character/world cross-refs: [`Ronan`](../../canon/Characters.md#ronan),
> [`Eleanor`](../../canon/Characters.md#eleanor),
> [`The Hidden Pack`](../../world/hidden_pack.md). Design-only; no shared gameplay
> systems are modified.

## Who he is
**Name: Bram.** A young man — barely into adulthood — from a frontier steading who
**awakened as a werewolf completely alone**: no mentor, no guidance, no family, no
one to teach control. What the settlements call "the monster" is a **terrified boy
who has been surviving on instinct**, and who is a **deliberate mirror of what
Ronan himself might have become** had he never found the party. He is **not evil**;
he is *lost*. (Full name / steading of origin / fate after rescue: `_TBD_`.)

## Look
- **Human form:** gaunt and hollow-cheeked from starvation; wild, unkempt dark
  hair; **frightened, over-bright eyes**; ragged, torn clothes he has long since
  outgrown caring for; flinching, defensive body language — a cornered animal in a
  person's shape.
- **Werewolf form:** a **lean, scarred, wild-eyed wolf** — matted fur, ribs
  showing, movements jerky and desperate rather than powerful. Crucially his eyes
  read **fear, not rage** — Eleanor's canon line, *"He's begging someone to stop
  hurting him,"* must be legible in his design. He should never be drawn as a
  hulking, confident monster; he is smaller and more frantic than Ronan's form.
- **Palette:** ashen greys and dirty browns; the one warm note is the amber eyes
  shared by all werewolves. Formal reference sheet: `_TBD_` (this doc is the brief).

## The encounter — "save, don't slay" *(defining design goal)*
The climax subverts the boss fight. Implemented and proven in
`tactical/showcase_lost_howl.py`:

1. **Initial objective — *Defeat the Beast*.** The party is thrown at Bram
   believing he is the killer. He is a genuine, dangerous threat (high HP, hits
   hard, panicked) — ignoring him is not free.
2. **The twist (round 4) — the Hidden Pack Alpha arrives** and the objective
   **flips to *Protect the Lost Wolf until the Pack reaches him*.**
3. **Victory = rescue, not a kill.** The good ending fires when the **Alpha reaches
   a still-living Bram.** **Killing Bram is the tragic FAILURE state**, not the win.

### The intended solution (compassion)
- **Ronan & Talos** *subdue, don't slay*: they **taunt and body-block** to draw
  Bram's panic onto themselves and shield the others — **they never attack him.**
- **Eleanor** is the key: she **approaches with empty hands** (*"You don't have to
  be afraid anymore"*), never treating him as "the wolf." Her compassion buys the
  turns; Ronan finds the courage to step forward.
- **The Alpha** closes in to bring Bram home.

### The proof (reproducible)
`resolve()` drives the same encounter under two playstyles:

| Playstyle | Behaviour | Outcome |
|---|---|---|
| **Compassion** | guardians taunt/body-block, Eleanor approaches, nobody attacks Bram; Alpha closes in | **`rescued` (100% over 20–30 seeds)** |
| **Murder-hobo** | everyone focuses Bram to defeat "the beast" | **`slain` — the tragic failure (100%)** |

The two outcomes prove the objective genuinely inverts the normal win condition:
**the naive "kill the boss" instinct produces the tragedy the quest is warning
against, and only restraint + compassion earns the rescue.**

## Reserved details (`_TBD_`)
- Bram's full name, home steading, and post-rescue fate (does he join the Hidden
  Pack? a later cameo?).
- Formal art reference sheet for Bram (human + werewolf forms).
- The player-facing UI for the mid-fight objective swap, dialogue triggers, and
  any partial/branching outcomes (e.g., Bram wounded-but-saved).

## Revision History
| Date | Change |
|---|---|
| 2026-06 | Authored the Lost Wolf (**Bram**) — name, look, and the *save-don't-slay* climax as a **playable slice** (`tactical/showcase_lost_howl.py` + report + tests). Proven: compassion → `rescued` 100%, murder-hobo → `slain` 100% (objective swap at round 4). Design/validation only; no shared systems changed. |
