import random

from world_state import (
    world_state,
    discover_lore,
    activate_world_event
)

from event_bus import (
    subscribe,
    emit
)

# =========================
# REGION DATABASE
# =========================

REGIONS = {

    "kingdom_capital": {

        "display_name": "Kingdom Capital",

        "biome": "urban",

        "danger": 10,

        "stability": 85,

        "prosperity": 90,

        "travel_difficulty": 1,

        "faction": "kingdom",

        "population": 12000,

        "weather": "clear",

        "resources": [

            "gold",
            "food",
            "iron"
        ],

        "story_themes": [

            "politics",
            "corruption",
            "nobility"
        ],

        "neighboring_regions": [

            "shadow_marsh",
            "arcane_ruins"
        ],

        "settlements": [

            "royal_city",
            "merchant_district",
            "castle_blackstone"
        ],

        "active_conflicts": [],

        "events": [],

        "discovered": True,

        "corrupted": False
    },

    "shadow_marsh": {

        "display_name": "Shadow Marsh",

        "biome": "swamp",

        "danger": 45,

        "stability": 40,

        "prosperity": 20,

        "travel_difficulty": 6,

        "faction": "shadow_cult",

        "population": 800,

        "weather": "foggy",

        "resources": [

            "herbs",
            "alchemy",
            "swamp_meat"
        ],

        "story_themes": [

            "horror",
            "madness",
            "corruption"
        ],

        "neighboring_regions": [

            "kingdom_capital",
            "ashen_wastes"
        ],

        "settlements": [

            "murkwater_village",
            "cult_hideout"
        ],

        "active_conflicts": [

            "cult_activity"
        ],

        "events": [],

        "discovered": False,

        "corrupted": True
    },

    "arcane_ruins": {

        "display_name": "Arcane Ruins",

        "biome": "magical_ruins",

        "danger": 60,

        "stability": 30,

        "prosperity": 50,

        "travel_difficulty": 5,

        "faction": "mages_guild",

        "population": 300,

        "weather": "arcane_storms",

        "resources": [

            "mana_crystals",
            "ancient_books"
        ],

        "story_themes": [

            "mystery",
            "forbidden_knowledge",
            "magic"
        ],

        "neighboring_regions": [

            "kingdom_capital",
            "ashen_wastes"
        ],

        "settlements": [

            "fallen_tower",
            "crystal_archive"
        ],

        "active_conflicts": [

            "mana_instability"
        ],

        "events": [],

        "discovered": False,

        "corrupted": False
    },

    "ashen_wastes": {

        "display_name": "Ashen Wastes",

        "biome": "volcanic",

        "danger": 80,

        "stability": 10,

        "prosperity": 5,

        "travel_difficulty": 9,

        "faction": "none",

        "population": 50,

        "weather": "ash_storm",

        "resources": [

            "obsidian",
            "sulfur"
        ],

        "story_themes": [

            "survival",
            "revenge",
            "desolation"
        ],

        "neighboring_regions": [

            "shadow_marsh",
            "arcane_ruins"
        ],

        "settlements": [

            "burned_outpost",
            "forgotten_forge"
        ],

        "active_conflicts": [

            "monster_raids"
        ],

        "events": [],

        "discovered": False,

        "corrupted": True
    }
}

# =========================
# GET REGION DATA
# =========================

def get_region_data(

    region_name

):

    return REGIONS.get(
        region_name
    )

# =========================
# GET CURRENT REGION
# =========================

def get_current_region():

    current_region = world_state[
        "regions"
    ]["current_region"]

    return REGIONS.get(
        current_region
    )

# =========================
# GET REGION THEMES
# =========================

