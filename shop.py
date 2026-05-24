from inventory import (
    add_item
)

from utils import (
    is_buy_potion,
    is_buy_weapon,
    is_leave_shop
)

# =========================
# SHOP SYSTEM
# =========================

def shop(

    player_gold,
    player_hp,
    inventory,
    equipped_weapon,
    weapon_bonus

):

    print(
        "\n=== SHOP ==="
    )

    print(
        "Gold:",
        player_gold
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

        if player_gold >= 15:

            player_gold -= 15

            inventory = add_item(
                inventory,
                "Healing Potion"
            )

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

        if player_gold >= 30:

            player_gold -= 30

            equipped_weapon = (
                "Steel Sword"
            )

            weapon_bonus = 6

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

    else:

        print(
            "\nInvalid choice."
        )

    return (

        player_gold,

        player_hp,

        inventory,

        equipped_weapon,

        weapon_bonus
    )