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
from tactical.living_world import frontier_overlay  # noqa: E402


def _render_living_world(beat_overlay):
    """Presentation only: render one beat's living-world overlay (no rules)."""
    for p in beat_overlay.get("presence", []):
        print(f"        · {p['line']}")
    ev = beat_overlay.get("banter")
    if ev:
        who = " & ".join(ev["participants"])
        print(f"        ~ banter ({ev['trigger']}) [{who}]:")
        for line in ev["lines"]:
            print(f"            {line['speaker']}: \"{line['text']}\"")
    for d in beat_overlay.get("environment", []):
        print(f"        » {d['description']}")
        if d.get("corwin_insight"):
            print(f"          {d['corwin_insight']}")
    for m in beat_overlay.get("landmark_moments", []):
        print(f"        ✦ (optional) {m['line']}")
    event = beat_overlay.get("event")
    if event:
        print(f"        ! world event — {event['title']}: {event['description']}")


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
    overlay, world = frontier_overlay.build_overlay(state, seed=seed)
    beat_overlays = {b["beat_id"]: b for b in overlay["beats"]}

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
        bo = beat_overlays.get(b["id"])
        if bo:
            _render_living_world(bo)

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

    # --- Living World: the region reacts, remembers, and endures -----------
    if world.deeds:
        print("\nThe Frontier remembers:")
        for d in world.deeds:
            print(f"  • {d.title} — \"{d.npc_line}\"")

    epi = overlay["epilogue"]
    print("\n" + "=" * 70)
    print(f"REGIONAL EPILOGUE — {epi['title']}  "
          f"({epi['positives']}/{epi['total']} threads hopeful)")
    print("=" * 70)
    for th in epi["threads"]:
        mark = "+" if th["outcome"] == "hopeful" else "~"
        print(f" [{mark}] {th['subject']}")
        print(f"      {th['text']}")
    print("-" * 70)
    print(epi["closing"])

    print("\n" + "=" * 70)
    print("RETURN TO THE FRONTIER — what a revisiting traveller now sees")
    print("=" * 70)
    for r in frontier_overlay.revisit_reports(world):
        if r["status"] in ("restored", "recovering", "prosperous", "corrupted"):
            print(f"\n{r['name']} [{r['status']}] — {r['prompt']}")
            for c in r["changes"]:
                print(f"    - {c}")
    print("=" * 70)


if __name__ == "__main__":
    main()
