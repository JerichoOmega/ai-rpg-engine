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

    # Capture combat- / skill- / equipment-mutated Player object fields
    # into world_state["player"] before serialising.  world_state is the
    # single authoritative persisted representation; this call makes
    # sure any direct `player.*` mutations since the last save are
    # reflected there.  Gold, inventory, name, class, race, hero_key and
    # other world-state-helper-managed fields are NOT overwritten.
    from player import sync_world_state_from_player
    sync_world_state_from_player()

    save_data = {

        # =========================
        # SAVE VERSION
        # =========================

        "save_version": 2,

        # NOTE: the top-level "player" section has been removed.
        # world_state["player"] (serialised below) is the single
        # authoritative representation; duplicating combat-side
        # Player fields here created a split that caused stale
        # values to win on load.  The load path's hasattr/setattr
        # loop now receives an empty dict and is a no-op; the
        # subsequent sync_player_from_world_state() call restores
        # the Player object from world_state["player"].

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

    # Guard: json.load() can return any JSON
    # value (list, string, number, etc.).
    # Every path below calls save_data.get()
    # so we must confirm it is a dict before
    # proceeding.

    if not isinstance(save_data, dict):

        print(
            "\nSave file is not a valid"
            " JSON object — cannot load."
        )

        return

    # =========================
    # PLAYER
    # =========================

    # Use .get() throughout so that saves
    # written before the refactor (which may
    # be missing any of these keys) load
    # cleanly instead of raising KeyError.
    # Only restore attributes that the Player
    # object actually declares; unknown fields
    # in the save are silently ignored so that
    # schema drift never crashes the load.

    # Type-safe helper: return the value only
    # when it is the expected container type;
    # fall back to `default` otherwise so
    # wrong-typed data never reaches .update()
    # or .extend().

    def _get_dict(key, fallback=None):
        v = save_data.get(key, fallback or {})
        return v if isinstance(v, dict) else {}

    def _get_list(key, fallback=None):
        v = save_data.get(key, fallback or [])
        return v if isinstance(v, list) else []

    _saved_player = _get_dict("player")

    for _attr, _val in _saved_player.items():

        if hasattr(player, _attr):

            setattr(player, _attr, _val)

    # =========================
    # INVENTORY
    # =========================

    world_state["player"]["inventory"].clear()

    world_state["player"]["inventory"].extend(
        _get_list("inventory")
    )

    # =========================
    # EQUIPMENT
    # =========================

    equipment.clear()

    equipment.update(
        _get_dict("equipment")
    )

    # =========================
    # PROGRESSION
    # =========================

    progression_state.clear()

    progression_state.update(
        _get_dict("progression")
    )

    # =========================
    # SKILLS
    # =========================

    player_skills.clear()

    player_skills.update(
        _get_dict("skills")
    )

    # =========================
    # WORLD STATE
    # =========================

    # If the save was written in the old flat
    # format (world_state contents at top
    # level, no nested "world_state" key),
    # collect those keys before updating so
    # legacy data is not silently discarded.

    _WORLD_STATE_KEYS = {
        "time", "player", "inventory",
        "quests", "companions", "factions",
        "regions", "world_conditions",
        "story_memory", "events", "history",
        "sessions", "civil_war",
        "cult_rising", "mages_rebellion",
        "dragon_alive", "world_chaos",
        "npcs",
    }

    if "world_state" in save_data:

        _raw_ws = save_data["world_state"]

    else:

        # Legacy flat format — gather top-
        # level world-state keys.

        _raw_ws = {
            k: save_data[k]
            for k in save_data
            if k in _WORLD_STATE_KEYS
        }

    # Guard: world_state must be a dict;
    # if not, start from an empty baseline
    # so ensure_world_state_defaults() fills
    # in safe defaults rather than crashing.

    if not isinstance(_raw_ws, dict):

        _raw_ws = {}

    world_state.clear()

    world_state.update(
        _raw_ws
    )

    # Backfill any keys absent in pre-refactor
    # saves immediately after loading so every
    # code path can assume the full schema.

    ensure_world_state_defaults()

    # =========================
    # QUESTS
    # =========================

    active_quests.clear()

    active_quests.extend(
        _get_list("active_quests")
    )

    completed_quests.clear()

    completed_quests.extend(
        _get_list("completed_quests")
    )

    # =========================
    # WORLD EVENTS
    # =========================

    active_world_events.clear()

    active_world_events.extend(
        _get_list("active_world_events")
    )

    completed_world_events.clear()

    completed_world_events.extend(
        _get_list("completed_world_events")
    )

    # =========================
    # DUNGEONS
    # =========================

    DUNGEONS.clear()

    DUNGEONS.update(
        _get_dict("dungeons")
    )

    # =========================
    # SETTLEMENTS
    # =========================

    SETTLEMENTS.clear()

    SETTLEMENTS.update(
        _get_dict("settlements")
    )

    # =========================
    # ECONOMY
    # =========================

    economy_state.clear()

    economy_state.update(
        _get_dict("economy")
    )

    # =========================
    # FACTIONS
    # =========================

    FACTIONS.clear()

    FACTIONS.update(
        _get_dict("factions")
    )

    # =========================
    # REGIONS
    # =========================

    REGIONS.clear()

    REGIONS.update(
        _get_dict("regions")
    )

    # =========================
    # STORY STATE
    # =========================

    story_state.clear()

    story_state.update(
        _get_dict("story_state")
    )

    # =========================
    # NPC RELATIONSHIPS
    # =========================

    npc_relationships.clear()

    npc_relationships.update(
        _get_dict("npc_relationships")
    )

    # =========================
    # SOCIAL STATE
    # =========================

    social_state.clear()

    social_state.update(
        _get_dict("social_state")
    )

    # =========================
    # COMPANIONS
    # =========================

    COMPANIONS.clear()

    COMPANIONS.update(
        _get_dict("companions")
    )

    active_companions.clear()

    active_companions.extend(
        _get_list("active_companions")
    )

    # =========================
    # AI DIRECTOR
    # =========================

    dm_state.clear()

    # "dm_state" was previously saved as
    # "director_state" — accept both names.

    _dm = _get_dict("dm_state")

    if not _dm:

        _dm = _get_dict("director_state")

    dm_state.update(_dm)

    # Re-populate the combat-side Player object from the just-loaded
    # world_state["player"] so every field (name, class, race,
    # hero_key, inventory, etc.) is current in both representations.
    from player import sync_player_from_world_state
    sync_player_from_world_state()

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

    # Structural validation: reject the save
    # before any mutation if the data cannot
    # be safely loaded, so that Safe Load
    # never delegates to the loader with
    # malformed input.

    if not isinstance(save_data, dict):

        print(
            "\nSave file is not a"
            " valid JSON object."
        )

        return False

    # Must contain at least one recognisable
    # root key to be considered a game save.

    if (

        "player" not in save_data

        and "world_state" not in save_data

    ):

        print(
            "\nSave file missing required"
            " keys — not a recognised game"
            " save format."
        )

        return False

    # When present, dict-typed sections must
    # actually be dicts, and list-typed
    # sections must actually be lists.
    # Wrong types here indicate corruption.

    _required_dicts = [
        "player", "world_state",
        "equipment", "progression",
        "skills", "economy",
        "factions", "regions",
        "dungeons", "settlements",
    ]

    for _key in _required_dicts:

        _val = save_data.get(_key)

        if _val is not None and not isinstance(
            _val, dict
        ):

            print(
                f"\nSave file: '{_key}'"
                f" must be an object,"
                f" got {type(_val).__name__}."
            )

            return False

    _required_lists = [
        "inventory",
        "active_quests",
        "completed_quests",
        "active_world_events",
        "completed_world_events",
        "active_companions",
    ]

    for _key in _required_lists:

        _val = save_data.get(_key)

        if _val is not None and not isinstance(
            _val, list
        ):

            print(
                f"\nSave file: '{_key}'"
                f" must be an array,"
                f" got {type(_val).__name__}."
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