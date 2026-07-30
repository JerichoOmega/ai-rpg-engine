import random

from world_state import (
    world_state,
    recruit_companion,
    remember_choice,
    change_faction_reputation
)

from event_bus import (
    subscribe
)

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
# EVENT REACTIONS
# =========================

def handle_enemy_killed(

    event_data

):

    enemy_name = event_data.get(
        "enemy_name"
    )

    party = world_state[
        "companions"
    ]["party"]

    if len(party) == 0:

        return

    for companion_name in party:

        print(
            f"\n{companion_name}"
            f" reacts to defeating"
            f" {enemy_name}."
        )

def handle_quest_completed(

    event_data

):

    quest_name = event_data.get(
        "quest_name"
    )

    party = world_state[
        "companions"
    ]["party"]

    for companion_name in party:

        world_state[
            "companions"
        ]["relationships"][
            companion_name
        ] += 2

        print(
            f"\n{companion_name}"
            f" feels inspired after"
            f" completing {quest_name}."
        )

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "enemy_killed",
    handle_enemy_killed
)

subscribe(
    "quest_completed",
    handle_quest_completed
)