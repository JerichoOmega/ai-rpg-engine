import random

from progression_manager import (
    reward_quest_completion,
    get_world_tier
)

from encounter_manager import (
    generate_encounter
)

from dungeon_manager import (
    DUNGEONS
)

from settlement_manager import (
    SETTLEMENTS
)

from region_manager import (
    REGIONS
)

from event_bus import (
    emit
)

# =========================
# ACTIVE QUESTS
# =========================

active_quests = []

completed_quests = []

# =========================
# QUEST TEMPLATES
# =========================

QUEST_TEMPLATES = {

    "bounty": {

        "objectives": [

            "defeat_enemy",

            "clear_encounter"
        ],

        "reward_gold": 100,

        "reward_xp": 75
    },

    "dungeon": {

        "objectives": [

            "clear_dungeon",

            "defeat_boss"
        ],

        "reward_gold": 250,

        "reward_xp": 200
    },

    "escort": {

        "objectives": [

            "travel_region",

            "protect_target"
        ],

        "reward_gold": 125,

        "reward_xp": 100
    },

    "investigation": {

        "objectives": [

            "discover_location",

            "solve_event"
        ],

        "reward_gold": 150,

        "reward_xp": 125
    },

    "faction": {

        "objectives": [

            "help_faction",

            "eliminate_rival"
        ],

        "reward_gold": 300,

        "reward_xp": 250
    }
}

# =========================
# GENERATE QUEST
# =========================

def generate_quest(

    region_name=None,

    quest_type=None

):

    if not quest_type:

        quest_type = random.choice(

            list(
                QUEST_TEMPLATES.keys()
            )
        )

    template = QUEST_TEMPLATES.get(
        quest_type
    )

    if not template:

        return None

    world_tier = get_world_tier()

    quest = {

        "id": random.randint(
            1000,
            9999
        ),

        "type": quest_type,

        "title": generate_quest_title(
            quest_type
        ),

        "region": region_name,

        "difficulty": (
            world_tier * 10
        ),

        "objectives": template[
            "objectives"
        ],

        "reward_gold": (

            template[
                "reward_gold"
            ] * world_tier
        ),

        "reward_xp": (

            template[
                "reward_xp"
            ] * world_tier
        ),

        "completed": False,

        "failed": False
    }

    active_quests.append(
        quest
    )

    print(
        f"\nNew Quest:"
        f" {quest['title']}"
    )

    emit(

        "quest_generated",

        quest=quest
    )

    return quest

# =========================
# QUEST TITLES
# =========================

def generate_quest_title(

    quest_type

):

    titles = {

        "bounty": [

            "Hunt the Cultists",

            "Eliminate the Beast",

            "Clear the Road"
        ],

        "dungeon": [

            "Into the Darkness",

            "The Forgotten Depths",

            "Secrets Beneath"
        ],

        "escort": [

            "Protect the Caravan",

            "Escort the Merchant",

            "Safe Passage"
        ],

        "investigation": [

            "Strange Disappearances",

            "The Corruption Spreads",

            "Mysteries of the Marsh"
        ],

        "faction": [

            "Serve the Kingdom",

            "Destroy the Rival Clan",

            "Secure Territory"
        ]
    }

    return random.choice(
        titles[
            quest_type
        ]
    )

# =========================
# COMPLETE QUEST
# =========================

def complete_quest(

    quest_id

):

    for quest in active_quests:

        if quest["id"] != quest_id:

            continue

        quest[
            "completed"
        ] = True

        reward_quest_completion()

        completed_quests.append(
            quest
        )

        active_quests.remove(
            quest
        )

        print(
            f"\nQuest Complete:"
            f" {quest['title']}"
        )

        print(
            f"Reward:"
            f" {quest['reward_gold']} gold"
        )

        emit(

            "quest_completed",

            quest=quest
        )

        return

# =========================
# FAIL QUEST
# =========================

def fail_quest(

    quest_id

):

    for quest in active_quests:

        if quest["id"] != quest_id:

            continue

        quest[
            "failed"
        ] = True

        active_quests.remove(
            quest
        )

        print(
            f"\nQuest Failed:"
            f" {quest['title']}"
        )

        emit(

            "quest_failed",

            quest=quest
        )

        return

