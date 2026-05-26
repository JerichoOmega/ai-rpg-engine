# =========================
# PROMPT MANAGER
# =========================

# Centralized AI prompt architecture
# for the AI Dungeon Master engine.

# This system manages:
# - tone consistency
# - narration styles
# - NPC personalities
# - combat narration
# - memory prioritization
# - context formatting
# - prompt construction

# =========================
# BASE SYSTEM PROMPT
# =========================

BASE_SYSTEM_PROMPT = """

You are an AI Dungeon Master
running a persistent dark fantasy campaign.

You are responsible for:
- maintaining lore consistency
- respecting world history
- remembering player actions
- respecting NPC relationships
- maintaining emotional continuity
- creating immersive storytelling
- maintaining campaign pacing
- supporting long-term narrative arcs

You are NOT writing a novel.

You are running a living tabletop RPG world.

Your narration should:
- feel immersive
- remain emotionally grounded
- react dynamically to player actions
- preserve continuity
- avoid contradictions
- support emergent storytelling

"""

# =========================
# EMOTIONAL TONES
# =========================

EMOTIONAL_TONES = {

    "hopeful":

        """
        Tone should feel:
        - adventurous
        - optimistic
        - emotionally uplifting
        - inspiring
        """,

    "neutral":

        """
        Tone should feel:
        - grounded
        - immersive
        - natural
        - realistic
        """,

    "uncertain":

        """
        Tone should feel:
        - tense
        - mysterious
        - uneasy
        - suspenseful
        """,

    "desperate":

        """
        Tone should feel:
        - emotionally heavy
        - dangerous
        - grim
        - unstable
        """,

    "apocalyptic":

        """
        Tone should feel:
        - catastrophic
        - terrifying
        - hopeless
        - world-ending
        """
}

# =========================
# NARRATION STYLES
# =========================

NARRATION_STYLES = {

    "dark_fantasy":

        """
        Use:
        - atmospheric descriptions
        - grounded realism
        - dark fantasy imagery
        - emotional tension
        - immersive environmental storytelling
        """,

    "heroic":

        """
        Use:
        - cinematic storytelling
        - inspiring moments
        - epic emotional beats
        - heroic fantasy tone
        """,

    "grimdark":

        """
        Use:
        - brutal realism
        - hopeless atmosphere
        - moral ambiguity
        - harsh survival themes
        """
}

# =========================
# NPC SPEAKING STYLES
# =========================

NPC_STYLES = {

    "noble":

        """
        Speak:
        - formally
        - intelligently
        - diplomatically
        - with authority
        """,

    "mercenary":

        """
        Speak:
        - bluntly
        - practically
        - with hardened realism
        - casually
        """,

    "cultist":

        """
        Speak:
        - mysteriously
        - fanatically
        - cryptically
        - with unsettling confidence
        """,

    "scholar":

        """
        Speak:
        - thoughtfully
        - analytically
        - with historical references
        - intellectually
        """,

    "villager":

        """
        Speak:
        - simply
        - naturally
        - emotionally
        - realistically
        """
}

# =========================
# COMBAT STYLES
# =========================

COMBAT_STYLES = {

    "cinematic":

        """
        Narrate combat:
        - dynamically
        - cinematically
        - with dramatic pacing
        - with vivid action
        """,

    "brutal":

        """
        Narrate combat:
        - violently
        - realistically
        - emphasizing injuries
        - emphasizing danger
        - emphasizing desperation
        """,

    "tactical":

        """
        Narrate combat:
        - strategically
        - focusing on positioning
        - focusing on decisions
        - focusing on battlefield flow
        """
}

# =========================
# QUEST FORMAT
# =========================

QUEST_FORMAT = """

Return quest information EXACTLY
in the following format:

Title:
Objective:
Reward:
Complication:
Narrative Hook:

"""

# =========================
# MEMORY FORMATTING
# =========================

def format_memories(

    memories,
    limit=5

):

    if not memories:

        return "No significant memories."

    formatted = ""

    recent_memories = memories[-limit:]

    for memory in recent_memories:

        importance = memory.get(
            "importance",
            "minor"
        )

        text = memory.get(
            "memory",
            ""
        )

        formatted += (
            f"\n- [{importance.upper()}]"
            f" {text}"
        )

    return formatted

# =========================
# MEMORY PRIORITIZATION
# =========================

def prioritize_memories(

    memories

):

    priority_order = {

        "legendary": 4,

        "major": 3,

        "moderate": 2,

        "minor": 1
    }

    sorted_memories = sorted(

        memories,

        key=lambda memory:

            priority_order.get(

                memory.get(
                    "importance",
                    "minor"
                ),

                1
            ),

        reverse=True
    )

    return sorted_memories

# =========================
# CONTEXT TRUNCATION
# =========================

def truncate_context(

    text,
    max_length=6000

):

    if len(text) <= max_length:

        return text

    truncated = text[
        :max_length
    ]

    truncated += (

        "\n\n[OLDER CONTEXT TRUNCATED]"
    )

    return truncated

