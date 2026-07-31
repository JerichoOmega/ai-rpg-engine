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

from world_state import (
    world_state
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

    # Scale companion to current player level before adding to party.
    _scale_companion_to_player_level(
        companion_name,
        companion
    )

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
# COMPANION LEVEL SCALING
# =========================

def _scale_companion_to_player_level(
    companion_name,
    companion
):
    """Scale a companion to the current player level on recruitment so
    benched heroes never fall behind the active party.

    Idempotent: base stats are stored in the roster entry on first recruit
    and reused on every subsequent recruit, so remove→re-recruit at a
    higher player level applies the delta correctly rather than stacking
    the full multiplier on already-scaled values.
    """

    from progression_manager import (
        progression_state,
        MAX_LEVEL,
        _xp_threshold
    )

    if "roster" not in world_state:
        world_state["roster"] = {}

    current_level = min(
        progression_state["level"],
        MAX_LEVEL
    )

    existing_entry = world_state["roster"].get(companion_name)

    if existing_entry and "base_max_hp" in existing_entry:
        # Re-recruit: scale from the stored immutable level-1 base stats.
        base_max_hp = existing_entry["base_max_hp"]
        base_damage = existing_entry["base_damage"]
    else:
        # First recruit: current companion stats are the level-1 base.
        base_max_hp = companion.get("max_hp", 100)
        base_damage = companion.get("damage", 10)

    scaled_max_hp = base_max_hp + (current_level - 1) * 20
    scaled_attack_bonus = 5 + (current_level - 1) * 2
    scaled_damage = base_damage + (current_level - 1) * 2

    # Update the companion's combat-facing stats.
    companion["max_hp"] = scaled_max_hp
    companion["hp"] = scaled_max_hp
    companion["damage"] = scaled_damage

    # Write (or overwrite) the roster entry.  base_max_hp and base_damage
    # are the immutable level-1 anchors used by future re-recruit calls.
    world_state["roster"][companion_name] = {
        "level": current_level,
        "xp": 0,
        "xp_to_next_level": _xp_threshold(current_level),
        "max_hp": scaled_max_hp,
        "attack_bonus": scaled_attack_bonus,
        "damage": scaled_damage,
        "base_max_hp": base_max_hp,
        "base_damage": base_damage,
    }

    if current_level > 1:
        print(
            f"\n{companion_name.title()}"
            f" joins at level {current_level}."
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