import random

from world_state import (
    world_state
)

from event_bus import (
    emit
)

from region_manager import (

    REGIONS,

    get_neighboring_regions,

    get_region_weather,

    discover_region
)

from location_manager import (

    LOCATIONS,

    discover_location,

    random_location_discovery,

    set_current_location
)

from encounter_generator import (
    generate_encounter
)

# =========================
# TRAVEL STATE
# =========================

travel_state = {

    "is_traveling": False,

    "travel_days": 0,

    "destination": None
}

# =========================
# START TRAVEL
# =========================

def travel_to_region(

    destination_region

):

    current_region = world_state[
        "regions"
    ]["current_region"]

    # =========================
    # VALIDATE DESTINATION
    # =========================

    neighbors = get_neighboring_regions(
        current_region
    )

    if destination_region not in neighbors:

        print(
            "\nThat region cannot"
            " currently be reached."
        )

        return

    region_data = REGIONS.get(
        destination_region
    )

    if not region_data:

        return

    # =========================
    # BEGIN TRAVEL
    # =========================

    travel_state[
        "is_traveling"
    ] = True

    travel_state[
        "destination"
    ] = destination_region

    difficulty = region_data[
        "travel_difficulty"
    ]

    travel_days = random.randint(
        difficulty,
        difficulty + 2
    )

    travel_state[
        "travel_days"
    ] = travel_days

    print(
        f"\nTraveling to"
        f" {destination_region}..."
    )

    print(
        f"Estimated travel days:"
        f" {travel_days}"
    )

    # =========================
    # TRAVEL LOOP
    # =========================

    for day in range(
        1,
        travel_days + 1
    ):

        print(
            f"\n--- Travel Day {day} ---"
        )

        process_travel_day(
            destination_region
        )

    # =========================
    # ARRIVAL
    # =========================

    complete_travel(
        destination_region
    )

# =========================
# PROCESS TRAVEL DAY
# =========================

def process_travel_day(

    destination_region

):

    weather = get_region_weather(
        destination_region
    )

    print(
        f"\nWeather:"
        f" {weather}"
    )

    roll = random.randint(
        1,
        100
    )

    # =========================
    # ENCOUNTER
    # =========================

    if roll <= 25:

        print(
            "\nYou encounter danger"
            " on the road."
        )

        generate_encounter()

    # =========================
    # DISCOVERY
    # =========================

    elif roll <= 45:

        print(
            "\nYou discover something"
            " interesting."
        )

        random_location_discovery()

    # =========================
    # TRAVEL EVENT
    # =========================

    elif roll <= 70:

        trigger_travel_event()

    # =========================
    # QUIET DAY
    # =========================

    else:

        print(
            "\nThe road remains quiet."
        )

# =========================
# COMPLETE TRAVEL
# =========================

def complete_travel(

    destination_region

):

    world_state[
        "regions"
    ]["current_region"] = (
        destination_region
    )

    discover_region(
        destination_region
    )

    travel_state[
        "is_traveling"
    ] = False

    print(
        f"\nYou arrive in"
        f" {destination_region}."
    )

    emit(

        "region_traveled",

        region_name=destination_region
    )

# =========================
# TRAVEL EVENTS
# =========================

def trigger_travel_event():

    events = [

        "merchant_caravan",

        "traveling_bard",

        "roadside_ruins",

        "strange_footprints",

        "wandering_knight",

        "abandoned_camp",

        "heavy_storm",

        "broken_bridge"
    ]

    event_name = random.choice(
        events
    )

    print(
        f"\nTravel Event:"
        f" {event_name}"
    )

    emit(

        "travel_event",

        event_name=event_name
    )

# =========================
# FAST TRAVEL
# =========================

def fast_travel(

    destination_region

):

    if destination_region not in REGIONS:

        return

    region = REGIONS[
        destination_region
    ]

    if not region[
        "discovered"
    ]:

        print(
            "\nYou have not discovered"
            " that region yet."
        )

        return

    world_state[
        "regions"
    ]["current_region"] = (
        destination_region
    )

    print(
        f"\nFast traveled to"
        f" {destination_region}."
    )

# =========================
# TRAVEL TO LOCATION
# =========================

def travel_to_location(

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

    location_region = location[
        "region"
    ]

    current_region = world_state[
        "regions"
    ]["current_region"]

    # =========================
    # TRAVEL TO REGION FIRST
    # =========================

    if location_region != current_region:

        travel_to_region(
            location_region
        )

    # =========================
    # ARRIVE AT LOCATION
    # =========================

    discover_location(
        location_name
    )

    set_current_location(
        location_name
    )

    print(
        f"\nArrived at"
        f" {location_name}."
    )

# =========================
# RANDOM ROAD ENCOUNTER
# =========================

def random_road_encounter():

    encounters = [

        "wolves",

        "bandits",

        "shadow_beast",

        "cult_patrol",

        "undead",

        "rogue_mage"
    ]

    encounter = random.choice(
        encounters
    )

    print(
        f"\nRoad Encounter:"
        f" {encounter}"
    )

# =========================
# WEATHER TRAVEL EFFECTS
# =========================

def apply_weather_effects(

    weather

):

    if weather == "storm":

        print(
            "\nTravel slows due"
            " to heavy storms."
        )

    elif weather == "foggy":

        print(
            "\nVisibility becomes poor."
        )

    elif weather == "ash_storm":

        print(
            "\nAsh fills the air,"
            " making travel dangerous."
        )

    elif weather == "arcane_storms":

        print(
            "\nUnstable magical energy"
            " crackles around you."
        )

# =========================
# SHOW CURRENT LOCATION
# =========================

def show_current_position():

    region = world_state[
        "regions"
    ]["current_region"]

    location = world_state[
        "regions"
    ].get(
        "current_location"
    )

    print(
        "\n=== CURRENT POSITION ==="
    )

    print(
        "Region:",
        region
    )

    print(
        "Location:",
        location
    )