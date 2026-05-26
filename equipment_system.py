from player import (
    player
)

from inventory import (
    inventory
)

from event_bus import (
    emit
)

# =========================
# EQUIPMENT SLOTS
# =========================

equipment = {

    "weapon": None,

    "armor": None,

    "helmet": None,

    "accessory": None
}

# =========================
# ITEM DATABASE
# =========================

ITEM_DATABASE = {

    "iron_sword": {

        "slot": "weapon",

        "attack_bonus": 5,

        "defense_bonus": 0,

        "rarity": "common"
    },

    "steel_armor": {

        "slot": "armor",

        "attack_bonus": 0,

        "defense_bonus": 8,

        "rarity": "uncommon"
    },

    "shadow_blade": {

        "slot": "weapon",

        "attack_bonus": 15,

        "defense_bonus": 0,

        "rarity": "rare"
    },

    "cult_amulet": {

        "slot": "accessory",

        "attack_bonus": 3,

        "defense_bonus": 3,

        "rarity": "rare"
    },

    "obsidian_helmet": {

        "slot": "helmet",

        "attack_bonus": 0,

        "defense_bonus": 6,

        "rarity": "epic"
    }
}

# =========================
# EQUIP ITEM
# =========================

def equip_item(

    item_name

):

    item = ITEM_DATABASE.get(
        item_name
    )

    if not item:

        print(
            "\nUnknown item."
        )

        return

    if item_name not in inventory:

        print(
            "\nItem not in inventory."
        )

        return

    slot = item["slot"]

    # =========================
    # UNEQUIP OLD ITEM
    # =========================

    old_item = equipment[slot]

    if old_item:

        remove_item_stats(
            old_item
        )

        inventory.append(
            old_item
        )

    # =========================
    # EQUIP NEW ITEM
    # =========================

    equipment[slot] = item_name

    inventory.remove(
        item_name
    )

    apply_item_stats(
        item_name
    )

    print(
        f"\nEquipped:"
        f" {item_name}"
    )

    emit(

        "item_equipped",

        item_name=item_name
    )

# =========================
# UNEQUIP ITEM
# =========================

def unequip_item(

    slot

):

    item_name = equipment.get(
        slot
    )

    if not item_name:

        print(
            "\nNo item equipped."
        )

        return

    remove_item_stats(
        item_name
    )

    inventory.append(
        item_name
    )

    equipment[slot] = None

    print(
        f"\nUnequipped:"
        f" {item_name}"
    )

    emit(

        "item_unequipped",

        item_name=item_name
    )

# =========================
# APPLY ITEM STATS
# =========================

def apply_item_stats(

    item_name

):

    item = ITEM_DATABASE.get(
        item_name
    )

    if not item:

        return

    player.attack_bonus += item[
        "attack_bonus"
    ]

    player.defense += item[
        "defense_bonus"
    ]

# =========================
# REMOVE ITEM STATS
# =========================

def remove_item_stats(

    item_name

):

    item = ITEM_DATABASE.get(
        item_name
    )

    if not item:

        return

    player.attack_bonus -= item[
        "attack_bonus"
    ]

    player.defense -= item[
        "defense_bonus"
    ]

# =========================
# SHOW EQUIPMENT
# =========================

def show_equipment():

    print(
        "\n=== EQUIPMENT ==="
    )

    for slot, item in equipment.items():

        print(
            f"\n{slot}: {item}"
        )

# =========================
# SHOW ITEM DETAILS
# =========================

def show_item_details(

    item_name

):

    item = ITEM_DATABASE.get(
        item_name
    )

    if not item:

        print(
            "\nUnknown item."
        )

        return

    print(
        "\n=== ITEM DETAILS ==="
    )

    print(
        "Item:",
        item_name
    )

    print(
        "Slot:",
        item["slot"]
    )

    print(
        "Attack Bonus:",
        item["attack_bonus"]
    )

    print(
        "Defense Bonus:",
        item["defense_bonus"]
    )

    print(
        "Rarity:",
        item["rarity"]
    )

# =========================
# TOTAL PLAYER POWER
# =========================

def calculate_player_power():

    power = 0

    for slot, item_name in equipment.items():

        if not item_name:

            continue

        item = ITEM_DATABASE.get(
            item_name
        )

        if not item:

            continue

        power += item[
            "attack_bonus"
        ]

        power += item[
            "defense_bonus"
        ]

    return power

# =========================
# LEGENDARY ITEM CHECK
# =========================

def has_legendary_equipment():

    for slot, item_name in equipment.items():

        if not item_name:

            continue

        item = ITEM_DATABASE.get(
            item_name
        )

        if not item:

            continue

        if item[
            "rarity"
        ] == "legendary":

            return True

    return False

# =========================
# ADD LEGENDARY ITEM
# =========================

def create_legendary_item(

    item_name,
    slot,
    attack_bonus,
    defense_bonus

):

    ITEM_DATABASE[
        item_name
    ] = {

        "slot": slot,

        "attack_bonus": attack_bonus,

        "defense_bonus": defense_bonus,

        "rarity": "legendary"
    }

    print(
        f"\nLegendary item created:"
        f" {item_name}"
    )

# =========================
# EQUIPMENT SUMMARY
# =========================

def show_equipment_summary():

    print(
        "\n=== EQUIPMENT SUMMARY ==="
    )

    print(
        "Player Power:",
        calculate_player_power()
    )

    print(
        "Legendary Equipped:",
        has_legendary_equipment()
    )