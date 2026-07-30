import random

from world_state import (
    world_state
)

from faction_manager import (
    get_faction_status
)

from story_manager import (
    story_state
)

from event_bus import (
    emit
)

# =========================
# NPC RELATIONSHIPS
# =========================

npc_relationships = {}

# =========================
# DIALOGUE DATABASE
# =========================

DIALOGUE_DATABASE = {

    "neutral": [

        "The roads grow more dangerous each day.",

        "Travel carefully out there.",

        "Strange things are happening lately."
    ],

    "friendly": [

        "Good to see you again, friend.",

        "People speak highly of your deeds.",

        "You are always welcome here."
    ],

    "hostile": [

        "I don't trust your kind.",

        "Leave before trouble starts.",

        "You bring danger with you."
    ],

    "enemy": [

        "You are not welcome here.",

        "Guards! Remove this threat!",

        "Your presence disgusts us."
    ],

    "corruption": [

        "Something dark follows you...",

        "Your soul feels tainted.",

        "The shadows whisper around you."
    ],

    "redemption": [

        "You bring hope to this land.",

        "People believe in you.",

        "Perhaps the world can still heal."
    ],

    "conquest": [

        "Power bends the world around you.",

        "Many fear your growing influence.",

        "You walk the path of domination."
    ]
}

# =========================
# START DIALOGUE
# =========================

def start_dialogue(

    npc_name,

    faction=None

):

    print(
        f"\n=== TALKING TO {npc_name.upper()} ==="
    )

    relationship = get_npc_relationship(
        npc_name
    )

    theme = story_state[
        "active_theme"
    ]

    # =========================
    # FACTION STATUS
    # =========================

    faction_status = "neutral"

    if faction:

        faction_status = get_faction_status(
            faction
        )

    # =========================
    # RELATIONSHIP OVERRIDE
    # =========================

    if relationship >= 50:

        faction_status = "friendly"

    elif relationship <= -50:

        faction_status = "enemy"

    elif relationship <= -25:

        faction_status = "hostile"

    # =========================
    # BASE DIALOGUE
    # =========================

    possible_dialogue = DIALOGUE_DATABASE.get(

        faction_status,

        DIALOGUE_DATABASE[
            "neutral"
        ]
    )

    dialogue = random.choice(
        possible_dialogue
    )

    print(
        f"\n{npc_name}:"
    )

    print(
        f'"{dialogue}"'
    )

    # =========================
    # THEME REACTION
    # =========================

    if theme in DIALOGUE_DATABASE:

        theme_dialogue = random.choice(

            DIALOGUE_DATABASE[
                theme
            ]
        )

        print(
            f'\n"{theme_dialogue}"'
        )

    emit(

        "dialogue_started",

        npc=npc_name
    )

# =========================
# NPC RELATIONSHIP
# =========================

def get_npc_relationship(

    npc_name

):

    return npc_relationships.get(

        npc_name,

        0
    )

# =========================
# CHANGE RELATIONSHIP
# =========================

def change_npc_relationship(

    npc_name,

    amount

):

    if npc_name not in npc_relationships:

        npc_relationships[
            npc_name
        ] = 0

    npc_relationships[
        npc_name
    ] += amount

    npc_relationships[
        npc_name
    ] = max(

        -100,

        min(

            npc_relationships[
                npc_name
            ],

            100
        )
    )

    print(
        f"\nRelationship with"
        f" {npc_name}"
        f" changed by {amount}."
    )

# =========================
# PERSUASION CHECK
# =========================

def persuasion_check(

    difficulty

):

    roll = random.randint(
        1,
        100
    )

    bonus = 0

    if story_state[
        "active_theme"
    ] == "redemption":

        bonus += 10

    total = roll + bonus

    print(
        f"\nPersuasion Roll:"
        f" {total}"
    )

    return total >= difficulty

# =========================
# INTIMIDATION CHECK
# =========================

def intimidation_check(

    difficulty

):

    roll = random.randint(
        1,
        100
    )

    bonus = 0

    if story_state[
        "active_theme"
    ] == "conquest":

        bonus += 15

    total = roll + bonus

    print(
        f"\nIntimidation Roll:"
        f" {total}"
    )

    return total >= difficulty

# =========================
# DIALOGUE CHOICE
# =========================

def dialogue_choice(

    npc_name,

    choice

):

    print(
        f"\nChoice:"
        f" {choice}"
    )

    # =========================
    # KIND
    # =========================

    if choice == "kind":

        change_npc_relationship(

            npc_name,

            10
        )

        emit(

            "player_choice",

            choice="mercy"
        )

        print(
            "\nThe conversation softens."
        )

    # =========================
    # AGGRESSIVE
    # =========================

    elif choice == "aggressive":

        change_npc_relationship(

            npc_name,

            -15
        )

        emit(

            "player_choice",

            choice="ruthless"
        )

        print(
            "\nTension fills the air."
        )

    # =========================
    # CORRUPT
    # =========================

    elif choice == "corrupt":

        change_npc_relationship(

            npc_name,

            -5
        )

        emit(

            "player_choice",

            choice="corrupt"
        )

        print(
            "\nDarkness creeps into"
            " the conversation."
        )

# =========================
# RUMOR SYSTEM
# =========================

def generate_rumor():

    rumors = [

        "A cult has been seen in the marshes.",

        "Travelers vanish near the ruins.",

        "A great beast stalks the wastes.",

        "War between factions may soon erupt.",

        "Strange magic spreads across the land."
    ]

    rumor = random.choice(
        rumors
    )

    print(
        "\n=== RUMOR ==="
    )

    print(
        rumor
    )

# =========================
# WORLD STATE DIALOGUE
# =========================

def world_state_dialogue():

    chaos = world_state[
        "world_conditions"
    ]["world_chaos"]

    print(
        "\n=== WORLD DISCUSSION ==="
    )

    if chaos < 25:

        print(
            "\nPeople remain hopeful."
        )

    elif chaos < 50:

        print(
            "\nFear spreads through"
            " the settlements."
        )

    elif chaos < 75:

        print(
            "\nCivilization begins"
            " breaking apart."
        )

    else:

        print(
            "\nThe world stands on"
            " the edge of destruction."
        )

# =========================
# COMPANION DIALOGUE
# =========================

def companion_dialogue(

    companion_name

):

    print(
        f"\n=== {companion_name.upper()} ==="
    )

    theme = story_state[
        "active_theme"
    ]

    if theme == "redemption":

        print(
            "\n'I believe we can"
            " still save this world.'"
        )

    elif theme == "corruption":

        print(
            "\n'The darkness is"
            " changing you...'"
        )

    elif theme == "conquest":

        print(
            "\n'Power is becoming"
            " your obsession.'"
        )

    else:

        print(
            "\n'We should keep moving.'"
        )

# =========================
# SHOW RELATIONSHIPS
# =========================

def show_relationships():

    print(
        "\n=== NPC RELATIONSHIPS ==="
    )

    if not npc_relationships:

        print(
            "\nNo tracked relationships."
        )

        return

    for npc, value in npc_relationships.items():

        print(
            f"\n{npc}: {value}"
        )

# =========================
# DIALOGUE SUMMARY
# =========================

def show_dialogue_summary():

    print(
        "\n=== DIALOGUE SYSTEM ==="
    )

    print(
        f"Tracked NPCs:"
        f" {len(npc_relationships)}"
    )

    print(
        f"Current Story Theme:"
        f" {story_state['active_theme']}"
    )