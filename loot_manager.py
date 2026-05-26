import random

from inventory import (
    add_item
)

from equipment_system import (
    ITEM_DATABASE
)

from event_bus import (
    emit
)

# =========================
# LOOT RARITIES
# =========================

RARITIES = {

    "common": {

        "chance": 50,

        "multiplier": 1.0
    },

    "uncommon": {

        "chance": 30,

        "multiplier": 1.5
    },

    "rare": {

        "chance": 15,

        "multiplier": 2.0
    },

    "epic": {

        "chance": 4,

        "multiplier": 3.0
    },

    "legendary": {

        "chance": 1,

        "multiplier": 5.0
    }
}

# =========================
# LOOT POOLS
# =========================

LOOT_POOLS = {

    "weapon": [

        "iron_sword",

        "shadow_blade"
    ],

    "armor": [

        "steel_armor"
    ],

    "accessory": [

        "cult_amulet"
    ],

    "helmet": [

        "obsidian_helmet"
    ]
}

# =========================
# DETERMINE RARITY
# =========================

def roll_rarity():

    roll = random.randint(
        1,
        100
    )

    total = 0

    for rarity, data in RARITIES.items():

        total += data[
            "chance"
        ]

        if roll <= total:

            return rarity

    return "common"

# =========================
# GENERATE RANDOM LOOT
# =========================

def generate_loot(

    loot_type=None

):

    rarity = roll_rarity()

    # =========================
    # RANDOM CATEGORY
    # =========================

    if loot_type is None:

        loot_type = random.choice(
            list(
                LOOT_POOLS.keys()
            )
        )

    pool = LOOT_POOLS.get(
        loot_type,
        []
    )

    if not pool:

        return None

    item_name = random.choice(
        pool
    )

    item = ITEM_DATABASE.get(
        item_name
    )

    if not item:

        return None

    loot = {

        "name": item_name,

        "rarity": rarity,

        "attack_bonus":

            scale_stat(

                item[
                    "attack_bonus"
                ],

                rarity
            ),

        "defense_bonus":

            scale_stat(

                item[
                    "defense_bonus"
                ],

                rarity
            )
    }

    return loot

# =========================
# SCALE STATS
# =========================

def scale_stat(

    value,
    rarity

):

    multiplier = RARITIES[
        rarity
    ]["multiplier"]

    return int(
        value * multiplier
    )

# =========================
# GENERATE DUNGEON LOOT
# =========================

def generate_dungeon_loot(

    dungeon_difficulty

):

    print(
        "\n=== DUNGEON LOOT ==="
    )

    loot = generate_loot()

    if not loot:

        print(
            "\nNo loot generated."
        )

        return

    # =========================
    # BONUS SCALING
    # =========================

    bonus = int(
        dungeon_difficulty / 10
    )

    loot[
        "attack_bonus"
    ] += bonus

    loot[
        "defense_bonus"
    ] += bonus

    # =========================
    # ADD TO INVENTORY
    # =========================

    add_item(
        loot["name"]
    )

    print(
        f"\nLoot Found:"
        f" {loot['name']}"
    )

    print(
        f"Rarity:"
        f" {loot['rarity']}"
    )

    print(
        f"Attack Bonus:"
        f" {loot['attack_bonus']}"
    )

    print(
        f"Defense Bonus:"
        f" {loot['defense_bonus']}"
    )

    emit(

        "loot_generated",

        loot=loot
    )

    return loot

# =========================
# BOSS LOOT
# =========================

def generate_boss_loot():

    print(
        "\n=== BOSS LOOT ==="
    )

    rarity = random.choice([

        "rare",

        "epic",

        "legendary"
    ])

    loot = generate_loot()

    if not loot:

        return

    loot[
        "rarity"
    ] = rarity

    loot[
        "attack_bonus"
    ] += 10

    loot[
        "defense_bonus"
    ] += 10

    add_item(
        loot["name"]
    )

    print(
        f"\nBoss Loot:"
        f" {loot['name']}"
    )

    print(
        f"Rarity:"
        f" {loot['rarity']}"
    )

    emit(

        "boss_loot_generated",

        loot=loot
    )

# =========================
# RANDOM TREASURE EVENT
# =========================

def random_treasure_event():

    print(
        "\n=== TREASURE FOUND ==="
    )

    loot = generate_loot()

    if not loot:

        return

    add_item(
        loot["name"]
    )

    print(
        f"\nTreasure:"
        f" {loot['name']}"
    )

# =========================
# SHOW LOOT TABLES
# =========================

def show_loot_tables():

    print(
        "\n=== LOOT TABLES ==="
    )

    for loot_type, items in LOOT_POOLS.items():

        print(
            f"\n{loot_type.upper()}"
        )

        for item in items:

            print(
                f"- {item}"
            )

# =========================
# ADD LOOT ITEM
# =========================

def add_loot_item(

    loot_type,
    item_name

):

    if loot_type not in LOOT_POOLS:

        LOOT_POOLS[
            loot_type
        ] = []

    LOOT_POOLS[
        loot_type
    ].append(
        item_name
    )

    print(
        f"\nAdded"
        f" {item_name}"
        f" to"
        f" {loot_type}"
        " loot pool."
    )

# =========================
# LEGENDARY DROP EVENT
# =========================

def trigger_legendary_drop():

    print(
        "\n=== LEGENDARY DROP ==="
    )

    loot = generate_loot()

    if not loot:

        return

    loot[
        "rarity"
    ] = "legendary"

    loot[
        "attack_bonus"
    ] += 25

    loot[
        "defense_bonus"
    ] += 25

    add_item(
        loot["name"]
    )

    print(
        f"\nLegendary Item:"
        f" {loot['name']}"
    )

    emit(

        "legendary_item_found",

        loot=loot
    )

# =========================
# LOOT SUMMARY
# =========================

def show_loot_summary():

    print(
        "\n=== LOOT SYSTEM ==="
    )

    print(
        "Rarities:"
    )

    for rarity in RARITIES:

        print(
            f"- {rarity}"
        )

    print(
        "\nLoot Categories:"
    )

    for category in LOOT_POOLS:

        print(
            f"- {category}"
        )