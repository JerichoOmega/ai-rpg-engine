import random

from event_bus import (
    emit
)

from combat import (
    combat
)

from inventory import (
    add_item
)

from location_manager import (
    LOCATIONS
)

# =========================
# DUNGEON DATABASE
# =========================

DUNGEONS = {

    "cult_hideout": {

        "display_name": "Cult Hideout",

        "difficulty": 35,

        "boss": "cult_leader",

        "floors": 3,

        "discovered": False,

        "cleared": False,

        "theme": "cult",

        "loot_table": [

            "gold",

            "dark_amulet",

            "cult_blade"
        ]
    },

    "fallen_tower": {

        "display_name": "Fallen Tower",

        "difficulty": 60,

        "boss": "arcane_construct",

        "floors": 5,

        "discovered": False,

        "cleared": False,

        "theme": "arcane",

        "loot_table": [

            "mana_crystal",

            "ancient_spellbook",

            "enchanted_staff"
        ]
    },

    "forgotten_forge": {

        "display_name": "Forgotten Forge",

        "difficulty": 80,

        "boss": "ashen_guardian",

        "floors": 7,

        "discovered": False,

        "cleared": False,

        "theme": "fire",

        "loot_table": [

            "obsidian_blade",

            "molten_core",

            "legendary_armor"
        ]
    }
}

# =========================
# GET DUNGEON DATA
# =========================

def get_dungeon_data(

    dungeon_name

):

    return DUNGEONS.get(
        dungeon_name
    )

# =========================
# SHOW DUNGEON
# =========================

def show_dungeon(

    dungeon_name

):

    dungeon = DUNGEONS.get(
        dungeon_name
    )

    if not dungeon:

        print(
            "\nUnknown dungeon."
        )

        return

    print(
        "\n=== DUNGEON INFO ==="
    )

    print(
        "Dungeon:",
        dungeon[
            "display_name"
        ]
    )

    print(
        "Difficulty:",
        dungeon[
            "difficulty"
        ]
    )

    print(
        "Floors:",
        dungeon[
            "floors"
        ]
    )

    print(
        "Theme:",
        dungeon[
            "theme"
        ]
    )

    print(
        "Boss:",
        dungeon[
            "boss"
        ]
    )

    print(
        "Cleared:",
        dungeon[
            "cleared"
        ]
    )

# =========================
# DISCOVER DUNGEON
# =========================

def discover_dungeon(

    dungeon_name

):

    dungeon = DUNGEONS.get(
        dungeon_name
    )

    if not dungeon:

        return

    if dungeon[
        "discovered"
    ]:

        return

    dungeon[
        "discovered"
    ] = True

    print(
        f"\nDungeon discovered:"
        f" {dungeon_name}"
    )

    emit(

        "dungeon_discovered",

        dungeon_name=dungeon_name
    )

# =========================
# ENTER DUNGEON
# =========================

def enter_dungeon(

    dungeon_name

):

    dungeon = DUNGEONS.get(
        dungeon_name
    )

    if not dungeon:

        print(
            "\nUnknown dungeon."
        )

        return

    print(
        f"\nEntering"
        f" {dungeon_name}..."
    )

    floors = dungeon[
        "floors"
    ]

    # =========================
    # FLOOR LOOP
    # =========================

    for floor in range(
        1,
        floors + 1
    ):

        print(
            f"\n=== FLOOR {floor} ==="
        )

        process_dungeon_floor(

            dungeon_name,

            floor
        )

    # =========================
    # BOSS FIGHT
    # =========================

    boss_name = dungeon[
        "boss"
    ]

    print(
        f"\nBoss Encounter:"
        f" {boss_name}"
    )

    victory = combat(

        boss_name,

        dungeon[
            "difficulty"
        ]
    )

    if victory:

        clear_dungeon(
            dungeon_name
        )

# =========================
# PROCESS FLOOR
# =========================

