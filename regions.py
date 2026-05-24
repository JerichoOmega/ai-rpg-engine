import random

from world_state import world_state

# =========================
# REGION DATABASE
# =========================

regions = {

    "kingdom_capital": {

        "name": "Kingdom Capital",

        "description":
            "The heart of the kingdom filled "
            "with nobles, guards, and political tension.",

        "danger_level": 1,

        "enemy_types": [
            "corrupted knight"
        ],

        "faction": "kingdom"
    },

    "shadow_marsh": {

        "name": "Shadow Marsh",

        "description":
            "A cursed swamp corrupted by "
            "dark rituals and hidden cultists.",

        "danger_level": 3,

        "enemy_types": [
            "hidden cult",
            "shadow beast"
        ],

        "faction": "shadow_cult"
    },

    "frostpeak_mountains": {

        "name": "Frostpeak Mountains",

        "description":
            "Frozen cliffs where ancient monsters "
            "and dragons once ruled.",

        "danger_level": 4,

        "enemy_types": [
            "ancient dragon",
            "shadow beast"
        ],

        "faction": "neutral"
    },

    "arcane_ruins": {

        "name": "Arcane Ruins",

        "description":
            "Ancient magical ruins overflowing "
            "with unstable arcane energy.",

        "danger_level": 3,

        "enemy_types": [
            "necromancer"
        ],

        "faction": "mages_guild"
    },

    "ashen_wastes": {

        "name": "Ashen Wastes",

        "description":
            "A burned wasteland haunted by "
            "wandering horrors and survivors.",

        "danger_level": 5,

        "enemy_types": [
            "shadow beast",
            "hidden cult",
            "necromancer"
        ],

        "faction": "neutral"
    }
}

# =========================
# SHOW REGIONS
# =========================

def show_regions():

    print(
        "\n=== WORLD MAP ==="
    )

    for region_key in regions:

        region = regions[
            region_key
        ]

        print(
            "\n•",
            region["name"]
        )

        print(
            region["description"]
        )

        print(
            "Danger Level:",
            region["danger_level"]
        )

# =========================
# TRAVEL SYSTEM
# =========================

def choose_region():

    print(
        "\n=== CHOOSE DESTINATION ==="
    )

    region_keys = list(
        regions.keys()
    )

    for index, region_key in enumerate(
        region_keys
    ):

        print(
            str(index + 1)
            + ".",
            regions[
                region_key
            ]["name"]
        )

    choice = input(
        "\nTravel to: "
    )

    try:

        choice_index = int(
            choice
        ) - 1

        selected_region = region_keys[
            choice_index
        ]

        region_data = regions[
            selected_region
        ]

        print(
            "\nTraveling to",
            region_data["name"]
        )

        print(
            region_data["description"]
        )

        return selected_region

    except:

        print(
            "\nInvalid choice."
        )

        print(
            "Traveling to Kingdom Capital."
        )

        return "kingdom_capital"

# =========================
# REGION ENEMY GENERATOR
# =========================

def region_enemy(
    selected_region
):

    region_data = regions[
        selected_region
    ]

    enemy = random.choice(

        region_data[
            "enemy_types"
        ]
    )

    return enemy

# =========================
# REGION WORLD EVENTS
# =========================

def region_world_event(
    selected_region
):

    region_data = regions[
        selected_region
    ]

    print(
        "\n=== REGIONAL EVENTS ==="
    )

    # =========================
    # CIVIL WAR
    # =========================

    if (

        selected_region
        == "kingdom_capital"

        and

        world_state[
            "civil_war"
        ]

    ):

        print(
            "\nRiots spread through"
            " the capital streets."
        )

    # =========================
    # CULT CONTROL
    # =========================

    if (

        selected_region
        == "shadow_marsh"

        and

        world_state[
            "cult_rising"
        ]

    ):

        print(
            "\nCultists patrol openly"
            " through the marsh."
        )

    # =========================
    # ARCANE STORMS
    # =========================

    if (

        selected_region
        == "arcane_ruins"

        and

        world_state[
            "mages_rebellion"
        ]

    ):

        print(
            "\nArcane storms erupt"
            " around the ruins."
        )

    # =========================
    # HIGH CHAOS
    # =========================

    if world_state[
        "world_chaos"
    ] >= 70:

        print(
            "\nThe region suffers from"
            " overwhelming darkness."
        )

# =========================
# REGION QUEST MODIFIERS
# =========================

def region_story_bonus(
    selected_region
):

    if selected_region == "shadow_marsh":

        return (
            "Dark whispers echo through"
            " the swamp."
        )

    elif selected_region == "frostpeak_mountains":

        return (
            "Freezing winds howl across"
            " the mountain paths."
        )

    elif selected_region == "arcane_ruins":

        return (
            "Ancient magic pulses through"
            " the ruins."
        )

    elif selected_region == "ashen_wastes":

        return (
            "Ash drifts endlessly across"
            " the wasteland."
        )

    return (
        "The road ahead feels uncertain."
    )