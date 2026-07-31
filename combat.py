import random

from player import (
    player
)

from world_state import (
    world_state
)

from event_bus import (
    emit
)

from llm_bridge import (

    ai_combat_narration,

    ai_narrate
)

from companion_manager import (

    active_companions,

    companion_attack,

    use_companion_ability,

    calculate_party_bonus
)

from progression_manager import (
    award_xp_to_roster
)

from status_effects import (
    process_status_effects
)

from dm_brain import (
    change_story_pressure
)

# =========================
# CRITICAL HIT
# =========================

def calculate_critical_hit(

    crit_chance=15

):

    roll = random.randint(
        1,
        100
    )

    return roll <= crit_chance

# =========================
# EVASION CHECK
# =========================

def check_evasion(

    evasion

):

    roll = random.randint(
        1,
        100
    )

    return roll <= evasion

# =========================
# SHOW ENCOUNTER
# =========================

def show_combat_status(

    enemies

):

    print(
        "\n=== ENCOUNTER STATUS ==="
    )

    print(
        f"\nPlayer HP:"
        f" {player.hp}/"
        f"{player.max_hp}"
    )

    # =========================
    # PARTY
    # =========================

    if active_companions:

        print(
            "\n=== PARTY ==="
        )

        for companion in active_companions:

            print(
                f"{companion['role']}"
                f" HP:"
                f" {companion['hp']}/"
                f"{companion['max_hp']}"
            )

    # =========================
    # ENEMIES
    # =========================

    print(
        "\n=== ENEMIES ==="
    )

    for index, enemy in enumerate(
        enemies
    ):

        print(
            f"\n[{index}]"
            f" {enemy['name']}"
        )

        print(
            f"HP:"
            f" {enemy['hp']}/"
            f"{enemy['max_hp']}"
        )

        print(
            f"Elite:"
            f" {enemy['elite']}"
        )

        print(
            f"Boss:"
            f" {enemy['boss']}"
        )

# =========================
# REMOVE DEAD ENEMIES
# =========================

def cleanup_defeated_enemies(

    enemies

):

    remaining = []

    for enemy in enemies:

        if enemy["hp"] > 0:

            remaining.append(
                enemy
            )

            continue

        enemy["hp"] = 0

        print(
            f"\n{enemy['name']}"
            " has been defeated!"
        )

        emit(

            "enemy_killed",

            enemy_name=enemy[
                "name"
            ]
        )

    return remaining

# =========================
# PLAYER TURN
# =========================

def player_turn(

    enemies

):

    print(
        "\n1. Attack"
    )

    print(
        "2. Heavy Attack"
    )

    print(
        "3. Heal"
    )

    action = input(
        "\nChoose: "
    ).strip()

    # =========================
    # ATTACK
    # =========================

    if action == "1":

        try:

            target_index = int(

                input(
                    "\nTarget Enemy #: "
                )
            )

            target = enemies[
                target_index
            ]

        except Exception:

            print(
                "\nInvalid target."
            )

            return

        damage = random.randint(
            5,
            12
        )

        damage += (
            player.attack_bonus
        )

        damage += (
            calculate_party_bonus()
        )

        critical = (
            calculate_critical_hit()
        )

        if critical:

            damage *= 2

            print(
                "\nCRITICAL HIT!"
            )

        target["hp"] -= damage

        target["hp"] = max(
            target["hp"],
            0
        )

        print(
            f"\nYou strike"
            f" {target['name']}"
            f" for {damage} damage."
        )

    # =========================
    # HEAVY ATTACK
    # =========================

    elif action == "2":

        try:

            target_index = int(

                input(
                    "\nTarget Enemy #: "
                )
            )

            target = enemies[
                target_index
            ]

        except Exception:

            print(
                "\nInvalid target."
            )

            return

        damage = random.randint(
            15,
            30
        )

        damage += (
            player.attack_bonus
        )

        critical = (
            calculate_critical_hit(
                10
            )
        )

        if critical:

            damage *= 2

            print(
                "\nDEVASTATING CRITICAL!"
            )

        target["hp"] -= damage

        target["hp"] = max(
            target["hp"],
            0
        )

        print(
            f"\nHeavy attack hits"
            f" {target['name']}"
            f" for {damage} damage!"
        )

    # =========================
    # HEAL
    # =========================

    elif action == "3":

        heal = random.randint(
            15,
            30
        )

        player.hp += heal

        player.hp = min(

            player.hp,

            player.max_hp
        )

        # Mirror into world_state so both representations agree.
        world_state["player"]["hp"] = player.hp

        print(
            f"\nYou recover"
            f" {heal} HP."
        )

    else:

        print(
            "\nInvalid action."
        )

