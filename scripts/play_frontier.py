#!/usr/bin/env python3
"""Play the Frontier first-region vertical slice end to end (headless).

Stitches the recruitment/investigation beats between the three existing tactical
showcases (Sundered Span, Forge Stand, Lost Howl) into one runnable flow.

Run: python scripts/play_frontier.py [seed]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tactical import frontier  # noqa: E402


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    man = frontier.slice_manifest()
    print("=" * 68)
    print(f"THE FRONTIER — first-region vertical slice  (seed {seed})")
    print("=" * 68)
    print(f"Region: {man['region']}  |  Beats: {man['beat_count']}  |  "
          f"Finale goal: {man['finale_goal']}")
    print("-" * 68)

    state = frontier.run_frontier(seed=seed)

    for i, b in enumerate(state.beats, 1):
        flag = "OK " if b["won"] else "!! "
        print(f"[{flag}] Beat {i}: {b['title']}  ({b['type']})")
        print(f"        teaches: {b['teaches']}")
        print(f"        outcome: {b['outcome']}")
        if b.get("recruited"):
            print(f"        recruited: {', '.join(b['recruited'])}")
        if b.get("clue"):
            print(f"        clue: {b['clue']}")

    print("-" * 68)
    print(f"Final party ({len(state.party)}): {', '.join(state.party)}")
    print(f"Clues gathered: {state.clues or 'none'}")
    print(f"Finale ending: {state.ending}")
    combat = [b for b in state.beats if b['type'] == 'combat']
    won = sum(1 for b in combat if b['won'])
    print(f"Combat beats won: {won}/{len(combat)}")
    print("=" * 68)


if __name__ == "__main__":
    main()
