# =========================
# PLAYER CREATION
# =========================

classes = {

    "warrior": {
        "hp": 70,
        "attack_bonus": 5
    },

    "mage": {
        "hp": 45,
        "attack_bonus": 10
    },

    "rogue": {
        "hp": 55,
        "attack_bonus": 7
    }
}

# =========================
# CREATE PLAYER
# =========================

def create_player():

    print("Choose your class:")
    print("Warrior")
    print("Mage")
    print("Rogue")

    player_class = input("> ").lower()

    player_hp = classes[player_class]["hp"]

    attack_bonus = classes[player_class]["attack_bonus"]

    print("\nYou chose:", player_class)

    return player_class, player_hp, attack_bonus


# =========================
# PLAYER LEVELING
# =========================

def check_level_up(
    player_level,
    player_xp,
    xp_to_next_level,
    player_hp,
    attack_bonus
):

    while player_xp >= xp_to_next_level:

        player_xp -= xp_to_next_level

        player_level += 1

        xp_to_next_level += 50

        player_hp += 10

        attack_bonus += 2

        print("\n=== LEVEL UP ===")
        print("You reached level", player_level)
        print("Max HP increased!")
        print("Attack power increased!")

    return (
        player_level,
        player_xp,
        xp_to_next_level,
        player_hp,
        attack_bonus
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
    xp_to_next_level
):

    print("\n=== STORY STATE ===")

    print("Cult Defeated:", cult_defeated)
    print("Dragon Defeated:", dragon_defeated)
    print("Knight Defeated:", knight_defeated)

    print("Gold:", player_gold)
    print("Reputation:", player_reputation)

    print("Level:", player_level)
    print("XP:", player_xp, "/", xp_to_next_level)