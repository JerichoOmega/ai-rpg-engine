"""
Play the gold-standard encounter interactively:

    python scripts/play_showcase.py

You drive the four heroes through the canonical tactical engine; the goblins
use the shared AI. Everything you can see, the AI sees too.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tactical import showcase                     # noqa: E402
from tactical.render import render_battlefield     # noqa: E402
from tactical.session import run_session           # noqa: E402


def main() -> int:
    eng = showcase.build_encounter()
    print(__doc__)
    print("\n=== THE SUNDERED SPAN ===")
    print(showcase.build_battlefield.__module__)
    print(render_battlefield(eng))
    print("\nHeroes carry healing potions (menu option 4). Button-mashing loses "
          "here — flank, take the high ground, focus the shaman/warlord.\n")
    outcome = run_session(eng, interactive=True)
    print(f"\n=== {'VICTORY' if outcome == 'player' else 'DEFEAT'} "
          f"(round {eng.round}) ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
