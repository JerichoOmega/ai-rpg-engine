import random

from world_state import (
    world_state,
    update_world_state,
    show_world_state,
    add_gold,
    add_item,
    damage_player,
    discover_region,
    set_current_region,
    remember_choice
)

from player import (
    create_player,
    check_level_up,
    show_player_status,
    show_story_state
)

from combat import combat

from shop import (
    shop,
    black_market
)

from inventory import (
    show_inventory,
    equip_weapon
)

from quests import (
    initialize_quests,
    show_quests,
    update_quests_from_enemy,
    update_companion_quests,
    show_completed_quests
)

from companions import (
    show_party,
    attempt_recruitment,
    loyalty_event,
    companion_reaction,
    companion_story_event,
    check_companion_departure
)

from save_system import (
    save_game,
    load_game,
    autosave,
    show_save_summary
)

from loot import (
    generate_loot
)

from hub import (
    town_hub,
    tavern_scene,
    dialogue_choice,
    dungeon_room
)

# =========================
# ENEMY DATABASE
# =========================

enemies = {

    "hidden cult": {

        "hp_min": 25,

        "hp_max": 40
    },

    "ancient dragon": {

        "hp_min": 80,

        "hp_max": 120
    },

    "corrupted knight": {

        "hp_min": 35,

        "hp_max": 55
    },

    "shadow beast": {

        "hp_min": 30,

        "hp_max": 45
    },

    "necromancer": {

        "hp_min": 40,

        "hp_max": 60
    }
}

# =========================
# REGIONS
# =========================

regions = [

    "kingdom_capital",

    "shadow_marsh",

    "frostpeak_mountains",

    "arcane_ruins",

    "ashen_wastes"
]

# =========================
# GAME START
# =========================

print(
    "\n=== AI DUNGEON MASTER ==="
)

print(
    "\n1. New Game"
)

print(
    "2. Load Game"
)

choice = input("> ").strip().lower()

# =========================
# LOAD GAME
# =========================

if choice in [

    "2",

    "load",

    "load game"
]:

    success = load_game()

    if not success:

        print(
            "\nStarting new game instead."
        )

        create_player()

# =========================
# NEW GAME
# =========================

else:

    create_player()

# =========================
# INITIALIZE QUESTS
# =========================

initialize_quests()

# =========================
# MAIN GAME LOOP
# =========================

game_running = True

while game_running:

    update_world_state()

    print(
        "\n========================"
    )

    print(
        "DAY",
        world_state["time"]["day"]
    )

    print(
        "========================"
    )

    # =========================
    # TOWN HUB
    # =========================

    hub_choice = town_hub()

    # =========================
    # TAVERN
    # =========================

    if hub_choice == "tavern":

        tavern_scene()

        companion_story_event()

        continue

    # =========================
    # SHOP
    # =========================

    elif hub_choice == "shop":

        shop()

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

        show_party()

        continue

    # =========================
    # SAVE GAME
    # =========================

    elif hub_choice == "save":

        save_game()

        continue

    # =========================
    # BEGIN ADVENTURE
    # =========================

    elif hub_choice == "adventure":

        print(
            "\n=== BEGIN ADVENTURE ==="
        )

    else:

        print(
            "\nInvalid option."
        )

        continue

    # =========================
    # REGION SELECTION
    # =========================

    print(
        "\n=== CHOOSE REGION ==="
    )

    for region in regions:

        print("•", region)

    selected_region = input(
        "\nTravel to: "
    ).strip().lower()

    if selected_region not in regions:

        selected_region = random.choice(
            regions
        )

        print(
            "\nYou lose your way and arrive at:",
            selected_region
        )

    set_current_region(
        selected_region
    )

    discover_region(
        selected_region
    )

    # =========================
    # DUNGEON LOOP
    # =========================

    room_count = 5

    current_room = 1

    while current_room <= room_count:

        print(
            f"\n=== ROOM {current_room} ==="
        )

        room_type = dungeon_room()

        # =========================
        # ENEMY ROOM
        # =========================

        if room_type == "enemy":

            enemy_name = random.choice(
                list(
                    enemies.keys()
                )
            )

            enemy_hp = random.randint(

                enemies[
                    enemy_name
                ]["hp_min"],

                enemies[
                    enemy_name
                ]["hp_max"]
            )

            print(
                "\nEnemy:",
                enemy_name
            )

            victory = combat(

                enemy_name,
                enemy_hp
            )

            # =========================
            # PLAYER VICTORY
            # =========================

            if victory:

                gold_reward = random.randint(
                    15,
                    35
                )

                xp_reward = random.randint(
                    25,
                    50
                )

                add_gold(
                    gold_reward
                )

                world_state[
                    "player"
                ]["xp"] += xp_reward

                print(
                    f"\nYou gained"
                    f" {gold_reward} gold!"
                )

                print(
                    f"You gained"
                    f" {xp_reward} XP!"
                )

                update_quests_from_enemy(
                    enemy_name
                )

                # =========================
                # LOOT
                # =========================

                loot = generate_loot(
                    enemy_name
                )

                add_item(
                    loot["name"]
                )

                print(
                    "\nLoot Found:"
                )

                print(
                    loot["name"]
                )

                # =========================
                # COMPANION EVENTS
                # =========================

                attempt_recruitment()

                loyalty_event()

                update_companion_quests(

                    world_state[
                        "companions"
                    ]["party"]
                )

                # =========================
                # LEVEL UP
                # =========================

                check_level_up()

            else:

                print(
                    "\nYour adventure ends here..."
                )

                game_running = False

                break

        # =========================
        # TREASURE ROOM
        # =========================

        elif room_type == "treasure":

            loot = generate_loot(
                "treasure"
            )

            add_item(
                loot["name"]
            )

            print(
                "\nTreasure Found:"
            )

            print(
                loot["name"]
            )

        # =========================
        # TRAP ROOM
        # =========================

        elif room_type == "trap":

            trap_damage = random.randint(
                10,
                20
            )

            damage_player(
                trap_damage
            )

            print(
                f"\nA trap deals"
                f" {trap_damage} damage!"
            )

            if world_state[
                "player"
            ]["hp"] <= 0:

                print(
                    "\nThe trap kills you!"
                )

                game_running = False

                break

        # =========================
        # DIALOGUE ROOM
        # =========================

        elif room_type == "dialogue":

            result = dialogue_choice()

            # =========================
            # PERSUADE
            # =========================

            if result == "persuade":

                remember_choice(
                    "merciful"
                )

                companion_reaction(
                    "mercy"
                )

            # =========================
            # THREATEN
            # =========================

            elif result == "threaten":

                remember_choice(
                    "ruthless"
                )

                companion_reaction(
                    "ruthless_actions"
                )

            # =========================
            # BRIBE
            # =========================

            elif result == "bribe":

                if (

                    world_state[
                        "player"
                    ]["gold"] >= 10

                ):

                    world_state[
                        "player"
                    ]["gold"] -= 10

                    print(
                        "\nYou pay 10 gold."
                    )

                else:

                    print(
                        "\nNot enough gold"
                        " to bribe."
                    )

        # =========================
        # EVENT ROOM
        # =========================

        elif room_type == "event":

            print(
                "\nA mysterious world event unfolds..."
            )

        current_room += 1

    # =========================
    # ADVENTURE COMPLETE
    # =========================

    if game_running:

        print(
            "\n=== ADVENTURE COMPLETE ==="
        )

        autosave()

# =========================
# GAME OVER
# =========================

print(
    "\n=== GAME OVER ==="
)

show_story_state()

show_completed_quests()

show_world_state()

show_inventory()

show_party()

show_save_summary()
