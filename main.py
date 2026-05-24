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

from events import (
    random_event,
    choice_event
)

from dialogue import npc_dialogue

from shop import shop

from loot import generate_loot

from factions import (
    factions,
    modify_reputation,
    check_faction_status
)

from memory import (
    story_memory,
    update_memory
)

from companions import (
    companions,
    recruit_companion,
    show_party
)

from player import (
    create_player,
    check_level_up,
    show_story_state
)

from save_system import save_game, load_game

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

party = []

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
        "special": "summon",
        "weakness": "fire",
        "resistance": "poison"
    },

    "ancient dragon": {
        "hp_min": 30,
        "hp_max": 45,
        "special": "fire",
        "weakness": "ice",
        "resistance": "fire"
    },

    "corrupted knight": {
        "hp_min": 20,
        "hp_max": 35,
        "special": "shield",
        "weakness": "poison",
        "resistance": "physical"
    },

    "shadow beast": {
        "hp_min": 18,
        "hp_max": 30,
        "special": "dodge",
        "weakness": "fire",
        "resistance": "ice"
    },

    "necromancer": {
        "hp_min": 20,
        "hp_max": 40,
        "special": "heal",
        "weakness": "fire",
        "resistance": "poison"
    }
}

# =========================
# LOAD OR NEW GAME
# =========================

print("1. New Game")
print("2. Load Game")

game_choice = input("> ")

if game_choice == "2":

    save_data = load_game()

    if save_data:

        player_hp = save_data["player_hp"]

        player_gold = save_data["player_gold"]

        player_level = save_data["player_level"]

        player_xp = save_data["player_xp"]

        xp_to_next_level = save_data["xp_to_next_level"]

        inventory = save_data["inventory"]

        equipped_weapon = save_data["equipped_weapon"]

        weapon_bonus = save_data["weapon_bonus"]

        player_reputation = save_data["player_reputation"]

        cult_defeated = save_data["cult_defeated"]

        dragon_defeated = save_data["dragon_defeated"]

        knight_defeated = save_data["knight_defeated"]

        player_class = save_data["player_class"]

        resource_name = save_data["resource_name"]

        player_resource = save_data["player_resource"]

        max_resource = save_data["max_resource"]

        player_defense = save_data["player_defense"]

        player_dodge = save_data["player_dodge"]

        attack_bonus = 5

        print("\nSave successfully loaded!")

    else:

        (
            player_class,
            player_hp,
            attack_bonus,
            resource_name,
            player_resource,
            max_resource,
            player_defense,
            player_dodge
        ) = create_player()

else:

    (
        player_class,
        player_hp,
        attack_bonus,
        resource_name,
        player_resource,
        max_resource,
        player_defense,
        player_dodge
    ) = create_player()

# =========================
# MAIN GAME LOOP
# =========================

