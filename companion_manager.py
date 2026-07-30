import random

from player import (
    player
)

from story_manager import (
    story_state
)

from faction_manager import (
    get_faction_status
)

from event_bus import (
    emit
)

# =========================
# ACTIVE COMPANIONS
# =========================

active_companions = []

# =========================
# COMPANION DATABASE
# =========================

COMPANIONS = {

    "kael": {

        "role": "warrior",

        "faction": "kingdom",

        "max_hp": 120,

        "hp": 120,

        "damage": 18,

        "loyalty": 50,

        "morality": "honorable",

        "corruption": 0,

        "abilities": [

            "shield_bash",

            "guardian_strike"
        ],

        "recruitable": True
    },

    "lyra": {

        "role": "mage",

        "faction": "mages_guild",

        "max_hp": 80,

        "hp": 80,

        "damage": 25,

        "loyalty": 50,

        "morality": "neutral",

        "corruption": 0,

        "abilities": [

            "arcane_burst",

            "mana_shield"
        ],

        "recruitable": True
    },

    "vex": {

        "role": "rogue",

        "faction": "shadow_cult",

        "max_hp": 90,

        "hp": 90,

        "damage": 22,

        "loyalty": 35,

        "morality": "ruthless",

        "corruption": 20,

        "abilities": [

            "bleed_attack",

            "shadow_step"
        ],

        "recruitable": True
    }
}

# =========================
# RECRUIT COMPANION
# =========================

def recruit_companion(

    companion_name

):

    companion = COMPANIONS.get(
        companion_name
    )

    if not companion:

        print(
            "\nUnknown companion."
        )

        return

    if companion in active_companions:

        print(
            "\nCompanion already recruited."
        )

        return

    # =========================
    # FACTION CHECK
    # =========================

    faction = companion[
        "faction"
    ]

    faction_status = get_faction_status(
        faction
    )

    if faction_status == "enemy":

        print(
            f"\n{companion_name}"
            " refuses to join you."
        )

        return

    active_companions.append(
        companion
    )

    print(
        f"\n{companion_name}"
        " joins your party."
    )

    emit(

        "companion_joined",

        companion_name=companion_name
    )

# =========================
# REMOVE COMPANION
# =========================

def remove_companion(

    companion_name

):

    for companion in active_companions:

        if companion[
            "role"
        ] == companion_name:

            active_companions.remove(
                companion
            )

            print(
                f"\n{companion_name}"
                " leaves the party."
            )

            return

# =========================
# COMPANION ATTACK
# =========================

def companion_attack(

    companion,

    enemy

):

    damage = random.randint(
        5,
        companion["damage"]
    )

    enemy["hp"] -= damage

    print(
        f"\n{companion['role'].title()}"
        f" attacks for"
        f" {damage} damage!"
    )

    return damage

# =========================
# COMPANION ABILITY
# =========================

def use_companion_ability(

    companion,

    enemy=None

):

    abilities = companion.get(
        "abilities",
        []
    )

    if not abilities:

        return

    ability = random.choice(
        abilities
    )

    print(
        f"\n{ability} activated!"
    )

    # =========================
    # WARRIOR
    # =========================

    if ability == "shield_bash":

        if enemy:

            enemy["hp"] -= 10

            print(
                "\nEnemy staggered!"
            )

    # =========================
    # MAGE
    # =========================

    elif ability == "arcane_burst":

        if enemy:

            enemy["hp"] -= 20

            print(
                "\nArcane energy erupts!"
            )

    # =========================
    # ROGUE
    # =========================

    elif ability == "bleed_attack":

        if enemy:

            enemy["hp"] -= 15

            print(
                "\nBleeding strike lands!"
            )

# =========================
# LOYALTY
# =========================

