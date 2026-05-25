import random

# =========================
# CORE WORLD
# =========================

from world_state import (
    world_state,
    update_world_state,
    show_world_state
)

# =========================
# SAVE + STATE
# =========================

from save_system import (
    save_game,
    load_game,
    autosave
)

from state_manager import (
    validate_world_state
)

# =========================
# SESSION SYSTEM
# =========================

from session_manager import (
    start_session,
    end_session,
    show_campaign_timeline
)

# =========================
# AI DIRECTOR
# =========================

from ai_director import (
    direct_gameplay,
    show_director_state,
    evaluate_session_flow,
    reset_session_trackers
)

# =========================
# CAMPAIGN
# =========================

from campaign_manager import (
    show_campaign_status,
    evaluate_campaign_progress
)

# =========================
# QUESTS
# =========================

from quests import (
    initialize_quests,
    show_quests
)

from quest_generator import (
    generate_quest,
    show_generated_quests
)

# =========================
# NPCS
# =========================

from npc_manager import (
    random_npc_event,
    show_npc
)

# =========================
# DIALOGUE
# =========================

from dialogue_ai import (
    random_conversation
)

# =========================
# REGIONS
# =========================

from region_manager import (
    random_region_event
)

# =========================
# ENCOUNTERS
# =========================

from encounter_generator import (
    random_travel_event
)

# =========================
# MEMORY
# =========================

from memory_engine import (
    show_memories,
    compress_memories
)

# =========================
# CONSISTENCY
# =========================

from consistency_engine import (
    run_full_consistency_check,
    auto_fix_simple_issues
)

# =========================
# NARRATIVE AI
# =========================

from narrative_ai import (
    generate_story_hook
)

# =========================
# EVENT SYSTEM
# =========================

from event_bus import (
    emit
)

# =========================
# FORCE SYSTEM IMPORTS
# =========================

import story_manager
import faction_manager
import narrative_ai
import memory_engine
import session_manager

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

choice = input(
    "\n> "
).strip().lower()

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
            "\nStarting new campaign..."
        )

# =========================
# VALIDATION
# =========================

run_full_consistency_check()

auto_fix_simple_issues()

validate_world_state(
    world_state
)

# =========================
# SESSION START
# =========================

start_session()

# =========================
# INITIALIZE QUESTS
# =========================

initialize_quests()

# =========================
# MAIN LOOP
# =========================

game_running = True

while game_running:

    # =========================
    # WORLD UPDATE
    # =========================

    update_world_state()

    evaluate_campaign_progress()

    evaluate_session_flow()

    compress_memories()

    # =========================
    # AI DIRECTOR
    # =========================

    direct_gameplay()

    # =========================
    # RANDOM WORLD EVENTS
    # =========================

    random_roll = random.randint(
        1,
        100
    )

    if random_roll <= 25:

        random_npc_event()

    elif random_roll <= 50:

        random_region_event()

    elif random_roll <= 70:

        random_conversation()

    elif random_roll <= 85:

        random_travel_event()

    else:

        generate_story_hook()

    # =========================
    # PLAYER MENU
    # =========================

    print(
        "\n========================"
    )

    print(
        "1. Show Quests"
    )

    print(
        "2. Show Generated Quests"
    )

    print(
        "3. Show Campaign Status"
    )

    print(
        "4. Show Timeline"
    )

    print(
        "5. Show Memories"
    )

    print(
        "6. Save Game"
    )

    print(
        "7. End Session"
    )

    player_choice = input(
        "\nChoose: "
    ).strip()

    # =========================
    # QUESTS
    # =========================

    if player_choice == "1":

        show_quests()

    elif player_choice == "2":

        show_generated_quests()

    # =========================
    # CAMPAIGN
    # =========================

    elif player_choice == "3":

        show_campaign_status()

    # =========================
    # TIMELINE
    # =========================

    elif player_choice == "4":

        show_campaign_timeline()

    # =========================
    # MEMORIES
    # =========================

    elif player_choice == "5":

        show_memories()

    # =========================
    # SAVE
    # =========================

    elif player_choice == "6":

        save_game()

    # =========================
    # END SESSION
    # =========================

    elif player_choice == "7":

        game_running = False

    # =========================
    # AUTOSAVE
    # =========================

    autosave()

    reset_session_trackers()

# =========================
# SESSION END
# =========================

end_session()

# =========================
# FINAL SAVE
# =========================

save_game()

# =========================
# GAME END
# =========================

print(
    "\n=== SESSION COMPLETE ==="
)

show_world_state()