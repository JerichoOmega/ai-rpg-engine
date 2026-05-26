import random

from settlement_manager import (
    SETTLEMENTS,
    change_settlement_prosperity
)

from region_manager import (
    REGIONS
)

from event_bus import (
    emit
)

# =========================
# GLOBAL ECONOMY
# =========================

economy_state = {

    "inflation": 1.0,

    "global_stability": 75,

    "scarcity": 20
}

# =========================
# ITEM MARKET VALUES
# =========================

MARKET_VALUES = {

    "food": 10,

    "iron": 25,

    "gold": 100,

    "herbs": 15,

    "mana_crystals": 80,

    "obsidian": 45,

    "weapons": 60,

    "armor": 75
}

# =========================
# TRADE ROUTES
# =========================

TRADE_ROUTES = [

    {

        "from": "royal_city",

        "to": "merchant_district",

        "risk": 15,

        "active": True
    },

    {

        "from": "merchant_district",

        "to": "murkwater_village",

        "risk": 45,

        "active": True
    }
]

# =========================
# GET ITEM PRICE
# =========================

def get_item_price(

    item_name,
    settlement_name=None

):

    base_price = MARKET_VALUES.get(
        item_name,
        10
    )

    price = base_price

    # =========================
    # GLOBAL INFLATION
    # =========================

    price *= economy_state[
        "inflation"
    ]

    # =========================
    # SETTLEMENT MODIFIER
    # =========================

    if settlement_name:

        settlement = SETTLEMENTS.get(
            settlement_name
        )

        if settlement:

            prosperity = settlement[
                "prosperity"
            ]

            if prosperity <= 25:

                price *= 1.5

            elif prosperity >= 75:

                price *= 0.8

    return round(
        price,
        2
    )

# =========================
# CHANGE INFLATION
# =========================

def change_inflation(

    amount

):

    economy_state[
        "inflation"
    ] += amount

    economy_state[
        "inflation"
    ] = max(

        0.5,

        min(
            economy_state[
                "inflation"
            ],
            3.0
        )
    )

    print(
        f"\nInflation changed to"
        f" {economy_state['inflation']}."
    )

# =========================
# CHANGE GLOBAL STABILITY
# =========================

def change_global_stability(

    amount

):

    economy_state[
        "global_stability"
    ] += amount

    economy_state[
        "global_stability"
    ] = max(

        0,

        min(
            economy_state[
                "global_stability"
            ],
            100
        )
    )

# =========================
# TRADE ROUTE EVENT
# =========================

def trigger_trade_route_event():

    if not TRADE_ROUTES:

        return

    route = random.choice(
        TRADE_ROUTES
    )

    events = [

        "bandit_attack",

        "merchant_boom",

        "trade_dispute",

        "caravan_destroyed",

        "new_trade_agreement"
    ]

    event_name = random.choice(
        events
    )

    print(
        f"\nTrade Route Event:"
        f" {event_name}"
    )

    # =========================
    # ECONOMIC EFFECTS
    # =========================

    if event_name == "bandit_attack":

        change_inflation(
            0.1
        )

    elif event_name == "merchant_boom":

        change_global_stability(
            5
        )

    elif event_name == "caravan_destroyed":

        change_inflation(
            0.2
        )

    emit(

        "trade_route_event",

        route=route,

        event_name=event_name
    )

# =========================
# ECONOMY EVOLUTION
# =========================

def evolve_economy():

    # =========================
    # GLOBAL STABILITY EFFECTS
    # =========================

    if economy_state[
        "global_stability"
    ] <= 25:

        change_inflation(
            0.1
        )

    elif economy_state[
        "global_stability"
    ] >= 75:

        change_inflation(
            -0.05
        )

    # =========================
    # RANDOM TRADE EVENTS
    # =========================

    roll = random.randint(
        1,
        100
    )

    if roll <= 35:

        trigger_trade_route_event()

# =========================
# REGION ECONOMY UPDATE
# =========================

def update_region_economy():

    for region_name, region in REGIONS.items():

        # =========================
        # CORRUPTED REGIONS
        # =========================

        if region["corrupted"]:

            economy_state[
                "scarcity"
            ] += 1

        # =========================
        # HIGH PROSPERITY
        # =========================

        if region["prosperity"] >= 75:

            change_global_stability(
                1
            )

# =========================
# SHOW MARKET PRICES
# =========================

def show_market_prices(

    settlement_name=None

):

    print(
        "\n=== MARKET PRICES ==="
    )

    for item, value in MARKET_VALUES.items():

        price = get_item_price(

            item,

            settlement_name
        )

        print(
            f"\n{item}: {price} gold"
        )

# =========================
# SHOW TRADE ROUTES
# =========================

def show_trade_routes():

    print(
        "\n=== TRADE ROUTES ==="
    )

    for route in TRADE_ROUTES:

        print(
            f"\n{route['from']}"
            f" -> "
            f"{route['to']}"
        )

        print(
            f"Risk:"
            f" {route['risk']}"
        )

        print(
            f"Active:"
            f" {route['active']}"
        )

# =========================
# ADD TRADE ROUTE
# =========================

def add_trade_route(

    from_settlement,
    to_settlement,
    risk=25

):

    TRADE_ROUTES.append({

        "from": from_settlement,

        "to": to_settlement,

        "risk": risk,

        "active": True
    })

    print(
        f"\nTrade route established:"
        f" {from_settlement}"
        f" -> "
        f"{to_settlement}"
    )

# =========================
# REMOVE TRADE ROUTE
# =========================

def disable_trade_route(

    from_settlement,
    to_settlement

):

    for route in TRADE_ROUTES:

        if (

            route["from"] == from_settlement

            and

            route["to"] == to_settlement

        ):

            route["active"] = False

            print(
                f"\nTrade route disabled:"
                f" {from_settlement}"
                f" -> "
                f"{to_settlement}"
            )

# =========================
# ECONOMIC CRISIS
# =========================

def trigger_economic_crisis():

    print(
        "\n=== ECONOMIC CRISIS ==="
    )

    change_inflation(
        0.5
    )

    change_global_stability(
        -20
    )

    for settlement_name in SETTLEMENTS:

        change_settlement_prosperity(

            settlement_name,

            -10
        )

    emit(
        "economic_crisis"
    )

# =========================
# ECONOMY SUMMARY
# =========================

def show_economy_summary():

    print(
        "\n=== ECONOMY SUMMARY ==="
    )

    print(
        "Inflation:",
        economy_state[
            "inflation"
        ]
    )

    print(
        "Global Stability:",
        economy_state[
            "global_stability"
        ]
    )

    print(
        "Scarcity:",
        economy_state[
            "scarcity"
        ]
    )