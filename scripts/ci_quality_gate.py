#!/usr/bin/env python3
"""
CI Quality Gate — headless, engine-agnostic validation for Elyndor.
===================================================================

A single command that gates changes on the whole quality bar, runnable in any
headless Python environment (no Godot, no browser, no display). It fails (exit
code 1) if any of the following fail:

* Tactical Combat Foundation verification (`tactical.verify`)
* Region Completion Review (`tactical.living_world.region_review`)
* Living-world content contracts (region manifests validate)
* Living-world save round-trip (persist -> JSON -> load is identical; legacy
  saves initialize to defaults)
* Documentation contract (required docs present)

Usage::

    python scripts/ci_quality_gate.py            # run the gate
    python scripts/ci_quality_gate.py --pytest    # also run the full pytest suite

Intended to run alongside `python -m tactical.verify` in CI.
"""

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tactical import verify as tactical_verify  # noqa: E402
from tactical import frontier  # noqa: E402
from tactical.living_world import region_review, persistence, frontier_overlay  # noqa: E402
from tactical.living_world.region import RegionContent  # noqa: E402

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REGION_MANIFESTS = ["frontier_region", "testregion_region"]
_REQUIRED_DOCS = [
    "docs/systems/living_world.md",
    "docs/architecture/ENGINE_INTERFACES.md",
    "docs/architecture/GODOT_MIGRATION_PLAN.md",
    "docs/architecture/LAYER_RULES.md",
]


def _gate_tactical_verify():
    report = tactical_verify.run()
    s = report["summary"]
    return (s["foundation_stable"],
            f"PASS {s['passed']}/{s['total']} FAIL {s['failed']} WARN {s['warned']}")


def _gate_region_review():
    report = region_review.run()
    s = report["summary"]
    return (s["region_ready"],
            f"OK {s['ok']}/{s['total']} WARN {s['warn']} GAP {s['gap']}")


def _gate_content_contracts():
    errors = {}
    for name in _REGION_MANIFESTS:
        errs = RegionContent.from_manifest(name).validate()
        if errs:
            errors[name] = errs
    return (not errors, f"manifests={_REGION_MANIFESTS} errors={errors or 'none'}")


def _gate_save_roundtrip():
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    _, world = frontier_overlay.build_overlay(golden, seed=7)
    ws = {}
    persistence.save_to_world_state(world, ws)
    ws = json.loads(json.dumps(ws))
    persistence.ensure_defaults(ws)
    back = persistence.load_from_world_state(ws)
    roundtrip_ok = back.to_state() == world.to_state()
    legacy = {}
    persistence.ensure_defaults(legacy)
    legacy_ok = persistence.load_from_world_state(legacy).to_state() == \
        persistence.default_state()
    return (roundtrip_ok and legacy_ok,
            f"roundtrip={roundtrip_ok} legacy_defaults={legacy_ok}")


def _gate_documentation():
    missing = [d for d in _REQUIRED_DOCS
               if not os.path.exists(os.path.join(_ROOT, d))]
    return (not missing, f"required_docs_present={len(_REQUIRED_DOCS)-len(missing)}/"
                         f"{len(_REQUIRED_DOCS)} missing={missing or 'none'}")


GATES = [
    ("Tactical Verification", _gate_tactical_verify),
    ("Region Completion Review", _gate_region_review),
    ("Content Contracts", _gate_content_contracts),
    ("Save Round-Trip", _gate_save_roundtrip),
    ("Documentation Contract", _gate_documentation),
]


def _run_pytest() -> bool:
    print("\n[pytest] running full suite ...")
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=_ROOT)
    return proc.returncode == 0


def main() -> int:
    print("=" * 66)
    print("CI QUALITY GATE — Elyndor (headless, engine-agnostic)")
    print("=" * 66)
    all_ok = True
    for name, fn in GATES:
        try:
            ok, detail = fn()
        except Exception as exc:  # noqa: BLE001
            ok, detail = False, f"exception: {exc!r}"
        all_ok = all_ok and ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        print(f"         {detail}")

    if "--pytest" in sys.argv:
        pt = _run_pytest()
        all_ok = all_ok and pt
        print(f"  [{'PASS' if pt else 'FAIL'}] Full pytest suite")

    print("-" * 66)
    print(f"QUALITY GATE: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 66)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
