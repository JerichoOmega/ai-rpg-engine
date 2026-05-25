from world_state import (
    world_state,
    add_gold,
    complete_quest,
    fail_quest,
    remember_major_event,
    change_faction_reputation
)

from event_bus import (
    subscribe,
    emit
)

# =========================
# QUEST DATABASE
# =========================

quest_database = {

    "Cult Hunt": {

        "description":
            "Defeat members of the Shadow Cult.",

        "target_enemy":
            "hidden cult",

        "required_kills": 3,

        "gold_reward": 50,

        "xp_reward": 75,

        "faction": "kingdom",

        "reputation_reward": 10
    },

    "Dragon Slayer": {

        "description":
            "Slay the ancient dragon.",

        "target_enemy":
            "ancient dragon",

        "required_kills": 1,

        "gold_reward": 150,

        "xp_reward": 200,

        "faction": "kingdom",

        "reputation_reward": 25
    },

    "Necromancer Purge": {

        "description":
            "Destroy dangerous necromancers.",

        "target_enemy":
            "necromancer",

        "required_kills": 2,

        "gold_reward": 80,

        "xp_reward": 100,

        "faction": "mages_guild",

        "reputation_reward": 15
    }
}

# =========================
# QUEST STATE
# =========================

quests = {

    "Cult Hunt": {

        "progress": 0,

        "completed": False
    },

    "Dragon Slayer": {

        "progress": 0,

        "completed": False
    },

    "Necromancer Purge": {

        "progress": 0,

        "completed": False
    }
}

# =========================
# INITIALIZE QUESTS
# =========================

def initialize_quests():

    for quest_name in quest_database:

        if (

            quest_name

            not in

            world_state[
                "quests"
            ]["active"]

        ):

            world_state[
                "quests"
            ]["active"].append(
                quest_name
            )

# =========================
# SHOW QUESTS
# =========================

def show_quests():

    print(
        "\n=== QUEST JOURNAL ==="
    )

    active_quests = world_state[
        "quests"
    ]["active"]

    if len(active_quests) == 0:

        print(
            "No active quests."
        )

        return

    for quest_name in active_quests:

        quest_data = quest_database[
            quest_name
        ]

        quest_state = quests[
            quest_name
        ]

        print(
            "\n•",
            quest_name
        )

        print(
            quest_data[
                "description"
            ]
        )

        print(

            "Progress:",

            str(
                quest_state[
                    "progress"
                ]
            )

            + "/"

            + str(

                quest_data[
                    "required_kills"
                ]
            )
        )

# =========================
# UPDATE QUESTS
# =========================

def update_quests_from_enemy(

    enemy_name

):

    active_quests = world_state[
        "quests"
    ]["active"]

    for quest_name in active_quests:

        quest_data = quest_database[
            quest_name
        ]

        quest_state = quests[
            quest_name
        ]

        if (

            enemy_name

            ==

            quest_data[
                "target_enemy"
            ]

        ):

            quest_state[
                "progress"
            ] += 1

            print(
                f"\nQuest Updated:"
                f" {quest_name}"
            )

            print(

                "Progress:",

                str(
                    quest_state[
                        "progress"
                    ]
                )

                + "/"

                + str(

                    quest_data[
                        "required_kills"
                    ]
                )
            )

            if (

                quest_state[
                    "progress"
                ]

                >=

                quest_data[
                    "required_kills"
                ]

            ):

                reward_quest(
                    quest_name
                )

# =========================
# QUEST REWARDS
# =========================

def reward_quest(quest_name):

    quest_data = quest_database[
        quest_name
    ]

    quest_state = quests[
        quest_name
    ]

    if quest_state["completed"]:

        return

    quest_state[
        "completed"
    ] = True

    if (

        quest_name

        in

        world_state[
            "quests"
        ]["active"]

    ):

        world_state[
            "quests"
        ]["active"].remove(
            quest_name
        )

    complete_quest(
        quest_name
    )

    add_gold(

        quest_data[
            "gold_reward"
        ]
    )

    world_state[
        "player"
    ]["xp"] += (

        quest_data[
            "xp_reward"
        ]
    )

    change_faction_reputation(

        quest_data[
            "faction"
        ],

        quest_data[
            "reputation_reward"
        ]
    )

    remember_major_event(
        quest_name
    )

    print(
        "\n=== QUEST COMPLETE ==="
    )

    print(
        quest_name
    )

    print(
        "Gold Reward:",
        quest_data[
            "gold_reward"
        ]
    )

    print(
        "XP Reward:",
        quest_data[
            "xp_reward"
        ]
    )

    emit(

        "quest_completed",

        quest_name=quest_name
    )

# =========================
# EVENT REACTIONS
# =========================

def handle_enemy_killed(

    event_data

):

    enemy_name = event_data.get(
        "enemy_name"
    )

    if enemy_name:

        update_quests_from_enemy(
            enemy_name
        )

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "enemy_killed",
    handle_enemy_killed
)