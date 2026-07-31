from world_state import (
    world_state
)

from event_bus import (
    emit
)

from player import (
    sync_player_from_world_state
)

# =========================
# PROGRESSION STATE
# =========================

progression_state = {

    "level": 1,

    "xp": 0,

    "xp_to_next_level": 100,

    "skill_points": 0,

    "world_tier": 1
}

# Maximum hero level — enforced for every roster member.
MAX_LEVEL = 25


# =========================
# XP THRESHOLD HELPER
# =========================

def _xp_threshold(level):
    """XP required to advance FROM `level` to level+1."""
    return 100 + (level - 1) * 50


# =========================
# ROSTER HELPERS
# =========================

def _ensure_player_roster_entry():
    """Seed the player roster entry from current progression_state
    if it does not already exist."""
    if "roster" not in world_state:
        world_state["roster"] = {}
    if "player" not in world_state["roster"]:
        world_state["roster"]["player"] = {
            "level": progression_state["level"],
            "xp": progression_state["xp"],
            "xp_to_next_level": progression_state["xp_to_next_level"],
            "max_hp": world_state["player"]["max_hp"],
            "attack_bonus": world_state["player"]["attack_bonus"],
        }


def _sync_player_xp_state(entry):
    """Lightweight sync — update progression_state and world_state['player']
    XP/level/xp_to_next without firing level-up events.  Called after
    every non-levelling award and when the player is at the level cap."""
    progression_state["level"] = entry["level"]
    progression_state["xp"] = entry["xp"]
    progression_state["xp_to_next_level"] = entry["xp_to_next_level"]
    world_state["player"]["level"] = entry["level"]
    world_state["player"]["xp"] = entry["xp"]
    world_state["player"]["xp_to_next_level"] = entry["xp_to_next_level"]


def _sync_player_from_roster_entry(entry):
    """Full level-up sync — push the player roster entry into
    progression_state and world_state['player'], fire the level-up
    event, and sync the runtime Player object."""
    _sync_player_xp_state(entry)
    progression_state["skill_points"] += 1

    world_state["player"]["max_hp"] = entry["max_hp"]
    world_state["player"]["hp"] = entry["max_hp"]
    world_state["player"]["attack_bonus"] = entry["attack_bonus"]

    emit("player_level_up", level=entry["level"])
    sync_player_from_world_state()
    update_world_tier()


def _sync_companion_combat_stats(companion_name, entry):
    """Push levelled-up stats from the roster entry back into the
    companion's combat-facing dict in companion_manager.COMPANIONS.
    Uses a local import to avoid a circular module-level dependency."""
    try:
        from companion_manager import COMPANIONS
        companion = COMPANIONS.get(companion_name)
        if companion is None:
            return
        companion["max_hp"] = entry["max_hp"]
        # Never exceed the new max hp.
        companion["hp"] = min(
            companion.get("hp", entry["max_hp"]),
            entry["max_hp"]
        )
        if "damage" in entry:
            companion["damage"] = entry["damage"]
    except ImportError:
        pass


# =========================
# PER-HERO LEVEL-UP CHECK
# =========================

def _check_hero_level_up(hero_name, entry):
    """Apply level-ups to a single roster entry up to MAX_LEVEL.
    Returns True if at least one level was gained.

    For companions, also syncs the levelled stats back into
    companion_manager.COMPANIONS so combat uses current values.
    """
    levelled = False
    while (
        entry["level"] < MAX_LEVEL
        and entry["xp"] >= entry["xp_to_next_level"]
    ):
        entry["xp"] -= entry["xp_to_next_level"]
        entry["level"] += 1
        entry["xp_to_next_level"] = _xp_threshold(entry["level"])
        entry["max_hp"] += 20
        entry["attack_bonus"] += 2
        # Companions scale their damage ceiling in step with attack_bonus.
        if hero_name != "player" and "damage" in entry:
            entry["damage"] += 2
        levelled = True

        if hero_name == "player":
            print(
                f"\n=== LEVEL UP ==="
            )
            print(
                f"You are now level"
                f" {entry['level']}!"
            )
            print("\n+20 Max HP")
            print("+2 Attack Bonus")
            print("+1 Skill Point")
        else:
            print(
                f"\n=== {hero_name.upper()}"
                f" LEVEL UP: {entry['level']} ==="
            )
            print("+20 Max HP | +2 Attack Bonus | +2 Damage")

    # Push updated combat stats back to the companion dict immediately.
    if levelled and hero_name != "player":
        _sync_companion_combat_stats(hero_name, entry)

    return levelled


# =========================
# ROSTER-WIDE XP AWARD
# =========================

