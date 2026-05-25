# =========================
# LLM BRIDGE
# =========================

# This file acts as the
# communication layer between
# the game engine and future AI models.

# =========================
# IMPORTS
# =========================

from world_state import (
    world_state
)

from dm_brain import (
    dm_state
)

from campaign_manager import (
    campaign_state
)

from memory_engine import (
    retrieve_memories
)

from npc_manager import (
    NPCS
)

from region_manager import (
    REGIONS
)

# =========================
# CONTEXT BUILDER
# =========================

def build_context():

    context = {

        "current_region":

            world_state[
                "regions"
            ]["current_region"],

        "world_chaos":

            world_state[
                "world_conditions"
            ]["world_chaos"],

        "campaign_stage":

            campaign_state[
                "campaign_stage"
            ],

        "emotional_tone":

            dm_state[
                "emotional_tone"
            ],

        "story_pressure":

            dm_state[
                "story_pressure"
            ],

        "active_threads":

            dm_state[
                "active_threads"
            ],

        "major_memories":

            retrieve_memories(
                "major_events"
            )[-5:]
    }

    return context

# =========================
# CONTEXT FORMATTER
# =========================

def format_context(

    context

):

    formatted = ""

    formatted += (
        f"\nCurrent Region:"
        f" {context['current_region']}"
    )

    formatted += (
        f"\nWorld Chaos:"
        f" {context['world_chaos']}"
    )

    formatted += (
        f"\nCampaign Stage:"
        f" {context['campaign_stage']}"
    )

    formatted += (
        f"\nEmotional Tone:"
        f" {context['emotional_tone']}"
    )

    formatted += (
        f"\nStory Pressure:"
        f" {context['story_pressure']}"
    )

    formatted += (
        "\n\nActive Story Threads:"
    )

    for thread in context[
        "active_threads"
    ]:

        formatted += (
            f"\n- {thread}"
        )

    formatted += (
        "\n\nRecent Major Events:"
    )

    for memory in context[
        "major_memories"
    ]:

        formatted += (
            f"\n- {memory['memory']}"
        )

    return formatted

# =========================
# BASE SYSTEM PROMPT
# =========================

def build_system_prompt():

    system_prompt = """

You are an AI Dungeon Master
running a dynamic dark fantasy campaign.

Your goals are:

- Maintain lore consistency
- Respect campaign history
- React to player choices
- Maintain emotional continuity
- Narrate vividly
- Avoid contradictions
- Preserve long-term story arcs
- Respect faction relationships
- Respect NPC memory
- Respect world state changes

You are NOT writing a novel.

You are running a living tabletop campaign.

"""

    return system_prompt

# =========================
# NARRATION PROMPT
# =========================

def build_narration_prompt(

    situation

):

    context = build_context()

    formatted_context = format_context(
        context
    )

    prompt = f"""

{build_system_prompt()}

=== CAMPAIGN CONTEXT ===

{formatted_context}

=== CURRENT SITUATION ===

{situation}

Narrate this scene naturally
as a tabletop Dungeon Master.

"""

    return prompt

# =========================
# DIALOGUE PROMPT
# =========================

def build_dialogue_prompt(

    npc_name,
    situation

):

    npc = NPCS.get(
        npc_name
    )

    if not npc:

        return None

    context = build_context()

    formatted_context = format_context(
        context
    )

    prompt = f"""

{build_system_prompt()}

=== NPC INFO ===

Name: {npc_name}

Role: {npc['role']}

Faction: {npc['faction']}

Relationship: {npc['relationship']}

Region: {npc['region']}

=== CAMPAIGN CONTEXT ===

{formatted_context}

=== CURRENT SITUATION ===

{situation}

Generate immersive NPC dialogue
that matches:
- the world state
- campaign tone
- faction alignment
- emotional tone
- relationship history

"""

    return prompt

# =========================
# QUEST PROMPT
# =========================

def build_quest_prompt():

    context = build_context()

    formatted_context = format_context(
        context
    )

    prompt = f"""

{build_system_prompt()}

=== CAMPAIGN CONTEXT ===

{formatted_context}

Generate a dynamic quest that:
- fits the campaign stage
- respects faction conflicts
- uses current world tension
- supports long-term storytelling
- feels like tabletop D&D

Return:
- quest title
- objective
- reward
- complication
- narrative hook

"""

    return prompt

# =========================
# COMBAT PROMPT
# =========================

def build_combat_prompt(

    enemy_name,
    combat_state

):

    context = build_context()

    formatted_context = format_context(
        context
    )

    prompt = f"""

{build_system_prompt()}

=== CAMPAIGN CONTEXT ===

{formatted_context}

=== ENEMY ===

{enemy_name}

=== COMBAT STATE ===

{combat_state}

Narrate this combat encounter:
- dynamically
- cinematically
- with emotional tension
- while maintaining campaign tone

"""

    return prompt

# =========================
# MOCK AI RESPONSE
# =========================

# Temporary placeholder until
# real LLM API integration.

def generate_ai_response(

    prompt

):

    print(
        "\n=== AI PROMPT SENT ==="
    )

    print(prompt)

    mock_response = """

[MOCK AI RESPONSE]

The storm deepens over the marshlands
as distant chanting echoes through
the fog-covered ruins...

"""

    return mock_response

# =========================
# AI NARRATION
# =========================

def ai_narrate(

    situation

):

    prompt = build_narration_prompt(
        situation
    )

    response = generate_ai_response(
        prompt
    )

    print(
        "\n=== AI NARRATION ==="
    )

    print(response)

# =========================
# AI DIALOGUE
# =========================

def ai_dialogue(

    npc_name,
    situation

):

    prompt = build_dialogue_prompt(

        npc_name,
        situation
    )

    response = generate_ai_response(
        prompt
    )

    print(
        "\n=== AI DIALOGUE ==="
    )

    print(response)

# =========================
# AI QUEST
# =========================

def ai_generate_quest():

    prompt = build_quest_prompt()

    response = generate_ai_response(
        prompt
    )

    print(
        "\n=== AI QUEST ==="
    )

    print(response)

# =========================
# AI COMBAT
# =========================

def ai_combat_narration(

    enemy_name,
    combat_state

):

    prompt = build_combat_prompt(

        enemy_name,
        combat_state
    )

    response = generate_ai_response(
        prompt
    )

    print(
        "\n=== AI COMBAT NARRATION ==="
    )

    print(response)