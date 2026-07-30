from world_state import (

    world_state,

    remember_choice,

    remember_major_event,

    discover_lore,

    activate_world_event
)

from event_bus import (

    subscribe,

    emit
)

# =========================
# STORY STATE
# =========================

story_state = {

    "campaign_phase": 1,

    "active_theme": "survival",

    "main_story_arc": "shadow_rising",

    "story_progress": 0,

    "major_story_flags": {}
}

# =========================
# STORY THEMES
# =========================

STORY_THEMES = {

    "survival": {

        "description":
            "The world struggles to endure."
    },

    "revenge": {

        "description":
            "Old wounds fuel conflict."
    },

    "corruption": {

        "description":
            "Darkness spreads across the land."
    },

    "redemption": {

        "description":
            "Hope rises from despair."
    },

    "conquest": {

        "description":
            "Power reshapes the world."
    }
}

# =========================
# ADVANCE STORY
# =========================

def advance_story(

    amount

):

    story_state[
        "story_progress"
    ] += amount

    print(
        f"\nStory Progress:"
        f" {story_state['story_progress']}"
    )

    evaluate_story_phase()

# =========================
# STORY PHASES
# =========================

def evaluate_story_phase():

    progress = story_state[
        "story_progress"
    ]

    current_phase = story_state[
        "campaign_phase"
    ]

    # =========================
    # PHASE 2
    # =========================

    if progress >= 25 and current_phase < 2:

        story_state[
            "campaign_phase"
        ] = 2

        print(
            "\nThe world grows unstable."
        )

        activate_world_event(
            "corruption_surge"
        )

    # =========================
    # PHASE 3
    # =========================

    elif progress >= 50 and current_phase < 3:

        story_state[
            "campaign_phase"
        ] = 3

        print(
            "\nFactions spiral toward war."
        )

        activate_world_event(
            "civil_war"
        )

    # =========================
    # PHASE 4
    # =========================

    elif progress >= 75 and current_phase < 4:

        story_state[
            "campaign_phase"
        ] = 4

        print(
            "\nThe world nears collapse."
        )

        activate_world_event(
            "void_breach"
        )

# =========================
# CHANGE STORY THEME
# =========================

def change_story_theme(

    theme_name

):

    if theme_name not in STORY_THEMES:

        print(
            "\nUnknown story theme."
        )

        return

    story_state[
        "active_theme"
    ] = theme_name

    print(
        f"\nStory Theme Changed:"
        f" {theme_name}"
    )

# =========================
# MAIN STORY ARC
# =========================

def set_main_story_arc(

    arc_name

):

    story_state[
        "main_story_arc"
    ] = arc_name

    print(
        f"\nMain Story Arc:"
        f" {arc_name}"
    )

# =========================
# STORY FLAGS
# =========================

def set_story_flag(

    flag_name,

    value=True

):

    story_state[
        "major_story_flags"
    ][flag_name] = value

# =========================
# ENEMY KILLED
# =========================

def on_enemy_killed(

    event_data

):

    enemy_name = event_data.get(
        "enemy_name"
    )

    if enemy_name == "cultist":

        remember_choice(
            "fighting_cult"
        )

        advance_story(
            2
        )

        print(
            "\nRumors spread of your"
            " war against the cult."
        )

        world_state[
            "factions"
        ]["shadow_cult"] -= 2

    elif enemy_name == "ashen_guardian":

        remember_major_event(
            "guardian_slain"
        )

        set_story_flag(
            "guardian_slain"
        )

        advance_story(
            10
        )

        print(
            "\nThe balance of power shifts."
        )

# =========================
# QUEST COMPLETED
# =========================

def on_quest_completed(

    event_data

):

    quest = event_data.get(
        "quest"
    )

    if not quest:

        return

    quest_type = quest.get(
        "type"
    )

    advance_story(
        5
    )

    if quest_type == "faction":

        print(
            "\nPolitical tensions rise."
        )

    elif quest_type == "world_event":

        print(
            "\nThe world changes forever."
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

    advance_story(
        1
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

        change_story_theme(
            "redemption"
        )

        print(
            "\nYour compassion becomes"
            " widely known."
        )

    elif choice == "ruthless":

        world_state[
            "story_memory"
        ]["ruthless"] = True

        change_story_theme(
            "conquest"
        )

        print(
            "\nFear spreads in your wake."
        )

    elif choice == "corrupt":

        change_story_theme(
            "corruption"
        )

        print(
            "\nDarkness consumes your path."
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

        advance_story(
            5
        )

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

    advance_story(
        3
    )

# =========================
# STORY SUMMARY
# =========================

def show_story_summary():

    print(
        "\n=== STORY SUMMARY ==="
    )

    print(
        f"Campaign Phase:"
        f" {story_state['campaign_phase']}"
    )

    print(
        f"Theme:"
        f" {story_state['active_theme']}"
    )

    print(
        f"Story Arc:"
        f" {story_state['main_story_arc']}"
    )

    print(
        f"Story Progress:"
        f" {story_state['story_progress']}"
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