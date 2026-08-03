"""What the Forest Carries -- Mossroot stewardship Legacy Questline."""

from legacy.framework.quest_framework import load_quest, Quest
from legacy.framework import companion_affinity
from legacy.quests import load_quest_data


def build() -> Quest:
    return load_quest(load_quest_data("what_the_forest_carries.json"))


def register_banter() -> None:
    companion_affinity.register_banter(
        "forest.silent", "corwin",
        "A quiet forest isn't peaceful. It's holding its breath. Listen.")
    companion_affinity.register_banter(
        "forest.crossing", "corwin",
        "The grey in the water -- it's the Ward bleeding out. We're close.")
    companion_affinity.register_banter(
        "forest.reunion", "corwin",
        "You held the heart while they held the people. That's stewardship, "
        "both halves of it.")