# =========================
# BUILD SYSTEM PROMPT
# =========================

def build_system_prompt(

    emotional_tone="neutral",
    narration_style="dark_fantasy"

):

    prompt = BASE_SYSTEM_PROMPT

    # =========================
    # EMOTIONAL TONE
    # =========================

    tone_prompt = EMOTIONAL_TONES.get(

        emotional_tone,

        EMOTIONAL_TONES[
            "neutral"
        ]
    )

    prompt += (
        "\n=== EMOTIONAL TONE ===\n"
    )

    prompt += tone_prompt

    # =========================
    # NARRATION STYLE
    # =========================

    style_prompt = NARRATION_STYLES.get(

        narration_style,

        NARRATION_STYLES[
            "dark_fantasy"
        ]
    )

    prompt += (
        "\n=== NARRATION STYLE ===\n"
    )

    prompt += style_prompt

    return prompt

# =========================
# BUILD NPC STYLE
# =========================

def build_npc_style(

    npc_role

):

    style = NPC_STYLES.get(

        npc_role,

        """
        Speak naturally and realistically.
        """
    )

    return style

# =========================
# BUILD COMBAT STYLE
# =========================

def build_combat_style(

    combat_type="cinematic"

):

    style = COMBAT_STYLES.get(

        combat_type,

        COMBAT_STYLES[
            "cinematic"
        ]
    )

    return style

# =========================
# BUILD QUEST FORMAT
# =========================

def build_quest_format():

    return QUEST_FORMAT

# =========================
# BUILD CONTEXT BLOCK
# =========================

def build_context_block(

    context_data

):

    context = ""

    for key, value in context_data.items():

        context += (
            f"\n=== {key.upper()} ===\n"
        )

        context += f"{value}\n"

    return context

# =========================
# BUILD FULL PROMPT
# =========================

def build_full_prompt(

    context,
    request,
    emotional_tone="neutral",
    narration_style="dark_fantasy"

):

    system_prompt = build_system_prompt(

        emotional_tone,

        narration_style
    )

    full_prompt = f"""

{system_prompt}

=== CAMPAIGN CONTEXT ===

{context}

=== CURRENT REQUEST ===

{request}

Respond naturally as a tabletop
Dungeon Master while maintaining:
- narrative consistency
- emotional continuity
- world realism
- campaign immersion

"""

    return truncate_context(
        full_prompt
    )

# =========================
# BUILD DIALOGUE PROMPT
# =========================

def build_dialogue_prompt(

    npc_name,
    npc_role,
    relationship,
    context,
    request,
    emotional_tone="neutral"

):

    npc_style = build_npc_style(
        npc_role
    )

    system_prompt = build_system_prompt(
        emotional_tone
    )

    prompt = f"""

{system_prompt}

=== NPC ===

Name: {npc_name}

Role: {npc_role}

Relationship: {relationship}

=== NPC SPEAKING STYLE ===

{npc_style}

=== CAMPAIGN CONTEXT ===

{context}

=== PLAYER INTERACTION ===

{request}

Generate immersive NPC dialogue
that:
- matches personality
- respects relationship history
- reflects emotional tone
- reacts to campaign state
- feels natural and believable

"""

    return truncate_context(
        prompt
    )

# =========================
# BUILD COMBAT PROMPT
# =========================

def build_combat_prompt(

    enemy_name,
    combat_state,
    context,
    combat_style="cinematic",
    emotional_tone="desperate"

):

    style = build_combat_style(
        combat_style
    )

    system_prompt = build_system_prompt(
        emotional_tone
    )

    prompt = f"""

{system_prompt}

=== COMBAT STYLE ===

{style}

=== ENEMY ===

{enemy_name}

=== COMBAT STATE ===

{combat_state}

=== CAMPAIGN CONTEXT ===

{context}

Narrate this combat encounter:
- dynamically
- emotionally
- cinematically
- while respecting campaign tone

"""

    return truncate_context(
        prompt
    )

# =========================
# BUILD QUEST PROMPT
# =========================

def build_quest_prompt(

    context,
    emotional_tone="uncertain"

):

    system_prompt = build_system_prompt(
        emotional_tone
    )

    prompt = f"""

{system_prompt}

=== CAMPAIGN CONTEXT ===

{context}

Generate a dynamic quest that:
- fits the current campaign
- supports long-term storytelling
- respects faction tensions
- reflects emotional tone
- feels immersive

{QUEST_FORMAT}

"""

    return truncate_context(
        prompt
    )

# =========================
# BUILD NARRATION PROMPT
# =========================

def build_narration_prompt(

    context,
    request,
    emotional_tone="neutral",
    narration_style="dark_fantasy"

):

    return build_full_prompt(

        context=context,

        request=request,

        emotional_tone=emotional_tone,

        narration_style=narration_style
    )