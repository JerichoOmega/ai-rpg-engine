#!/usr/bin/env python3
"""Headless proof for The Forge Stand: compares Torren-builds vs Torren-brawls
win-rates over many seeds. Run: python scripts/forge_showcase_report.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tactical import showcase_forge as sf  # noqa: E402


def main() -> None:
    seeds = 40
    forge = sf.win_rate(sf.forge_tactician_controller, seeds=seeds)
    brawl = sf.win_rate(sf.no_forge_controller, seeds=seeds)
    print("=" * 60)
    print("THE FORGE STAND — Torren Field-Forge showcase")
    print("=" * 60)
    print(f"Seeds per controller: {seeds}")
    print(f"Torren BUILDS (Field Forge):  {forge*100:5.1f}% wins")
    print(f"Torren BRAWLS (no constructs): {brawl*100:5.1f}% wins")
    print(f"Delta (the value of the Field Forge): {(forge-brawl)*100:+.1f} pts")
    print("-" * 60)
    print("Sample battle log (forge, seed 0):")
    eng = sf.build_encounter(rng=__import__("random").Random(0))
    outcome = eng.auto_battle(max_rounds=40,
                              player_controller=sf.forge_tactician_controller)
    for line in eng.log[-14:]:
        print("  " + line)
    print(f"  => outcome: {outcome}")


if __name__ == "__main__":
    main()
