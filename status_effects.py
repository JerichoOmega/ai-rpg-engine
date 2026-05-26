# =========================
# STATUS EFFECT DATABASE
# =========================

STATUS_EFFECTS = {

    "burn": {

        "damage": 5,

        "stackable": False
    },

    "poison": {

        "damage": 3,

        "stackable": True
    },

    "bleed": {

        "damage": 4,

        "stackable": True
    }
}

# =========================
# APPLY STATUS EFFECT
# =========================

def add_status_effect(

    active_effects,

    effect_name,

    duration

):

    effect_data = STATUS_EFFECTS.get(
        effect_name
    )

    if not effect_data:

        print(
            "\nUnknown status effect."
        )

        return active_effects

    # =========================
    # PREVENT DUPLICATE EFFECTS
    # =========================

    if not effect_data["stackable"]:

        for effect in active_effects:

            if effect["effect"] == effect_name:

                print(
                    f"\n{effect_name}"
                    " is already active."
                )

                return active_effects

    # =========================
    # APPLY EFFECT
    # =========================

    active_effects.append({

        "effect": effect_name,

        "duration": duration
    })

    print(
        f"\nStatus Applied:"
        f" {effect_name}"
    )

    return active_effects

# =========================
# PROCESS STATUS EFFECTS
# =========================

def process_status_effects(

    entity,

    active_effects

):

    remaining_effects = []

    for effect_data in active_effects:

        effect_name = effect_data[
            "effect"
        ]

        duration = effect_data[
            "duration"
        ]

        effect = STATUS_EFFECTS.get(
            effect_name
        )

        if not effect:

            continue

        # =========================
        # APPLY DAMAGE
        # =========================

        damage = effect.get(
            "damage",
            0
        )

        if damage > 0:

            entity.hp -= damage

            print(
                f"\n{effect_name.title()}"
                f" deals {damage}"
                " damage!"
            )

        # =========================
        # REDUCE DURATION
        # =========================

        duration -= 1

        # =========================
        # KEEP EFFECT ACTIVE
        # =========================

        if duration > 0:

            remaining_effects.append({

                "effect": effect_name,

                "duration": duration
            })

        else:

            print(
                f"\n{effect_name}"
                " has worn off."
            )

    return remaining_effects

# =========================
# REMOVE STATUS EFFECT
# =========================

def remove_status_effect(

    active_effects,

    effect_name

):

    updated_effects = [

        effect

        for effect in active_effects

        if effect["effect"] != effect_name
    ]

    print(
        f"\nRemoved status:"
        f" {effect_name}"
    )

    return updated_effects

# =========================
# CHECK STATUS
# =========================

def has_status_effect(

    active_effects,

    effect_name

):

    for effect in active_effects:

        if effect["effect"] == effect_name:

            return True

    return False

# =========================
# SHOW STATUS EFFECTS
# =========================

def show_status_effects(

    active_effects

):

    print(
        "\n=== STATUS EFFECTS ==="
    )

    if not active_effects:

        print(
            "\nNo active effects."
        )

        return

    for effect in active_effects:

        print(
            f"\n{effect['effect']}"
        )

        print(
            f"Duration:"
            f" {effect['duration']}"
        )