import random

from enemy_manager import (

    generate_enemy_group
)

from event_bus import (
    emit
)

# =========================
# ENCOUNTER DIFFICULTY
# =========================

def calculate_encounter_difficulty(

    enemies

):

    total_power = 0

    for enemy in enemies:

        total_power += enemy[
            "hp"
        ]

        total_power += (
            enemy["damage"] * 2
        )

        if enemy["elite"]:

            total_power += 50

        if enemy["boss"]:

            total_power += 150

    if total_power < 100:

        return "Easy"

    elif total_power < 250:

        return "Medium"

    elif total_power < 450:

        return "Hard"

    return "Deadly"

# =========================
# GENERATE ENCOUNTER
# =========================

def generate_encounter(

    region_name=None

):

    roll = random.randint(
        1,
        100
    )

    if roll <= 40:

        enemy_count = 1

    elif roll <= 75:

        enemy_count = 2

    elif roll <= 95:

        enemy_count = 3

    else:

        enemy_count = 4

    enemies = generate_enemy_group(

        count=enemy_count,

        region_name=region_name
    )

    difficulty = (
        calculate_encounter_difficulty(
            enemies
        )
    )

    print(
        "\n=== ENCOUNTER ==="
    )

    print(
        f"\nDifficulty: {difficulty}"
    )

    for enemy in enemies:

        print(
            f"- {enemy['name']}"
        )

    emit(

        "encounter_started",

        difficulty=difficulty,

        enemy_count=len(
            enemies
        )
    )

    return enemies

# =========================
# NARRATIVE ENCOUNTER
# =========================

def generate_narrative_encounter():

    print(
        "\nA story event unfolds."
    )

    emit(
        "narrative_encounter"
    )

    return {

        "type": "narrative"
    }

# =========================
# AMBUSH ENCOUNTER
# =========================

def ambush_encounter(

    region_name=None

):

    print(
        "\nYou are ambushed!"
    )

    enemies = generate_enemy_group(

        count=random.randint(
            2,
            5
        ),

        region_name=region_name
    )

    for enemy in enemies:

        enemy["damage"] += 2

    emit(
        "player_ambushed"
    )

    return enemies

# =========================
# ELITE ENCOUNTER
# =========================

def elite_encounter(

    region_name=None

):

    print(
        "\nAn elite enemy appears!"
    )

    enemies = generate_enemy_group(

        count=2,

        region_name=region_name
    )

    for enemy in enemies:

        enemy["elite"] = True

        enemy["hp"] += 30

        enemy["max_hp"] += 30

        enemy["damage"] += 5

    emit(
        "elite_encounter"
    )

    return enemies

# =========================
# BOSS ENCOUNTER
# =========================

def boss_encounter(

    region_name=None

):

    print(
        "\nA terrifying boss emerges!"
    )

    enemies = generate_enemy_group(

        count=1,

        region_name=region_name
    )

    boss = enemies[0]

    boss["boss"] = True

    boss["elite"] = True

    boss["hp"] += 150

    boss["max_hp"] += 150

    boss["damage"] += 15

    emit(

        "boss_encounter_started",

        boss_name=boss[
            "name"
        ]
    )

    return enemies

# =========================
# WORLD EVENT ENCOUNTER
# =========================

def generate_world_event_encounter(

    event_name=None

):

    print(
        "\nA world event encounter begins!"
    )

    if event_name == "Cult Retaliation":

        enemies = generate_enemy_group(
            count=4
        )

        for enemy in enemies:

            enemy["damage"] += 3

        return enemies

    return generate_enemy_group(
        count=3
    )