# =========================
# COMPANION TURNS
# =========================

def companion_turns(

    enemies

):

    if not active_companions:

        return

    print(
        "\n=== COMPANION TURNS ==="
    )

    for companion in active_companions:

        if companion["hp"] <= 0:

            continue

        if not enemies:

            return

        target = random.choice(
            enemies
        )

        companion_attack(

            companion,

            target
        )

        target["hp"] = max(
            target["hp"],
            0
        )

        ability_roll = random.randint(
            1,
            100
        )

        if ability_roll <= 35:

            use_companion_ability(

                companion,

                target
            )

            target["hp"] = max(
                target["hp"],
                0
            )

# =========================
# ENEMY TURNS
# =========================

def enemy_turns(

    enemies

):

    # =========================
    # LOCAL IMPORTS
    # =========================

    from enemy_manager import (

        use_enemy_ability,

        boss_phase_check
    )

    print(
        "\n=== ENEMY TURNS ==="
    )

    for enemy in enemies:

        if enemy["hp"] <= 0:

            continue

        # =========================
        # BOSS PHASE
        # =========================

        if enemy["boss"]:

            boss_phase_check(
                enemy
            )

        # =========================
        # ENEMY ABILITY
        # =========================

        ability_roll = random.randint(
            1,
            100
        )

        if ability_roll <= 30:

            use_enemy_ability(
                enemy
            )

        # =========================
        # TARGETS
        # =========================

        valid_targets = [

            "player"
        ]

        for companion in active_companions:

            if companion["hp"] > 0:

                valid_targets.append(
                    companion
                )

        chosen_target = random.choice(
            valid_targets
        )

        # =========================
        # DAMAGE
        # =========================

        damage = random.randint(

            int(
                enemy["damage"] * 0.7
            ),

            enemy["damage"]
        )

        critical = (
            calculate_critical_hit(

                enemy[
                    "crit_chance"
                ]
            )
        )

        if critical:

            damage *= 2

            print(
                f"\n{enemy['name']}"
                " lands a CRITICAL strike!"
            )

        # =========================
        # PLAYER TARGET
        # =========================

        if chosen_target == "player":

            if check_evasion(
                player.evasion
            ):

                print(
                    "\nYou evade the attack!"
                )

                continue

            damage -= player.defense

            damage = max(
                damage,
                0
            )

            player.hp -= damage

            player.hp = max(
                player.hp,
                0
            )

            # Mirror into world_state so both representations agree.
            world_state["player"]["hp"] = player.hp

            print(
                f"\n{enemy['name']}"
                f" hits you for"
                f" {damage} damage."
            )

            emit(

                "player_damaged",

                amount=damage
            )

        # =========================
        # COMPANION TARGET
        # =========================

        else:

            chosen_target[
                "hp"
            ] -= damage

            chosen_target[
                "hp"
            ] = max(

                chosen_target[
                    "hp"
                ],

                0
            )

            print(
                f"\n{enemy['name']}"
                f" hits"
                f" {chosen_target['role']}"
                f" for {damage} damage."
            )

