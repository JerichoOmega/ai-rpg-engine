#!/usr/bin/env python3
"""Play the Frontier first-region vertical slice end to end.

Stitches the interactive recruitment/investigation scenes between the three
tactical showcases (Sundered Span, Forge Stand, Lost Howl) and the regional
finale (The Corruption Avatar) into one runnable flow.

Modes:
    python scripts/play_frontier.py            # interactive prompts (falls back
                                               #   to the golden read if no TTY)
    python scripts/play_frontier.py 7 golden   # auto-play the golden read
    python scripts/play_frontier.py 7 worst    # auto-play the sub-optimal read
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tactical import frontier  # noqa: E402


def make_terminal_decider():
    """Prompt the player at each Choice; fall back to the golden option on an
    empty answer or when stdin is not interactive (keeps CI/headless runs safe)."""
    def decide(state, choice):
        if not sys.stdin.isatty():
            return choice.golden_id()
        print()
        print(f"  >> {choice.prompt}")
        for i, opt in enumerate(choice.options, 1):
            print(f"     {i}. {opt['label']} — {opt['desc']}")
        raw = input("     Choose [1] > ").strip()
        if not raw:
            return choice.options[0]["id"]
        try:
            return choice.options[int(raw) - 1]["id"]
        except (ValueError, IndexError):
            return choice.options[0]["id"]
    return decide


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    mode = sys.argv[2] if len(sys.argv) > 2 else "interactive"
    if mode == "golden":
        decider = frontier.golden_decider
    elif mode == "worst":
        decider = frontier.worst_decider
    else:
        decider = make_terminal_decider()

    man = frontier.slice_manifest()
    print("=" * 70)
    print(f"THE FRONTIER — first-region vertical slice  (seed {seed}, mode {mode})")
    print("=" * 70)
    print(f"Region: {man['region']}  |  Beats: {man['beat_count']}  |  "
          f"Finale: {man['finale']}")
    print("-" * 70)

    state = frontier.run_frontier(seed=seed, decider=decider)

    for i, b in enumerate(state.beats, 1):
        flag = "OK " if b["won"] else "!! "
        print(f"[{flag}] Beat {i}: {b['title']}  ({b['type']})")
        print(f"        teaches: {b['teaches']}")
        if b.get("choice"):
            print(f"        choice : {b['choice']}")
        print(f"        outcome: {b['outcome']}")
        if b.get("recruited"):
            print(f"        recruited: {', '.join(b['recruited'])}")
        if b.get("clue"):
            print(f"        clue: {b['clue']}")

    print("-" * 70)
    print(f"Final party ({len(state.party)}): {', '.join(state.party)}")
    print(f"Clues gathered: {state.clues or 'none'}")
    print(f"Flags: {sorted(k for k, v in state.flags.items() if v) or 'none'}")
    print(f"Preparedness going into the finale: {state.preparedness:+d}")
    print(f"Ronan's climax (Lost Howl): {state.howl_ending}")
    print(f"Region outcome (Corruption Avatar): {state.region_outcome}")
    if state.region_outcome == "cleansed":
        print("The Frontier is cleansed — but the true source of the blight "
              "remains unknown. (_TBD_)")
    print("=" * 70)


if __name__ == "__main__":
    main()