def process_dungeon_floor(

    dungeon_name,
    floor

):

    roll = random.randint(
        1,
        100
    )

    # =========================
    # COMBAT
    # =========================

    if roll <= 50:

        enemy = random.choice([

            "cultist",

            "undead",

            "shadow_beast",

            "rogue_mage"
        ])

        print(
            f"\nEnemy Encounter:"
            f" {enemy}"
        )

        combat(
            enemy,
            25 + floor * 5
        )

    # =========================
    # LOOT
    # =========================

    elif roll <= 75:

        generate_dungeon_loot(
            dungeon_name
        )

    # =========================
    # EVENT
    # =========================

    else:

        trigger_dungeon_event(
            dungeon_name
        )

# =========================
# GENERATE LOOT
# =========================

def generate_dungeon_loot(

    dungeon_name

):

    dungeon = DUNGEONS.get(
        dungeon_name
    )

    if not dungeon:

        return

    loot = random.choice(
        dungeon[
            "loot_table"
        ]
    )

    print(
        f"\nLoot Found:"
        f" {loot}"
    )

    add_item(
        loot
    )

    emit(

        "loot_found",

        loot_name=loot
    )

# =========================
# DUNGEON EVENTS
# =========================

def trigger_dungeon_event(

    dungeon_name

):

    events = [

        "hidden_room",

        "collapsed_corridor",

        "ancient_altar",

        "dark_whispers",

        "magical_trap",

        "strange_vision"
    ]

    event_name = random.choice(
        events
    )

    print(
        f"\nDungeon Event:"
        f" {event_name}"
    )

    emit(

        "dungeon_event",

        dungeon_name=dungeon_name,

        event_name=event_name
    )

# =========================
# CLEAR DUNGEON
# =========================

def clear_dungeon(

    dungeon_name

):

    dungeon = DUNGEONS.get(
        dungeon_name
    )

    if not dungeon:

        return

    dungeon[
        "cleared"
    ] = True

    print(
        f"\nDungeon Cleared:"
        f" {dungeon_name}"
    )

    emit(

        "dungeon_cleared",

        dungeon_name=dungeon_name
    )

# =========================
# RANDOM DUNGEON DISCOVERY
# =========================

def random_dungeon_discovery():

    undiscovered = [

        name

        for name, dungeon

        in DUNGEONS.items()

        if not dungeon[
            "discovered"
        ]
    ]

    if not undiscovered:

        return

    dungeon_name = random.choice(
        undiscovered
    )

    discover_dungeon(
        dungeon_name
    )

# =========================
# DUNGEON EVOLUTION
# =========================

def evolve_dungeons():

    for dungeon_name, dungeon in DUNGEONS.items():

        if dungeon[
            "cleared"
        ]:

            continue

        # =========================
        # DUNGEON GROWS STRONGER
        # =========================

        dungeon[
            "difficulty"
        ] += 1

        dungeon[
            "difficulty"
        ] = min(

            dungeon[
                "difficulty"
            ],

            100
        )

# =========================
# SHOW ALL DUNGEONS
# =========================

def show_all_dungeons():

    print(
        "\n=== DUNGEONS ==="
    )

    for dungeon_name, dungeon in DUNGEONS.items():

        if not dungeon[
            "discovered"
        ]:

            continue

        print(
            f"\n{dungeon['display_name']}"
        )

        print(
            f"Difficulty:"
            f" {dungeon['difficulty']}"
        )

        print(
            f"Cleared:"
            f" {dungeon['cleared']}"
        )

# =========================
# LEGENDARY DUNGEON EVENT
# =========================

def trigger_legendary_dungeon():

    print(
        "\n=== LEGENDARY DUNGEON EMERGES ==="
    )

    legendary_name = (
        "abyssal_cathedral"
    )

    DUNGEONS[
        legendary_name
    ] = {

        "display_name":
            "Abyssal Cathedral",

        "difficulty": 100,

        "boss":
            "void_lord",

        "floors": 10,

        "discovered": False,

        "cleared": False,

        "theme": "apocalypse",

        "loot_table": [

            "void_blade",

            "crown_of_ashes",

            "godkiller_relic"
        ]
    }

    emit(
        "legendary_dungeon_spawned"
    )