from world_state import (
    world_state
)

from utils import (
    normalize_input,
    is_warrior,
    is_mage,
    is_rogue
)

# =========================
# PLAYER CREATION
# =========================

def create_player():

    print(
        "\n=== CHARACTER CREATION ==="
    )

    print(
        "\nChoose Your Class"
    )

    print(
        "(type warrior, mage, or rogue)"
    )

    print("• Warrior")
    print("• Mage")
    print("• Rogue")

    choice = normalize_input(
        input("> ")
    )

    player = world_state["player"]

    # =========================
    # WARRIOR
    # =========================

    if is_warrior(choice):

        player["class"] = "Warrior"

        player["hp"] = 140

        player["max_hp"] = 140

        player["attack_bonus"] = 8

        player["resource_name"] = "Stamina"

        player["resource"] = 100

        player["max_resource"] = 100

        player["defense"] = 5

        player["dodge"] = 5

        print(
            "\nA heavily armored fighter"
            " capable of surviving brutal combat."
        )

    # =========================
    # MAGE
    # =========================

    elif is_mage(choice):

        player["class"] = "Mage"

        player["hp"] = 90

        player["max_hp"] = 90

        player["attack_bonus"] = 12

        player["resource_name"] = "Mana"

        player["resource"] = 120

        player["max_resource"] = 120

        player["defense"] = 2

        player["dodge"] = 10

        print(
            "\nA master of destructive magic"
            " and arcane abilities."
        )

    # =========================
    # ROGUE
    # =========================

    elif is_rogue(choice):

        player["class"] = "Rogue"

        player["hp"] = 100

        player["max_hp"] = 100

        player["attack_bonus"] = 10

        player["resource_name"] = "Stamina"

        player["resource"] = 110

        player["max_resource"] = 110

        player["defense"] = 3

        player["dodge"] = 20

        print(
            "\nA swift assassin specializing"
            " in agility and critical strikes."
        )

    # =========================
    # DEFAULT
    # =========================

    else:

        print(
            "\nInvalid choice."
        )

        print(
            "Defaulting to Warrior."
        )

        player["class"] = "Warrior"

        player["hp"] = 140

        player["max_hp"] = 140

        player["attack_bonus"] = 8

        player["resource_name"] = "Stamina"

        player["resource"] = 100

        player["max_resource"] = 100

        player["defense"] = 5

        player["dodge"] = 5

    print(
        "\nYou are now a",
        player["class"]
    )

# =========================
# LEVEL SYSTEM
# =========================

def check_level_up():

    player = world_state["player"]

    while (

        player["xp"]

        >=

        player["xp_to_next_level"]

    ):

        player["level"] += 1

        player["xp"] -= (
            player["xp_to_next_level"]
        )

        player["xp_to_next_level"] += 50

        player["max_hp"] += 20

        player["hp"] = (
            player["max_hp"]
        )

        player["attack_bonus"] += 2

        player["max_resource"] += 10

        player["resource"] = (
            player["max_resource"]
        )

        print(
            "\n=== LEVEL UP ==="
        )

        print(
            "You reached level",
            player["level"]
        )

        print(
            "Max HP increased!"
        )

        print(
            "Attack power increased!"
        )

        print(
            "Maximum resource increased!"
        )

# =========================
# PLAYER STATUS DISPLAY
# =========================

def show_player_status():

    player = world_state["player"]

    print(
        "\n=== PLAYER STATUS ==="
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
        "XP:",
        str(player["xp"])
        + "/"
        + str(
            player["xp_to_next_level"]
        )
    )

    print(
        "HP:",
        str(player["hp"])
        + "/"
        + str(player["max_hp"])
    )

    print(
        player["resource_name"]
        + ":",
        str(player["resource"])
        + "/"
        + str(
            player["max_resource"]
        )
    )

    print(
        "Gold:",
        player["gold"]
    )

    print(
        "Attack Bonus:",
        player["attack_bonus"]
    )

    print(
        "Defense:",
        player["defense"]
    )

    print(
        "Dodge Chance:",
        str(player["dodge"])
        + "%"
    )

    print(
        "Weapon:",
        player["equipped_weapon"]
    )

# =========================
# STORY SUMMARY
# =========================

def show_story_state():

    player = world_state["player"]

    story_memory = world_state[
        "story_memory"
    ]

    print(
        "\n=== FINAL STORY STATE ==="
    )

    print(
        "Player Class:",
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
        "\n=== STORY MEMORY ==="
    )

    for memory in story_memory:

        print(
            memory,
            "-",
            story_memory[memory]
        )

    print(
        "\n=== PLAYER HISTORY ==="
    )

    history = world_state[
        "history"
    ]

    print(
        "Choices Made:",
        len(
            history["choices"]
        )
    )

    print(
        "Lore Discovered:",
        len(
            history[
                "discovered_lore"
            ]
        )
    )

    print(
        "Major Events:",
        len(
            history[
                "major_events"
            ]
        )
    )