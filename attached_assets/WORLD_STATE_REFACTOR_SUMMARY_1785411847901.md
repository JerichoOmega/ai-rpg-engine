# world_state.py — Typed Data Model Refactor

## Design decision: dict-subclassed sections, not plain dataclasses
`save_system.py` calls `json.dump(world_state, ...)` and, on load,
`world_state.clear()` / `world_state.update(...)` directly on the
`world_state` object. Plain `@dataclass` instances support neither.
At least four other reviewed modules also do direct bracket access
into nested fields (`world_state["regions"]["current_region"]`, etc.).

So each section (PlayerState, InventoryState, QuestState,
CompanionState, FactionState, RegionState, WorldConditions,
StoryMemory, HistoryState, SessionState, TimeState) is a `dict`
subclass: still a real dict (same JSON shape, same `.clear()`/
`.update()`/bracket behavior everywhere else in the codebase), plus
typed properties (`section.gold` as well as `section["gold"]`) backed
by the exact same storage. `world_state` itself stays a plain
top-level `dict`, required by `save_system.py`.

## Section responsibilities (also documented in-file)
| Section | Owns |
|---|---|
| PlayerState | name/class, level/xp, hp/max_hp, gold, combat modifiers |
| InventoryState | carried items (+ flagged duplicate gold field) |
| QuestState | active/completed/failed quest name lists |
| CompanionState | party membership, relationship/loyalty per companion |
| FactionState | reputation **only** (not full faction stats) |
| RegionState | current/discovered regions, faction control per region |
| WorldConditions | world_chaos, active_disasters |
| StoryMemory | major_choices, important_flags |
| HistoryState | major_events log |
| SessionState | session_count, last_session_summary |
| TimeState | day/hour/season |

## About "Campaign State", full "Faction State", and "NPC State"
The task asked for five clearly separated sections including Campaign,
Faction, and NPC state. In this codebase, those three already live
outside `world_state.py`:
- Campaign state → `campaign_manager.py` (`campaign_state`)
- Full faction data (stats, alliances, wars) → `faction_manager.py` (`FACTIONS`)
- NPC roster/dialogue data → `npc_manager.py` (`NPCS`)

`world_state.py` never held full versions of these — only a faction
*reputation* dict and party/companion data. I did not duplicate
campaign/faction/NPC state into this file, since that would create a
second source of truth for data that already has one owner (the
opposite of the goal), and those three files were not reviewed as part
of this task. This is called out explicitly in the module docstring so
it isn't a silent gap.

## Duplicate/unused fields: flagged, not removed
Two candidates found, both **left in place**:
- **`inventory.gold` duplicates `player.gold`** — nothing in the 9
  files I've reviewed reads/writes `inventory["gold"]`, only
  `player["gold"]`. Likely dead, but `inventory.py`/`shop.py`/
  `economy_manager.py` weren't reviewed and might use it.
- **`companions.relationships` / `companions.loyalty`** — declared,
  never populated or read in any reviewed file. `companions.py` is the
  likely (unreviewed) consumer.

I did not remove either, because doing so without checking the ~40
files I haven't read risks a silent gameplay regression that no amount
of "the code still runs" checking would catch. Both are flagged with
a specific recommended grep/manual-check in the file's docstring —
that's a five-minute follow-up, not a re-review of the whole repo.

## Verification actually performed
Unlike the last refactor (dm_brain.py), `world_state.py` has **zero
external imports** — so I could genuinely execute it, not just check
syntax. I ran, in a real Python process:

1. `world_state` is still a plain `dict` (not a subclass instance)
2. `json.dumps(world_state)` succeeds
3. Top-level keys match the original schema exactly (12 keys)
4. Every nested section's keys match the original nested dict literals exactly
5. Bracket read/write works, including adding a brand-new faction key
   dynamically (`world_state["factions"]["new_faction"] = 0`), matching
   how `faction_manager.py` actually does it
6. Attribute access (`player.gold`) and bracket access
   (`player["gold"]`) read/write the identical value
7. The exact `save_system.py` pattern — `json.dumps` → `json.loads` →
   `world_state.clear()` → `world_state.update(...)` — round-trips
   correctly
8. `save_system.py`'s `validate_save()` required-sections check passes
9. All six module-level functions (`update_world_state`,
   `discover_region`, `remember_choice`, `activate_world_event`,
   `remember_major_event`, `set_current_region`) behave identically to
   the original implementation

All 9 checks passed. I also caught and fixed a `SyntaxWarning` (stray
regex-style backslashes in a docstring) that `-W error` turned up.

## What I could NOT verify
I could not run the full engine (`main.py`) — the other ~40 modules it
imports (`campaign_manager`, `encounter_generator`, `npc_manager`,
etc.) aren't available in my sandbox and weren't part of this review.
The 9-point check above proves `world_state.py` itself is behaviorally
identical and save/load-safe in isolation; it does not prove every
other file's direct field access still gets exactly what it expects.
Before trusting this in production:
```bash
grep -rn "world_state\[" --include="*.py" .
```
and spot-check a sample of the hits against the section classes above
— they should all still resolve, since every original key name is
preserved, but this is worth a human pass given the file count.

## How to apply
```bash
cd /path/to/ai-rpg-engine
cp /path/to/downloaded/world_state.py ./world_state.py
git add world_state.py
git commit -m "Refactor world_state.py into typed, dict-backed section classes

- Replaced raw nested dict literals with documented dict-subclass typed
  sections: TimeState, PlayerState, InventoryState, QuestState,
  CompanionState, FactionState, RegionState, WorldConditions,
  StoryMemory, HistoryState, SessionState.
- Each section supports both attribute access (section.field, typed,
  for new code) and bracket access (section[\"field\"], unchanged, for
  every existing call site elsewhere in the codebase) against the same
  underlying storage.
- world_state itself remains a plain top-level dict (required by
  save_system.py's world_state.clear()/update() calls).
- All original top-level and nested keys preserved exactly -- save/load
  shape is byte-for-byte compatible with existing save files.
- Documented that Campaign State, full Faction State, and NPC State
  already live in campaign_manager.py / faction_manager.py /
  npc_manager.py respectively and were intentionally not duplicated
  into this file.
- Flagged (not removed, pending verification against unreviewed files):
  duplicate inventory.gold vs player.gold, and unused-looking
  companions.relationships / companions.loyalty.
- Verified in isolation: json save/load round-trip, bracket access,
  dynamic faction-key addition, attribute/bracket sync, and all six
  module-level functions behave identically to the pre-refactor version."
git push
```
As before, I don't have push access to this repo, so you'll need to
run these yourself, and I'd strongly recommend running `main.py` for a
real playthrough (or at minimum a save → load → save cycle against the
existing `save_data.json`) before merging, given the unreviewed files
this touches indirectly.
