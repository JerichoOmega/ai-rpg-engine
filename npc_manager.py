import random

from world_state import (
    world_state,
    remember_major_event
)

from event_bus import (
    subscribe,
    emit
)

# =========================
# NPC DATABASE
# =========================

NPCS = {

    "Elandor": {

        "region": "kingdom_capital",

        "faction": "mages_guild",

        "relationship": 10,

        "alive": True,

        "knows_player": False,

        "memories": [],

        "role": "Archmage"
    },

    "Sera": {

        "region": "shadow_marsh",

        "faction": "rebels",

        "relationship": 0,

        "alive": True,

        "knows_player": False,

        "memories": [],

        "role": "Scout"
    },

    "Varkun": {

        "region": "ashen_wastes",

        "faction": "shadow_cult",

        "relationship": -20,

        "alive": True,

        "knows_player": True,

        "memories": [],

        "role": "Cult Leader"
    }
}

# =========================
# GET NPC
# =========================

def get_npc(

    npc_name

):

    return NPCS.get(
        npc_name
    )

# =========================
# SHOW NPC
# =========================

def show_npc(

    npc_name

):

    npc = get_npc(
        npc_name
    )

    if not npc:

        print(
            "\nNPC not found."
        )

        return

    print(
        "\n=== NPC INFO ==="
    )

    print(
        "Name:",
        npc_name
    )

    print(
        "Role:",
        npc["role"]
    )

    print(
        "Faction:",
        npc["faction"]
    )

    print(
        "Region:",
        npc["region"]
    )

    print(
        "Relationship:",
        npc["relationship"]
    )

    print(
        "Alive:",
        npc["alive"]
    )

# =========================
# CHANGE RELATIONSHIP
# =========================

def change_relationship(

    npc_name,
    amount

):

    npc = get_npc(
        npc_name
    )

    if not npc:

        return

    npc[
        "relationship"
    ] += amount

    print(
        f"\nRelationship with"
        f" {npc_name}"
        f" changed by"
        f" {amount}."
    )

    evaluate_relationship(
        npc_name
    )

# =========================
# EVALUATE RELATIONSHIP
# =========================

def evaluate_relationship(

    npc_name

):

    npc = get_npc(
        npc_name
    )

    relationship = npc[
        "relationship"
    ]

    if relationship >= 50:

        print(
            f"\n{npc_name}"
            " deeply trusts you."
        )

    elif relationship <= -50:

        print(
            f"\n{npc_name}"
            " now hates you."
        )

# =========================
# NPC MEMORY
# =========================

def add_memory(

    npc_name,
    memory

):

    npc = get_npc(
        npc_name
    )

    if not npc:

        return

    npc[
        "memories"
    ].append(memory)

    print(
        f"\n{npc_name}"
        f" remembers:"
        f" {memory}"
    )

# =========================
# SHOW MEMORIES
# =========================

def show_memories(

    npc_name

):

    npc = get_npc(
        npc_name
    )

    if not npc:

        return

    print(
        f"\n=== {npc_name} MEMORIES ==="
    )

    memories = npc[
        "memories"
    ]

    if len(memories) == 0:

        print(
            "No memories."
        )

        return

    for memory in memories:

        print(
            "•",
            memory
        )

# =========================
# MOVE NPC
# =========================

def move_npc(

    npc_name,
    region_name

):

    npc = get_npc(
        npc_name
    )

    if not npc:

        return

    npc[
        "region"
    ] = region_name

    print(
        f"\n{npc_name}"
        f" traveled to"
        f" {region_name}."
    )

# =========================
# NPC DEATH
# =========================

def kill_npc(

    npc_name

):

    npc = get_npc(
        npc_name
    )

    if not npc:

        return

    npc[
        "alive"
    ] = False

    remember_major_event(
        f"{npc_name}_died"
    )

    print(
        f"\n{npc_name}"
        " has died."
    )

    emit(

        "npc_died",

        npc_name=npc_name
    )

# =========================
# RUMOR SYSTEM
# =========================

def spread_rumor(

    rumor

):

    print(
        "\nRumor spreads:"
    )

    print(
        rumor
    )

    for npc_name in NPCS:

        NPCS[
            npc_name
        ]["memories"].append(
            rumor
        )

# =========================
# RANDOM NPC EVENT
# =========================

def random_npc_event():

    npc_name = random.choice(
        list(NPCS.keys())
    )

    npc = NPCS[npc_name]

    if not npc["alive"]:

        return

    print(
        f"\nNPC Event:"
        f" {npc_name}"
    )

    possible_regions = [

        "kingdom_capital",

        "shadow_marsh",

        "arcane_ruins",

        "ashen_wastes"
    ]

    new_region = random.choice(
        possible_regions
    )

    move_npc(
        npc_name,
        new_region
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

    if enemy_name == "ancient dragon":

        spread_rumor(
            "A dragon has been slain."
        )

        change_relationship(
            "Elandor",
            10
        )

def on_quest_completed(

    event_data

):

    quest_name = event_data.get(
        "quest_name"
    )

    spread_rumor(
        f"The quest"
        f" '{quest_name}'"
        f" was completed."
    )

def on_faction_enemy(

    event_data

):

    faction = event_data.get(
        "faction"
    )

    for npc_name in NPCS:

        npc = NPCS[npc_name]

        if npc["faction"] == faction:

            change_relationship(
                npc_name,
                -10
            )

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "enemy_killed",
    on_enemy_killed
)

subscribe(
    "quest_completed",
    on_quest_completed
)

subscribe(
    "faction_enemy",
    on_faction_enemy
)