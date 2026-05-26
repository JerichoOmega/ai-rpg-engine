from player import (
    player
)

from event_bus import (
    emit
)

# =========================
# PLAYER SKILLS
# =========================

player_skills = {

    "available_points": 3,

    "unlocked_skills": []
}

# =========================
# SKILL DATABASE
# =========================

SKILLS = {

    "power_strike": {

        "category": "warrior",

        "description":
            "Increase attack power.",

        "cost": 1,

        "effect": {

            "attack_bonus": 5
        }
    },

    "iron_skin": {

        "category": "warrior",

        "description":
            "Increase defense.",

        "cost": 1,

        "effect": {

            "defense_bonus": 5
        }
    },

    "shadow_step": {

        "category": "rogue",

        "description":
            "Improve evasion and stealth.",

        "cost": 2,

        "effect": {

            "evasion_bonus": 10
        }
    },

    "arcane_mastery": {

        "category": "mage",

        "description":
            "Increase magical power.",

        "cost": 2,

        "effect": {

            "magic_bonus": 10
        }
    },

    "survival_instinct": {

        "category": "survivor",

        "description":
            "Increase maximum health.",

        "cost": 1,

        "effect": {

            "max_hp_bonus": 20
        }
    },

    "void_touch": {

        "category": "corruption",

        "description":
            "Gain forbidden power.",

        "cost": 3,

        "effect": {

            "attack_bonus": 15,

            "corruption": 10
        }
    }
}

# =========================
# UNLOCK SKILL
# =========================

def unlock_skill(

    skill_name

):

    skill = SKILLS.get(
        skill_name
    )

    if not skill:

        print(
            "\nUnknown skill."
        )

        return

    if skill_name in player_skills[
        "unlocked_skills"
    ]:

        print(
            "\nSkill already unlocked."
        )

        return

    cost = skill["cost"]

    if player_skills[
        "available_points"
    ] < cost:

        print(
            "\nNot enough skill points."
        )

        return

    # =========================
    # SPEND POINTS
    # =========================

    player_skills[
        "available_points"
    ] -= cost

    player_skills[
        "unlocked_skills"
    ].append(
        skill_name
    )

    apply_skill_effects(
        skill_name
    )

    print(
        f"\nUnlocked skill:"
        f" {skill_name}"
    )

    emit(

        "skill_unlocked",

        skill_name=skill_name
    )

# =========================
# APPLY SKILL EFFECTS
# =========================

def apply_skill_effects(

    skill_name

):

    skill = SKILLS.get(
        skill_name
    )

    if not skill:

        return

    effects = skill[
        "effect"
    ]

    # =========================
    # ATTACK BONUS
    # =========================

    if "attack_bonus" in effects:

        player.attack_bonus += effects[
            "attack_bonus"
        ]

    # =========================
    # DEFENSE BONUS
    # =========================

    if "defense_bonus" in effects:

        player.defense += effects[
            "defense_bonus"
        ]

    # =========================
    # MAX HP BONUS
    # =========================

    if "max_hp_bonus" in effects:

        player.max_hp += effects[
            "max_hp_bonus"
        ]

        player.hp += effects[
            "max_hp_bonus"
        ]

    # =========================
    # MAGIC BONUS
    # =========================

    if "magic_bonus" in effects:

        player.magic_power += effects[
            "magic_bonus"
        ]

    # =========================
    # EVASION BONUS
    # =========================

    if "evasion_bonus" in effects:

        player.evasion += effects[
            "evasion_bonus"
        ]

# =========================
# GAIN SKILL POINT
# =========================

def gain_skill_point(

    amount=1

):

    player_skills[
        "available_points"
    ] += amount

    print(
        f"\nGained"
        f" {amount}"
        " skill point(s)."
    )

# =========================
# SHOW SKILLS
# =========================

def show_skill_tree():

    print(
        "\n=== SKILL TREE ==="
    )

    print(
        f"\nAvailable Points:"
        f" {player_skills['available_points']}"
    )

    for skill_name, skill_data in SKILLS.items():

        unlocked = (

            skill_name

            in

            player_skills[
                "unlocked_skills"
            ]
        )

        status = "UNLOCKED"

        if not unlocked:

            status = "LOCKED"

        print(
            f"\n{skill_name}"
        )

        print(
            f"Category:"
            f" {skill_data['category']}"
        )

        print(
            f"Cost:"
            f" {skill_data['cost']}"
        )

        print(
            f"Status:"
            f" {status}"
        )

        print(
            f"Description:"
            f" {skill_data['description']}"
        )

# =========================
# PLAYER BUILD SUMMARY
# =========================

def show_player_build():

    print(
        "\n=== PLAYER BUILD ==="
    )

    print(
        "Unlocked Skills:"
    )

    for skill in player_skills[
        "unlocked_skills"
    ]:

        print(
            f"- {skill}"
        )

# =========================
# RANDOM SKILL REWARD
# =========================

def random_skill_reward():

    gain_skill_point(
        1
    )

    print(
        "\nYou feel yourself growing stronger."
    )

# =========================
# RESET SKILLS
# =========================

def reset_skills():

    player_skills[
        "available_points"
    ] = 3

    player_skills[
        "unlocked_skills"
    ] = []

    print(
        "\nSkills reset."
    )

# =========================
# SKILL CATEGORY FILTER
# =========================

def show_skill_category(

    category_name

):

    print(
        f"\n=== {category_name.upper()} SKILLS ==="
    )

    for skill_name, skill_data in SKILLS.items():

        if skill_data[
            "category"
        ] != category_name:

            continue

        print(
            f"\n{skill_name}"
        )

        print(
            f"{skill_data['description']}"
        )

# =========================
# LEGENDARY SKILL
# =========================

def unlock_legendary_skill():

    legendary_name = (
        "worldbreaker"
    )

    SKILLS[
        legendary_name
    ] = {

        "category": "legendary",

        "description":
            "Gain immense destructive power.",

        "cost": 5,

        "effect": {

            "attack_bonus": 50,

            "max_hp_bonus": 100
        }
    }

    print(
        "\nLegendary skill unlocked:"
        " worldbreaker"
    )

# =========================
# SKILL PROGRESSION SUMMARY
# =========================

def show_skill_progression():

    unlocked = len(

        player_skills[
            "unlocked_skills"
        ]
    )

    total = len(SKILLS)

    completion = round(

        (unlocked / total) * 100,

        2
    )

    print(
        "\n=== SKILL PROGRESSION ==="
    )

    print(
        f"Unlocked Skills:"
        f" {unlocked}/{total}"
    )

    print(
        f"Completion:"
        f" {completion}%"
    )