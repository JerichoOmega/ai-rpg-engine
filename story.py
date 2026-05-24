import random

from world_state import (
    world_state,
    world_story_modifier
)

# =========================
# STORY GENERATION SYSTEM
# =========================

def generate_story(
    enemies,
    factions,
    story_memory
):

    story_modifiers = world_story_modifier()

    # =========================
    # DEFAULT LOCATIONS
    # =========================

    locations = [

        "A ruined village covered in ash.",

        "An ancient forest filled with whispers.",

        "A frozen mountain pass.",

        "A cursed battlefield.",

        "Dark catacombs beneath the capital.",

        "A forgotten temple buried underground."
    ]

    # =========================
    # WORLD STATE LOCATIONS
    # =========================

    if world_state[
        "civil_war"
    ]:

        locations.append(

            "A war-torn city engulfed in flames."
        )

    if world_state[
        "cult_rising"
    ]:

        locations.append(

            "A corrupted village controlled by cultists."
        )

    if world_state[
        "mages_rebellion"
    ]:

        locations.append(

            "An unstable arcane tower crackling with energy."
        )

    if world_state[
        "world_chaos"
    ] >= 60:

        locations.append(

            "A shattered landscape consumed by darkness."
        )

    # =========================
    # SELECT LOCATION
    # =========================

    location = random.choice(
        locations
    )

    # =========================
    # DEFAULT QUESTS
    # =========================

    quests = [

        "Recover a lost relic.",

        "Defeat the enemy threatening the region.",

        "Investigate strange disappearances.",

        "Protect innocent travelers.",

        "Track a dangerous beast.",

        "Explore forgotten ruins."
    ]

    # =========================
    # WORLD QUESTS
    # =========================

    if world_state[
        "cult_rising"
    ]:

        quests.append(

            "Stop a dark ritual before it spreads corruption."
        )

    if world_state[
        "civil_war"
    ]:

        quests.append(

            "Choose a side in the growing civil war."
        )

    if world_state[
        "mages_rebellion"
    ]:

        quests.append(

            "Investigate forbidden magical experiments."
        )

    if not world_state[
        "dragon_alive"
    ]:

        quests.append(

            "Help villages rebuild after the dragon attacks."
        )

    # =========================
    # STORY MEMORY QUESTS
    # =========================

    if story_memory[
        "joined_shadow_cult"
    ]:

        quests.append(

            "Strengthen the influence of the Shadow Cult."
        )

    if story_memory[
        "spared_cultist"
    ]:

        quests.append(

            "Search for the cultist you once spared."
        )

    if story_memory[
        "executed_cultist"
    ]:

        quests.append(

            "Deal with growing fear surrounding your reputation."
        )

    if story_memory[
        "dragon_slain"
    ]:

        quests.append(

            "Face the consequences of slaying the dragon."
        )

    # =========================
    # FACTION QUESTS
    # =========================

    if factions[
        "kingdom"
    ] >= 30:

        quests.append(

            "The kingdom requests your aid against rising threats."
        )

    if factions[
        "shadow_cult"
    ] >= 40:

        quests.append(

            "The Shadow Cult offers you forbidden power."
        )

    if factions[
        "mages_guild"
    ] >= 40:

        quests.append(

            "The Mages Guild seeks your help recovering lost knowledge."
        )

    # =========================
    # SELECT QUEST
    # =========================

    quest = random.choice(
        quests
    )

    # =========================
    # ENEMY SELECTION
    # =========================

    enemy_pool = list(
        enemies.keys()
    )

    # =========================
    # WORLD ENEMY CHANGES
    # =========================

    if world_state[
        "cult_rising"
    ]:

        enemy_pool.extend([

            "hidden cult",

            "hidden cult"
        ])

    if world_state[
        "civil_war"
    ]:

        enemy_pool.extend([

            "corrupted knight"
        ])

    if world_state[
        "mages_rebellion"
    ]:

        enemy_pool.extend([

            "necromancer"
        ])

    if world_state[
        "world_chaos"
    ] >= 70:

        enemy_pool.extend([

            "shadow beast",

            "shadow beast"
        ])

    # =========================
    # STORY MEMORY ENEMIES
    # =========================

    if story_memory[
        "joined_shadow_cult"
    ]:

        if "hidden cult" in enemy_pool:

            enemy_pool.remove(
                "hidden cult"
            )

    # =========================
    # SELECT ENEMY
    # =========================

    enemy_name = random.choice(
        enemy_pool
    )

    # =========================
    # STORY MODIFIERS
    # =========================

    print(
        "\n=== WORLD CONDITIONS ==="
    )

    if len(story_modifiers) == 0:

        print(
            "The world remains relatively stable."
        )

    else:

        for modifier in story_modifiers:

            print(
                "-",
                modifier
            )

    # =========================
    # DYNAMIC INTRO TEXT
    # =========================

    intro_text = [

        "Rumors spread across the land.",

        "Fear grips the nearby settlements.",

        "Travelers whisper of growing danger.",

        "Ancient powers begin to awaken.",

        "The balance of the world shifts."
    ]

    if world_state[
        "world_chaos"
    ] >= 50:

        intro_text.append(

            "Darkness spreads uncontrollably across the kingdom."
        )

    if world_state[
        "civil_war"
    ]:

        intro_text.append(

            "The sounds of war echo in the distance."
        )

    if world_state[
        "cult_rising"
    ]:

        intro_text.append(

            "Cult symbols appear carved into ruined walls."
        )

    print(
        "\n" + random.choice(
            intro_text
        )
    )

    return (
        quest,
        location,
        enemy_name
    )