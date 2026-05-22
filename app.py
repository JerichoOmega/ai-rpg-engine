import random
from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "dark-quest-secret-key"

ADVENTURE_LENGTH = 3

CLASSES = {
    "warrior": {
        "hp": 70,
        "attack_bonus": 5,
        "desc": "Heavily armored with great endurance.",
        "icon": "&#9876;",
    },
    "mage": {
        "hp": 45,
        "attack_bonus": 10,
        "desc": "Fragile but devastatingly powerful.",
        "icon": "&#10024;",
    },
    "rogue": {
        "hp": 55,
        "attack_bonus": 7,
        "desc": "Swift and cunning — strikes from shadow.",
        "icon": "&#128481;",
    },
}

QUESTS = [
    "A village is haunted by whispers at night.",
    "A merchant caravan disappeared in the woods.",
    "A mining town has suddenly gone silent.",
    "A royal tomb has been broken into.",
    "A mysterious plague spreads through the kingdom.",
]

LOCATIONS = [
    "inside cursed woods",
    "beneath an ancient castle",
    "under a ruined city",
    "inside frozen caves",
    "within a dark swamp",
]

ENEMIES = {
    "Hidden Cult":      {"hp_min": 15, "hp_max": 25, "special": "summon"},
    "Ancient Dragon":   {"hp_min": 30, "hp_max": 45, "special": "fire"},
    "Corrupted Knight": {"hp_min": 20, "hp_max": 35, "special": "shield"},
    "Shadow Beast":     {"hp_min": 18, "hp_max": 30, "special": "dodge"},
    "Necromancer":      {"hp_min": 20, "hp_max": 40, "special": "heal"},
}

SPECIAL_FLAVOR = {
    "fire":   ("Flames engulf the battlefield!", True),
    "heal":   ("Dark magic crackles — the enemy mends their wounds.", False),
    "dodge":  ("The shadow beast melts into darkness.", False),
    "shield": ("The corrupted knight raises a heavy shield.", False),
    "summon": ("The cultists begin chanting for reinforcements!", False),
}

EVENTS = [
    "You discover a hidden treasure chest.",
    "A wandering merchant appears.",
    "You step into a dangerous trap.",
    "An old traveler gives you advice.",
    "You find an ancient magical shrine.",
]

LOOT_ITEMS = [
    "Iron Sword",
    "Magic Staff",
    "Shadow Dagger",
    "Healing Potion",
    "Dragon Shield",
]

WEAPON_BONUSES = {
    "Iron Sword":    3,
    "Magic Staff":   5,
    "Shadow Dagger": 4,
}

ATTACK_DESCRIPTIONS = [
    "You slash forward with deadly force!",
    "Your weapon crashes into the enemy!",
    "You strike with incredible speed!",
    "A powerful blow lands against the enemy!",
    "Steel clashes as your attack hits hard!",
]

ENEMY_ATTACKS = [
    "The enemy lunges at you!",
    "A brutal strike hits your armor!",
    "Dark magic crashes into you!",
    "The enemy attacks without mercy!",
    "A savage blow knocks you backward!",
]


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def slog(key, msg):
    """Append msg to a session list, safely reassigning so Flask detects the change."""
    lst = session.get(key, [])
    lst.append(msg)
    session[key] = lst


def new_game():
    session.clear()
    session["phase"] = "class_select"
    session["player_gold"] = 25
    session["player_reputation"] = 0
    session["equipped_weapon"] = "Rusty Sword"
    session["weapon_bonus"] = 0
    session["inventory"] = []
    session["current_room"] = 1
    session["cult_defeated"] = False
    session["dragon_defeated"] = False
    session["knight_defeated"] = False
    session["combat_log"] = []
    session["event_log"] = []
    session["rep_log"] = []


def load_encounter():
    enemy_name = random.choice(list(ENEMIES.keys()))
    enemy_hp = random.randint(ENEMIES[enemy_name]["hp_min"], ENEMIES[enemy_name]["hp_max"])
    session["quest"] = random.choice(QUESTS)
    session["location"] = random.choice(LOCATIONS)
    session["enemy_name"] = enemy_name
    session["enemy_hp"] = enemy_hp
    session["enemy_max_hp"] = enemy_hp
    session["enemy_special"] = ENEMIES[enemy_name]["special"]
    session["combat_log"] = []
    session["event_log"] = []
    session["rep_log"] = []


