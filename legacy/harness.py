"""
Automated Quest Harness
=======================

Non-interactive, scripted playthroughs that validate every major quest
state and branching path across all three Legacy Questlines. This *does not
replace* manual play -- it is a fast regression net that proves the shared
frameworks (quest runner, dialogue, speech checks, affinity gating, split
party, timed/ritual encounters, puzzles, consequences, living world) work
end-to-end for both prepared and minimal parties.

Run it directly::

    python legacy/harness.py            # summary
    python legacy/harness.py -v         # verbose transcript

Exit code is 0 when every scenario passes, 1 otherwise. A machine-readable
report is written to ``legacy/harness_report.json``.
"""

from __future__ import annotations

import json
import os
import sys

# Allow running as a script (`python legacy/harness.py`) from repo root.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from world_state import world_state                       # noqa: E402
from legacy.framework import registry                     # noqa: E402
from legacy.framework.quest_framework import manager      # noqa: E402
from legacy.framework import world_flags, companion_affinity  # noqa: E402
from legacy.framework.io import ScriptedIO, set_io        # noqa: E402


# ---------------------------------------------------------------------------
# State reset between scenarios
# ---------------------------------------------------------------------------
def reset_state() -> None:
    world_state["legacy"] = {}
    registry.ensure_legacy_world_state()
    world_state.setdefault("companions", {})["party"] = []
    world_state.setdefault("player", {})["level"] = 3
    try:
        from companion_manager import active_companions
        active_companions.clear()
    except Exception:
        pass


def seat(names, affinity=80):
    world_state["companions"]["party"] = list(names)
    for name in names:
        companion_affinity.set_affinity(name, affinity)
    try:
        from companion_manager import active_companions, COMPANIONS
        active_companions.clear()
        for name in names:
            entry = dict(COMPANIONS.get(name, {"role": name}))
            entry["name"] = name
            active_companions.append(entry)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Scenario runner + assertions
# ---------------------------------------------------------------------------
class Scenario:
    def __init__(self, name, quest_id, party, script, expect_flags,
                 expect_missing=None, affinity=80):
        self.name = name
        self.quest_id = quest_id
        self.party = party
        self.script = script
        self.expect_flags = expect_flags
        self.expect_missing = expect_missing or []
        self.affinity = affinity
        self.failures = []

    def run(self, verbose=False):
        reset_state()
        seat(self.party, self.affinity)
        io = ScriptedIO(self.script, verbose=verbose)
        set_io(io)
        state = manager.play(self.quest_id, io=io)

        # 1. Quest reaches completed state.
        if state != "completed":
            self.failures.append(f"quest did not complete (state={state})")
        status = manager.status(self.quest_id)
        if status["state"] != "completed":
            self.failures.append(f"status not completed: {status['state']}")

        # 2. All non-optional objectives recorded.
        quest = manager.get(self.quest_id)
        for stage in quest.stages.values():
            for objective in stage.objectives:
                if not objective.optional and not status["objectives"].get(
                        objective.id):
                    self.failures.append(
                        f"missing objective {objective.id}")

        # 3. Expected living-world flags present/truthy.
        for flag, expected in self.expect_flags.items():
            actual = world_flags.get_flag(flag)
            if expected is True and not actual:
                self.failures.append(f"flag {flag} expected truthy, got {actual}")
            elif expected is not True and actual != expected:
                self.failures.append(
                    f"flag {flag} expected {expected}, got {actual}")

        # 4. Flags that must NOT be set (branch exclusivity / no leaks).
        for flag in self.expect_missing:
            if world_flags.has_flag(flag):
                self.failures.append(f"flag {flag} should not be set")

        return len(self.failures) == 0