def get_region_story_themes(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return []

    return region.get(
        "story_themes",
        []
    )

# =========================
# GET NEIGHBORING REGIONS
# =========================

def get_neighboring_regions(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return []

    return region.get(
        "neighboring_regions",
        []
    )

# =========================
# GET REGION SETTLEMENTS
# =========================

def get_region_settlements(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return []

    return region.get(
        "settlements",
        []
    )

# =========================
# GET REGION WEATHER
# =========================

def get_region_weather(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return "unknown"

    return region.get(
        "weather",
        "clear"
    )

# =========================
# CHANGE REGION WEATHER
# =========================

def change_region_weather(

    region_name,
    new_weather

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    old_weather = region[
        "weather"
    ]

    region[
        "weather"
    ] = new_weather

    print(
        f"\nWeather in"
        f" {region_name}"
        f" changed from"
        f" {old_weather}"
        f" to"
        f" {new_weather}."
    )

# =========================
# CHANGE STABILITY
# =========================

def change_region_stability(

    region_name,
    amount

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    region[
        "stability"
    ] += amount

    region[
        "stability"
    ] = max(

        0,

        min(
            region[
                "stability"
            ],
            100
        )
    )

    print(
        f"\nStability in"
        f" {region_name}"
        f" changed by"
        f" {amount}."
    )

# =========================
# CHANGE PROSPERITY
# =========================

def change_region_prosperity(

    region_name,
    amount

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    region[
        "prosperity"
    ] += amount

    region[
        "prosperity"
    ] = max(

        0,

        min(
            region[
                "prosperity"
            ],
            100
        )
    )

    print(
        f"\nProsperity in"
        f" {region_name}"
        f" changed by"
        f" {amount}."
    )

# =========================
# RANDOM WEATHER UPDATE
# =========================

def random_weather_update():

    possible_weather = [

        "clear",

        "rain",

        "storm",

        "foggy",

        "ash_storm",

        "arcane_storms"
    ]

    region_name = random.choice(
        list(REGIONS.keys())
    )

    weather = random.choice(
        possible_weather
    )

    change_region_weather(

        region_name,

        weather
    )

# =========================
# REGION EVOLUTION
# =========================

def evolve_region(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    # =========================
    # CORRUPTED REGIONS DECAY
    # =========================

    if region["corrupted"]:

        change_region_stability(

            region_name,

            -2
        )

        change_region_prosperity(

            region_name,

            -1
        )

    # =========================
    # PEACEFUL REGIONS RECOVER
    # =========================

    elif region["danger"] <= 20:

        change_region_stability(

            region_name,

            1
        )

        change_region_prosperity(

            region_name,

            1
        )

# =========================
# EVOLVE ALL REGIONS
# =========================

def evolve_world_regions():

    for region_name in REGIONS:

        evolve_region(
            region_name
        )

# =========================
# SHOW REGION
# =========================

def show_region(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        print(
            "\nUnknown region."
        )

        return

    print(
        "\n=== REGION INFO ==="
    )

    print(
        "Region:",
        region[
            "display_name"
        ]
    )

    print(
        "Biome:",
        region["biome"]
    )

    print(
        "Danger:",
        region["danger"]
    )

    print(
        "Faction:",
        region["faction"]
    )

    print(
        "Weather:",
        region["weather"]
    )

    print(
        "Stability:",
        region["stability"]
    )

    print(
        "Prosperity:",
        region["prosperity"]
    )

    print(
        "Corrupted:",
        region["corrupted"]
    )

# =========================
# DISCOVER REGION
# =========================

def discover_region(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    if region["discovered"]:

        return

    region["discovered"] = True

    print(
        f"\nNew region discovered:"
        f" {region_name}"
    )

    emit(

        "region_discovered",

        region_name=region_name
    )

# =========================
# CHANGE DANGER
# =========================

def change_danger(

    region_name,
    amount

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    region["danger"] += amount

    region["danger"] = max(
        0,
        min(region["danger"], 100)
    )

    print(
        f"\nDanger in"
        f" {region_name}"
        f" changed by"
        f" {amount}."
    )

    evaluate_region(
        region_name
    )

# =========================
# EVALUATE REGION
# =========================

def evaluate_region(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    danger = region["danger"]

    # =========================
    # HIGH DANGER
    # =========================

    if danger >= 75:

        print(
            f"\n{region_name}"
            " has become extremely dangerous."
        )

        activate_world_event(
            f"{region_name}_crisis"
        )

        emit(

            "region_crisis",

            region_name=region_name
        )

    # =========================
    # LOW DANGER
    # =========================

    elif danger <= 15:

        print(
            f"\n{region_name}"
            " has become relatively peaceful."
        )

# =========================
# REGION EVENTS
# =========================

def add_region_event(

    region_name,
    event_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    region["events"].append(
        event_name
    )

    print(
        f"\nEvent in"
        f" {region_name}:"
        f" {event_name}"
    )

# =========================
# CHANGE CONTROL
# =========================

def change_region_control(

    region_name,
    faction_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    old_faction = region["faction"]

    region["faction"] = faction_name

    print(
        f"\n{region_name}"
        f" changed control from"
        f" {old_faction}"
        f" to"
        f" {faction_name}."
    )

    emit(

        "region_control_changed",

        region_name=region_name,

        faction_name=faction_name
    )

# =========================
# CORRUPTION
# =========================

def corrupt_region(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    region["corrupted"] = True

    print(
        f"\nDark corruption spreads through"
        f" {region_name}."
    )

    emit(

        "region_corrupted",

        region_name=region_name
    )

# =========================
# RANDOM REGION EVENT
# =========================

def random_region_event():

    region_name = random.choice(
        list(REGIONS.keys())
    )

    possible_events = [

        "bandit_attack",

        "monster_sighting",

        "trade_boom",

        "magical_storm",

        "undead_rising"
    ]

    event_name = random.choice(
        possible_events
    )

    add_region_event(
        region_name,
        event_name
    )

# =========================
# EVENT REACTIONS
# =========================

def on_enemy_killed(

    event_data

):

    enemy_name = event_data.get(
        "enemy_name"
    )

    current_region = world_state[
        "regions"
    ]["current_region"]

    if enemy_name == "hidden cult":

        change_danger(
            current_region,
            -3
        )

    elif enemy_name == "shadow beast":

        change_danger(
            current_region,
            -2
        )

def on_world_collapse(

    event_data

):

    print(
        "\nThe world spirals further into chaos."
    )

    for region_name in REGIONS:

        change_danger(
            region_name,
            10
        )

def on_faction_war_started(

    event_data

):

    faction_one = event_data.get(
        "faction_one"
    )

    faction_two = event_data.get(
        "faction_two"
    )

    print(
        f"\nWar spreads between"
        f" {faction_one}"
        f" and"
        f" {faction_two}."
    )

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "enemy_killed",
    on_enemy_killed
)

subscribe(
    "world_collapse",
    on_world_collapse
)

subscribe(
    "faction_war_started",
    on_faction_war_started
)