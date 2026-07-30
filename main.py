from game_loop import (
    run_game
)

from save_manager import (

    load_game,

    safe_load_game,

    autosave
)

# =========================
# MAIN MENU
# =========================

def show_start_menu():

    print(
        "\n=== AI RPG ==="
    )

    print(
        "\n1. New Game"
    )

    print(
        "2. Load Game"
    )

    print(
        "3. Safe Load"
    )

    print(
        "4. Exit"
    )

# =========================
# START GAME
# =========================

def start_new_game():

    print(
        "\nStarting new adventure..."
    )

    run_game()

# =========================
# LOAD GAME
# =========================

def continue_game():

    print(
        "\nLoading save..."
    )

    load_game()

    run_game()

# =========================
# SAFE LOAD
# =========================

def continue_safe_load():

    print(
        "\nRunning safe load..."
    )

    safe_load_game()

    run_game()

# =========================
# MAIN LOOP
# =========================

def main():

    running = True

    while running:

        show_start_menu()

        choice = input(
            "\nChoose: "
        ).strip()

        # =========================
        # NEW GAME
        # =========================

        if choice == "1":

            start_new_game()

        # =========================
        # LOAD GAME
        # =========================

        elif choice == "2":

            continue_game()

        # =========================
        # SAFE LOAD
        # =========================

        elif choice == "3":

            continue_safe_load()

        # =========================
        # EXIT
        # =========================

        elif choice == "4":

            print(
                "\nClosing game..."
            )

            autosave()

            running = False

        # =========================
        # INVALID
        # =========================

        else:

            print(
                "\nInvalid choice."
            )

# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":

    main()