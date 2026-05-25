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

        "danger": 10,

        "faction": "kingdom",

        "discovered": True,

        "events": [],

        "corrupted": False
    },

    "shadow_marsh": {

        "danger": 45,

        "faction": "shadow_cult",

        "discovered": False,

        "events": [],

        "corrupted": True
    },

    "arcane_ruins": {

        "danger": 60,

        "faction": "mages_guild",

        "discovered": False,

        "events": [],

        "corrupted": False
    },

    "ashen_wastes": {

        "danger": 80,

        "faction": "none",

        "discovered": False,

        "events": [],

        "corrupted": True
    }
}

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
        region_name
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

    region = REGIONS[region_name]

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