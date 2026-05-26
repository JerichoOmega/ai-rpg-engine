from region_manager import (
    REGIONS,
    get_neighboring_regions
)

from location_manager import (
    LOCATIONS
)

from world_state import (
    world_state
)

# =========================
# WORLD MAP DATA
# =========================

WORLD_MAP = {

    "regions": REGIONS,

    "locations": LOCATIONS
}

# =========================
# SHOW WORLD MAP
# =========================

def show_world_map():

    print(
        "\n=== WORLD MAP ==="
    )

    current_region = world_state[
        "regions"
    ]["current_region"]

    for region_name, region_data in REGIONS.items():

        discovered = region_data[
            "discovered"
        ]

        if not discovered:

            continue

        marker = " "

        if region_name == current_region:

            marker = "*"

        print(
            f"\n[{marker}] "
            f"{region_data['display_name']}"
        )

        print(
            f"Biome:"
            f" {region_data['biome']}"
        )

        print(
            f"Danger:"
            f" {region_data['danger']}"
        )

        print(
            f"Faction:"
            f" {region_data['faction']}"
        )

        print(
            f"Weather:"
            f" {region_data['weather']}"
        )

# =========================
# SHOW REGION CONNECTIONS
# =========================

def show_region_connections(

    region_name

):

    region = REGIONS.get(
        region_name
    )

    if not region:

        return

    print(
        f"\n=== CONNECTIONS:"
        f" {region['display_name']} ==="
    )

    neighbors = get_neighboring_regions(
        region_name
    )

    if not neighbors:

        print(
            "\nNo known neighboring regions."
        )

        return

    for neighbor in neighbors:

        neighbor_data = REGIONS.get(
            neighbor
        )

        if not neighbor_data:

            continue

        print(
            f"\n- {neighbor_data['display_name']}"
        )

# =========================
# SHOW REGION LOCATIONS
# =========================

def show_region_locations(

    region_name

):

    print(
        f"\n=== LOCATIONS:"
        f" {region_name} ==="
    )

    found = False

    for location_name, location_data in LOCATIONS.items():

        if location_data["region"] != region_name:

            continue

        if not location_data[
            "discovered"
        ]:

            continue

        found = True

        print(
            f"\n- {location_data['display_name']}"
        )

        print(
            f"Type:"
            f" {location_data['type']}"
        )

        print(
            f"Danger:"
            f" {location_data['danger']}"
        )

    if not found:

        print(
            "\nNo discovered locations."
        )

# =========================
# GET DISCOVERED REGIONS
# =========================

def get_discovered_regions():

    discovered = []

    for region_name, region_data in REGIONS.items():

        if region_data["discovered"]:

            discovered.append(
                region_name
            )

    return discovered

# =========================
# GET DISCOVERED LOCATIONS
# =========================

def get_discovered_locations():

    discovered = []

    for location_name, location_data in LOCATIONS.items():

        if location_data["discovered"]:

            discovered.append(
                location_name
            )

    return discovered

# =========================
# REGION ACCESS CHECK
# =========================

def can_travel_to_region(

    current_region,
    destination_region

):

    neighbors = get_neighboring_regions(
        current_region
    )

    return destination_region in neighbors

# =========================
# GET REGION DANGER RANKING
# =========================

def get_most_dangerous_regions():

    ranked = sorted(

        REGIONS.items(),

        key=lambda item:

            item[1]["danger"],

        reverse=True
    )

    return ranked

# =========================
# SHOW DANGER MAP
# =========================

def show_danger_map():

    print(
        "\n=== DANGER MAP ==="
    )

    ranked = get_most_dangerous_regions()

    for region_name, region_data in ranked:

        if not region_data[
            "discovered"
        ]:

            continue

        print(
            f"\n{region_data['display_name']}"
        )

        print(
            f"Danger:"
            f" {region_data['danger']}"
        )

# =========================
# SHOW FACTION CONTROL MAP
# =========================

def show_faction_map():

    print(
        "\n=== FACTION CONTROL ==="
    )

    for region_name, region_data in REGIONS.items():

        if not region_data[
            "discovered"
        ]:

            continue

        print(
            f"\n{region_data['display_name']}"
        )

        print(
            f"Controlled By:"
            f" {region_data['faction']}"
        )

# =========================
# SHOW WEATHER MAP
# =========================

def show_weather_map():

    print(
        "\n=== WEATHER MAP ==="
    )

    for region_name, region_data in REGIONS.items():

        if not region_data[
            "discovered"
        ]:

            continue

        print(
            f"\n{region_data['display_name']}"
        )

        print(
            f"Weather:"
            f" {region_data['weather']}"
        )

# =========================
# WORLD SUMMARY
# =========================

def show_world_summary():

    discovered_regions = (
        len(
            get_discovered_regions()
        )
    )

    discovered_locations = (
        len(
            get_discovered_locations()
        )
    )

    print(
        "\n=== WORLD SUMMARY ==="
    )

    print(
        "Discovered Regions:",
        discovered_regions
    )

    print(
        "Discovered Locations:",
        discovered_locations
    )

    print(
        "Total Regions:",
        len(REGIONS)
    )

    print(
        "Total Locations:",
        len(LOCATIONS)
    )

# =========================
# MAP PROGRESSION
# =========================

def calculate_world_completion():

    total_regions = len(REGIONS)

    discovered_regions = len(
        get_discovered_regions()
    )

    completion = (

        discovered_regions
        /
        total_regions

    ) * 100

    return round(
        completion,
        2
    )

# =========================
# SHOW WORLD COMPLETION
# =========================

def show_world_completion():

    completion = (
        calculate_world_completion()
    )

    print(
        "\n=== WORLD EXPLORATION ==="
    )

    print(
        f"World Completion:"
        f" {completion}%"
    )