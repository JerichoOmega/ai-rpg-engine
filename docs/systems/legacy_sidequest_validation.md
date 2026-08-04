# Framework Validation — The Jammed Mill (Side Quest)

> Purpose: prove the Legacy Quest Framework scales *down* to ordinary RPG
> content, not just epic Legacy Questlines — **without adding engine code**.
> Date: 2026-06.

## The quest (deliverable)

`legacy/data/the_jammed_mill.json` — a ~5–15 minute side quest:

* **One NPC:** Miller Bramwell (original side-quest character; not tied to any
  approved canon — renameable in the JSON).
* **One small location:** a riverside village mill / its sluice gate.
* **One simple problem:** the waterwheel is jammed by driftwood and a nest of
  corrupted river-vermin.
* **One speech check:** `mill.cause.insight` (Insight) — reading the jam;
  plus an optional Persuasion check to calm the miller.
* **One optional combat encounter:** driving off the corrupted vermin
  (`multi_stage`, non-signature) — fully skippable via the coax path.
* **One meaningful choice:** accept the miller's hard-spared silver, or waive
  it toward the harvest fair (gold-ish vs. reputation/standing).
* **One visible Living-World consequence:** the mill is repaired →
  `millers_village` gains fresh flour & bread stock, ambient dialogue and
  tavern rumors change, prosperity rises; the generous choice adds a distinct
  rumor and regional reputation. All immediately observable through the
  reaction query API.

## Files modified

| File | Change | New engine feature? |
|---|---|---|
| `legacy/data/the_jammed_mill.json` | New quest (pure data). | No |
| `legacy/quests/the_jammed_mill.py` | Thin loader + banter. | No |
| `legacy/framework/registry.py` | Registered the quest (one line). | No |
| `legacy/data/living_world_reactions.json` | Added `mill_repaired` / `mill_generous_remembered` mappings (pure data). | No |
| `legacy/framework/quest_framework.py` | Added optional `Quest.category` (default `"legacy"`). | **Generality refactor** (backward-compatible), not a new system |
| `legacy/menu.py` | Menu now shows `[category]` and reads "QUESTS". | Presentation only |
| `legacy/harness.py` | Two new scenarios (both branches). | No |
| `legacy/validator.py` | Validates the 4th quest. | No |

## Confirmation: no new engine systems required

The side quest reuses, unchanged: **Quest Framework, Dialogue, Speech
Checks, Companion Banter, Reputation, Living World + reactions,
Consequences, Save/Load, Quest Tracking, optional Multi-Stage Encounter,
and stage branching (`goto_stage`)**. The only code touched in the framework
was a one-field, backward-compatible `category` addition — the prompt
explicitly invited generality refactors of anything too tightly coupled to
Legacy Questlines.

## Verification

* `python legacy/harness.py` → **8/8** (incl. `mill_generous_no_combat`,
  `mill_paid_with_combat`).
* `python legacy/validator.py` → **PASS: 0 errors across 4 quests**.
* Before/after Living-World check shows the world visibly reacting
  (merchant stock, rumors, ambient dialogue, regional reputation) and
  `world_state` round-trips through JSON.
* Independent testing-agent pass: 100%, 0 issues.

## Lessons learned about the framework

1. **It scales down cleanly.** A trivial quest is just a short stage list; no
   ceremony, no Legacy-specific scaffolding. Authoring was JSON-only.
2. **The one real coupling was cosmetic** — the framework had no notion of
   quest *category* and the menu was labelled "Legacy Questlines". A single
   optional field (`category`) fixed both without breaking saves or APIs.
   Worth having found this now rather than after dozens of quests.
3. **Living World reactions are the star reuse win.** Making a consequence
   *visible* was a data edit (one flag → reactions), not code. This is
   exactly the "add JSON, not engine" property we wanted.
4. **The validator paid for itself immediately** — it caught nothing here
   because the ungated-fallback / objective-coverage rules were followed, but
   it gave instant confidence that the new content had no soft-locks.
5. **Optional combat via `goto_stage` branch stages** is a clean, reusable
   pattern (coax vs. fight) other side/companion quests can copy directly.

**Conclusion:** the architecture is validated at both large (Legacy) and
small (side) scales. Ready for content creation — Quest #4 and beyond need
JSON + dialogue + design, not engine work.
