# =========================
# BOSS PHASE SYSTEM
# =========================

def check_boss_phase(
    enemy_name,
    enemy_hp,
    max_enemy_hp
):

    phase = 1

    special_attack = None

    # =========================
    # DRAGON PHASES
    # =========================

    if enemy_name == "ancient dragon":

        # PHASE 3

        if enemy_hp <= max_enemy_hp * 0.25:

            phase = 3

            special_attack = "meteor"

        # PHASE 2

        elif enemy_hp <= max_enemy_hp * 0.5:

            phase = 2

            special_attack = "inferno"

    # =========================
    # NECROMANCER PHASES
    # =========================

    elif enemy_name == "necromancer":

        # PHASE 3

        if enemy_hp <= max_enemy_hp * 0.25:

            phase = 3

            special_attack = "death_magic"

        # PHASE 2

        elif enemy_hp <= max_enemy_hp * 0.5:

            phase = 2

            special_attack = "summon_undead"

    # =========================
    # SHADOW BEAST PHASES
    # =========================

    elif enemy_name == "shadow beast":

        if enemy_hp <= max_enemy_hp * 0.3:

            phase = 2

            special_attack = "shadow_frenzy"

    return phase, special_attack