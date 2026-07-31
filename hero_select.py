"""
hero_select.py
==============

Hero selection screen shown at new game start.

Public API
----------
select_hero() -> None
    Display the roster, prompt for a choice, and apply the selected
    hero's data to world_state["player"] and the Player object.

apply_hero(hero_key: str) -> None
    Programmatically apply a hero by key (used by tests and future
    custom-hero path); also updates player.py's Player object so that
    combat.py's direct `player.*` attribute reads stay in sync.
"""

from hero_roster import HERO_ROSTER, HERO_ORDER

from world_state import world_state, ensure_world_state_defaults

from equipment_system import equipment, equip_slot_only

from skill_tree import player_skills

from progression_manager import progression_state

from quest_manager import active_quests, completed_quests

from world_event_manager import (
    active_world_events,
    completed_world_events,
)

from economy_manager import economy_state

from story_manager import story_state

from dialogue_manager import npc_relationships

from relationship_manager import social_state

from companion_manager import active_companions

from dm_brain import dm_state


# =========================
# APPLY HERO
# =========================

def apply_hero(hero_key):
    """
    Write the chosen hero's starting data into world_state["player"]
    and sync the Player object used by combat.py.

    Accepts either a lower-case roster key ("talos") or the hero's
    display name ("Talos") — both work so callers don't have to
    normalise before calling.
    """

    key = hero_key.lower()

    if key not in HERO_ROSTER:

        # Try matching by display name
        for roster_key, data in HERO_ROSTER.items():

            if data["name"].lower() == key:

                key = roster_key

                break

        else:

            raise ValueError(
                f"Unknown hero key: {hero_key!r}. "
                f"Valid keys: {list(HERO_ROSTER.keys())}"
            )

    hero = HERO_ROSTER[key]

    # ── Write into world_state["player"] ──────────────────────────
    # Preserve all existing keys (e.g. any schema defaults not in
    # hero data) by only updating the keys the hero defines.

    player_ws = world_state["player"]

    player_ws["name"]             = hero["name"]
    player_ws["class"]            = hero["player_class"]
    player_ws["race"]             = hero["race"]
    player_ws["hp"]               = hero["hp"]
    player_ws["max_hp"]           = hero["max_hp"]
    player_ws["attack_bonus"]     = hero["attack_bonus"]
    player_ws["defense"]          = hero["defense"]
    player_ws["dodge"]            = hero["dodge"]
    player_ws["resource_name"]    = hero["resource_name"]
    player_ws["resource"]         = hero["resource"]
    player_ws["max_resource"]     = hero["max_resource"]
    player_ws["gold"]             = hero["gold"]
    player_ws["equipped_weapon"]  = hero["equipped_weapon"]
    player_ws["weapon_bonus"]     = hero["weapon_bonus"]

    # Build inventory: start from the full roster list, then remove
    # exactly one copy of each starting-equipment item (it moves into
    # its slot).  Duplicates (e.g. Ronan's two Short Swords) and
    # consumables (Healing Potion, Repair Kit) remain in the bag.
    _inv = list(hero["inventory"])
    _starting_eq = hero.get("starting_equipment", {})
    for _item_key in _starting_eq.values():
        if _item_key in _inv:
            _inv.remove(_item_key)

    player_ws["inventory"] = _inv
    player_ws["level"]            = hero["level"]
    player_ws["xp"]               = hero["xp"]
    player_ws["xp_to_next_level"] = hero["xp_to_next_level"]
    # Always reset magic_power to 0 at hero selection — heroes have no
    # starting magic; skills grant it during play.  Without this reset,
    # a prior session's persisted magic_power could bleed into the new hero.
    player_ws["magic_power"]      = 0

    # Store the roster key so save/load can identify which hero was
    # chosen (used for dialogue hooks, companion reactions, etc.)
    player_ws["hero_key"] = key

    # ── Populate equipment slots for all starting items ────────────
    # equip_slot_only() records each item in its slot WITHOUT adding
    # its stat bonus — the hero roster's attack_bonus/defense already
    # include each item's contribution.  This ensures later
    # unequip/swap operations (which call remove_item_stats) correctly
    # subtract the bonuses rather than treating slots as empty.
    for _item_key in _starting_eq.values():
        equip_slot_only(_item_key)

    # ── Sync the Player object (used by combat.py) ─────────────────
    # combat.py imports `player` from player.py and reads `.hp`,
    # `.attack_bonus`, etc. directly. Keep these in sync so both
    # paths see the same values.
    # sync_player_from_world_state() reads back from world_state so
    # it picks up the values we just wrote above.

    from player import sync_player_from_world_state

    sync_player_from_world_state()


