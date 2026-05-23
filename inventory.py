# =========================
# INVENTORY SYSTEM
# =========================

def show_inventory(inventory, equipped_weapon, weapon_bonus):

    print("\n=== INVENTORY ===")

    if len(inventory) == 0:

        print("Your inventory is empty.")

    else:

        for item in inventory:

            print("-", item)

    print("\nEquipped Weapon:", equipped_weapon)
    print("Weapon Bonus:", weapon_bonus)


# =========================
# ADD ITEM
# =========================

def add_item(inventory, item):

    inventory.append(item)

    print("\nYou obtained:", item)

    return inventory


# =========================
# REMOVE ITEM
# =========================

def remove_item(inventory, item):

    if item in inventory:

        inventory.remove(item)

        print("\nRemoved:", item)

    return inventory


# =========================
# USE HEALING POTION
# =========================

def use_potion(inventory, player_hp):

    if "Healing Potion" in inventory:

        heal = 20

        player_hp += heal

        inventory.remove("Healing Potion")

        print("\nYou drink a Healing Potion.")
        print("Recovered", heal, "HP!")

    else:

        print("\nNo Healing Potions available.")

    return player_hp


# =========================
# EQUIP WEAPON
# =========================

def equip_weapon(item):

    equipped_weapon = "Rusty Sword"

    weapon_bonus = 0

    if item == "Iron Sword":

        equipped_weapon = "Iron Sword"
        weapon_bonus = 3

    elif item == "Magic Staff":

        equipped_weapon = "Magic Staff"
        weapon_bonus = 5

    elif item == "Shadow Dagger":

        equipped_weapon = "Shadow Dagger"
        weapon_bonus = 4

    elif item == "Steel Sword":

        equipped_weapon = "Steel Sword"
        weapon_bonus = 6

    print("\nEquipped:", equipped_weapon)

    return equipped_weapon, weapon_bonus