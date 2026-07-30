"""
world_state.py
===============

Central, persistent world state for a single playthrough.

This module owns the following sections (see each class docstring
below for what it's responsible for):

    - TimeState          : the in-world clock.
    - PlayerState         : the player character's own stats/resources.
    - InventoryState       : carried items (+ a flagged duplicate, see below).
    - QuestState           : active / completed / failed quest name lists.
    - CompanionState        : party membership and per-companion
                              relationship/loyalty tracking.
    - FactionState           : per-faction REPUTATION values only.
    - RegionState             : discovered regions, current region, and
                                which faction controls which region.
    - WorldConditions          : global instability/chaos and active
                                 disasters.
    - StoryMemory                : major player choices and narrative flags.
    - HistoryState                 : a log of major world events.
    - SessionState                  : save/session bookkeeping.

--------------------------------------------------------------------
Scope note: Player / World / Campaign / Faction / NPC separation
--------------------------------------------------------------------
This refactor was asked to clearly separate Player, World, Campaign,
Faction, and NPC state. In the actual codebase, three of those five
already live in their own dedicated modules, not in world_state.py:

    - Campaign State        -> campaign_manager.py (`campaign_state`)
    - Full Faction State     -> faction_manager.py (`FACTIONS`: military
                                power, economy, alliances, wars, etc.)
    - NPC State (roster/dialogue) -> npc_manager.py (`NPCS`)

world_state.py itself only ever held a thin slice of two of those:
per-faction *reputation integers* (`factions`) and party/companion
data (`companions`). Duplicating campaign_manager.py's or
npc_manager.py's state into this file would create a second source of
truth for data that already has one owner, which is the opposite of
this task's goal and would risk real gameplay drift. So this refactor:

    - Gives PlayerState, InventoryState, QuestState, CompanionState,
      FactionState (reputation only), RegionState, WorldConditions,
      StoryMemory, HistoryState, SessionState, and TimeState each
      their own documented, typed class.
    - Leaves campaign_manager.py, faction_manager.py, and npc_manager.py
      untouched and unduplicated -- they were not reviewed as part of
      this task, and changing them was out of scope.

--------------------------------------------------------------------
Why dict subclasses instead of plain @dataclass
--------------------------------------------------------------------
Two hard constraints ruled out plain (non-dict-backed) dataclasses:

1. save_system.py calls `json.dump(world_state, ...)` directly, and on
   load does `world_state.clear(); world_state.update(loaded_data)`.
   `json.dump` can't serialize an arbitrary object without a custom
   encoder, and `.clear()` / `.update()` are dict methods a plain
   dataclass instance doesn't have.

2. Multiple other modules (faction_manager.py, memory_engine.py,
   consistency_engine.py, llm_bridge.py, dm_brain.py -- and likely
   others not reviewed as part of this task) read and write nested
   fields directly with bracket syntax, e.g.
   `world_state["factions"][name] = 0`,
   `world_state["regions"]["current_region"]`. Rewriting every call
   site across the repo was out of scope for "refactor world_state.py"
   and risks behavior changes in code this task did not review.

Every section below is therefore a `dict` subclass: it IS a dict, so
`json.dump`, `.clear()`, `.update()`, `"key" in section`, and
`section["key"]` all keep working exactly as before -- existing save
files load and save with the identical shape. Each section also
exposes its fields as typed attributes (`section.gold` as well as
`section["gold"]`) for new code; attribute and item access read/write
the same underlying storage, so they can never drift out of sync.

--------------------------------------------------------------------
Duplicate/unused fields found -- flagged, NOT removed
--------------------------------------------------------------------
The task asked to remove duplicate or unused fields. Two candidates
were found, but neither was removed, because I could not verify
against the full codebase (only 9 of ~50 files were reviewed) that
nothing else depends on them -- removing either risks a silent
gameplay regression that "verify the engine still runs exactly as
before" would not catch without a full manual playtest:

  * DUPLICATE: `player.gold` and `inventory.gold` are two independent
    counters for what looks like the same value (both start at 100).
    Nothing in the 9 files reviewed for this task reads or writes
    `inventory["gold"]` -- only `player["gold"]` is touched (e.g. by
    save_system.py's `show_save_summary()`). This strongly suggests
    `inventory.gold` is dead, but `inventory.py` / `shop.py` /
    `economy_manager.py` were not reviewed and may use it.
    RECOMMENDATION: run a repo-wide search for inventory["gold"] and
    inventory.gold (e.g. `grep -rn "inventory" --include="*.py" .` and
    inspect the hits by hand); if there are zero uses of that key
    outside this file,
    it's safe to delete `inventory["gold"]` in a follow-up commit.

  * UNUSED (possibly): `companions.relationships` and
    `companions.loyalty` are declared but never populated or read in
    any of the 9 files reviewed. `companions.py` (not reviewed) is the
    most likely place they're actually used.
    RECOMMENDATION: search companions.py for "relationships" and
    "loyalty" by hand before removing.

Both fields are preserved as-is in this refactor to keep the "no
gameplay changes" guarantee airtight.
"""


