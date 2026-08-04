"""The Jammed Mill -- a small side quest that validates the framework.

Deliberately ordinary content (one NPC, one location, one problem, one speech
check, one optional fight, one meaningful choice, one visible Living-World
change) built with the *same* reusable systems as the Legacy Questlines and
*no* new engine code.
"""

from legacy.framework.quest_framework import load_quest, Quest
from legacy.framework import companion_affinity
from legacy.quests import load_quest_data


def build() -> Quest:
    return load_quest(load_quest_data("the_jammed_mill.json"))


def register_banter() -> None:
    companion_affinity.register_banter(
        "mill.arrival", "kael",
        "A jammed mill and a worried miller. Not every day has to be a war.")
    companion_affinity.register_banter(
        "mill.fight", "kael",
        "Rats in the sluice -- corrupted ones at that. Watch the teeth.")
