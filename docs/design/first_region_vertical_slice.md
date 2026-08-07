# The Frontier — First-Region Vertical Slice (Design)

> **Status:** Vertical-slice **design/plan** (2026-06). Additive; **no gameplay,
> combat, AI, saves, or data changed by this document.** It stitches the *existing*
> companions, companion quests, encounter definitions, and playable tactical
> showcases into one coherent first-region experience and pacing plan.
>
> **Scope honesty:** the tactical **set-pieces already exist and are headless-tested**
> ([`showcase.py`](../../tactical/showcase.py), [`showcase_forge.py`](../../tactical/showcase_forge.py),
> [`showcase_lost_howl.py`](../../tactical/showcase_lost_howl.py)); the seven
> encounter definitions exist in [`encounters.json`](../../tactical/data/encounters.json).
> This doc is the **connective design** that sequences them. A single fully-interactive
> region build (menus/flow wiring end-to-end) is a **follow-up** and is marked `_TBD_`
> where it depends on new implementation.

## Why the Frontier
[`WORLD_BIBLE.md`](../world/WORLD_BIBLE.md) establishes **the Frontier** as *"where
most campaigns begin"* — weak institutions, visible Corruption, constant monster
activity, and a Mages/Adventurers Guild presence. It is the canonical first region.
Authored travel encounters live in [`frontier_encounters.md`](../systems/frontier_encounters.md).

## Slice goals
1. **Teach the combat pillars** in order (positioning → priority → coordination →
   pressure → terrain → escalation) using the bestiary's one-lesson-per-enemy design
   ([`enemies/README.md`](enemies/README.md)).
2. **Introduce the party** and land each companion's *philosophy* through a signature
   beat, not exposition.
3. **Seed every companion quest** so the region ends with clear threads pulling
   forward — culminating in one fully-realized companion questline as the slice's
   emotional spine.
4. **Show the Corruption spreading** so the stakes escalate by the finale.

## Pacing — beats and their tactical anchors
Ordered so each fight teaches one new idea before combining them. Anchors reuse
existing encounters/showcases; companion beats land their philosophy.

