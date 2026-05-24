import random

# =========================
# RARITY DATA
# =========================

rarities = {

    "Common": {
        "multiplier": 2
    },

    "Rare": {
        "multiplier": 4
    },

    "Epic": {
        "multiplier": 7
    },

    "Legendary": {
        "multiplier": 12
    }
}

# =========================
# ITEM AFFIXES
# =========================

affixes = {

    "Flaming": {
        "effect": "burn",
        "element": "fire"
    },

    "Frozen": {
        "effect": "freeze",
        "element": "ice"
    },

    "Venomous": {
        "effect": "poison",
        "element": "poison"
    },

    "Vampiric": {
        "effect": "lifesteal",
        "element": "dark"
    }
}

# =========================
# GENERATE LOOT
# =========================

def generate_loot(base_item):

    rarity_roll = random.randint(1, 100)

    # =========================
    # DETERMINE RARITY
    # =========================

    if rarity_roll <= 50:

        rarity = "Common"

    elif rarity_roll <= 80:

        rarity = "Rare"

    elif rarity_roll <= 95:

        rarity = "Epic"

    else:

        rarity = "Legendary"

    multiplier = rarities[rarity]["multiplier"]

    # =========================
    # RANDOM AFFIX
    # =========================

    affix_name = random.choice(
        list(affixes.keys())
    )

    affix_effect = affixes[affix_name]["effect"]

    element_type = affixes[affix_name]["element"]

    # =========================
    # FINAL ITEM DATA
    # =========================

    item_data = {

        "name": (
            rarity
            + " "
            + affix_name
            + " "
            + base_item
        ),

        "rarity": rarity,

        "effect": affix_effect,

        "element": element_type,

        "damage_bonus": multiplier,

        "crit_bonus": multiplier * 2,

        "defense_bonus": multiplier
    }

    return item_data