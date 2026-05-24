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

from loot import affixes

from bosses import check_boss_phase

from companions import companions

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

    turn_count = 1

    active_effects = []

    max_enemy_hp = enemy_hp

    while player_hp > 0 and enemy_hp > 0:

        # =========================
        # BOSS PHASE SYSTEM
        # =========================

        phase, special_attack = check_boss_phase(
            enemy_name,
            enemy_hp,
            max_enemy_hp
        )

        print("\nBoss Phase:", phase)

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

        print("Dodge:", str(player_dodge) + "%")

        print(enemy_name, "HP:", enemy_hp)

        print("Equipped Weapon:", equipped_weapon)

        print("\nParty:", party)

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

            # =========================
            # ELEMENTAL SYSTEM
            # =========================

            weapon_name = equipped_weapon.lower()

            weapon_element = None

            if "flaming" in weapon_name:

                weapon_element = "fire"

            elif "frozen" in weapon_name:

                weapon_element = "ice"

            elif "venomous" in weapon_name:

                weapon_element = "poison"

            elif "vampiric" in weapon_name:

                weapon_element = "dark"

            enemy_weakness = enemies[enemy_name]["weakness"]

            enemy_resistance = enemies[enemy_name]["resistance"]

            # =========================
            # ELEMENTAL WEAKNESS
            # =========================

            if weapon_element == enemy_weakness:

                damage = int(damage * 1.5)

                print("\n=== ELEMENTAL WEAKNESS ===")

                print(
                    enemy_name,
                    "is weak to",
                    weapon_element + "!"
                )

            # =========================
            # ELEMENTAL RESISTANCE
            # =========================

            elif weapon_element == enemy_resistance:

                damage = int(damage * 0.5)

                print("\n=== ELEMENTAL RESISTED ===")

                print(
                    enemy_name,
                    "resists",
                    weapon_element + "!"
                )

            # =========================
            # APPLY DAMAGE
            # =========================

            enemy_hp -= damage

            print("\nYou attack with", equipped_weapon + "!")

            print("You deal", damage, "damage!")

            # =========================
            # WEAPON EFFECTS
            # =========================

            # FLAMING

            if "flaming" in weapon_name:

                active_effects = add_status_effect(
                    active_effects,
                    "burn",
                    3
                )

                print("The weapon ignites the enemy!")

            # VENOMOUS

            elif "venomous" in weapon_name:

                active_effects = add_status_effect(
                    active_effects,
                    "poison",
                    3
                )

                print("Poison spreads through the enemy!")

            # VAMPIRIC

            elif "vampiric" in weapon_name:

                lifesteal = random.randint(3, 8)

                player_hp += lifesteal

                print(
                    "\nVampiric energy restores",
                    lifesteal,
                    "HP!"
                )

            # FROZEN

            elif "frozen" in weapon_name:

                freeze_roll = random.randint(1, 100)

                if freeze_roll <= 25:

                    print(
                        "\nThe enemy is frozen solid!"
                    )

                    continue

        # =========================
        # SKILLS
        # =========================

        elif action.lower() == "skills":

            print("\n=== SKILLS ===")

            # WARRIOR

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

            # MAGE

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

            # ROGUE

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
        # COMPANION ATTACKS
        # =========================

        for member in party:

            companion_damage = companions[
                member
            ]["damage"]

            enemy_hp -= companion_damage

            print(
                "\n" + member,
                "attacks for",
                companion_damage,
                "damage!"
            )

            if enemy_hp <= 0:

                print(
                    enemy_name,
                    "was defeated by",
                    member + "!"
                )

                break

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
        # BOSS PHASE BONUSES
        # =========================

        if phase == 2:

            print("\n=== PHASE 2 ACTIVATED ===")

        elif phase == 3:

            print("\n=== FINAL PHASE ===")

        # =========================
        # HIDDEN CULT
        # =========================

        if special == "summon":

            if turn_count % 3 == 0:

                enemy_damage = random.randint(8, 16)

                print(
                    "\nThe cult summons dark reinforcements!"
                )

            else:

                enemy_damage = random.randint(4, 10)

        # =========================
        # ANCIENT DRAGON
        # =========================

        elif special == "fire":

            if turn_count % 2 == 0:

                enemy_damage = random.randint(14, 22)

                print(
                    "\nThe dragon unleashes FIRE BREATH!"
                )

                active_effects = add_status_effect(
                    active_effects,
                    "burn",
                    3
                )

            else:

                enemy_damage = random.randint(6, 12)

            # =========================
            # DRAGON PHASE ATTACKS
            # =========================

            if special_attack == "inferno":

                enemy_damage += 5

                print(
                    "\nThe dragon unleashes INFERNO!"
                )

            elif special_attack == "meteor":

                enemy_damage += 10

                print(
                    "\nMETEORS crash from the sky!"
                )

        # =========================
        # CORRUPTED KNIGHT
        # =========================

        elif special == "shield":

            if turn_count % 3 == 0:

                enemy_damage = random.randint(5, 8)

                print(
                    "\nThe knight raises a massive shield!"
                )

                print(
                    "Your next attack will be weakened."
                )

            else:

                enemy_damage = random.randint(7, 14)

        # =========================
        # SHADOW BEAST
        # =========================

        elif special == "dodge":

            dodge_chance = random.randint(1, 100)

            if dodge_chance <= 35:

                print(
                    "\nThe shadow beast vanishes into darkness!"
                )

                print(
                    "It completely dodges your attack!"
                )

                enemy_damage = random.randint(5, 12)

            else:

                enemy_damage = random.randint(7, 15)

            # =========================
            # SHADOW FRENZY
            # =========================

            if special_attack == "shadow_frenzy":

                enemy_damage += 6

                print(
                    "\nThe Shadow Beast enters a frenzy!"
                )

        # =========================
        # NECROMANCER
        # =========================

        elif special == "heal":

            if turn_count % 2 == 0:

                heal_amount = random.randint(5, 12)

                enemy_hp += heal_amount

                print(
                    "\nDark magic restores the necromancer!"
                )

                print(
                    enemy_name,
                    "heals",
                    heal_amount,
                    "HP!"
                )

            enemy_damage = random.randint(5, 10)

            # =========================
            # NECROMANCER PHASES
            # =========================

            if special_attack == "summon_undead":

                enemy_damage += 4

                print(
                    "\nUndead warriors rise from the ground!"
                )

            elif special_attack == "death_magic":

                enemy_damage += 8

                print(
                    "\nThe necromancer casts DEATH MAGIC!"
                )

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
        # DODGE SYSTEM
        # =========================

        dodge_roll = random.randint(1, 100)

        if dodge_roll <= player_dodge:

            print("\nYou DODGE the attack!")

        else:

            player_hp -= enemy_damage

            print("\nThe enemy attacks!")

            print(
                "You take",
                enemy_damage,
                "damage!"
            )

        turn_count += 1

    return player_hp, enemy_hp, player_resource