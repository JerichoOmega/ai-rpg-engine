import random
from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "rpg-secret-key-2024"

QUESTS = [
    "A village is haunted by whispers at night.",
    "A merchant caravan disappeared in the woods.",
    "A mining town has suddenly gone silent.",
    "A royal tomb has been broken into.",
    "A mysterious plague spreads through the kingdom."
]

LOCATIONS = [
    "inside cursed woods",
    "beneath an ancient castle",
    "under a ruined city",
    "inside frozen caves",
    "within a dark swamp"
]

ENEMIES = [
    "Hidden Cult",
    "Ancient Dragon",
    "Corrupted Knight",
    "Shadow Beast",
    "Necromancer"
]

ATTACK_DESCRIPTIONS = [
    "You slash forward with deadly force!",
    "Your weapon crashes into the enemy!",
    "You strike with incredible speed!",
    "A powerful blow lands against the enemy!",
    "Steel clashes as your attack hits hard!"
]

ENEMY_ATTACKS = [
    "The enemy lunges at you!",
    "A brutal strike hits your armor!",
    "Dark magic crashes into you!",
    "The enemy attacks without mercy!",
    "A savage blow knocks you backward!"
]

ADVENTURE_LENGTH = 3


def new_game():
    session.clear()
    session["player_hp"] = 50
    session["player_gold"] = 25
    session["current_room"] = 1
    session["cult_defeated"] = False
    session["dragon_defeated"] = False
    session["knight_defeated"] = False
    session["phase"] = "encounter"
    session["log"] = []
    load_encounter()


def load_encounter():
    session["quest"] = random.choice(QUESTS)
    session["location"] = random.choice(LOCATIONS)
    session["enemy_name"] = random.choice(ENEMIES)
    session["enemy_hp"] = random.randint(15, 30)
    session["log"] = []


def add_log(msg):
    log = session.get("log", [])
    log.append(msg)
    session["log"] = log


@app.route("/")
def index():
    if "player_hp" not in session:
        new_game()
    return render_template("index.html",
                           player_hp=session["player_hp"],
                           player_gold=session["player_gold"],
                           current_room=session["current_room"],
                           adventure_length=ADVENTURE_LENGTH,
                           quest=session.get("quest"),
                           location=session.get("location"),
                           enemy_name=session.get("enemy_name"),
                           enemy_hp=session.get("enemy_hp"),
                           phase=session.get("phase"),
                           log=session.get("log", []),
                           cult_defeated=session.get("cult_defeated"),
                           dragon_defeated=session.get("dragon_defeated"),
                           knight_defeated=session.get("knight_defeated"))


@app.route("/action", methods=["POST"])
def action():
    action = request.form.get("action")
    phase = session.get("phase")

    if phase == "encounter":
        enemy_name = session["enemy_name"]
        enemy_hp = session["enemy_hp"]
        player_hp = session["player_hp"]

        if action == "attack":
            damage = random.randint(5, 15)
            session["enemy_hp"] = enemy_hp - damage
            add_log(random.choice(ATTACK_DESCRIPTIONS))
            add_log(f"You dealt <strong>{damage}</strong> damage!")

        elif action == "heal":
            heal = random.randint(8, 15)
            session["player_hp"] = player_hp + heal
            add_log("A warm light surrounds you.")
            add_log(f"You healed <strong>{heal}</strong> HP!")

        elif action == "run":
            add_log("You escape into the darkness...")
            session["phase"] = "ran"
            return redirect(url_for("index"))

        enemy_hp = session["enemy_hp"]
        player_hp = session["player_hp"]

        if enemy_hp <= 0:
            reward = random.randint(10, 30)
            session["player_gold"] = session["player_gold"] + reward
            add_log(f"<strong>Victory!</strong> The {enemy_name} has fallen.")
            add_log(f"You gained <strong>{reward}</strong> gold!")

            name_lower = enemy_name.lower()
            if "cult" in name_lower:
                session["cult_defeated"] = True
            elif "dragon" in name_lower:
                session["dragon_defeated"] = True
            elif "knight" in name_lower:
                session["knight_defeated"] = True

            session["current_room"] = session["current_room"] + 1

            if session["current_room"] > ADVENTURE_LENGTH:
                session["phase"] = "won"
            else:
                session["phase"] = "victory"

            return redirect(url_for("index"))

        if player_hp > 0:
            enemy_damage = random.randint(4, 12)
            session["player_hp"] = player_hp - enemy_damage
            add_log(random.choice(ENEMY_ATTACKS))
            add_log(f"You take <strong>{enemy_damage}</strong> damage!")

        if session["player_hp"] <= 0:
            session["phase"] = "dead"

    elif phase == "victory" and action == "continue":
        load_encounter()
        session["phase"] = "encounter"

    elif phase in ("dead", "won", "ran") and action == "restart":
        new_game()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
