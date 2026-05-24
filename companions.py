# =========================
# COMPANION SYSTEM
# =========================

companions = {

    "Mira": {
        "class": "mage",
        "hp": 80,
        "damage": 15,
        "role": "support",
        "ability": "arcane_shield",
        "loyalty": 50
    },

    "Thorn": {
        "class": "warrior",
        "hp": 120,
        "damage": 10,
        "role": "tank",
        "ability": "shield_block",
        "loyalty": 50
    },

    "Kael": {
        "class": "rogue",
        "hp": 90,
        "damage": 18,
        "role": "assassin",
        "ability": "poison_blade",
        "loyalty": 50
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
# CHANGE LOYALTY
# =========================

def change_loyalty(
    companion_name,
    amount
):

    companions[
        companion_name
    ]["loyalty"] += amount

    # =========================
    # LOYALTY LIMITS
    # =========================

    if companions[
        companion_name
    ]["loyalty"] > 100:

        companions[
            companion_name
        ]["loyalty"] = 100

    elif companions[
        companion_name
    ]["loyalty"] < 0:

        companions[
            companion_name
        ]["loyalty"] = 0

    print(
        "\n" + companion_name,
        "loyalty changed by",
        amount
    )

    print(
        "Current Loyalty:",
        companions[
            companion_name
        ]["loyalty"]
    )

# =========================
# LOYALTY STATUS
# =========================

def loyalty_status(
    companion_name
):

    loyalty = companions[
        companion_name
    ]["loyalty"]

    if loyalty >= 80:

        return "Devoted"

    elif loyalty <= 20:

        return "Disloyal"

    else:

        return "Neutral"

# =========================
# SHOW PARTY
# =========================

def show_party(party):

    print("\n=== PARTY ===")

    if len(party) == 0:

        print(
            "No companions recruited."
        )

    else:

        for member in party:

            status = loyalty_status(
                member
            )

            print(
                member,
                "-",
                companions[member]["class"],
                "| Role:",
                companions[member]["role"],
                "| Loyalty:",
                companions[member]["loyalty"],
                "| Status:",
                status
            )

# =========================
# COMPANION ABILITIES
# =========================

def companion_ability(
    member,
    player_defense,
    active_effects
):

    ability = companions[
        member
    ]["ability"]

    # =========================
    # MIRA — ARCANE SHIELD
    # =========================

    if ability == "arcane_shield":

        print(
            "\nMira casts Arcane Shield!"
        )

        print(
            "Your defense increases by 2!"
        )

        player_defense += 2

    # =========================
    # THORN — SHIELD BLOCK
    # =========================

    elif ability == "shield_block":

        print(
            "\nThorn steps forward to protect you!"
        )

        print(
            "Incoming damage will be reduced!"
        )

        player_defense += 4

    # =========================
    # KAEL — POISON BLADE
    # =========================

    elif ability == "poison_blade":

        print(
            "\nKael coats his blades with poison!"
        )

        active_effects.append({

            "effect": "poison",

            "duration": 3
        })

    return (
        player_defense,
        active_effects
    )

# =========================
# COMPANION REACTIONS
# =========================

def companion_reaction(
    story_memory
):

    print(
        "\n=== COMPANION REACTIONS ==="
    )

    # =========================
    # SHADOW CULT
    # =========================

    if story_memory[
        "joined_shadow_cult"
    ]:

        print(
            "\nMira looks uneasy around"
            " the cult influence."
        )

        change_loyalty(
            "Mira",
            -10
        )

        print(
            "\nKael grins approvingly."
        )

        change_loyalty(
            "Kael",
            10
        )

    # =========================
    # DRAGON SLAYER
    # =========================

    if story_memory[
        "dragon_slain"
    ]:

        print(
            "\nThorn respects your victory"
            " over the dragon."
        )

        change_loyalty(
            "Thorn",
            10
        )

    # =========================
    # SPARED CULTIST
    # =========================

    if story_memory[
        "spared_cultist"
    ]:

        print(
            "\nMira approves of your mercy."
        )

        change_loyalty(
            "Mira",
            5
        )

    # =========================
    # EXECUTED CULTIST
    # =========================

    if story_memory[
        "executed_cultist"
    ]:

        print(
            "\nKael respects your ruthlessness."
        )

        change_loyalty(
            "Kael",
            5
        )

        print(
            "\nMira disapproves of the execution."
        )

        change_loyalty(
            "Mira",
            -5
        )

# =========================
# REMOVE COMPANION
# =========================

def remove_companion(
    party,
    companion_name
):

    if companion_name in party:

        party.remove(
            companion_name
        )

        print(
            "\n" + companion_name,
            "has left the party!"
        )

    return party

# =========================
# LOYALTY EVENTS
# =========================

def loyalty_event(
    party,
    story_memory,
    factions
):

    # =========================
    # MIRA LEAVES
    # =========================

    if "Mira" in party:

        if companions[
            "Mira"
        ]["loyalty"] <= 20:

            if story_memory[
                "joined_shadow_cult"
            ]:

                print(
                    "\nMira can no longer tolerate"
                    " your dark choices."
                )

                party = remove_companion(
                    party,
                    "Mira"
                )

    # =========================
    # THORN MORALITY CONFLICT
    # =========================

    if "Thorn" in party:

        if factions[
            "kingdom"
        ] <= -50:

            print(
                "\nThorn questions your actions"
                " against the kingdom."
            )

            change_loyalty(
                "Thorn",
                -10
            )

            if companions[
                "Thorn"
            ]["loyalty"] <= 20:

                print(
                    "\nThorn abandons your cause."
                )

                party = remove_companion(
                    party,
                    "Thorn"
                )

    # =========================
    # KAEL DEVOTION BONUS
    # =========================

    if "Kael" in party:

        if companions[
            "Kael"
        ]["loyalty"] >= 80:

            print(
                "\nKael is fiercely loyal."
            )

            print(
                "His critical strikes grow deadlier."
            )

    return party