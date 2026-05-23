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

    print("\n=== SHOP ===")

    print("Gold:", player_gold)

    print("\n1. Healing Potion (15 gold)")
    print("2. Steel Sword (+6 attack) (30 gold)")
    print("3. Leave Shop")

    choice = input("\nChoose: ")

    # =========================
    # HEALING POTION
    # =========================

    if choice == "1":

        if player_gold >= 15:

            player_gold -= 15

            inventory.append("Healing Potion")

            print("\nYou bought a Healing Potion.")

        else:

            print("\nNot enough gold.")

    # =========================
    # STEEL SWORD
    # =========================

    elif choice == "2":

        if player_gold >= 30:

            player_gold -= 30

            equipped_weapon = "Steel Sword"

            weapon_bonus = 6

            inventory.append("Steel Sword")

            print("\nYou equipped the Steel Sword!")

        else:

            print("\nNot enough gold.")

    # =========================
    # LEAVE SHOP
    # =========================

    elif choice == "3":

        print("\nYou leave the shop.")

    return (
        player_gold,
        player_hp,
        inventory,
        equipped_weapon,
        weapon_bonus
    )