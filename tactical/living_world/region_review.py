"""
region_review — the Region Completion Review (runnable, reusable).
==================================================================

A rerunnable quality gate for a region: it evaluates the living-world systems
with objective metrics and prints a concise, human-readable report (and writes
JSON for the record). Rerun it after any change to spot regressions or
incomplete systems quickly.

    python -m tactical.living_world.region_review          # checklist
    python -m tactical.living_world.region_review --json    # machine report

This is a *dev/QA tool* (like ``tactical/verify.py``): only :func:`main` does
I/O. The evaluation itself (:func:`run`) returns plain data and touches nothing
in the game. It is the template for reviewing every future region of Elyndor.

Vocabulary: ``OK`` (complete), ``WARN`` (works, gap noted), ``GAP`` (missing).
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Dict, List, Tuple

from tactical import frontier
from . import content, frontier_overlay, banter as banter_mod
from .region_state import STATES, is_natural_transition

# Reusable framework modules that MUST stay engine-agnostic (no print/input,
# no engine imports). region_review itself is a dev tool and is excluded.
_CORE_MODULES = [
    "__init__", "region_state", "reputation", "events", "companions",
    "banter", "environment", "memory", "epilogue", "world", "content",
    "persistence", "region", "overlay", "runtime", "npcs", "frontier_overlay",
]

_PARTY = ["Ronan", "Talos", "Maeve Ashwood", "Torren", "Corwin", "Eleanor",
          "Ragash"]

_DOCS = [
    "docs/systems/living_world.md",
    "docs/systems/reputation.md",
    "docs/architecture/ENGINE_INTERFACES.md",
    "docs/architecture/LAYER_RULES.md",
]


def _repo_root() -> str:
    # tactical/living_world/region_review.py -> repo root is three up.
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _check_completion() -> Tuple[str, str]:
    state = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    _, world = frontier_overlay.build_overlay(state, seed=7)
    region = world.location("the_frontier")
    cleansed = state.region_outcome == "cleansed"
    restored = any(l.status == "restored" for l in world.locations.values())
    ok = cleansed and restored and region is not None
    return ("OK" if ok else "GAP",
            f"golden finale={state.region_outcome} region_status={region.status if region else '?'} "
            f"restored_locations={sum(1 for l in world.locations.values() if l.status=='restored')}")


def _check_companion_coverage() -> Tuple[str, str]:
    presence = content.companion_presence()
    landmarks = content.companion_landmarks()
    missing_presence = [c for c in _PARTY if not presence.get(c)]
    missing_landmark = [c for c in _PARTY if not landmarks.get(c)]
    status = "OK" if not missing_presence and not missing_landmark else "WARN"
    return (status,
            f"presence={len(_PARTY)-len(missing_presence)}/{len(_PARTY)} "
            f"landmarks={len(_PARTY)-len(missing_landmark)}/{len(_PARTY)} "
            f"missing_presence={missing_presence or 'none'} "
            f"missing_landmark={missing_landmark or 'none'}")


def _check_banter_coverage() -> Tuple[str, str]:
    cat = content.banter()
    covered = [t for t in banter_mod.TRIGGERS if cat.get(t)]
    missing = [t for t in banter_mod.TRIGGERS if not cat.get(t)]
    # every listed exchange must reference known party members
    bad = []
    for trig, exchanges in cat.items():
        for ex in exchanges:
            for p in ex.get("participants", []):
                if p not in _PARTY:
                    bad.append(f"{trig}:{p}")
    status = "OK" if not missing and not bad else ("WARN" if not bad else "GAP")
    return (status,
            f"triggers={len(covered)}/{len(banter_mod.TRIGGERS)} "
            f"missing={missing or 'none'} unknown_participants={bad or 'none'}")


def _check_beat_and_encounter_coverage() -> Tuple[str, str]:
    state = frontier.run_frontier(seed=7)
    beats = [b["id"] for b in state.beats]
    anchors = {"sundered_span", "forge_stand", "lost_howl"}
    anchor_wins = all(b["won"] for b in state.beats if b["id"] in anchors)
    mapped = all(b in frontier_overlay.BEAT_CONTEXT for b in beats)
    ok = len(beats) == 9 and anchor_wins and mapped
    return ("OK" if ok else "GAP",
            f"beats={len(beats)} anchors_win={anchor_wins} all_beats_mapped={mapped}")


def _check_event_coverage() -> Tuple[str, str]:
    templates = content.event_templates()
    ids = {t["id"] for t in templates}
    expected = {
        "merchant_under_attack", "lost_child", "traveling_healer",
        "hidden_pack_scouts", "wandering_knight", "corrupted_wildlife",
        "refugee_caravan", "traveling_storyteller", "abandoned_campsite",
        "injured_animal",
    }
    missing = expected - ids
    all_have_choices = all(t.get("choices") for t in templates)
    status = "OK" if not missing and all_have_choices else "WARN"
    return (status,
            f"templates={len(templates)} required_present={not missing} "
            f"all_have_choices={all_have_choices} missing={sorted(missing) or 'none'}")


def _check_reputation_triggers() -> Tuple[str, str]:
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    _, world = frontier_overlay.build_overlay(golden, seed=7)
    worst = frontier.run_frontier(seed=7, decider=frontier.worst_decider)
    _, wworld = frontier_overlay.build_overlay(worst, seed=7)
    ok = len(world.deeds) >= 5 and all(d.npc_line for d in world.deeds)
    reactive = len(world.deeds) > len(wworld.deeds)
    return ("OK" if ok and reactive else "WARN",
            f"golden_deeds={len(world.deeds)} worst_deeds={len(wworld.deeds)} "
            f"all_have_npc_line={all(d.npc_line for d in world.deeds)} reactive={reactive}")


def _check_memory_triggers() -> Tuple[str, str]:
    mem = content.regional_memory()
    covered = [s for s in STATES if mem.get(s, {}).get("changes")]
    have_prompt = all(mem.get(s, {}).get("prompt") for s in STATES if mem.get(s))
    status = "OK" if len(covered) == len(STATES) and have_prompt else "WARN"
    return (status,
            f"statuses_with_changes={len(covered)}/{len(STATES)} all_have_prompt={have_prompt}")


def _check_world_transitions() -> Tuple[str, str]:
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    _, world = frontier_overlay.build_overlay(golden, seed=7)
    transitions = [h for l in world.locations.values() for h in l.history]
    unnatural = [t for t in transitions if not t.get("natural")]
    status = "OK" if transitions and not unnatural else ("WARN" if transitions else "GAP")
    return (status,
            f"transitions={len(transitions)} all_natural={not unnatural} "
            f"unnatural={[(t['from'],t['to']) for t in unnatural] or 'none'}")


def _check_documentation() -> Tuple[str, str]:
    root = _repo_root()
    missing = [d for d in _DOCS if not os.path.exists(os.path.join(root, d))]
    return ("OK" if not missing else "GAP",
            f"present={len(_DOCS)-len(missing)}/{len(_DOCS)} missing={missing or 'none'}")


def _check_godot_compat() -> Tuple[str, str]:
    """Core framework modules must not do screen I/O or import an engine."""
    here = os.path.dirname(os.path.abspath(__file__))
    offenders: List[str] = []
    pat = re.compile(r"(?<![A-Za-z_])(print|input)\s*\(")
    for mod in _CORE_MODULES:
        path = os.path.join(here, f"{mod}.py")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        for m in pat.finditer(src):
            offenders.append(f"{mod}:{m.group(1)}")
    return ("OK" if not offenders else "GAP",
            f"core_modules={len(_CORE_MODULES)} screen_io={offenders or 'none'}")


def _check_serialization_roundtrip() -> Tuple[str, str]:
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    _, world = frontier_overlay.build_overlay(golden, seed=7)
    blob = json.dumps(world.to_state())
    from .world import LivingWorld
    back = LivingWorld.from_state(json.loads(blob))
    ok = back.to_state() == world.to_state()
    return ("OK" if ok else "GAP", f"living_world_json_roundtrip={ok}")


def _check_content_contract() -> Tuple[str, str]:
    from .region import RegionContent
    region = RegionContent.from_manifest("frontier_region")
    errors = region.validate()
    return ("OK" if not errors else "GAP",
            f"frontier_region contract errors={errors or 'none'}")


def _check_npc_population() -> Tuple[str, str]:
    from .region import RegionContent
    from . import npcs as npc_mod
    region = RegionContent.from_manifest("frontier_region")
    ref_errors = npc_mod.resolve_references(region.npcs, region)
    # every non-wilderness settlement/landmark should have at least one NPC
    inhabited = {n.get("location_id") for n in region.npcs}
    settlements = [l["id"] for l in region.locations
                   if l.get("kind") == "settlement"]
    empty_settlements = [s for s in settlements if s not in inhabited]
    categories = {n.get("category") for n in region.npcs}
    ok = (not ref_errors and not empty_settlements
          and len(region.npcs) >= 8 and "major" in categories)
    return ("OK" if ok else ("GAP" if ref_errors or empty_settlements else "WARN"),
            f"npcs={len(region.npcs)} categories={len(categories)} "
            f"ref_errors={ref_errors or 'none'} empty_settlements={empty_settlements or 'none'}")


def _check_save_persistence() -> Tuple[str, str]:
    from . import persistence
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    _, world = frontier_overlay.build_overlay(golden, seed=7)
    ws: dict = {}
    persistence.save_to_world_state(world, ws)
    # survive a JSON round-trip (as the save layer would do)
    ws = json.loads(json.dumps(ws))
    persistence.ensure_defaults(ws)
    back = persistence.load_from_world_state(ws)
    ok = back.to_state() == world.to_state()
    # legacy save (no living_world key) initializes to defaults safely
    legacy_ws: dict = {}
    persistence.ensure_defaults(legacy_ws)
    legacy = persistence.load_from_world_state(legacy_ws)
    legacy_ok = legacy.to_state() == persistence.default_state()
    return ("OK" if ok and legacy_ok else "GAP",
            f"world_state_roundtrip={ok} legacy_defaults_ok={legacy_ok}")


def _check_playtest_readiness() -> Tuple[str, str]:
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    worst = frontier.run_frontier(seed=7, decider=frontier.worst_decider)
    full = {"Ronan", "Talos", "Maeve Ashwood", "Torren", "Corwin", "Eleanor", "Ragash"}
    ok = (golden.region_outcome == "cleansed"
          and set(golden.party) == full and set(worst.party) == full
          and golden.howl_ending == "rescued")
    return ("OK" if ok else "WARN",
            f"golden_cleansed={golden.region_outcome=='cleansed'} "
            f"party_intact={set(golden.party)==full and set(worst.party)==full} "
            f"bram_saved={golden.howl_ending=='rescued'}")


def _check_outstanding_todos() -> Tuple[str, str]:
    here = os.path.dirname(os.path.abspath(__file__))
    todos: List[str] = []
    for root, _dirs, files in os.walk(here):
        for fn in files:
            if not fn.endswith((".py", ".json", ".md")):
                continue
            if fn == "region_review.py":  # skip the detector itself
                continue
            if fn.endswith("_report.json"):  # skip generated report artifacts
                continue
            with open(os.path.join(root, fn), encoding="utf-8") as fh:
                for i, line in enumerate(fh, 1):
                    if "TODO" in line or "FIXME" in line or "XXX" in line:
                        todos.append(f"{fn}:{i}")
    return ("OK" if not todos else "WARN",
            f"outstanding={todos or 'none'}")


CHECKS = [
    ("Region Completion", _check_completion),
    ("Companion Presence", _check_companion_coverage),
    ("Companion Banter", _check_banter_coverage),
    ("Quest / Encounter Coverage", _check_beat_and_encounter_coverage),
    ("Dynamic Events", _check_event_coverage),
    ("Reputation (Remembered Deeds)", _check_reputation_triggers),
    ("Regional Memory", _check_memory_triggers),
    ("World-State Transitions", _check_world_transitions),
    ("Documentation", _check_documentation),
    ("Godot Migration Compatibility", _check_godot_compat),
    ("Serialization Round-Trip", _check_serialization_roundtrip),
    ("Content Contract", _check_content_contract),
    ("NPC Population", _check_npc_population),
    ("Save Persistence", _check_save_persistence),
    ("Playtest Readiness", _check_playtest_readiness),
    ("Outstanding TODOs", _check_outstanding_todos),
]


def run() -> Dict:
    results = []
    for name, fn in CHECKS:
        try:
            status, detail = fn()
        except Exception as exc:  # noqa: BLE001
            status, detail = "GAP", f"exception: {exc!r}"
        results.append({"name": name, "status": status, "detail": detail})
    summary = {
        "total": len(results),
        "ok": sum(r["status"] == "OK" for r in results),
        "warn": sum(r["status"] == "WARN" for r in results),
        "gap": sum(r["status"] == "GAP" for r in results),
    }
    summary["region_ready"] = summary["gap"] == 0
    return {"region": "The Frontier", "summary": summary, "results": results}


def _print(report: Dict) -> None:
    icon = {"OK": "\u2713", "WARN": "!", "GAP": "\u2717"}
    print("\n== Region Completion Review — The Frontier ==\n")
    for r in report["results"]:
        print(f"  {icon.get(r['status'], '?'):>2} {r['status']:<4} {r['name']}")
        print(f"        {r['detail']}")
    s = report["summary"]
    print(f"\nTOTAL {s['total']}  OK {s['ok']}  WARN {s['warn']}  GAP {s['gap']}")
    print(f"REGION READY FOR REGION TWO: {'YES' if s['region_ready'] else 'NO'}\n")


def main() -> int:
    report = run()
    out = os.path.join(os.path.dirname(__file__), "region_review_report.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
    else:
        _print(report)
        print(f"(report written to {out})")
    return 0 if report["summary"]["region_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
