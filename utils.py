# =========================
# INPUT NORMALIZATION
# =========================

def normalize_input(user_input):

    return (

        user_input

        .strip()

        .lower()
    )

# =========================
# YES / NO INPUTS
# =========================

def is_yes(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "yes",
        "y",
        "yeah",
        "yep",
        "sure",
        "ok",
        "okay"
    ]

def is_no(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "no",
        "n",
        "nope"
    ]

# =========================
# COMBAT COMMANDS
# =========================

def is_attack(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "attack",
        "hit",
        "strike",
        "fight",
        "swing",
        "basic attack"
    ]

def is_skills(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "skills",
        "skill",
        "magic",
        "spell",
        "abilities",
        "ability"
    ]

def is_heal(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "heal",
        "potion",
        "drink potion",
        "use potion",
        "recover"
    ]

def is_inventory(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "inventory",
        "items",
        "bag",
        "gear",
        "equipment"
    ]

def is_run(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "run",
        "escape",
        "flee",
        "retreat"
    ]

# =========================
# MORAL CHOICES
# =========================

def is_spare(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "1",
        "spare",
        "spare them",
        "forgive",
        "mercy",
        "show mercy"
    ]

def is_execute(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "2",
        "execute",
        "execute them",
        "kill",
        "kill them",
        "finish them"
    ]

def is_recruit(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "3",
        "recruit",
        "recruit them",
        "convert",
        "join us"
    ]

# =========================
# SHOP COMMANDS
# =========================

def is_buy_potion(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "1",
        "buy potion",
        "healing potion",
        "potion"
    ]

def is_buy_weapon(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "2",
        "buy weapon",
        "steel sword",
        "weapon",
        "sword"
    ]

def is_leave_shop(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "3",
        "leave",
        "exit",
        "leave shop",
        "done"
    ]

# =========================
# CLASS SELECTION
# =========================

def is_warrior(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "warrior",
        "fighter",
        "tank"
    ]

def is_mage(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "mage",
        "wizard",
        "sorcerer",
        "caster"
    ]

def is_rogue(user_input):

    user_input = normalize_input(
        user_input
    )

    return user_input in [

        "rogue",
        "assassin",
        "thief",
        "shadow"
    ]