import random

# =========================
# QUESTS
# =========================

quests = [
    "A village is haunted by whispers at night.",
    "A merchant caravan disappeared in the woods.",
    "A mining town has suddenly gone silent.",
    "A royal tomb has been broken into.",
    "A mysterious plague spreads through the kingdom."
]

# =========================
# LOCATIONS
# =========================

locations = [
    "inside cursed woods",
    "beneath an ancient castle",
    "under a ruined city",
    "inside frozen caves",
    "within a dark swamp"
]

# =========================
# STORY GENERATION
# =========================

def generate_story(enemies):

    quest = random.choice(quests)

    location = random.choice(locations)

    enemy_name = random.choice(list(enemies.keys()))

    return quest, location, enemy_name