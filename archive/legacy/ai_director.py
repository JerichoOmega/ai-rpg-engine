import random

from world_state import (
    world_state
)

from story_manager import (
    story_state
)

from relationship_manager import (
    social_state
)

from world_event_manager import (
    calculate_global_danger
)

from encounter_manager import (
    generate_encounter,
    generate_world_event_encounter
)

from quest_manager import (
    generate_quest
)

from faction_manager import (
    FACTIONS
)

from companion_manager import (
    active_companions
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

    "recent_social_events": 0,

    "session_phase": "exploration",

    "campaign_mood": "uncertain",

    "last_major_event": None
}

# =========================
# SHOW DIRECTOR STATE
# =========================

def show_director_state():

    print(
        "\n=== AI DIRECTOR ==="
    )

    print(
        f"Tension:"
        f" {director_state['tension']}"
    )

    print(
        f"Phase:"
        f" {director_state['session_phase']}"
    )

    print(
        f"Mood:"
        f" {director_state['campaign_mood']}"
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

    if tension <= 25:

        director_state[
            "session_phase"
        ] = "recovery"

    elif tension <= 60:

        director_state[
            "session_phase"
        ] = "exploration"

    else:

        director_state[
            "session_phase"
        ] = "crisis"

# =========================
# CAMPAIGN MOOD
# =========================

def evaluate_campaign_mood():

    theme = story_state[
        "active_theme"
    ]

    global_danger = (
        calculate_global_danger()
    )

    if global_danger >= 200:

        director_state[
            "campaign_mood"
        ] = "apocalyptic"

    elif theme == "redemption":

        director_state[
            "campaign_mood"
        ] = "hopeful"

    elif theme == "corruption":

        director_state[
            "campaign_mood"
        ] = "dark"

    elif theme == "conquest":

        director_state[
            "campaign_mood"
        ] = "oppressive"

    else:

        director_state[
            "campaign_mood"
        ] = "uncertain"

# =========================
# DIRECT GAMEPLAY
# =========================

def direct_gameplay():

    evaluate_campaign_mood()

    phase = director_state[
        "session_phase"
    ]

    mood = director_state[
        "campaign_mood"
    ]

    print(
        "\n=== AI DIRECTOR DECISION ==="
    )

    print(
        f"Campaign Mood:"
        f" {mood}"
    )

    # =========================