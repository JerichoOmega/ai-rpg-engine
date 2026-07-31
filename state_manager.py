import json
import copy
import os

from world_state import (
    world_state,
    ensure_world_state_defaults
)

# =========================
# SAVE CONFIG
# =========================

SAVE_FILE = "save_data.json"

BACKUP_FILE = "save_backup.json"

SAVE_VERSION = 1

# =========================
# SAVE GAME
# =========================

def save_game():

    try:

        # Capture any combat-side mutations (HP, gold, stats) into
        # world_state["player"] before serialising so that progress
        # made since hero selection is not lost.
        from player import sync_world_state_from_player
        sync_world_state_from_player()

        save_data = {

            "version": SAVE_VERSION,

            "world_state": world_state
        }

        # =========================
        # CREATE BACKUP
        # =========================

        if os.path.exists(
            SAVE_FILE
        ):

            with open(

                SAVE_FILE,

                "r"

            ) as old_save:

                old_data = json.load(
                    old_save
                )

            with open(

                BACKUP_FILE,

                "w"

            ) as backup:

                json.dump(

                    old_data,

                    backup,

                    indent=4
                )

        # =========================
        # WRITE SAVE
        # =========================

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

        print(
            "Save Version:",
            SAVE_VERSION
        )

        return True

    except Exception as error:

        print(
            "\nSave failed:"
        )

        print(error)

        return False

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

        # =========================
        # VALIDATE VERSION
        # =========================

        version = save_data.get(
            "version",
            0
        )

        if version != SAVE_VERSION:

            print(
                "\nSave version mismatch."
            )

            print(
                "Attempting migration..."
            )

            save_data = migrate_save(
                save_data
            )

        loaded_state = save_data.get(
            "world_state"
        )

        if loaded_state is None:

            print(
                "\nInvalid save structure."
            )

            return False

        # If world_state is present but has
        # the wrong type (e.g. a string due to
        # corruption), treat it as empty so
        # ensure_world_state_defaults() can
        # fill in safe defaults rather than
        # letting world_state.update() crash.

        if not isinstance(
            loaded_state, dict
        ):

            print(
                "\nworld_state has unexpected"
                " type; loading defaults."
            )

            loaded_state = {}

        # =========================
        # LOAD INTO MEMORY
        # =========================

        # Snapshot the live state so we can
        # restore it if validation fails OR if
        # an exception is raised during the
        # update — prevents a rejected or
        # interrupted load from corrupting the
        # current session.

        _snapshot = copy.deepcopy(
            world_state
        )

        world_state.clear()

        world_state.update(
            loaded_state
        )

        # Backfill any keys absent in saves
        # written before the refactor BEFORE
        # validation so the check sees the
        # complete schema, not the raw sparse
        # saved state.

        ensure_world_state_defaults()

        # =========================
        # VALIDATE STRUCTURE
        # =========================

        if not validate_world_state(
            world_state
        ):

            print(
                "\nSave validation failed."
                " Restoring previous state."
            )

            world_state.clear()

            world_state.update(
                _snapshot
            )

            return False

        # Re-populate the combat-side Player object from the
        # just-loaded world_state["player"] so combat.py always
        # sees the selected hero's stats, not stale defaults.
        from player import sync_player_from_world_state
        sync_player_from_world_state()

        print(
            "\n=== GAME LOADED ==="
        )

        print(
            "Save Version:",
            version
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

        # Restore the pre-load snapshot if
        # an exception was raised after
        # world_state was already cleared.
        # _snapshot may not exist if the
        # exception was raised before it was
        # assigned (e.g. during JSON parsing),
        # so guard with locals().

        if "_snapshot" in dir():

            try:

                world_state.clear()

                world_state.update(
                    _snapshot
                )

            except Exception:

                pass

        return False

# =========================
# AUTOSAVE
# =========================

def autosave():

    print(
        "\n=== AUTOSAVE ==="
    )

    save_game()

# =========================
# SAVE MIGRATION
# =========================

def migrate_save(save_data):

    old_version = save_data.get(
        "version",
        0
    )

    print(
        f"\nMigrating save"
        f" from version"
        f" {old_version}"
    )

    # =========================
    # VERSION 0 → 1 MIGRATION
    # =========================

    if old_version < 1:

        if (

            "world_state"

            not in save_data

        ):

            # Pre-refactor saves serialised the
            # world_state contents directly at
            # the top level of the save file
            # rather than nested under a
            # "world_state" key.  Collect any
            # recognised world-state keys and
            # move them into the nested dict so
            # the rest of load_game() finds them.

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

            nested = {}

            for key in list(save_data.keys()):

                if key in _WORLD_STATE_KEYS:

                    nested[key] = (
                        save_data.pop(key)
                    )

            save_data[
                "world_state"
            ] = nested

    # =========================
    # UPDATE VERSION
    # =========================

    save_data[
        "version"
    ] = SAVE_VERSION

    print(
        "\nMigration complete."
    )

    return save_data

# =========================
# WORLD STATE VALIDATION
# =========================

def validate_world_state(

    state

):

    # "npcs" is owned by npc_manager.py and is
    # not a key in the world_state schema; it
    # has been removed from the required list.
    required_sections = [

        "time",

        "player",

        "companions",

        "world_conditions",

        "factions",

        "regions",

        "quests",

        "story_memory",

        "history",

        "events"
    ]

    missing_sections = []

    for section in required_sections:

        if section not in state:

            missing_sections.append(
                section
            )

    if len(missing_sections) > 0:

        print(
            "\nMissing Sections:"
        )

        for section in missing_sections:

            print("•", section)

        return False

    return True

# =========================
# DELETE SAVE
# =========================

def delete_save():

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
            "\nNo save exists."
        )

# =========================
# RESTORE BACKUP
# =========================

def restore_backup():

    try:

        with open(

            BACKUP_FILE,

            "r"

        ) as backup:

            backup_data = json.load(
                backup
            )

        with open(

            SAVE_FILE,

            "w"

        ) as save_file:

            json.dump(

                backup_data,

                save_file,

                indent=4
            )

        print(
            "\nBackup restored."
        )

        return True

    except Exception as error:

        print(
            "\nBackup restore failed:"
        )

        print(error)

        return False

# =========================
# SNAPSHOT SYSTEM
# =========================

def create_snapshot():

    snapshot = copy.deepcopy(
        world_state
    )

    return snapshot

def restore_snapshot(snapshot):

    world_state.clear()

    world_state.update(
        snapshot
    )

    print(
        "\nWorld state restored"
        " from snapshot."
    )

# =========================
# SAVE SUMMARY
# =========================

def show_save_summary():

    player = world_state["player"]

    print(
        "\n=== SAVE SUMMARY ==="
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
        "Region:",
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
# DEBUG STATE REPORT
# =========================

def debug_state_report():

    print(
        "\n=== DEBUG REPORT ==="
    )

    print(
        "Save Version:",
        SAVE_VERSION
    )

    print(
        "Player Exists:",
        "player" in world_state
    )

    print(
        "Quest Count:",
        len(

            world_state[
                "quests"
            ]["active"]
        )
    )

    print(
        "Party Members:",
        len(

            world_state[
                "companions"
            ]["party"]
        )
    )

    print(
        "Known Regions:",
        len(

            world_state[
                "regions"
            ]["discovered_regions"]
        )
    )

    print(
        "Major Events:",
        len(

            world_state[
                "history"
            ]["major_events"]
        )
    )
