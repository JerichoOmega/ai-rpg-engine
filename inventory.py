from world_state import (
    world_state,
    add_item,
    remove_item,
    heal_player
)

# =========================
# INVENTORY DISPLAY
# =========================

def show_inventory():

    player = world_state["player"]

    inventory = player["inventory"]

    print(
        "\n=== INVENTORY ==="
    )

    if len(inventory) == 0:

        print(
            "Your inventory is empty."
        )

    else:

        for item in inventory:

            print("•", item)

    print(
        "\nEquipped Weapon:",
        player["equipped_weapon"]
    )

    print(
        "Weapon Bonus:",
        player["weapon_bonus"]
    )

# =========================
# ADD ITEM
# =========================

def give_item(item_name):

    add_item(item_name)

# =========================
# REMOVE ITEM
# =========================

def take_item(item_name):

    remove_item(item_name)

# =========================
# HEALING POTION
# =========================

def use_potion():

    inventory = world_state[
        "player"
    ]["inventory"]

    if "Healing Potion" in inventory:

        heal_amount = 30

        heal_player(
            heal_amount
        )

        remove_item(
            "Healing Potion"
        )

        print(
            f"\nYou restored"
            f" {heal_amount} HP!"
        )

        print(
            "Current HP:",
            world_state[
                "player"
            ]["hp"]
        )

    else:

        print(
            "\nYou do not have"
            " a Healing Potion."
        )

# =========================
# EQUIP WEAPON
# =========================

def equip_weapon(item_name):

    player = world_state["player"]

    inventory = player["inventory"]

    if item_name not in inventory:

        print(
            "\nYou do not own"
            " that weapon."
        )

        return

    weapon_data = {

        "Rusty Sword": 0,

        "Iron Sword": 4,

        "Steel Sword": 6,

        "Shadow Dagger": 8,

        "Magic Staff": 10,

        "Dragon Slayer": 15,

        "Mystic Weapon": 12,

        "Ancient Relic": 20
    }

    if item_name in weapon_data:

        player[
            "equipped_weapon"
        ] = item_name

        player[
            "weapon_bonus"
        ] = weapon_data[
            item_name
        ]

        print(
            f"\nEquipped:"
            f" {item_name}"
        )

        print(
            "Weapon Bonus:",
            player[
                "weapon_bonus"
            ]
        )

    else:

        print(
            "\nThat item cannot"
            " be equipped."
        )

# =========================
# INVENTORY CHECKS
# =========================

def has_item(item_name):

    return (

        item_name

        in

        world_state[
            "player"
        ]["inventory"]
    )

def inventory_count():

    return len(

        world_state[
            "player"
        ]["inventory"]
    )

# =========================
# LOOT HANDLING
# =========================

def receive_loot(loot):

    print(
        "\n=== LOOT RECEIVED ==="
    )

    print(
        "Item:",
        loot["name"]
    )

    print(
        "Rarity:",
        loot["rarity"]
    )

    print(
        "Effect:",
        loot["effect"]
    )

    print(
        "Element:",
        loot["element"]
    )

    print(
        "Damage Bonus:",
        loot["damage_bonus"]
    )

    print(
        "Crit Bonus:",
        loot["crit_bonus"]
    )

    print(
        "Defense Bonus:",
        loot["defense_bonus"]
    )

    add_item(
        loot["name"]
    )

# =========================
# GOLD DISPLAY
# =========================

def show_gold():

    print(
        "\nGold:",
        world_state[
            "player"
        ]["gold"]
    )