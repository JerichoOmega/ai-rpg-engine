"""Eternal Forge -- Dwarven Kingdom Legacy Questline."""

from legacy.framework.quest_framework import load_quest, Quest
from legacy.framework import companion_affinity
from legacy.quests import load_quest_data


def build() -> Quest:
    return load_quest(load_quest_data("eternal_forge.json"))


def register_banter() -> None:
    companion_affinity.register_banter(
        "forge.arrival", "talos",
        "These are my people's marks. If the Forge is cold, something is "
        "very wrong.")
    companion_affinity.register_banter(
        "forge.city", "talos",
        "Look -- nothing looted, nothing broken. They left in order. Dwarves "
        "don't flee. They evacuate.")
    companion_affinity.register_banter(
        "forge.faults", "talos",
        "Every failure, carved with the name of who owned it. That's not "
        "shame. That's how nothing lasts by accident.")
    companion_affinity.register_banter(
        "forge.constructs", "talos",
        "I helped build ones like these. Putting them down... I'll not "
        "forget it.")
    companion_affinity.register_banter(
        "forge.resolution", "talos",
        "We relit what was needed and left the rest sealed. That took more "
        "restraint than the whole climb down.")
