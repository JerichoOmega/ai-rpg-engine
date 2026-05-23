import random

from combat import combat

from story import generate_story

from inventory import (
    show_inventory,
    add_item,
    remove_item,
    use_potion,
    equip_weapon
)

from events import random_event

from shop import shop

from player import (
    create_player,
    check_level_up,
    show_story_state
)

# =========================
# PLAYER MEMORY / STORY STATE
# =========================

cult_defeated = False
dragon_defeated = False
knight_defeated = False

player_gold = 25
player_reputation = 0

# =========================
# PLAYER PROGRESSION
# =========================

player_level = 1
player_xp = 0
xp_to_next_level = 100

# =========================
# INVENTORY / EQUIPMENT
# =========================

inventory = []

equipped_weapon = "Rusty Sword"

weapon_bonus = 0

# =========================
# ADVENTURE SETTINGS
# =========================

adventure_length = 3
current_room = 1

# =========================
# ENEMIES
# =========================

enemies = {

    "hidden cult": {
        "hp_min": 15,
        "hp_max": 25,
        "special": "summon"
    },

    "ancient dragon": {
        "hp_min": 30,
        "hp_max": 45,
        "special": "fire"
    },

    "corrupted knight": {
        "hp_min": 20,
        "hp_max": 35,
        "special": "shield"
    },

    "shadow beast": {
        "hp_min": 18,
        "hp_max": 30,
        "special": "dodge"
    },

    "necromancer": {
        "hp_min": 20,
        "hp_max": 40,
        "special": "heal"
    }
}

# =========================
# CREATE PLAYER
# =========================

player_class, player_hp, attack_bonus = create_player()

# =========================
# MAIN GAME LOOP
# =========================

while current_room <= adventure_length and player_hp > 0:

    # STORY GENERATION

    quest, location, enemy_name = generate_story(enemies)

    enemy_hp = random.randint(
        enemies[enemy_name]["hp_min"],
        enemies[enemy_name]["hp_max"]
    )

    print("\n=== YOUR ADVENTURE ===")

    print("\n" + quest)

    print("\nThe danger waits...")
    print(location)

    print("\nMain Enemy:")
    print(enemy_name)

    # =========================
    # COMBAT
    # =========================

    player_hp, enemy_hp = combat(
        player_hp,
        enemy_name,
        enemy_hp,
        attack_bonus,
        inventory,
        enemies,
        equipped_weapon,
        weapon_bonus
    )

    # =========================
    # PLAYER DEFEATED
    # =========================

    if player_hp <= 0:

        print("\nYou were defeated...")
        print("Darkness closes in around you.")

    # =========================
    # PLAYER VICTORY
    # =========================

    elif enemy_hp <= 0:

        print("\nVictory!")
        print("The enemy has fallen.")

        # GOLD

        reward = random.randint(10, 30)

        player_gold += reward

        print("You gained", reward, "gold!")
        print("Total Gold:", player_gold)

        # XP

        xp_gained = random.randint(40, 70)

        player_xp += xp_gained

        print("You gained", xp_gained, "XP!")

        (
            player_level,
            player_xp,
            xp_to_next_level,
            player_hp,
            attack_bonus
        ) = check_level_up(
            player_level,
            player_xp,
            xp_to_next_level,
            player_hp,
            attack_bonus
        )

        # =========================
        # LOOT
        # =========================

        loot_items = [
            "Iron Sword",
            "Magic Staff",
            "Shadow Dagger",
            "Healing Potion",
            "Dragon Shield"
        ]

        loot = random.choice(loot_items)

        inventory = add_item(inventory, loot)

        # EQUIP WEAPON

        if loot in [
            "Iron Sword",
            "Magic Staff",
            "Shadow Dagger",
            "Steel Sword"
        ]:

            equipped_weapon, weapon_bonus = equip_weapon(loot)

        # =========================
        # STORY MEMORY
        # =========================

        if enemy_name == "hidden cult":

            cult_defeated = True

        elif enemy_name == "ancient dragon":

            dragon_defeated = True

        elif enemy_name == "corrupted knight":

            knight_defeated = True

        # =========================
        # RANDOM EVENT
        # =========================

        (
            player_hp,
            player_gold,
            inventory
        ) = random_event(
            player_hp,
            player_gold,
            inventory
        )

        # =========================
        # SHOP
        # =========================

        (
            player_gold,
            player_hp,
            inventory,
            equipped_weapon,
            weapon_bonus
        ) = shop(
            player_gold,
            player_hp,
            inventory,
            equipped_weapon,
            weapon_bonus
        )

        current_room += 1

        # =========================
        # CONTINUE
        # =========================

        if current_room <= adventure_length:

            print("\nYou continue deeper into the adventure...")

        else:

            print("\n=== FINAL VICTORY ===")
            print("You survived the adventure!")

# =========================
# FINAL STORY STATE
# =========================

show_story_state(
    cult_defeated,
    dragon_defeated,
    knight_defeated,
    player_gold,
    player_reputation,
    player_level,
    player_xp,
    xp_to_next_level
)

show_inventory(
    inventory,
    equipped_weapon,
    weapon_bonus
)