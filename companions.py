# =========================
# COMPANION SYSTEM
# =========================

companions = {

    "Mira": {
        "class": "mage",
        "hp": 80,
        "damage": 15
    },

    "Thorn": {
        "class": "warrior",
        "hp": 120,
        "damage": 10
    },

    "Kael": {
        "class": "rogue",
        "hp": 90,
        "damage": 18
    }
}

# =========================
# RECRUIT COMPANION
# =========================

def recruit_companion(
    party,
    companion_name
):

    if companion_name not in party:

        party.append(companion_name)

        print(
            "\n" + companion_name,
            "joins your adventure!"
        )

    else:

        print(
            "\n" + companion_name,
            "is already in your party."
        )

    return party

# =========================
# SHOW PARTY
# =========================

def show_party(party):

    print("\n=== PARTY ===")

    if len(party) == 0:

        print("No companions recruited.")

    else:

        for member in party:

            print(
                member,
                "-",
                companions[member]["class"]
            )