import random

from combat import (
    quick_encounter,
    boss_encounter
)

from quest_manager import (
    generate_quest,
    show_active_quests
)

from world_event_manager import (

    update_world_events,

    generate_random_world_event,

    show_active_world_events
)

from faction_manager import (
    evolve_factions
)

from economy_manager import (
    evolve_economy
)

from relationship_manager import (

    decay_relationships,

    generate_social_event
)

from companion_manager import (

    random_companion_banter,

    show_party
)

from dm_brain import (

    update_dm_brain,

    show_dm_state
)

from story_manager import (
    show_story_summary
)

from save_manager import (
    autosave
)

from region_manager import (
    show_regions
)

from settlement_manager import (
    show_all_settlements as show_settlements
)

from dialogue_manager import (
    generate_rumor
)

# =========================
# GAME STATE
# =========================

game_state = {

    "running": True,

    "day": 1,

    "tick": 0,

    "autosave_interval": 5
}

# =========================
# MAIN MENU
# =========================

def show_main_menu():

    print(
        "\n=== MAIN MENU ==="
    )

    print(
        "\n1. Explore"
    )

    print(
        "2. Travel"
    )

    print(
        "3. View Quests"
    )

    print(
        "4. View Party"
    )

    print(
        "5. View Regions"
    )

    print(
        "6. View Settlements"
    )

    print(
        "7. Story Summary"
    )

    print(
        "8. World Events"
    )

    print(
        "9. Director State"
    )

    print(
        "10. Save Game"
    )

    print(
        "11. Legacy Questlines"
    )

    print(
        "12. Exit Game"
    )

# =========================
# GAME TICK
# =========================

def process_game_tick():

    game_state[
        "tick"
    ] += 1

    print(
        f"\n=== WORLD TICK"
        f" {game_state['tick']} ==="
    )

    # =========================
    # WORLD SIMULATION
    # =========================

    update_world_events()

    evolve_factions()

    evolve_economy()

    decay_relationships()

    # =========================
    # AI DIRECTOR
    # =========================

    update_dm_brain()

    # =========================
    # RANDOM SOCIAL EVENTS
    # =========================

    social_roll = random.randint(
        1,
        100
    )

    if social_roll <= 25:

        generate_social_event()

    # =========================
    # RANDOM RUMORS
    # =========================

    rumor_roll = random.randint(
        1,
        100
    )

    if rumor_roll <= 20:

        generate_rumor()

    # =========================
    # COMPANION BANTER
    # =========================

    banter_roll = random.randint(
        1,
        100
    )

    if banter_roll <= 30:

        random_companion_banter()

    # =========================
    # WORLD EVENTS
    # =========================

    world_event_roll = random.randint(
        1,
        100
    )

    if world_event_roll <= 15:

        generate_random_world_event()

    # =========================
    # AUTOSAVE
    # =========================

    if (

        game_state["tick"]

        %
        game_state[
            "autosave_interval"
        ]

        == 0

    ):

        autosave()

# =========================
# EXPLORE
# =========================

def explore():

    # Player-driven exploration: choices that reuse the existing encounter,
    # quest and world-event systems (see world_actions.explore_menu).
    from world_actions import explore_menu

    explore_menu()

# =========================
# TRAVEL
# =========================

def travel():

    # Real travel: destination selection + region transition + road events,
    # driven by the existing travel_manager (see world_actions.travel_menu).
    # travel_menu advances the world simulation itself, so no extra tick here.
    from world_actions import travel_menu

    travel_menu()

# =========================
# REST
# =========================

def rest():

    print(
        "\n=== RESTING ==="
    )

    print(
        "\nThe party recovers."
    )

    process_game_tick()

# =========================
# RANDOM BOSS EVENT
# =========================

def random_boss_encounter():

    boss_roll = random.randint(
        1,
        100
    )

    if boss_roll <= 10:

        print(
            "\nA legendary threat appears!"
        )

        boss_encounter(
            "ashen_guardian"
        )

# =========================
# GAME LOOP
# =========================

def run_game():

    print(
        "\n=== AI RPG STARTED ==="
    )

    while game_state[
        "running"
    ]:

        show_main_menu()

        choice = input(
            "\nChoose: "
        ).strip()

        # =========================
        # EXPLORE
        # =========================

        if choice == "1":

            explore()

            random_boss_encounter()

            process_game_tick()

        # =========================
        # TRAVEL
        # =========================

        elif choice == "2":

            travel()

        # =========================
        # QUESTS
        # =========================

        elif choice == "3":

            show_active_quests()

        # =========================
        # PARTY
        # =========================

        elif choice == "4":

            show_party()

        # =========================
        # REGIONS
        # =========================

        elif choice == "5":

            show_regions()

            from world_actions import world_map_menu

            world_map_menu()

        # =========================
        # SETTLEMENTS
        # =========================

        elif choice == "6":

            from world_actions import settlement_menu

            settlement_menu()

        # =========================
        # STORY
        # =========================

        elif choice == "7":

            show_story_summary()

        # =========================
        # WORLD EVENTS
        # =========================

        elif choice == "8":

            show_active_world_events()

        # =========================
        # DIRECTOR
        # =========================

        elif choice == "9":

            show_dm_state()

        # =========================
        # SAVE
        # =========================

        elif choice == "10":

            autosave()

        # =========================
        # LEGACY QUESTLINES
        # =========================

        elif choice == "11":

            from legacy.menu import show_legacy_menu

            show_legacy_menu()

        # =========================
        # EXIT
        # =========================

        elif choice == "12":

            print(
                "\nSaving before exit..."
            )

            autosave()

            print(
                "\nGame closed."
            )

            game_state[
                "running"
            ] = False

        # =========================
        # INVALID
        # =========================

        else:

            print(
                "\nInvalid choice."
            )

# =========================
# START GAME
# =========================

if __name__ == "__main__":

    run_game()