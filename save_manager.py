import json

from player import (
    player
)

from world_state import (
    world_state,
    ensure_world_state_defaults
)

from progression_manager import (
    progression_state
)

from skill_tree import (
    player_skills
)

from equipment_system import (
    equipment
)

from quest_manager import (

    active_quests,

    completed_quests
)

from world_event_manager import (

    active_world_events,

    completed_world_events
)

from dungeon_manager import (
    DUNGEONS
)

from settlement_manager import (
    SETTLEMENTS
)

from economy_manager import (
    economy_state
)

from faction_manager import (
    FACTIONS
)

from region_manager import (
    REGIONS
)

from story_manager import (
    story_state
)

from dialogue_manager import (
    npc_relationships
)

from relationship_manager import (
    social_state
)

from companion_manager import (

    active_companions,

    COMPANIONS
)

from dm_brain import (
    dm_state
)

# =========================
# SAVE FILE
# =========================

SAVE_FILE = "save_data.json"

# =========================
# SAVE GAME
# =========================

def save_game():

    save_data = {

        # =========================
        # SAVE VERSION
        # =========================

        "save_version": 2,

        # =========================
        # PLAYER
        # =========================

        "player": {

            "hp": player.hp,

            "max_hp": player.max_hp,

            "attack_bonus": player.attack_bonus,

            "defense": player.defense,

            "magic_power": player.magic_power,

            "evasion": player.evasion
        },

        # =========================
        # INVENTORY
        # =========================

        "inventory": world_state["player"]["inventory"],

        # =========================
        # EQUIPMENT
        # =========================

        "equipment": equipment,

        # =========================
        # PROGRESSION
        # =========================

        "progression": progression_state,

        # =========================
        # SKILLS
        # =========================

        "skills": player_skills,

        # =========================
        # WORLD STATE
        # =========================

        "world_state": world_state,

        # =========================
        # QUESTS
        # =========================

        "active_quests": active_quests,

        "completed_quests": completed_quests,

        # =========================
        # WORLD EVENTS
        # =========================

        "active_world_events":
            active_world_events,

        "completed_world_events":
            completed_world_events,

        # =========================
        # DUNGEONS
        # =========================

        "dungeons": DUNGEONS,

        # =========================
        # SETTLEMENTS
        # =========================

        "settlements": SETTLEMENTS,

        # =========================
        # ECONOMY
        # =========================

        "economy": economy_state,

        # =========================
        # FACTIONS
        # =========================

        "factions": FACTIONS,

        # =========================
        # REGIONS
        # =========================

        "regions": REGIONS,

        # =========================
        # STORY STATE
        # =========================

        "story_state": story_state,

        # =========================
        # NPC RELATIONSHIPS
        # =========================

        "npc_relationships":
            npc_relationships,

        # =========================
        # SOCIAL STATE
        # =========================

        "social_state":
            social_state,

        # =========================
        # COMPANIONS
        # =========================

        "companions":
            COMPANIONS,

        "active_companions":
            active_companions,

        # =========================
        # AI DIRECTOR
        # =========================

        "dm_state":
            dm_state
    }

    try:

        with open(

            SAVE_FILE,

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

    except Exception as error:

        print(
            "\nSave failed:"
        )

        print(error)

# =========================
# LOAD GAME
# =========================

def load_game():

    try:

        with open(

            SAVE_FILE,

            "r"

        ) as save_file:

            save_data = json.load(
                save_file
            )

    except FileNotFoundError:

        print(
            "\nNo save file found."
        )

        return

    except Exception as error:

        print(
            "\nLoad failed:"
        )

        print(error)

        return

    # =========================
    # PLAYER
    # =========================

    player.hp = save_data[
        "player"
    ]["hp"]

    player.max_hp = save_data[
        "player"
    ]["max_hp"]

    player.attack_bonus = save_data[
        "player"
    ]["attack_bonus"]

    player.defense = save_data[
        "player"
    ]["defense"]

    player.magic_power = save_data[
        "player"
    ]["magic_power"]

    player.evasion = save_data[
        "player"
    ]["evasion"]

    # =========================
    # INVENTORY
    # =========================

    world_state["player"]["inventory"].clear()

    world_state["player"]["inventory"].extend(

        save_data.get(
            "inventory",
            []
        )
    )

    # =========================
    # EQUIPMENT
    # =========================

    equipment.clear()

    equipment.update(

        save_data[
            "equipment"
        ]
    )

    # =========================
    # PROGRESSION
    # =========================

    progression_state.clear()

    progression_state.update(

        save_data[
            "progression"
        ]
    )

    # =========================
    # SKILLS
    # =========================

    player_skills.clear()

    player_skills.update(

        save_data[
            "skills"
        ]
    )

    # =========================
    # WORLD STATE
    # =========================

    world_state.clear()

    world_state.update(

        save_data[
            "world_state"
        ]
    )

    ensure_world_state_defaults()

    # =========================
    # QUESTS
    # =========================

    active_quests.clear()

    active_quests.extend(

        save_data[
            "active_quests"
        ]
    )

    completed_quests.clear()

    completed_quests.extend(

        save_data[
            "completed_quests"
        ]
    )

    # =========================
    # WORLD EVENTS
    # =========================

    active_world_events.clear()

    active_world_events.extend(

        save_data[
            "active_world_events"
        ]
    )

    completed_world_events.clear()

    completed_world_events.extend(

        save_data[
            "completed_world_events"
        ]
    )

    # =========================
    # DUNGEONS
    # =========================

    DUNGEONS.clear()

    DUNGEONS.update(

        save_data[
            "dungeons"
        ]
    )

    # =========================
    # SETTLEMENTS
    # =========================

    SETTLEMENTS.clear()

    SETTLEMENTS.update(

        save_data[
            "settlements"
        ]
    )

    # =========================
    # ECONOMY
    # =========================

    economy_state.clear()

    economy_state.update(

        save_data[
            "economy"
        ]
    )

    # =========================
    # FACTIONS
    # =========================

    FACTIONS.clear()

    FACTIONS.update(

        save_data[
            "factions"
        ]
    )

    # =========================
    # REGIONS
    # =========================

    REGIONS.clear()

    REGIONS.update(

        save_data[
            "regions"
        ]
    )

    # =========================
    # STORY STATE
    # =========================

    story_state.clear()

    story_state.update(

        save_data.get(

            "story_state",

            {}
        )
    )

    # =========================
    # NPC RELATIONSHIPS
    # =========================

    npc_relationships.clear()

    npc_relationships.update(

        save_data.get(

            "npc_relationships",

            {}
        )
    )

    # =========================
    # SOCIAL STATE
    # =========================

    social_state.clear()

    social_state.update(

        save_data.get(

            "social_state",

            {}
        )
    )

    # =========================
    # COMPANIONS
    # =========================

    COMPANIONS.clear()

    COMPANIONS.update(

        save_data.get(

            "companions",

            {}
        )
    )

    active_companions.clear()

    active_companions.extend(

        save_data.get(

            "active_companions",

            []
        )
    )

    # =========================
    # AI DIRECTOR
    # =========================

    dm_state.clear()

    dm_state.update(

        save_data.get(

            "dm_state",

            save_data.get(
                "director_state",
                {}
            )
        )
    )

    print(
        "\n=== GAME LOADED ==="
    )

# =========================
# AUTOSAVE
# =========================

def autosave():

    print(
        "\nAutosaving..."
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
            "\nSave deleted."
        )

    else:

        print(
            "\nNo save file exists."
        )

# =========================
# SAVE SUMMARY
# =========================

def show_save_summary():

    print(
        "\n=== SAVE DATA ==="
    )

    print(
        f"Player HP:"
        f" {player.hp}/"
        f"{player.max_hp}"
    )

    print(
        f"Inventory Items:"
        f" {len(world_state['player']['inventory'])}"
    )

    print(
        f"Active Quests:"
        f" {len(active_quests)}"
    )

    print(
        f"World Events:"
        f" {len(active_world_events)}"
    )

    print(
        f"Player Level:"
        f" {progression_state['level']}"
    )

    print(
        f"Companions:"
        f" {len(active_companions)}"
    )

    print(
        f"Campaign Theme:"
        f" {story_state['active_theme']}"
    )

# =========================
# SAVE VALIDATION
# =========================

def validate_save_data(

    save_data

):

    required_keys = [

        "player",

        "inventory",

        "equipment",

        "progression",

        "skills",

        "world_state",

        "story_state",

        "social_state",

        "dm_state"
    ]

    for key in required_keys:

        if key not in save_data:

            print(
                f"\nMissing save key:"
                f" {key}"
            )

            return False

    return True

# =========================
# SAFE LOAD
# =========================

def safe_load_game():

    try:

        with open(

            SAVE_FILE,

            "r"

        ) as save_file:

            save_data = json.load(
                save_file
            )

    except Exception as error:

        print(
            "\nSafe load failed:"
        )

        print(error)

        return

    if not validate_save_data(
        save_data
    ):

        print(
            "\nSave file corrupted."
        )

        return

    load_game()

# =========================
# EXPORT SAVE
# =========================

def export_save(

    export_name="exported_save.json"

):

    try:

        with open(

            SAVE_FILE,

            "r"

        ) as original:

            save_data = json.load(
                original
            )

        with open(

            export_name,

            "w"

        ) as export_file:

            json.dump(

                save_data,

                export_file,

                indent=4
            )

        print(
            "\nSave exported successfully."
        )

    except Exception as error:

        print(
            "\nExport failed:"
        )

        print(error)