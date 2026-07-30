import random

from world_state import (
    world_state
)

from region_manager import (
    REGIONS
)

from campaign_manager import (
    campaign_state
)

from narrative_ai import (
    narrate_battle
)

from combat import (
    combat
)

from event_bus import (
    emit
)

# =========================
# REGION ENCOUNTERS
# =========================

REGION_ENCOUNTERS = {

    "kingdom_capital": [

        "bandits",

        "political unrest",

        "merchant dispute"
    ],

    "shadow_marsh": [

        "hidden cult",

        "shadow beast",

        "swamp ambush"
    ],

    "arcane_ruins": [

        "rogue mage",

        "arcane anomaly",

        "living construct"
    ],

    "ashen_wastes": [

        "undead horde",

        "necromancer",

        "demon scout"
    ]
}

# =========================
# ENCOUNTER TYPES
# =========================

NARRATIVE_EVENTS = [

    "wandering refugee",

    "traveling bard",

    "dying messenger",

    "lost child",

    "mysterious merchant"
]

# =========================
# GENERATE ENCOUNTER
# =========================

def generate_encounter():

    current_region = world_state[
        "regions"
    ]["current_region"]

    region = REGIONS.get(
        current_region
    )

    if not region:

        return

    danger = region[
        "danger"
    ]

    print(
        "\n=== ENCOUNTER ==="
    )

    # =========================
    # HIGH DANGER
    # =========================

    if danger >= 70:

        generate_combat_encounter(
            current_region
        )

    # =========================
    # MEDIUM DANGER
    # =========================

    elif danger >= 35:

        roll = random.randint(
            1,
            100
        )

        if roll <= 60:

            generate_combat_encounter(
                current_region
            )

        else:

            generate_narrative_encounter()

    # =========================
    # LOW DANGER
    # =========================

    else:

        generate_narrative_encounter()

# =========================
# COMBAT ENCOUNTER
# =========================

def generate_combat_encounter(

    region_name

):

    encounters = REGION_ENCOUNTERS.get(
        region_name,
        []
    )

    if len(encounters) == 0:

        return

    enemy_name = random.choice(
        encounters
    )

    enemy_hp = random.randint(
        25,
        70
    )

    print(
        f"\nA dangerous encounter begins:"
        f" {enemy_name}"
    )

    narrate_battle(
        enemy_name
    )

    emit(

        "encounter_started",

        encounter=enemy_name
    )

    combat(
        enemy_name,
        enemy_hp
    )

# =========================
# NARRATIVE ENCOUNTER
# =========================

def generate_narrative_encounter():

    event_name = random.choice(
        NARRATIVE_EVENTS
    )

    print(
        "\n=== NARRATIVE EVENT ==="
    )

    print(
        f"\nYou encounter:"
        f" {event_name}"
    )

    # =========================
    # SPECIFIC EVENTS
    # =========================

    if event_name == "wandering refugee":

        print(
            "\nThe refugee speaks of war"
            " spreading across nearby lands."
        )

    elif event_name == "traveling bard":

        print(
            "\nThe bard sings of ancient heroes."
        )

    elif event_name == "dying messenger":

        print(
            "\nThe messenger warns of"
            " growing darkness."
        )

    emit(

        "narrative_encounter",

        event_name=event_name
    )

# =========================
# CAMPAIGN ENCOUNTERS
# =========================

def generate_campaign_encounter():

    stage = campaign_state[
        "campaign_stage"
    ]

    print(
        "\n=== CAMPAIGN ENCOUNTER ==="
    )

    if stage == "emergence":

        print(
            "\nCult influence quietly spreads."
        )

    elif stage == "regional_conflict":

        print(
            "\nSoldiers march toward war."
        )

    elif stage == "world_crisis":

        print(
            "\nRefugees flee collapsing cities."
        )

    elif stage == "final_catastrophe":

        print(
            "\nThe world itself begins to fail."
        )

# =========================
# RANDOM TRAVEL EVENT
# =========================

def random_travel_event():

    roll = random.randint(
        1,
        100
    )

    if roll <= 50:

        generate_encounter()

    else:

        print(
            "\nYour travels remain quiet..."
        )

# =========================
# ESCALATION
# =========================

def evaluate_encounter_difficulty():

    chaos = world_state[
        "world_conditions"
    ]["world_chaos"]

    if chaos >= 50:

        print(
            "\nEncounters grow increasingly deadly."
        )

# =========================
# EVENT REACTIONS
# =========================

def on_region_crisis(

    event_data

):

    region_name = event_data.get(
        "region_name"
    )

    print(
        f"\nEncounters worsen in"
        f" {region_name}."
    )

def on_faction_war_started(

    event_data

):

    print(
        "\nWar creates dangerous new encounters."
    )

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "region_crisis",
    on_region_crisis
)

subscribe(
    "faction_war_started",
    on_faction_war_started
)