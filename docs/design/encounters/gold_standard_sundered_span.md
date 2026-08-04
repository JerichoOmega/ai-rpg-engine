# Gold-Standard Encounter — "The Sundered Span"

**Status:** COMPLETE, independently verified (2026-06).
**Implementation:** `tactical/showcase.py` · **Tests:** `backend/tests/test_showcase_encounter.py` (19)
**Play it:** `python scripts/play_showcase.py` · **Demo/verify:** `python scripts/showcase_report.py`

This is the **reference encounter** for Elyndor — the single hand-built battle
that demonstrates every canonical combat pillar at once. It is not a template to
mass-produce; it is the bar every future encounter is measured against. All
Encounter Design Bible principles below are *derived from what makes this fight
work*, and are backed by the independent verification suite.

---

## 1. The fight at a glance

A four-hero party (Guardian, Ranger, Mage, Rogue — 100 HP total) is ambushed at
a ravine bridge by a five-goblin raiding party (148 HP total) of **five distinct
AI archetypes**: a buffing Warlord (commander), a healing Shaman (support), a
spear-wielding Bridge Warden (defender), a Ridge Sniper on high ground
(skirmisher), and a Corrupted Raider (brute).

The goblins are **armoured** (armour 1–5) and hit hard (6–14) into squishy,
armour-less heroes who chip for only 3–8 with a basic swing. The math is
deliberate:

> **Button-mashing loses. Tactics win.**

Verified: mindless attacking loses **30/30** seeds; the reference tactician plan
wins **~23/30 (77%)**, with an average of ~2 of 4 heroes surviving. The battle
resolves decisively in ~13 rounds — no stalemates, no infinite loops.

---

## 2. Every pillar, and the decision it creates

Each pillar is physically instantiated on the map (asserted by
`TestPillarStructure`) and cited from `showcase.pillar_manifest()`:

| Pillar | Feature on the map | Decision it forces |
|---|---|---|
| Battlefield is a character | Ravine + bridge chokepoint + southern ford | Cross fast and exposed, or slow and safe? |
| Difficult terrain | Forest (2), water ford (3), hills/cliff (2) | Pay movement for cover/height, or stay mobile? |
| Cover | Half (trees), full (wall, boulders) | Advance behind cover vs the sniper |
| Elevation | Mid-field hill + SW cliff; enemy NE ridge | Take the hill for the to-hit / LOS edge |
| Line of sight | Trees/walls/boulders block; height sees over | Break the sniper's LOS or out-elevate it |
| Movement & AP | Wide field, chokepoint, squishy back line | Ration move vs action under threat |
| Facing / flank / opportunity | Armoured foes; melee raiders chase | Flank for rear damage; don't provoke |
| Prepare reactions | Guardian counter / ranger shot / rogue evade | Hold the span behind prepared reactions |
| Abilities & cooldowns | Signature skills on heroes + warlord/shaman | Abilities punch armour that basics can't |
| Items | A healing potion per hero (+ antidote) | Spend the party's only sustain well |
| AI personalities | 5 distinct profiles | Read intent; kill the healer/warlord first |
| Battlefield evolves | Oil slicks + explosive barrel by the warlord | Ignite to deny ground — then respect the fire |
| Information before commitment | Hit/move/ability previews | No blind moves; every threat is legible |
| Companion party | 4 complementary roles | Win by combined arms, not one hero |
| Multiple solutions | Four+ viable plans | Several distinct strategies all contribute |

---

## 3. Why it succeeds (the design principles)

These are the transferable rules for the Encounter Design Bible.

1. **Tune the math so tactics matter more than trades.** Give enemies enough
   armour/HP that a basic swing is *inefficient*, so flanking (rear ×1.25),
   high ground (+10% hit, +1 dmg), abilities (backstab 14, aimed shot 12), and
   focus-fire become the *correct* answer — not optional flavour.
2. **Every terrain feature must change a decision.** The bridge is a chokepoint
   *because* the ravine is impassable and the ford is slow; high ground matters
   *because* a sniper contests it; the oil matters *because* the warlord stands
   on it. No decoration.
3. **Two+ ways across, two+ ways to win.** A bridge *and* a ford; ranged heroes
   shoot across while melee crosses. Focus the healer, take the height, flank
   the warlord, hold the span, or spend potions — the fight rewards several
   coherent plans (`TestSolutionLevers`).
4. **Composition tells a story the player can read.** Five roles with legible
   intent (the Warlord buffs, the Shaman heals) turn "which do I hit?" into a
   real priority puzzle. Verified: the AI *expresses* its role via abilities
   (`TestAiAndPersistence`).
5. **Give sustain, then make it scarce.** One potion per hero is enough to
   survive good play and not enough to survive bad play — the Item pillar
   becomes a tension, not a crutch.
6. **The battlefield should remember.** Fire scorches the ground and it
   persists to `world_state` — the world carries the scar of the fight.
7. **No hidden information.** The player and the AI read the same previews;
   difficulty comes from the situation, never from opacity.

## 4. Where it is deliberately hard (accepted trade-offs)

* **Environmental fire is chip/zone-control, not a nuke** (4/round, burns out in
  ~2 rounds). Igniting the oil denies the warlord his spot and chips the
  backline; it does not win the fight alone. This keeps fire a *tool*, not an
  "I-win button".
* **The ambush is genuinely dangerous.** Losing a hero or two is a normal good
  outcome. A flawless win requires strong sequencing. This is intended — a
  gold-standard fight should be beatable, memorable, and slightly scary.

## 5. Verification

* `backend/tests/test_showcase_encounter.py` — **19/19 pass**: pillar structure,
  winnable-with-tactics / not-with-mashing, each solution lever, AI role
  expression, persistence.
* Full backend suite **194 passed**; tactical harness **62/62, 0 WARN**.
* Live demo: `python scripts/showcase_report.py` (win-rate + narrated log);
  interactive: `python scripts/play_showcase.py`.
