"""
Quest Framework
===============

The reusable spine of the Legacy Questline architecture. A quest is
authored as **data** (see ``legacy/data/*.json``) and executed by a generic,
step-based :class:`QuestRunner`. Every other framework (dialogue, speech
checks, companion affinity, split party, timed objectives, multi-stage
encounters, environmental puzzles, living world, reputation, consequences)
is invoked through declarative *steps*, so a new quest needs **no new engine
code** -- only a new data file and a one-line registration.

Runtime model
-------------
* :class:`Quest` -> ordered :class:`QuestStage` s -> a list of *steps*.
* State (which stage, which objectives) persists under
  ``world_state["legacy"]["quests"][quest_id]`` so it saves/loads and dev
  tools can jump straight to any stage.
* :class:`QuestManager` is the singleton registry the game and dev tools
  talk to.

Step types (data ``"type"`` values) handled by the runner:

    narrate | banter | dialogue | speech_check | choice | effects |
    complete_objective | encounter | split_party | resolve_evacuation |
    reunite | puzzle

All player I/O flows through the :mod:`legacy.framework.io` adapter, so the
identical quest data runs interactively, under the automated harness, and
from developer tools.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from world_state import world_state
from event_bus import emit
from .io import get_io, Option
from . import (companion_affinity, reputation, world_flags, speech_checks,
               dialogue_trees, split_party, encounters, puzzles, consequences)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class QuestObjective:
    id: str
    description: str
    optional: bool = False


@dataclass
class QuestStage:
    id: str
    title: str
    description: str = ""
    objectives: List[QuestObjective] = field(default_factory=list)
    steps: List[Dict[str, Any]] = field(default_factory=list)
    next: Optional[str] = None      # default next stage id (None => end)


@dataclass
class Quest:
    id: str
    name: str
    civilization: str = ""
    featured_companion: str = ""
    theme: str = ""
    signature_encounter: str = ""
    # Quest category: "legacy" | "main" | "companion" | "side" | "faction" ...
    # Purely descriptive metadata; the runner treats every category
    # identically. Defaults to "legacy" for backward compatibility.
    category: str = "legacy"
    start_stage: str = ""
    stages: Dict[str, QuestStage] = field(default_factory=dict)
    consequences: List[Dict[str, Any]] = field(default_factory=list)

    def stage_order(self) -> List[str]:
        """Best-effort linear order following ``next`` links from start."""
        order, seen, current = [], set(), self.start_stage
        while current and current in self.stages and current not in seen:
            order.append(current)
            seen.add(current)
            current = self.stages[current].next
        # Append any stages only reachable by branching so tools see them all.
        for stage_id in self.stages:
            if stage_id not in seen:
                order.append(stage_id)
        return order


# ---------------------------------------------------------------------------
# Persistent quest state helpers
# ---------------------------------------------------------------------------
def _quest_store() -> Dict[str, Any]:
    legacy = world_state.setdefault("legacy", {})
    return legacy.setdefault("quests", {})


def _state_for(quest: Quest) -> Dict[str, Any]:
    store = _quest_store()
    if quest.id not in store:
        store[quest.id] = {
            "state": "not_started",
            "current_stage": None,
            "objectives": {},
            "started": False,
        }
    return store[quest.id]


# ---------------------------------------------------------------------------
# Declarative effect application (shared by choices / dialogue outcomes)
# ---------------------------------------------------------------------------
def apply_effects(effects: List[Dict[str, Any]], quest: Quest) -> Optional[str]:
    """Apply a list of effects. Returns a ``goto_stage`` id if one of the
    effects requests a stage jump, else None."""
    goto_stage: Optional[str] = None
    for effect in effects:
        kind = effect.get("type")
        if kind == "flag":
            world_flags.set_flag(effect["name"], effect.get("value", True))
        elif kind == "counter":
            world_flags.adjust_counter(effect["name"], int(effect["amount"]))
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
        elif kind == "complete_objective":
            _complete_objective(quest, effect["objective"])
        elif kind == "goto_stage":
            goto_stage = effect["stage"]
    return goto_stage


def _complete_objective(quest: Quest, objective_id: str) -> None:
    state = _state_for(quest)
    if not state["objectives"].get(objective_id):
        state["objectives"][objective_id] = True
        emit("quest_objective_completed", quest_id=quest.id,
             objective=objective_id)


# ---------------------------------------------------------------------------
# Quest runner (step interpreter)
# ---------------------------------------------------------------------------
class QuestRunner:
    """Executes a quest's stages/steps through the active IO adapter."""

    def __init__(self, io=None):
        self.io = io or get_io()

    def play(self, quest: Quest, start_stage: Optional[str] = None) -> str:
        state = _state_for(quest)
        state["state"] = "active"
        state["started"] = True
        emit("quest_started", quest_id=quest.id)

        current = start_stage or state.get("current_stage") \
            or quest.start_stage
        self.io.say(f"===== {quest.name} =====")
        if quest.theme:
            self.io.say(f"Theme: {quest.theme}")

        guard = 0
        while current and current in quest.stages:
            guard += 1
            if guard > 200:  # safety valve against authoring cycles
                break
            state["current_stage"] = current
            stage = quest.stages[current]
            goto = self._run_stage(quest, stage)
            current = goto or stage.next

        state["state"] = "completed"
        state["current_stage"] = None
        self._complete(quest)
        return "completed"

    def _run_stage(self, quest: Quest, stage: QuestStage) -> Optional[str]:
        self.io.say(f"--- {stage.title} ---")
        if stage.description:
            self.io.say(stage.description)
        emit("quest_stage_entered", quest_id=quest.id, stage=stage.id)

        goto: Optional[str] = None
        for step in stage.steps:
            result = self._run_step(quest, step)
            if result:
                goto = result  # a step requested a stage jump
        return goto

    def _run_step(self, quest: Quest, step: Dict[str, Any]) -> Optional[str]:
        kind = step.get("type")

        if kind == "narrate":
            self.io.say(step["text"], speaker=step.get("speaker"))

        elif kind == "banter":
            companion_affinity.trigger_banter(step["context"], io=self.io)

        elif kind == "effects":
            return apply_effects(step.get("effects", []), quest)

        elif kind == "complete_objective":
            _complete_objective(quest, step["objective"])

        elif kind == "dialogue":
            tree = dialogue_trees.from_dict(step["tree"])
            outcome = dialogue_trees.run_dialogue(tree, io=self.io)
            self.io.say(f"[Conversation outcome: {outcome}]")
            on_outcome = step.get("on_outcome", {})
            if outcome in on_outcome:
                return apply_effects(on_outcome[outcome], quest)

        elif kind == "speech_check":
            check = speech_checks.from_dict(step)
            if step.get("prompt"):
                self.io.say(step["prompt"])
            result = speech_checks.resolve(check, io=self.io)
            branch = step.get("on_success" if result.success
                              else "on_failure", [])
            return apply_effects(branch, quest)

        elif kind == "choice":
            return self._run_choice(quest, step)

        elif kind == "encounter":
            encounters.run_encounter(step["spec"], io=self.io)

        elif kind == "split_party":
            plan = split_party.from_dict(step["plan"])
            plan = split_party.execute_split(plan, io=self.io)
            self._active_split = plan
            if step.get("resolve", True):
                split_party.resolve_evacuation(
                    plan, base_saved=int(step.get("base_saved", 20)),
                    io=self.io)

        elif kind == "resolve_evacuation":
            plan = getattr(self, "_active_split", None)
            if plan:
                split_party.resolve_evacuation(
                    plan, base_saved=int(step.get("base_saved", 20)),
                    io=self.io)

        elif kind == "reunite":
            plan = getattr(self, "_active_split", None)
            if plan:
                split_party.reunite(plan, io=self.io)

        elif kind == "puzzle":
            puzzle = puzzles.from_dict(step["puzzle"])
            puzzles.solve_puzzle(puzzle, io=self.io)

        else:
            self.io.say(f"[unknown step type: {kind}]")

        return None

    def _run_choice(self, quest: Quest, step: Dict[str, Any]) -> Optional[str]:
        options: List[Option] = []
        raw_options = step.get("options", [])
        for opt in raw_options:
            available = True
            note = opt.get("locked_note", "")
            gate = opt.get("available_if")
            if gate:
                available = self._evaluate_gate(gate)
                if not available and not note:
                    note = "needs preparation"
            options.append(Option(opt["key"], opt["label"], available, note))

        available_keys = [o.key for o in options if o.available]
        default = available_keys[0] if available_keys else raw_options[0]["key"]
        chosen = self.io.choose(step.get("prompt", "Choose:"), options,
                                key=step.get("key"), default=default)
        selected = next(o for o in raw_options if o["key"] == chosen)
        return apply_effects(selected.get("effects", []), quest)

    @staticmethod
    def _evaluate_gate(gate: Dict[str, Any]) -> bool:
        """Evaluate a choice-availability gate (companion/affinity/flag/
        standing). Missing requirements evaluate to True."""
        companion = gate.get("companion")
        tier = gate.get("affinity_tier")
        if companion and tier:
            if not companion_affinity.affinity_at_least(companion, tier):
                return False
        elif companion:
            if not companion_affinity.has_companion(companion):
                return False
        if gate.get("flag") and not world_flags.has_flag(gate["flag"]):
            return False
        standing = gate.get("standing")
        if standing:
            if reputation.get_standing(standing["civ"]) < standing["min"]:
                return False
        return True

    def _complete(self, quest: Quest) -> None:
        self.io.say(f"===== {quest.name}: COMPLETE =====")
        emit("quest_completed", quest_name=quest.id,
             quest={"id": quest.id, "type": "legacy"})
        consequences.apply_consequences(quest.id, quest.consequences,
                                        io=self.io)


