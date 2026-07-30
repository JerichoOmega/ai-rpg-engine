"""
dm_brain.py
===========

SINGLE SOURCE OF TRUTH for AI Dungeon Master orchestration / pacing.

Responsibilities of this module:

- Owns the DM's narrative state (`dm_state`): current focus, story
  pressure, emotional tone, priority threat, active story threads, and
  short-term session counters (recent battles / recent story beats).

- Pressure-based pacing: `story_pressure` (0-100) determines the
  current narrative focus (recovery / exploration / crisis). That
  focus decides what the DM does next each loop tick, via
  `update_dm_brain()` -- this is the function `main.py` calls once per
  game loop iteration.

- Session-flow smoothing: helper functions that nudge `story_pressure`
  based on recent play patterns (too much combat -> ease off, too much
  downtime -> escalate) or campaign stage. These are available but not
  currently invoked by `main.py` (they weren't invoked before this
  merge either -- see history note below).

- Reacting to game events (`enemy_killed`, `world_collapse`,
  `quest_completed`, `narrative_encounter`) by adjusting
  `story_pressure` and the session counters.

This module does NOT call any real LLM. `ai_narrate()` /
`ai_generate_quest()` (imported from llm_bridge.py) currently return a
hardcoded mock response -- that is unchanged by this refactor and is
out of scope for it.

--------------------------------------------------------------------
Merge history (this refactor)
--------------------------------------------------------------------
This module previously had a parallel, largely-redundant counterpart,
`ai_director.py`, which maintained its own separate `tension` /
`session_phase` state and subscribed to an overlapping set of events
(`enemy_killed`, `world_collapse`, plus `narrative_encounter` and
`quest_completed`, which dm_brain.py did not previously handle).

`ai_director.py`'s own dispatcher (`direct_gameplay()`) duplicated
`update_dm_brain()`'s logic almost exactly (same three phases, same
generator calls) and was never called from anywhere in the codebase,
so it has been dropped rather than merged -- carrying it forward would
just be two copies of the same dispatch logic in one file.

Everything else non-dead from `ai_director.py` has been folded in
below: `evaluate_session_flow()`, `evaluate_campaign_pressure()`,
`reset_session_trackers()`, `show_director_state()` (renamed
`show_dm_state()`), and the `recent_battles` / `recent_story_events`
counters. These were not called by `main.py` before the merge and
still are not -- they are preserved as available-but-dormant
functions, same status as before, so this does not change gameplay
behavior.

`ai_director.py` has been deleted. `dm_state["story_pressure"]` is now
the single tension/pacing metric for the whole DM system, replacing
the old parallel `director_state["tension"]` (which nothing outside
`ai_director.py` ever read).

The only observable behavior change: `enemy_killed` and
`world_collapse` were previously each handled by two independent
subscribers (one in dm_brain.py, one in ai_director.py) that adjusted
two different, disconnected numbers. Now each event is handled once,
adjusting the single `story_pressure` value that actually drives
`update_dm_brain()`'s dispatch -- which is the only one of the two
numbers that was ever affecting gameplay in the first place.
"""

import random

from world_state import (
    world_state
)

from campaign_manager import (
    campaign_state,
    generate_campaign_event
)

from encounter_manager import (
    generate_encounter,
    generate_narrative_encounter
)

from npc_manager import (
    random_npc_event
)

from region_manager import (
    random_region_event
)

from llm_bridge import (
    ai_narrate,
    ai_generate_quest
)

from memory_engine import (
    retrieve_memories
)

from event_bus import (
    emit,
    subscribe
)

# =========================
# DM STATE
# =========================
# story_pressure (0-100) is the single tension/pacing metric for the
# whole DM system. Replaces ai_director.py's separate
# director_state["tension"].
dm_state = {
    "current_focus": "exploration",
    "story_pressure": 25,
    "emotional_tone": "neutral",
    "priority_threat": "shadow_cult",
    "active_threads": [],
    # merged in from ai_director.director_state:
    "recent_battles": 0,
    "recent_story_events": 0
}

