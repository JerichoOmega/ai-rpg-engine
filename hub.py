import random


def town_hub():

    print("\n=== TOWN OF ASHFALL ===")

    print("1. Tavern")
    print("2. Shop")
    print("3. Quest Board")
    print("4. Party Camp")
    print("5. Save Game")
    print("6. Begin Adventure")

    choice = input("> ").strip().lower()

    options = {

        "1": "tavern",
        "tavern": "tavern",

        "2": "shop",
        "shop": "shop",

        "3": "quests",
        "quest": "quests",
        "quest board": "quests",

        "4": "party",
        "camp": "party",
        "party": "party",

        "5": "save",
        "save": "save",

        "6": "adventure",
        "begin": "adventure",
        "begin adventure": "adventure"
    }

    return options.get(
        choice,
        "invalid"
    )


def tavern_scene():

    tavern_dialogue = [

        "A hooded traveler whispers about ancient ruins.",

        "Mercenaries argue over a dragon sighting.",

        "A bard sings of the fallen king.",

        "A frightened merchant warns of cult activity.",

        "Drunken adventurers boast near the fire."
    ]

    print("\n=== TAVERN ===")

    print(
        random.choice(
            tavern_dialogue
        )
    )

    print("\n1. Buy Drink")
    print("2. Listen For Rumors")
    print("3. Leave")

    choice = input("> ").strip().lower()

    return choice


def dialogue_choice():

    print("\n=== DIALOGUE ===")

    print(
        "A suspicious guard blocks your path."
    )

    print("\n1. Persuade")
    print("2. Threaten")
    print("3. Bribe")
    print("4. Leave")

    choice = input("> ").strip().lower()

    if choice in ["1", "persuade"]:

        print(
            "\nThe guard reluctantly allows passage."
        )

        return "persuade"

    elif choice in ["2", "threaten"]:

        print(
            "\nThe guard becomes hostile."
        )

        return "threaten"

    elif choice in ["3", "bribe"]:

        print(
            "\nGold changes hands quietly."
        )

        return "bribe"

    else:

        print(
            "\nYou leave peacefully."
        )

        return "leave"


def dungeon_room():

    rooms = [

        "enemy",

        "treasure",

        "event",

        "dialogue",

        "trap"
    ]

    room = random.choice(
        rooms
    )

    print("\n=== DUNGEON ROOM ===")

    if room == "enemy":

        print(
            "Enemies emerge from the shadows!"
        )

    elif room == "treasure":

        print(
            "You discover an ancient treasure chest."
        )

    elif room == "event":

        print(
            "A strange magical event unfolds."
        )

    elif room == "dialogue":

        print(
            "You encounter a mysterious traveler."
        )

    elif room == "trap":

        print(
            "You trigger a hidden trap!"
        )

    return room