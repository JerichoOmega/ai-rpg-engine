import random

from event_bus import (
    emit
)

from faction_manager import (

    start_faction_war,

    evolve_factions,

    attempt_faction_takeover
)

from region_manager import (
    REGIONS
)

from economy_manager import (
    trigger_economic_crisis
)

from encounter_manager import (
    generate_world_event_encounter
)

from progression_manager import (
    get_world_tier
)

# =========================
# ACTIVE WORLD EVENTS
# =========================

active_world_events = []

completed_world_events = []

# =========================
# WORLD EVENT DATABASE
# =========================

WORLD_EVENTS = {

    "corruption_surge": {

        "severity": 25,

        "duration": 5,

        "effects": [

            "corruption",

            "enemy_strength"
        ]
    },

    "demonic_invasion": {

        "severity": 75,

        "duration": 10,

        "effects": [

            "elite_enemies",

            "region_instability"
        ]
    },

    "economic_collapse": {

        "severity": 60,

        "duration": 8,

        "effects": [

            "inflation",

            "scarcity"
        ]
    },

    "civil_war": {

        "severity": 80,

        "duration": 12,

        "effects": [

            "territory_conflict",

            "faction_war"
        ]
    },

    "void_breach": {

        "severity": 100,

        "duration": 15,

        "effects": [

            "legendary_enemies",

            "world_corruption"
        ]
    }
}

# =========================
# START WORLD EVENT
# =========================

def start_world_event(

    event_name

):

    event_data = WORLD_EVENTS.get(
        event_name
    )

    if not event_data:

        print(
            "\nUnknown world event."
        )

        return

    event = {

        "name": event_name,

        "severity": event_data[
            "severity"
        ],

        "duration": event_data[
            "duration"
        ],

        "remaining_duration": event_data[
            "duration"
        ],

        "effects": event_data[
            "effects"
        ],

        "active": True
    }

    active_world_events.append(
        event
    )

    print(
        f"\n=== WORLD EVENT STARTED ==="
    )

    print(
        f"Event:"
        f" {event_name}"
    )

    print(
        f"Severity:"
        f" {event['severity']}"
    )

    emit(

        "world_event_started",

        event=event
    )

    apply_world_event_effects(
        event
    )

# =========================
# APPLY WORLD EFFECTS
# =========================

def apply_world_event_effects(

    event

):

    event_name = event[
        "name"
    ]

    # =========================
    # CORRUPTION SURGE
    # =========================

    if event_name == "corruption_surge":

        for region in REGIONS.values():

            region[
                "danger"
            ] += 10

        print(
            "\nCorruption spreads"
            " across the land."
        )

    # =========================
    # DEMONIC INVASION
    # =========================

    elif event_name == "demonic_invasion":

        enemies = (
            generate_world_event_encounter()
        )

        print(
            "\nDemonic forces emerge."
        )

        emit(

            "demonic_invasion",

            enemies=enemies
        )

    # =========================
    # ECONOMIC COLLAPSE
    # =========================

    elif event_name == "economic_collapse":

        trigger_economic_crisis()

    # =========================
    # CIVIL WAR
    # =========================

    elif event_name == "civil_war":

        start_faction_war(

            "kingdom",

            "shadow_cult"
        )

    # =========================
    # VOID BREACH
    # =========================

    elif event_name == "void_breach":

        print(
            "\nReality begins tearing apart."
        )

        emit(
            "void_breach"
        )

# =========================
# UPDATE WORLD EVENTS
# =========================

def update_world_events():

    completed = []

    for event in active_world_events:

        event[
            "remaining_duration"
        ] -= 1

        print(
            f"\nWorld Event:"
            f" {event['name']}"
        )

        print(
            f"Remaining Duration:"
            f" {event['remaining_duration']}"
        )

        # =========================
        # ESCALATION
        # =========================

        escalate_world_event(
            event
        )

        # =========================
        # EVENT END
        # =========================

        if event[
            "remaining_duration"
        ] <= 0:

            completed.append(
                event
            )

    for event in completed:

        end_world_event(
            event
        )

# =========================
# ESCALATION
# =========================

def escalate_world_event(

    event

):

    severity = event[
        "severity"
    ]

    # =========================
    # HIGH SEVERITY EVENTS
    # =========================

    if severity >= 75:

        roll = random.randint(
            1,
            100
        )

        if roll <= 25:

            random_region = random.choice(
                list(
                    REGIONS.keys()
                )
            )

            attempt_faction_takeover(

                random_region,

                "shadow_cult"
            )

# =========================
# END WORLD EVENT
# =========================

def end_world_event(

    event

):

    event[
        "active"
    ] = False

    active_world_events.remove(
        event
    )

    completed_world_events.append(
        event
    )

    print(
        f"\n=== WORLD EVENT ENDED ==="
    )

    print(
        f"Event:"
        f" {event['name']}"
    )

    emit(

        "world_event_ended",

        event=event
    )

# =========================
# RANDOM WORLD EVENT
# =========================

def generate_random_world_event():

    world_tier = get_world_tier()

    event_pool = [

        "corruption_surge",

        "economic_collapse"
    ]

    if world_tier >= 3:

        event_pool.extend([

            "civil_war",

            "demonic_invasion"
        ])

    if world_tier >= 5:

        event_pool.append(
            "void_breach"
        )

    chosen_event = random.choice(
        event_pool
    )

    start_world_event(
        chosen_event
    )

# =========================
# SHOW ACTIVE EVENTS
# =========================

def show_active_world_events():

    print(
        "\n=== ACTIVE WORLD EVENTS ==="
    )

    if not active_world_events:

        print(
            "\nNo active world events."
        )

        return

    for event in active_world_events:

        print(
            f"\n{event['name']}"
        )

        print(
            f"Severity:"
            f" {event['severity']}"
        )

        print(
            f"Remaining:"
            f" {event['remaining_duration']}"
        )

# =========================
# SHOW COMPLETED EVENTS
# =========================

def show_completed_world_events():

    print(
        "\n=== COMPLETED EVENTS ==="
    )

    if not completed_world_events:

        print(
            "\nNo completed events."
        )

        return

    for event in completed_world_events:

        print(
            f"\n{event['name']}"
        )

# =========================
# GLOBAL DANGER
# =========================

def calculate_global_danger():

    danger = 0

    for event in active_world_events:

        danger += event[
            "severity"
        ]

    return danger

# =========================
# SHOW GLOBAL DANGER
# =========================

def show_global_danger():

    danger = calculate_global_danger()

    print(
        "\n=== GLOBAL DANGER ==="
    )

    print(
        f"Danger Level:"
        f" {danger}"
    )

    if danger >= 200:

        print(
            "\nThe world stands"
            " on the edge of collapse."
        )

# =========================
# WORLD EVENT SUMMARY
# =========================

def show_world_event_summary():

    print(
        "\n=== WORLD EVENT SUMMARY ==="
    )

    print(
        f"Active Events:"
        f" {len(active_world_events)}"
    )

    print(
        f"Completed Events:"
        f" {len(completed_world_events)}"
    )

    print(
        f"Global Danger:"
        f"{calculate_global_danger()}"
    )

# =========================
# LEGENDARY APOCALYPSE
# =========================

def trigger_apocalypse():

    print(
        "\n=== APOCALYPSE BEGINS ==="
    )

    start_world_event(
        "void_breach"
    )

    start_world_event(
        "civil_war"
    )

    start_world_event(
        "demonic_invasion"
    )

    emit(
        "apocalypse_started"
    )