def apply_random_event():
    event = random.choice(EVENTS)
    slog("event_log", f"<span class='log-event'>&#9889; {event}</span>")

    player_hp = session["player_hp"]
    player_gold = session["player_gold"]

    if "treasure" in event:
        gold_found = random.randint(10, 25)
        player_gold += gold_found
        slog("event_log", f"You found <strong>{gold_found} gold</strong>!")
    elif "merchant" in event:
        player_hp += 10
        slog("event_log", "The merchant gives you a healing potion. You gain <strong>10 HP</strong>.")
    elif "trap" in event:
        trap_damage = random.randint(5, 12)
        player_hp -= trap_damage
        slog("event_log", f"The trap deals <strong>{trap_damage} damage</strong>!")
    elif "traveler" in event:
        slog("event_log", "The traveler warns you about the dangers ahead.")
    elif "shrine" in event:
        player_hp += 15
        slog("event_log", "Mystical energy restores your strength. You gain <strong>15 HP</strong>.")

    session["player_hp"] = player_hp
    session["player_gold"] = player_gold


def apply_reputation_event():
    rep = session["player_reputation"]
    player_gold = session["player_gold"]

    slog("rep_log", "<span class='log-event'>&#127758; World Reaction</span>")

    if rep >= 15:
        reward = random.randint(15, 30)
        player_gold += reward
        slog("rep_log", f"The people celebrate your heroic deeds! A village gifts you <strong>{reward} gold</strong>.")
    elif rep <= -15:
        slog("rep_log", "Whispers spread about your cruelty. Travelers scatter from your path.")
    else:
        slog("rep_log", "The world still watches your actions carefully.")

    session["player_gold"] = player_gold


def get_ctx():
    """Build the full template context from session."""
    enemy_hp = session.get("enemy_hp", 0)
    enemy_max_hp = max(session.get("enemy_max_hp", 1), 1)
    player_hp = session.get("player_hp", 0)
    player_max_hp = max(session.get("player_max_hp", 1), 1)

    enemy_pct = max(0, min(100, int(enemy_hp / enemy_max_hp * 100)))
    player_pct = max(0, min(100, int(player_hp / player_max_hp * 100)))

    rep = session.get("player_reputation", 0)
    if rep >= 15:
        rep_label = "Hero"
        rep_class = "rep-hero"
    elif rep <= -15:
        rep_label = "Villain"
        rep_class = "rep-villain"
    else:
        rep_label = "Unknown"
        rep_class = "rep-neutral"

    return {
        "phase":            session.get("phase", "class_select"),
        "player_class":     session.get("player_class", ""),
        "player_hp":        player_hp,
        "player_max_hp":    player_max_hp,
        "player_pct":       player_pct,
        "player_gold":      session.get("player_gold", 0),
        "player_reputation":rep,
        "rep_label":        rep_label,
        "rep_class":        rep_class,
        "attack_bonus":     session.get("attack_bonus", 0),
        "equipped_weapon":  session.get("equipped_weapon", "Rusty Sword"),
        "weapon_bonus":     session.get("weapon_bonus", 0),
        "inventory":        session.get("inventory", []),
        "current_room":     session.get("current_room", 1),
        "adventure_length": ADVENTURE_LENGTH,
        "quest":            session.get("quest", ""),
        "location":         session.get("location", ""),
        "enemy_name":       session.get("enemy_name", ""),
        "enemy_hp":         enemy_hp,
        "enemy_max_hp":     enemy_max_hp,
        "enemy_pct":        enemy_pct,
        "enemy_special":    session.get("enemy_special", ""),
        "enemy_special_flavor": SPECIAL_FLAVOR.get(session.get("enemy_special", ""), ("", False))[0],
        "combat_log":       session.get("combat_log", []),
        "event_log":        session.get("event_log", []),
        "rep_log":          session.get("rep_log", []),
        "cult_defeated":    session.get("cult_defeated", False),
        "dragon_defeated":  session.get("dragon_defeated", False),
        "knight_defeated":  session.get("knight_defeated", False),
        "classes":          CLASSES,
        "loot":             session.get("loot", ""),
    }


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def index():
    if "phase" not in session:
        new_game()
    return render_template("index.html", **get_ctx())


