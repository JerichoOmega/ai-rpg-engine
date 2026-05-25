# =========================
# CENTRAL WORLD STATE
# =========================

world_state = {

    # =========================
    # TIME
    # =========================

    "time": {

        "day": 1,

        "hour": 8,

        "season": "spring"
    },

    # =========================
    # PLAYER
    # =========================

    "player": {

        "name": "Wanderer",

        "class": "Adventurer",

        "level": 1,

        "xp": 0,

        "gold": 100,

        "hp": 100,

        "max_hp": 100,

        "attack_bonus": 5,

        "weapon_bonus": 0
    },

    # =========================
    # INVENTORY
    # =========================

    "inventory": {

        "items": [],

        "gold": 100
    },

    # =========================
    # QUESTS
    # =========================

    "quests": {

        "active": [],

        "completed": [],

        "failed": []
    },

    # =========================
    # COMPANIONS
    # =========================

    "companions": {

        "party": [],

        "relationships": {},

        "loyalty": {}
    },

    # =========================
    # FACTIONS
    # =========================

    "factions": {

        "kingdom": 0,

        "mages_guild": 0,

        "shadow_cult": 0,

        "rebels": 0
    },

    # =========================
    # REGIONS
    # =========================

    "regions": {

        "current_region":
            "kingdom_capital",

        "discovered_regions": [

            "kingdom_capital"
        ],

        "faction_control": {}
    },

    # =========================
    # WORLD CONDITIONS
    # =========================

    "world_conditions": {

        "world_chaos": 0,

        "active_disasters": []
    },

    # =========================
    # STORY MEMORY
    # =========================

    "story_memory": {

        "major_choices": [],

        "important_flags": {}
    },

    # =========================
    # EVENTS
    # =========================

    "events": [],

    # =========================
    # HISTORY
    # =========================

    "history": {

        "major_events": []
    },

    # =========================
    # SESSION DATA
    # =========================

    "sessions": {

        "session_count": 1,

        "last_session_summary": ""
    }
}

# =========================
# TIME UPDATE
# =========================

def update_world_state():

    world_state[
        "time"
    ]["hour"] += 1

    if (

        world_state[
            "time"
        ]["hour"]

        >= 24

    ):

        world_state[
            "time"
        ]["hour"] = 0

        world_state[
            "time"
        ]["day"] += 1

# =========================
# SHOW WORLD STATE
# =========================

def show_world_state():

    print(
        "\n=== WORLD STATE ==="
    )

    print(
        "Day:",
        world_state[
            "time"
        ]["day"]
    )

    print(
        "Region:",
        world_state[
            "regions"
        ]["current_region"]
    )

    print(
        "Chaos:",
        world_state[
            "world_conditions"
        ]["world_chaos"]
    )

# =========================
# EVENT STORAGE
# =========================

def activate_world_event(

    event_name

):

    if (

        event_name

        not in

        world_state[
            "events"
        ]

    ):

        world_state[
            "events"
        ].append(
            event_name
        )

# =========================
# STORY MEMORY
# =========================

def remember_major_event(

    event_name

):

    world_state[
        "history"
    ]["major_events"].append(
        event_name
    )

def remember_choice(

    choice

):

    world_state[
        "story_memory"
    ]["major_choices"].append(
        choice
    )

# =========================
# REGION MANAGEMENT
# =========================

def discover_region(

    region_name

):

    discovered = world_state[
        "regions"
    ]["discovered_regions"]

    if region_name not in discovered:

        discovered.append(
            region_name
        )

def set_current_region(

    region_name

):

    world_state[
        "regions"
    ]["current_region"] = (
        region_name
    )