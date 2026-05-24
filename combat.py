import random

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

    player_hp,
    enemy_name,
    enemy_hp,
    attack_bonus,
    inventory,
    enemies,
    equipped_weapon,
    weapon_bonus,
    party,
    player_class,
    player_resource,
    max_resource,
    resource_name,
    player_defense,
    player_dodge

):

    boss_phase = 1

    while player_hp > 0 and enemy_hp > 0:

        print("\n====================")

        print("Your HP:", player_hp)

        print(
            resource_name + ":",
            str(player_resource)
            + " / "
            + str(max_resource)
        )

        print(
            "Defense:",
            player_defense
        )

        print(
            "Dodge:",
            str(player_dodge) + "%"
        )

        print(
            enemy_name + " HP:",
            enemy_hp
        )

        print(
            "Equipped Weapon:",
            equipped_weapon
        )

        print(
            "\nParty:",
            party
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
                8,
                15
            )

            damage += attack_bonus

            damage += weapon_bonus

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
                equipped_weapon + "!"
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

            if player_class == "Warrior":

                print(
                    "• Shield Slam (20 stamina)"
                )

                print(
                    "• Battle Cry (15 stamina)"
                )

            # =========================
            # MAGE
            # =========================

            elif player_class == "Mage":

                print(
                    "• Fireball (25 mana)"
                )

                print(
                    "• Arcane Burst (35 mana)"
                )

            # =========================
            # ROGUE
            # =========================

            elif player_class == "Rogue":

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

            if player_class == "Warrior":

                if (
                    skill_choice
                    == "shield slam"
                ):

                    if player_resource >= 20:

                        player_resource -= 20

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

                elif (
                    skill_choice
                    == "battle cry"
                ):

                    if player_resource >= 15:

                        player_resource -= 15

                        attack_bonus += 5

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

            elif player_class == "Mage":

                if (
                    skill_choice
                    == "fireball"
                ):

                    if player_resource >= 25:

                        player_resource -= 25

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

                elif (
                    skill_choice
                    == "arcane burst"
                ):

                    if player_resource >= 35:

                        player_resource -= 35

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

            elif player_class == "Rogue":

                if (
                    skill_choice
                    == "backstab"
                ):

                    if player_resource >= 20:

                        player_resource -= 20

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

                elif (
                    skill_choice
                    == "shadow strike"
                ):

                    if player_resource >= 30:

                        player_resource -= 30

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

            player_hp = use_potion(
                inventory,
                player_hp
            )

        # =========================
        # INVENTORY
        # =========================

        elif is_inventory(action):

            show_inventory(
                inventory,
                equipped_weapon,
                weapon_bonus
            )

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

                break

            else:

                print(
                    "\nEscape failed!"
                )

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
                party,
                enemy_hp
            )

        # =========================
        # BOSS PHASES
        # =========================

        if (

            enemy_hp <= 25

            and

            enemy_hp > 0

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

            break

        # =========================
        # DODGE
        # =========================

        dodge_roll = random.randint(
            1,
            100
        )

        if dodge_roll <= player_dodge:

            print(
                "\nYou dodge the attack!"
            )

            continue

        # =========================
        # ENEMY ATTACK
        # =========================

        enemy_damage = random.randint(
            5,
            12
        )

        if boss_phase == 2:

            enemy_damage += 5

        enemy_damage -= player_defense

        if enemy_damage < 1:

            enemy_damage = 1

        player_hp -= enemy_damage

        print(
            "\nThe",
            enemy_name,
            "hits you for",
            enemy_damage,
            "damage!"
        )

    return (
        player_hp,
        enemy_hp,
        player_resource
    )