def change_loyalty(

    companion_name,

    amount

):

    companion = COMPANIONS.get(
        companion_name
    )

    if not companion:

        return

    companion[
        "loyalty"
    ] += amount

    companion[
        "loyalty"
    ] = max(

        0,

        min(

            companion[
                "loyalty"
            ],

            100
        )
    )

    print(
        f"\n{companion_name}"
        f" loyalty changed by"
        f" {amount}."
    )

    evaluate_loyalty(
        companion_name
    )

# =========================
# EVALUATE LOYALTY
# =========================

def evaluate_loyalty(

    companion_name

):

    companion = COMPANIONS.get(
        companion_name
    )

    if not companion:

        return

    loyalty = companion[
        "loyalty"
    ]

    # =========================
    # BETRAYAL
    # =========================

    if loyalty <= 10:

        print(
            f"\n{companion_name}"
            " may betray you..."
        )

        emit(

            "companion_betrayal",

            companion=companion_name
        )

    # =========================
    # DEVOTION
    # =========================

    elif loyalty >= 90:

        print(
            f"\n{companion_name}"
            " is deeply loyal."
        )

# =========================
# CORRUPTION
# =========================

def corrupt_companion(

    companion_name,

    amount

):

    companion = COMPANIONS.get(
        companion_name
    )

    if not companion:

        return

    companion[
        "corruption"
    ] += amount

    print(
        f"\n{companion_name}"
        f" corruption increased by"
        f" {amount}."
    )

    # =========================
    # CORRUPTION REACTION
    # =========================

    if companion[
        "corruption"
    ] >= 75:

        print(
            f"\n{companion_name}"
            " is consumed by darkness."
        )

        emit(

            "companion_corrupted",

            companion=companion_name
        )

# =========================
# COMPANION REACTION
# =========================

def companion_story_reaction(

    companion_name

):

    companion = COMPANIONS.get(
        companion_name
    )

    if not companion:

        return

    theme = story_state[
        "active_theme"
    ]

    print(
        f"\n=== {companion_name.upper()} REACTS ==="
    )

    if theme == "redemption":

        print(
            "\n'I still believe"
            " there is hope.'"
        )

    elif theme == "corruption":

        print(
            "\n'The darkness grows"
            " stronger around us.'"
        )

    elif theme == "conquest":

        print(
            "\n'Power changes people.'"
        )

    else:

        print(
            "\n'We should stay focused.'"
        )

# =========================
# PARTY BONUS
# =========================

def calculate_party_bonus():

    bonus = 0

    for companion in active_companions:

        bonus += int(
            companion[
                "loyalty"
            ] / 10
        )

    return bonus

# =========================
# HEAL PARTY
# =========================

def heal_party():

    for companion in active_companions:

        companion[
            "hp"
        ] = companion[
            "max_hp"
        ]

    print(
        "\nThe party recovers."
    )

# =========================
# PARTY STATUS
# =========================

def show_party():

    print(
        "\n=== PARTY ==="
    )

    if not active_companions:

        print(
            "\nNo companions recruited."
        )

        return

    for companion in active_companions:

        print(
            f"\nRole:"
            f" {companion['role']}"
        )

        print(
            f"HP:"
            f" {companion['hp']}"
            f"/"
            f"{companion['max_hp']}"
        )

        print(
            f"Loyalty:"
            f" {companion['loyalty']}"
        )

        print(
            f"Corruption:"
            f" {companion['corruption']}"
        )

# =========================
# COMPANION BANTER
# =========================

def random_companion_banter():

    if not active_companions:

        return

    banter = [

        "The road ahead feels dangerous.",

        "I don't trust these lands.",

        "We should prepare for battle.",

        "Something is watching us.",

        "This world grows darker each day."
    ]

    chosen = random.choice(
        banter
    )

    print(
        "\n=== PARTY BANTER ==="
    )

    print(
        chosen
    )

# =========================
# COMPANION SUMMARY
# =========================

def show_companion_summary():

    print(
        "\n=== COMPANION SUMMARY ==="
    )

    print(
        f"Active Companions:"
        f" {len(active_companions)}"
    )

    print(
        f"Party Bonus:"
        f" {calculate_party_bonus()}"
    )