def _dict_property(key):
    """Build a property that proxies attribute access to a dict key on
    `self`. Used so each typed section supports both `section.field`
    (typed, for new code) and `section["field"]` (unchanged, for every
    existing call site in the rest of the codebase) against the exact
    same underlying storage.
    """
    def getter(self):
        return self[key]

    def setter(self, value):
        self[key] = value

    return property(getter, setter)


# =========================
# TIME STATE
# =========================
class TimeState(dict):
    """The in-world clock: current day, hour (0-23), and season."""

    def __init__(self, day=1, hour=8, season="spring"):
        super().__init__(day=day, hour=hour, season=season)

    day = _dict_property("day")
    hour = _dict_property("hour")
    season = _dict_property("season")


# =========================
# PLAYER STATE
# =========================
class PlayerState(dict):
    """
    Player State
    ------------
    The player character's own stats and resources: identity
    (name / class), level & xp progression, hp / max_hp, gold, and
    combat modifiers (attack_bonus, weapon_bonus). This is per-player
    data, as distinct from world-level or faction-level data.
    """

    def __init__(self, name="Wanderer", player_class="Adventurer", level=1,
                 xp=0, gold=100, hp=100, max_hp=100, attack_bonus=5,
                 weapon_bonus=0):
        super().__init__(
            name=name,
            level=level,
            xp=xp,
            gold=gold,
            hp=hp,
            max_hp=max_hp,
            attack_bonus=attack_bonus,
            weapon_bonus=weapon_bonus,
        )
        # "class" is a reserved word, so it can't be a Python attribute
        # name -- same limitation the original plain dict already had
        # (it was always bracket-only: world_state["player"]["class"]).
        self["class"] = player_class

    name = _dict_property("name")
    level = _dict_property("level")
    xp = _dict_property("xp")
    gold = _dict_property("gold")
    hp = _dict_property("hp")
    max_hp = _dict_property("max_hp")
    attack_bonus = _dict_property("attack_bonus")
    weapon_bonus = _dict_property("weapon_bonus")

    @property
    def player_class(self):
        """Typed alias for the "class" key (see __init__ note)."""
        return self["class"]

    @player_class.setter
    def player_class(self, value):
        self["class"] = value


# =========================
# INVENTORY STATE
# =========================
class InventoryState(dict):
    """
    Inventory State
    ---------------
    Carried items. Also currently holds a `gold` field -- see the
    module-level "Duplicate/unused fields" note above; this duplicates
    PlayerState.gold and was flagged but not removed.
    """

    def __init__(self, items=None, gold=100):
        super().__init__(items=list(items) if items else [], gold=gold)

    # Not exposed as `.items` -- that name is already dict.items(), the
    # built-in method for iterating key/value pairs. Exposing it here
    # would silently shadow that method. Every existing call site in
    # the codebase already uses bracket access (`inventory["items"]`)
    # for this field, so this is not a behavior change -- just a
    # documented limit of the typed-attribute convenience layer.
    gold = _dict_property("gold")


# =========================
# QUEST STATE
# =========================
class QuestState(dict):
    """Active / completed / failed quest name lists."""

    def __init__(self, active=None, completed=None, failed=None):
        super().__init__(
            active=list(active) if active else [],
            completed=list(completed) if completed else [],
            failed=list(failed) if failed else [],
        )

    active = _dict_property("active")
    completed = _dict_property("completed")
    failed = _dict_property("failed")


# =========================
# COMPANION STATE
# =========================
class CompanionState(dict):
    """
    Companion State
    ---------------
    Party membership and per-companion relationship/loyalty tracking.
    This is the closest thing world_state.py owns to "NPC state" --
    but it only covers party members' standing with the player, not
    full NPC data (dialogue, roster, etc.), which lives in
    npc_manager.py's NPCS dict and is out of scope for this file.

    `relationships` and `loyalty` are flagged as possibly-unused; see
    the module-level note above.
    """

    def __init__(self, party=None, relationships=None, loyalty=None):
        super().__init__(
            party=list(party) if party else [],
            relationships=dict(relationships) if relationships else {},
            loyalty=dict(loyalty) if loyalty else {},
        )

    party = _dict_property("party")
    relationships = _dict_property("relationships")
    loyalty = _dict_property("loyalty")


# =========================
# FACTION STATE
# =========================
class FactionState(dict):
    """
    Faction State (reputation only)
    --------------------------------
    Maps faction name -> player reputation (int, -100 to 100). This is
    the ONLY faction data world_state.py owns. Faction stats (military
    power, economy, alliances, wars) live entirely in
    faction_manager.py's FACTIONS dict and are not duplicated here.

    Faction names are dynamic, not fixed: faction_manager.py's
    change_reputation() adds a new key the first time an unfamiliar
    faction is referenced (`if faction_name not in world_state["factions"]:
    world_state["factions"][faction_name] = 0`). Because of this, this
    class intentionally does NOT declare one static property per
    faction -- doing so would break the ability to track reputation
    with a faction not known when the class was written. It behaves as
    a plain dict of arbitrary faction-name keys, with one typed
    convenience method added on top.
    """

    def __init__(self, **starting_reputations):
        super().__init__(**starting_reputations)

    def get_reputation(self, faction_name, default=0):
        """Typed convenience accessor; equivalent to
        `self.get(faction_name, default)`."""
        return self.get(faction_name, default)


