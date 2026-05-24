# =========================
# WORLD STATE SYSTEM
# =========================

from factions import modify_reputation

from memory import update_memory

# =========================
# GLOBAL WORLD STATE
# =========================

world_state = {

    "kingdom_influence": 0,

    "cult_influence": 0,

    "mages_guild_influence": 0,

    "world_chaos": 0,

    "dragon_alive": True,

    "kingdom_stability": 100,

    "cult_rising": False,

    "mages_rebellion": False,

    "civil_war": False,

    "shadow_corruption": 0
}

# =========================
# SHOW WORLD STATE
# =========================

def show_world_state():

    print(
        "\n=== WORLD STATE ==="
    )

    for state in world_state:

        print(
            state,
            ":",
            world_state[state]
        )

# =========================
# UPDATE WORLD STATE
# =========================

def update_world_state(
    factions,
    story_memory,
    party
):

    print(
        "\n=== WORLD EVOLUTION ==="
    )

    # =========================
    # SHADOW CULT RISING
    # =========================

    if factions[
        "shadow_cult"
    ] >= 50:

        if not world_state[
            "cult_rising"
        ]:

            print(
                "\nThe Shadow Cult spreads"
                " across the kingdom."
            )

            world_state[
                "cult_rising"
            ] = True

        world_state[
            "cult_influence"
        ] += 10

        world_state[
            "shadow_corruption"
        ] += 5

        world_state[
            "world_chaos"
        ] += 5

    # =========================
    # KINGDOM COLLAPSE
    # =========================

    if factions[
        "kingdom"
    ] <= -50:

        print(
            "\nThe kingdom begins"
            " to collapse into unrest."
        )

        world_state[
            "kingdom_stability"
        ] -= 15

        world_state[
            "world_chaos"
        ] += 10

    # =========================
    # MAGES GUILD POWER
    # =========================

    if factions[
        "mages_guild"
    ] >= 40:

        print(
            "\nThe Mages Guild gains"
            " political influence."
        )

        world_state[
            "mages_guild_influence"
        ] += 10

    # =========================
    # DRAGON DEFEATED
    # =========================

    if story_memory[
        "dragon_slain"
    ]:

        if world_state[
            "dragon_alive"
        ]:

            print(
                "\nVillages celebrate"
                " the dragon's defeat."
            )

            world_state[
                "dragon_alive"
            ] = False

            world_state[
                "kingdom_stability"
            ] += 20

    # =========================
    # CULT DOMINANCE
    # =========================

    if world_state[
        "cult_influence"
    ] >= 60:

        print(
            "\nDark rituals spread"
            " through the land."
        )

        world_state[
            "world_chaos"
        ] += 15

    # =========================
    # MAGES REBELLION
    # =========================

    if world_state[
        "mages_guild_influence"
    ] >= 50:

        if not world_state[
            "mages_rebellion"
        ]:

            print(
                "\nThe Mages Guild begins"
                " an uprising."
            )

            world_state[
                "mages_rebellion"
            ] = True

    # =========================
    # CIVIL WAR
    # =========================

    if (

        world_state[
            "kingdom_stability"
        ] <= 40

        and

        world_state[
            "world_chaos"
        ] >= 50

    ):

        if not world_state[
            "civil_war"
        ]:

            print(
                "\nCivil war erupts"
                " across the kingdom!"
            )

            world_state[
                "civil_war"
            ] = True

    # =========================
    # COMPANION EFFECTS
    # =========================

    if "Mira" not in party:

        print(
            "\nWithout Mira,"
            " magical instability grows."
        )

        world_state[
            "world_chaos"
        ] += 1

    if "Thorn" not in party:

        print(
            "\nWithout Thorn,"
            " kingdom morale weakens."
        )

        world_state[
            "kingdom_stability"
        ] -= 1

    if "Kael" not in party:

        print(
            "\nWithout Kael,"
            " underground intelligence fades."
        )

        world_state[
            "cult_influence"
        ] += 1

    # =========================
    # WORLD LIMITS
    # =========================

    if world_state[
        "kingdom_stability"
    ] > 100:

        world_state[
            "kingdom_stability"
        ] = 100

    elif world_state[
        "kingdom_stability"
    ] < 0:

        world_state[
            "kingdom_stability"
        ] = 0

    if world_state[
        "world_chaos"
    ] > 100:

        world_state[
            "world_chaos"
        ] = 100

    elif world_state[
        "world_chaos"
        ] < 0:

        world_state[
            "world_chaos"
        ] = 0

# =========================
# WORLD EVENT GENERATOR
# =========================

def world_event():

    print(
        "\n=== WORLD EVENT ==="
    )

    # =========================
    # CULT EVENTS
    # =========================

    if world_state[
        "cult_rising"
    ]:

        print(
            "\nCultists have begun"
            " appearing openly in cities."
        )

    # =========================
    # CIVIL WAR EVENTS
    # =========================

    if world_state[
        "civil_war"
    ]:

        print(
            "\nRefugees flee from"
            " war-torn villages."
        )

    # =========================
    # MAGES REBELLION
    # =========================

    if world_state[
        "mages_rebellion"
    ]:

        print(
            "\nArcane storms erupt"
            " near ancient ruins."
        )

    # =========================
    # HIGH CHAOS
    # =========================

    if world_state[
        "world_chaos"
    ] >= 70:

        print(
            "\nThe world spirals deeper"
            " into darkness."
        )

# =========================
# WORLD STORY MODIFIERS
# =========================

def world_story_modifier():

    modifiers = []

    # =========================
    # CULT CONTROL
    # =========================

    if world_state[
        "cult_influence"
    ] >= 50:

        modifiers.append(
            "Cult-controlled regions"
        )

    # =========================
    # CIVIL WAR
    # =========================

    if world_state[
        "civil_war"
    ]:

        modifiers.append(
            "War-torn battlefields"
        )

    # =========================
    # DRAGON DEAD
    # =========================

    if not world_state[
        "dragon_alive"
    ]:

        modifiers.append(
            "Villages rebuilding after"
            " dragon attacks"
        )

    # =========================
    # ARCANE CHAOS
    # =========================

    if world_state[
        "mages_rebellion"
    ]:

        modifiers.append(
            "Arcane storms"
        )

    return modifiers