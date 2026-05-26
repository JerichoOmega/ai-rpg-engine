# =========================
# LLM BRIDGE
# =========================

# This file acts as the bridge
# between the game engine and
# future AI language models.

# Responsibilities:
# - context collection
# - prompt construction
# - AI request routing
# - response handling
# - fallback management
# - future API integration

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

from prompt_manager import (

    build_narration_prompt,

    build_dialogue_prompt,

    build_combat_prompt,

    build_quest_prompt,

    format_memories,

    prioritize_memories
)

# =========================
# CONTEXT COLLECTION
# =========================

def build_context():

    # =========================
    # BASIC WORLD INFO
    # =========================

    current_region = world_state[
        "regions"
    ]["current_region"]

    region_data = REGIONS.get(
        current_region,
        {}
    )

    world_chaos = world_state[
        "world_conditions"
    ]["world_chaos"]

    # =========================
    # CAMPAIGN INFO
    # =========================

    campaign_stage = campaign_state[
        "campaign_stage"
    ]

    emotional_tone = dm_state[
        "emotional_tone"
    ]

    story_pressure = dm_state[
        "story_pressure"
    ]

    active_threads = dm_state[
        "active_threads"
    ]

    # =========================
    # MEMORIES
    # =========================

    memories = retrieve_memories(
        "major_events"
    )

    prioritized_memories = (
        prioritize_memories(
            memories
        )
    )

    formatted_memories = (
        format_memories(
            prioritized_memories,
            limit=5
        )
    )

    # =========================
    # CONTEXT BLOCK
    # =========================

    context = f"""

Current Region:
{current_region}

Region Description:
{region_data.get('description', 'Unknown region.')}

World Chaos:
{world_chaos}

Campaign Stage:
{campaign_stage}

Emotional Tone:
{emotional_tone}

Story Pressure:
{story_pressure}

Active Story Threads:
{active_threads}

Recent Major Memories:
{formatted_memories}

"""

    return context

# =========================
# MOCK AI RESPONSE
# =========================

# Temporary placeholder until
# real API integration exists.

def generate_ai_response(

    prompt

):

    print(
        "\n=== AI PROMPT ==="
    )

    print(prompt)

    mock_response = """

[MOCK AI RESPONSE]

Dark clouds gather over the ruined
kingdom as distant bells echo
through the cold night air...

"""

    return mock_response

# =========================
# AI NARRATION
# =========================

def ai_narrate(

    request,

    emotional_tone=None,

    narration_style="dark_fantasy"

):

    context = build_context()

    if emotional_tone is None:

        emotional_tone = dm_state[
            "emotional_tone"
        ]

    prompt = build_narration_prompt(

        context=context,

        request=request,

        emotional_tone=emotional_tone,

        narration_style=narration_style
    )

    response = generate_ai_response(
        prompt
    )

    print(
        "\n=== AI NARRATION ==="
    )

    print(response)

    return response

# =========================
# AI DIALOGUE
# =========================

def ai_dialogue(

    npc_name,
    request

):

    npc = NPCS.get(
        npc_name
    )

    if not npc:

        print(
            "\nUnknown NPC."
        )

        return None

    context = build_context()

    emotional_tone = dm_state[
        "emotional_tone"
    ]

    prompt = build_dialogue_prompt(

        npc_name=npc_name,

        npc_role=npc[
            "role"
        ],

        relationship=npc[
            "relationship"
        ],

        context=context,

        request=request,

        emotional_tone=emotional_tone
    )

    response = generate_ai_response(
        prompt
    )

    print(
        "\n=== AI DIALOGUE ==="
    )

    print(response)

    return response

# =========================
# AI COMBAT NARRATION
# =========================

def ai_combat_narration(

    enemy_name,
    combat_state

):

    context = build_context()

    emotional_tone = "desperate"

    prompt = build_combat_prompt(

        enemy_name=enemy_name,

        combat_state=combat_state,

        context=context,

        combat_style="cinematic",

        emotional_tone=emotional_tone
    )

    response = generate_ai_response(
        prompt
    )

    print(
        "\n=== AI COMBAT ==="
    )

    print(response)

    return response

# =========================
# AI QUEST GENERATION
# =========================

def ai_generate_quest():

    context = build_context()

    emotional_tone = dm_state[
        "emotional_tone"
    ]

    prompt = build_quest_prompt(

        context=context,

        emotional_tone=emotional_tone
    )

    response = generate_ai_response(
        prompt
    )

    print(
        "\n=== AI QUEST ==="
    )

    print(response)

    return response

# =========================
# AI SCENE GENERATION
# =========================

def ai_generate_scene(

    location,
    scene_type="exploration"

):

    request = f"""

Generate a detailed scene for:

Location:
{location}

Scene Type:
{scene_type}

Focus on:
- atmosphere
- immersion
- environmental storytelling
- emotional tone

"""

    return ai_narrate(
        request
    )

# =========================
# AI VILLAIN MONOLOGUE
# =========================

def ai_villain_monologue(

    villain_name,
    villain_goal

):

    request = f"""

Generate a villain monologue.

Villain:
{villain_name}

Goal:
{villain_goal}

The monologue should:
- feel intelligent
- feel threatening
- reflect campaign history
- maintain emotional tension

"""

    return ai_narrate(

        request,

        emotional_tone="desperate"
    )

# =========================
# AI WORLD EVENT
# =========================

def ai_world_event():

    request = """

Generate a major dynamic world event.

The event should:
- impact the campaign world
- reflect faction tensions
- escalate narrative pressure
- feel immersive
- create future consequences

"""

    return ai_narrate(

        request,

        emotional_tone="uncertain"
    )

# =========================
# AI EMOTIONAL MOMENT
# =========================

def ai_emotional_scene(

    situation

):

    request = f"""

Generate an emotional character moment.

Situation:
{situation}

Focus on:
- character emotion
- atmosphere
- subtle storytelling
- immersion

"""

    return ai_narrate(

        request,

        emotional_tone="hopeful"
    )

# =========================
# FUTURE API PLACEHOLDER
# =========================

# Future real integrations:
#
# - OpenAI API
# - Claude API
# - Local LLMs
# - Streaming responses
# - Structured JSON outputs
# - Token optimization
# - Context compression
#
# Replace:
# generate_ai_response()
#
# with:
# real API calls later.