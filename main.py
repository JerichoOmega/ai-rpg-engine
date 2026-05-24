import random

from combat import combat

from story import generate_story

from inventory import (
    show_inventory,
    add_item
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
    show_party,
    loyalty_event
)

from quests import (
    quests,
    show_quests,
    update_quests_from_enemy,
    update_companion_quests,
    complete_quest_rewards
)

from world_state import (
    update_world_state,
    show_world_state,
    world_event
)

from player import (
    create_player,
    check_level_up,
    show_story_state
)

from save_system import (
    save_game,
    load_game
)

from regions import (
    show_regions,
    choose_region,
    region_enemy,
    region_world_event,
    region_story_bonus
)

from hub import (
    town_hub,
    tavern_scene,
    dialogue_choice,
    dungeon_room
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

party = []

equipped_weapon = "Rusty Sword"

weapon_bonus = 0

# =========================
# ADVENTURE SETTINGS
# =========================

adventure_length = 5

# =========================
# ENEMIES
# =========================

enemies = {

    "hidden cult": {
        "hp_min": 40,
        "hp_max": 65,
        "special": "summon",
        "weakness": "fire",
        "resistance": "poison"
    },

    "ancient dragon": {
        "hp_min": 90,
        "hp_max": 130,
        "special": "fire",
        "weakness": "ice",
        "resistance": "fire"
    },

    "corrupted knight": {
        "hp_min": 60,
        "hp_max": 90,
        "special": "shield",
        "weakness": "poison",
        "resistance": "physical"
    },

    "shadow beast": {
        "hp_min": 50,
        "hp_max": 80,
        "special": "dodge",
        "weakness": "fire",
        "resistance": "ice"
    },

    "necromancer": {
        "hp_min": 65,
        "hp_max": 100,
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

game_choice = input("> ").strip().lower()

if game_choice in ["2", "load", "load game"]:

    save_data = load_game()

    if save_data:

        player_hp = save_data["player_hp"]

        player_gold = save_data["player_gold"]

        player_level = save_data["player_level"]

        player_xp = save_data["player_xp"]

        xp_to_next_level = save_data[
            "xp_to_next_level"
        ]

        player_class = save_data["player_class"]

        resource_name = save_data[
            "resource_name"
        ]

        player_resource = save_data[
            "player_resource"
        ]

        max_resource = save_data[
            "max_resource"
        ]

        player_defense = save_data[
            "player_defense"
        ]

        player_dodge = save_data[
            "player_dodge"
        ]

        inventory = save_data["inventory"]

        equipped_weapon = save_data[
            "equipped_weapon"
        ]

        weapon_bonus = save_data[
            "weapon_bonus"
        ]

        player_reputation = save_data[
            "player_reputation"
        ]

        cult_defeated = save_data[
            "cult_defeated"
        ]

        dragon_defeated = save_data[
            "dragon_defeated"
        ]

        knight_defeated = save_data[
            "knight_defeated"
        ]

        factions = save_data["factions"]

        story_memory = save_data[
            "story_memory"
        ]

        party = save_data["party"]

        attack_bonus = save_data[
            "attack_bonus"
        ]

        print("\nSave loaded!")

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

game_running = True

while game_running and player_hp > 0:

    # =========================
    # TOWN HUB
    # =========================

    hub_choice = town_hub()

    # =========================
    # TAVERN
    # =========================

    if hub_choice == "tavern":

        tavern_scene()

        npc_dialogue(
            factions,
            story_memory
        )

        continue

    # =========================
    # QUEST BOARD
    # =========================

    elif hub_choice == "quests":

        show_quests()

        continue

    # =========================
    # PARTY CAMP
    # =========================

    elif hub_choice == "party":

        show_party(party)

        continue

    # =========================
    # SAVE GAME
    # =========================

    elif hub_choice == "save":

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
            knight_defeated,
            player_class,
            resource_name,
            player_resource,
            max_resource,
            player_defense,
            player_dodge,
            factions,
            story_memory,
            party,
            attack_bonus
        )

        continue

    # =========================
    # SHOP
    # =========================

    elif hub_choice == "shop":

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

        continue

    # =========================
    # BEGIN ADVENTURE
    # =========================

    elif hub_choice == "adventure":

        print(
            "\n=== BEGINNING ADVENTURE ==="
        )

    else:

        print("\nInvalid option.")

        continue

    # =========================
    # ADVENTURE LOOP
    # =========================

    current_room = 1

    while (
        current_room <= adventure_length
        and player_hp > 0
    ):

        print(
            f"\n=== ROOM {current_room} ==="
        )

        update_world_state(
            factions,
            story_memory,
            party
        )

        world_event()

        # =========================
        # REGION SELECTION
        # =========================

        show_regions()

        selected_region = choose_region()

        region_world_event(
            selected_region
        )

        regional_story = region_story_bonus(
            selected_region
        )

        print(
            "\n=== REGION ATMOSPHERE ==="
        )

        print(regional_story)

        # =========================
        # ROOM GENERATION
        # =========================

        room_type = dungeon_room()

        # =========================
        # DIALOGUE ROOM
        # =========================

        if room_type == "dialogue":

            result = dialogue_choice()

            if result == "persuade":

                modify_reputation(
                    factions,
                    "kingdom",
                    5
                )

            elif result == "threaten":

                modify_reputation(
                    factions,
                    "kingdom",
                    -5
                )

            elif result == "bribe":

                if player_gold >= 10:

                    player_gold -= 10

                    modify_reputation(
                        factions,
                        "kingdom",
                        3
                    )

                    print(
                        "\nThe guard pockets"
                        " the coin."
                    )

                else:

                    print(
                        "\nNot enough gold"
                        " to bribe."
                    )

        # =========================
        # TREASURE ROOM
        # =========================

        elif room_type == "treasure":

            treasure = generate_loot(
                "Ancient Relic"
            )

            inventory = add_item(
                inventory,
                treasure["name"]
            )

            print(
                "\nYou obtained:",
                treasure["name"]
            )

        # =========================
        # TRAP ROOM
        # =========================

        elif room_type == "trap":

            damage = random.randint(
                5,
                15
            )

            player_hp -= damage

            print(
                f"\nYou take {damage} trap damage!"
            )

        # =========================
        # EVENT ROOM
        # =========================

        elif room_type == "event":

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
        # ENEMY ROOM
        # =========================

        elif room_type == "enemy":

            (
                quest,
                location,
                _
            ) = generate_story(
                enemies,
                factions,
                story_memory
            )

            enemy_name = region_enemy(
                selected_region
            )

            enemy_hp = random.randint(
                enemies[enemy_name]["hp_min"],
                enemies[enemy_name]["hp_max"]
            )

            print(
                "\n=== YOUR ADVENTURE ==="
            )

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
            # PLAYER VICTORY
            # =========================

            if enemy_hp <= 0:

                print("\nVictory!")

                reward = random.randint(
                    15,
                    40
                )

                xp_gained = random.randint(
                    40,
                    80
                )

                player_gold += reward

                player_xp += xp_gained

                print(
                    f"You gained {reward} gold!"
                )

                print(
                    f"You gained {xp_gained} XP!"
                )

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

                loot = generate_loot(
                    "Mystic Weapon"
                )

                inventory = add_item(
                    inventory,
                    loot["name"]
                )

                print(
                    "\nLoot Found:"
                )

                print(
                    loot["name"]
                )

                update_quests_from_enemy(
                    enemy_name
                )

                update_companion_quests(
                    party
                )

                for quest_key in list(
                    quests.keys()
                ):

                    (
                        player_gold,
                        player_xp,
                        factions,
                        story_memory
                    ) = complete_quest_rewards(
                        quest_key,
                        player_gold,
                        player_xp,
                        factions,
                        story_memory
                    )

                choice_roll = random.randint(
                    1,
                    100
                )

                if choice_roll <= 35:

                    (
                        factions,
                        story_memory
                    ) = choice_event(
                        factions,
                        story_memory
                    )

                recruit_roll = random.randint(
                    1,
                    100
                )

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

                party = loyalty_event(
                    party,
                    story_memory,
                    factions
                )

        current_room += 1

    # =========================
    # ADVENTURE COMPLETE
    # =========================

    print(
        "\n=== ADVENTURE COMPLETE ==="
    )

    print(
        "You return to Ashfall."
    )

# =========================
# GAME OVER
# =========================

print("\n=== FINAL RESULTS ===")

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
        "(" + str(
            factions[faction_name]
        ) + ")"
    )

print("\n=== STORY MEMORY ===")

for memory_key in story_memory:

    print(
        memory_key,
        "-",
        story_memory[memory_key]
    )

show_world_state()

show_inventory(
    inventory,
    equipped_weapon,
    weapon_bonus
)

show_party(party)

show_quests()