# =========================
# PROCESS STATUSES
# =========================

def process_combat_statuses(

    enemies

):

    # =========================
    # PLAYER
    # =========================

    if hasattr(

        player,

        "status_effects"
    ):

        player.hp, player.status_effects = (

            process_status_effects(

                player.hp,

                player.status_effects
            )
        )

        # Mirror into world_state so both representations agree.
        world_state["player"]["hp"] = player.hp

    # =========================
    # ENEMIES
    # =========================

    for enemy in enemies:

        enemy["hp"], enemy[
            "status_effects"
        ] = process_status_effects(

            enemy["hp"],

            enemy[
                "status_effects"
            ]
        )

# =========================
# COMBAT LOOP
# =========================

def combat(

    enemies

):

    # =========================
    # LOCAL IMPORTS
    # =========================

    from encounter_manager import (
        calculate_encounter_difficulty
    )

    print(
        "\n=== COMBAT START ==="
    )

    # Track how many enemies entered so we can award XP after victory
    # even though the list is emptied during cleanup.
    initial_enemy_count = len(enemies)

    try:

        ai_combat_narration(

            "Encounter",

            {

                "enemy_count":
                    len(enemies),

                "difficulty":
                    calculate_encounter_difficulty(
                        enemies
                    ),

                "player_hp":
                    player.hp
            }
        )

    except Exception:

        print(
            "\nDanger surrounds you."
        )

    # =========================
    # MAIN LOOP
    # =========================

    while enemies and player.hp > 0:

        show_combat_status(
            enemies
        )

        # =========================
        # PLAYER TURN
        # =========================

        player_turn(
            enemies
        )

        # =========================
        # COMPANION TURNS
        # =========================

        companion_turns(
            enemies
        )

        # =========================
        # PROCESS STATUS EFFECTS
        # =========================

        process_combat_statuses(
            enemies
        )

        # =========================
        # CLEANUP
        # =========================

        enemies = cleanup_defeated_enemies(
            enemies
        )

        if not enemies:

            break

        # =========================
        # ENEMY TURNS
        # =========================

        enemy_turns(
            enemies
        )

        # =========================
        # TENSION
        # =========================

        change_story_pressure(
            5
        )

        # =========================
        # LOW HP
        # =========================

        if player.hp <= 25:

            print(
                "\nYou are critically wounded!"
            )

    # =========================
    # VICTORY
    # =========================

    if player.hp > 0:

        print(
            "\n=== VICTORY ==="
        )

        # Award XP to every hero in the roster — 15 XP per enemy defeated.
        combat_xp = initial_enemy_count * 15
        if combat_xp > 0:
            award_xp_to_roster(combat_xp)

        try:

            ai_narrate(

                "Narrate the aftermath"
                " of the battle victory."
            )

        except Exception:

            print(
                "\nThe battle is over."
            )

        return True

    # =========================
    # DEFEAT
    # =========================

    print(
        "\n=== DEFEAT ==="
    )

    emit(
        "player_defeated"
    )

    return False

# =========================
# QUICK ENCOUNTER
# =========================

def quick_encounter(

    region_name=None,

    enemy_count=3

):

    # =========================
    # LOCAL IMPORT
    # =========================

    from enemy_manager import (
        generate_random_enemy
    )

    enemies = []

    for _ in range(
        enemy_count
    ):

        enemy = generate_random_enemy(
            region_name
        )

        if enemy:

            enemies.append(
                enemy
            )

    return combat(
        enemies
    )

# =========================
# BOSS ENCOUNTER
# =========================

def boss_encounter(

    boss_name

):

    # =========================
    # LOCAL IMPORT
    # =========================

    from enemy_manager import (
        create_enemy
    )

    boss = create_enemy(
        boss_name
    )

    if not boss:

        print(
            "\nBoss not found."
        )

        return False

    boss["boss"] = True

    return combat(
        [boss]
    )