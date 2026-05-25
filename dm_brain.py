import random

from world_state import (
    world_state
)

from campaign_manager import (
    campaign_state,
    generate_campaign_event
)

from ai_director import (
    change_tension
)

from encounter_generator import (
    generate_encounter,
    generate_narrative_encounter
)

from npc_manager import (
    random_npc_event
)

from region_manager import (
    random_region_event
)

from llm_bridge import (
    ai_narrate,
    ai_generate_quest
)

from memory_engine import (
    retrieve_memories
)

from event_bus import (
    emit,
    subscribe
)

# =========================
# DM STATE
# =========================

dm_state = {

    "current_focus": "exploration",

    "story_pressure": 25,

    "emotional_tone": "neutral",

    "priority_threat": "shadow_cult",

    "active_threads": []
}

# =========================
# STORY PRESSURE
# =========================

def change_story_pressure(

    amount

):

    dm_state[
        "story_pressure"
    ] += amount

    dm_state[
        "story_pressure"
    ] = max(

        0,

        min(
            dm_state[
                "story_pressure"
            ],
            100
        )
    )

# =========================
# EVALUATE STATE
# =========================

def evaluate_story_state():

    pressure = dm_state[
        "story_pressure"
    ]

    if pressure <= 25:

        dm_state[
            "current_focus"
        ] = "recovery"

    elif pressure <= 60:

        dm_state[
            "current_focus"
        ] = "exploration"

    else:

        dm_state[
            "current_focus"
        ] = "crisis"

# =========================
# MAIN DM UPDATE
# =========================

def update_dm_brain():

    evaluate_story_state()

    focus = dm_state[
        "current_focus"
    ]

    print(
        "\n=== DM BRAIN ==="
    )

    # =========================
    # RECOVERY
    # =========================

    if focus == "recovery":

        generate_narrative_encounter()

        random_npc_event()

        try:

            ai_narrate(

                "Generate a calm emotional "
                "moment after recent conflict."
            )

        except Exception:

            print(
                "\nThe world briefly calms."
            )

    # =========================
    # EXPLORATION
    # =========================

    elif focus == "exploration":

        roll = random.randint(
            1,
            100
        )

        if roll <= 50:

            try:

                ai_generate_quest()

            except Exception:

                print(
                    "\nRumors spread of danger."
                )

        else:

            random_region_event()

    # =========================
    # CRISIS
    # =========================

    elif focus == "crisis":

        generate_campaign_event()

        generate_encounter()

        try:

            ai_narrate(

                "Narrate a major campaign "
                "crisis escalation."
            )

        except Exception:

            print(
                "\nThe campaign spirals into chaos."
            )

# =========================
# EVENT REACTIONS
# =========================

def on_enemy_killed(

    event_data

):

    change_story_pressure(
        5
    )

def on_world_collapse(

    event_data

):

    change_story_pressure(
        25
    )

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "enemy_killed",
    on_enemy_killed
)

subscribe(
    "world_collapse",
    on_world_collapse
)