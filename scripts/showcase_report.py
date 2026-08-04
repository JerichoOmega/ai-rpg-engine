"""
Headless demonstration + verification artifact for the gold-standard encounter.

    python scripts/showcase_report.py

Runs the reference tactician plan, prints the battlefield, the pillar manifest,
the outcome, and a win-rate summary (competent play vs mindless attacking).
"""

import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tactical import showcase                     # noqa: E402
from tactical.render import render_battlefield     # noqa: E402


def main() -> int:
    eng = showcase.build_encounter(rng=random.Random(3))
    print("=== THE SUNDERED SPAN — gold-standard vertical slice ===\n")
    print(render_battlefield(eng))

    print("\n-- Canonical pillars demonstrated --")
    for pillar, info in showcase.pillar_manifest().items():
        print(f"  * {pillar}: {info['feature']}")

    out = eng.auto_battle(max_rounds=40,
                          player_controller=showcase.tactician_controller)
    print(f"\n-- Reference tactician run (seed 3): {out.upper()} in "
          f"round {eng.round} --")
    survivors = [u.name for u in eng.combatants if u.team == "player" and u.alive]
    print(f"   Surviving heroes: {survivors or 'none'}")
    for line in eng.log[-14:]:
        print("   " + line)

    tac, naive = Counter(), Counter()
    for s in range(30):
        e1 = showcase.build_encounter(rng=random.Random(s))
        tac[e1.auto_battle(max_rounds=40,
                           player_controller=showcase.tactician_controller)] += 1
        e2 = showcase.build_encounter(rng=random.Random(s))
        naive[e2.auto_battle(max_rounds=40)] += 1
    print(f"\n-- Win rate over 30 seeds --")
    print(f"   Competent tactics : {dict(tac)}  (target: players win a majority)")
    print(f"   Mindless attacking: {dict(naive)}  (target: the ambush punishes it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
