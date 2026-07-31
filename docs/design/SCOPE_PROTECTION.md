# Scope Protection

> **Canon Status:** CONFIRMED — established July 2026.
> **Authority:** Binding process rule for all major feature additions. Enforces Pillar 9 (Quality Over Quantity) of [`CORE_DESIGN_PILLARS.md`](CORE_DESIGN_PILLARS.md); applied together with [`FEATURE_EVALUATION.md`](FEATURE_EVALUATION.md).

---

## The Rule

**Before adding any major feature, first ask:**

| Question | If the answer is unfavorable… |
|---|---|
| **Can an existing system accomplish the same goal?** | Extend the existing system instead. The project already has deep systems for state ([`world_state/`](world_state/README.md)), quests, reputation, journal, events, and companions — most "new system" ideas are new *content* for an old system |
| **Can this idea be implemented as an expansion instead?** | Record it as post-release content and defer. Nothing is lost by shipping the core first |
| **Does this increase development complexity more than player enjoyment?** | Defer. Complexity is paid on every future feature; enjoyment is paid once |
| **Does this strengthen the Living World?** | If it doesn't deepen the world's reactivity, persistence, or believability, it is decoration — defer |

**If the answers do not clearly favor building it now, defer it.** Deferral is recorded, not forgotten: keep the idea with its answers so it can be re-evaluated when circumstances change.

## What Counts as "Major"

New mechanics, new simulation layers, new content *categories* (not new content within an existing category), new UI surfaces, and anything touching the save schema. Authored content inside existing frameworks — quests, NPCs, handouts, encounter entries, lore — is not gated by this document.

## Why This Exists

The project's identity is a small number of deeply developed systems and places ([`../world/WORLD_BIBLE.md`](../world/WORLD_BIBLE.md) World Philosophy). Every deferred feature protects the depth of an existing one. The most common failure mode of ambitious RPG projects is not bad features — it is too many good ones.

---

## Document History

| Date | Change |
|---|---|
| 2026-07-31 | Created — four gate questions, definition of "major," and deferral policy. |
