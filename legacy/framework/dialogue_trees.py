"""
Dialogue Tree Framework
=======================

Branching, stateful conversations built from data. A :class:`DialogueTree`
is a set of :class:`DialogueNode` s; each node has narration and a list of
:class:`DialogueChoice` s. Choices can be:

* **gated** -- only *offered* when requirements are met (companion present
  and warmed up, a world flag, or a civilization standing). Locked choices
  are still shown so the player sees what preparation unlocks, but the main
  path is always reachable.
* **check-driven** -- selecting the choice triggers a speech check whose
  result routes to a success/failure node and applies effects.
* **effectful** -- set living-world flags, adjust affinity/standing, or end
  the conversation with a labelled outcome the quest branches on.

The same tree runs interactively or under the scripted harness because all
I/O goes through the :mod:`legacy.framework.io` adapter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .io import get_io, Option
from . import companion_affinity, reputation, world_flags, speech_checks


@dataclass
class DialogueChoice:
    key: str
    label: str
    # Routing:
    goto: Optional[str] = None          # next node id
    # Requirements to *offer* the choice (all must pass):
    requires_companion: Optional[str] = None
    requires_affinity_tier: Optional[str] = None
    requires_flag: Optional[str] = None
    requires_standing: Optional[Dict[str, int]] = None  # {civ: min}
    locked_note: str = ""
    # Optional speech check; on resolve, route to success/failure node.
    check: Optional[Dict[str, Any]] = None
    on_success_goto: Optional[str] = None
    on_failure_goto: Optional[str] = None
    # Side effects applied when the choice is taken (list of effect dicts).
    effects: List[Dict[str, Any]] = field(default_factory=list)

    def is_available(self) -> bool:
        if self.requires_companion and not companion_affinity.has_companion(
                self.requires_companion):
            return False
        if self.requires_affinity_tier and self.requires_companion:
            if not companion_affinity.affinity_at_least(
                    self.requires_companion, self.requires_affinity_tier):
                return False
        if self.requires_flag and not world_flags.has_flag(self.requires_flag):
            return False
        if self.requires_standing:
            for civ, minimum in self.requires_standing.items():
                if reputation.get_standing(civ) < minimum:
                    return False
        return True


@dataclass
class DialogueNode:
    id: str
    speaker: str = ""
    text: str = ""
    choices: List[DialogueChoice] = field(default_factory=list)
    # Terminal node: end the conversation with this outcome label.
    outcome: Optional[str] = None


class DialogueTree:
    def __init__(self, tree_id: str, start: str,
                 nodes: Dict[str, DialogueNode]):
        self.id = tree_id
        self.start = start
        self.nodes = nodes


def _apply_effects(effects: List[Dict[str, Any]]) -> None:
    """Apply a list of declarative effects (shared with the quest runner)."""
    for effect in effects:
        kind = effect.get("type")
        if kind == "flag":
            world_flags.set_flag(effect["name"], effect.get("value", True))
        elif kind == "affinity":
            companion_affinity.adjust_affinity(
                effect["companion"], int(effect["amount"]))
        elif kind == "standing":
            reputation.adjust_standing(effect["civ"], int(effect["amount"]))
        elif kind == "relationship":
            reputation.adjust_relationship(
                effect["civ_a"], effect["civ_b"], int(effect["amount"]))
        elif kind == "reputation":
            reputation.adjust_reputation(
                effect["faction"], int(effect["amount"]))


def run_dialogue(tree: DialogueTree, io=None) -> str:
    """Run ``tree`` to a terminal node and return its outcome label.

    Guarantees termination: a node with no available choices and no outcome
    resolves to the ``"default"`` outcome so a mis-authored tree can never
    stall a playthrough.
    """
    io = io or get_io()
    node = tree.nodes[tree.start]
    guard = 0

    while True:
        guard += 1
        if guard > 100:  # safety valve against authoring cycles
            return "default"

        if node.text:
            io.say(node.text, speaker=node.speaker or None)

        if node.outcome is not None:
            return node.outcome

        # Build the option list (available + locked-for-visibility).
        options: List[Option] = []
        for choice in node.choices:
            available = choice.is_available()
            note = "" if available else (choice.locked_note or "needs preparation")
            options.append(Option(choice.key, choice.label, available, note))

        available_choices = [c for c in node.choices if c.is_available()]
        if not available_choices:
            return "default"

        chosen_key = io.choose(
            "What do you say?", options,
            key=f"{tree.id}.{node.id}",
            default=available_choices[0].key,
        )
        choice = next(c for c in node.choices if c.key == chosen_key)

        _apply_effects(choice.effects)

        # Speech-check routing takes precedence over a plain goto.
        if choice.check:
            check = speech_checks.from_dict(choice.check)
            result = speech_checks.resolve(check, io=io)
            target = (choice.on_success_goto if result.success
                      else choice.on_failure_goto) or choice.goto
        else:
            target = choice.goto

        if not target or target not in tree.nodes:
            return "default"
        node = tree.nodes[target]


# ---------------------------------------------------------------------------
# JSON loader
# ---------------------------------------------------------------------------
def from_dict(data: Dict[str, Any]) -> DialogueTree:
    nodes: Dict[str, DialogueNode] = {}
    for node_data in data["nodes"]:
        choices = [
            DialogueChoice(
                key=c["key"],
                label=c["label"],
                goto=c.get("goto"),
                requires_companion=c.get("requires_companion"),
                requires_affinity_tier=c.get("requires_affinity_tier"),
                requires_flag=c.get("requires_flag"),
                requires_standing=c.get("requires_standing"),
                locked_note=c.get("locked_note", ""),
                check=c.get("check"),
                on_success_goto=c.get("on_success_goto"),
                on_failure_goto=c.get("on_failure_goto"),
                effects=list(c.get("effects", [])),
            )
            for c in node_data.get("choices", [])
        ]
        nodes[node_data["id"]] = DialogueNode(
            id=node_data["id"],
            speaker=node_data.get("speaker", ""),
            text=node_data.get("text", ""),
            choices=choices,
            outcome=node_data.get("outcome"),
        )
    return DialogueTree(data["id"], data["start"], nodes)