# =========================
# REGION STATE
# =========================
class RegionState(dict):
    """
    Region State
    ------------
    Which region the player is currently in, which regions have been
    discovered, and which faction (if any) controls each region.
    `faction_control` keys are dynamic region names, same reasoning as
    FactionState above.
    """

    def __init__(self, current_region="kingdom_capital",
                 discovered_regions=None, faction_control=None):
        super().__init__(
            current_region=current_region,
            discovered_regions=(
                list(discovered_regions) if discovered_regions
                else ["kingdom_capital"]
            ),
            faction_control=dict(faction_control) if faction_control else {},
        )

    current_region = _dict_property("current_region")
    discovered_regions = _dict_property("discovered_regions")
    faction_control = _dict_property("faction_control")


# =========================
# WORLD CONDITIONS
# =========================
class WorldConditions(dict):
    """Global instability (`world_chaos`, 0-100) and any active
    world-level disasters."""

    def __init__(self, world_chaos=0, active_disasters=None):
        super().__init__(
            world_chaos=world_chaos,
            active_disasters=(
                list(active_disasters) if active_disasters else []
            ),
        )

    world_chaos = _dict_property("world_chaos")
    active_disasters = _dict_property("active_disasters")


# =========================
# STORY MEMORY
# =========================
class StoryMemory(dict):
    """Major player choices and narrative flags used for continuity
    checks (see consistency_engine.py's validate_story_memory())."""

    def __init__(self, major_choices=None, important_flags=None):
        super().__init__(
            major_choices=list(major_choices) if major_choices else [],
            important_flags=(
                dict(important_flags) if important_flags else {}
            ),
        )

    major_choices = _dict_property("major_choices")
    important_flags = _dict_property("important_flags")


# =========================
# HISTORY STATE
# =========================
class HistoryState(dict):
    """A running log of major world events (distinct from
    story_memory's *choices* -- this is *events*)."""

    def __init__(self, major_events=None):
        super().__init__(
            major_events=list(major_events) if major_events else []
        )

    major_events = _dict_property("major_events")


# =========================
# SESSION STATE
# =========================
class SessionState(dict):
    """Save/session bookkeeping."""

    def __init__(self, session_count=1, last_session_summary=""):
        super().__init__(
            session_count=session_count,
            last_session_summary=last_session_summary,
        )

    session_count = _dict_property("session_count")
    last_session_summary = _dict_property("last_session_summary")


# =========================
# CENTRAL WORLD STATE
# =========================
# world_state itself stays a plain top-level dict (not a subclass) --
# save_system.py's load_game() calls world_state.clear() and
# world_state.update(loaded_data) directly on this exact object, so it
# must remain a real dict at this level. Its values are now the typed
# sections above instead of raw nested dict literals; every existing
# key name is unchanged, so `world_state["player"]["gold"]`-style
# access everywhere else in the codebase keeps working unmodified.
world_state = {
    "time": TimeState(),
    "player": PlayerState(),
    "inventory": InventoryState(),
    "quests": QuestState(),
    "companions": CompanionState(),
    "factions": FactionState(
        kingdom=0,
        mages_guild=0,
        shadow_cult=0,
        rebels=0,
    ),
    "regions": RegionState(),
    "world_conditions": WorldConditions(),
    "story_memory": StoryMemory(),
    # Kept as a plain list (not a typed section): it's a flat event-name
    # log with no sub-fields, so there's nothing to type beyond "list of
    # strings" -- wrapping it would add a class with zero fields.
    "events": [],
    "history": HistoryState(),
    "sessions": SessionState(),
}

# =========================
# TIME UPDATE
# =========================
def update_world_state():
    world_state["time"]["hour"] += 1
    if world_state["time"]["hour"] >= 24:
        world_state["time"]["hour"] = 0
        world_state["time"]["day"] += 1

# =========================
# SHOW WORLD STATE
# =========================
def show_world_state():
    print("\n=== WORLD STATE ===")
    print("Day:", world_state["time"]["day"])
    print("Region:", world_state["regions"]["current_region"])
    print("Chaos:", world_state["world_conditions"]["world_chaos"])

# =========================
# EVENT STORAGE
# =========================
def activate_world_event(event_name):
    if event_name not in world_state["events"]:
        world_state["events"].append(event_name)

# =========================
# STORY MEMORY
# =========================
def remember_major_event(event_name):
    world_state["history"]["major_events"].append(event_name)

def remember_choice(choice):
    world_state["story_memory"]["major_choices"].append(choice)

# =========================
# REGION MANAGEMENT
# =========================
def discover_region(region_name):
    discovered = world_state["regions"]["discovered_regions"]
    if region_name not in discovered:
        discovered.append(region_name)

def set_current_region(region_name):
    world_state["regions"]["current_region"] = region_name
