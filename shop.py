from world_state import (
    world_state,
    add_gold,
    remove_gold
)

from inventory import (
    give_item,
    equip_weapon,
    show_inventory
)

from utils import (
    is_buy_potion,
    is_buy_weapon,
    is_leave_shop
)

# =========================
# SHOP DATABASE
# =========================

shop_items = {

    "Healing Potion": {

        "price": 15,

        "type": "consumable"
    },

    "Steel Sword": {

        "price": 30,

        "type": "weapon"
    },

    "Shadow Dagger": {

        "price": 50,

        "type": "weapon"
    },

    "Magic Staff": {

        "price": 60,

        "type": "weapon"
    }
}

# =========================
# SHOP SYSTEM
# =========================

def shop():

    player = world_state["player"]

    print(
        "\n=== SHOP ==="
    )

    print(
        "Gold:",
        player["gold"]
    )

    print(
        "\n1. Healing Potion (15 gold)"
    )

    print(
        "2. Steel Sword (+6 attack)"
        " (30 gold)"
    )

    print(
        "3. Leave Shop"
    )

    choice = input(
        "\nChoose: "
    )

    # =========================
    # BUY POTION
    # =========================

    if is_buy_potion(choice):

        item = "Healing Potion"

        cost = shop_items[
            item
        ]["price"]

        if player["gold"] >= cost:

            remove_gold(cost)

            give_item(item)

            print(
                "\nYou purchased"
                " a Healing Potion."
            )

        else:

            print(
                "\nNot enough gold."
            )

    # =========================
    # BUY WEAPON
    # =========================

    elif is_buy_weapon(choice):

        item = "Steel Sword"

        cost = shop_items[
            item
        ]["price"]

        if player["gold"] >= cost:

            remove_gold(cost)

            give_item(item)

            equip_weapon(item)

            print(
                "\nYou purchased"
                " a Steel Sword!"
            )

        else:

            print(
                "\nNot enough gold."
            )

    # =========================
    # LEAVE SHOP
    # =========================

    elif is_leave_shop(choice):

        print(
            "\nYou leave the shop."
        )

    # =========================
    # INVALID
    # =========================

    else:

        print(
            "\nInvalid choice."
        )

# =========================
# SPECIAL SHOP
# =========================

def black_market():

    player = world_state["player"]

    print(
        "\n=== BLACK MARKET ==="
    )

    print(
        "A hooded merchant watches"
        " you carefully."
    )

    print(
        "\n1. Shadow Dagger (50 gold)"
    )

    print(
        "2. Magic Staff (60 gold)"
    )

    print(
        "3. Leave"
    )

    choice = input("> ").strip().lower()

    # =========================
    # SHADOW DAGGER
    # =========================

    if choice in [

        "1",

        "shadow dagger"
    ]:

        item = "Shadow Dagger"

        cost = shop_items[
            item
        ]["price"]

        if player["gold"] >= cost:

            remove_gold(cost)

            give_item(item)

            print(
                "\nThe merchant quietly"
                " hands over the dagger."
            )

        else:

            print(
                "\nYou cannot afford it."
            )

    # =========================
    # MAGIC STAFF
    # =========================

    elif choice in [

        "2",

        "magic staff"
    ]:

        item = "Magic Staff"

        cost = shop_items[
            item
        ]["price"]

        if player["gold"] >= cost:

            remove_gold(cost)

            give_item(item)

            print(
                "\nArcane power pulses"
                " from the staff."
            )

        else:

            print(
                "\nYou cannot afford it."
            )

    else:

        print(
            "\nYou leave the black market."
        )

# =========================
# SELL ITEMS
# =========================

def sell_item(item_name):

    player = world_state["player"]

    inventory = player["inventory"]

    if item_name not in inventory:

        print(
            "\nYou do not own"
            " that item."
        )

        return

    sell_values = {

        "Healing Potion": 5,

        "Iron Sword": 10,

        "Steel Sword": 15,

        "Shadow Dagger": 25,

        "Magic Staff": 30,

        "Dragon Slayer": 50
    }

    value = sell_values.get(
        item_name,
        1
    )

    inventory.remove(item_name)

    add_gold(value)

    print(
        f"\nSold {item_name}"
        f" for {value} gold."
    )

# =========================
# SHOP STATUS
# =========================

def show_shop_status():

    player = world_state["player"]

    print(
        "\n=== SHOP STATUS ==="
    )

    print(
        "Gold:",
        player["gold"]
    )

    print(
        "Inventory Space:",
        len(
            player["inventory"]
        )
    )

    print(
        "Equipped Weapon:",
        player["equipped_weapon"]
    )

    show_inventory()