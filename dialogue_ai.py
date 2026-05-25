import random

from world_state import (
    world_state
)

from npc_manager import (
    NPCS
)

from memory_engine import (
    search_memories
)

from campaign_manager import (
    campaign_state
)

from llm_bridge import (
    ai_dialogue
)

# =========================
# FALLBACK DIALOGUE
# =========================

FRIENDLY_DIALOGUE = [

    "It's good to see you again.",

    "People still speak of your deeds.",

    "You have my trust.",

    "The realm needs heroes like you."
]

NEUTRAL_DIALOGUE = [

    "Times are uncertain.",

    "Travel carefully.",

    "Strange things are happening lately.",

    "Not everything is as it seems."
]

HOSTILE_DIALOGUE = [

    "You are not welcome here.",

    "Your actions have consequences.",

    "Leave before trouble begins.",

    "I know what you've done."
]

FEARFUL_DIALOGUE = [

    "The world is falling apart.",

    "Darkness spreads everywhere.",

    "People vanish every night.",

    "Something terrible is coming."
]

# =========================
# NPC ATTITUDE
# =========================

def get_npc_attitude(

    npc_name

):

    npc = NPCS.get(
        npc_name
    )

    if not npc:

        return "neutral"

    relationship = npc[
        "relationship"
    ]

    if relationship >= 50:

        return "friendly"

    elif relationship <= -50:

        return "hostile"

    return "neutral"

# =========================
# WORLD TONE
# =========================

def get_world_tone():

    chaos = world_state[
        "world_conditions"
    ]["world_chaos"]

    if chaos >= 50:

        return "fearful"

    return "normal"

# =========================
# FALLBACK DIALOGUE
# =========================

def fallback_dialogue(

    npc_name

):

    attitude = get_npc_attitude(
        npc_name
    )

    world_tone = get_world_tone()

    print(
        "\n=== FALLBACK DIALOGUE ==="
    )

    if world_tone == "fearful":

        line = random.choice(
            FEARFUL_DIALOGUE
        )

    elif attitude == "friendly":

        line = random.choice(
            FRIENDLY_DIALOGUE
        )

    elif attitude == "hostile":

        line = random.choice(
            HOSTILE_DIALOGUE
        )

    else:

        line = random.choice(
            NEUTRAL_DIALOGUE
        )

    print(
        f"\n{npc_name}:"
    )

    print(
        f'"{line}"'
    )

# =========================
# MEMORY CALLBACKS
# =========================

def generate_memory_callback(

    npc_name

):

    dragon_memories = search_memories(
        "dragon"
    )

    cult_memories = search_memories(
        "cult"
    )

    if len(dragon_memories) > 0:

        print(
            f'\n"{npc_name} remembers'
            ' tales of the dragon slayer."'
        )

    if len(cult_memories) > 0:

        print(
            f'\n"{npc_name} fears'
            ' rising cult influence."'
        )

# =========================
# CAMPAIGN TALK
# =========================

def generate_campaign_dialogue():

    stage = campaign_state[
        "campaign_stage"
    ]

    print(
        "\n=== CAMPAIGN TALK ==="
    )

    if stage == "emergence":

        print(
            '"Rumors spread from'
            ' the marshlands..."'
        )

    elif stage == "regional_conflict":

        print(
            '"The factions edge'
            ' closer to war."'
        )

    elif stage == "world_crisis":

        print(
            '"Entire cities now'
            ' fear collapse."'
        )

    elif stage == "final_catastrophe":

        print(
            '"This may be the end'
            ' of everything."'
        )

# =========================
# AI NPC CONVERSATION
# =========================

def npc_conversation(

    npc_name

):

    npc = NPCS.get(
        npc_name
    )

    if not npc:

        print(
            "\nUnknown NPC."
        )

        return

    if not npc["alive"]:

        print(
            f"\nOnly silence remains"
            f" where {npc_name}"
            " once stood."
        )

        return

    print(
        "\n=== NPC CONVERSATION ==="
    )

    # =========================
    # AI DIALOGUE
    # =========================

    try:

        ai_dialogue(

            npc_name,

            "The player approaches "
            "for conversation."
        )

    # =========================
    # FALLBACK
    # =========================

    except Exception:

        fallback_dialogue(
            npc_name
        )

    generate_memory_callback(
        npc_name
    )

    generate_campaign_dialogue()

    dialogue_choice(
        npc_name
    )

# =========================
# DIALOGUE CHOICES
# =========================

def dialogue_choice(

    npc_name

):

    print(
        "\n=== DIALOGUE CHOICE ==="
    )

    print(
        "1. Be Kind"
    )

    print(
        "2. Threaten"
    )

    print(
        "3. Ask Questions"
    )

    choice = input(
        "\nChoose: "
    ).strip()

    npc = NPCS.get(
        npc_name
    )

    if not npc:

        return

    # =========================
    # KIND
    # =========================

    if choice == "1":

        print(
            "\nYou respond kindly."
        )

        npc[
            "relationship"
        ] += 5

        print(
            f"\n{npc_name}"
            " appreciates your kindness."
        )

    # =========================
    # THREATEN
    # =========================

    elif choice == "2":

        print(
            "\nYou threaten them."
        )

        npc[
            "relationship"
        ] -= 10

        print(
            f"\n{npc_name}"
            " distrusts you more."
        )

    # =========================
    # QUESTIONS
    # =========================

    else:

        print(
            "\nYou ask careful questions."
        )

# =========================
# RANDOM CONVERSATION
# =========================

def random_conversation():

    npc_name = random.choice(
        list(NPCS.keys())
    )

    npc_conversation(
        npc_name
    )