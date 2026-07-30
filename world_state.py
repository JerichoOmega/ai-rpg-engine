"""
world_state.py
===============

Central, persistent world state for a single playthrough.

This module owns the following sections (see each class docstring
below for what it's responsible for):

    - TimeState          : the in-world clock.
    - PlayerState        : the player character's own stats/resources.
    - InventoryState     : carried items (+ a flagged duplicate, see below).
    - QuestState         : active / completed / failed quest name lists.
    - CompanionState     : party membership and per-companion
                          relationship/loyalty tracking.
    - FactionState       : per-faction REPUTATION values only.
    - RegionState        : discovered regions, current region/location, and
                          which faction controls which region.
    - WorldConditions    : global instability/chaos and active disasters.
    - StoryMemory        : major player choices and narrative flags.
    - HistoryState       : a log of major world events, choices, and lore.
    - SessionState       : save/session bookkeeping.

--------------------------------------------------------------------
Scope note: Player / World / Campaign / Faction / NPC separation
--------------------------------------------------------------------
Campaign State -> campaign_manager.py (`campaign_state`)
Full Faction State -> faction_manager.py (`FACTIONS`)
NPC State (roster/dialogue) -> npc_manager.py (`NPCS`)

world_state.py owns per-faction *reputation integers* (`factions`)
and party/companion data (`companions`).

--------------------------------------------------------------------
Why dict subclasses instead of plain @dataclass
--------------------------------------------------------------------
save_system.py / state_manager.py call `json.dump(world_state, ...)`
directly and on load do `world_state.clear(); world_state.update(...)`.
Plain dataclass instances support neither. Multiple modules also do
direct bracket access into nested fields. Every section is therefore a
`dict` subclass: it IS a dict, so JSON serialisation, `.clear()`,
`.update()`, `"key" in section`, and `section["key"]` all keep
working exactly as before. Each section also exposes typed attribute
properties (`section.gold` and `section["gold"]`) for new code.

--------------------------------------------------------------------
Duplicate / unused fields — flagged, NOT removed
--------------------------------------------------------------------
  * DUPLICATE: `player.gold` and `inventory.gold` are two counters
    that appear to track the same value. Only `player["gold"]` is
    written by engine modules; `inventory.gold` may be read by
    inventory.py / shop.py / economy_manager.py. Both preserved.

  * POSSIBLY UNUSED: `companions.relationships` and
    `companions.loyalty` declared but not written in reviewed files.
    Preserved pending verification against companions.py.
"""