# =========================
# DISPLAY ROSTER
# =========================

def _show_roster():

    print(
        "\n=== CHOOSE YOUR HERO ==="
    )

    print(
        "\nFive heroes stand ready."
        " Each has walked a different road."
        "\nChoose the one whose story"
        " you want to continue.\n"
    )

    for index, key in enumerate(HERO_ORDER, start=1):

        hero = HERO_ROSTER[key]

        print(
            f"  {index}. {hero['name']}"
            f"  [{hero['race']} — {hero['player_class']}]"
        )

        print(
            f"     {hero['key_trait']}"
        )

        print(
            f"     HP {hero['max_hp']}"
            f"  |  ATK +{hero['attack_bonus']}"
            f"  |  DEF {hero['defense']}"
            f"  |  DODGE {hero['dodge']}"
            f"  |  {hero['resource_name']} {hero['max_resource']}"
        )

        print(
            f"     Starting gear:"
            f" {', '.join(hero['inventory'])}"
            f"  |  {hero['gold']} gold\n"
        )


# =========================
# SELECT HERO
# =========================

def select_hero():
    """
    Show the hero roster and prompt the player to pick one.
    Loops until a valid selection is made; typing the hero's
    name (e.g. "Eleanor") is accepted as well as the number.
    Applies the choice to world_state["player"] before returning.
    """

    valid_numbers = {
        str(i): HERO_ORDER[i - 1]
        for i in range(1, len(HERO_ORDER) + 1)
    }

    valid_names = {
        HERO_ROSTER[key]["name"].lower(): key
        for key in HERO_ORDER
    }

    while True:

        _show_roster()

        raw = input(
            "Enter a number (1–5) or"
            " a hero name: "
        ).strip()

        # Match by number
        if raw in valid_numbers:

            chosen_key = valid_numbers[raw]

            break

        # Match by name (case-insensitive)
        if raw.lower() in valid_names:

            chosen_key = valid_names[raw.lower()]

            break

        print(
            "\nUnrecognised choice."
            " Please enter a number"
            " from 1 to 5, or a"
            " hero name.\n"
        )

    hero = HERO_ROSTER[chosen_key]

    # ── Full new-game reset ────────────────────────────────────────
    # Clear every global that carries per-run state so that no prior
    # session's progress leaks into the freshly chosen hero.

    # 1. world_state (quests, factions, regions, inventory, etc.)
    world_state.clear()
    ensure_world_state_defaults()

    # 2. Equipment slots — previously equipped items must not persist.
    for slot in list(equipment.keys()):
        equipment[slot] = None

    # 3. Player runtime state — status effects bleed into first combat.
    from player import player as _player
    _player.status_effects = []

    # 4. Skill points and unlocked skills — skills grant stat bonuses
    #    that are captured by sync_world_state_from_player(); leaving
    #    them set would double-apply those bonuses on the new hero.
    player_skills["available_points"] = 3
    player_skills["unlocked_skills"]  = []

    # 5. Progression state — level/XP/world_tier from a prior run must
    #    not persist into the new hero's session or it mismatches the
    #    world_state["player"] level=1 fields set by apply_hero().
    progression_state["level"]            = 1
    progression_state["xp"]              = 0
    progression_state["xp_to_next_level"] = 100
    progression_state["skill_points"]     = 0
    progression_state["world_tier"]       = 1

    # 6. Manager globals serialised by save_manager — each must start
    #    fresh so prior-run quest/story/faction/companion/dm state
    #    does not bleed into the new playthrough.
    active_quests.clear()
    completed_quests.clear()
    active_world_events.clear()
    completed_world_events.clear()
    active_companions.clear()
    npc_relationships.clear()

    economy_state.update({
        "inflation": 1.0,
        "global_stability": 75,
        "scarcity": 20,
    })
    story_state.update({
        "campaign_phase":   1,
        "active_theme":     "survival",
        "main_story_arc":   "shadow_rising",
        "story_progress":   0,
        "major_story_flags": {},
    })
    social_state.update({
        "fear":   0,
        "respect": 0,
        "infamy":  0,
        "renown":  0,
    })
    dm_state.update({
        "current_focus":         "exploration",
        "story_pressure":        25,
        "emotional_tone":        "neutral",
        "priority_threat":       "shadow_cult",
        "active_threads":        [],
        "recent_battles":        0,
        "recent_story_events":   0,
    })

    apply_hero(chosen_key)

    print(
        f"\nYou have chosen"
        f" {hero['name']}."
    )

    print(
        f"\"{hero['key_trait']}\""
    )

    print(
        "\nYour adventure begins...\n"
    )
