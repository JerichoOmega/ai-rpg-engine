# =========================
# DYNAMIC NPC DIALOGUE
# =========================

def npc_dialogue(
    factions,
    story_memory
):

    print("\n=== NPC DIALOGUE ===")

    # =========================
    # SHADOW CULT REACTION
    # =========================

    if story_memory["joined_shadow_cult"]:

        print(
            "\nA nervous merchant whispers:"
        )

        print(
            "\"I've heard rumors about you..."
            " dark rumors.\""
        )

    # =========================
    # DRAGON SLAYER REACTION
    # =========================

    elif story_memory["dragon_slain"]:

        print(
            "\nVillagers cheer as you arrive."
        )

        print(
            "\"The Dragon Slayer has returned!\""
        )

    # =========================
    # KINGDOM ENEMY
    # =========================

    elif factions["kingdom"] <= -50:

        print(
            "\nThe city guards glare at you."
        )

        print(
            "\"You're not welcome here.\""
        )

    # =========================
    # KINGDOM ALLY
    # =========================

    elif factions["kingdom"] >= 50:

        print(
            "\nA royal knight salutes you."
        )

        print(
            "\"The kingdom stands with you.\""
        )

    # =========================
    # DEFAULT
    # =========================

    else:

        print(
            "\nTravelers quietly gather around"
            " the tavern fire."
        )

        print(
            "\"Danger grows across the land...\""
        )