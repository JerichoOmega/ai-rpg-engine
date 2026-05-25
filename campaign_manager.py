import random

from world_state import (
    world_state,
    activate_world_event,
    remember_major_event
)

from event_bus import (
    subscribe,
    emit
)

# =========================
# CAMPAIGN STATE
# =========================

campaign_state = {

    "current_act": 1,

    "main_threat": "shadow_cult",

    "campaign_stage": "emergence",

    "villains": {

        "Varkun": {

            "alive": True,

            "power": 50,

            "last_seen": "shadow_marsh"
        }
    }
}

# =========================
# SHOW CAMPAIGN STATUS
# =========================

def show_campaign_status():

    print(
        "\n=== CAMPAIGN STATUS ==="
    )

    print(
        "Current Act:",
        campaign_state[
            "current_act"
        ]
    )

    print(
        "Stage:",
        campaign_state[
            "campaign_stage"
        ]
    )

    print(
        "Main Threat:",
        campaign_state[
            "main_threat"
        ]
    )

# =========================
# ADVANCE CAMPAIGN
# =========================

def advance_campaign():

    campaign_state[
        "current_act"
    ] += 1

    act = campaign_state[
        "current_act"
    ]

    print(
        f"\nCampaign advances"
        f" to Act {act}."
    )

    # =========================
    # ACT PROGRESSION
    # =========================

    if act == 2:

        campaign_state[
            "campaign_stage"
        ] = "regional_conflict"

        activate_world_event(
            "Faction Unrest"
        )

    elif act == 3:

        campaign_state[
            "campaign_stage"
        ] = "world_crisis"

        activate_world_event(
            "World Crisis"
        )

    elif act >= 4:

        campaign_state[
            "campaign_stage"
        ] = "final_catastrophe"

        activate_world_event(
            "Final Catastrophe"
        )

    emit(

        "campaign_advanced",

        act=act
    )

# =========================
# WORLD ESCALATION
# =========================

def evaluate_campaign_progress():

    chaos = world_state[
        "world_conditions"
    ]["world_chaos"]

    if chaos >= 25:

        advance_campaign()

# =========================
# RANDOM CAMPAIGN EVENT
# =========================

def generate_campaign_event():

    events = [

        "Assassination Attempt",

        "Cult Ritual",

        "City Revolt",

        "Magical Disaster",

        "Ancient Awakening"
    ]

    event_name = random.choice(
        events
    )

    print(
        "\n=== CAMPAIGN EVENT ==="
    )

    print(event_name)

    activate_world_event(
        event_name
    )

# =========================
# VILLAIN ESCALATION
# =========================

def strengthen_villain(

    villain_name,
    amount

):

    villain = campaign_state[
        "villains"
    ].get(villain_name)

    if not villain:

        return

    villain[
        "power"
    ] += amount

    print(
        f"\n{villain_name}"
        f" grows stronger."
    )

# =========================
# RECURRING VILLAIN
# =========================

def villain_returns(

    villain_name

):

    villain = campaign_state[
        "villains"
    ].get(villain_name)

    if not villain:

        return

    if not villain["alive"]:

        return

    print(
        f"\n{villain_name}"
        " returns from the shadows."
    )

    emit(

        "villain_returned",

        villain_name=villain_name
    )

# =========================
# EVENT REACTIONS
# =========================

def on_quest_completed(

    event_data

):

    quest_name = event_data.get(
        "quest_name"
    )

    if quest_name == "Cult Hunt":

        strengthen_villain(
            "Varkun",
            10
        )

def on_region_crisis(

    event_data

):

    region_name = event_data.get(
        "region_name"
    )

    print(
        f"\nThe crisis in"
        f" {region_name}"
        " escalates the campaign."
    )

    world_state[
        "world_conditions"
    ]["world_chaos"] += 5

def on_world_collapse(

    event_data

):

    print(
        "\nThe campaign enters"
        " its darkest phase."
    )

    advance_campaign()

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "quest_completed",
    on_quest_completed
)

subscribe(
    "region_crisis",
    on_region_crisis
)

subscribe(
    "world_collapse",
    on_world_collapse
)