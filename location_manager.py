import random

from world_state import (
    world_state
)

from event_bus import (
    emit
)

from region_manager import (
    REGIONS,
    get_region_data
)

# =========================
# LOCATION DATABASE
# =========================

LOCATIONS = {

    "royal_city": {

        "display_name": "Royal City",

        "region": "kingdom_capital",

        "type": "city",

        "danger": 5,

        "discovered": True,

        "population": 9000,

        "services": [

            "shop",
            "blacksmith",
            "tavern",
            "healer"
        ],

        "story_tags": [

            "politics",
            "nobility",
            "corruption"
        ],

        "active_events": []
    },

    "merchant_district": {

        "display_name": "Merchant District",

        "region": "kingdom_capital",

        "type": "district",

        "danger": 10,

        "discovered": True,

        "population": 3000,

        "services": [

            "market",
            "inn",
            "fence"
        ],

        "story_tags": [

            "trade",
            "crime",
            "economy"
        ],

        "active_events": []
    },

    "murkwater_village": {

        "display_name": "Murkwater Village",

        "region": "shadow_marsh",

        "type": "village",

        "danger": 40,

        "discovered": False,

        "population": 400,

        "services": [

            "tavern",
            "herbalist"
        ],

        "story_tags": [

            "horror",
            "madness",
            "survival"
        ],

        "active_events": []
    },

    "cult_hideout": {

        "display_name": "Cult Hideout",

        "region": "shadow_marsh",

        "type": "dungeon",

        "danger": 75,

        "discovered": False,

        "population": 60,

        "services": [],

        "story_tags": [

            "cult",
            "rituals",
            "darkness"
        ],

        "active_events": []
    },

    "fallen_tower": {

        "display_name": "Fallen Tower",

        "region": "arcane_ruins",

        "type": "ruin",

        "danger": 65,

        "discovered": False,

        "population": 0,

        "services": [],

        "story_tags": [

            "magic",
            "mystery",
            "forbidden_knowledge"
        ],

        "active_events": []
    },

    "forgotten_forge": {

        "display_name": "Forgotten Forge",

        "region": "ashen_wastes",

        "type": "dungeon",

        "danger": 85,

        "discovered": False,

        "population": 0,

        "services": [],

        "story_tags": [

            "revenge",
            "fire",
            "desolation"
        ],

        "active_events": []
    }
}

# =========================
# GET LOCATION DATA
# =========================

def get_location_data(

    location_name

):

    return LOCATIONS.get(
        location_name
    )

# =========================
# SHOW LOCATION
# =========================

def show_location(

    location_name

):

    location = LOCATIONS.get(
        location_name
    )

    if not location:

        print(
            "\nUnknown location."
        )

        return

    print(
        "\n=== LOCATION INFO ==="
    )

    print(
        "Name:",
        location[
            "display_name"
        ]
    )

    print(
        "Type:",
        location[
            "type"
        ]
    )

    print(
        "Region:",
        location[
            "region"
        ]
    )

    print(
        "Danger:",
        location[
            "danger"
        ]
    )

    print(
        "Population:",
        location[
            "population"
        ]
    )

    print(
        "Services:",
        ", ".join(
            location[
                "services"
            ]
        )
    )

# =========================
# DISCOVER LOCATION
# =========================

def discover_location(

    location_name

):

    location = LOCATIONS.get(
        location_name
    )

    if not location:

        return

    if location["discovered"]:

        return

    location[
        "discovered"
    ] = True

    print(
        f"\nNew location discovered:"
        f" {location_name}"
    )

    emit(

        "location_discovered",

        location_name=location_name
    )

# =========================
# GET REGION LOCATIONS
# =========================

def get_locations_in_region(

    region_name

):

    locations = []

    for name, data in LOCATIONS.items():

        if data["region"] == region_name:

            locations.append(
                name
            )

    return locations

# =========================
# RANDOM LOCATION EVENT
# =========================

def random_location_event(

    location_name

):

    location = LOCATIONS.get(
        location_name
    )

    if not location:

        return

    possible_events = [

        "mysterious_stranger",

        "bandit_raid",

        "festival",

        "cult_activity",

        "merchant_arrival",

        "monster_attack"
    ]

    event_name = random.choice(
        possible_events
    )

    location[
        "active_events"
    ].append(
        event_name
    )

    print(
        f"\nEvent at"
        f" {location_name}:"
        f" {event_name}"
    )

    emit(

        "location_event",

        location_name=location_name,

        event_name=event_name
    )

# =========================
# LOCATION DANGER UPDATE
# =========================

def change_location_danger(

    location_name,
    amount

):

    location = LOCATIONS.get(
        location_name
    )

    if not location:

        return

    location[
        "danger"
    ] += amount

    location[
        "danger"
    ] = max(

        0,

        min(
            location[
                "danger"
            ],
            100
        )
    )

    print(
        f"\nDanger in"
        f" {location_name}"
        f" changed by"
        f" {amount}."
    )

# =========================
# RANDOM DISCOVERY
# =========================

def random_location_discovery():

    undiscovered = [

        name

        for name, data

        in LOCATIONS.items()

        if not data[
            "discovered"
        ]
    ]

    if not undiscovered:

        return

    discovered = random.choice(
        undiscovered
    )

    discover_location(
        discovered
    )

# =========================
# LOCATION EVOLUTION
# =========================

def evolve_locations():

    for name, location in LOCATIONS.items():

        region_data = get_region_data(
            location["region"]
        )

        if not region_data:

            continue

        # =========================
        # CORRUPTED REGIONS
        # =========================

        if region_data["corrupted"]:

            change_location_danger(
                name,
                1
            )

        # =========================
        # STABLE REGIONS
        # =========================

        elif region_data["stability"] >= 75:

            change_location_danger(
                name,
                -1
            )

# =========================
# CURRENT LOCATION
# =========================

def set_current_location(

    location_name

):

    if location_name not in LOCATIONS:

        return

    world_state[
        "regions"
    ]["current_location"] = (
        location_name
    )

    print(
        f"\nCurrent location:"
        f" {location_name}"
    )

# =========================
# GET CURRENT LOCATION
# =========================

def get_current_location():

    location_name = world_state[
        "regions"
    ].get(
        "current_location"
    )

    return LOCATIONS.get(
        location_name
    )