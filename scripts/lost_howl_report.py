#!/usr/bin/env python3
"""Headless proof for The Lost Howl climax: the 'save, don't slay' objective swap.
Run: python scripts/lost_howl_report.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tactical import showcase_lost_howl as lh  # noqa: E402


def main() -> None:
    seeds = 30
    comp = lh.outcome_rate(lh.compassion_controller, "rescued", seeds=seeds)
    mur = lh.outcome_rate(lh.murderhobo_controller, "slain", seeds=seeds)
    print("=" * 62)
    print("THE LOST HOWL — climax objective-swap ('save, don't slay')")
    print("=" * 62)
    man = lh.objective_manifest()
    for k, v in man.items():
        print(f"  {k}: {v}")
    print("-" * 62)
    print(f"Seeds per playstyle: {seeds}")
    print(f"COMPASSION play  -> rescued: {comp*100:5.1f}%")
    print(f"MURDER-HOBO play -> slain (failure): {mur*100:5.1f}%")
    print("-" * 62)
    outcome, eng = lh.resolve(lh.compassion_controller, seed=0)
    print("Sample compassion log (seed 0):")
    for line in eng.log[-12:]:
        print("  " + line)
    print(f"  => outcome: {outcome}")


if __name__ == "__main__":
    main()
