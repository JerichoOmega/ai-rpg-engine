import random

# =========================
# RANDOM EVENTS
# =========================

events = [

    "You discover a hidden treasure chest.",
    "A wandering merchant appears.",
    "You step into a dangerous trap.",
    "An old traveler gives you advice.",
    "You find an ancient magical shrine."
]

# =========================
# RANDOM EVENT SYSTEM
# =========================

def random_event(player_hp, player_gold, inventory):

    event = random.choice(events)

    print("\n=== RANDOM EVENT ===")
    print(event)

    # TREASURE

    if "treasure" in event:

        gold_found = random.randint(10, 25)

        player_gold += gold_found

        print("You found", gold_found, "gold!")

    # MERCHANT

    elif "merchant" in event:

        print("The merchant gives you a Healing Potion.")

        inventory.append("Healing Potion")

    # TRAP

    elif "trap" in event:

        trap_damage = random.randint(5, 12)

        player_hp -= trap_damage

        print("The trap deals", trap_damage, "damage!")

    # TRAVELER

    elif "traveler" in event:

        print("The traveler warns you about future dangers.")

    # SHRINE

    elif "shrine" in event:

        print("Mystical energy restores your strength.")

        player_hp += 15

    return player_hp, player_gold, inventory