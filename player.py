import random

from status_effects import (
    add_status_effect,
    process_status_effects
)

from skills import (
    power_strike,
    fireball,
    backstab
)

from equipment import get_weapon_stats

def combat(
    player_hp,
    enemy_name,
    enemy_hp,
    attack_bonus,
    inventory,
    enemies,
    equipped_weapon,
    weapon_bonus,
    player_class,
    player_resource,
    max_resource,
    resource_name,
    player_defense
):

    turn_count = 1

    active_effects = []

    while player_hp > 0 and enemy_hp > 0:

        # =========================
        # PROCESS STATUS EFFECTS
        # =========================

        player_hp, active_effects = process_status_effects(
            player_hp,
            active_effects
        )

        print("\n======================")
        print("Your HP:", player_hp)

        print(
            resource_name + ":",
            player_resource,
            "/",
            max_resource
        )

        print("Defense:", player_defense)

        print(enemy_name, "HP:", enemy_hp)

        action = input(
            "\nChoose action "
            "(attack / skills / heal / inventory): "
        )

        # =========================
        # INVENTORY
        # =========================

        if action.lower() == "inventory":

            print("\n=== INVENTORY ===")

            if len(inventory) == 0:

                print("Inventory empty.")

            else:

                for item in inventory:

                    print("-", item)

            continue

        # =========================
        # BASIC ATTACK
        # =========================

        elif action.lower() == "attack":

            # =========================
            # WEAPON STATS
            # =========================

            weapon_stats = get_weapon_stats(
                equipped_weapon
            )

            # =========================
            # CRITICAL HIT SYSTEM
            # =========================

            crit_chance = 10

            crit_chance += weapon_stats["crit_bonus"]

            # ROGUES HAVE HIGHER CRIT CHANCE

            if player_class == "rogue":

                crit_chance += 15

            # =========================
            # DAMAGE CALCULATION
            # =========================

            damage = random.randint(5, 15)

            damage += attack_bonus

            damage += weapon_stats["damage"]

            crit_roll = random.randint(1, 100)

            # =========================
            # CRITICAL HIT
            # =========================

            if crit_roll <= crit_chance:

                damage *= 2

                print("\n=== CRITICAL HIT ===")

            enemy_hp -= damage

            print("\nYou attack with", equipped_weapon + "!")
            print("You deal", damage, "damage!")

        # =========================
        # SKILLS
        # =========================

        elif action.lower() == "skills":

            print("\n=== SKILLS ===")

            # =========================
            # WARRIOR
            # =========================

            if player_class == "warrior":

                print("1. Power Strike (15 Stamina)")

                skill_choice = input("> ")

                if skill_choice == "1":

                    if player_resource >= 15:

                        player_resource -= 15

                        enemy_hp = power_strike(
                            enemy_hp,
                            attack_bonus
                        )

                    else:

                        print(
                            "\nNot enough",
                            resource_name + "!"
                        )

            # =========================
            # MAGE
            # =========================

            elif player_class == "mage":

                print("1. Fireball (20 Mana)")

                skill_choice = input("> ")

                if skill_choice == "1":

                    if player_resource >= 20:

                        player_resource -= 20

                        enemy_hp = fireball(enemy_hp)

                        active_effects = add_status_effect(
                            active_effects,
                            "burn",
                            3
                        )

                    else:

                        print(
                            "\nNot enough",
                            resource_name + "!"
                        )

            # =========================
            # ROGUE
            # =========================

            elif player_class == "rogue":

                print("1. Backstab (10 Stamina)")

                skill_choice = input("> ")

                if skill_choice == "1":

                    if player_resource >= 10:

                        player_resource -= 10

                        enemy_hp = backstab(enemy_hp)

                    else:

                        print(
                            "\nNot enough",
                            resource_name + "!"
                        )

        # =========================
        # HEALING POTION
        # =========================

        elif action.lower() == "heal":

            if "Healing Potion" in inventory:

                heal_amount = 20

                player_hp += heal_amount

                inventory.remove("Healing Potion")

                print("\nYou drink a Healing Potion!")
                print("Recovered", heal_amount, "HP!")

            else:

                print("\nYou don't have any potions.")

            continue

        # =========================
        # INVALID ACTION
        # =========================

        else:

            print("\nInvalid action.")
            continue

        # =========================
        # ENEMY DEFEATED
        # =========================

        if enemy_hp <= 0:

            print("\nThe enemy collapses!")

            break

        # =========================
        # ENEMY AI SYSTEM
        # =========================

        special = enemies[enemy_name]["special"]

        # =========================
        # HIDDEN CULT
        # =========================

        if special == "summon":

            if turn_count % 3 == 0:

                enemy_damage = random.randint(8, 16)

                print("\nThe cult summons dark reinforcements!")

            else:

                enemy_damage = random.randint(4, 10)

        # =========================
        # ANCIENT DRAGON
        # =========================

        elif special == "fire":

            if turn_count % 2 == 0:

                enemy_damage = random.randint(14, 22)

                print("\nThe dragon unleashes FIRE BREATH!")

                active_effects = add_status_effect(
                    active_effects,
                    "burn",
                    3
                )

            else:

                enemy_damage = random.randint(6, 12)

            if enemy_hp < 15:

                enemy_damage += 5

                print("The dragon enters an ENRAGED state!")

        # =========================
        # CORRUPTED KNIGHT
        # =========================

        elif special == "shield":

            if turn_count % 3 == 0:

                enemy_damage = random.randint(5, 8)

                print("\nThe knight raises a massive shield!")
                print("Your next attack will be weakened.")

            else:

                enemy_damage = random.randint(7, 14)

        # =========================
        # SHADOW BEAST
        # =========================

        elif special == "dodge":

            dodge_chance = random.randint(1, 100)

            if dodge_chance <= 35:

                print("\nThe shadow beast vanishes into darkness!")
                print("It completely dodges your attack!")

                enemy_damage = random.randint(5, 12)

            else:

                enemy_damage = random.randint(7, 15)

        # =========================
        # NECROMANCER
        # =========================

        elif special == "heal":

            if turn_count % 2 == 0:

                heal_amount = random.randint(5, 12)

                enemy_hp += heal_amount

                print("\nDark magic restores the necromancer!")
                print(enemy_name, "heals", heal_amount, "HP!")

            enemy_damage = random.randint(5, 10)

        # =========================
        # DEFAULT
        # =========================

        else:

            enemy_damage = random.randint(4, 12)

        # =========================
        # ARMOR / DEFENSE
        # =========================

        enemy_damage -= player_defense

        if enemy_damage < 1:

            enemy_damage = 1

        # =========================
        # ENEMY ATTACK
        # =========================

        player_hp -= enemy_damage

        print("\nThe enemy attacks!")
        print("You take", enemy_damage, "damage!")

        turn_count += 1

    return player_hp, enemy_hp, player_resource