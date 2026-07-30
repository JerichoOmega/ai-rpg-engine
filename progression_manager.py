from world_state import (
    world_state
)

from event_bus import (
    emit
)

# =========================
# PROGRESSION STATE
# =========================

progression_state = {

    "level": 1,

    "xp": 0,

    "xp_to_next_level": 100,

    "skill_points": 0,

    "world_tier": 1
}

# =========================
# ADD EXPERIENCE
# =========================

def add_experience(

    amount

):

    progression_state[
        "xp"
    ] += amount

    print(
        f"\nYou gained"
        f" {amount} XP."
    )

    check_level_up()

# =========================
# LEVEL UP CHECK
# =========================

def check_level_up():

    while (

        progression_state["xp"]

        >=

        progression_state[
            "xp_to_next_level"
        ]

    ):

        progression_state[
            "xp"
        ] -= progression_state[
            "xp_to_next_level"
        ]

        progression_state[
            "level"
        ] += 1

        progression_state[
            "xp_to_next_level"
        ] += 50

        progression_state[
            "skill_points"
        ] += 1

        # =========================
        # PLAYER SCALING
        # =========================

        player_data = world_state[
            "player"
        ]

        player_data[
            "max_hp"
        ] += 20

        player_data[
            "hp"
        ] = player_data[
            "max_hp"
        ]

        player_data[
            "attack_bonus"
        ] += 2

        print(
            "\n=== LEVEL UP ==="
        )

        print(
            f"You are now level"
            f" {progression_state['level']}!"
        )

        print(
            "\n+20 Max HP"
        )

        print(
            "+2 Attack Bonus"
        )

        print(
            "+1 Skill Point"
        )

        emit(

            "player_level_up",

            level=progression_state[
                "level"
            ]
        )

        # =========================
        # WORLD TIER SCALING
        # =========================

        update_world_tier()

# =========================
# WORLD TIER
# =========================

def update_world_tier():

    level = progression_state[
        "level"
    ]

    old_tier = progression_state[
        "world_tier"
    ]

    if level >= 20:

        progression_state[
            "world_tier"
        ] = 5

    elif level >= 15:

        progression_state[
            "world_tier"
        ] = 4

    elif level >= 10:

        progression_state[
            "world_tier"
        ] = 3

    elif level >= 5:

        progression_state[
            "world_tier"
        ] = 2

    else:

        progression_state[
            "world_tier"
        ] = 1

    new_tier = progression_state[
        "world_tier"
    ]

    if new_tier > old_tier:

        print(
            f"\n=== WORLD TIER"
            f" INCREASED:"
            f" {new_tier} ==="
        )

        emit(

            "world_tier_changed",

            tier=new_tier
        )

# =========================
# SCALE ENEMY POWER
# =========================

def scale_enemy_power(

    base_value

):

    tier = progression_state[
        "world_tier"
    ]

    multiplier = 1 + (
        (tier - 1) * 0.35
    )

    return int(
        base_value * multiplier
    )

# =========================
# GET WORLD TIER
# =========================

def get_world_tier():

    return progression_state[
        "world_tier"
    ]

# =========================
# QUEST REWARDS
# =========================

def reward_quest_completion(

    xp_reward=50,

    gold_reward=25

):

    add_experience(
        xp_reward
    )

    world_state[
        "player"
    ][
        "gold"
    ] += gold_reward

    print(
        "\nQuest rewards:"
    )

    print(
        f"+{xp_reward} XP"
    )

    print(
        f"+{gold_reward} Gold"
    )

    emit(

        "quest_reward_given",

        xp=xp_reward,

        gold=gold_reward
    )

# =========================
# SHOW PROGRESSION
# =========================

def show_progression():

    print(
        "\n=== PROGRESSION ==="
    )

    print(
        f"Level:"
        f" {progression_state['level']}"
    )

    print(
        f"XP:"
        f" {progression_state['xp']}"
        f"/"
        f"{progression_state['xp_to_next_level']}"
    )

    print(
        f"Skill Points:"
        f" {progression_state['skill_points']}"
    )

    print(
        f"World Tier:"
        f" {progression_state['world_tier']}"
    )