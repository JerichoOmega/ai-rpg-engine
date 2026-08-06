"""
The Frontier — First-Region Vertical Slice (playable end-to-end flow)
=====================================================================

Turns the design in ``docs/design/first_region_vertical_slice.md`` into a
**runnable, headless-testable** end-to-end flow that stitches the three existing,
separately-tested tactical showcases together with the connective **recruitment**
and **investigation** beats and lightweight skirmishes.

This module is an *orchestrator*: it **reuses** the canonical engine and the
existing showcase encounters — it does **not** fork or modify any combat system.
Combat beats delegate to:

* ``showcase``            — **The Sundered Span** (goblin ambush at the bridge)
* ``showcase_forge``      — **The Forge Stand** (Torren holds the forge)
* ``showcase_lost_howl``  — **The Lost Howl** finale ("save, don't slay")

The lighter travel beats (wolves on the road, a roadside ambush, the corrupted
woods) are resolved as real auto-battles built from ``enemies.json`` data, and the
recruitment/investigation beats advance party + story state. The whole slice runs
deterministically for a given seed so it can be verified.

Run interactively:  ``python scripts/play_frontier.py``
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from .battlefield import Battlefield
from .engine import CombatEngine, CombatContext
from . import enemies
from . import showcase
from . import showcase_forge
from . import showcase_lost_howl as lost_howl


# ---------------------------------------------------------------------------
# Run state
# ---------------------------------------------------------------------------
@dataclass
class FrontierState:
    party: List[str] = field(default_factory=lambda: ["Ronan"])   # Ronan starts with you
    clues: List[str] = field(default_factory=list)
    beats: List[Dict] = field(default_factory=list)
    ending: Optional[str] = None

    def recruit(self, *names: str) -> None:
        for n in names:
            if n not in self.party:
                self.party.append(n)


# ---------------------------------------------------------------------------
# Generic skirmish (real combat built from enemy data)
# ---------------------------------------------------------------------------
def _skirmish(enemy_spec, seed: int, max_rounds: int = 30) -> str:
    """Resolve a real auto-battle: the reference tactician party vs a spawned
    enemy group on an open field. Returns the engine's outcome string."""
    bf = Battlefield(11, 7, battlefield_id="frontier_skirmish")
    party = showcase.build_party()
    for i, hero in enumerate(party):          # deploy party on the west edge
        hero.x, hero.y = 1, 1 + i
    foes = [enemies.spawn_enemy(eid, x, y) for eid, x, y in enemy_spec]
    eng = CombatEngine(bf, party + foes,
                       context=CombatContext("location", "frontier_skirmish"),
                       rng=random.Random(seed))
    return eng.auto_battle(max_rounds=max_rounds,
                           player_controller=showcase.tactician_controller)


def _won(outcome: str) -> bool:
    o = (outcome or "").lower()
    return "player" in o or "victor" in o or "won" in o


# ---------------------------------------------------------------------------
# Beats
# ---------------------------------------------------------------------------
def _beat_road_in(state: FrontierState, seed: int) -> Dict:
    outcome = _skirmish([("wolf", 8, 1), ("wolf", 9, 3), ("dire_wolf", 8, 5)], seed)
    return {"id": "road_in", "title": "The Road In", "type": "combat",
            "teaches": "positioning & spacing (wolf pack flanking)",
            "outcome": outcome, "won": _won(outcome)}


def _beat_roadside_ambush(state: FrontierState, seed: int) -> Dict:
    outcome = _skirmish([("bandit", 8, 1), ("bandit_archer", 9, 0),
                         ("bandit_leader", 10, 2)], seed)
    # Talos steps between the party and the ambush — Duty.
    state.recruit("Talos")
    return {"id": "roadside_ambush", "title": "Ambush on the Road", "type": "combat",
            "teaches": "cover & kill-the-leader; Talos joins (Duty)",
            "outcome": outcome, "won": _won(outcome), "recruited": ["Talos"]}


