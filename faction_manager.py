from world_state import (
    world_state,
    activate_world_event
)

from event_bus import (
    subscribe,
    emit
)

# =========================
# FACTION THRESHOLDS
# =========================

FACTION_STATES = {

    "ally": 75,

    "friendly": 25,

    "neutral": 0,

    "hostile": -25,

    "enemy": -75
}

# =========================
# GET FACTION STATUS
# =========================

def get_faction_status(

    faction_name

):

    reputation = world_state[
        "factions"
    ].get(

        faction_name,
        0
    )

    if reputation >= 75:

        return "ally"

    elif reputation >= 25:

        return "friendly"

    elif reputation > -25:

        return "neutral"

    elif reputation > -75:

        return "hostile"

    return "enemy"

# =========================
# CHANGE REPUTATION
# =========================

def change_reputation(

    faction_name,
    amount

):

    world_state[
        "factions"
    ][faction_name] += amount

    reputation = world_state[
        "factions"
    ][faction_name]

    print(
        f"\nFaction reputation with"
        f" {faction_name}"
        f" changed by {amount}."
    )

    print(
        "New Reputation:",
        reputation
    )

    evaluate_faction_state(
        faction_name
    )

# =========================
# EVALUATE FACTION STATE
# =========================

def evaluate_faction_state(

    faction_name

):

    status = get_faction_status(
        faction_name
    )

    print(
        f"\n{faction_name}"
        f" status is now:"
        f" {status}"
    )

    # =========================
    # HOSTILE
    # =========================

    if status == "hostile":

        emit(

            "faction_hostile",

            faction=faction_name
        )

    # =========================
    # ENEMY
    # =========================

    elif status == "enemy":

        emit(

            "faction_enemy",

            faction=faction_name
        )

    # =========================
    # ALLY
    # =========================

    elif status == "ally":

        emit(

            "faction_ally",

            faction=faction_name
        )

# =========================
# FACTION EVENTS
# =========================

def on_faction_hostile(

    event_data

):

    faction = event_data.get(
        "faction"
    )

    print(
        f"\n{faction}"
        " has become hostile!"
    )

    if faction == "shadow_cult":

        activate_world_event(
            "Cult Assassins"
        )

        print(
            "\nCult assassins begin"
            " hunting the player."
        )

def on_faction_enemy(

    event_data

):

    faction = event_data.get(
        "faction"
    )

    print(
        f"\n{faction}"
        " now considers you"
        " an enemy."
    )

    if faction == "kingdom":

        activate_world_event(
            "Kingdom Bounty"
        )

        print(
            "\nA bounty has been placed"
            " on your head."
        )

def on_faction_ally(

    event_data

):

    faction = event_data.get(
        "faction"
    )

    print(
        f"\n{faction}"
        " now views you"
        " as a trusted ally."
    )

    if faction == "mages_guild":

        print(
            "\nRare magical knowledge"
            " becomes available."
        )

# =========================
# REGION CONTROL
# =========================

def change_region_control(

    region_name,
    faction_name

):

    world_state[
        "regions"
    ]["faction_control"][
        region_name
    ] = faction_name

    print(
        f"\n{faction_name}"
        f" now controls"
        f" {region_name}."
    )

    emit(

        "region_control_changed",

        region=region_name,

        faction=faction_name
    )

# =========================
# FACTION WAR
# =========================

def start_faction_war(

    faction_one,
    faction_two

):

    print(
        f"\nWAR:"
        f" {faction_one}"
        f" vs"
        f" {faction_two}"
    )

    activate_world_event(

        f"{faction_one}_vs_"
        f"{faction_two}_war"
    )

    emit(

        "faction_war_started",

        faction_one=faction_one,

        faction_two=faction_two
    )

# =========================
# WORLD CHAOS EFFECTS
# =========================

def evaluate_world_chaos():

    chaos = world_state[
        "world_conditions"
    ]["world_chaos"]

    if chaos >= 25:

        print(
            "\nThe world grows unstable."
        )

    if chaos >= 50:

        print(
            "\nCivilization begins collapsing."
        )

        emit(
            "world_collapse"
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

    if enemy_name == "hidden cult":

        change_reputation(
            "shadow_cult",
            -5
        )

        change_reputation(
            "kingdom",
            2
        )

def on_quest_completed(

    event_data

):

    quest_name = event_data.get(
        "quest_name"
    )

    if quest_name == "Cult Hunt":

        change_reputation(
            "kingdom",
            10
        )

        change_reputation(
            "shadow_cult",
            -10
        )

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "enemy_killed",
    on_enemy_killed
)

subscribe(
    "quest_completed",
    on_quest_completed
)

subscribe(
    "faction_hostile",
    on_faction_hostile
)

subscribe(
    "faction_enemy",
    on_faction_enemy
)

subscribe(
    "faction_ally",
    on_faction_ally
)