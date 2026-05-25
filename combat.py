import random

from world_state import (
    world_state,
    damage_player
)

from inventory import (
    use_potion,
    show_inventory
)

from companions import (
    companion_attack
)

from event_bus import (
    emit
)

from utils import (
    is_attack,
    is_skills,
    is_heal,
    is_inventory,
    is_run
)

def combat(

    enemy_name,
    enemy_hp

):

    player = world_state["player"]

    companions = world_state[
        "companions"
    ]["party"]

    boss_phase = 1

    while (

        player["hp"] > 0

        and

        enemy_hp > 0

    ):

        print(
            "\n===================="
        )

        print(
            "Your HP:",
            str(player["hp"])
            + "/"
            + str(player["max_hp"])
        )

        print(
            enemy_name + " HP:",
            enemy_hp
        )

        action = input(

            "\nChoose action "
            "(attack / skills / heal / inventory / run): "

        )

        if is_attack(action):

            damage = random.randint(
                6,
                12
            )

            damage += player[
                "attack_bonus"
            ]

            damage += player[
                "weapon_bonus"
            ]

            print(
                "\nYou deal",
                damage,
                "damage!"
            )

            enemy_hp -= damage

        elif is_heal(action):

            use_potion()

        elif is_inventory(action):

            show_inventory()

        elif is_run(action):

            print(
                "\nYou escaped!"
            )

            return False

        if enemy_hp > 0:

            enemy_hp = companion_attack(

                companions,
                enemy_hp

            )

        if enemy_hp <= 0:

            print(
                "\nThe enemy collapses!"
            )

            emit(

                "enemy_killed",

                enemy_name=enemy_name
            )

            return True

        enemy_damage = random.randint(
            6,
            14
        )

        damage_player(
            enemy_damage
        )

    if player["hp"] <= 0:

        print(
            "\nYou were defeated..."
        )

        return False

    return True