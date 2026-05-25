from world_state import (
    world_state
)

from npc_manager import (
    NPCS
)

from region_manager import (
    REGIONS
)

# =========================
# CONSISTENCY ERRORS
# =========================

consistency_errors = []

# =========================
# ADD ERROR
# =========================

def add_error(

    error_message

):

    consistency_errors.append(
        error_message
    )

    print(
        "\n[CONSISTENCY ERROR]"
    )

    print(
        error_message
    )

# =========================
# CLEAR ERRORS
# =========================

def clear_errors():

    consistency_errors.clear()

# =========================
# SHOW ERRORS
# =========================

def show_errors():

    print(
        "\n=== CONSISTENCY ERRORS ==="
    )

    if len(consistency_errors) == 0:

        print(
            "No consistency issues detected."
        )

        return

    for error in consistency_errors:

        print(
            "•",
            error
        )

# =========================
# VALIDATE NPCS
# =========================

def validate_npcs():

    for npc_name in NPCS:

        npc = NPCS[npc_name]

        # =========================
        # DEAD NPC MEMORY
        # =========================

        if (

            npc["alive"] is False

            and

            npc["relationship"] > 0

        ):

            add_error(

                f"{npc_name}"
                " is dead but still"
                " has active relationships."
            )

        # =========================
        # INVALID REGION
        # =========================

        if (

            npc["region"]

            not in REGIONS

        ):

            add_error(

                f"{npc_name}"
                " exists in unknown region:"
                f" {npc['region']}"
            )

# =========================
# VALIDATE REGIONS
# =========================

def validate_regions():

    for region_name in REGIONS:

        region = REGIONS[
            region_name
        ]

        # =========================
        # INVALID DANGER
        # =========================

        if (

            region["danger"] < 0

            or

            region["danger"] > 100

        ):

            add_error(

                f"{region_name}"
                " has invalid danger level."
            )

        # =========================
        # INVALID FACTION
        # =========================

        faction = region["faction"]

        if (

            faction

            not in world_state[
                "factions"
            ]

            and

            faction != "none"

        ):

            add_error(

                f"{region_name}"
                " references unknown faction:"
                f" {faction}"
            )

# =========================
# VALIDATE QUESTS
# =========================

def validate_quests():

    quests = world_state[
        "quests"
    ]

    # =========================
    # DUPLICATE QUESTS
    # =========================

    completed = quests[
        "completed"
    ]

    active = quests[
        "active"
    ]

    for quest_name in completed:

        if quest_name in active:

            add_error(

                f"Quest '{quest_name}'"
                " is both active"
                " and completed."
            )

# =========================
# VALIDATE STORY MEMORY
# =========================

def validate_story_memory():

    story_memory = world_state[
        "story_memory"
    ]

    # =========================
    # DRAGON CONSISTENCY
    # =========================

    if (

        story_memory.get(
            "dragon_slain"
        )

        and

        "Dragon Slayer"

        not in world_state[
            "quests"
        ]["completed"]

    ):

        add_error(

            "Dragon marked slain"
            " before Dragon Slayer"
            " quest completion."
        )

# =========================
# VALIDATE WORLD EVENTS
# =========================

def validate_world_events():

    events = world_state[
        "events"
    ]

    # =========================
    # DUPLICATE EVENTS
    # =========================

    seen = set()

    for event in events:

        if event in seen:

            add_error(

                f"Duplicate world event:"
                f" {event}"
            )

        seen.add(event)

# =========================
# VALIDATE FACTIONS
# =========================

def validate_factions():

    factions = world_state[
        "factions"
    ]

    for faction_name in factions:

        reputation = factions[
            faction_name
        ]

        # =========================
        # INVALID REPUTATION
        # =========================

        if (

            reputation < -100

            or

            reputation > 100

        ):

            add_error(

                f"{faction_name}"
                " reputation outside"
                " valid range."
            )

# =========================
# FULL VALIDATION
# =========================

def run_full_consistency_check():

    clear_errors()

    print(
        "\n=== RUNNING CONSISTENCY CHECK ==="
    )

    validate_npcs()

    validate_regions()

    validate_quests()

    validate_story_memory()

    validate_world_events()

    validate_factions()

    print(
        "\nConsistency check complete."
    )

    show_errors()

# =========================
# AUTO FIXES
# =========================

def auto_fix_simple_issues():

    print(
        "\n=== AUTO FIXING ==="
    )

    # =========================
    # FIX REGION DANGER
    # =========================

    for region_name in REGIONS:

        region = REGIONS[
            region_name
        ]

        region["danger"] = max(

            0,

            min(
                region["danger"],
                100
            )
        )

    # =========================
    # FIX FACTION REPUTATION
    # =========================

    for faction_name in world_state[
        "factions"
    ]:

        reputation = world_state[
            "factions"
        ][faction_name]

        world_state[
            "factions"
        ][faction_name] = max(

            -100,

            min(
                reputation,
                100
            )
        )

    print(
        "\nSimple fixes applied."
    )