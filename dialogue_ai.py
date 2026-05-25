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

# =========================
# DIALOGUE TONES
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
# GET NPC ATTITUDE
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
# GET WORLD TONE
# =========================

def get_world_tone():

    chaos = world_state[
        "world_conditions"
    ]["world_chaos"]

    if chaos >= 50:

        return "fearful"

    return "normal"

# =========================
# GENERATE DIALOGUE
# =========================

def generate_dialogue(

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

    attitude = get_npc_attitude(
        npc_name
    )

    world_tone = get_world_tone()

    print(
        "\n=== DIALOGUE ==="
    )

    # =========================
    # FEARFUL WORLD OVERRIDE
    # =========================

    if world_tone == "fearful":

        line = random.choice(
            FEARFUL_DIALOGUE
        )

        print(
            f"\n{npc_name}:"
        )

        print(
            f'"{line}"'
        )

    # =========================
    # FRIENDLY
    # =========================

    elif attitude == "friendly":

        line = random.choice(
            FRIENDLY_DIALOGUE
        )

        print(
            f"\n{npc_name}:"
        )

        print(
            f'"{line}"'
        )

    # =========================
    # HOSTILE
    # =========================

    elif attitude == "hostile":

        line = random.choice(
            HOSTILE_DIALOGUE
        )

        print(
            f"\n{npc_name}:"
        )

        print(
            f'"{line}"'
        )

    # =========================
    # NEUTRAL
    # =========================

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

    generate_memory_callback(
        npc_name
    )

    generate_campaign_dialogue()

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
            f'\n"{npc_name} whispers about'
            ' the dragon slayer..."'
        )

    if len(cult_memories) > 0:

        print(
            f'\n"{npc_name} seems worried'
            ' about cult activity."'
        )

# =========================
# CAMPAIGN DIALOGUE
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
# DIALOGUE CHOICES
# =========================

def dialogue_choice():

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

    if choice == "1":

        print(
            "\nYou respond kindly."
        )

        return "kind"

    elif choice == "2":

        print(
            "\nYou threaten them."
        )

        return "threaten"

    else:

        print(
            "\nYou ask carefully."
        )

        return "question"

# =========================
# NPC CONVERSATION
# =========================

def npc_conversation(

    npc_name

):

    generate_dialogue(
        npc_name
    )

    result = dialogue_choice()

    npc = NPCS.get(
        npc_name
    )

    if not npc:

        return

    # =========================
    # RELATIONSHIP EFFECTS
    # =========================

    if result == "kind":

        npc[
            "relationship"
        ] += 5

        print(
            f"\n{npc_name}"
            " appreciates your kindness."
        )

    elif result == "threaten":

        npc[
            "relationship"
        ] -= 10

        print(
            f"\n{npc_name}"
            " distrusts you more."
        )

# =========================
# RANDOM NPC CONVERSATION
# =========================

def random_conversation():

    npc_name = random.choice(
        list(NPCS.keys())
    )

    npc_conversation(
        npc_name
    )