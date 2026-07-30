# =========================
# WORLD STATE
# =========================

world_state = {

    "player": {

        "class": "Warrior",

        "level": 1,

        "xp": 0,

        "xp_to_next_level": 100,

        "hp": 100,

        "max_hp": 100,

        "resource_name": "Stamina",

        "resource": 100,

        "max_resource": 100,

        "gold": 0,

        "attack_bonus": 5,

        "defense": 2,

        "dodge": 5,

        "equipped_weapon": "Rusty Sword"
    },

    "story_memory": {

    },

    "history": {

        "choices": [],

        "discovered_lore": [],

        "major_events": []
    },

    "factions": {

        "shadow_cult": 0,

        "kingdom": 0,

        "rebels": 0
    },

    "world_conditions": {

        "world_chaos": 0
    },

    "active_world_events": []
}

# =========================
# REMEMBER PLAYER CHOICE
# =========================

def remember_choice(

    choice

):

    world_state[
        "history"
    ][
        "choices"
    ].append(
        choice
    )

# =========================
# REMEMBER MAJOR EVENT
# =========================

def remember_major_event(

    event_name

):

    world_state[
        "history"
    ][
        "major_events"
    ].append(
        event_name
    )

# =========================
# DISCOVER LORE
# =========================

def discover_lore(

    lore_entry

):

    world_state[
        "history"
    ][
        "discovered_lore"
    ].append(
        lore_entry
    )

    print(
        f"\nLore discovered:"
        f" {lore_entry}"
    )

# =========================
# ACTIVATE WORLD EVENT
# =========================

def activate_world_event(

    event_name

):

    world_state[
        "active_world_events"
    ].append(
        event_name
    )

    print(
        f"\nWorld Event Activated:"
        f" {event_name}"
    )