# ---------------------------------------------------------------------------
# Quest manager (singleton registry)
# ---------------------------------------------------------------------------
class QuestManager:
    def __init__(self):
        self._quests: Dict[str, Quest] = {}

    def register(self, quest: Quest) -> Quest:
        self._quests[quest.id] = quest
        return quest

    def get(self, quest_id: str) -> Optional[Quest]:
        return self._quests.get(quest_id)

    def all(self) -> List[Quest]:
        return list(self._quests.values())

    def play(self, quest_id: str, io=None,
             start_stage: Optional[str] = None) -> str:
        quest = self._quests[quest_id]
        return QuestRunner(io=io).play(quest, start_stage=start_stage)

    def status(self, quest_id: str) -> Dict[str, Any]:
        quest = self._quests[quest_id]
        state = _state_for(quest)
        return {
            "id": quest.id,
            "name": quest.name,
            "state": state["state"],
            "current_stage": state["current_stage"],
            "objectives": dict(state["objectives"]),
        }

    def jump_to_stage(self, quest_id: str, stage_id: str, io=None) -> str:
        """Developer utility: play a quest starting from an arbitrary stage."""
        quest = self._quests[quest_id]
        if stage_id not in quest.stages:
            raise KeyError(f"{quest_id} has no stage {stage_id!r}")
        return QuestRunner(io=io).play(quest, start_stage=stage_id)

    def complete_objective(self, quest_id: str, objective_id: str) -> None:
        """Developer utility: mark an objective complete out of band."""
        _complete_objective(self._quests[quest_id], objective_id)

    def fail_objective(self, quest_id: str, objective_id: str) -> None:
        """Developer utility: record an objective as failed."""
        state = _state_for(self._quests[quest_id])
        state["objectives"][objective_id] = False
        emit("quest_objective_failed", quest_id=quest_id,
             objective=objective_id)

    def fail_quest(self, quest_id: str) -> None:
        """Mark a quest failed (dev utility / future fail branches)."""
        state = _state_for(self._quests[quest_id])
        state["state"] = "failed"
        emit("quest_failed", quest_name=quest_id,
             quest={"id": quest_id, "type": "legacy"})

    def set_stage(self, quest_id: str, stage_id: str) -> None:
        """Developer utility: set the persisted current stage without playing."""
        quest = self._quests[quest_id]
        if stage_id not in quest.stages:
            raise KeyError(f"{quest_id} has no stage {stage_id!r}")
        state = _state_for(quest)
        state["state"] = "active"
        state["started"] = True
        state["current_stage"] = stage_id

    def export_state(self, quest_id: str) -> Dict[str, Any]:
        """Return a JSON-serialisable snapshot of a quest's runtime state."""
        quest = self._quests[quest_id]
        return {
            "quest": {"id": quest.id, "name": quest.name,
                      "civilization": quest.civilization,
                      "featured_companion": quest.featured_companion,
                      "stage_order": quest.stage_order()},
            "state": dict(_state_for(quest)),
        }


