from player import (
    player
)

from world_state import (
    world_state
)

from event_bus import (
    emit
)

# =========================
# EQUIPMENT SLOTS
# =========================

equipment = {

    "weapon": None,

    "armor": None,

    "helmet": None,

    "accessory": None
}

# =========================
# ITEM DATABASE
# =========================

ITEM_DATABASE = {

    # =========================
    # HERO STARTING ITEMS
    # Keys match hero inventory display names exactly so that
    # equip/unequip operations work without any translation layer.
    # =========================

    "Longsword": {

        "slot": "weapon",

        "attack_bonus": 4,

        "defense_bonus": 0,

        "rarity": "common"
    },

    "Knight's Shield": {

        "slot": "armor",

        "attack_bonus": 0,

        "defense_bonus": 3,

        "rarity": "common"
    },

    "Apprentice's Staff": {

        "slot": "weapon",

        "attack_bonus": 6,

        "defense_bonus": 0,

        "rarity": "common"
    },

    "Short Sword": {

        "slot": "weapon",

        "attack_bonus": 3,

        "defense_bonus": 0,

        "rarity": "common"
    },

    "Forging Hammer": {

        "slot": "weapon",

        "attack_bonus": 5,

        "defense_bonus": 0,

        "rarity": "common"
    },

    # =========================
    # DROPPED / PURCHASABLE
    # =========================

    "iron_sword": {

        "slot": "weapon",

        "attack_bonus": 5,

        "defense_bonus": 0,

        "rarity": "common"
    },

    "steel_armor": {

        "slot": "armor",

        "attack_bonus": 0,

        "defense_bonus": 8,

        "rarity": "uncommon"
    },

    "shadow_blade": {

        "slot": "weapon",

        "attack_bonus": 15,

        "defense_bonus": 0,

        "rarity": "rare"
    },

    "cult_amulet": {

        "slot": "accessory",

        "attack_bonus": 3,

        "defense_bonus": 3,

        "rarity": "rare"
    },

    "obsidian_helmet": {

        "slot": "helmet",

        "attack_bonus": 0,

        "defense_bonus": 6,

        "rarity": "epic"
    }
}

# =========================
# EQUIP STARTING ITEM
# =========================

def equip_slot_only(item_key):
    """Record a starting item as equipped WITHOUT applying its stat bonus.

    Used at hero selection when the hero roster's attack_bonus/defense
    already includes the equipped weapon's contribution.  Populating
    the equipment slot ensures the equipment system correctly tracks
    what is worn for later unequip/swap operations (remove_item_stats
    will then correctly subtract the weapon bonus when it is changed).

    Does NOT add the item to or remove it from inventory — callers
    are responsible for building the inventory list as needed.
    """

    item = ITEM_DATABASE.get(item_key)

    if not item:

        return

    slot = item["slot"]

    equipment[slot] = item_key

    # Keep world_state display fields in sync for weapon slot
    _sync_weapon_display()


# =========================
# SYNC WEAPON DISPLAY FIELDS
# =========================

def _sync_weapon_display():
    """Keep world_state[\"player\"][\"equipped_weapon\"] and weapon_bonus
    in sync with the authoritative equipment[\"weapon\"] slot.

    Called by equip_slot_only, equip_item, and unequip_item so that
    every code path (shop display, inventory screen, dialogue) reads
    the same state as combat.
    """

    weapon_key = equipment.get("weapon")

    ws_player = world_state["player"]

    if weapon_key:

        item = ITEM_DATABASE.get(weapon_key, {})

        ws_player["equipped_weapon"] = weapon_key

        ws_player["weapon_bonus"]    = item.get(
            "attack_bonus", 0
        )

    else:

        ws_player["equipped_weapon"] = ""

        ws_player["weapon_bonus"]    = 0


# =========================
# EQUIP ITEM
# =========================

def equip_item(

    item_name

):

    item = ITEM_DATABASE.get(
        item_name
    )

    if not item:

        print(
            "\nUnknown item."
        )

        return

    if item_name not in world_state["player"]["inventory"]:

        print(
            "\nItem not in inventory."
        )

        return

    slot = item["slot"]

    # =========================
    # UNEQUIP OLD ITEM
    # =========================

    old_item = equipment[slot]

    if old_item:

        remove_item_stats(
            old_item
        )

        world_state["player"]["inventory"].append(
            old_item
        )

    # =========================
    # EQUIP NEW ITEM
    # =========================

    equipment[slot] = item_name

    world_state["player"]["inventory"].remove(
        item_name
    )

    apply_item_stats(
        item_name
    )

    # Keep world_state display fields in sync for weapon slot
    if slot == "weapon":
        _sync_weapon_display()

    print(
        f"\nEquipped:"
        f" {item_name}"
    )

    emit(

        "item_equipped",

        item_name=item_name
    )

