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
# CHARACTER CLASSES
# =========================

classes = {

    "warrior": {
        "hp": 70,
        "attack_bonus": 5
    },

    "mage": {
        "hp": 45,
        "attack_bonus": 10
    },

    "rogue": {
        "hp": 55,
        "attack_bonus": 7
    }
}

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

enemies = {

    "hidden cult": {
        "hp_min": 15,
        "hp_max": 25,
        "special": "summon"
    },

    "ancient dragon": {
        "hp_min": 30,
        "hp_max": 45,
        "special": "fire"
    },

    "corrupted knight": {
        "hp_min": 20,
        "hp_max": 35,
        "special": "shield"
    },

    "shadow beast": {
        "hp_min": 18,
        "hp_max": 30,
        "special": "dodge"
    },

    "necromancer": {
        "hp_min": 20,
        "hp_max": 40,
        "special": "heal"
    }
}

# =========================
# RANDOM EVENTS
# =========================

events = [

    "You discover a hidden treasure chest.",
    "A wandering merchant appears.",
    "You step into a dangerous trap.",
    "An old traveler gives you advice.",
    "You find an ancient magical shrine."
]

# =========================
# FUNCTIONS
# =========================

def generate_story():

    quest = random.choice(quests)
    location = random.choice(locations)
    enemy_name = random.choice(list(enemies.keys()))

    return quest, location, enemy_name


def random_event(player_hp, player_gold):

    def story_choice(player_gold, player_reputation):

    print("\n=== STORY CHOICE ===")
    print("A wounded traveler begs for your help.")

    print("\n1. Help the traveler")
    print("2. Ignore the traveler")
    print("3. Rob the traveler")

    choice = input("\nChoose: ")

    # HELP

    if choice == "1":

        player_reputation += 5

        print("\nYou help the traveler.")
        print("Your reputation increases.")

    # IGNORE

    elif choice == "2":

        print("\nYou continue on your journey.")

    # ROB

    elif choice == "3":

        gold_stolen = random.randint(10, 25)

        player_gold += gold_stolen

        player_reputation -= 10

        print("\nYou rob the traveler!")
        print("You steal", gold_stolen, "gold.")
        print("Your reputation decreases.")

    return player_gold, player_reputation

    event = random.choice(events)

    print("\n=== RANDOM EVENT ===")
    print(event)

    # TREASURE

    if "treasure" in event:

        gold_found = random.randint(10, 25)

        player_gold += gold_found

        print("You found", gold_found, "gold!")

    # MERCHANT

    elif "merchant" in event:

        print("The merchant gives you a healing potion.")

        player_hp += 10

        print("You gain 10 HP!")

    # TRAP

    elif "trap" in event:

        trap_damage = random.randint(5, 12)

        player_hp -= trap_damage

        print("The trap deals", trap_damage, "damage!")

    # TRAVELER

    elif "traveler" in event:

        print("The traveler warns you about future dangers.")

    # SHRINE

    elif "shrine" in event:

        print("Mystical energy restores your strength.")

        player_hp += 15

    return player_hp, player_gold


def combat(player_hp, enemy_name, enemy_hp, attack_bonus):

    while player_hp > 0 and enemy_hp > 0:

        print("\n=========================")
        print("Your HP:", player_hp)
        print(enemy_name, "HP:", enemy_hp)

        action = input("\nWhat do you do? ")

        # =========================
        # ATTACK
        # =========================

        if action.lower() == "attack":

            damage = random.randint(5, 15) + attack_bonus

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
            # SPECIAL ABILITIES
            # =========================

            special = enemies[enemy_name]["special"]

            # FIRE BREATH

            if special == "fire":

                extra_fire = random.randint(3, 8)

                player_hp -= extra_fire

                print("Flames engulf the battlefield!")
                print("You take", extra_fire, "fire damage!")

            # NECROMANCER HEAL

            elif special == "heal":

                heal_amount = random.randint(4, 10)

                enemy_hp += heal_amount

                print("Dark magic restores the necromancer!")
                print(enemy_name, "heals", heal_amount, "HP!")

            # SHADOW DODGE

            elif special == "dodge":

                print("The shadow beast melts into darkness.")

            # KNIGHT SHIELD

            elif special == "shield":

                print("The corrupted knight raises a heavy shield.")

            # CULT SUMMON

            elif special == "summon":

                print("The cultists begin chanting for reinforcements!")

    return player_hp, enemy_hp


def show_story_state():

    print("\n=== STORY STATE ===")

    print("Cult Defeated:", cult_defeated)
    print("Dragon Defeated:", dragon_defeated)
    print("Knight Defeated:", knight_defeated)

    print("Gold:", player_gold)


# =========================
# CHOOSE CLASS
# =========================

print("Choose your class:")
print("Warrior")
print("Mage")
print("Rogue")

player_class = input("> ").lower()

player_hp = classes[player_class]["hp"]

attack_bonus = classes[player_class]["attack_bonus"]

print("\nYou chose:", player_class)

# =========================
# MAIN ADVENTURE LOOP
# =========================

while current_room <= adventure_length and player_hp > 0:

    # GENERATE STORY

    quest, location, enemy_name = generate_story()

    enemy_hp = random.randint(
        enemies[enemy_name]["hp_min"],
        enemies[enemy_name]["hp_max"]
    )

    print("\n=== YOUR ADVENTURE ===")

    print("\n" + quest)

    print("\nThe danger waits...")
    print(location)

    print("\nMain Enemy:")
    print(enemy_name)

    # COMBAT

    player_hp, enemy_hp = combat(
        player_hp,
        enemy_name,
        enemy_hp,
        attack_bonus
    )

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

        player_reputation = 0

        if enemy_name == "hidden cult":
            cult_defeated = True

        elif enemy_name == "ancient dragon":
            dragon_defeated = True

        elif enemy_name == "corrupted knight":
            knight_defeated = True

        # RANDOM EVENT

        player_hp, player_gold = random_event(
            player_hp,
            player_gold
        )

        current_room += 1

        # CONTINUE ADVENTURE

        if current_room <= adventure_length:

            print("\nYou continue deeper into the adventure...")

        else:

            print("\n=== FINAL VICTORY ===")
            print("You survived the adventure!")

# =========================
# FINAL STORY STATE
# =========================

show_story_state()

def show_story_state():

print("\n=== STORY STATE ===")

print("Cult Defeated:", cult_defeated)
print("Dragon Defeated:", dragon_defeated)
print("Knight Defeated:", knight_defeated)

print("Gold:", player_gold)

print("Reputation:", player_reputation)