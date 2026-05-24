import random

from factions import modify_reputation

from memory import update_memory

from companions import (
    change_loyalty,
    companion_reaction
)

# =========================
# RANDOM EVENT SYSTEM
# =========================

def random_event(
    player_hp,
    player_gold,
    inventory
):

    event_roll = random.randint(1, 4)

    # =========================
    # TREASURE EVENT
    # =========================

    if event_roll == 1:

        gold_found = random.randint(
            10,
            25
        )

        player_gold += gold_found

        print(
            "\n=== RANDOM EVENT ==="
        )

        print(
            "You discover a hidden treasure chest!"
        )

        print(
            "You gain",
            gold_found,
            "gold!"
        )

    # =========================
    # HEALING FOUNTAIN
    # =========================

    elif event_roll == 2:

        heal_amount = random.randint(
            10,
            20
        )

        player_hp += heal_amount

        print(
            "\n=== RANDOM EVENT ==="
        )

        print(
            "You discover a healing fountain."
        )

        print(
            "Recovered",
            heal_amount,
            "HP!"
        )

    # =========================
    # POTION FIND
    # =========================

    elif event_roll == 3:

        inventory.append(
            "Healing Potion"
        )

        print(
            "\n=== RANDOM EVENT ==="
        )

        print(
            "You find a Healing Potion!"
        )

    # =========================
    # AMBUSH EVENT
    # =========================

    elif event_roll == 4:

        damage = random.randint(
            5,
            15
        )

        player_hp -= damage

        print(
            "\n=== RANDOM EVENT ==="
        )

        print(
            "Bandits ambush you in the dark!"
        )

        print(
            "You take",
            damage,
            "damage!"
        )

    return (
        player_hp,
        player_gold,
        inventory
    )

# =========================
# CHOICE EVENT SYSTEM
# =========================

def choice_event(
    factions,
    story_memory
):

    print(
        "\n=== MORAL CHOICE ==="
    )

    print(
        "\nYou discover a wounded cultist"
        " begging for mercy."
    )

    print("\n1. Spare them")

    print("2. Execute them")

    print("3. Recruit them")

    choice = input("> ")

    # =========================
    # SPARE
    # =========================

    if choice == "1":

        print(
            "\nYou spare the cultist."
        )

        story_memory = update_memory(
            story_memory,
            "spared_cultist"
        )

        factions = modify_reputation(
            factions,
            "kingdom",
            5
        )

        factions = modify_reputation(
            factions,
            "shadow_cult",
            -5
        )

        # =========================
        # COMPANION REACTIONS
        # =========================

        change_loyalty(
            "Mira",
            5
        )

        print(
            "\nMira approves of your mercy."
        )

    # =========================
    # EXECUTE
    # =========================

    elif choice == "2":

        print(
            "\nYou execute the cultist."
        )

        story_memory = update_memory(
            story_memory,
            "executed_cultist"
        )

        factions = modify_reputation(
            factions,
            "kingdom",
            10
        )

        factions = modify_reputation(
            factions,
            "shadow_cult",
            -15
        )

        # =========================
        # COMPANION REACTIONS
        # =========================

        change_loyalty(
            "Kael",
            5
        )

        print(
            "\nKael respects your ruthlessness."
        )

        change_loyalty(
            "Mira",
            -5
        )

        print(
            "\nMira disapproves of the execution."
        )

    # =========================
    # RECRUIT
    # =========================

    elif choice == "3":

        print(
            "\nThe cultist joins your cause."
        )

        story_memory = update_memory(
            story_memory,
            "recruited_cultist"
        )

        story_memory = update_memory(
            story_memory,
            "joined_shadow_cult"
        )

        factions = modify_reputation(
            factions,
            "shadow_cult",
            15
        )

        factions = modify_reputation(
            factions,
            "kingdom",
            -10
        )

        # =========================
        # COMPANION REACTIONS
        # =========================

        change_loyalty(
            "Mira",
            -10
        )

        print(
            "\nMira distrusts your alliance"
            " with the cult."
        )

        change_loyalty(
            "Kael",
            10
        )

        print(
            "\nKael fully supports your"
            " darker ambitions."
        )

    else:

        print(
            "\nInvalid choice."
        )

    # =========================
    # GLOBAL COMPANION REACTIONS
    # =========================

    companion_reaction(
        story_memory
    )

    return (
        factions,
        story_memory
    )