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

from event_bus import (
    subscribe
)

# =========================
# NARRATIVE TONE
# =========================

def get_world_tone():

    chaos = world_state[
        "world_conditions"
    ]["world_chaos"]

    if chaos >= 75:

        return "apocalyptic"

    elif chaos >= 50:

        return "grim"

    elif chaos >= 25:

        return "unstable"

    return "normal"

# =========================
# REGION NARRATION
# =========================

def narrate_region(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    tone = get_world_tone()

    print(
        "\n=== NARRATION ==="
    )

    if tone == "apocalyptic":

        print(
            f"\n{region_name}"
            " burns beneath a collapsing sky."
        )

    elif tone == "grim":

        print(
            f"\nFear grips"
            f" {region_name}."
        )

    elif tone == "unstable":

        print(
            f"\nTension spreads through"
            f" {region_name}."
        )

    else:

        print(
            f"\nThe people of"
            f" {region_name}"
            " continue their daily lives."
        )

    if region["corrupted"]:

        print(
            "\nDark corruption stains the land."
        )

# =========================
# NPC NARRATION
# =========================

def narrate_npc(

    npc_name

):

    npc = NPCS.get(
        npc_name
    )

    if not npc:

        return

    if not npc["alive"]:

        print(
            f"\nStories still linger"
            f" about the late"
            f" {npc_name}."
        )

        return

    relationship = npc[
        "relationship"
    ]

    print(
        "\n=== NPC NARRATION ==="
    )

    if relationship >= 50:

        print(
            f"\n{npc_name}"
            " greets you warmly."
        )

    elif relationship <= -50:

        print(
            f"\n{npc_name}"
            " watches you with hatred."
        )

    else:

        print(
            f"\n{npc_name}"
            " studies you carefully."
        )

# =========================
# DYNAMIC STORY HOOKS
# =========================

def generate_story_hook():

    chaos = world_state[
        "world_conditions"
    ]["world_chaos"]

    active_events = world_state[
        "events"
    ]

    hooks = []

    if chaos >= 25:

        hooks.append(
            "Refugees flee from distant conflicts."
        )

    if "Cult Retaliation" in active_events:

        hooks.append(
            "Cult symbols appear across nearby villages."
        )

    if world_state[
        "story_memory"
    ].get("dragon_slain"):

        hooks.append(
            "Bards sing of the dragon slayer."
        )

    if len(hooks) == 0:

        hooks.append(
            "Rumors whisper of forgotten ruins."
        )

    hook = random.choice(
        hooks
    )

    print(
        "\n=== STORY HOOK ==="
    )

    print(hook)

# =========================
# BATTLE NARRATION
# =========================

def narrate_battle(

    enemy_name

):

    tone = get_world_tone()

    print(
        "\n=== BATTLE NARRATION ==="
    )

    if tone == "grim":

        print(
            f"\nThe battle against"
            f" {enemy_name}"
            " feels hopeless."
        )

    elif tone == "apocalyptic":

        print(
            f"\nThe clash with"
            f" {enemy_name}"
            " unfolds beneath a dying world."
        )

    else:

        print(
            f"\nYou prepare to face"
            f" {enemy_name}."
        )

# =========================
# QUEST NARRATION
# =========================

def narrate_quest(

    quest_name

):

    print(
        "\n=== QUEST NARRATION ==="
    )

    if quest_name == "Cult Hunt":

        print(
            "\nVillagers whisper of disappearances"
            " tied to dark rituals."
        )

    elif quest_name == "Dragon Slayer":

        print(
            "\nAncient prophecies speak"
            " of a dragon's fall."
        )

    else:

        print(
            f"\nA new journey begins:"
            f" {quest_name}"
        )

# =========================
# EVENT REACTIONS
# =========================

def on_enemy_killed(

    event_data

):

    enemy_name = event_data.get(
        "enemy_name"
    )

    print(
        "\n=== DYNAMIC NARRATION ==="
    )

    if enemy_name == "hidden cult":

        print(
            "\nThe cult's influence weakens."
        )

    elif enemy_name == "ancient dragon":

        print(
            "\nThe age of dragons begins to fade."
        )

def on_region_crisis(

    event_data

):

    region_name = event_data.get(
        "region_name"
    )

    print(
        "\n=== WORLD NARRATION ==="
    )

    print(
        f"\nPanic spreads through"
        f" {region_name}."
    )

def on_faction_war_started(

    event_data

):

    faction_one = event_data.get(
        "faction_one"
    )

    faction_two = event_data.get(
        "faction_two"
    )

    print(
        "\n=== WAR NARRATION ==="
    )

    print(
        f"\nWar erupts between"
        f" {faction_one}"
        f" and"
        f" {faction_two}."
    )

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "enemy_killed",
    on_enemy_killed
)

subscribe(
    "region_crisis",
    on_region_crisis
)

subscribe(
    "faction_war_started",
    on_faction_war_started
)