import random

from enemy_manager import (

    generate_random_enemy,

    create_elite_enemy,

    create_legendary_enemy
)

from progression_manager import (
    get_world_tier
)

from region_manager import (
    REGIONS
)

# =========================
# REGION ENCOUNTER TABLES
# =========================

REGION_ENCOUNTERS = {

    "shadow_marsh": {

        "common": [

            "cultist",

            "shadow_beast"
        ],

        "rare": [

            "rogue_mage"
        ],

        "boss": [

            "ashen_guardian"
        ]
    },

    "arcane_ruins": {

        "common": [

            "rogue_mage"
        ],

        "rare": [

            "shadow_beast"
        ],

        "boss": [

            "ashen_guardian"
        ]
    },

    "ashen_wastes": {

        "common": [

            "shadow_beast"
        ],

        "rare": [

            "cultist"
        ],

        "boss": [

            "ashen_guardian"
        ]
    }
}

# =========================
# GENERATE ENCOUNTER
# =========================

def generate_encounter(

    region_name,

    encounter_type="random"

):

    encounter_table = REGION_ENCOUNTERS.get(
        region_name
    )

    if not encounter_table:

        print(
            "\nNo encounter data found."
        )

        return []

    world_tier = get_world_tier()

    enemies = []

    # =========================
    # BOSS ENCOUNTER
    # =========================

    if encounter_type == "boss":

        boss_name = random.choice(

            encounter_table[
                "boss"
            ]
        )

        boss = generate_random_enemy(
            region_name
        )

        if boss:

            boss["boss"] = True

            enemies.append(
                boss
            )

        return enemies

    # =========================
    # LEGENDARY ENCOUNTER
    # =========================

    legendary_roll = random.randint(
        1,
        1000
    )

    if legendary_roll == 1000:

        enemies.append(
            create_legendary_enemy()
        )

        return enemies

    # =========================
    # ENCOUNTER SIZE
    # =========================

    enemy_count = random.randint(
        1,
        3 + world_tier
    )

    # =========================
    # GENERATE ENEMIES
    # =========================

    for _ in range(enemy_count):

        rarity_roll = random.randint(
            1,
            100
        )

        # =========================
        # RARE ENEMY
        # =========================

        if rarity_roll <= 15:

            enemy_name = random.choice(

                encounter_table[
                    "rare"
                ]
            )

        # =========================
        # COMMON ENEMY
        # =========================

        else:

            enemy_name = random.choice(

                encounter_table[
                    "common"
                ]
            )

        # =========================
        # ELITE CHANCE
        # =========================

        elite_roll = random.randint(
            1,
            100
        )

        if elite_roll <= 10:

            enemy = create_elite_enemy(
                enemy_name
            )

        else:

            enemy = generate_random_enemy(
                region_name
            )

        if enemy:

            enemies.append(
                enemy
            )

    return enemies

# =========================
# AMBUSH ENCOUNTER
# =========================

def generate_ambush(

    region_name

):

    print(
        "\n=== AMBUSH ==="
    )

    enemies = generate_encounter(
        region_name
    )

    for enemy in enemies:

        enemy[
            "damage"
        ] += 5

    return enemies

# =========================
# NIGHT ENCOUNTER
# =========================

def generate_night_encounter(

    region_name

):

    print(
        "\n=== NIGHT ENCOUNTER ==="
    )

    enemies = generate_encounter(
        region_name
    )

    for enemy in enemies:

        enemy[
            "crit_chance"
        ] += 10

    return enemies

# =========================
# WEATHER MODIFIER
# =========================

def apply_weather_modifier(

    enemies,

    weather

):

    if weather == "storm":

        for enemy in enemies:

            enemy[
                "evasion"
            ] += 5

    elif weather == "foggy":

        for enemy in enemies:

            enemy[
                "crit_chance"
            ] += 5

    elif weather == "ash_storm":

        for enemy in enemies:

            enemy[
                "damage"
            ] += 5

    return enemies

# =========================
# FACTION ENCOUNTER
# =========================

def generate_faction_encounter(

    faction_name

):

    enemies = []

    for enemy_name in [

        "cultist",

        "rogue_mage",

        "shadow_beast"
    ]:

        enemy = generate_random_enemy()

        if not enemy:

            continue

        if enemy[
            "faction"
        ] == faction_name:

            enemies.append(
                enemy
            )

    return enemies

# =========================
# ELITE PATROL
# =========================

def generate_elite_patrol(

    region_name

):

    print(
        "\n=== ELITE PATROL ==="
    )

    patrol_size = random.randint(
        2,
        4
    )

    enemies = []

    for _ in range(
        patrol_size
    ):

        enemy_name = random.choice(

            REGION_ENCOUNTERS[
                region_name
            ]["common"]
        )

        enemy = create_elite_enemy(
            enemy_name
        )

        enemies.append(
            enemy
        )

    return enemies

# =========================
# ENCOUNTER SUMMARY
# =========================

def show_encounter(

    enemies

):

    print(
        "\n=== ENCOUNTER ==="
    )

    for enemy in enemies:

        print(
            f"\n{enemy['name']}"
        )

        print(
            f"HP:"
            f" {enemy['hp']}"
        )

        print(
            f"Damage:"
            f" {enemy['damage']}"
        )

        print(
            f"Elite:"
            f" {enemy['elite']}"
        )

        print(
            f"Boss:"
            f" {enemy['boss']}"
        )

# =========================
# DANGER LEVEL
# =========================

def calculate_encounter_difficulty(

    enemies

):

    difficulty = 0

    for enemy in enemies:

        difficulty += enemy[
            "damage"
        ]

        difficulty += int(
            enemy["hp"] / 10
        )

        if enemy["elite"]:

            difficulty += 25

        if enemy["boss"]:

            difficulty += 100

    return difficulty

# =========================
# SHOW DIFFICULTY
# =========================

def show_encounter_difficulty(

    enemies

):

    difficulty = (
        calculate_encounter_difficulty(
            enemies
        )
    )

    print(
        "\n=== ENCOUNTER DIFFICULTY ==="
    )

    print(
        f"Difficulty Score:"
        f" {difficulty}"
    )

# =========================
# WORLD EVENT ENCOUNTER
# =========================

def generate_world_event_encounter():

    print(
        "\n=== WORLD EVENT ==="
    )

    event_types = [

        "corruption_surge",

        "demonic_invasion",

        "undead_rising",

        "void_breach"
    ]

    event_name = random.choice(
        event_types
    )

    print(
        f"\nEvent:"
        f" {event_name}"
    )

    enemies = []

    enemy_count = random.randint(
        3,
        6
    )

    for _ in range(enemy_count):

        enemies.append(
            create_elite_enemy(
                "shadow_beast"
            )
        )

    return enemies