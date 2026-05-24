import random

from utils import (
    is_spare,
    is_execute,
    is_recruit
)

# =========================
# RANDOM EVENTS
# =========================

def random_event(

    player_hp,
    player_gold,
    inventory

):

    print(
        "\n=== RANDOM EVENT ==="
    )

    event_roll = random.randint(
        1,
        4
    )

    if event_roll == 1:

        print(
            "You find a Healing Potion!"
        )

        inventory.append(
            "Healing Potion"
        )

    elif event_roll == 2:

        gold_found = random.randint(
            10,
            25
        )

        player_gold += gold_found

        print(
            "You discover",
            gold_found,
            "gold!"
        )

    elif event_roll == 3:

        damage = random.randint(
            5,
            10
        )

        player_hp -= damage

        print(
            "Bandits ambush you"
            " in the dark!"
        )

        print(
            "You take",
            damage,
            "damage!"
        )

    else:

        print(
            "The road remains quiet."
        )

    return (
        player_hp,
        player_gold,
        inventory
    )

# =========================
# MORAL CHOICE EVENTS
# =========================

def choice_event(

    factions,
    story_memory

):

    print(
        "\n=== MORAL CHOICE ==="
    )

    print(
        "\nYou discover a wounded"
        " cultist begging for mercy."
    )

    print("1. Spare them")
    print("2. Execute them")
    print("3. Recruit them")

    choice = input("> ")

    # =========================
    # SPARE
    # =========================

    if is_spare(choice):

        print(
            "\nYou spare the cultist."
        )

        factions[
            "kingdom"
        ] += 5

        story_memory[
            "spared_cultist"
        ] = True

    # =========================
    # EXECUTE
    # =========================

    elif is_execute(choice):

        print(
            "\nYou execute the cultist."
        )

        factions[
            "shadow_cult"
        ] -= 10

        story_memory[
            "executed_cultist"
        ] = True

    # =========================
    # RECRUIT
    # =========================

    elif is_recruit(choice):

        print(
            "\nThe cultist secretly"
            " joins your cause."
        )

        factions[
            "shadow_cult"
        ] += 10

        story_memory[
            "recruited_cultist"
        ] = True

    else:

        print(
            "\nInvalid choice."
        )

    return (
        factions,
        story_memory
    )