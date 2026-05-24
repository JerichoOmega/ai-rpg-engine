# =========================
# WEAPON DATABASE
# =========================

weapons = {

    "Rusty Sword": {
        "damage": 2,
        "crit_bonus": 0
    },

    "Iron Sword": {
        "damage": 4,
        "crit_bonus": 2
    },

    "Shadow Dagger": {
        "damage": 2,
        "crit_bonus": 10
    },

    "Magic Staff": {
        "damage": 5,
        "crit_bonus": 5
    },

    "Dragon Slayer": {
        "damage": 8,
        "crit_bonus": 15
    }
}

# =========================
# ARMOR DATABASE
# =========================

armor = {

    "Leather Armor": {
        "defense": 2
    },

    "Iron Armor": {
        "defense": 5
    },

    "Dragon Armor": {
        "defense": 10
    }
}

# =========================
# GET WEAPON STATS
# =========================

def get_weapon_stats(weapon_name):

    if weapon_name in weapons:

        return weapons[weapon_name]

    return {
        "damage": 0,
        "crit_bonus": 0
    }

# =========================
# GET ARMOR STATS
# =========================

def get_armor_stats(armor_name):

    if armor_name in armor:

        return armor[armor_name]

    return {
        "defense": 0
    }