import random

# =========================
# POWER STRIKE
# =========================

def power_strike(enemy_hp, attack_bonus):

    damage = random.randint(12, 20)

    damage += attack_bonus

    enemy_hp -= damage

    print("\nPOWER STRIKE!")
    print("You deal", damage, "massive damage!")

    return enemy_hp


# =========================
# FIREBALL
# =========================

def fireball(enemy_hp):

    damage = random.randint(10, 18)

    enemy_hp -= damage

    print("\nFIREBALL erupts across the battlefield!")
    print("Enemy takes", damage, "fire damage!")

    return enemy_hp


# =========================
# BACKSTAB
# =========================

def backstab(enemy_hp):

    crit = random.randint(1, 100)

    if crit <= 35:

        damage = random.randint(18, 30)

        print("\nCRITICAL BACKSTAB!")

    else:

        damage = random.randint(8, 15)

    enemy_hp -= damage

    print("Enemy takes", damage, "damage!")

    return enemy_hp