import random

def combat(
    player_hp,
    enemy_name,
    enemy_hp,
    attack_bonus,
    inventory,
    enemies,
    equipped_weapon,
    weapon_bonus
):

    while player_hp > 0 and enemy_hp > 0:

        print("\n=========================")
        print("Your HP:", player_hp)
        print(enemy_name, "HP:", enemy_hp)

        action = input("\nWhat do you do? ")

        # ATTACK

        if action.lower() == "attack":

            damage = random.randint(5, 15) + attack_bonus + weapon_bonus

            enemy_hp -= damage

            attack_descriptions = [

                "You slash forward with deadly force!",
                "Your weapon crashes into the enemy!",
                "You strike with incredible speed!",
                "A powerful blow lands against the enemy!",
                "Steel clashes as your attack hits hard!"
            ]

            print("\n" + random.choice(attack_descriptions))
            print("You dealt", damage, "damage!")

        # HEAL

        elif action.lower() == "heal":

            if "Healing Potion" in inventory:

                heal = random.randint(15, 25)

                player_hp += heal

                inventory.remove("Healing Potion")

                print("\nYou drink a Healing Potion.")
                print("You recover", heal, "HP!")

            else:

                print("\nYou do not have any Healing Potions.")

        # INVENTORY

        elif action.lower() == "inventory":

            print("\n=== INVENTORY ===")

            if len(inventory) == 0:

                print("Your inventory is empty.")

            else:

                for item in inventory:
                    print("-", item)

            print("\nEquipped Weapon:", equipped_weapon)
            print("Weapon Bonus:", weapon_bonus)

        # RUN

        elif action.lower() == "run":

            print("\nYou escape into the darkness...")
            break

        # INVALID

        else:

            print("\nYou hesitate and lose your chance!")

        # ENEMY TURN

        if enemy_hp > 0:

            enemy_damage = random.randint(4, 12)

            player_hp -= enemy_damage

            enemy_attacks = [

                "The enemy lunges at you!",
                "A brutal strike hits your armor!",
                "Dark magic crashes into you!",
                "The enemy attacks without mercy!",
                "A savage blow knocks you backward!"
            ]

            print("\n" + random.choice(enemy_attacks))
            print("You take", enemy_damage, "damage!")

            # SPECIAL ABILITIES

            special = enemies[enemy_name]["special"]

            # FIRE

            if special == "fire":

                extra_fire = random.randint(3, 8)

                player_hp -= extra_fire

                print("Flames engulf the battlefield!")
                print("You take", extra_fire, "fire damage!")

            # HEAL

            elif special == "heal":

                heal_amount = random.randint(4, 10)

                enemy_hp += heal_amount

                print("Dark magic restores the necromancer!")
                print(enemy_name, "heals", heal_amount, "HP!")

            # DODGE

            elif special == "dodge":

                print("The shadow beast melts into darkness.")

            # SHIELD

            elif special == "shield":

                print("The corrupted knight raises a heavy shield.")

            # SUMMON

            elif special == "summon":

                print("The cultists begin chanting for reinforcements!")

    return player_hp, enemy_hp