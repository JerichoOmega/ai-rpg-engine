# =========================
# CENTRAL WORLD STATE SYSTEM
# =========================

world_state = {

    # =========================
    # TIME
    # =========================

    "time": {

        "day": 1,

        "hour": 8,

        "weather": "clear"
    },

    # =========================
    # PLAYER
    # =========================

    "player": {

        "name": "Adventurer",

        "class": "",

        "hp": 100,

        "max_hp": 100,

        "gold": 25,

        "level": 1,

        "xp": 0,

        "xp_to_next_level": 100,

        "resource_name": "Stamina",

        "resource": 100,

        "max_resource": 100,

        "attack_bonus": 5,

        "defense": 0,

        "dodge": 0,

        "reputation": 0,

        "inventory": [],

        "equipped_weapon": "Rusty Sword",

        "weapon_bonus": 0,

        "status_effects": []
    },

    # =========================
    # COMPANIONS
    # =========================

    "companions": {

        "party": [],

        "recruited": [],

        "relationships": {},

        "loyalty": {}
    },

    # =========================
    # WORLD CONDITIONS
    # =========================

    "world_conditions": {

        "world_chaos": 0,

        "civil_war": False,

        "cult_rising": False,

        "mages_rebellion": False,

        "dragon_awakened": False
    },

    # =========================
    # FACTIONS
    # =========================

    "factions": {

        "kingdom": 0,

        "shadow_cult": 0,

        "mages_guild": 0,

        "neutral": 0
    },

    # =========================
    # REGIONS
    # =========================

    "regions": {

        "current_region": "kingdom_capital",

        "discovered_regions": [],

        "faction_control": {

            "kingdom_capital": "kingdom",

            "shadow_marsh": "shadow_cult",

            "frostpeak_mountains": "neutral",

            "arcane_ruins": "mages_guild",

            "ashen_wastes": "neutral"
        }
    },

    # =========================
    # NPCS
    # =========================

    "npcs": {

        "King Aldric": {

            "alive": True,

            "location": "kingdom_capital",

            "relationship": 0,

            "role": "king"
        },

        "Archmage Seraph": {

            "alive": True,

            "location": "arcane_ruins",

            "relationship": 0,

            "role": "mage_leader"
        },

        "Shade Prophet": {

            "alive": True,

            "location": "shadow_marsh",

            "relationship": 0,

            "role": "cult_leader"
        }
    },

    # =========================
    # QUESTS
    # =========================

    "quests": {

        "active": [],

        "completed": [],

        "failed": [],

        "progress": {}
    },

    # =========================
    # STORY MEMORY
    # =========================

    "story_memory": {

        "used_dark_magic": False,

        "dragon_slain": False,

        "merciful": False,

        "ruthless": False,

        "cult_connections": False
    },

    # =========================
    # PLAYER HISTORY
    # =========================

    "history": {

        "choices": [],

        "discovered_lore": [],

        "major_events": []
    },

    # =========================
    # WORLD EVENTS
    # =========================

    "events": {

        "active": [],

        "completed": []
    }
}

# =========================
# PLAYER HELPERS
# =========================

def get_player():

    return world_state["player"]

def add_gold(amount):

    world_state["player"]["gold"] += amount

def remove_gold(amount):

    world_state["player"]["gold"] -= amount

    if world_state["player"]["gold"] < 0:

        world_state["player"]["gold"] = 0

def damage_player(amount):

    defense = world_state[
        "player"
    ]["defense"]

    final_damage = amount - defense

    if final_damage < 1:

        final_damage = 1

    world_state["player"]["hp"] -= final_damage

    if world_state["player"]["hp"] < 0:

        world_state["player"]["hp"] = 0

    print(
        f"\nPlayer takes"
        f" {final_damage} damage!"
    )

def heal_player(amount):

    world_state["player"]["hp"] += amount

    if (

        world_state["player"]["hp"]

        >

        world_state["player"]["max_hp"]

    ):

        world_state["player"]["hp"] = (

            world_state["player"]["max_hp"]
        )

# =========================
# INVENTORY HELPERS
# =========================

def add_item(item_name):

    world_state[
        "player"
    ]["inventory"].append(item_name)

    print(
        f"\nAdded {item_name}"
        f" to inventory."
    )

def remove_item(item_name):

    if (

        item_name

        in

        world_state[
            "player"
        ]["inventory"]

    ):

        world_state[
            "player"
        ]["inventory"].remove(item_name)

        print(
            f"\nRemoved {item_name}"
            f" from inventory."
        )

# =========================
# COMPANION HELPERS
# =========================

def recruit_companion(companion_name):

    if (

        companion_name

        not in

        world_state[
            "companions"
        ]["party"]

    ):

        world_state[
            "companions"
        ]["party"].append(
            companion_name
        )

        world_state[
            "companions"
        ]["recruited"].append(
            companion_name
        )

        world_state[
            "companions"
        ]["relationships"][
            companion_name
        ] = 0

        world_state[
            "companions"
        ]["loyalty"][
            companion_name
        ] = 50

        print(
            f"\n{companion_name}"
            f" joined your party!"
        )

# =========================
# FACTION HELPERS
# =========================

def change_faction_reputation(

    faction_name,
    amount

):

    world_state[
        "factions"
    ][faction_name] += amount

    print(
        f"\nFaction reputation with"
        f" {faction_name}"
        f" changed by {amount}."
    )