@app.route("/action", methods=["POST"])
def handle_action():
    player_action = request.form.get("action", "")
    phase = session.get("phase", "class_select")

    # ── CLASS SELECTION ───────────────────────────────────────
    if phase == "class_select":
        if player_action in CLASSES:
            session["player_class"] = player_action
            session["player_hp"] = CLASSES[player_action]["hp"]
            session["player_max_hp"] = CLASSES[player_action]["hp"]
            session["attack_bonus"] = CLASSES[player_action]["attack_bonus"]
            load_encounter()
            session["phase"] = "encounter"

    # ── ENCOUNTER (pre-combat briefing) ───────────────────────
    elif phase == "encounter":
        if player_action == "begin":
            session["phase"] = "combat"

    # ── COMBAT ───────────────────────────────────────────────
    elif phase == "combat":
        enemy_name    = session["enemy_name"]
        enemy_hp      = session["enemy_hp"]
        player_hp     = session["player_hp"]
        attack_bonus  = session["attack_bonus"]
        weapon_bonus  = session["weapon_bonus"]

        # ── Player action ──
        if player_action == "attack":
            damage = random.randint(5, 15) + attack_bonus + weapon_bonus
            session["enemy_hp"] = enemy_hp - damage
            slog("combat_log", random.choice(ATTACK_DESCRIPTIONS))
            slog("combat_log", f"You dealt <strong>{damage} damage</strong>.")

        elif player_action == "heal":
            heal = random.randint(8, 15)
            session["player_hp"] = player_hp + heal
            slog("combat_log", "A warm light surrounds you.")
            slog("combat_log", f"You healed <strong>{heal} HP</strong>.")

        elif player_action == "run":
            slog("combat_log", "You escape into the darkness...")
            session["phase"] = "ran"
            return redirect(url_for("index"))

        # Refresh after player action
        enemy_hp  = session["enemy_hp"]
        player_hp = session["player_hp"]

        # ── Check: enemy defeated ──
        if enemy_hp <= 0:
            reward = random.randint(10, 30)
            session["player_gold"] = session["player_gold"] + reward
            slog("combat_log", f"<span class='log-victory'>&#9876; Victory! The {enemy_name} has fallen!</span>")
            slog("combat_log", f"You gained <strong>{reward} gold</strong>.")

            # Loot drop
            loot = random.choice(LOOT_ITEMS)
            inv = session.get("inventory", [])
            inv.append(loot)
            session["inventory"] = inv
            session["loot"] = loot
            slog("combat_log", f"You found: <strong>{loot}</strong>!")

            # Equip if weapon
            if loot in WEAPON_BONUSES:
                session["equipped_weapon"] = loot
                session["weapon_bonus"] = WEAPON_BONUSES[loot]
                slog("combat_log", f"You equipped <strong>{loot}</strong> (+{WEAPON_BONUSES[loot]} ATK).")

            # Story memory
            name_lower = enemy_name.lower()
            if "cult" in name_lower:
                session["cult_defeated"] = True
            elif "dragon" in name_lower:
                session["dragon_defeated"] = True
            elif "knight" in name_lower:
                session["knight_defeated"] = True

            # Random event
            apply_random_event()

            session["phase"] = "post_combat"
            return redirect(url_for("index"))

        # ── Enemy turn ──
        if enemy_hp > 0:
            enemy_damage = random.randint(4, 12)
            session["player_hp"] = player_hp - enemy_damage
            slog("combat_log", f"<span class='log-enemy'>{random.choice(ENEMY_ATTACKS)}</span>")
            slog("combat_log", f"You take <strong>{enemy_damage} damage</strong>.")

            # Special ability
            special = session.get("enemy_special", "")
            flavor, has_extra = SPECIAL_FLAVOR.get(special, ("", False))
            if flavor:
                slog("combat_log", f"<span class='log-special'>{flavor}</span>")

            if special == "fire":
                extra = random.randint(3, 8)
                session["player_hp"] = session["player_hp"] - extra
                slog("combat_log", f"You take <strong>{extra} fire damage</strong>!")
            elif special == "heal":
                heal_amount = random.randint(4, 10)
                session["enemy_hp"] = session["enemy_hp"] + heal_amount
                slog("combat_log", f"The {enemy_name} heals <strong>{heal_amount} HP</strong>.")

        # Check player death
        if session["player_hp"] <= 0:
            session["phase"] = "dead"

    # ── POST COMBAT (loot + random event shown) ───────────────
    elif phase == "post_combat":
        if player_action == "continue":
            session["phase"] = "story_choice"

    # ── STORY CHOICE ──────────────────────────────────────────
    elif phase == "story_choice":
        player_gold       = session["player_gold"]
        player_reputation = session["player_reputation"]

        slog("event_log", "<span class='log-event'>&#128100; A wounded traveler begs for your help.</span>")

        if player_action == "help":
            player_reputation += 5
            slog("event_log", "You kneel and tend to their wounds.")
            slog("event_log", "Reputation <strong>+5</strong>.")
        elif player_action == "ignore":
            slog("event_log", "You step past without a word and continue your journey.")
        elif player_action == "rob":
            gold_stolen = random.randint(10, 25)
            player_gold += gold_stolen
            player_reputation -= 10
            slog("event_log", f"You rob the traveler of <strong>{gold_stolen} gold</strong>!")
            slog("event_log", "Reputation <strong>-10</strong>.")

        session["player_gold"] = player_gold
        session["player_reputation"] = player_reputation

        apply_reputation_event()
        session["phase"] = "reputation"

    # ── REPUTATION (world reaction shown) ─────────────────────
    elif phase == "reputation":
        if player_action == "continue":
            session["current_room"] = session["current_room"] + 1
            if session["current_room"] > ADVENTURE_LENGTH:
                session["phase"] = "won"
            else:
                load_encounter()
                session["phase"] = "encounter"

    # ── END SCREENS ───────────────────────────────────────────
    elif phase in ("dead", "won", "ran"):
        if player_action == "restart":
            new_game()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
