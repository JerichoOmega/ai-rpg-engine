"""
In-game menu for Legacy Questlines
==================================

Thin presentation layer that lets a player browse and play the registered
Legacy Questlines from the main game loop. All quest logic lives in the
frameworks; this only renders a menu and delegates to the shared
:data:`legacy.framework.quest_framework.manager`.
"""

from __future__ import annotations

from legacy.framework import registry
from legacy.framework.quest_framework import manager
from legacy.framework.io import InteractiveIO, set_io


def show_legacy_menu() -> None:
    """Display the Legacy Questline menu and run the player's choice."""
    registry.ensure_legacy_world_state()
    if not registry.is_registered():
        registry.register_all()

    quests = manager.all()

    print("\n=== QUESTS ===")
    for index, quest in enumerate(quests, start=1):
        status = manager.status(quest.id)
        label = quest.civilization or quest.category
        print(f"{index}. {quest.name}  [{quest.category}]  [{status['state']}]"
              f"  -- {label}")
    print(f"{len(quests) + 1}. Back")

    raw = input("\nChoose a quest: ").strip()
    try:
        choice = int(raw)
    except ValueError:
        print("Invalid choice.")
        return

    if choice == len(quests) + 1 or not (1 <= choice <= len(quests)):
        return

    quest = quests[choice - 1]
    print(f"\nBeginning: {quest.name}")
    print(f"Featured companion (recommended, never required): "
          f"{quest.featured_companion or 'none'}")

    previous = set_io(InteractiveIO())
    try:
        manager.play(quest.id)
    finally:
        set_io(previous)
