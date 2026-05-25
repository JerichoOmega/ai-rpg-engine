import random

from world_state import (
    world_state
)

from campaign_manager import (
    campaign_state
)

from event_bus import (
    emit
)

from llm_bridge import (
    ai_generate_quest
)

# =========================
# GENERATED QUESTS
# =========================

generated_quests = []

# =========================
# FALLBACK QUESTS
# =========================

FALLBACK_QUESTS = [

    "Eliminate Cultists",

    "Escort Caravan",

    "Investigate Ruins",

    "Recover Artifact",

    "Defend Village"
]

# =========================
# GENERATE QUEST
# =========================

def generate_quest():

    print(
        "\n=== QUEST GENERATION ==="
    )

    # =========================
    # AI QUEST
    # =========================

    try:

        ai_generate_quest()

    # =========================
    # FALLBACK
    # =========================

    except Exception:

        fallback = random.choice(
            FALLBACK_QUESTS
        )

        print(
            f"\nFallback Quest:"
            f" {fallback}"
        )

    quest_name = random.choice(
        FALLBACK_QUESTS
    )

    quest = {

        "name": quest_name,

        "completed": False,

        "region":

            world_state[
                "regions"
            ]["current_region"],

        "campaign_stage":

            campaign_state[
                "campaign_stage"
            ]
    }

    generated_quests.append(
        quest
    )

    emit(

        "quest_generated",

        quest_name=quest_name
    )

    return quest

# =========================
# COMPLETE QUEST
# =========================

def complete_generated_quest(

    quest_name

):

    for quest in generated_quests:

        if quest["name"] == quest_name:

            if quest["completed"]:

                return

            quest[
                "completed"
            ] = True

            print(
                f"\nQuest completed:"
                f" {quest_name}"
            )

            emit(

                "quest_completed",

                quest_name=quest_name
            )

# =========================
# SHOW QUESTS
# =========================

def show_generated_quests():

    print(
        "\n=== GENERATED QUESTS ==="
    )

    if len(generated_quests) == 0:

        print(
            "No generated quests."
        )

        return

    for quest in generated_quests:

        print(
            "\n•",
            quest["name"]
        )

        print(
            "Region:",
            quest["region"]
        )

        print(
            "Completed:",
            quest["completed"]
        )