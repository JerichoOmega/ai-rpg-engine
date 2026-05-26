from world_state import (
    world_state,
    activate_world_event
)

from event_bus import (
    subscribe,
    emit
)

# =========================
# FACTION DATABASE
# =========================

FACTIONS = {

    "kingdom": {

        "type": "nation",

        "military_power": 85,

        "economy": 80,

        "influence": 90,

        "aggression": 35,

        "corruption": 10,

        "allies": [

            "mages_guild"
        ],

        "enemies": [

            "shadow_cult"
        ]
    },

    "shadow_cult": {

        "type": "cult",

        "military_power": 55,

        "economy": 40,

        "influence": 60,

        "aggression": 80,

        "corruption": 95,

        "allies": [],

        "enemies": [

            "kingdom",

            "mages_guild"
        ]
    },

    "mages_guild": {

        "type": "guild",

        "military_power": 45,

        "economy": 90,

        "influence": 75,

        "aggression": 15,

        "corruption": 5,

        "allies": [

            "kingdom"
        ],

        "enemies": [

            "shadow_cult"
        ]
    }
}

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
# GET FACTION DATA
# =========================

def get_faction_data(

    faction_name

):

    return FACTIONS.get(
        faction_name
    )

# =========================
# CHANGE REPUTATION
# =========================

def change_reputation(

    faction_name,
    amount

):

    if faction_name not in world_state[
        "factions"
    ]:

        world_state[
            "factions"
        ][faction_name] = 0

    world_state[
        "factions"
    ][faction_name] += amount

    reputation = world_state[
        "factions"
    ][faction_name]

    reputation = max(
        -100,
        min(
            reputation,
            100
        )
    )

    world_state[
        "factions"
    ][faction_name] = reputation

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

    if status == "hostile":

        emit(

            "faction_hostile",

            faction=faction_name
        )

    elif status == "enemy":

        emit(

            "faction_enemy",

            faction=faction_name
        )

    elif status == "ally":

        emit(

            "faction_ally",

            faction=faction_name
        )

# =========================
# FACTION RELATIONS
# =========================

def are_factions_allied(

    faction_one,
    faction_two

):

    faction = FACTIONS.get(
        faction_one
    )

    if not faction:

        return False

    return faction_two in faction[
        "allies"
    ]

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

    faction_one_data = FACTIONS.get(
        faction_one
    )

    faction_two_data = FACTIONS.get(
        faction_two
    )

    if faction_one_data:

        if faction_two not in faction_one_data[
            "enemies"
        ]:

            faction_one_data[
                "enemies"
            ].append(
                faction_two
            )

    if faction_two_data:

        if faction_one not in faction_two_data[
            "enemies"
        ]:

            faction_two_data[
                "enemies"
            ].append(
                faction_one
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
# GET REGION CONTROLLER
# =========================

def get_region_controller(

    region_name

):

    return world_state[
        "regions"
    ]["faction_control"].get(
        region_name
    )

# =========================
# FACTION POWER GROWTH
# =========================

def evolve_factions():

    for faction_name, faction in FACTIONS.items():

        # =========================
        # CORRUPT FACTIONS EXPAND
        # =========================

        if faction[
            "corruption"
        ] >= 75:

            faction[
                "influence"
            ] += 2

            faction[
                "aggression"
            ] += 1

        # =========================
        # STRONG ECONOMIES
        # =========================

        if faction[
            "economy"
        ] >= 75:

            faction[
                "military_power"
            ] += 1

        # =========================
        # CAP VALUES
        # =========================

        faction[
            "military_power"
        ] = min(

            faction[
                "military_power"
            ],

            100
        )

        faction[
            "influence"
        ] = min(

            faction[
                "influence"
            ],

            100
        )

# =========================
# FACTION TAKEOVER
# =========================

def attempt_faction_takeover(

    region_name,
    invading_faction

):

    current_controller = (
        get_region_controller(
            region_name
        )
    )

    if not current_controller:

        change_region_control(

            region_name,

            invading_faction
        )

        return

    attacker = FACTIONS.get(
        invading_faction
    )

    defender = FACTIONS.get(
        current_controller
    )

    if not attacker or not defender:

        return

    attack_power = (

        attacker[
            "military_power"
        ]

        +

        attacker[
            "influence"
        ]
    )

    defense_power = (

        defender[
            "military_power"
        ]

        +

        defender[
            "influence"
        ]
    )

    if attack_power > defense_power:

        print(
            f"\n{invading_faction}"
            f" has conquered"
            f" {region_name}!"
        )

        change_region_control(

            region_name,

            invading_faction
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

    if chaos >= 75:

        print(
            "\nTotal war spreads"
            " across the world."
        )

        emit(
            "global_war"
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
# EVENT REACTIONS
# =========================

def on_enemy_killed(

    event_data

):

    enemy_name = event_data.get(
        "enemy_name"
    )

    if enemy_name == "cultist":

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

    quest = event_data.get(
        "quest"
    )

    if not quest:

        return

    if quest.get(
        "type"
    ) == "faction":

        faction = quest.get(
            "faction"
        )

        if faction:

            change_reputation(
                faction,
                10
            )

# =========================
# SHOW FACTIONS
# =========================

def show_factions():

    print(
        "\n=== FACTIONS ==="
    )

    for faction_name, faction in FACTIONS.items():

        print(
            f"\n{faction_name}"
        )

        print(
            f"Military:"
            f" {faction['military_power']}"
        )

        print(
            f"Economy:"
            f" {faction['economy']}"
        )

        print(
            f"Influence:"
            f" {faction['influence']}"
        )

        print(
            f"Corruption:"
            f" {faction['corruption']}"
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