def _beat_settlement(state: FrontierState, seed: int) -> Dict:
    # Recruitment beat — A Light in the Ashes. Maeve won't leave until it can stand.
    state.recruit("Maeve Ashwood")
    return {"id": "settlement", "title": "The Refugee Settlement", "type": "recruit",
            "teaches": "protect / civilian rescue; Maeve joins (Compassion)",
            "quest": "A Light in the Ashes", "recruited": ["Maeve Ashwood"],
            "outcome": "recruited", "won": True}


def _beat_sundered_span(state: FrontierState, seed: int) -> Dict:
    outcome = showcase.play_headless(seed=seed)
    return {"id": "sundered_span", "title": "The Sundered Span", "type": "combat",
            "teaches": "terrain, elevation, readability (gold-standard)",
            "outcome": outcome, "won": _won(outcome)}


def _beat_forge_stand(state: FrontierState, seed: int) -> Dict:
    outcome = showcase_forge.play_headless(
        seed=seed, controller=showcase_forge.forge_tactician_controller)
    state.recruit("Torren")
    return {"id": "forge_stand", "title": "Hold the Forge", "type": "combat",
            "teaches": "use the environment (build vs brawl); Torren joins (Honour & Legacy)",
            "outcome": outcome, "won": _won(outcome), "recruited": ["Torren"]}


def _beat_investigation(state: FrontierState, seed: int) -> Dict:
    # The Silent Witness seed — Corwin reads the world and finds what others missed.
    state.clues.append("corruption traced to the deep woods")
    state.recruit("Corwin")
    return {"id": "investigation", "title": "The Investigator's Warning", "type": "investigate",
            "teaches": "battlefield awareness / hidden info; Corwin joins (Truth & Discovery)",
            "quest": "The Silent Witness", "clue": state.clues[-1],
            "recruited": ["Corwin"], "outcome": "clue_found", "won": True}


def _beat_corrupted_woods(state: FrontierState, seed: int) -> Dict:
    outcome = _skirmish([("corrupted_wolf", 8, 1), ("corrupted_boar", 9, 3),
                         ("corrupted_goblin", 9, 5)], seed)
    state.recruit("Eleanor", "Ragash")
    return {"id": "corrupted_woods", "title": "The Corrupted Woods", "type": "combat",
            "teaches": "escalation of the familiar; Eleanor (Hope) & Ragash (Loyalty) join",
            "outcome": outcome, "won": _won(outcome),
            "recruited": ["Eleanor", "Ragash"]}


def _beat_lost_howl(state: FrontierState, seed: int) -> Dict:
    outcome, _ = lost_howl.resolve(lost_howl.compassion_controller, seed=seed)
    state.ending = outcome
    return {"id": "lost_howl", "title": "The Lost Howl (Finale)", "type": "combat",
            "teaches": "save, don't slay — Ronan's spine (Belonging)",
            "quest": "The Lost Howl", "outcome": outcome,
            "won": outcome == "rescued"}


BEATS: List[Callable[[FrontierState, int], Dict]] = [
    _beat_road_in,
    _beat_roadside_ambush,
    _beat_settlement,
    _beat_sundered_span,
    _beat_forge_stand,
    _beat_investigation,
    _beat_corrupted_woods,
    _beat_lost_howl,
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def run_frontier(seed: int = 7) -> FrontierState:
    """Play the whole Frontier slice end to end (headless, deterministic)."""
    state = FrontierState()
    rng = random.Random(seed)
    for beat in BEATS:
        state.beats.append(beat(state, rng.randint(0, 10_000)))
    return state


def slice_manifest() -> Dict:
    """Static description of the slice (region, beats, companions, quests)."""
    return {
        "region": "The Frontier",
        "beat_count": len(BEATS),
        "companions": ["Ronan", "Talos", "Maeve Ashwood", "Torren",
                       "Corwin", "Eleanor", "Ragash"],
        "anchor_showcases": ["The Sundered Span", "The Forge Stand", "The Lost Howl"],
        "finale_goal": "rescued",   # 'save, don't slay'
    }