SCENARIOS = [
    # ---- The Debt Comes Due -----------------------------------------------
    Scenario(
        "debt_prepared_peace", "debt_comes_due", ["talos"],
        script={
            "choices": {
                "debt.grakkor.root": "press",
                "debt.rourke.root": "diplomacy",
                "debt.learn_customs": "learn",
                "debt.negotiation.approach": "evidence",
                "debt.hero_moment": "hold",
            },
            "speech": {
                "debt.grakkor.insight": True,
                "debt.rourke.diplomacy": True,
                "debt.evidence.insight": True,
                "debt.negotiation.diplomacy": True,
            },
            "seed": 1,
        },
        expect_flags={
            "debt_peace_brokered": True,
            "frontier_camp_closed": True,
            "talos_town_growing": True,
            "symbolic_goblins_remain_with_refugees": True,
            "hook_foundations_of_the_council_of_embers": True,
        },
        expect_missing=["debt_uneasy_truce"],
    ),
    Scenario(
        "debt_minimal_truce", "debt_comes_due", [],
        script={
            "choices": {
                "debt.grakkor.root": "listen",
                "debt.rourke.root": "honest",
                "debt.learn_customs": "skip",
                "debt.negotiation.approach": "pressure",
                "debt.hero_moment": "organize",
            },
            "speech": {
                "debt.grakkor.insight": False,
                "debt.rourke.diplomacy": False,
                "debt.evidence.insight": False,
                "debt.negotiation.diplomacy": False,
            },
            "seed": 2,
        },
        expect_flags={"debt_uneasy_truce": True, "frontier_camp_closed": True},
        expect_missing=["debt_peace_brokered"],
    ),

    # ---- What the Forest Carries ------------------------------------------
    Scenario(
        "forest_prepared", "what_the_forest_carries",
        ["corwin", "kael", "lyra"],
        script={
            "choices": {
                "forest.vess.root": "insight",
                "forest.crossing.method": "corwin_reads",
                "forest.warden.close": "corwin_word",
            },
            "speech": {
                "forest.vess.insight": True,
                "forest.track.cultural": True,
                "forest.ward.insight": True,
            },
            "seed": 3,
        },
        expect_flags={
            "forest_ward_renewed": True,
            "forest_restored": True,
            "wildlife_returned": True,
            "warden_distant_sightings": True,
        },
    ),
    Scenario(
        "forest_minimal_no_corwin", "what_the_forest_carries", [],
        script={
            "choices": {
                "forest.vess.root": "listen",
                "forest.crossing.method": "careful",
                "forest.warden.close": "silent",
            },
            "speech": {
                "forest.vess.insight": False,
                "forest.track.cultural": False,
                "forest.ward.insight": False,
            },
            "seed": 4,
        },
        # Ritual endures even without the recommended companion.
        expect_flags={"forest_ward_renewed": True, "forest_restored": True},
        expect_missing=["warden_distant_sightings"],
    ),

    # ---- Eternal Forge ----------------------------------------------------
    Scenario(
        "forge_prepared", "eternal_forge", ["talos"],
        script={
            "choices": {
                "forge.elder.root": "oath",
                "forge.construct.mark": "restore",
                "forge.first_strike": "talos",
            },
            "speech": {
                "forge.elder.cultural": True,
                "forge.evacuation.insight": True,
            },
            "seed": 5,
        },
        expect_flags={
            "eternal_forge_active": True,
            "great_lift_restored": True,
            "forge_infrastructure_restored": True,
            "forge_chamber_secured": True,
            "deep_stair_remains_sealed": True,
            "foundry_construct_ally": True,
            "hook_sealed_lower_chamber": True,
        },
    ),
    Scenario(
        "forge_minimal", "eternal_forge", [],
        script={
            "choices": {
                "forge.elder.root": "why",
                "forge.construct.mark": "retire",
                "forge.first_strike": "self",
            },
            "speech": {
                "forge.elder.cultural": False,
                "forge.evacuation.insight": False,
            },
            "seed": 6,
        },
        expect_flags={
            "eternal_forge_active": True,
            "great_lift_restored": True,
            "deep_stair_remains_sealed": True,
        },
        expect_missing=["foundry_construct_ally"],
    ),

    # ---- The Jammed Mill (side quest -- framework validation) -------------
    Scenario(
        "mill_generous_no_combat", "the_jammed_mill", ["kael"],
        script={
            "choices": {
                "mill.miller.root": "reassure",
                "mill.approach": "coax",
                "mill.payment": "waive",
            },
            "speech": {
                "mill.reassure": True,
                "mill.cause.insight": True,
                "mill.coax": True,
            },
            "seed": 7,
        },
        expect_flags={
            "mill_wheel_freed": True,
            "mill_repaired": True,
            "mill_generous": True,
            "mill_generous_remembered": True,
        },
        expect_missing=["mill_vermin_driven_off", "mill_paid"],
    ),
    Scenario(
        "mill_paid_with_combat", "the_jammed_mill", [],
        script={
            "choices": {
                "mill.miller.root": "agree",
                "mill.approach": "fight",
                "mill.payment": "take",
            },
            "speech": {"mill.cause.insight": False},
            "seed": 8,
        },
        expect_flags={
            "mill_vermin_driven_off": True,
            "mill_wheel_freed": True,
            "mill_repaired": True,
            "mill_paid": True,
        },
        expect_missing=["mill_generous"],
    ),
]


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    verbose = "-v" in argv or "--verbose" in argv

    results = []
    all_pass = True
    for scenario in SCENARIOS:
        passed = scenario.run(verbose=verbose)
        all_pass = all_pass and passed
        results.append({
            "scenario": scenario.name,
            "quest": scenario.quest_id,
            "passed": passed,
            "failures": scenario.failures,
        })
        mark = "PASS" if passed else "FAIL"
        print(f"[{mark}] {scenario.name} ({scenario.quest_id})")
        for failure in scenario.failures:
            print(f"        - {failure}")

    report = {"all_pass": all_pass, "results": results}
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "harness_report.json")
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\n{passed}/{total} scenarios passed. Report: {report_path}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
