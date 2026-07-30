import random

from world_state import (
    world_state
)

from event_bus import (
    emit
)

# =========================
# ENEMY DATABASE
# =========================

enemy_database = {

    "goblin": {

        "name": "Goblin",

        "hp": 35,

        "max_hp": 35,

        "damage": 8,

        "elite": False,

        "boss": False,

        "crit_chance": 5,

        "status_effects": []
    },

    "skeleton": {

        "name": "Skeleton",

        "hp": 45,

        "max_hp": 45,

        "damage": 10,

        "elite": False,

        "boss": False,

        "crit_chance": 8,

        "status_effects": []
    },

    "orc": {

        "name": "Orc Warrior",

        "hp": 65,

        "max_hp": 65,

        "damage": 14,

        "elite": True,

        "boss": False,

        "crit_chance": 10,

        "status_effects": []
    },

    "dragon": {

        "name": "Ancient Dragon",

        "hp": 250,

        "max_hp": 250,

        "damage": 35,

        "elite": True,

        "boss": True,

        "crit_chance": 20,

        "status_effects": []
    }
}

# =========================
# CREATE ENEMY
# =========================

def create_enemy(

    enemy_key

):

    enemy_template = enemy_database.get(
        enemy_key.lower()
    )

    if not enemy_template:

        print(
            f"\nEnemy not found:"
            f" {enemy_key}"
        )

        return None

    enemy = dict(
        enemy_template
    )

    return enemy

# =========================
# RANDOM ENEMY
# =========================

def generate_random_enemy(

    region_name=None

):

    enemy_keys = list(
        enemy_database.keys()
    )

    selected_enemy = random.choice(
        enemy_keys
    )

    enemy = create_enemy(
        selected_enemy
    )

    if not enemy:

        return None

    # =========================
    # REGION MODIFIERS
    # =========================

    if region_name == "dark_forest":

        enemy["hp"] += 10

        enemy["max_hp"] += 10

    elif region_name == "ancient_ruins":

        enemy["damage"] += 3

    # =========================
    # WORLD CHAOS SCALING
    # =========================

    chaos = world_state[
        "world_conditions"
    ][
        "world_chaos"
    ]

    enemy["hp"] += chaos

    enemy["max_hp"] += chaos

    enemy["damage"] += int(
        chaos * 0.3
    )

    return enemy

# =========================
# ENEMY ABILITIES
# =========================

def use_enemy_ability(

    enemy

):

    enemy_name = enemy[
        "name"
    ].lower()

    # =========================
    # GOBLIN
    # =========================

    if "goblin" in enemy_name:

        print(
            "\nGoblin throws sand"
            " in your eyes!"
        )

    # =========================
    # SKELETON
    # =========================

    elif "skeleton" in enemy_name:

        print(
            "\nSkeleton reforms"
            " damaged bones!"
        )

        heal = random.randint(
            5,
            12
        )

        enemy["hp"] += heal

        enemy["hp"] = min(

            enemy["hp"],

            enemy["max_hp"]
        )

    # =========================
    # ORC
    # =========================

    elif "orc" in enemy_name:

        print(
            "\nOrc enters a rage!"
        )

        enemy["damage"] += 2

    # =========================
    # DRAGON
    # =========================

    elif "dragon" in enemy_name:

        print(
            "\nThe dragon breathes fire!"
        )

        emit(
            "dragon_fire"
        )

# =========================
# BOSS PHASES
# =========================

def boss_phase_check(

    enemy

):

    if not enemy["boss"]:

        return

    hp_percent = (

        enemy["hp"] /

        enemy["max_hp"]
    ) * 100

    # =========================
    # PHASE 2
    # =========================

    if (

        hp_percent <= 50

        and not enemy.get(
            "phase_2_triggered"
        )
    ):

        enemy[
            "phase_2_triggered"
        ] = True

        enemy["damage"] += 10

        print(
            f"\n{enemy['name']}"
            " becomes enraged!"
        )

        emit(

            "boss_phase_changed",

            enemy_name=enemy[
                "name"
            ],

            phase=2
        )

    # =========================
    # FINAL PHASE
    # =========================

    if (

        hp_percent <= 20

        and not enemy.get(
            "final_phase_triggered"
        )
    ):

        enemy[
            "final_phase_triggered"
        ] = True

        enemy["damage"] += 15

        print(
            f"\n{enemy['name']}"
            " enters FINAL PHASE!"
        )

        emit(

            "boss_phase_changed",

            enemy_name=enemy[
                "name"
            ],

            phase=3
        )

# =========================
# ENEMY REWARD
# =========================

def reward_player_for_enemy(

    enemy

):

    reward_gold = random.randint(
        5,
        20
    )

    if enemy["elite"]:

        reward_gold *= 2

    if enemy["boss"]:

        reward_gold *= 5

    world_state[
        "player"
    ][
        "gold"
    ] += reward_gold

    print(
        f"\nYou gain"
        f" {reward_gold} gold."
    )

# =========================
# ENCOUNTER GENERATION
# =========================

def generate_enemy_group(

    count=3,

    region_name=None

):

    enemies = []

    for _ in range(
        count
    ):

        enemy = generate_random_enemy(
            region_name
        )

        if enemy:

            enemies.append(
                enemy
            )

    return enemies