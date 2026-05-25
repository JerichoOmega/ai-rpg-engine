import random

from world_state import (
    world_state,
    recruit_companion,
    remember_choice,
    change_faction_reputation
)

# =========================
# COMPANION DATABASE
# =========================

companions = {

    "Mira": {

        "role": "Mage",

        "combat_bonus": 8,

        "personality": "kind",

        "likes": [
            "mercy",
            "helping_people"
        ],

        "dislikes": [
            "ruthless_actions"
        ]
    },

    "Thorn": {

        "role": "Warrior",

        "combat_bonus": 10,

        "personality": "aggressive",

        "likes": [
            "strength",
            "battle"
        ],

        "dislikes": [
            "cowardice"
        ]
    },

    "Kael": {

        "role": "Rogue",

        "combat_bonus": 7,

        "personality": "mysterious",

        "likes": [
            "secrets",
            "shadow_magic"
        ],

        "dislikes": [
            "authority"
        ]
    }
}

# =========================
# RECRUITMENT
# =========================

def attempt_recruitment():

    available = list(
        companions.keys()
    )

    companion_name = random.choice(
        available
    )

    current_party = world_state[
        "companions"
    ]["party"]

    if companion_name in current_party:

        return

    recruit_roll = random.randint(
        1,
        100
    )

    if recruit_roll <= 30:

        recruit_companion(
            companion_name
        )

# =========================
# PARTY DISPLAY
# =========================

def show_party():

    party = world_state[
        "companions"
    ]["party"]

    print(
        "\n=== PARTY ==="
    )

    if len(party) == 0:

        print(
            "You travel alone."
        )

        return

    for companion_name in party:

        companion = companions[
            companion_name
        ]

        loyalty = world_state[
            "companions"
        ]["loyalty"][
            companion_name
        ]

        relationship = world_state[
            "companions"
        ]["relationships"][
            companion_name
        ]

        print(
            "\n•",
            companion_name
        )

        print(
            "Role:",
            companion["role"]
        )

        print(
            "Loyalty:",
            loyalty
        )

        print(
            "Relationship:",
            relationship
        )

        print(
            "Personality:",
            companion[
                "personality"
            ]
        )

# =========================
# COMPANION ATTACKS
# =========================

def companion_attack(

    party,
    enemy_hp

):

    if len(party) == 0:

        return enemy_hp

    for companion_name in party:

        companion = companions[
            companion_name
        ]

        damage = random.randint(
            3,
            companion[
                "combat_bonus"
            ]
        )

        enemy_hp -= damage

        print(
            f"\n{companion_name}"
            f" attacks for"
            f" {damage} damage!"
        )

    return enemy_hp

# =========================
# COMPANION REACTIONS
# =========================

def companion_reaction(

    action_tag

):

    party = world_state[
        "companions"
    ]["party"]

    for companion_name in party:

        companion = companions[
            companion_name
        ]

        likes = companion["likes"]

        dislikes = companion[
            "dislikes"
        ]

        # =========================
        # LIKES
        # =========================

        if action_tag in likes:

            world_state[
                "companions"
            ]["relationships"][
                companion_name
            ] += 5

            print(
                f"\n{companion_name}"
                " approves of your actions."
            )

        # =========================
        # DISLIKES
        # =========================

        if action_tag in dislikes:

            world_state[
                "companions"
            ]["relationships"][
                companion_name
            ] -= 5

            print(
                f"\n{companion_name}"
                " disapproves of your actions."
            )

# =========================
# LOYALTY EVENTS
# =========================

def loyalty_event():

    party = world_state[
        "companions"
    ]["party"]

    if len(party) == 0:

        return

    print(
        "\n=== COMPANION EVENT ==="
    )

    companion_name = random.choice(
        party
    )

    loyalty = world_state[
        "companions"
    ]["loyalty"][
        companion_name
    ]

    relationship = world_state[
        "companions"
    ]["relationships"][
        companion_name
    ]

    # =========================
    # HIGH RELATIONSHIP
    # =========================

    if relationship >= 25:

        print(
            f"\n{companion_name}"
            " trusts you deeply."
        )

        loyalty += 5

    # =========================
    # LOW RELATIONSHIP
    # =========================

    elif relationship <= -25:

        print(
            f"\n{companion_name}"
            " questions your leadership."
        )

        loyalty -= 10

    else:

        print(
            f"\n{companion_name}"
            " remains uncertain about you."
        )

    world_state[
        "companions"
    ]["loyalty"][
        companion_name
    ] = loyalty

# =========================
# COMPANION ABILITIES
# =========================

def companion_ability(

    companion_name,
    enemy_name

):

    if companion_name == "Mira":

        print(
            "\nMira casts an arcane shield!"
        )

        world_state[
            "player"
        ]["defense"] += 2

    elif companion_name == "Thorn":

        print(
            "\nThorn taunts the enemy!"
        )

    elif companion_name == "Kael":

        print(
            "\nKael strikes from the shadows!"
        )

# =========================
# COMPANION LEAVING
# =========================

def check_companion_departure():

    party = world_state[
        "companions"
    ]["party"]

    for companion_name in party[:]:

        loyalty = world_state[
            "companions"
        ]["loyalty"][
            companion_name
        ]

        if loyalty <= 0:

            print(
                f"\n{companion_name}"
                " abandons the party!"
            )

            party.remove(
                companion_name
            )

# =========================
# COMPANION STORY EVENTS
# =========================

def companion_story_event():

    party = world_state[
        "companions"
    ]["party"]

    if len(party) == 0:

        return

    companion_name = random.choice(
        party
    )

    print(
        "\n=== COMPANION STORY ==="
    )

    if companion_name == "Mira":

        print(
            "Mira speaks about the dangers"
            " of uncontrolled magic."
        )

        remember_choice(
            "learned_magic_lore"
        )

    elif companion_name == "Thorn":

        print(
            "Thorn recalls battles from"
            " the civil war."
        )

        remember_choice(
            "heard_war_story"
        )

    elif companion_name == "Kael":

        print(
            "Kael reveals hidden knowledge"
            " about shadow cult rituals."
        )

        remember_choice(
            "learned_cult_secret"
        )