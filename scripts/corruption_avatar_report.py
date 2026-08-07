#!/usr/bin/env python3
"""Design-evidence report for the regional finale — **The Corruption Avatar**.

Proves the encounter's core lesson with a measurable gap: the *right* read
(break the wardstones first) reliably cleanses the region, while the naive read
(tunnel the boss) fails because the Avatar's wards nullify the damage.

Run: python scripts/corruption_avatar_report.py [seeds]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tactical import showcase_corruption_avatar as ca  # noqa: E402


def main() -> None:
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    man = ca.objective_manifest()

    print("=" * 70)
    print("THE CORRUPTION AVATAR — regional finale design report")
    print("=" * 70)
    print(f"Boss     : {man['name']}")
    print(f"Framing  : {man['framing']}")
    print(f"Mechanic : {man['mechanic']}")
    for p in man["phases"]:
        print(f"           - {p}")
    print(f"Lesson   : {man['lesson']}")
    print("-" * 70)

    siege = ca.outcome_rate(ca.siege_controller, "cleansed", seeds=seeds)
    tunnel = ca.outcome_rate(ca.tunnel_controller, "cleansed", seeds=seeds)
    t_fail = 1.0 - tunnel
    print(f"seeds tested: {seeds}")
    print(f"  BREAK THE WARDS (right)  -> cleansed: {siege*100:5.1f}%")
    print(f"  TUNNEL THE AVATAR (naive)-> cleansed: {tunnel*100:5.1f}%  "
          f"(failed: {t_fail*100:.1f}%)")
    print(f"  strategic gap: {(siege - tunnel)*100:+.1f} percentage points")
    print("-" * 70)

    for prep, label in [(1, "well-prepared (good choices)"),
                        (0, "neutral"),
                        (-1, "rushed/uninformed (poor choices)")]:
        r = ca.outcome_rate(ca.siege_controller, "cleansed", seeds=seeds,
                            preparedness=prep)
        print(f"  right read, {label:32s}: cleansed {r*100:5.1f}%")
    print("=" * 70)
    print(man["foreshadowing"])
    print("=" * 70)


if __name__ == "__main__":
    main()
