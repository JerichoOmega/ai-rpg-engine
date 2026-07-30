import random

from dialogue_manager import (
    npc_relationships
)

from companion_manager import (
    COMPANIONS,
    active_companions
)

from faction_manager import (
    change_reputation
)

from story_manager import (
    story_state
)

from event_bus import (
    emit
)

# =========================
# SOCIAL STATE
# =========================

social_state = {

    "fear": 0,

    "respect": 0,

    "infamy": 0,

    "renown": 0
}

# =========================
# RELATIONSHIP THRESHOLDS
# =========================

RELATIONSHIP_LEVELS = {

    "devoted": 90,

    "trusted": 60,

    "friendly": 25,

    "neutral": 0,

    "disliked": -25,

    "hated": -60,

    "enemy": -90
}

# =========================
# GET RELATIONSHIP LEVEL
# =========================

def get_relationship_level(

    value

):

    if value >= 90:

        return "devoted"

    elif value >= 60:

        return "trusted"

    elif value >= 25:

        return "friendly"

    elif value > -25:

        return "neutral"

    elif value > -60:

        return "disliked"

    elif value > -90:

        return "hated"

    return "enemy"

# =========================
# CHANGE NPC RELATIONSHIP
# =========================

def modify_relationship(

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

    value = npc_relationships[
        npc_name
    ]

    level = get_relationship_level(
        value
    )

    print(
        f"\nRelationship with"
        f" {npc_name}"
        f" changed by {amount}."
    )

    print(
        f"Relationship Level:"
        f" {level}"
    )

    evaluate_relationship(
        npc_name
    )

# =========================
# EVALUATE RELATIONSHIP
# =========================

def evaluate_relationship(

    npc_name

):

    value = npc_relationships.get(

        npc_name,

        0
    )

    level = get_relationship_level(
        value
    )

    # =========================
    # BETRAYAL
    # =========================

    if level == "enemy":

        print(
            f"\n{npc_name}"
            " may seek revenge."
        )

        emit(

            "npc_enemy",

            npc=npc_name
        )

    # =========================
    # TRUST
    # =========================

    elif level == "trusted":

        print(
            f"\n{npc_name}"
            " deeply trusts you."
        )

    # =========================
    # DEVOTION
    # =========================

    elif level == "devoted":

        print(
            f"\n{npc_name}"
            " would risk everything"
            " for you."
        )

# =========================
# FEAR
# =========================

def increase_fear(

    amount

):

    social_state[
        "fear"
    ] += amount

    social_state[
        "fear"
    ] = min(

        social_state[
            "fear"
        ],

        100
    )

    print(
        f"\nFear increased by"
        f" {amount}."
    )

# =========================
# RESPECT
# =========================

def increase_respect(

    amount

):

    social_state[
        "respect"
    ] += amount

    social_state[
        "respect"
    ] = min(

        social_state[
            "respect"
        ],

        100
    )

    print(
        f"\nRespect increased by"
        f" {amount}."
    )

# =========================
# INFAMY
# =========================

def increase_infamy(

    amount

):

    social_state[
        "infamy"
    ] += amount

    social_state[
        "infamy"
    ] = min(

        social_state[
            "infamy"
        ],

        100
    )

    print(
        f"\nInfamy increased by"
        f" {amount}."
    )

# =========================
# RENOWN
# =========================

def increase_renown(

    amount

):

    social_state[
        "renown"
    ] += amount

    social_state[
        "renown"
    ] = min(

        social_state[
            "renown"
        ],

        100
    )

    print(
        f"\nRenown increased by"
        f" {amount}."
    )

# =========================
# RELATIONSHIP DECAY
# =========================

def decay_relationships():

    for npc_name in npc_relationships:

        value = npc_relationships[
            npc_name
        ]

        if value > 0:

            npc_relationships[
                npc_name
            ] -= 1

        elif value < 0:

            npc_relationships[
                npc_name
            ] += 1

# =========================
# COMPANION CONFLICT
# =========================

def evaluate_companion_conflicts():

    if len(active_companions) < 2:

        return

    for companion in active_companions:

        morality = companion[
            "morality"
        ]

        corruption = companion[
            "corruption"
        ]

        # =========================
        # HIGH CORRUPTION
        # =========================

        if corruption >= 75:

            print(
                f"\n{companion['role']}"
                " is becoming unstable."
            )

        # =========================
        # MORALITY CONFLICT
        # =========================

        if morality == "honorable":

            if story_state[
                "active_theme"
            ] == "corruption":

                print(
                    f"\n{companion['role']}"
                    " disapproves of your actions."
                )

# =========================
# SOCIAL REACTION
# =========================

def world_social_reaction():

    fear = social_state[
        "fear"
    ]

    respect = social_state[
        "respect"
    ]

    infamy = social_state[
        "infamy"
    ]

    renown = social_state[
        "renown"
    ]

    print(
        "\n=== SOCIAL REACTION ==="
    )

    # =========================
    # FEARED
    # =========================

    if fear >= 75:

        print(
            "\nPeople fear your presence."
        )

    # =========================
    # RESPECTED
    # =========================

    if respect >= 75:

        print(
            "\nYour reputation inspires others."
        )

    # =========================
    # INFAMOUS
    # =========================

    if infamy >= 75:

        print(
            "\nYour name spreads terror."
        )

    # =========================
    # LEGENDARY
    # =========================

    if renown >= 75:

        print(
            "\nYou are becoming legendary."
        )

# =========================
# FACTION SOCIAL IMPACT
# =========================

def faction_social_effect(

    faction_name,

    action

):

    if action == "help":

        change_reputation(
            faction_name,
            10
        )

        increase_respect(
            5
        )

    elif action == "betray":

        change_reputation(
            faction_name,
            -15
        )

        increase_infamy(
            10
        )

# =========================
# RANDOM SOCIAL EVENT
# =========================

def generate_social_event():

    events = [

        "A bard sings of your deeds.",

        "A merchant spreads rumors about you.",

        "Villagers whisper as you pass.",

        "A noble seeks your audience.",

        "A criminal organization watches you."
    ]

    event = random.choice(
        events
    )

    print(
        "\n=== SOCIAL EVENT ==="
    )

    print(
        event
    )

# =========================
# SOCIAL SUMMARY
# =========================

def show_social_summary():

    print(
        "\n=== SOCIAL SUMMARY ==="
    )

    print(
        f"Fear:"
        f" {social_state['fear']}"
    )

    print(
        f"Respect:"
        f" {social_state['respect']}"
    )

    print(
        f"Infamy:"
        f" {social_state['infamy']}"
    )

    print(
        f"Renown:"
        f" {social_state['renown']}"
    )

# =========================
# RELATIONSHIP SUMMARY
# =========================

def show_relationship_summary():

    print(
        "\n=== RELATIONSHIPS ==="
    )

    if not npc_relationships:

        print(
            "\nNo tracked relationships."
        )

        return

    for npc, value in npc_relationships.items():

        level = get_relationship_level(
            value
        )

        print(
            f"\n{npc}:"
            f" {value}"
            f" ({level})"
        )