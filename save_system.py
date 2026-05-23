import json

# =========================
# SAVE GAME
# =========================

def save_game(
    player_hp,
    player_gold,
    player_level,
    player_xp,
    xp_to_next_level,
    inventory,
    equipped_weapon,
    weapon_bonus,
    player_reputation,
    cult_defeated,
    dragon_defeated,
    knight_defeated
):

    save_data = {

        "player_hp": player_hp,
        "player_gold": player_gold,
        "player_level": player_level,
        "player_xp": player_xp,
        "xp_to_next_level": xp_to_next_level,

        "inventory": inventory,

        "equipped_weapon": equipped_weapon,
        "weapon_bonus": weapon_bonus,

        "player_reputation": player_reputation,

        "cult_defeated": cult_defeated,
        "dragon_defeated": dragon_defeated,
        "knight_defeated": knight_defeated
    }

    with open("savegame.json", "w") as save_file:

        json.dump(save_data, save_file, indent=4)

    print("\nGame Saved!")


# =========================
# LOAD GAME
# =========================

def load_game():

    try:

        with open("savegame.json", "r") as save_file:

            save_data = json.load(save_file)

        print("\nGame Loaded!")

        return save_data

    except FileNotFoundError:

        print("\nNo save file found.")

        return None