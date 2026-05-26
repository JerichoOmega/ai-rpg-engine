import random

from progression_manager import (
    scale_enemy_power,
    get_world_tier
)

from status_effects import (
    add_status_effect
)

# =========================
# ENEMY DATABASE
# =========================

ENEMIES = {

    "cultist": {

        "type": "humanoid",

        "faction": "shadow_cult",

        "base_hp": 35,

        "base_damage": 8,

        "crit_chance": 5,

        "evasion": 3,

        "resistances": [

            "corruption"
        ],

        "weaknesses": [

            "fire"
        ],

        "abilities": [

            "dark_strike"
        ],

        "loot_table": [

            "gold",

            "cult_amulet"
        ],

        "regions": [

            "shadow_marsh"
        ]
    },

    "shadow_beast": {

        "type": "monster",

        "faction": "none",

        "base_hp": 55,

        "base_damage": 12,

        "crit_chance": 10,

        "evasion": 8,

        "resistances": [

            "poison"
        ],

        "weaknesses": [

            "holy"
        ],

        "abilities": [

            "bleed_attack"
        ],

        "loot_table": [

            "shadow_blade"
        ],

        "regions": [

            "shadow_marsh",

            "ashen_wastes"
        ]
    },

    "rogue_mage": {

        "type": "mage",

        "faction": "mages_guild",

        "base_hp": 45,

        "base_damage": 15,

        "crit_chance": 12,

        "evasion": 5,

        "resistances": [

            "arcane"
        ],

        "weaknesses": [

            "physical"
        ],

        "abilities": [

            "arcane_burst",

            "burn"
        ],

        "loot_table": [

            "mana_crystal"
        ],

        "regions": [

            "arcane_ruins"
        ]
    },

    "ashen_guardian": {

        "type": "boss",

        "faction": "ancient",

        "base_hp": 150,

        "base_damage": 22,

        "crit_chance": 15,

        "evasion": 5,

        "resistances": [

            "fire",

            "burn"
        ],

        "weaknesses": [

            "ice"
        ],

        "abilities": [

            "fire_slam",

            "burning_roar"
        ],

        "loot_table": [

            "legendary_armor",

            "obsidian_blade"
        ],

        "regions": [

            "ashen_wastes"
        ]
    }
}

# =========================
# CREATE ENEMY
# =========================

def create_enemy(

    enemy_name

):

    enemy_data = ENEMIES.get(
        enemy_name
    )

    if not enemy_data:

        return None

    world_tier = get_world_tier()

    enemy = {

        "name": enemy_name,

        "type": enemy_data[
            "type"
        ],

        "faction": enemy_data[
            "faction"
        ],

        "hp": scale_enemy_power(

            enemy_data[
                "base_hp"
            ]
        ),

        "max_hp": scale_enemy_power(

            enemy_data[
                "base_hp"
            ]
        ),

        "damage": scale_enemy_power(

            enemy_data[
                "base_damage"
            ]
        ),

        "crit_chance": enemy_data[
            "crit_chance"
        ],

        "evasion": enemy_data[
            "evasion"
        ],

        "resistances": enemy_data[
            "resistances"
        ],

        "weaknesses": enemy_data[
            "weaknesses"
        ],

        "abilities": enemy_data[
            "abilities"
        ],

        "loot_table": enemy_data[
            "loot_table"
        ],

        "status_effects": [],

        "elite": False,

        "boss": (

            enemy_data["type"]
            == "boss"
        ),

        "world_tier": world_tier
    }

    return enemy

# =========================
# ELITE ENEMY
# =========================

def create_elite_enemy(

    enemy_name

):

    enemy = create_enemy(
        enemy_name
    )

    if not enemy:

        return None

    enemy["elite"] = True

    enemy["hp"] *= 2

    enemy["max_hp"] *= 2

    enemy["damage"] += 10

    enemy["crit_chance"] += 10

    return enemy

# =========================
# RANDOM ENEMY
# =========================

def generate_random_enemy(

    region_name=None

):

    valid_enemies = []

    for enemy_name, enemy_data in ENEMIES.items():

        if region_name:

            if region_name not in enemy_data[
                "regions"
            ]:

                continue

        valid_enemies.append(
            enemy_name
        )

    if not valid_enemies:

        return None

    chosen_enemy = random.choice(
        valid_enemies
    )

    elite_roll = random.randint(
        1,
        100
    )

    if elite_roll <= 10:

        return create_elite_enemy(
            chosen_enemy
        )

    return create_enemy(
        chosen_enemy
    )

# =========================
# APPLY ENEMY STATUS
# =========================

def apply_enemy_status(

    enemy,

    effect_name,

    duration

):

    if effect_name in enemy[
        "resistances"
    ]:

        print(
            f"\n{enemy['name']}"
            f" resisted"
            f" {effect_name}!"
        )

        return enemy

    enemy[
        "status_effects"
    ] = add_status_effect(

        enemy[
            "status_effects"
        ],

        effect_name,

        duration
    )

    return enemy

# =========================
# ENEMY ABILITY
# =========================

def use_enemy_ability(

    enemy

):

    abilities = enemy.get(
        "abilities",
        []
    )

    if not abilities:

        return None

    ability = random.choice(
        abilities
    )

    print(
        f"\n{enemy['name']}"
        f" uses"
        f" {ability}!"
    )

    return ability

# =========================
# SHOW ENEMY
# =========================

def show_enemy(

    enemy

):

    print(
        "\n=== ENEMY INFO ==="
    )

    print(
        "Name:",
        enemy["name"]
    )

    print(
        "Type:",
        enemy["type"]
    )

    print(
        "HP:",
        enemy["hp"]
    )

    print(
        "Damage:",
        enemy["damage"]
    )

    print(
        "Elite:",
        enemy["elite"]
    )

    print(
        "Boss:",
        enemy["boss"]
    )

# =========================
# ENEMY SUMMARY
# =========================

def show_enemy_database():

    print(
        "\n=== ENEMY DATABASE ==="
    )

    for enemy_name, enemy_data in ENEMIES.items():

        print(
            f"\n{enemy_name}"
        )

        print(
            f"Type:"
            f" {enemy_data['type']}"
        )

        print(
            f"Faction:"
            f" {enemy_data['faction']}"
        )

        print(
            f"Base HP:"
            f" {enemy_data['base_hp']}"
        )

# =========================
# BOSS PHASE CHECK
# =========================

def boss_phase_check(

    enemy

):

    if not enemy["boss"]:

        return

    hp_percent = (

        enemy["hp"]
        /
        enemy["max_hp"]

    ) * 100

    if hp_percent <= 50:

        print(
            f"\n{enemy['name']}"
            " enters a rage phase!"
        )

        enemy["damage"] += 10

# =========================
# LEGENDARY ENEMY
# =========================

def create_legendary_enemy():

    enemy = {

        "name": "void_harbinger",

        "type": "legendary",

        "faction": "void",

        "hp": 500,

        "max_hp": 500,

        "damage": 45,

        "crit_chance": 25,

        "evasion": 15,

        "resistances": [

            "fire",

            "poison",

            "corruption"
        ],

        "weaknesses": [

            "holy"
        ],

        "abilities": [

            "void_blast",

            "reality_tear",

            "soul_drain"
        ],

        "loot_table": [

            "godkiller_relic"
        ],

        "status_effects": [],

        "elite": True,

        "boss": True,

        "world_tier": 999
    }

    return enemy