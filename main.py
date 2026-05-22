import random

# =========================
# PLAYER MEMORY / STORY STATE
# =========================

cult_defeated = False
dragon_defeated = False
knight_defeated = False

player_gold = 25

# =========================
# ADVENTURE SETTINGS
# =========================

adventure_length = 3
current_room = 1

# =========================
# QUESTS
# =========================

quests = [
    "A village is haunted by whispers at night.",
    "A merchant caravan disappeared in the woods.",
    "A mining town has suddenly gone silent.",
    "A royal tomb has been broken into.",
    "A mysterious plague spreads through the kingdom."
]

# =========================
# LOCATIONS
# =========================

locations = [
    "inside cursed woods",
    "beneath an ancient castle",
    "under a ruined city",
    "inside frozen caves",
    "within a dark swamp"
]

# =========================
# ENEMIES
# =========================

enemies = [
    "hidden cult",
    "ancient dragon",
    "corrupted knight",
    "shadow beast",
    "necromancer"
]

# =========================
# START PLAYER
# =========================

player_hp = 50

# =========================
# MAIN ADVENTURE LOOP
# =========================

while current_room <= adventure_length and player_hp > 0:

    # GENERATE STORY
    quest = random.choice(quests)
    location = random.choice(locations)
    enemy_name = random.choice(enemies)

    enemy_hp = random.randint(15, 30)

    print("\n=== YOUR ADVENTURE ===")

    print("\n" + quest)

    print("\nThe danger waits...")
    print(location)

    print("\nMain Enemy:")
    print(enemy_name)

    # =========================
    # COMBAT LOOP
    # =========================

    while player_hp > 0 and enemy_hp > 0:

        print("\nYour HP:", player_hp)
        print(enemy_name, "HP:", enemy_hp)

        action = input("\nWhat do you do? ")

        # =========================
        # ATTACK
        # =========================

        if action.lower() == "attack":

            damage = random.randint(5, 15)

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

        # =========================
        # HEAL
        # =========================

        elif action.lower() == "heal":

            heal = random.randint(8, 15)

            player_hp += heal

            print("\nA warm light surrounds you.")
            print("You healed", heal, "HP!")

        # =========================
        # RUN
        # =========================

        elif action.lower() == "run":

            print("\nYou escape into the darkness...")
            break

        # =========================
        # INVALID ACTION
        # =========================

        else:

            print("\nYou hesitate and lose your chance!")

        # =========================
        # ENEMY TURN
        # =========================

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

    # =========================
    # ENDINGS
    # =========================

    if player_hp <= 0:

        print("\nYou were defeated...")
        print("Darkness closes in around you.")

    elif enemy_hp <= 0:

        print("\nVictory!")
        print("The enemy has fallen.")

        reward = random.randint(10, 30)

        player_gold += reward

        print("You gained", reward, "gold!")
        print("Total Gold:", player_gold)

        # STORY MEMORY

        if enemy_name == "hidden cult":
            cult_defeated = True

        elif enemy_name == "ancient dragon":
            dragon_defeated = True

        elif enemy_name == "corrupted knight":
            knight_defeated = True

        current_room += 1

        # CONTINUE ADVENTURE

        if current_room <= adventure_length:

            print("\nYou continue deeper into the adventure...")

        else:

            print("\n=== FINAL VICTORY ===")
            print("You survived the adventure!")

# =========================
# STORY STATE
# =========================

print("\n=== STORY STATE ===")

print("Cult Defeated:", cult_defeated)
print("Dragon Defeated:", dragon_defeated)
print("Knight Defeated:", knight_defeated)

print("Gold:", player_gold)