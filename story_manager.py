from world_state import (
    world_state,
    remember_choice,
    remember_major_event,
    discover_lore,
    activate_world_event
)

from event_bus import (
    subscribe
)

# =========================
# ENEMY KILLED
# =========================

def on_enemy_killed(

    event_data

):

    enemy_name = event_data.get(
        "enemy_name"
    )

    # =========================
    # CULT TRACKING
    # =========================

    if enemy_name == "hidden cult":

        remember_choice(
            "fighting_cult"
        )

        print(
            "\nRumors spread of your"
            " war against the cult."
        )

        world_state[
            "factions"
        ]["shadow_cult"] -= 2

    # =========================
    # DRAGON MEMORY
    # =========================

    elif enemy_name == "ancient dragon":

        remember_major_event(
            "dragon_slain"
        )

        world_state[
            "story_memory"
        ]["dragon_slain"] = True

        print(
            "\nThe world trembles after"
            " the dragon's death."
        )

# =========================
# QUEST COMPLETED
# =========================

def on_quest_completed(

    event_data

):

    quest_name = event_data.get(
        "quest_name"
    )

    # =========================
    # CULT HUNT
    # =========================

    if quest_name == "Cult Hunt":

        activate_world_event(
            "Cult Retaliation"
        )

        print(
            "\nThe Shadow Cult begins"
            " hunting you."
        )

    # =========================
    # DRAGON SLAYER
    # =========================

    elif quest_name == "Dragon Slayer":

        discover_lore(
            "dragon_prophecy"
        )

        print(
            "\nAncient prophecies begin"
            " resurfacing across the world."
        )

# =========================
# REGION DISCOVERED
# =========================

def on_region_discovered(

    event_data

):

    region_name = event_data.get(
        "region_name"
    )

    print(
        f"\nYou have entered"
        f" {region_name}."
    )

    if region_name == "arcane_ruins":

        discover_lore(
            "ancient_magic"
        )

        print(
            "\nYou uncover traces"
            " of forbidden magic."
        )

# =========================
# PLAYER CHOICE
# =========================

def on_player_choice(

    event_data

):

    choice = event_data.get(
        "choice"
    )

    if choice == "mercy":

        world_state[
            "story_memory"
        ]["merciful"] = True

        print(
            "\nYour compassion becomes"
            " widely known."
        )

    elif choice == "ruthless":

        world_state[
            "story_memory"
        ]["ruthless"] = True

        print(
            "\nFear spreads in your wake."
        )

# =========================
# WORLD EVENTS
# =========================

def on_world_event(

    event_data

):

    event_name = event_data.get(
        "event_name"
    )

    print(
        f"\nWorld Event Triggered:"
        f" {event_name}"
    )

    if event_name == "Cult Retaliation":

        world_state[
            "world_conditions"
        ]["world_chaos"] += 5

        print(
            "\nCult assassins spread"
            " chaos across the land."
        )

# =========================
# COMPANION EVENTS
# =========================

def on_companion_joined(

    event_data

):

    companion_name = event_data.get(
        "companion_name"
    )

    print(
        f"\n{companion_name}"
        " becomes part of your legend."
    )

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "enemy_killed",
    on_enemy_killed
)

subscribe(
    "quest_completed",
    on_quest_completed
)

subscribe(
    "region_discovered",
    on_region_discovered
)

subscribe(
    "player_choice",
    on_player_choice
)

subscribe(
    "world_event",
    on_world_event
)

subscribe(
    "companion_joined",
    on_companion_joined
)