def _dict_property(key):
    """Build a property that proxies attribute access to a dict key on
    `self`. Lets each typed section support both `section.field`
    (typed, for new code) and `section["field"]` (unchanged, for every
    existing call site in the rest of the codebase) against the same
    underlying storage.
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
    The player character's own stats and resources.

    All fields that the engine reads/writes are included, including
    backward-compat fields (xp_to_next_level, resource_name, resource,
    max_resource, defense, dodge, equipped_weapon, inventory) that were
    in the original schema and are required by inventory.py, shop.py,
    progression_manager.py, and combat subsystems.
    """

    def __init__(self,
                 name="Wanderer",
                 player_class="Warrior",
                 level=1,
                 xp=0,
                 xp_to_next_level=100,
                 gold=0,
                 hp=100,
                 max_hp=100,
                 resource_name="Stamina",
                 resource=100,
                 max_resource=100,
                 attack_bonus=5,
                 defense=2,
                 dodge=5,
                 weapon_bonus=0,
                 equipped_weapon="Rusty Sword",
                 inventory=None):
        super().__init__(
            name=name,
            level=level,
            xp=xp,
            xp_to_next_level=xp_to_next_level,
            gold=gold,
            hp=hp,
            max_hp=max_hp,
            resource_name=resource_name,
            resource=resource,
            max_resource=max_resource,
            attack_bonus=attack_bonus,
            defense=defense,
            dodge=dodge,
            weapon_bonus=weapon_bonus,
            equipped_weapon=equipped_weapon,
            inventory=list(inventory) if inventory else [],
        )
        # "class" is a reserved word — kept as bracket-only access
        # (world_state["player"]["class"]), same as original.
        self["class"] = player_class

    name = _dict_property("name")
    level = _dict_property("level")
    xp = _dict_property("xp")
    xp_to_next_level = _dict_property("xp_to_next_level")
    gold = _dict_property("gold")
    hp = _dict_property("hp")
    max_hp = _dict_property("max_hp")
    resource_name = _dict_property("resource_name")
    resource = _dict_property("resource")
    max_resource = _dict_property("max_resource")
    attack_bonus = _dict_property("attack_bonus")
    defense = _dict_property("defense")
    dodge = _dict_property("dodge")
    weapon_bonus = _dict_property("weapon_bonus")
    equipped_weapon = _dict_property("equipped_weapon")
    # NOTE: "inventory" not exposed as an attribute because that name
    # shadows dict.inventory() if it existed (no clash here, but kept
    # as bracket-only for clarity: world_state["player"]["inventory"]).

    @property
    def player_class(self):
        """Typed alias for the "class" key."""
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
    Top-level carried-items section (world_state["inventory"]).
    Also currently holds a `gold` field that duplicates PlayerState.gold
    — flagged but not removed; see module-level note above.

    NOTE: inventory.py reads world_state["player"]["inventory"] (a list
    inside PlayerState), NOT this section. This section is preserved for
    future use / save compatibility.
    """

    def __init__(self, items=None, gold=0):
        super().__init__(items=list(items) if items else [], gold=gold)

    # `.items` not exposed as an attribute — it shadows dict.items().
    gold = _dict_property("gold")


# =========================
# QUEST STATE
# =========================
class QuestState(dict):
    """Active / completed / failed quest name lists.
    Used by quests.py, consistency_engine.py, state_manager.py."""

    def __init__(self, active=None, completed=None, failed=None,
                 progress=None):
        super().__init__(
            active=list(active) if active else [],
            completed=list(completed) if completed else [],
            failed=list(failed) if failed else [],
            # progress: dict of quest_name -> kill/task count,
            # used by quests.py's update_quests_from_enemy().
            progress=dict(progress) if progress else {},
        )

    active = _dict_property("active")
    completed = _dict_property("completed")
    failed = _dict_property("failed")
    progress = _dict_property("progress")


# =========================
# COMPANION STATE
# =========================
class CompanionState(dict):
    """
    Companion State
    ---------------
    Party membership and per-companion relationship/loyalty tracking.
    Covers party members' standing with the player only; full NPC data
    lives in npc_manager.py.

    `relationships` and `loyalty` are flagged as possibly-unused; see
    module-level note above.
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
    Maps faction name -> player reputation (int, -100 to 100).
    Faction names are dynamic: faction_manager.py adds new keys at
    runtime (`world_state["factions"][faction_name] = 0`), so no
    static per-faction property is declared.
    """

    def __init__(self, **starting_reputations):
        super().__init__(**starting_reputations)

    def get_reputation(self, faction_name, default=0):
        """Typed convenience accessor."""
        return self.get(faction_name, default)


# =========================
# REGION STATE
# =========================
class RegionState(dict):
    """
    Region State
    ------------
    Which region the player is currently in, which have been
    discovered, and which faction (if any) controls each region.
    `faction_control` and `current_location` keys are dynamic.
    """

    def __init__(self, current_region="kingdom_capital",
                 discovered_regions=None, faction_control=None,
                 current_location=None):
        super().__init__(
            current_region=current_region,
            discovered_regions=(
                list(discovered_regions) if discovered_regions
                else ["kingdom_capital"]
            ),
            faction_control=dict(faction_control) if faction_control else {},
            current_location=current_location,
        )

    current_region = _dict_property("current_region")
    discovered_regions = _dict_property("discovered_regions")
    faction_control = _dict_property("faction_control")
    current_location = _dict_property("current_location")


# =========================
# WORLD CONDITIONS
# =========================
class WorldConditions(dict):
    """Global instability (`world_chaos`, 0-100) and active
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
    checks (consistency_engine.py, narrative_ai.py).

    Supports arbitrary `.get(key)` access for story flags set at
    runtime (e.g. story_memory["dragon_slain"]), since it is a plain
    dict subclass with no locked-down key set.
    """

    def __init__(self, major_choices=None, important_flags=None,
                 **extra_flags):
        super().__init__(
            major_choices=list(major_choices) if major_choices else [],
            important_flags=(
                dict(important_flags) if important_flags else {}
            ),
        )
        # Absorb any extra story flags preserved from save files
        self.update(extra_flags)

    major_choices = _dict_property("major_choices")
    important_flags = _dict_property("important_flags")


# =========================
# HISTORY STATE
# =========================
class HistoryState(dict):
    """
    History State
    -------------
    A running log of major world events (distinct from StoryMemory's
    *flags*).

    Includes:
      major_events  — world/story events (e.g. "dragon_slain")
      choices       — player choice log (backward-compat with old
                      world_state["history"]["choices"] pattern)
      discovered_lore — lore entries found during play (used by
                      region_manager.py / story_manager.py via
                      discover_lore())
    """

    def __init__(self, major_events=None, choices=None,
                 discovered_lore=None):
        super().__init__(
            major_events=list(major_events) if major_events else [],
            choices=list(choices) if choices else [],
            discovered_lore=(
                list(discovered_lore) if discovered_lore else []
            ),
        )

    major_events = _dict_property("major_events")
    choices = _dict_property("choices")
    discovered_lore = _dict_property("discovered_lore")


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
# world_state itself stays a plain top-level dict — save_system.py /
# state_manager.py call world_state.clear() and world_state.update()
# directly on this object, so it must remain a real (non-subclassed)
# dict at the top level. Its values are now the typed sections above.
# Every original key name is preserved, so world_state["player"]["gold"]
# -style access everywhere in the codebase keeps working unmodified.
world_state = {
    # --- Clock ---
    "time": TimeState(),

    # --- Player ---
    "player": PlayerState(),

    # --- Carried items (top-level section; player["inventory"] is
    #     the list that inventory.py actually reads/writes) ---
    "inventory": InventoryState(),

    # --- Quests ---
    "quests": QuestState(),

    # --- Party / companions ---
    "companions": CompanionState(),

    # --- Faction reputations (dynamic keys added at runtime) ---
    "factions": FactionState(
        kingdom=0,
        mages_guild=0,
        shadow_cult=0,
        rebels=0,
    ),

    # --- Regions ---
    "regions": RegionState(),

    # --- World instability ---
    "world_conditions": WorldConditions(),

    # --- Narrative flags / choices ---
    "story_memory": StoryMemory(),

    # --- World event log (flat list; key is "events", matching
    #     consistency_engine.py and narrative_ai.py) ---
    "events": [],

    # --- History log ---
    "history": HistoryState(),

    # --- Session bookkeeping ---
    "sessions": SessionState(),

    # --- Top-level story flags accessed directly by story.py ---
    # These are flat booleans/ints on world_state, not nested.
    "civil_war": False,
    "cult_rising": False,
    "mages_rebellion": False,
    "dragon_alive": True,
    "world_chaos": 0,
}


# =========================
# TIME UPDATE
# =========================
def update_world_state():
    """Advance the in-game clock by one hour."""
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
    """Add a world event to the log (no duplicates)."""
    if event_name not in world_state["events"]:
        world_state["events"].append(event_name)
        print(f"\nWorld Event Activated: {event_name}")


# =========================
# STORY MEMORY
# =========================
def remember_major_event(event_name):
    """Append a major event name to the history log."""
    world_state["history"]["major_events"].append(event_name)


def remember_choice(choice):
    """Log a player choice to both history and story_memory."""
    world_state["history"]["choices"].append(choice)
    world_state["story_memory"]["major_choices"].append(choice)


def discover_lore(lore_entry):
    """Append a lore discovery to the history log."""
    world_state["history"]["discovered_lore"].append(lore_entry)
    print(f"\nLore discovered: {lore_entry}")


# =========================
# REGION MANAGEMENT
# =========================
def discover_region(region_name):
    """Mark a region as discovered (idempotent)."""
    discovered = world_state["regions"]["discovered_regions"]
    if region_name not in discovered:
        discovered.append(region_name)


def set_current_region(region_name):
    """Set the player's current region."""
    world_state["regions"]["current_region"] = region_name