# =========================
# QUEST HELPERS
# =========================

def add_active_quest(quest_name):

    if (

        quest_name

        not in

        world_state[
            "quests"
        ]["active"]

    ):

        world_state[
            "quests"
        ]["active"].append(
            quest_name
        )

def complete_quest(quest_name):

    if (

        quest_name

        in

        world_state[
            "quests"
        ]["active"]

    ):

        world_state[
            "quests"
        ]["active"].remove(
            quest_name
        )

    if (

        quest_name

        not in

        world_state[
            "quests"
        ]["completed"]

    ):

        world_state[
            "quests"
        ]["completed"].append(
            quest_name
        )

        print(
            f"\nQuest completed:"
            f" {quest_name}"
        )

def fail_quest(quest_name):

    if (

        quest_name

        not in

        world_state[
            "quests"
        ]["failed"]

    ):

        world_state[
            "quests"
        ]["failed"].append(
            quest_name
        )

# =========================
# STORY MEMORY HELPERS
# =========================

def remember_choice(choice):

    world_state[
        "history"
    ]["choices"].append(choice)

def remember_major_event(event):

    world_state[
        "history"
    ]["major_events"].append(event)

def discover_lore(lore):

    if (

        lore

        not in

        world_state[
            "history"
        ]["discovered_lore"]

    ):

        world_state[
            "history"
        ]["discovered_lore"].append(
            lore
        )

# =========================
# NPC HELPERS
# =========================

def kill_npc(npc_name):

    if npc_name in world_state["npcs"]:

        world_state["npcs"][
            npc_name
        ]["alive"] = False

        print(
            f"\n{npc_name} has died."
        )

def move_npc(

    npc_name,
    new_location

):

    if npc_name in world_state["npcs"]:

        world_state["npcs"][
            npc_name
        ]["location"] = new_location

# =========================
# REGION HELPERS
# =========================

def discover_region(region_name):

    if (

        region_name

        not in

        world_state[
            "regions"
        ]["discovered_regions"]

    ):

        world_state[
            "regions"
        ]["discovered_regions"].append(
            region_name
        )

        print(
            f"\nNew region discovered:"
            f" {region_name}"
        )

def set_current_region(region_name):

    world_state[
        "regions"
    ]["current_region"] = region_name

# =========================
# WORLD EVENT HELPERS
# =========================

def activate_world_event(event_name):

    if (

        event_name

        not in

        world_state[
            "events"
        ]["active"]

    ):

        world_state[
            "events"
        ]["active"].append(
            event_name
        )

        print(
            f"\nWorld Event Started:"
            f" {event_name}"
        )

def complete_world_event(event_name):

    if (

        event_name

        in

        world_state[
            "events"
        ]["active"]

    ):

        world_state[
            "events"
        ]["active"].remove(
            event_name
        )

        world_state[
            "events"
        ]["completed"].append(
            event_name
        )

# =========================
# WORLD EVOLUTION
# =========================

def update_world_state():

    print(
        "\n=== WORLD EVOLUTION ==="
    )

    world_state["time"]["day"] += 1

    print(
        "Day:",
        world_state["time"]["day"]
    )

    chaos = world_state[
        "world_conditions"
    ]["world_chaos"]

    if len(

        world_state[
            "companions"
        ]["party"]

    ) == 0:

        chaos += 1

    if world_state[
        "story_memory"
    ]["used_dark_magic"]:

        chaos += 2

    world_state[
        "world_conditions"
    ]["world_chaos"] = chaos

    print(
        "World Chaos:",
        chaos
    )

    # =========================
    # CULT RISING
    # =========================

    if (

        world_state[
            "factions"
        ]["shadow_cult"]

        >= 40

    ):

        world_state[
            "world_conditions"
        ]["cult_rising"] = True

    # =========================
    # CIVIL WAR
    # =========================

    if (

        world_state[
            "factions"
        ]["kingdom"]

        <= -30

    ):

        world_state[
            "world_conditions"
        ]["civil_war"] = True

    # =========================
    # MAGE REBELLION
    # =========================

    if (

        world_state[
            "factions"
        ]["mages_guild"]

        <= -20

    ):

        world_state[
            "world_conditions"
        ]["mages_rebellion"] = True

# =========================
# WORLD STATE DISPLAY
# =========================

def show_world_state():

    print(
        "\n=== WORLD STATE ==="
    )

    print(
        "Day:",
        world_state[
            "time"
        ]["day"]
    )

    print(
        "Current Region:",
        world_state[
            "regions"
        ]["current_region"]
    )

    print(
        "World Chaos:",
        world_state[
            "world_conditions"
        ]["world_chaos"]
    )

    print(
        "\n=== PLAYER ==="
    )

    player = world_state["player"]

    print(
        "Class:",
        player["class"]
    )

    print(
        "HP:",
        f"{player['hp']}"
        f"/{player['max_hp']}"
    )

    print(
        "Gold:",
        player["gold"]
    )

    print(
        "Level:",
        player["level"]
    )

    print(
        "\n=== COMPANIONS ==="
    )

    for companion in world_state[
        "companions"
    ]["party"]:

        print("•", companion)

    print(
        "\n=== ACTIVE QUESTS ==="
    )

    for quest in world_state[
        "quests"
    ]["active"]:

        print("•", quest)

    print(
        "\n=== ACTIVE WORLD EVENTS ==="
    )

    for event in world_state[
        "events"
    ]["active"]:

        print("•", event)