# =========================
# QUEST BOARD
# =========================

def generate_quest_board(

    settlement_name

):

    print(
        "\n=== QUEST BOARD ==="
    )

    quests = []

    quest_count = random.randint(
        2,
        5
    )

    for _ in range(quest_count):

        quest = generate_quest()

        if quest:

            quests.append(
                quest
            )

    return quests

# =========================
# FACTION QUEST
# =========================

def generate_faction_quest(

    faction_name

):

    quest = generate_quest(
        quest_type="faction"
    )

    if not quest:

        return None

    quest[
        "faction"
    ] = faction_name

    print(
        f"\nFaction Quest:"
        f" {faction_name}"
    )

    return quest

# =========================
# DUNGEON QUEST
# =========================

def generate_dungeon_quest():

    dungeon_name = random.choice(
        list(
            DUNGEONS.keys()
        )
    )

    quest = generate_quest(
        quest_type="dungeon"
    )

    if not quest:

        return None

    quest[
        "target_dungeon"
    ] = dungeon_name

    print(
        f"\nDungeon Target:"
        f" {dungeon_name}"
    )

    return quest

# =========================
# WORLD EVENT QUEST
# =========================

def generate_world_event_quest():

    event_titles = [

        "The Dead Rise",

        "Void Corruption",

        "The Burning Skies",

        "The Black Plague"
    ]

    quest = {

        "id": random.randint(
            1000,
            9999
        ),

        "type": "world_event",

        "title": random.choice(
            event_titles
        ),

        "difficulty": 100,

        "reward_gold": 1000,

        "reward_xp": 750,

        "completed": False,

        "failed": False
    }

    active_quests.append(
        quest
    )

    print(
        f"\nWORLD EVENT:"
        f" {quest['title']}"
    )

    return quest

# =========================
# QUEST ENCOUNTER
# =========================

def generate_quest_encounter(

    region_name

):

    print(
        "\n=== QUEST ENCOUNTER ==="
    )

    enemies = generate_encounter(
        region_name
    )

    return enemies

# =========================
# SHOW ACTIVE QUESTS
# =========================

def show_active_quests():

    print(
        "\n=== ACTIVE QUESTS ==="
    )

    if not active_quests:

        print(
            "\nNo active quests."
        )

        return

    for quest in active_quests:

        print(
            f"\n[{quest['id']}]"
            f" {quest['title']}"
        )

        print(
            f"Type:"
            f" {quest['type']}"
        )

        print(
            f"Difficulty:"
            f" {quest['difficulty']}"
        )

        print(
            f"Reward XP:"
            f" {quest['reward_xp']}"
        )

# =========================
# SHOW COMPLETED QUESTS
# =========================

def show_completed_quests():

    print(
        "\n=== COMPLETED QUESTS ==="
    )

    if not completed_quests:

        print(
            "\nNo completed quests."
        )

        return

    for quest in completed_quests:

        print(
            f"\n{quest['title']}"
        )

# =========================
# QUEST DIFFICULTY
# =========================

def calculate_quest_difficulty(

    quest

):

    difficulty = quest[
        "difficulty"
    ]

    if quest["type"] == "dungeon":

        difficulty += 25

    elif quest["type"] == "world_event":

        difficulty += 50

    return difficulty

# =========================
# BRANCHING OUTCOME
# =========================

def resolve_quest_choice(

    quest,

    choice

):

    print(
        f"\nChoice Made:"
        f" {choice}"
    )

    if choice == "mercy":

        print(
            "\nYour compassion spreads hope."
        )

    elif choice == "execute":

        print(
            "\nFear spreads across the region."
        )

    elif choice == "corrupt":

        print(
            "\nDarkness grows stronger."
        )

# =========================
# QUEST SUMMARY
# =========================

def show_quest_summary():

    print(
        "\n=== QUEST SUMMARY ==="
    )

    print(
        f"Active Quests:"
        f" {len(active_quests)}"
    )

    print(
        f"Completed Quests:"
        f" {len(completed_quests)}"
    )