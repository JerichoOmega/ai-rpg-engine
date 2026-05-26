import random

from location_manager import (
    LOCATIONS
)

from region_manager import (
    REGIONS
)

from event_bus import (
    emit
)

# =========================
# SETTLEMENT DATABASE
# =========================

SETTLEMENTS = {

    "royal_city": {

        "prosperity": 90,

        "security": 85,

        "population": 9000,

        "faction": "kingdom",

        "services": [

            "blacksmith",

            "market",

            "inn",

            "tavern",

            "healer"
        ],

        "active_events": [],

        "rumors": [

            "A noble house plots rebellion.",

            "Bandits raid caravans nearby.",

            "The king grows increasingly paranoid."
        ]
    },

    "murkwater_village": {

        "prosperity": 25,

        "security": 30,

        "population": 400,

        "faction": "shadow_cult",

        "services": [

            "tavern",

            "herbalist"
        ],

        "active_events": [],

        "rumors": [

            "Villagers vanish at night.",

            "Something lurks beneath the swamp.",

            "Cult rituals echo through the marsh."
        ]
    },

    "merchant_district": {

        "prosperity": 80,

        "security": 60,

        "population": 3000,

        "faction": "merchant_guild",

        "services": [

            "market",

            "inn",

            "fence"
        ],

        "active_events": [],

        "rumors": [

            "Smugglers control the docks.",

            "A merchant prince disappeared.",

            "Prices continue rising rapidly."
        ]
    }
}

# =========================
# GET SETTLEMENT DATA
# =========================

def get_settlement_data(

    settlement_name

):

    return SETTLEMENTS.get(
        settlement_name
    )

# =========================
# SHOW SETTLEMENT
# =========================

def show_settlement(

    settlement_name

):

    settlement = SETTLEMENTS.get(
        settlement_name
    )

    if not settlement:

        print(
            "\nUnknown settlement."
        )

        return

    print(
        "\n=== SETTLEMENT INFO ==="
    )

    print(
        "Settlement:",
        settlement_name
    )

    print(
        "Population:",
        settlement[
            "population"
        ]
    )

    print(
        "Prosperity:",
        settlement[
            "prosperity"
        ]
    )

    print(
        "Security:",
        settlement[
            "security"
        ]
    )

    print(
        "Faction:",
        settlement[
            "faction"
        ]
    )

    print(
        "Services:"
    )

    for service in settlement[
        "services"
    ]:

        print(
            f"- {service}"
        )

# =========================
# RANDOM RUMOR
# =========================

def get_random_rumor(

    settlement_name

):

    settlement = SETTLEMENTS.get(
        settlement_name
    )

    if not settlement:

        return None

    rumors = settlement.get(
        "rumors",
        []
    )

    if not rumors:

        return None

    rumor = random.choice(
        rumors
    )

    print(
        f"\nRumor:"
        f" {rumor}"
    )

    return rumor

# =========================
# ADD SETTLEMENT EVENT
# =========================

def add_settlement_event(

    settlement_name,
    event_name

):

    settlement = SETTLEMENTS.get(
        settlement_name
    )

    if not settlement:

        return

    settlement[
        "active_events"
    ].append(
        event_name
    )

    print(
        f"\nSettlement Event:"
        f" {event_name}"
    )

    emit(

        "settlement_event",

        settlement_name=settlement_name,

        event_name=event_name
    )

# =========================
# CHANGE PROSPERITY
# =========================

def change_settlement_prosperity(

    settlement_name,
    amount

):

    settlement = SETTLEMENTS.get(
        settlement_name
    )

    if not settlement:

        return

    settlement[
        "prosperity"
    ] += amount

    settlement[
        "prosperity"
    ] = max(

        0,

        min(
            settlement[
                "prosperity"
            ],
            100
        )
    )

    print(
        f"\nSettlement prosperity changed"
        f" by {amount}."
    )

# =========================
# CHANGE SECURITY
# =========================

def change_settlement_security(

    settlement_name,
    amount

):

    settlement = SETTLEMENTS.get(
        settlement_name
    )

    if not settlement:

        return

    settlement[
        "security"
    ] += amount

    settlement[
        "security"
    ] = max(

        0,

        min(
            settlement[
                "security"
            ],
            100
        )
    )

    print(
        f"\nSettlement security changed"
        f" by {amount}."
    )

# =========================
# RANDOM SETTLEMENT EVENT
# =========================

def random_settlement_event(

    settlement_name

):

    events = [

        "festival",

        "riot",

        "plague",

        "merchant_arrival",

        "bandit_attack",

        "public_execution",

        "strange_disappearances"
    ]

    event_name = random.choice(
        events
    )

    add_settlement_event(

        settlement_name,

        event_name
    )

# =========================
# EVOLVE SETTLEMENT
# =========================

def evolve_settlement(

    settlement_name

):

    settlement = SETTLEMENTS.get(
        settlement_name
    )

    if not settlement:

        return

    # =========================
    # LOW SECURITY
    # =========================

    if settlement[
        "security"
    ] <= 25:

        change_settlement_prosperity(

            settlement_name,

            -2
        )

    # =========================
    # HIGH PROSPERITY
    # =========================

    if settlement[
        "prosperity"
    ] >= 75:

        change_settlement_security(

            settlement_name,

            1
        )

# =========================
# EVOLVE ALL SETTLEMENTS
# =========================

def evolve_settlements():

    for settlement_name in SETTLEMENTS:

        evolve_settlement(
            settlement_name
        )

# =========================
# SERVICE CHECK
# =========================

def settlement_has_service(

    settlement_name,
    service_name

):

    settlement = SETTLEMENTS.get(
        settlement_name
    )

    if not settlement:

        return False

    return service_name in settlement[
        "services"
    ]

# =========================
# SHOW SERVICES
# =========================

def show_settlement_services(

    settlement_name

):

    settlement = SETTLEMENTS.get(
        settlement_name
    )

    if not settlement:

        return

    print(
        "\n=== SERVICES ==="
    )

    for service in settlement[
        "services"
    ]:

        print(
            f"- {service}"
        )

# =========================
# SETTLEMENT SUMMARY
# =========================

def show_all_settlements():

    print(
        "\n=== SETTLEMENTS ==="
    )

    for settlement_name in SETTLEMENTS:

        settlement = SETTLEMENTS[
            settlement_name
        ]

        print(
            f"\n{settlement_name}"
        )

        print(
            f"Prosperity:"
            f" {settlement['prosperity']}"
        )

        print(
            f"Security:"
            f" {settlement['security']}"
        )

        print(
            f"Faction:"
            f" {settlement['faction']}"
        )