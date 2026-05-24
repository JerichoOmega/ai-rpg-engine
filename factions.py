# =========================
# FACTION SYSTEM
# =========================

factions = {

    "kingdom": 0,

    "mages_guild": 0,

    "shadow_cult": 0
}

# =========================
# MODIFY REPUTATION
# =========================

def modify_reputation(
    factions,
    faction_name,
    amount
):

    factions[faction_name] += amount

    print(
        "\nReputation with",
        faction_name,
        "changed by",
        amount
    )

    print(
        "Current Reputation:",
        factions[faction_name]
    )

    return factions

# =========================
# CHECK FACTION STATUS
# =========================

def check_faction_status(
    factions,
    faction_name
):

    reputation = factions[faction_name]

    if reputation >= 50:

        return "ally"

    elif reputation <= -50:

        return "enemy"

    else:

        return "neutral"