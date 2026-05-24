import random

# =========================
# STORY GENERATION SYSTEM
# =========================

def generate_story(
    enemies,
    factions,
    story_memory
):

    quest = ""

    location = ""

    enemy_name = ""

    # =========================
    # SHADOW CULT PATH
    # =========================

    if story_memory["joined_shadow_cult"]:

        quest = (
            "The Shadow Cult secretly requests"
            " your assistance in corrupting"
            " a royal sanctuary."
        )

        location = (
            "A forgotten underground temple"
            " lit by cursed candles."
        )

        enemy_name = "corrupted knight"

    # =========================
    # DRAGON SLAYER PATH
    # =========================

    elif story_memory["dragon_slain"]:

        quest = (
            "Villagers beg the legendary"
            " dragon slayer for help against"
            " rising undead."
        )

        location = (
            "A ruined village covered"
            " in black ash."
        )

        enemy_name = "necromancer"

    # =========================
    # DEFAULT RANDOM STORIES
    # =========================

    else:

        story_templates = [

            {
                "quest": (
                    "A hidden cult has begun"
                    " summoning dark creatures"
                    " beneath the city."
                ),

                "location": (
                    "An abandoned cathedral"
                    " filled with strange whispers."
                ),

                "enemy": "hidden cult"
            },

            {
                "quest": (
                    "An ancient dragon terrorizes"
                    " nearby villages with fire"
                    " and destruction."
                ),

                "location": (
                    "A volcanic mountain surrounded"
                    " by rivers of lava."
                ),

                "enemy": "ancient dragon"
            },

            {
                "quest": (
                    "A corrupted knight guards"
                    " the ruins of a fallen kingdom."
                ),

                "location": (
                    "A shattered battlefield covered"
                    " in rusted weapons."
                ),

                "enemy": "corrupted knight"
            },

            {
                "quest": (
                    "A shadow beast stalks travelers"
                    " within the cursed forest."
                ),

                "location": (
                    "Dark woods where fog crawls"
                    " across twisted roots."
                ),

                "enemy": "shadow beast"
            },

            {
                "quest": (
                    "A necromancer raises undead"
                    " armies beneath an ancient crypt."
                ),

                "location": (
                    "A forgotten tomb illuminated"
                    " by eerie green flames."
                ),

                "enemy": "necromancer"
            }
        ]

        selected_story = random.choice(
            story_templates
        )

        quest = selected_story["quest"]

        location = selected_story["location"]

        enemy_name = selected_story["enemy"]

    return (
        quest,
        location,
        enemy_name
    )