def award_xp_to_roster(amount):
    """Award XP to every hero in the roster — active and benched.

    This is the canonical XP entry point.  All callers (quests, combat,
    exploration) should use this function so no hero falls behind.

    Cap policy: heroes at MAX_LEVEL receive no further XP.  progression_state
    and world_state['player'] are always kept in sync with the roster entry —
    including when the player is already at cap — so UI and saves reflect the
    correct state regardless of whether a level-up occurred.
    """
    if "roster" not in world_state:
        world_state["roster"] = {}

    _ensure_player_roster_entry()

    for hero_name, entry in world_state["roster"].items():
        if entry["level"] >= MAX_LEVEL:
            # At cap: no XP accumulated beyond this point.
            # Sync progression_state so display and saves stay consistent.
            if hero_name == "player":
                _sync_player_xp_state(entry)
            continue
        entry["xp"] += amount
        levelled = _check_hero_level_up(hero_name, entry)
        if hero_name == "player":
            if levelled:
                _sync_player_from_roster_entry(entry)
            else:
                # No level-up, but keep progression_state current.
                _sync_player_xp_state(entry)

    print(
        f"\nAll heroes gained"
        f" {amount} XP."
    )


# =========================
# ADD EXPERIENCE
# =========================

def add_experience(

    amount

):
    """Award XP to all roster members. Thin wrapper kept for
    backward compatibility with existing callers."""

    award_xp_to_roster(amount)

# =========================
# SAVE / LOAD RECONCILIATION
# =========================

def reconcile_player_roster_before_save():
    """Called at save time, after sync_world_state_from_player().

    sync_world_state_from_player() may overwrite world_state["player"]
    level/max_hp/attack_bonus from the runtime Player object, which can
    diverge from the roster entry if any legacy code path mutated the
    player object directly.  This function re-asserts the roster entry as
    the authoritative source for all progression fields before the save
    file is written.

    If no roster entry exists yet, one is seeded from world_state["player"]
    so the save file always contains a valid roster.
    """
    if "roster" not in world_state:
        world_state["roster"] = {}
    if "player" not in world_state["roster"]:
        _ensure_player_roster_entry()
        return

    entry = world_state["roster"]["player"]
    # Roster wins for progression fields; keep both representations aligned.
    world_state["player"]["level"] = entry["level"]
    world_state["player"]["max_hp"] = entry["max_hp"]
    world_state["player"]["attack_bonus"] = entry["attack_bonus"]
    world_state["player"]["xp"] = entry["xp"]
    world_state["player"]["xp_to_next_level"] = entry["xp_to_next_level"]
    progression_state["level"] = entry["level"]
    progression_state["xp"] = entry["xp"]
    progression_state["xp_to_next_level"] = entry["xp_to_next_level"]


def reconcile_player_roster_after_load():
    """Called at load time, after sync_player_from_world_state().

    Three responsibilities:

    1. Player entry — preserve a valid saved roster entry if it exists;
       only reconstruct it from world_state["player"] when the saved
       roster has no player entry (legacy saves) or the levels disagree.

    2. Companion entries — for every companion in COMPANIONS (all saved
       companions, active or benched), either sync the companion's combat
       dict FROM its saved roster entry, or seed a new roster entry from
       the companion's saved stats when none exists (legacy saves).

    3. progression_state alignment — ensure progression_state agrees with
       the final player roster entry so the first XP award after load
       uses the correct level rather than module-init values.
    """
    if "roster" not in world_state:
        world_state["roster"] = {}

    ws = world_state["player"]
    ws_level = ws.get("level", progression_state.get("level", 1))

    # ── 1. Player roster entry ──
    player_entry = world_state["roster"].get("player")
    if player_entry is None or player_entry.get("level") != ws_level:
        # Missing (legacy save) or diverged — rebuild from world_state["player"].
        world_state["roster"]["player"] = {
            "level": ws_level,
            "xp": ws.get("xp", 0),
            "xp_to_next_level": ws.get(
                "xp_to_next_level", _xp_threshold(ws_level)
            ),
            "max_hp": ws.get("max_hp", 100),
            "attack_bonus": ws.get("attack_bonus", 5),
        }
    else:
        # Valid saved entry — trust it but push its progression fields
        # back into world_state["player"] to keep them consistent.
        world_state["player"]["level"] = player_entry["level"]
        world_state["player"]["xp"] = player_entry["xp"]
        world_state["player"]["xp_to_next_level"] = player_entry["xp_to_next_level"]
        world_state["player"]["max_hp"] = player_entry["max_hp"]
        world_state["player"]["attack_bonus"] = player_entry["attack_bonus"]

    # Align progression_state with the final player entry.
    final_entry = world_state["roster"]["player"]
    progression_state["level"] = final_entry["level"]
    progression_state["xp"] = final_entry["xp"]
    progression_state["xp_to_next_level"] = final_entry["xp_to_next_level"]

    # ── 2. Companion entries ──
    try:
        from companion_manager import COMPANIONS
        player_level = final_entry["level"]
        for name, companion in COMPANIONS.items():
            existing = world_state["roster"].get(name)
            if existing:
                # Saved roster entry exists — sync companion combat dict FROM it.
                companion["max_hp"] = existing["max_hp"]
                companion["hp"] = min(
                    companion.get("hp", existing["max_hp"]),
                    existing["max_hp"]
                )
                if "damage" in existing:
                    companion["damage"] = existing["damage"]
            else:
                # No roster entry — legacy save.  Treat current saved stats
                # as the level-1 base (since they pre-date scaling) and seed
                # an entry at the current player level.
                base_max_hp = companion.get("max_hp", 100)
                base_damage = companion.get("damage", 10)
                scaled_max_hp = base_max_hp + (player_level - 1) * 20
                scaled_damage = base_damage + (player_level - 1) * 2
                companion["max_hp"] = scaled_max_hp
                companion["hp"] = min(
                    companion.get("hp", scaled_max_hp), scaled_max_hp
                )
                companion["damage"] = scaled_damage
                world_state["roster"][name] = {
                    "level": player_level,
                    "xp": 0,
                    "xp_to_next_level": _xp_threshold(player_level),
                    "max_hp": scaled_max_hp,
                    "attack_bonus": 5 + (player_level - 1) * 2,
                    "damage": scaled_damage,
                    "base_max_hp": base_max_hp,
                    "base_damage": base_damage,
                }
    except ImportError:
        pass


