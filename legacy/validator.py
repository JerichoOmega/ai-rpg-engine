"""
Quest Flow Validator (Phase 5)
==============================

A static + dynamic analysis pass over every registered Legacy Questline.
It is both a CI gate and a permanent authoring aid: run it after editing any
quest JSON to catch problems long before playtesting.

Checks performed
----------------
Static (per quest, from the raw JSON):

* **Stage graph** -- every ``next`` / ``goto_stage`` target exists; every
  stage is reachable from the start; the quest can terminate.
* **Objective coverage** -- every non-optional objective is completed by
  some step on some path (no completion soft-lock).
* **Choice soft-locks** -- every ``choice`` step and every non-terminal
  dialogue node exposes at least one *ungated* option, so the main path is
  always reachable regardless of party/preparation.
* **Dialogue integrity** -- node reachability, valid goto/success/failure
  targets, a reachable terminal (no infinite loop without an exit).
* **Speech checks** -- valid skill + difficulty; probability is never zero
  (framework clamps to a 5% floor, so "impossible" checks cannot exist).
* **Flag producibility** -- flags referenced by gates / speech preparation /
  consequence ``requires`` are set somewhere (in this quest or flagged as a
  cross-quest / world dependency).
* **Encounter sanity** -- ritual defences have rounds > 0; multi-stage
  encounters have at least one wave.

Dynamic (per quest):

* A scripted default playthrough completes without raising.
* The resulting ``world_state`` round-trips through JSON (save/load safe).

Run: ``python legacy/validator.py`` (exit 0 = clean; 1 = errors found).
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Set, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from legacy.framework.speech_checks import SKILLS, DIFFICULTY_BASE   # noqa: E402
from legacy.framework import registry                                # noqa: E402
from legacy.framework.quest_framework import manager                 # noqa: E402
from legacy.quests import load_quest_data                            # noqa: E402


QUEST_FILES = {
    "debt_comes_due": "debt_comes_due.json",
    "what_the_forest_carries": "what_the_forest_carries.json",
    "eternal_forge": "eternal_forge.json",
    "the_jammed_mill": "the_jammed_mill.json",
}


class Report:
    def __init__(self, quest_id: str):
        self.quest_id = quest_id
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


# ---------------------------------------------------------------------------
# Effect / step walkers
# ---------------------------------------------------------------------------
def _walk_effect_lists(step: Dict[str, Any]):
    """Yield every effect-list embedded anywhere in a step."""
    for key in ("effects", "on_success", "on_failure"):
        if isinstance(step.get(key), list):
            yield step[key]
    for opt in step.get("options", []):
        if isinstance(opt.get("effects"), list):
            yield opt["effects"]
    if step.get("type") == "dialogue":
        tree = step.get("tree", {})
        for node in tree.get("nodes", []):
            for choice in node.get("choices", []):
                if isinstance(choice.get("effects"), list):
                    yield choice["effects"]
        for effects in step.get("on_outcome", {}).values():
            if isinstance(effects, list):
                yield effects


def collect_flags_set(stages: List[Dict], consequences: List[Dict]) -> Set[str]:
    flags: Set[str] = set()
    for stage in stages:
        for step in stage.get("steps", []):
            for effect_list in _walk_effect_lists(step):
                for effect in effect_list:
                    if effect.get("type") == "flag":
                        flags.add(effect["name"])
                    if effect.get("type") == "counter":
                        flags.add(effect["name"])
            if step.get("type") == "puzzle":
                flags.update(step["puzzle"].get("on_solve_flags", []))
            if step.get("type") == "encounter":
                spec = step["spec"]
                if spec.get("success_flag"):
                    flags.add(spec["success_flag"])
                flags.update(spec.get("on_complete_flags", []))
                for wave in spec.get("waves", []):
                    if wave.get("setback_flag"):
                        flags.add(wave["setback_flag"])
                for opt in spec.get("optional_objectives", []):
                    if opt.get("flag_if_met"):
                        flags.add(opt["flag_if_met"])
    for cons in consequences:
        if cons.get("type") in ("flag", "counter") and cons.get("name"):
            flags.add(cons["name"])
    return flags


def collect_objectives_completed(stages: List[Dict]) -> Set[str]:
    done: Set[str] = set()
    for stage in stages:
        for step in stage.get("steps", []):
            if step.get("type") == "complete_objective":
                done.add(step["objective"])
            for effect_list in _walk_effect_lists(step):
                for effect in effect_list:
                    if effect.get("type") == "complete_objective":
                        done.add(effect["objective"])
    return done


def collect_goto_targets(stages: List[Dict]) -> Set[str]:
    targets: Set[str] = set()
    for stage in stages:
        for step in stage.get("steps", []):
            for effect_list in _walk_effect_lists(step):
                for effect in effect_list:
                    if effect.get("type") == "goto_stage":
                        targets.add(effect["stage"])
    return targets


# ---------------------------------------------------------------------------
# Static checks
# ---------------------------------------------------------------------------
def _check_stage_graph(data: Dict, report: Report) -> None:
    stages = {s["id"]: s for s in data["stages"]}
    start = data.get("start_stage") or data["stages"][0]["id"]

    # reachability via next + goto_stage
    goto_targets = collect_goto_targets(data["stages"])
    reachable: Set[str] = set()
    frontier = [start]
    while frontier:
        current = frontier.pop()
        if current in reachable or current not in stages:
            continue
        reachable.add(current)
        nxt = stages[current].get("next")
        if nxt:
            frontier.append(nxt)
    frontier = list(goto_targets)
    while frontier:
        current = frontier.pop()
        if current in reachable or current not in stages:
            continue
        reachable.add(current)
        nxt = stages[current].get("next")
        if nxt:
            frontier.append(nxt)

    for stage_id in stages:
        if stage_id not in reachable:
            report.warn(f"stage '{stage_id}' is unreachable")
    for stage in data["stages"]:
        nxt = stage.get("next")
        if nxt and nxt not in stages:
            report.error(f"stage '{stage['id']}' -> next '{nxt}' does not exist")
    for target in goto_targets:
        if target not in stages:
            report.error(f"goto_stage '{target}' does not exist")

    # terminate: at least one reachable stage has next == null
    if not any(stages[s].get("next") is None for s in reachable):
        report.error("no reachable stage ends the quest (next: null)")


def _check_objectives(data: Dict, report: Report) -> None:
    completed = collect_objectives_completed(data["stages"])
    for stage in data["stages"]:
        for obj in stage.get("objectives", []):
            if not obj.get("optional") and obj["id"] not in completed:
                report.error(
                    f"non-optional objective '{obj['id']}' "
                    f"(stage '{stage['id']}') is never completed")


def _check_choices(data: Dict, report: Report) -> None:
    for stage in data["stages"]:
        for step in stage.get("steps", []):
            if step.get("type") == "choice":
                options = step.get("options", [])
                if not any("available_if" not in o for o in options):
                    report.error(
                        f"choice '{step.get('key')}' (stage '{stage['id']}') "
                        f"has no ungated option -> potential soft-lock")


def _check_dialogue(data: Dict, report: Report) -> None:
    for stage in data["stages"]:
        for step in stage.get("steps", []):
            if step.get("type") != "dialogue":
                continue
            tree = step["tree"]
            nodes = {n["id"]: n for n in tree["nodes"]}
            start = tree["start"]
            if start not in nodes:
                report.error(f"dialogue '{tree['id']}' start node missing")
                continue

            # goto validity + ungated option per non-terminal node
            for node in tree["nodes"]:
                if node.get("outcome") is not None:
                    continue
                choices = node.get("choices", [])
                if not choices:
                    report.error(
                        f"dialogue '{tree['id']}' node '{node['id']}' has no "
                        f"choices and no outcome (dead end)")
                gated = []
                for choice in choices:
                    for goto_key in ("goto", "on_success_goto",
                                     "on_failure_goto"):
                        target = choice.get(goto_key)
                        if target and target not in nodes:
                            report.error(
                                f"dialogue '{tree['id']}' choice "
                                f"'{choice['key']}' -> {goto_key} '{target}' "
                                f"does not exist")
                    is_gated = any(k in choice for k in (
                        "requires_companion", "requires_affinity_tier",
                        "requires_flag", "requires_standing"))
                    gated.append(is_gated)
                if choices and all(gated):
                    report.error(
                        f"dialogue '{tree['id']}' node '{node['id']}' has no "
                        f"ungated choice -> potential soft-lock")

            # reachability + terminal reachable
            reachable: Set[str] = set()
            frontier = [start]
            while frontier:
                current = frontier.pop()
                if current in reachable or current not in nodes:
                    continue
                reachable.add(current)
                for choice in nodes[current].get("choices", []):
                    for goto_key in ("goto", "on_success_goto",
                                     "on_failure_goto"):
                        if choice.get(goto_key):
                            frontier.append(choice[goto_key])
            for node_id in nodes:
                if node_id not in reachable:
                    report.warn(
                        f"dialogue '{tree['id']}' node '{node_id}' unreachable")
            if not any(nodes[n].get("outcome") is not None for n in reachable):
                report.error(
                    f"dialogue '{tree['id']}' has no reachable terminal node "
                    f"-> infinite loop risk")


def _iter_speech_checks(data: Dict):
    for stage in data["stages"]:
        for step in stage.get("steps", []):
            if step.get("type") == "speech_check":
                yield step, f"stage '{stage['id']}'"
            if step.get("type") == "dialogue":
                for node in step["tree"]["nodes"]:
                    for choice in node.get("choices", []):
                        if choice.get("check"):
                            yield choice["check"], f"dialogue '{step['tree']['id']}'"


def _check_speech(data: Dict, report: Report, flags_set: Set[str]) -> None:
    for check, where in _iter_speech_checks(data):
        skill = check.get("skill", "persuasion")
        if skill not in SKILLS:
            report.error(f"speech check '{check.get('id')}' ({where}) uses "
                         f"unknown skill '{skill}'")
        difficulty = check.get("difficulty", "medium")
        if difficulty not in DIFFICULTY_BASE:
            report.error(f"speech check '{check.get('id')}' ({where}) uses "
                         f"unknown difficulty '{difficulty}'")
        for flag in check.get("preparation_flags", []):
            if flag not in flags_set:
                report.warn(f"speech check '{check.get('id')}' preparation "
                            f"flag '{flag}' is not set anywhere in this quest "
                            f"(cross-quest/world dependency?)")


def _check_flag_refs(data: Dict, report: Report, flags_set: Set[str]) -> None:
    # choice available_if.flag and dialogue requires_flag
    referenced: List[Tuple[str, str]] = []
    for stage in data["stages"]:
        for step in stage.get("steps", []):
            if step.get("type") == "choice":
                for opt in step.get("options", []):
                    gate = opt.get("available_if", {})
                    if gate.get("flag"):
                        referenced.append((gate["flag"], f"choice {step.get('key')}"))
            if step.get("type") == "dialogue":
                for node in step["tree"]["nodes"]:
                    for choice in node.get("choices", []):
                        if choice.get("requires_flag"):
                            referenced.append(
                                (choice["requires_flag"],
                                 f"dialogue {step['tree']['id']}"))
    for cons in data.get("consequences", []):
        req = cons.get("requires")
        if isinstance(req, str):
            referenced.append((req, "consequence"))
        elif isinstance(req, dict) and req.get("flag"):
            referenced.append((req["flag"], "consequence"))
    for flag, where in referenced:
        if flag not in flags_set:
            report.warn(f"flag '{flag}' referenced by {where} is not set "
                        f"anywhere in this quest (cross-quest/world dep?)")


def _check_encounters(data: Dict, report: Report) -> None:
    for stage in data["stages"]:
        for step in stage.get("steps", []):
            if step.get("type") != "encounter":
                continue
            spec = step["spec"]
            if spec.get("type") == "ritual_defense":
                if int(spec.get("rounds", 0)) <= 0:
                    report.error(f"ritual encounter '{spec['id']}' has no rounds")
            else:
                if not spec.get("waves"):
                    report.error(f"multi-stage encounter '{spec['id']}' has no waves")


# ---------------------------------------------------------------------------
# Dynamic check
# ---------------------------------------------------------------------------
def _check_dynamic(quest_id: str, report: Report) -> None:
    from world_state import world_state, ensure_world_state_defaults
    from legacy.framework.io import ScriptedIO, set_io

    world_state["legacy"] = {}
    registry.ensure_legacy_world_state()
    world_state.setdefault("companions", {})["party"] = []

    io = ScriptedIO({})
    previous = set_io(io)
    try:
        state = manager.play(quest_id, io=io)
        if state != "completed":
            report.error(f"default scripted playthrough did not complete "
                         f"(state={state})")
        # save/load round-trip
        try:
            blob = json.dumps(world_state)
            reloaded = json.loads(blob)
            world_state.clear()
            world_state.update(reloaded)
            ensure_world_state_defaults()
        except (TypeError, ValueError) as exc:
            report.error(f"world_state is not JSON round-trippable: {exc}")
    except Exception as exc:  # pragma: no cover - defensive
        report.error(f"playthrough raised {type(exc).__name__}: {exc}")
    finally:
        set_io(previous)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def validate_quest(quest_id: str, filename: str) -> Report:
    report = Report(quest_id)
    data = load_quest_data(filename)
    flags_set = collect_flags_set(data["stages"], data.get("consequences", []))

    _check_stage_graph(data, report)
    _check_objectives(data, report)
    _check_choices(data, report)
    _check_dialogue(data, report)
    _check_speech(data, report, flags_set)
    _check_flag_refs(data, report, flags_set)
    _check_encounters(data, report)
    _check_dynamic(quest_id, report)
    return report


def main(argv=None) -> int:
    reports = [validate_quest(qid, fn) for qid, fn in QUEST_FILES.items()]
    total_errors = 0
    for report in reports:
        status = "CLEAN" if not report.errors else "ERRORS"
        print(f"\n=== {report.quest_id}: {status} "
              f"({len(report.errors)} errors, {len(report.warnings)} warnings) ===")
        for err in report.errors:
            print(f"  [ERROR] {err}")
        for warn in report.warnings:
            print(f"  [warn]  {warn}")
        total_errors += len(report.errors)

    print(f"\n{'PASS' if total_errors == 0 else 'FAIL'}: "
          f"{total_errors} error(s) across {len(reports)} quests.")
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
