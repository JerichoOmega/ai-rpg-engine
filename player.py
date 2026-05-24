# =========================
# PLAYER SYSTEM
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

    choice = input("> ").lower()

    # =========================
    # WARRIOR
    # =========================

    if (

        choice == "warrior"

    ):

        player_class = "Warrior"

        player_hp = 140

        attack_bonus = 8

        resource_name = "Stamina"

        player_resource = 100

        max_resource = 100

        player_defense = 5

        player_dodge = 5

        print(
            "\nA heavily armored fighter"
            " capable of surviving brutal combat."
        )

    # =========================
    # MAGE
    # =========================

    elif (

        choice == "mage"

    ):

        player_class = "Mage"

        player_hp = 90

        attack_bonus = 12

        resource_name = "Mana"

        player_resource = 120

        max_resource = 120

        player_defense = 2

        player_dodge = 10

        print(
            "\nA master of destructive magic"
            " and arcane abilities."
        )

    # =========================
    # ROGUE
    # =========================

    elif (

        choice == "rogue"

    ):

        player_class = "Rogue"

        player_hp = 100

        attack_bonus = 10

        resource_name = "Stamina"

        player_resource = 110

        max_resource = 110

        player_defense = 3

        player_dodge = 20

        print(
            "\nA swift assassin specializing"
            " in agility and critical strikes."
        )

    # =========================
    # DEFAULT CLASS
    # =========================

    else:

        print(
            "\nInvalid choice."
        )

        print(
            "Defaulting to Warrior."
        )

        player_class = "Warrior"

        player_hp = 140

        attack_bonus = 8

        resource_name = "Stamina"

        player_resource = 100

        max_resource = 100

        player_defense = 5

        player_dodge = 5

    print(
        "\nYou are now a",
        player_class
    )

    return (

        player_class,

        player_hp,

        attack_bonus,

        resource_name,

        player_resource,

        max_resource,

        player_defense,

        player_dodge
    )

# =========================
# LEVEL SYSTEM
# =========================

def check_level_up(

    player_level,
    player_xp,
    xp_to_next_level,
    player_hp,
    attack_bonus,
    max_resource

):

    while player_xp >= xp_to_next_level:

        player_level += 1

        player_xp -= xp_to_next_level

        xp_to_next_level += 50

        player_hp += 20

        attack_bonus += 2

        max_resource += 10

        print(
            "\n=== LEVEL UP ==="
        )

        print(
            "You reached level",
            player_level
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

    return (

        player_level,

        player_xp,

        xp_to_next_level,

        player_hp,

        attack_bonus,

        max_resource
    )

# =========================
# STORY STATE DISPLAY
# =========================

def show_story_state(

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

):

    print(
        "\n=== FINAL PLAYER STATE ==="
    )

    print(
        "Level:",
        player_level
    )

    print(
        "XP:",
        str(player_xp)
        + "/"
        + str(xp_to_next_level)
    )

    print(
        "Gold:",
        player_gold
    )

    print(
        "Reputation:",
        player_reputation
    )

    print(
        resource_name + ":",
        str(player_resource)
        + "/"
        + str(max_resource)
    )

    print(
        "Defense:",
        player_defense
    )

    print(
        "Dodge Chance:",
        str(player_dodge) + "%"
    )

    print(
        "\n=== STORY PROGRESS ==="
    )

    print(
        "Cult Defeated:",
        cult_defeated
    )

    print(
        "Dragon Defeated:",
        dragon_defeated
    )

    print(
        "Knight Defeated:",
        knight_defeated
    )