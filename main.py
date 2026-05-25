import random

from world_state import (
    update_world_state
)

from session_manager import (
    start_session,
    end_session
)

from save_system import (
    save_game,
    load_game,
    autosave
)

from dm_brain import (
    update_dm_brain
)

from consistency_engine import (
    run_full_consistency_check
)

from memory_engine import (
    compress_memories
)

from quest_generator import (
    show_generated_quests
)

from dialogue_ai import (
    random_conversation
)

from npc_manager import (
    show_npc
)

from llm_bridge import (
    ai_narrate
)

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
).strip()

# =========================
# LOAD
# =========================

if choice == "2":

    load_game()

# =========================
# SESSION START
# =========================

start_session()

# =========================
# MAIN LOOP
# =========================

game_running = True

while game_running:

    # =========================
    # WORLD UPDATE
    # =========================

    update_world_state()

    compress_memories()

    run_full_consistency_check()

    # =========================
    # DM BRAIN
    # =========================

    update_dm_brain()

    # =========================
    # RANDOM AI STORY MOMENT
    # =========================

    roll = random.randint(
        1,
        100
    )

    if roll <= 30:

        random_conversation()

    elif roll <= 60:

        try:

            ai_narrate(

                "Narrate a mysterious "
                "event happening in the world."
            )

        except Exception:

            print(
                "\nThe wind carries uneasy whispers."
            )

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
        "2. Save Game"
    )

    print(
        "3. End Session"
    )

    player_choice = input(
        "\nChoose: "
    ).strip()

    # =========================
    # QUESTS
    # =========================

    if player_choice == "1":

        show_generated_quests()

    # =========================
    # SAVE
    # =========================

    elif player_choice == "2":

        save_game()

    # =========================
    # END
    # =========================

    elif player_choice == "3":

        game_running = False

    autosave()

# =========================
# SESSION END
# =========================

end_session()

save_game()

print(
    "\n=== SESSION COMPLETE ==="
)