# =========================
# UNEQUIP ITEM
# =========================

def unequip_item(

    slot

):

    item_name = equipment.get(
        slot
    )

    if not item_name:

        print(
            "\nNo item equipped."
        )

        return

    remove_item_stats(
        item_name
    )

    world_state["player"]["inventory"].append(
        item_name
    )

    equipment[slot] = None

    # Keep world_state display fields in sync for weapon slot
    if slot == "weapon":
        _sync_weapon_display()

    print(
        f"\nUnequipped:"
        f" {item_name}"
    )

    emit(

        "item_unequipped",

        item_name=item_name
    )

# =========================
# APPLY ITEM STATS
# =========================

def apply_item_stats(

    item_name

):

    item = ITEM_DATABASE.get(
        item_name
    )

    if not item:

        return

    player.attack_bonus += item[
        "attack_bonus"
    ]

    player.defense += item[
        "defense_bonus"
    ]

    # Mirror stat changes into world_state["player"] immediately so
    # world-state consumers see up-to-date values before the next save.
    from player import sync_world_state_from_player
    sync_world_state_from_player()

# =========================
# REMOVE ITEM STATS
# =========================

def remove_item_stats(

    item_name

):

    item = ITEM_DATABASE.get(
        item_name
    )

    if not item:

        return

    player.attack_bonus -= item[
        "attack_bonus"
    ]

    player.defense -= item[
        "defense_bonus"
    ]

    # Mirror stat changes into world_state["player"] immediately.
    from player import sync_world_state_from_player
    sync_world_state_from_player()

# =========================
# SHOW EQUIPMENT
# =========================

def show_equipment():

    print(
        "\n=== EQUIPMENT ==="
    )

    for slot, item in equipment.items():

        print(
            f"\n{slot}: {item}"
        )

# =========================
# SHOW ITEM DETAILS
# =========================

def show_item_details(

    item_name

):

    item = ITEM_DATABASE.get(
        item_name
    )

    if not item:

        print(
            "\nUnknown item."
        )

        return

    print(
        "\n=== ITEM DETAILS ==="
    )

    print(
        "Item:",
        item_name
    )

    print(
        "Slot:",
        item["slot"]
    )

    print(
        "Attack Bonus:",
        item["attack_bonus"]
    )

    print(
        "Defense Bonus:",
        item["defense_bonus"]
    )

    print(
        "Rarity:",
        item["rarity"]
    )

# =========================
# TOTAL PLAYER POWER
# =========================

def calculate_player_power():

    power = 0

    for slot, item_name in equipment.items():

        if not item_name:

            continue

        item = ITEM_DATABASE.get(
            item_name
        )

        if not item:

            continue

        power += item[
            "attack_bonus"
        ]

        power += item[
            "defense_bonus"
        ]

    return power

# =========================
# LEGENDARY ITEM CHECK
# =========================

def has_legendary_equipment():

    for slot, item_name in equipment.items():

        if not item_name:

            continue

        item = ITEM_DATABASE.get(
            item_name
        )

        if not item:

            continue

        if item[
            "rarity"
        ] == "legendary":

            return True

    return False

# =========================
# ADD LEGENDARY ITEM
# =========================

def create_legendary_item(

    item_name,
    slot,
    attack_bonus,
    defense_bonus

):

    ITEM_DATABASE[
        item_name
    ] = {

        "slot": slot,

        "attack_bonus": attack_bonus,

        "defense_bonus": defense_bonus,

        "rarity": "legendary"
    }

    print(
        f"\nLegendary item created:"
        f" {item_name}"
    )

# =========================
# EQUIPMENT SUMMARY
# =========================

def show_equipment_summary():

    print(
        "\n=== EQUIPMENT SUMMARY ==="
    )

    print(
        "Player Power:",
        calculate_player_power()
    )

    print(
        "Legendary Equipped:",
        has_legendary_equipment()
    )