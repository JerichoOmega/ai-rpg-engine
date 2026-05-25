import random

from player import (
    player
)

from event_bus import (
    emit
)

from llm_bridge import (
    ai_combat_narration,
    ai_narrate
)

# =========================
# COMBAT
# =========================

def combat(

    enemy_name,
    enemy_hp

):

    print(
        "\n=== COMBAT START ==="
    )

    # =========================
    # AI INTRO NARRATION
    # =========================

    combat_state = {

        "enemy_hp": enemy_hp,

        "player_hp": player.hp
    }

    try:

        ai_combat_narration(

            enemy_name,

            combat_state
        )

    except Exception:

        print(
            f"\nA dangerous"
            f" {enemy_name}"
            " approaches."
        )

    # =========================
    # COMBAT LOOP
    # =========================

    while enemy_hp > 0 and player.hp > 0:

        print(
            "\n========================"
        )

        print(
            f"Player HP:"
            f" {player.hp}/"
            f"{player.max_hp}"
        )

        print(
            f"{enemy_name} HP:"
            f" {enemy_hp}"
        )

        print(
            "\n1. Attack"
        )

        print(
            "2. Heavy Attack"
        )

        print(
            "3. Heal"
        )

        action = input(
            "\nChoose: "
        ).strip()

        # =========================
        # ATTACK
        # =========================

        if action == "1":

            damage = random.randint(
                5,
                12
            )

            damage += (
                player.attack_bonus
            )

            enemy_hp -= damage

            print(
                f"\nYou strike the"
                f" {enemy_name}"
                f" for {damage} damage."
            )

        # =========================
        # HEAVY ATTACK
        # =========================

        elif action == "2":

            damage = random.randint(
                10,
                20
            )

            enemy_hp -= damage

            print(
                f"\nHeavy attack hits for"
                f" {damage} damage!"
            )

        # =========================
        # HEAL
        # =========================

        elif action == "3":

            heal = random.randint(
                10,
                20
            )

            player.hp += heal

            player.hp = min(

                player.hp,

                player.max_hp
            )

            print(
                f"\nYou recover"
                f" {heal} HP."
            )

        # =========================
        # INVALID
        # =========================

        else:

            print(
                "\nInvalid action."
            )

            continue

        # =========================
        # ENEMY DEFEATED
        # =========================

        if enemy_hp <= 0:

            print(
                f"\nYou defeated"
                f" {enemy_name}!"
            )

            emit(

                "enemy_killed",

                enemy_name=enemy_name
            )

            # =========================
            # AI AFTERMATH
            # =========================

            try:

                ai_narrate(

                    f"The player defeated"
                    f" {enemy_name}."
                    " Narrate the aftermath."
                )

            except Exception:

                print(
                    "\nThe battle ends."
                )

            return True

        # =========================
        # ENEMY TURN
        # =========================

        enemy_damage = random.randint(
            5,
            15
        )

        player.hp -= enemy_damage

        print(
            f"\nThe {enemy_name}"
            f" hits you for"
            f" {enemy_damage} damage."
        )

        emit(

            "player_damaged",

            amount=enemy_damage
        )

        # =========================
        # LOW HP
        # =========================

        if player.hp <= 25:

            print(
                "\nYou are critically wounded!"
            )

        # =========================
        # PLAYER DEFEATED
        # =========================

        if player.hp <= 0:

            print(
                "\nYou have fallen in battle..."
            )

            emit(
                "player_defeated"
            )

            return False