# =========================
# PLAYER HELPERS
# =========================
def heal_player(amount):
    """Restore HP up to max_hp. Used by inventory.py."""
    player = world_state["player"]
    player["hp"] = min(player["hp"] + amount, player["max_hp"])
    print(f"\nPlayer heals {amount} HP!")


def damage_player(amount):
    """Deal damage reduced by defense, clamp to 0. Used by main.py."""
    player = world_state["player"]
    defense = player.get("defense", 0)
    actual = max(0, amount - defense)
    player["hp"] = max(0, player["hp"] - actual)
    print(f"\nPlayer takes {actual} damage!")


def add_gold(amount):
    """Add gold to the player. Used by quests.py, shop.py."""
    world_state["player"]["gold"] += amount


def remove_gold(amount):
    """Remove gold from the player, clamped to 0. Used by shop.py."""
    player = world_state["player"]
    player["gold"] = max(0, player["gold"] - amount)


# =========================
# INVENTORY HELPERS
# =========================
def add_item(item_name):
    """Add an item to the player's inventory list. Used by inventory.py."""
    world_state["player"]["inventory"].append(item_name)


def remove_item(item_name):
    """Remove an item from the player's inventory. Used by inventory.py."""
    inv = world_state["player"]["inventory"]
    if item_name in inv:
        inv.remove(item_name)


