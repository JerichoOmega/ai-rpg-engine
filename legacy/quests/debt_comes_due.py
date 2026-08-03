"""The Debt Comes Due -- flagship Legacy Civilization Questline."""

from legacy.framework.quest_framework import load_quest, Quest
from legacy.framework import companion_affinity
from legacy.quests import load_quest_data


def build() -> Quest:
    return load_quest(load_quest_data("debt_comes_due.json"))


def register_banter() -> None:
    companion_affinity.register_banter(
        "debt.opening", "talos",
        "My hometown took in strangers once. Look where the road can lead.")
    companion_affinity.register_banter(
        "debt.crisis", "talos",
        "Steel and stone -- goblin and human -- it's all one wall now. Hold it!")
    companion_affinity.register_banter(
        "debt.resolution", "talos",
        "New hands, new marks on the gateposts. That's how a town grows.")
