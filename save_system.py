import json

from companions import companions

from quests import quests

from world_state import world_state

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
    knight_defeated,
    player_class,
    resource_name,
    player_resource,
    max_resource,
    player_defense,
    player_dodge,
    factions,
    story_memory,
    party

):

    save_data = {

        # =========================
        # PLAYER DATA
        # =========================

        "player_hp": player_hp,

        "player_gold": player_gold,

        "player_level": player_level,

        "player_xp": player_xp,

        "xp_to_next_level": xp_to_next_level,

        "player_class": player_class,

        "resource_name": resource_name,

        "player_resource": player_resource,

        "max_resource": max_resource,

        "player_defense": player_defense,

        "player_dodge": player_dodge,

        # =========================
        # INVENTORY / EQUIPMENT
        # =========================

        "inventory": inventory,

        "equipped_weapon": equipped_weapon,

        "weapon_bonus": weapon_bonus,

        # =========================
        # STORY FLAGS
        # =========================

        "player_reputation": player_reputation,

        "cult_defeated": cult_defeated,

        "dragon_defeated": dragon_defeated,

        "knight_defeated": knight_defeated,

        # =========================
        # FACTIONS
        # =========================

        "factions": factions,

        # =========================
        # STORY MEMORY
        # =========================

        "story_memory": story_memory,

        # =========================
        # PARTY
        # =========================

        "party": party,

        # =========================
        # COMPANIONS
        # =========================

        "companions": companions,

        # =========================
        # QUESTS
        # =========================

        "quests": quests,

        # =========================
        # WORLD STATE
        # =========================

        "world_state": world_state
    }

    with open(
        "savegame.json",
        "w"
    ) as save_file:

        json.dump(
            save_data,
            save_file,
            indent=4
        )

    print(
        "\n=== GAME SAVED ==="
    )

# =========================
# LOAD GAME
# =========================

def load_game():

    try:

        with open(
            "savegame.json",
            "r"
        ) as save_file:

            save_data = json.load(
                save_file
            )

        # =========================
        # RESTORE COMPANIONS
        # =========================

        companions.clear()

        companions.update(
            save_data[
                "companions"
            ]
        )

        # =========================
        # RESTORE QUESTS
        # =========================

        quests.clear()

        quests.update(
            save_data[
                "quests"
            ]
        )

        # =========================
        # RESTORE WORLD STATE
        # =========================

        world_state.clear()

        world_state.update(
            save_data[
                "world_state"
            ]
        )

        print(
            "\n=== SAVE LOADED ==="
        )

        return save_data

    except FileNotFoundError:

        print(
            "\nNo save file found."
        )

        return None