# Module-level singleton the game and tools share.
manager = QuestManager()


# ---------------------------------------------------------------------------
# JSON loader
# ---------------------------------------------------------------------------
def load_quest(data: Dict[str, Any]) -> Quest:
    """Build a :class:`Quest` from a quest-definition dict (parsed JSON)."""
    stages: Dict[str, QuestStage] = {}
    for stage_data in data["stages"]:
        objectives = [
            QuestObjective(o["id"], o.get("description", o["id"]),
                           bool(o.get("optional", False)))
            for o in stage_data.get("objectives", [])
        ]
        stages[stage_data["id"]] = QuestStage(
            id=stage_data["id"],
            title=stage_data.get("title", stage_data["id"]),
            description=stage_data.get("description", ""),
            objectives=objectives,
            steps=list(stage_data.get("steps", [])),
            next=stage_data.get("next"),
        )
    start_stage = data.get("start_stage") or data["stages"][0]["id"]
    return Quest(
        id=data["id"],
        name=data["name"],
        civilization=data.get("civilization", ""),
        featured_companion=data.get("featured_companion", ""),
        theme=data.get("theme", ""),
        signature_encounter=data.get("signature_encounter", ""),
        category=data.get("category", "legacy"),
        start_stage=start_stage,
        stages=stages,
        consequences=list(data.get("consequences", [])),
    )
