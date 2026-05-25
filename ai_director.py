import random

from world_state import (
    world_state
)

from campaign_manager import (
    campaign_state
)

from encounter_generator import (
    generate_encounter,
    generate_narrative_encounter,
    generate_campaign_encounter
)

from quest_generator import (
    generate_quest
)

from event_bus import (
    subscribe,
    emit
)

# =========================
# DIRECTOR STATE
# =========================

director_state = {

    "tension": 25,

    "recent_battles": 0,

    "recent_story_events": 0,

    "session_phase": "exploration"
}

# =========================
# SHOW DIRECTOR STATE
# =========================

def show_director_state():

    print(
        "\n=== AI DIRECTOR ==="
    )

    print(
        "Tension:",
        director_state[
            "tension"
        ]
    )

    print(
        "Phase:",
        director_state[
            "session_phase"
        ]
    )

# =========================
# CHANGE TENSION
# =========================

def change_tension(

    amount

):

    director_state[
        "tension"
    ] += amount

    director_state[
        "tension"
    ] = max(

        0,

        min(
            director_state[
                "tension"
            ],
            100
        )
    )

    evaluate_pacing()

# =========================
# EVALUATE PACING
# =========================

def evaluate_pacing():

    tension = director_state[
        "tension"
    ]

    # =========================
    # LOW TENSION
    # =========================

    if tension <= 25:

        director_state[
            "session_phase"
        ] = "recovery"

    # =========================
    # MEDIUM TENSION
    # =========================

    elif tension <= 60:

        director_state[
            "session_phase"
        ] = "exploration"

    # =========================
    # HIGH TENSION
    # =========================

    else:

        director_state[
            "session_phase"
        ] = "crisis"

# =========================
# DIRECT NEXT EVENT
# =========================

def direct_gameplay():

    phase = director_state[
        "session_phase"
    ]

    print(
        "\n=== AI DIRECTOR DECISION ==="
    )

    # =========================
    # RECOVERY
    # =========================

    if phase == "recovery":

        print(
            "\nThe world briefly calms."
        )

        generate_narrative_encounter()

    # =========================
    # EXPLORATION
    # =========================

    elif phase == "exploration":

        roll = random.randint(
            1,
            100
        )

        if roll <= 50:

            generate_quest()

        else:

            generate_encounter()

    # =========================
    # CRISIS
    # =========================

    elif phase == "crisis":

        print(
            "\nDanger escalates rapidly."
        )

        generate_campaign_encounter()

        generate_encounter()

# =========================
# SESSION FLOW
# =========================

def evaluate_session_flow():

    battles = director_state[
        "recent_battles"
    ]

    story_events = director_state[
        "recent_story_events"
    ]

    # =========================
    # TOO MUCH COMBAT
    # =========================

    if battles >= 3:

        print(
            "\nAI Director slows combat pacing."
        )

        change_tension(
            -15
        )

    # =========================
    # TOO QUIET
    # =========================

    elif story_events >= 3:

        print(
            "\nAI Director escalates tension."
        )

        change_tension(
            15
        )

# =========================
# CAMPAIGN ESCALATION
# =========================

def evaluate_campaign_pressure():

    stage = campaign_state[
        "campaign_stage"
    ]

    if stage == "world_crisis":

        change_tension(
            20
        )

    elif stage == "final_catastrophe":

        change_tension(
            35
        )

# =========================
# EVENT REACTIONS
# =========================

def on_enemy_killed(

    event_data

):

    director_state[
        "recent_battles"
    ] += 1

    change_tension(
        10
    )

def on_narrative_encounter(

    event_data

):

    director_state[
        "recent_story_events"
    ] += 1

    change_tension(
        -5
    )

def on_quest_completed(

    event_data

):

    print(
        "\nAI Director recognizes"
        " story progression."
    )

    change_tension(
        -10
    )

def on_world_collapse(

    event_data

):

    print(
        "\nAI Director shifts"
        " into catastrophe pacing."
    )

    change_tension(
        30
    )

# =========================
# RESET SESSION TRACKERS
# =========================

def reset_session_trackers():

    director_state[
        "recent_battles"
    ] = 0

    director_state[
        "recent_story_events"
    ] = 0

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "enemy_killed",
    on_enemy_killed
)

subscribe(
    "narrative_encounter",
    on_narrative_encounter
)

subscribe(
    "quest_completed",
    on_quest_completed
)

subscribe(
    "world_collapse",
    on_world_collapse
)