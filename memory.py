# =========================
# NARRATIVE MEMORY SYSTEM
# =========================

story_memory = {

    "spared_cultist": False,

    "executed_cultist": False,

    "recruited_cultist": False,

    "joined_shadow_cult": False,

    "dragon_slain": False,

    "used_dark_magic": False
}

# =========================
# UPDATE MEMORY
# =========================

def update_memory(
    story_memory,
    memory_key
):

    if memory_key in story_memory:

        story_memory[memory_key] = True

        print(
            "\nMemory Updated:",
            memory_key
        )

    return story_memory