# =========================
# STORY PRESSURE
# =========================
def change_story_pressure(amount):
    """Adjust story_pressure and re-evaluate the current narrative focus.

    Merged equivalent of ai_director.change_tension(): now updates the
    single dm_state["story_pressure"] instead of a separate
    director_state["tension"].
    """
    dm_state["story_pressure"] += amount
    dm_state["story_pressure"] = max(0, min(dm_state["story_pressure"], 100))
    evaluate_story_state()

# =========================
# EVALUATE STATE
# =========================
def evaluate_story_state():
    pressure = dm_state["story_pressure"]
    if pressure <= 25:
        dm_state["current_focus"] = "recovery"
    elif pressure <= 60:
        dm_state["current_focus"] = "exploration"
    else:
        dm_state["current_focus"] = "crisis"

# =========================
# SHOW DM STATE
# =========================
def show_dm_state():
    """Merged from ai_director.show_director_state()."""
    print("\n=== DM BRAIN STATE ===")
    print("Story Pressure:", dm_state["story_pressure"])
    print("Focus:", dm_state["current_focus"])

# =========================
# MAIN DM UPDATE
# =========================
# This is the function main.py calls once per game loop iteration.
# Unchanged from the pre-merge version.
def update_dm_brain():
    evaluate_story_state()
    focus = dm_state["current_focus"]

    print("\n=== DM BRAIN ===")

    # ── RECOVERY ──
    if focus == "recovery":
        generate_narrative_encounter()
        random_npc_event()
        try:
            ai_narrate("Generate a calm emotional moment after recent conflict.")
        except Exception:
            print("\nThe world briefly calms.")

    # ── EXPLORATION ──
    elif focus == "exploration":
        roll = random.randint(1, 100)
        if roll <= 50:
            try:
                ai_generate_quest()
            except Exception:
                print("\nRumors spread of danger.")
        else:
            random_region_event()

    # ── CRISIS ──
    elif focus == "crisis":
        generate_campaign_event()
        generate_encounter()
        try:
            ai_narrate("Narrate a major campaign crisis escalation.")
        except Exception:
            print("\nThe campaign spirals into chaos.")

# =========================
# SESSION FLOW
# =========================
# Merged from ai_director.evaluate_session_flow(). Not currently called
# from anywhere -- ai_director's version wasn't called either. Kept
# available for future wiring; calling it is a decision for a later
# task, not this refactor.
def evaluate_session_flow():
    battles = dm_state["recent_battles"]
    story_events = dm_state["recent_story_events"]

    if battles >= 3:
        print("\nDM Brain slows combat pacing.")
        change_story_pressure(-15)
    elif story_events >= 3:
        print("\nDM Brain escalates tension.")
        change_story_pressure(15)

# =========================
# CAMPAIGN ESCALATION
# =========================
# Merged from ai_director.evaluate_campaign_pressure(). Same status as
# evaluate_session_flow() above: available, not currently called.
def evaluate_campaign_pressure():
    stage = campaign_state["campaign_stage"]
    if stage == "world_crisis":
        change_story_pressure(20)
    elif stage == "final_catastrophe":
        change_story_pressure(35)

# =========================
# RESET SESSION TRACKERS
# =========================
# Merged from ai_director.reset_session_trackers().
def reset_session_trackers():
    dm_state["recent_battles"] = 0
    dm_state["recent_story_events"] = 0

# =========================
# EVENT REACTIONS
# =========================
def on_enemy_killed(event_data):
    dm_state["recent_battles"] += 1
    change_story_pressure(5)

def on_world_collapse(event_data):
    change_story_pressure(25)

def on_narrative_encounter(event_data):
    """Merged from ai_director.on_narrative_encounter. dm_brain.py did
    not previously subscribe to this event; ai_director.py did."""
    dm_state["recent_story_events"] += 1
    change_story_pressure(-5)

def on_quest_completed(event_data):
    """Merged from ai_director.on_quest_completed. dm_brain.py did not
    previously subscribe to this event; ai_director.py did."""
    print("\nDM Brain recognizes story progression.")
    change_story_pressure(-10)

# =========================
# REGISTER EVENTS
# =========================
subscribe("enemy_killed", on_enemy_killed)
subscribe("world_collapse", on_world_collapse)
subscribe("narrative_encounter", on_narrative_encounter)
subscribe("quest_completed", on_quest_completed)
