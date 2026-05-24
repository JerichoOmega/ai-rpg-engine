# =========================
# QUEST SYSTEM
# =========================

from memory import update_memory

from factions import modify_reputation

# =========================
# QUEST DATABASE
# =========================

quests = {

    "shadow_cult_rising": {

        "name": "Shadow Cult Rising",

        "description":
            "Investigate growing cult activity "
            "across the kingdom.",

        "completed": False,

        "reward_claimed": False,

        "progress": 0,

        "goal": 3,

        "reward_gold": 100,

        "reward_xp": 150
    },

    "dragon_hunter": {

        "name": "Dragon Hunter",

        "description":
            "Defeat the ancient dragon "
            "terrorizing nearby villages.",

        "completed": False,

        "reward_claimed": False,

        "progress": 0,

        "goal": 1,

        "reward_gold": 200,

        "reward_xp": 300
    },

    "mage_rebellion": {

        "name": "Mage Rebellion",

        "description":
            "Assist the Mages Guild in stopping "
            "forbidden dark rituals.",

        "completed": False,

        "reward_claimed": False,

        "progress": 0,

        "goal": 2,

        "reward_gold": 120,

        "reward_xp": 180
    },

    "thorn_honor": {

        "name": "Thorn's Honor",

        "description":
            "Help Thorn restore his family's honor.",

        "completed": False,

        "reward_claimed": False,

        "progress": 0,

        "goal": 2,

        "reward_gold": 150,

        "reward_xp": 200
    },

    "mira_mentor": {

        "name": "Mira's Lost Mentor",

        "description":
            "Search for Mira's missing mentor "
            "within ancient ruins.",

        "completed": False,

        "reward_claimed": False,

        "progress": 0,

        "goal": 2,

        "reward_gold": 180,

        "reward_xp": 220
    }
}

# =========================
# SHOW QUESTS
# =========================

def show_quests():

    print("\n=== QUEST JOURNAL ===")

    for quest_key in quests:

        quest = quests[quest_key]

        status = "Completed"

        if not quest["completed"]:

            status = "Active"

        print("\n" + quest["name"])

        print(quest["description"])

        print(
            "Progress:",
            str(quest["progress"])
            + "/"
            + str(quest["goal"])
        )

        print("Status:", status)

# =========================
# PROGRESS QUEST
# =========================

def progress_quest(
    quest_key
):

    if quest_key not in quests:

        print(
            "\nQuest does not exist."
        )

        return

    quest = quests[quest_key]

    # =========================
    # ALREADY COMPLETE
    # =========================

    if quest["completed"]:

        return

    # =========================
    # ADD PROGRESS
    # =========================

    quest["progress"] += 1

    print(
        "\n=== QUEST UPDATED ==="
    )

    print(
        quest["name"]
    )

    print(
        str(quest["progress"])
        + "/"
        + str(quest["goal"])
    )

    # =========================
    # COMPLETE QUEST
    # =========================

    if quest["progress"] >= quest["goal"]:

        quest["completed"] = True

        print(
            "\n=== QUEST COMPLETED ==="
        )

        print(
            quest["name"]
        )

# =========================
# QUEST REWARDS
# =========================

def complete_quest_rewards(
    quest_key,
    player_gold,
    player_xp,
    factions,
    story_memory
):

    if quest_key not in quests:

        return (
            player_gold,
            player_xp,
            factions,
            story_memory
        )

    quest = quests[quest_key]

    # =========================
    # QUEST NOT COMPLETE
    # =========================

    if not quest["completed"]:

        return (
            player_gold,
            player_xp,
            factions,
            story_memory
        )

    # =========================
    # REWARD ALREADY CLAIMED
    # =========================

    if quest["reward_claimed"]:

        return (
            player_gold,
            player_xp,
            factions,
            story_memory
        )

    # =========================
    # GIVE REWARDS
    # =========================

    player_gold += quest["reward_gold"]

    player_xp += quest["reward_xp"]

    quest["reward_claimed"] = True

    print(
        "\n=== QUEST REWARDS ==="
    )

    print(
        "Gold Gained:",
        quest["reward_gold"]
    )

    print(
        "XP Gained:",
        quest["reward_xp"]
    )

    # =========================
    # QUEST CONSEQUENCES
    # =========================

    if quest_key == "shadow_cult_rising":

        factions = modify_reputation(
            factions,
            "kingdom",
            15
        )

        story_memory = update_memory(
            story_memory,
            "cult_defeated"
        )

    elif quest_key == "dragon_hunter":

        factions = modify_reputation(
            factions,
            "kingdom",
            25
        )

        story_memory = update_memory(
            story_memory,
            "dragon_slain"
        )

    elif quest_key == "mage_rebellion":

        factions = modify_reputation(
            factions,
            "mages_guild",
            20
        )

    elif quest_key == "thorn_honor":

        factions = modify_reputation(
            factions,
            "kingdom",
            10
        )

    elif quest_key == "mira_mentor":

        factions = modify_reputation(
            factions,
            "mages_guild",
            15
        )

    return (
        player_gold,
        player_xp,
        factions,
        story_memory
    )

# =========================
# QUEST EVENT CHECKS
# =========================

def update_quests_from_enemy(
    enemy_name
):

    # =========================
    # CULT QUEST
    # =========================

    if enemy_name == "hidden cult":

        progress_quest(
            "shadow_cult_rising"
        )

    # =========================
    # DRAGON QUEST
    # =========================

    elif enemy_name == "ancient dragon":

        progress_quest(
            "dragon_hunter"
        )

    # =========================
    # MAGE QUEST
    # =========================

    elif enemy_name == "necromancer":

        progress_quest(
            "mage_rebellion"
        )

# =========================
# COMPANION QUEST EVENTS
# =========================

def update_companion_quests(
    party
):

    if "Thorn" in party:

        progress_quest(
            "thorn_honor"
        )

    if "Mira" in party:

        progress_quest(
            "mira_mentor"
        )