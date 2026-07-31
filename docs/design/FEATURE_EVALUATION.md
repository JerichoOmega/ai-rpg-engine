# Feature Evaluation Checklist

> **Canon Status:** CONFIRMED — established July 2026.
> **Authority:** Every proposed feature — gameplay system, content category, UI addition, simulation layer — must pass through this checklist before implementation begins. It operationalizes [`CORE_DESIGN_PILLARS.md`](CORE_DESIGN_PILLARS.md) and [`SCOPE_PROTECTION.md`](SCOPE_PROTECTION.md).
> **Cross-references:** [`CORE_DESIGN_PILLARS.md`](CORE_DESIGN_PILLARS.md) · [`SCOPE_PROTECTION.md`](SCOPE_PROTECTION.md) · [`docs/systems/quests.md`](../systems/quests.md) (the equivalent test for quests)

---

## The Checklist

Answer all seven in writing before building:

| # | Question | What a good answer looks like |
|---|---|---|
| 1 | **What player problem does this solve?** | A specific moment of confusion, boredom, or missed opportunity — not "it would be cool" |
| 2 | **Which Core Design Pillar does it reinforce?** | At least one named pillar from [`CORE_DESIGN_PILLARS.md`](CORE_DESIGN_PILLARS.md), with the pillar's test applied |
| 3 | **Does it affect the World State?** | Names the state categories it reads or writes ([`world_state/WORLD_STATE_SYSTEM.md`](world_state/WORLD_STATE_SYSTEM.md)); features that touch nothing persistent are suspect |
| 4 | **Does it improve player immersion?** | Deepens the sense of a lived-in, reactive world rather than adding UI or bookkeeping |
| 5 | **Can players clearly understand it?** | Explainable in two sentences; its effects are visible and communicated ([`PLAYER_COMMUNICATION.md`](PLAYER_COMMUNICATION.md)) |
| 6 | **Is it worth delaying release?** | The honest cost in schedule and complexity is stated and accepted |
| 7 | **Would the game noticeably suffer if this feature were removed?** | The removal test — the same test quests must pass. If no one would notice, do not build it |

## The Rule

**If the answer to several of these is "No," the feature is postponed** — recorded, not rejected. Log deferred features with their checklist answers so they can be revisited when the answers change (e.g., as expansion content — see [`SCOPE_PROTECTION.md`](SCOPE_PROTECTION.md)).

## Notes

- Bug fixes, polish of existing systems, and authored content within existing frameworks do **not** require this checklist — it exists to gate *new* systems and mechanics, not to slow down deepening what exists (Pillar 9: Quality Over Quantity).
- For quests specifically, the Quest Design Philosophy criteria in [`docs/systems/quests.md`](../systems/quests.md) apply instead; for major quests, the Quest Integration Standard there also applies.

---

## Document History

| Date | Change |
|---|---|
| 2026-07-31 | Created — seven-question gate with postponement rule and exemptions. |