# =========================
# LEVEL UP CHECK (player only — legacy path)
# =========================

def check_level_up():
    """Legacy single-player level-up check.  Now delegates to the
    roster entry so the level-25 cap and stat scaling stay consistent."""
    _ensure_player_roster_entry()
    entry = world_state["roster"]["player"]

    # Keep the roster entry in sync with progression_state before checking.
    entry["xp"] = progression_state["xp"]
    entry["level"] = progression_state["level"]
    entry["xp_to_next_level"] = progression_state["xp_to_next_level"]

    levelled = _check_hero_level_up("player", entry)
    if levelled:
        _sync_player_from_roster_entry(entry)

# =========================
# WORLD TIER
# =========================

def update_world_tier():

    level = progression_state[
        "level"
    ]

    old_tier = progression_state[
        "world_tier"
    ]

    if level >= 20:

        progression_state[
            "world_tier"
        ] = 5

    elif level >= 15:

        progression_state[
            "world_tier"
        ] = 4

    elif level >= 10:

        progression_state[
            "world_tier"
        ] = 3

    elif level >= 5:

        progression_state[
            "world_tier"
        ] = 2

    else:

        progression_state[
            "world_tier"
        ] = 1

    new_tier = progression_state[
        "world_tier"
    ]

    if new_tier > old_tier:

        print(
            f"\n=== WORLD TIER"
            f" INCREASED:"
            f" {new_tier} ==="
        )

        emit(

            "world_tier_changed",

            tier=new_tier
        )

# =========================
# SCALE ENEMY POWER
# =========================

def scale_enemy_power(

    base_value

):

    tier = progression_state[
        "world_tier"
    ]

    multiplier = 1 + (
        (tier - 1) * 0.35
    )

    return int(
        base_value * multiplier
    )

# =========================
# GET WORLD TIER
# =========================

def get_world_tier():

    return progression_state[
        "world_tier"
    ]

# =========================
# QUEST REWARDS
# =========================

def reward_quest_completion(

    xp_reward=50,

    gold_reward=25

):

    add_experience(
        xp_reward
    )

    world_state[
        "player"
    ][
        "gold"
    ] += gold_reward

    print(
        "\nQuest rewards:"
    )

    print(
        f"+{xp_reward} XP"
    )

    print(
        f"+{gold_reward} Gold"
    )

    emit(

        "quest_reward_given",

        xp=xp_reward,

        gold=gold_reward
    )

# =========================
# SHOW PROGRESSION
# =========================

def show_progression():

    print(
        "\n=== PROGRESSION ==="
    )

    print(
        f"Level:"
        f" {progression_state['level']}"
    )

    print(
        f"XP:"
        f" {progression_state['xp']}"
        f"/"
        f"{progression_state['xp_to_next_level']}"
    )

    print(
        f"Skill Points:"
        f" {progression_state['skill_points']}"
    )

    print(
        f"World Tier:"
        f" {progression_state['world_tier']}"
    )