import random

from world_state import (
    world_state
)

from npc_manager import (
    NPCS
)

from region_manager import (
    REGIONS
)

from campaign_manager import (
    campaign_state
)

from event_bus import (
    emit
)

# =========================
# QUEST COMPONENTS
# =========================

OBJECTIVES = [

    "eliminate",

    "escort",

    "investigate",

    "recover",

    "defend",

    "survive"
]

TARGETS = [

    "cultists",

    "bandits",

    "shadow beasts",

    "undead",

    "rogue mages",

    "corrupted knights"
]

REWARDS = [

    "gold",

    "artifact",

    "faction reputation",

    "rare weapon",

    "ancient knowledge"
]

# =========================
# GENERATED QUESTS
# =========================

generated_quests = []

# =========================
# GENERATE QUEST
# =========================

def generate_quest():

    current_region = world_state[
        "regions"
    ]["current_region"]

    region = REGIONS.get(
        current_region
    )

    objective = random.choice(
        OBJECTIVES
    )

    target = random.choice(
        TARGETS
    )

    reward = random.choice(
        REWARDS
    )

    npc_name = random.choice(
        list(NPCS.keys())
    )

    campaign_stage = campaign_state[
        "campaign_stage"
    ]

    quest_name = (

        objective.title()

        + " "

        + target.title()
    )

    quest = {

        "name": quest_name,

        "objective": objective,

        "target": target,

        "reward": reward,

        "region": current_region,

        "giver": npc_name,

        "campaign_stage": campaign_stage,

        "completed": False
    }

    generated_quests.append(
        quest
    )

    print(
        "\n=== GENERATED QUEST ==="
    )

    print(
        "Quest:",
        quest_name
    )

    print(
        "Region:",
        current_region
    )

    print(
        "Quest Giver:",
        npc_name
    )

    print(
        "Reward:",
        reward
    )

    narrate_generated_quest(
        quest
    )

    emit(

        "quest_generated",

        quest_name=quest_name
    )

    return quest

# =========================
# QUEST NARRATION
# =========================

def narrate_generated_quest(

    quest

):

    print(
        "\n=== QUEST HOOK ==="
    )

    objective = quest[
        "objective"
    ]

    target = quest[
        "target"
    ]

    region = quest[
        "region"
    ]

    giver = quest[
        "giver"
    ]

    print(
        f"\n{giver} requests your help"
        f" to {objective}"
        f" {target}"
        f" within {region}."
    )

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

            apply_reward(
                quest
            )

            emit(

                "generated_quest_completed",

                quest_name=quest_name
            )

# =========================
# APPLY REWARD
# =========================

def apply_reward(

    quest

):

    reward = quest[
        "reward"
    ]

    print(
        f"\nReward earned:"
        f" {reward}"
    )

    if reward == "gold":

        world_state[
            "player"
        ]["gold"] += 50

    elif reward == "faction reputation":

        world_state[
            "factions"
        ]["kingdom"] += 10

# =========================
# SHOW GENERATED QUESTS
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
            "Giver:",
            quest["giver"]
        )

        print(
            "Completed:",
            quest["completed"]
        )

# =========================
# CAMPAIGN-BASED QUESTS
# =========================

def generate_campaign_quest():

    stage = campaign_state[
        "campaign_stage"
    ]

    print(
        "\n=== CAMPAIGN QUEST ==="
    )

    if stage == "emergence":

        print(
            "\nRumors spread of hidden cult activity."
        )

    elif stage == "regional_conflict":

        print(
            "\nFactions seek mercenaries for war."
        )

    elif stage == "world_crisis":

        print(
            "\nEntire regions collapse into chaos."
        )

    elif stage == "final_catastrophe":

        print(
            "\nThe fate of the world hangs by a thread."
        )

# =========================
# DYNAMIC ESCALATION
# =========================

def evaluate_generated_quests():

    incomplete = 0

    for quest in generated_quests:

        if not quest["completed"]:

            incomplete += 1

    if incomplete >= 5:

        print(
            "\nToo many unresolved quests"
            " are destabilizing the world."
        )

        world_state[
            "world_conditions"
        ]["world_chaos"] += 5