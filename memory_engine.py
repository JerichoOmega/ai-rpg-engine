from world_state import (
    world_state
)

from event_bus import (
    subscribe
)

# =========================
# MEMORY STORAGE
# =========================

memory_database = {

    "major_events": [],

    "npc_memories": [],

    "faction_memories": [],

    "region_memories": [],

    "combat_memories": [],

    "player_choices": []
}

# =========================
# STORE MEMORY
# =========================

def store_memory(

    category,
    memory,
    importance="minor"

):

    if category not in memory_database:

        return

    memory_entry = {

        "memory": memory,

        "importance": importance
    }

    memory_database[
        category
    ].append(memory_entry)

    print(
        "\n[MEMORY STORED]"
    )

    print(memory)

# =========================
# RETRIEVE MEMORIES
# =========================

def retrieve_memories(

    category

):

    return memory_database.get(
        category,
        []
    )

# =========================
# SEARCH MEMORIES
# =========================

def search_memories(

    keyword

):

    results = []

    for category in memory_database:

        memories = memory_database[
            category
        ]

        for memory_entry in memories:

            memory_text = memory_entry[
                "memory"
            ]

            if (

                keyword.lower()

                in

                memory_text.lower()

            ):

                results.append(
                    memory_entry
                )

    return results

# =========================
# SHOW MEMORIES
# =========================

def show_memories():

    print(
        "\n=== MEMORY DATABASE ==="
    )

    for category in memory_database:

        print(
            f"\n{category.upper()}"
        )

        memories = memory_database[
            category
        ]

        if len(memories) == 0:

            print(
                "No memories."
            )

            continue

        for memory_entry in memories:

            print(
                "•",
                memory_entry[
                    "memory"
                ]
            )

# =========================
# MEMORY COMPRESSION
# =========================

def compress_memories():

    print(
        "\n=== MEMORY COMPRESSION ==="
    )

    combat_memories = memory_database[
        "combat_memories"
    ]

    if len(combat_memories) >= 10:

        summary = (

            "The player survived many"
            " dangerous battles."
        )

        memory_database[
            "combat_memories"
        ] = [

            {

                "memory": summary,

                "importance": "major"
            }
        ]

        print(
            "\nCombat memories compressed."
        )

# =========================
# CONTEXT GENERATION
# =========================

def build_story_context():

    context = {

        "region": world_state[
            "regions"
        ]["current_region"],

        "world_chaos": world_state[
            "world_conditions"
        ]["world_chaos"],

        "major_events": retrieve_memories(
            "major_events"
        ),

        "player_choices": retrieve_memories(
            "player_choices"
        )
    }

    return context

# =========================
# EVENT REACTIONS
# =========================

def on_enemy_killed(

    event_data

):

    enemy_name = event_data.get(
        "enemy_name"
    )

    memory = (

        f"Defeated"
        f" {enemy_name}"
    )

    store_memory(

        "combat_memories",

        memory,

        "minor"
    )

def on_quest_completed(

    event_data

):

    quest_name = event_data.get(
        "quest_name"
    )

    memory = (

        f"Completed quest:"
        f" {quest_name}"
    )

    store_memory(

        "major_events",

        memory,

        "major"
    )

def on_region_discovered(

    event_data

):

    region_name = event_data.get(
        "region_name"
    )

    memory = (

        f"Discovered region:"
        f" {region_name}"
    )

    store_memory(

        "region_memories",

        memory,

        "major"
    )

def on_player_choice(

    event_data

):

    choice = event_data.get(
        "choice"
    )

    memory = (

        f"Player chose:"
        f" {choice}"
    )

    store_memory(

        "player_choices",

        memory,

        "major"
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

    memory = (

        f"War began between"
        f" {faction_one}"
        f" and"
        f" {faction_two}"
    )

    store_memory(

        "faction_memories",

        memory,

        "legendary"
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
    "region_discovered",
    on_region_discovered
)

subscribe(
    "player_choice",
    on_player_choice
)

subscribe(
    "faction_war_started",
    on_faction_war_started
)