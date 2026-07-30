import random

from encounter_manager import (
    generate_encounter,
    boss_encounter
)

from event_bus import (
    emit
)

# =========================
# DUNGEON DATABASE
# =========================

dungeon_database = {

    "dark_cave": {

        "name": "Dark Cave",

        "region": "dark_forest",

        "rooms": 5,

        "boss_chance": 20
    },

    "ancient_ruins": {

        "name": "Ancient Ruins",

        "region": "ancient_ruins",

        "rooms": 7,

        "boss_chance": 35
    },

    "dragon_lair": {

        "name": "Dragon Lair",

        "region": "dragon_mountains",

        "rooms": 10,

        "boss_chance": 75
    }
}

# =========================
# DUNGEON RUN
# =========================

def run_dungeon(dungeon_id):

    # Delayed import prevents circular import
    from combat import combat

    if dungeon_id not in dungeon_database:

        print(
            "\nDungeon not found."
        )

        return

    dungeon = dungeon_database[
        dungeon_id
    ]

    print(
        f"\nEntering {dungeon['name']}..."
    )

    emit(

        "dungeon_started",

        dungeon=dungeon[
            "name"
        ]
    )

    room_count = dungeon[
        "rooms"
    ]

    for room in range(
        room_count
    ):

        print(
            f"\nRoom {room + 1}/{room_count}"
        )

        enemies = generate_encounter(

            dungeon[
                "region"
            ]
        )

        combat(
            enemies
        )

    if random.randint(
        1,
        100
    ) <= dungeon[
        "boss_chance"
    ]:

        print(
            "\nBoss Room!"
        )

        enemies = boss_encounter(

            dungeon[
                "region"
            ]
        )

        combat(
            enemies
        )

    emit(

        "dungeon_completed",

        dungeon=dungeon[
            "name"
        ]
    )

    print(
        f"\n{dungeon['name']} completed!"
    )

# =========================
# LEGACY COMPATIBILITY
# =========================

DUNGEONS = dungeon_database