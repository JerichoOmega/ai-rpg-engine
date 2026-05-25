from datetime import datetime

from world_state import (
    world_state
)

from memory_engine import (
    retrieve_memories
)

from campaign_manager import (
    campaign_state
)

from event_bus import (
    subscribe
)

# =========================
# SESSION STATE
# =========================

session_state = {

    "campaign_title": "Shadows of the Fallen Realm",

    "session_number": 1,

    "chapter": 1,

    "chapter_title": "Rising Shadows",

    "session_history": [],

    "last_played": None
}

# =========================
# START SESSION
# =========================

def start_session():

    session_state[
        "last_played"
    ] = str(
        datetime.now()
    )

    print(
        "\n=== SESSION START ==="
    )

    print(
        "Campaign:",
        session_state[
            "campaign_title"
        ]
    )

    print(
        "Session:",
        session_state[
            "session_number"
        ]
    )

    print(
        "Chapter:",
        session_state[
            "chapter_title"
        ]
    )

    generate_session_recap()

# =========================
# END SESSION
# =========================

def end_session():

    print(
        "\n=== SESSION END ==="
    )

    summary = generate_session_summary()

    session_state[
        "session_history"
    ].append(summary)

    session_state[
        "session_number"
    ] += 1

# =========================
# SESSION SUMMARY
# =========================

def generate_session_summary():

    summary = {

        "session": session_state[
            "session_number"
        ],

        "date": str(
            datetime.now()
        ),

        "chapter": session_state[
            "chapter_title"
        ],

        "world_chaos": world_state[
            "world_conditions"
        ]["world_chaos"],

        "campaign_stage": campaign_state[
            "campaign_stage"
        ]
    }

    print(
        "\n=== SESSION SUMMARY ==="
    )

    print(
        "Session:",
        summary["session"]
    )

    print(
        "Campaign Stage:",
        summary["campaign_stage"]
    )

    print(
        "World Chaos:",
        summary["world_chaos"]
    )

    return summary

# =========================
# SESSION RECAP
# =========================

def generate_session_recap():

    print(
        "\n=== PREVIOUS EVENTS ==="
    )

    memories = retrieve_memories(
        "major_events"
    )

    if len(memories) == 0:

        print(
            "No major events yet."
        )

        return

    recent = memories[-3:]

    for memory in recent:

        print(
            "•",
            memory["memory"]
        )

# =========================
# ADVANCE CHAPTER
# =========================

def advance_chapter():

    session_state[
        "chapter"
    ] += 1

    chapter = session_state[
        "chapter"
    ]

    if chapter == 2:

        session_state[
            "chapter_title"
        ] = "Fractured Kingdoms"

    elif chapter == 3:

        session_state[
            "chapter_title"
        ] = "Age of Ruin"

    elif chapter >= 4:

        session_state[
            "chapter_title"
        ] = "Final Catastrophe"

    print(
        f"\nCampaign advances"
        f" to:"
        f" {session_state['chapter_title']}"
    )

# =========================
# SHOW SESSION HISTORY
# =========================

def show_session_history():

    print(
        "\n=== SESSION HISTORY ==="
    )

    history = session_state[
        "session_history"
    ]

    if len(history) == 0:

        print(
            "No completed sessions."
        )

        return

    for entry in history:

        print(
            "\n• Session",
            entry["session"]
        )

        print(
            "Chapter:",
            entry["chapter"]
        )

        print(
            "Campaign Stage:",
            entry["campaign_stage"]
        )

# =========================
# CAMPAIGN TIMELINE
# =========================

def show_campaign_timeline():

    print(
        "\n=== CAMPAIGN TIMELINE ==="
    )

    memories = retrieve_memories(
        "major_events"
    )

    if len(memories) == 0:

        print(
            "Timeline empty."
        )

        return

    for memory in memories:

        print(
            "•",
            memory["memory"]
        )

# =========================
# EVENT REACTIONS
# =========================

def on_campaign_advanced(

    event_data

):

    act = event_data.get(
        "act"
    )

    print(
        f"\nCampaign reaches"
        f" Act {act}."
    )

    if act >= 2:

        advance_chapter()

def on_world_collapse(

    event_data

):

    print(
        "\nThe campaign enters"
        " a dark new age."
    )

# =========================
# REGISTER EVENTS
# =========================

subscribe(
    "campaign_advanced",
    on_campaign_advanced
)

subscribe(
    "world_collapse",
    on_world_collapse
)