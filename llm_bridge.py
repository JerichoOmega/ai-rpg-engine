"""
llm_bridge.py
=============
Bridge to the AI language model layer.

All functions currently return hardcoded mock responses. Replace the
mock bodies with real LLM API calls when a model is connected.

Exported functions (called by dm_brain.py, combat.py, dialogue_ai.py):
  - ai_narrate(prompt)                    — print a narrative beat
  - ai_generate_quest()                   — print a quest rumour
  - ai_combat_narration(attacker, ...)    — print combat flavour text
  - ai_dialogue(npc, context)             — return an NPC dialogue line
"""

import random

# =========================
# AI NARRATE
# =========================

_NARRATE_LINES = [
    "The world holds its breath as your actions ripple outward.",
    "Shadows lengthen across the land, hinting at darker times ahead.",
    "The wind carries whispers of great change on the horizon.",
    "History will remember this moment, for better or worse.",
    "Something stirs in the deep places of the world.",
    "The sky darkens as though the heavens themselves take notice.",
    "An uneasy silence falls before the storm.",
]

def ai_narrate(prompt):
    """Generate a narrative beat. Mock implementation — replace with
    a real LLM call when a model is available."""
    print("\n[DM]", random.choice(_NARRATE_LINES))


# =========================
# AI GENERATE QUEST
# =========================

_QUEST_RUMORS = [
    "A merchant whispers of a lost artefact in the eastern ruins.",
    "Travellers report strange lights near the old watchtower.",
    "The guild posts a bounty — dangerous quarry, generous reward.",
    "Scouts have gone missing near the cult's last known stronghold.",
    "A dying soldier clutches a map with trembling hands.",
    "Word spreads of a village whose residents vanished overnight.",
    "An anonymous letter slips under your door, sealed in black wax.",
]

def ai_generate_quest():
    """Generate a new quest hook. Mock implementation."""
    print("\n[Quest Hook]", random.choice(_QUEST_RUMORS))


# =========================
# AI COMBAT NARRATION
# =========================

_COMBAT_LINES = [
    "Steel rings against steel in a deadly dance.",
    "The air crackles with the tension of the fight.",
    "Every blow lands with decisive purpose.",
    "The enemy staggers but refuses to fall.",
    "The battle reaches its fevered peak.",
    "Pain and adrenaline sharpen every sense.",
    "The ground shakes with the force of the exchange.",
]

def ai_combat_narration(attacker=None, defender=None, damage=0):
    """Generate combat flavour text. Mock implementation."""
    print("\n[Combat]", random.choice(_COMBAT_LINES))


# =========================
# AI DIALOGUE
# =========================

_DIALOGUE_LINES = [
    "I have nothing more to say to you.",
    "There are rumours … dark ones. Be careful out there.",
    "The roads are dangerous. Stock up before you leave.",
    "I've heard the cult has been more active lately.",
    "You look like someone who can handle themselves.",
    "Strange times. Strange times indeed.",
    "Keep your blade sharp and your wits sharper.",
]

def ai_dialogue(npc=None, context=None):
    """Generate an NPC dialogue line. Mock implementation.
    Returns a string (does not print directly — caller decides how to
    surface it)."""
    return random.choice(_DIALOGUE_LINES)
