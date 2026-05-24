# =========================
# APPLY STATUS EFFECT
# =========================

def add_status_effect(active_effects, effect_name, duration):

    active_effects.append({

        "effect": effect_name,
        "duration": duration
    })

    print("\nStatus Applied:", effect_name)

    return active_effects


# =========================
# PROCESS STATUS EFFECTS
# =========================

def process_status_effects(player_hp, active_effects):

    remaining_effects = []

    for effect_data in active_effects:

        effect = effect_data["effect"]

        duration = effect_data["duration"]

        # =========================
        # BURN
        # =========================

        if effect == "burn":

            burn_damage = 5

            player_hp -= burn_damage

            print("\nBurn deals", burn_damage, "damage!")

        # =========================
        # POISON
        # =========================

        elif effect == "poison":

            poison_damage = 3

            player_hp -= poison_damage

            print("\nPoison deals", poison_damage, "damage!")

        # =========================
        # REDUCE DURATION
        # =========================

        duration -= 1

        # =========================
        # KEEP EFFECT ACTIVE
        # =========================

        if duration > 0:

            remaining_effects.append({

                "effect": effect,
                "duration": duration
            })

        else:

            print(effect, "has worn off.")

    return player_hp, remaining_effects