| # | Beat | Teaches | Tactical anchor (existing) | Companion focus |
|---|---|---|---|---|
| 1 | **Road in** | Positioning & spacing | `forest_wolf_pack` ([wildlife](enemies/wildlife.md)) | Ronan reads the woods (Belonging seed) |
| 2 | **Ambush on the road** | Cover, kill the leader | `roadside_ambush` ([bandits](enemies/bandits.md)) | Talos — duty; protect the vulnerable |
| 3 | **The refugee settlement** | Protect / civilian rescue | *(recruitment beat)* | **Maeve Ashwood** — [A Light in the Ashes](../quests/a_light_in_the_ashes.md); she won't leave until it can stand |
| 4 | **The broken crossing** | Terrain, elevation, readability | **The Sundered Span** ([`showcase.py`](../../tactical/showcase.py); [design](encounters/gold_standard_sundered_span.md)) | Party coordination; goblin coordination ([goblins](enemies/goblins.md)) |
| 5 | **Hold the forge** | Building vs. brawling; use the environment | **The Forge Stand** ([`showcase_forge.py`](../../tactical/showcase_forge.py); [design](encounters/forge_stand_torren.md)) | **Torren** — [The Empty Pedestal](../quests/the_empty_pedestal.md) seed (Honour & Legacy) |
| 6 | **The investigator's warning** | Battlefield awareness / hidden info | *(investigation beat; mechanics `_TBD_`)* | **Corwin** — [The Silent Witness](../quests/the_silent_witness.md) seed (Truth & Discovery) |
| 7 | **The corrupted woods** | Escalation of the familiar | `corrupted_incursion` ([corrupted](enemies/corrupted.md)) | Eleanor — hope under pressure; Ragash — loyalty tested |
| 8 | **The Lost Howl (Ronan's climax)** | Save, don't slay | **The Lost Wolf (Bram)** ([`showcase_lost_howl.py`](../../tactical/showcase_lost_howl.py); [design](encounters/the_lost_wolf_bram.md)) | **Ronan** — [The Lost Howl](../quests/the_lost_howl.md); the slice's emotional spine |
| 9 | **The Corruption Avatar (finale)** | Don't tunnel the boss — break its wards first | **The Corruption Avatar** ([`showcase_corruption_avatar.py`](../../tactical/showcase_corruption_avatar.py); [design](encounters/the_corruption_avatar.md)) | **Whole party** converges; Corwin's evidence exposes the source |

> **Pacing note:** Ronan's Lost Howl is the *emotional* climax; the Corruption
> Avatar is the *tactical* climax the whole chapter builds toward. Bram's rescue
> and the Hidden Pack's acceptance resolve **before** the party turns to the
> heart of the blight, so the companion arcs **feed into** the finale rather than
> competing with it. The Avatar's identity is canonically `_TBD_` — a
> manifestation of The Corruption; the region is cleansed, but its true source is
> left unresolved for future acts.

*(Undead/orcs/constructs — `ruins_undead`, `orc_warband`, cave/ruin set-pieces — are
available as optional side content for players who explore, teaching priority and
pressure without gating the main line.)*

## Companion recruitment & philosophy landing
The slice is designed so each companion **arrives through a beat that proves their
philosophy** rather than a menu:
- **Ronan (Belonging)** — present from the road; his arc anchors the finale.
- **Talos (Duty)** — steps between danger and the defenceless at the ambush.
- **Maeve Ashwood (Compassion)** — met holding the settlement together; recruited via
  [A Light in the Ashes](../quests/a_light_in_the_ashes.md) (refuse-to-leave preserved).
- **Torren (Honour & Legacy)** — met at the forge stand he refuses to abandon.
- **Corwin (Truth & Discovery)** — the one who *noticed* the corruption first.
- **Eleanor (Justice & Hope)** & **Ragash (Loyalty)** — threaded through the corrupted-woods
  escalation; full recruitment beats `_TBD_` per their questlines.

Full roster/quest map: [`companion_quests_index.md`](../quests/companion_quests_index.md).

## Difficulty & readability curve
Follows the gold-standard readability of [The Sundered Span](encounters/gold_standard_sundered_span.md):
trivial/low threat early (wolves, a lone boar), moderate mid (bandit leaders, goblin
coordination), high at the corrupted/finale beats. One new mechanic per beat; combine
only after each is taught. No difficulty spikes that outrun what the player has learned.

## What exists vs. what's `_TBD_`
- **Exists & playable/tested (headless):** Sundered Span, Forge Stand, Lost Wolf,
  **and the Corruption Avatar finale**; the 7 encounter definitions; 76 bestiary
  units; the **end-to-end Frontier flow with interactive player-choice scenes**
  ([`tactical/frontier.py`](../../tactical/frontier.py),
  [`scripts/play_frontier.py`](../../scripts/play_frontier.py)). Recruitment and
  investigation beats are now **real choices with branching consequences** (flags,
  clues, rewards, and finale `preparedness`) — no permanent companion loss; the
  golden resolution always stays reachable.
- **`_TBD_` (follow-up):** the Corruption Avatar's identity/lore; presentation-layer
  (menu/UI) wiring beyond the terminal runner; Eleanor/Ragash bespoke recruitment
  scenes; save/flow integration; a hand-built finale battlefield for a full build.
  None of the reserved lore is invented here.

## Reactive Combat (pillar) in the slice
Every combat beat is a teaching ground for the **Reactive Combat** pillar
([`../design/REACTIVE_COMBAT.md`](../design/REACTIVE_COMBAT.md)): the wolf-pack flank, the
bandit leader opening, the forge environment, and the finale wardstones are all
**opportunities** the party recognizes and capitalizes on for shared **Resolve**. The slice's
onboarding should introduce Resolve, the time-slow decision prompt, and the first authorized
reaction here. Wiring is Planned Additive (`_TBD_`).

## Validation notes
This is design documentation only. It changes no engine, data, AI, or save; it
references existing, separately-tested set-pieces. Building the interactive region is
a scoped follow-up that should proceed **incrementally with tests green after each
step**, per [`GODOT_MIGRATION_PLAN.md`](../architecture/GODOT_MIGRATION_PLAN.md) §5 and
the project's additive workflow.

## Document History
| Date | Change |
|---|---|
| 2026-06 | Authored the Frontier first-region vertical-slice design: 8-beat pacing stitching existing encounters + the three playable showcases + companion philosophy/recruitment beats, with a readability/difficulty curve and an explicit exists-vs-`_TBD_` scope split. Documentation-only; no systems changed. |
| 2026-06 | Added the 9th beat — **The Corruption Avatar** regional finale (identity `_TBD_`) — and updated the flow to reflect **interactive player-choice** recruitment/investigation scenes with branching consequences and finale `preparedness`. Reflects implemented code/tests; additive. |