# =========================
# QUEST HELPERS
# =========================
def complete_quest(quest_name):
    """Move a quest from active to completed. Used by quests.py."""
    quests = world_state["quests"]
    if quest_name in quests["active"]:
        quests["active"].remove(quest_name)
    if quest_name not in quests["completed"]:
        quests["completed"].append(quest_name)


def fail_quest(quest_name):
    """Move a quest from active to failed. Used by quests.py."""
    quests = world_state["quests"]
    if quest_name in quests["active"]:
        quests["active"].remove(quest_name)
    if quest_name not in quests["failed"]:
        quests["failed"].append(quest_name)


# =========================
# FACTION HELPERS
# =========================
def change_faction_reputation(faction_name, amount):
    """Adjust faction reputation, clamped to [-100, 100]."""
    if faction_name not in world_state["factions"]:
        world_state["factions"][faction_name] = 0
    world_state["factions"][faction_name] += amount
    world_state["factions"][faction_name] = max(
        -100, min(world_state["factions"][faction_name], 100)
    )


# =========================
# STORY MODIFIERS
# =========================
def ensure_world_state_defaults():
    """Backfill keys that are absent after loading a save written before
    the typed-section refactor.  Call immediately after any
    world_state.clear() + world_state.update(loaded_data) sequence so
    that every code path can assume the full current schema is present.
    """
    # --- top-level scalar flags (story.py, story_manager.py) ---
    _top = {
        "civil_war": False,
        "cult_rising": False,
        "mages_rebellion": False,
        "dragon_alive": True,
        "world_chaos": 0,
        "events": [],
    }
    for key, default in _top.items():
        if key not in world_state:
            world_state[key] = default

    # --- nested section defaults ---
    _sections = {
        "time": {"day": 1, "hour": 8, "season": "spring"},
        "inventory": {"items": [], "gold": 0},
        "quests": {
            "active": [], "completed": [], "failed": [], "progress": {}
        },
        "companions": {"party": [], "relationships": {}, "loyalty": {}},
        "regions": {
            "current_region": "kingdom_capital",
            "discovered_regions": ["kingdom_capital"],
            "faction_control": {},
            "current_location": None,
        },
        "world_conditions": {"world_chaos": 0, "active_disasters": []},
        "story_memory": {"major_choices": [], "important_flags": {}},
        "history": {"major_events": [], "choices": [], "discovered_lore": []},
        "sessions": {"session_count": 1, "last_session_summary": ""},
        "factions": {
            "kingdom": 0, "mages_guild": 0,
            "shadow_cult": 0, "rebels": 0,
        },
        "player": {
            "class": "Warrior", "name": "Wanderer",
            "level": 1, "xp": 0, "xp_to_next_level": 100,
            "gold": 0, "hp": 100, "max_hp": 100,
            "resource_name": "Stamina", "resource": 100,
            "max_resource": 100, "attack_bonus": 5,
            "defense": 2, "dodge": 5, "weapon_bonus": 0,
            "equipped_weapon": "Rusty Sword", "inventory": [],
        },
    }
    for section, sub_defaults in _sections.items():
        if section not in world_state:
            world_state[section] = sub_defaults
        elif isinstance(world_state[section], dict):
            for sub_key, sub_val in sub_defaults.items():
                if sub_key not in world_state[section]:
                    world_state[section][sub_key] = sub_val


# =========================
# STORY MODIFIERS
# =========================
def world_story_modifier():
    """Return a dict of world-state modifiers for story generation.
    Used by story.py's generate_story()."""
    return {
        "chaos": world_state["world_conditions"]["world_chaos"],
        "region": world_state["regions"]["current_region"],
        "civil_war": world_state["civil_war"],
        "cult_rising": world_state["cult_rising"],
        "mages_rebellion": world_state["mages_rebellion"],
        "dragon_alive": world_state["dragon_alive"],
        "factions": dict(world_state["factions"]),
    }
