import random

from world_state import (
    world_state,
    update_world_state,
    show_world_state,
    add_gold,
    add_item,
    discover_region,
    set_current_region,
    remember_choice
)

from player import (
    create_player,
    check_level_up,
    show_story_state
)

from combat import combat

from shop import shop

from inventory import (
    show_inventory
)

from quests import (
    initialize_quests,
    show_quests
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
    autosave
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

from event_bus import (
    emit
)

# =========================
# IMPORT STORY MANAGER
# =========================

import story_manager

# =========================
# ENEMIES
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

if choice in [

    "2",

    "load",

    "load game"
]:

    success = load_game()

    if not success:

        create_player()

else:

    create_player()

initialize_quests()

# =========================
# MAIN LOOP
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
    # QUESTS
    # =========================

    elif hub_choice == "quests":

        show_quests()

        continue

    # =========================
    # PARTY
    # =========================

    elif hub_choice == "party":

        show_party()

        continue

    # =========================
    # SAVE
    # =========================

    elif hub_choice == "save":

        save_game()

        continue

    # =========================
    # ADVENTURE
    # =========================

    elif hub_choice == "adventure":

        print(
            "\n=== BEGIN ADVENTURE ==="
        )

    else:

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

    set_current_region(
        selected_region
    )

    discover_region(
        selected_region
    )

    emit(

        "region_discovered",

        region_name=selected_region
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

                loot = generate_loot(
                    enemy_name
                )

                add_item(
                    loot["name"]
                )

                attempt_recruitment()

                loyalty_event()

                update_world_state()

                check_level_up()

            else:

                print(
                    "\nYour adventure ends here..."
                )

                game_running = False

                break

        # =========================
        # DIALOGUE ROOM
        # =========================

        elif room_type == "dialogue":

            result = dialogue_choice()

            if result == "persuade":

                remember_choice(
                    "merciful"
                )

                emit(

                    "player_choice",

                    choice="mercy"
                )

                companion_reaction(
                    "mercy"
                )

            elif result == "threaten":

                remember_choice(
                    "ruthless"
                )

                emit(

                    "player_choice",

                    choice="ruthless"
                )

                companion_reaction(
                    "ruthless_actions"
                )

        current_room += 1

    # =========================
    # END OF ADVENTURE
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

show_world_state()

show_inventory()

show_party()