while current_room <= adventure_length and player_hp > 0:

    # =========================
    # STORY GENERATION
    # =========================

    quest, location, enemy_name = generate_story(
        enemies,
        factions,
        story_memory
    )

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

    print(
        "Weakness:",
        enemies[enemy_name]["weakness"]
    )

    print(
        "Resistance:",
        enemies[enemy_name]["resistance"]
    )

    # =========================
    # COMBAT
    # =========================

    (
        player_hp,
        enemy_hp,
        player_resource
    ) = combat(
        player_hp,
        enemy_name,
        enemy_hp,
        attack_bonus,
        inventory,
        enemies,
        equipped_weapon,
        weapon_bonus,
        party,
        player_class,
        player_resource,
        max_resource,
        resource_name,
        player_defense,
        player_dodge
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

        # =========================
        # GOLD REWARD
        # =========================

        reward = random.randint(10, 30)

        player_gold += reward

        print("You gained", reward, "gold!")

        # =========================
        # XP REWARD
        # =========================

        xp_gained = random.randint(40, 70)

        player_xp += xp_gained

        print("You gained", xp_gained, "XP!")

        (
            player_level,
            player_xp,
            xp_to_next_level,
            player_hp,
            attack_bonus,
            max_resource
        ) = check_level_up(
            player_level,
            player_xp,
            xp_to_next_level,
            player_hp,
            attack_bonus,
            max_resource
        )

        # =========================
        # PROCEDURAL LOOT
        # =========================

        loot_items = [
            "Iron Sword",
            "Magic Staff",
            "Shadow Dagger",
            "Healing Potion",
            "Dragon Slayer"
        ]

        base_loot = random.choice(loot_items)

        loot = generate_loot(base_loot)

        inventory = add_item(
            inventory,
            loot["name"]
        )

        print("\n=== LOOT FOUND ===")

        print("Item:", loot["name"])

        print("Rarity:", loot["rarity"])

        print("Effect:", loot["effect"])

        print("Element:", loot["element"])

        print("Damage Bonus:", loot["damage_bonus"])

        print("Crit Bonus:", loot["crit_bonus"])

        print("Defense Bonus:", loot["defense_bonus"])

        # =========================
        # EQUIP WEAPON
        # =========================

        if base_loot in [
            "Iron Sword",
            "Magic Staff",
            "Shadow Dagger",
            "Dragon Slayer"
        ]:

            equipped_weapon = loot["name"]

            print("\nYou equipped:", equipped_weapon)

        # =========================
        # STORY MEMORY / FACTIONS
        # =========================

        if enemy_name == "hidden cult":

            cult_defeated = True

            factions = modify_reputation(
                factions,
                "kingdom",
                10
            )

            factions = modify_reputation(
                factions,
                "shadow_cult",
                -15
            )

        elif enemy_name == "ancient dragon":

            dragon_defeated = True

            story_memory = update_memory(
                story_memory,
                "dragon_slain"
            )

            factions = modify_reputation(
                factions,
                "kingdom",
                20
            )

        elif enemy_name == "corrupted knight":

            knight_defeated = True

            factions = modify_reputation(
                factions,
                "mages_guild",
                10
            )

        elif enemy_name == "necromancer":

            story_memory = update_memory(
                story_memory,
                "used_dark_magic"
            )

            factions = modify_reputation(
                factions,
                "shadow_cult",
                15
            )

            factions = modify_reputation(
                factions,
                "kingdom",
                -10
            )

        # =========================
        # COMPANION RECRUITMENT
        # =========================

        recruit_roll = random.randint(1, 100)

        if recruit_roll <= 30:

            available_companions = [
                "Mira",
                "Thorn",
                "Kael"
            ]

            new_companion = random.choice(
                available_companions
            )

            party = recruit_companion(
                party,
                new_companion
            )

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
        # NPC DIALOGUE
        # =========================

        npc_dialogue(
            factions,
            story_memory
        )

        # =========================
        # CHOICE EVENT
        # =========================

        choice_roll = random.randint(1, 100)

        if choice_roll <= 35:

            (
                factions,
                story_memory
            ) = choice_event(
                factions,
                story_memory
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

        # =========================
        # SAVE GAME
        # =========================

        save_game(
            player_hp,
            player_gold,
            player_level,
            player_xp,
            xp_to_next_level,
            inventory,
            equipped_weapon,
            weapon_bonus,
            player_reputation,
            cult_defeated,
            dragon_defeated,
            knight_defeated
        )

        current_room += 1

        # =========================
        # CONTINUE ADVENTURE
        # =========================

        if current_room <= adventure_length:

            print(
                "\nYou continue deeper into the adventure..."
            )

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
    xp_to_next_level,
    resource_name,
    player_resource,
    max_resource,
    player_defense,
    player_dodge
)

# =========================
# FACTION STATUS
# =========================

print("\n=== FACTIONS ===")

for faction_name in factions:

    status = check_faction_status(
        factions,
        faction_name
    )

    print(
        faction_name,
        "-",
        status,
        "(" + str(factions[faction_name]) + ")"
    )

# =========================
# STORY MEMORY
# =========================

print("\n=== STORY MEMORY ===")

for memory_key in story_memory:

    print(
        memory_key,
        "-",
        story_memory[memory_key]
    )

# =========================
# FINAL INVENTORY
# =========================

show_inventory(
    inventory,
    equipped_weapon,
    weapon_bonus
)

# =========================
# FINAL PARTY
# =========================

show_party(party)