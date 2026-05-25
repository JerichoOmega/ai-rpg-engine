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

from utils import (
    is_attack,
    is_skills,
    is_heal,
    is_inventory,
    is_run
)

# =========================
# COMBAT SYSTEM
# =========================

def combat(

    enemy_name,
    enemy_hp

):

    player = world_state["player"]

    companions = world_state[
        "companions"
    ]["party"]

    boss_phase = 1

    battle_cry_bonus = 0

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

            player["resource_name"]
            + ":",

            str(player["resource"])
            + " / "
            + str(
                player["max_resource"]
            )
        )

        print(
            "Defense:",
            player["defense"]
        )

        print(
            "Dodge:",
            str(
                player["dodge"]
            ) + "%"
        )

        print(
            enemy_name + " HP:",
            enemy_hp
        )

        print(
            "Equipped Weapon:",
            player[
                "equipped_weapon"
            ]
        )

        print(
            "\nParty:",
            companions
        )

        action = input(

            "\nChoose action "
            "(attack / skills / heal / inventory / run): "

        )

        # =========================
        # ATTACK
        # =========================

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

            damage += battle_cry_bonus

            crit_roll = random.randint(
                1,
                100
            )

            if crit_roll <= 10:

                damage *= 2

                print(
                    "\nCRITICAL HIT!"
                )

            print(
                "\nYou attack with",
                player[
                    "equipped_weapon"
                ] + "!"
            )

            print(
                "You deal",
                damage,
                "damage!"
            )

            enemy_hp -= damage

        # =========================
        # SKILLS
        # =========================

        elif is_skills(action):

            print(
                "\n=== SKILLS ==="
            )

            # =========================
            # WARRIOR
            # =========================

            if player["class"] == "Warrior":

                print(
                    "• Shield Slam (20 stamina)"
                )

                print(
                    "• Battle Cry (15 stamina)"
                )

            # =========================
            # MAGE
            # =========================

            elif player["class"] == "Mage":

                print(
                    "• Fireball (25 mana)"
                )

                print(
                    "• Arcane Burst (35 mana)"
                )

            # =========================
            # ROGUE
            # =========================

            elif player["class"] == "Rogue":

                print(
                    "• Backstab (20 stamina)"
                )

                print(
                    "• Shadow Strike (30 stamina)"
                )

            skill_choice = input(
                "\nUse skill: "
            ).strip().lower()

            # =========================
            # WARRIOR SKILLS
            # =========================

            if player["class"] == "Warrior":

                if skill_choice == "shield slam":

                    if player["resource"] >= 20:

                        player["resource"] -= 20

                        damage = random.randint(
                            18,
                            28
                        )

                        enemy_hp -= damage

                        print(
                            "\nYou slam the enemy"
                            " with your shield!"
                        )

                        print(
                            "Damage:",
                            damage
                        )

                    else:

                        print(
                            "\nNot enough stamina!"
                        )

                elif skill_choice == "battle cry":

                    if player["resource"] >= 15:

                        player["resource"] -= 15

                        battle_cry_bonus += 5

                        print(
                            "\nYour battle cry"
                            " empowers you!"
                        )

                    else:

                        print(
                            "\nNot enough stamina!"
                        )

            # =========================
            # MAGE SKILLS
            # =========================

            elif player["class"] == "Mage":

                if skill_choice == "fireball":

                    if player["resource"] >= 25:

                        player["resource"] -= 25

                        damage = random.randint(
                            25,
                            40
                        )

                        enemy_hp -= damage

                        print(
                            "\nA blazing fireball"
                            " explodes!"
                        )

                        print(
                            "Damage:",
                            damage
                        )

                    else:

                        print(
                            "\nNot enough mana!"
                        )

                elif skill_choice == "arcane burst":

                    if player["resource"] >= 35:

                        player["resource"] -= 35

                        damage = random.randint(
                            35,
                            55
                        )

                        enemy_hp -= damage

                        print(
                            "\nArcane energy erupts!"
                        )

                        print(
                            "Damage:",
                            damage
                        )

                    else:

                        print(
                            "\nNot enough mana!"
                        )

            # =========================
            # ROGUE SKILLS
            # =========================

            elif player["class"] == "Rogue":

                if skill_choice == "backstab":

                    if player["resource"] >= 20:

                        player["resource"] -= 20

                        damage = random.randint(
                            22,
                            36
                        )

                        enemy_hp -= damage

                        print(
                            "\nYou strike from"
                            " the shadows!"
                        )

                        print(
                            "Damage:",
                            damage
                        )

                    else:

                        print(
                            "\nNot enough stamina!"
                        )

                elif skill_choice == "shadow strike":

                    if player["resource"] >= 30:

                        player["resource"] -= 30

                        damage = random.randint(
                            32,
                            48
                        )

                        enemy_hp -= damage

                        print(
                            "\nA devastating"
                            " shadow attack lands!"
                        )

                        print(
                            "Damage:",
                            damage
                        )

                    else:

                        print(
                            "\nNot enough stamina!"
                        )

        # =========================
        # HEAL
        # =========================

        elif is_heal(action):

            use_potion()

        # =========================
        # INVENTORY
        # =========================

        elif is_inventory(action):

            show_inventory()

        # =========================
        # RUN
        # =========================

        elif is_run(action):

            escape_roll = random.randint(
                1,
                100
            )

            if escape_roll <= 50:

                print(
                    "\nYou escaped!"
                )

                return False

            else:

                print(
                    "\nEscape failed!"
                )

        # =========================
        # INVALID ACTION
        # =========================

        else:

            print(
                "\nInvalid action."
            )

            continue

        # =========================
        # COMPANION ATTACKS
        # =========================

        if enemy_hp > 0:

            enemy_hp = companion_attack(

                companions,
                enemy_hp

            )

        # =========================
        # BOSS PHASE
        # =========================

        if (

            enemy_hp > 0

            and

            enemy_hp <= 25

            and

            boss_phase == 1

        ):

            boss_phase = 2

            print(
                "\n=== BOSS PHASE 2 ==="
            )

            print(
                enemy_name,
                "becomes enraged!"
            )

        # =========================
        # ENEMY DEFEATED
        # =========================

        if enemy_hp <= 0:

            print(
                "\nThe enemy collapses!"
            )

            return True

        # =========================
        # PLAYER DODGE
        # =========================

        dodge_roll = random.randint(
            1,
            100
        )

        if dodge_roll <= player["dodge"]:

            print(
                "\nYou dodge the attack!"
            )

            continue

        # =========================
        # ENEMY ATTACK
        # =========================

        enemy_damage = random.randint(
            6,
            14
        )

        if boss_phase == 2:

            enemy_damage += 4

        damage_player(
            enemy_damage
        )

        print(
            "\nThe",
            enemy_name,
            "attacks you!"
        )

    # =========================
    # PLAYER DEFEATED
    # =========================

    if player["hp"] <= 0:

        print(
            "\nYou were defeated..."
        )

        return False

    return True