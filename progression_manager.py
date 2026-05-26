from player import (
    player
)

from event_bus import (
    emit
)

from skill_tree import (
    gain_skill_point
)

from dungeon_manager import (
    evolve_dungeons
)

from region_manager import (
    evolve_world_regions
)

from settlement_manager import (
    evolve_settlements
)

from economy_manager import (
    evolve_economy
)

# =========================
# PROGRESSION STATE
# =========================

progression_state = {

    "level": 1,

    "xp": 0,

    "xp_to_next_level": 100,

    "world_tier": 1,

    "difficulty_scale": 1.0
}

# =========================
# XP REWARDS
# =========================

XP_REWARDS = {

    "enemy_defeat": 25,

    "boss_defeat": 150,

    "quest_complete": 100,

    "region_discovery": 50,

    "dungeon_clear": 200,

    "legendary_event": 500
}

# =========================
# GAIN XP
# =========================

def gain_xp(

    amount

):

    progression_state[
        "xp"
    ] += amount

    print(
        f"\nGained"
        f" {amount}"
        " XP."
    )

    check_level_up()

# =========================
# CHECK LEVEL UP
# =========================

def check_level_up():

    current_xp = progression_state[
        "xp"
    ]

    xp_needed = progression_state[
        "xp_to_next_level"
    ]

    while current_xp >= xp_needed:

        progression_state[
            "xp"
        ] -= xp_needed

        level_up()

        current_xp = progression_state[
            "xp"
        ]

        xp_needed = progression_state[
            "xp_to_next_level"
        ]

# =========================
# LEVEL UP
# =========================

def level_up():

    progression_state[
        "level"
    ] += 1

    level = progression_state[
        "level"
    ]

    # =========================
    # XP SCALING
    # =========================

    progression_state[
        "xp_to_next_level"
    ] = int(

        progression_state[
            "xp_to_next_level"
        ] * 1.35
    )

    # =========================
    # PLAYER STAT GROWTH
    # =========================

    player.max_hp += 10

    player.hp = player.max_hp

    player.attack_bonus += 2

    player.defense += 1

    # =========================
    # SKILL POINT REWARD
    # =========================

    gain_skill_point(
        1
    )

    print(
        f"\n=== LEVEL UP ==="
    )

    print(
        f"Reached Level {level}!"
    )

    print(
        "\nStat increases:"
    )

    print(
        "+10 Max HP"
    )

    print(
        "+2 Attack"
    )

    print(
        "+1 Defense"
    )

    emit(

        "player_level_up",

        level=level
    )

    # =========================
    # WORLD SCALING
    # =========================

    if level % 5 == 0:

        increase_world_tier()

# =========================
# WORLD TIER
# =========================

def increase_world_tier():

    progression_state[
        "world_tier"
    ] += 1

    progression_state[
        "difficulty_scale"
    ] += 0.25

    tier = progression_state[
        "world_tier"
    ]

    print(
        f"\n=== WORLD TIER INCREASED ==="
    )

    print(
        f"World Tier:"
        f" {tier}"
    )

    # =========================
    # EVOLVE WORLD
    # =========================

    evolve_world_regions()

    evolve_settlements()

    evolve_economy()

    evolve_dungeons()

    emit(

        "world_tier_increased",

        tier=tier
    )

# =========================
# GET PLAYER LEVEL
# =========================

def get_player_level():

    return progression_state[
        "level"
    ]

# =========================
# GET WORLD TIER
# =========================

def get_world_tier():

    return progression_state[
        "world_tier"
    ]

# =========================
# SCALE ENEMY
# =========================

def scale_enemy_power(

    base_power

):

    scale = progression_state[
        "difficulty_scale"
    ]

    return int(
        base_power * scale
    )

# =========================
# REWARD HELPERS
# =========================

def reward_enemy_defeat():

    gain_xp(
        XP_REWARDS[
            "enemy_defeat"
        ]
    )

def reward_boss_defeat():

    gain_xp(
        XP_REWARDS[
            "boss_defeat"
        ]
    )

def reward_quest_completion():

    gain_xp(
        XP_REWARDS[
            "quest_complete"
        ]
    )

def reward_region_discovery():

    gain_xp(
        XP_REWARDS[
            "region_discovery"
        ]
    )

def reward_dungeon_clear():

    gain_xp(
        XP_REWARDS[
            "dungeon_clear"
        ]
    )

def reward_legendary_event():

    gain_xp(
        XP_REWARDS[
            "legendary_event"
        ]
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
        f"World Tier:"
        f" {progression_state['world_tier']}"
    )

    print(
        f"Difficulty Scale:"
        f" {progression_state['difficulty_scale']}"
    )

# =========================
# PROGRESSION SUMMARY
# =========================

def show_progression_summary():

    print(
        "\n=== CHARACTER SUMMARY ==="
    )

    print(
        f"Level:"
        f" {progression_state['level']}"
    )

    print(
        f"HP:"
        f" {player.hp}"
        f"/"
        f"{player.max_hp}"
    )

    print(
        f"Attack:"
        f" {player.attack_bonus}"
    )

    print(
        f"Defense:"
        f" {player.defense}"
    )

# =========================
# MILESTONE CHECK
# =========================

def check_progression_milestones():

    level = progression_state[
        "level"
    ]

    if level == 10:

        print(
            "\nYou are becoming"
            " a legendary adventurer."
        )

    elif level == 20:

        print(
            "\nYour actions now shape"
            " entire kingdoms."
        )

    elif level == 30:

        print(
            "\nThe world trembles"
            " at your power."
        )

# =========================
# EVENT XP INTEGRATION
# =========================

def on_enemy_killed(

    event_data

):

    reward_enemy_defeat()

def on_boss_defeated(

    event_data

):

    reward_boss_defeat()

def on_quest_completed(

    event_data

):

    reward_quest_completion()

def on_region_discovered(

    event_data

):

    reward_region_discovery()

def on_dungeon_cleared(

    event_data

):

    reward_dungeon_clear()

# =========================
# REGISTER EVENTS
# =========================

from event_bus import subscribe

subscribe(
    "enemy_killed",
    on_enemy_killed
)

subscribe(
    "boss_defeated",
    on_boss_defeated
)

subscribe(
    "quest_completed",
    on_quest_completed
)

subscribe(
    "region_discovered",
    on_region_discovered
)

subscribe(
    "dungeon_cleared",
    on_dungeon_cleared
)