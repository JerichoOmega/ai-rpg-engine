import json

from world_state import (
    world_state
)

# =========================
# SAVE FILE
# =========================

SAVE_FILE = "save_data.json"

# =========================
# SAVE GAME
# =========================

def save_game():

    try:

        with open(

            SAVE_FILE,

            "w"

        ) as save_file:

            json.dump(

                world_state,

                save_file,

                indent=4
            )

        print(
            "\n=== GAME SAVED ==="
        )

    except Exception as error:

        print(
            "\nSave failed:"
        )

        print(error)

# =========================
# LOAD GAME
# =========================

def load_game():

    global world_state

    try:

        with open(

            SAVE_FILE,

            "r"

        ) as save_file:

            loaded_data = json.load(
                save_file
            )

        # =========================
        # OVERWRITE WORLD STATE
        # =========================

        world_state.clear()

        world_state.update(
            loaded_data
        )

        print(
            "\n=== GAME LOADED ==="
        )

        return True

    except FileNotFoundError:

        print(
            "\nNo save file found."
        )

        return False

    except Exception as error:

        print(
            "\nLoad failed:"
        )

        print(error)

        return False

# =========================
# AUTO SAVE
# =========================

def autosave():

    print(
        "\n=== AUTOSAVE ==="
    )

    save_game()

# =========================
# DELETE SAVE
# =========================

def delete_save():

    import os

    if os.path.exists(
        SAVE_FILE
    ):

        os.remove(
            SAVE_FILE
        )

        print(
            "\nSave file deleted."
        )

    else:

        print(
            "\nNo save file exists."
        )

# =========================
# SAVE PREVIEW
# =========================

def show_save_summary():

    player = world_state["player"]

    print(
        "\n=== SAVE SUMMARY ==="
    )

    print(
        "Class:",
        player["class"]
    )

    print(
        "Level:",
        player["level"]
    )

    print(
        "Gold:",
        player["gold"]
    )

    print(
        "Current Region:",
        world_state[
            "regions"
        ]["current_region"]
    )

    print(
        "Party Size:",
        len(

            world_state[
                "companions"
            ]["party"]
        )
    )

    print(
        "Completed Quests:",
        len(

            world_state[
                "quests"
            ]["completed"]
        )
    )

    print(
        "World Chaos:",
        world_state[
            "world_conditions"
        ]["world_chaos"]
    )

# =========================
# SAVE VALIDATION
# =========================

def validate_save():

    required_sections = [

        "player",

        "companions",

        "quests",

        "factions",

        "regions",

        "world_conditions",

        "story_memory"
    ]

    missing_sections = []

    for section in required_sections:

        if section not in world_state:

            missing_sections.append(
                section
            )

    if len(missing_sections) == 0:

        print(
            "\nSave structure valid."
        )

        return True

    else:

        print(
            "\nMissing save sections:"
        )

        for section in missing_sections:

            print("•", section)

        return False