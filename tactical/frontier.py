"""
The Frontier — First-Region Vertical Slice (playable, interactive end-to-end flow)
==================================================================================

Turns the design in ``docs/design/first_region_vertical_slice.md`` into a
**runnable, headless-testable** end-to-end flow that stitches the three existing,
separately-tested tactical showcases together with **real player-choice**
recruitment/investigation scenes, lightweight skirmishes, and the region's
**climactic finale** — *The Corruption Avatar*.

This module is an *orchestrator*: it **reuses** the canonical engine and the
existing showcase encounters — it does **not** fork or modify any combat system.
Combat beats delegate to:

* ``showcase``                    — **The Sundered Span** (goblin ambush at the bridge)
* ``showcase_forge``              — **The Forge Stand** (Torren holds the forge)
* ``showcase_lost_howl``          — **The Lost Howl** (Ronan's emotional climax)
* ``showcase_corruption_avatar``  — **The Corruption Avatar** (regional finale)

Player choice (engine-neutral)
------------------------------
Recruitment/investigation beats present a :class:`Choice` with real options that
have **meaningful, branching consequences** — flags, clues, rewards and how
hard the finale is (``preparedness``). Wrong choices make things harder or hide
lore, but the *golden* resolution stays reachable (no permanent companion loss
in the main campaign). Decisions are made by a **decider** callback so the same
flow runs headlessly in tests (``golden_decider`` / ``worst_decider``) or from a
terminal prompt (``scripts/play_frontier.py``) — the core carries **no** UI/input.

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
from . import showcase_corruption_avatar as avatar


# ---------------------------------------------------------------------------
# Choices (engine-neutral decision data)
# ---------------------------------------------------------------------------
@dataclass
class Choice:
    id: str
    prompt: str
    options: List[Dict] = field(default_factory=list)  # {id,label,desc,golden}

    def golden_id(self) -> str:
        return next((o["id"] for o in self.options if o.get("golden")),
                    self.options[0]["id"])

    def option(self, oid: str) -> Dict:
        return next(o for o in self.options if o["id"] == oid)


Decider = Callable[["FrontierState", Choice], str]


def golden_decider(state: "FrontierState", choice: Choice) -> str:
    """Default 'good judgement' player — always takes the golden option."""
    return choice.golden_id()


def worst_decider(state: "FrontierState", choice: Choice) -> str:
    """A player who always takes the sub-optimal option (proves branching)."""
    return next((o["id"] for o in choice.options if not o.get("golden")),
                choice.options[0]["id"])


# ---------------------------------------------------------------------------
# Run state
# ---------------------------------------------------------------------------
@dataclass
class FrontierState:
    party: List[str] = field(default_factory=lambda: ["Ronan"])   # Ronan starts with you
    clues: List[str] = field(default_factory=list)
    beats: List[Dict] = field(default_factory=list)
    flags: Dict[str, bool] = field(default_factory=dict)
    decisions: List[Dict] = field(default_factory=list)
    preparedness: int = 0
    howl_ending: Optional[str] = None
    region_outcome: Optional[str] = None

    def recruit(self, *names: str) -> None:
        for n in names:
            if n not in self.party:
                self.party.append(n)


def _make_chooser(state: FrontierState, decider: Decider):
    """Bind a decider to the state and record every decision made."""
    def choose(choice: Choice) -> Dict:
        oid = decider(state, choice)
        opt = choice.option(oid)
        rec = {"choice": choice.id, "prompt": choice.prompt,
               "chosen": oid, "label": opt["label"],
               "golden": bool(opt.get("golden"))}
        state.decisions.append(rec)
        return opt
    return choose


# ---------------------------------------------------------------------------
# Generic skirmish (real combat built from enemy data)
# ---------------------------------------------------------------------------
def _skirmish(enemy_spec, seed: int, max_rounds: int = 30) -> str:
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
# Beats  —  signature: (state, seed, choose) -> Dict
# ---------------------------------------------------------------------------
def _beat_road_in(state: FrontierState, seed: int, choose) -> Dict:
    outcome = _skirmish([("wolf", 8, 1), ("wolf", 9, 3), ("dire_wolf", 8, 5)], seed)
    return {"id": "road_in", "title": "The Road In", "type": "combat",
            "teaches": "positioning & spacing (wolf pack flanking)",
            "outcome": outcome, "won": _won(outcome)}


def _beat_roadside_ambush(state: FrontierState, seed: int, choose) -> Dict:
    opt = choose(Choice(
        "ambush_response",
        "Bandits spring an ambush on travellers ahead. How do you meet it?",
        [{"id": "shield_civilians", "label": "Shield the travellers first",
          "desc": "Body-block the ambush so no traveller falls — Talos is watching.",
          "golden": True},
         {"id": "break_through", "label": "Break through the ambushers",
          "desc": "Hit the leader fast; a traveller may get hurt in the crossfire."}],
    ))
    outcome = _skirmish([("bandit", 8, 1), ("bandit_archer", 9, 0),
                         ("bandit_leader", 10, 2)], seed)
    state.recruit("Talos")                    # Talos joins either way (Duty)
    if opt["id"] == "shield_civilians":
        state.flags["talos_trust"] = True
        state.preparedness += 1
    else:
        state.flags["civilian_hurt"] = True
        state.preparedness -= 1
    return {"id": "roadside_ambush", "title": "Ambush on the Road", "type": "combat",
            "teaches": "cover & kill-the-leader; Talos joins (Duty)",
            "choice": opt["label"], "outcome": outcome, "won": _won(outcome),
            "recruited": ["Talos"]}


def _beat_settlement(state: FrontierState, seed: int, choose) -> Dict:
    opt = choose(Choice(
        "settlement_help",
        "A refugee settlement is barely holding. Maeve won't leave until it can stand.",
        [{"id": "stay_and_secure", "label": "Stay and secure the settlement",
          "desc": "Fortify, treat the wounded, hear their story of what drove them here.",
          "golden": True},
         {"id": "press_on", "label": "Press on — time is short",
          "desc": "Leave quickly; Maeve follows but the camp stays fragile."}],
    ))
    state.recruit("Maeve Ashwood")            # Maeve joins either way (Compassion)
    if opt["id"] == "stay_and_secure":
        state.flags["settlement_secured"] = True
        state.preparedness += 1
        state.clues.append("refugees fled a blight radiating from the deep woods")
    else:
        state.flags["settlement_fragile"] = True
        state.preparedness -= 1
    return {"id": "settlement", "title": "The Refugee Settlement", "type": "recruit",
            "teaches": "protect / civilian rescue; Maeve joins (Compassion)",
            "quest": "A Light in the Ashes", "choice": opt["label"],
            "recruited": ["Maeve Ashwood"], "outcome": "recruited", "won": True}


def _beat_sundered_span(state: FrontierState, seed: int, choose) -> Dict:
    outcome = showcase.play_headless(seed=seed)
    return {"id": "sundered_span", "title": "The Sundered Span", "type": "combat",
            "teaches": "terrain, elevation, readability (gold-standard)",
            "outcome": outcome, "won": _won(outcome)}


def _beat_forge_stand(state: FrontierState, seed: int, choose) -> Dict:
    opt = choose(Choice(
        "forge_approach",
        "The forge can be held. Do you build the defence, or just stand and fight?",
        [{"id": "build_the_defence", "label": "Use the forge — build the defence",
          "desc": "Turn the environment into your weapon (Torren's way).",
          "golden": True},
         {"id": "brawl_it_out", "label": "Stand and trade blows",
          "desc": "Win it the hard way — costlier, and Torren notes the waste."}],
    ))
    # The set-piece stays a reliable anchor win; the choice colours the cost.
    outcome = showcase_forge.play_headless(
        seed=seed, controller=showcase_forge.forge_tactician_controller)
    state.recruit("Torren")
    if opt["id"] == "build_the_defence":
        state.flags["forge_mastered"] = True
        state.preparedness += 1
    else:
        state.flags["forge_costly"] = True
    return {"id": "forge_stand", "title": "Hold the Forge", "type": "combat",
            "teaches": "use the environment (build vs brawl); Torren joins (Honour & Legacy)",
            "choice": opt["label"], "outcome": outcome, "won": _won(outcome),
            "recruited": ["Torren"]}


def _beat_investigation(state: FrontierState, seed: int, choose) -> Dict:
    opt = choose(Choice(
        "investigation_method",
        "Corwin can trace the corruption's source — carefully, or quickly?",
        [{"id": "follow_the_evidence", "label": "Follow the evidence carefully",
          "desc": "Read the world; find what everyone else missed.",
          "golden": True},
         {"id": "chase_rumors", "label": "Chase the loudest rumour",
          "desc": "Faster, but you miss the deeper pattern."}],
    ))
    state.recruit("Corwin")                   # Corwin joins either way (Truth)
    if opt["id"] == "follow_the_evidence":
        clue = ("the blight radiates from an ancient wardstone-anchored presence "
                "deep in the woods — something old wearing the corruption like a mask")
        state.flags["knows_source"] = True
        state.preparedness += 1
    else:
        clue = "something in the deep woods is spreading the rot"
    state.clues.append(clue)
    return {"id": "investigation", "title": "The Investigator's Warning",
            "type": "investigate",
            "teaches": "battlefield awareness / hidden info; Corwin joins (Truth & Discovery)",
            "quest": "The Silent Witness", "choice": opt["label"], "clue": clue,
            "recruited": ["Corwin"], "outcome": "clue_found", "won": True}


def _beat_corrupted_woods(state: FrontierState, seed: int, choose) -> Dict:
    opt = choose(Choice(
        "woods_approach",
        "The woods you cleared aren't safe anymore. How do you push in?",
        [{"id": "cleanse_carefully", "label": "Advance carefully, cleanse as you go",
          "desc": "Methodical — the party reaches the heart in good order.",
          "golden": True},
         {"id": "push_hard", "label": "Push hard and fast",
          "desc": "Reach the source sooner, but arrive worn down."}],
    ))
    outcome = _skirmish([("corrupted_wolf", 8, 1), ("corrupted_boar", 9, 3),
                         ("corrupted_goblin", 9, 5)], seed)
    state.recruit("Eleanor", "Ragash")        # both join either way
    if opt["id"] == "cleanse_carefully":
        state.flags["woods_cleansed"] = True
        state.preparedness += 1
    else:
        state.flags["woods_costly"] = True
        state.preparedness -= 1
    return {"id": "corrupted_woods", "title": "The Corrupted Woods", "type": "combat",
            "teaches": "escalation of the familiar; Eleanor (Hope) & Ragash (Loyalty) join",
            "choice": opt["label"], "outcome": outcome, "won": _won(outcome),
            "recruited": ["Eleanor", "Ragash"]}


def _beat_lost_howl(state: FrontierState, seed: int, choose) -> Dict:
    # Ronan's emotional climax. Rescue is the canonical character beat; the
    # choice colours how bonded the Hidden Pack becomes (a finale ally boost).
    opt = choose(Choice(
        "howl_response",
        "The Lost Wolf — Bram — is cornered and terrified. What does Ronan do?",
        [{"id": "reach_out", "label": "Reach out — save, don't slay",
          "desc": "Subdue and shield him until the Pack arrives.",
          "golden": True},
         {"id": "hold_the_line", "label": "Hold the line and wait",
          "desc": "Keep him contained; he is still saved, but the Pack stays wary."}],
    ))
    outcome, _ = lost_howl.resolve(lost_howl.compassion_controller, seed=seed)
    state.howl_ending = outcome
    if opt["id"] == "reach_out" and outcome == "rescued":
        state.flags["pack_ally"] = True       # the Pack aids you at the finale
        state.preparedness += 1
    return {"id": "lost_howl", "title": "The Lost Howl (Ronan's Climax)",
            "type": "combat",
            "teaches": "save, don't slay — Ronan's spine (Belonging)",
            "quest": "The Lost Howl", "choice": opt["label"], "outcome": outcome,
            "won": outcome == "rescued"}


def _beat_corruption_avatar(state: FrontierState, seed: int, choose) -> Dict:
    # The regional finale the whole chapter builds toward. Corwin's evidence
    # (knows_source) telegraphs the wardstone mechanic; earlier good choices
    # (preparedness) make it easier. The golden read is always winnable.
    telegraph = ("Corwin's evidence pays off — the wardstones anchor the Avatar; "
                 "break them first." if state.flags.get("knows_source")
                 else "The Avatar's wounds keep knitting shut — something must be sustaining it.")
    opt = choose(Choice(
        "finale_strategy",
        "The Corruption Avatar rises at the heart of the blight. " + telegraph,
        [{"id": "break_the_anchors", "label": "Break the wardstones first",
          "desc": "Dismantle what sustains it, then strike the exposed Avatar.",
          "golden": True},
         {"id": "strike_the_heart", "label": "Throw everything at the Avatar",
          "desc": "Ignore the wardstones and hammer the boss directly."}],
    ))
    controller = (avatar.siege_controller if opt["id"] == "break_the_anchors"
                  else avatar.tunnel_controller)
    outcome, _ = avatar.resolve(controller, seed=seed, preparedness=state.preparedness)
    state.region_outcome = outcome
    return {"id": "corruption_avatar", "title": "The Corruption Avatar (Finale)",
            "type": "boss", "teaches": "don't tunnel the boss — break its wards first",
            "quest": "The Corruption Avatar", "choice": opt["label"],
            "identity": "_TBD_ (a manifestation of The Corruption, not a named individual)",
            "preparedness": state.preparedness, "outcome": outcome,
            "won": outcome == "cleansed"}


BEATS: List[Callable] = [
    _beat_road_in,
    _beat_roadside_ambush,
    _beat_settlement,
    _beat_sundered_span,
    _beat_forge_stand,
    _beat_investigation,
    _beat_corrupted_woods,
    _beat_lost_howl,
    _beat_corruption_avatar,
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def run_frontier(seed: int = 7, decider: Decider = golden_decider) -> FrontierState:
    """Play the whole Frontier slice end to end (headless, deterministic for a
    given seed + decider)."""
    state = FrontierState()
    choose = _make_chooser(state, decider)
    rng = random.Random(seed)
    for beat in BEATS:
        state.beats.append(beat(state, rng.randint(0, 10_000), choose))
    return state


def slice_manifest() -> Dict:
    """Static description of the slice (region, beats, companions, quests)."""
    return {
        "region": "The Frontier",
        "beat_count": len(BEATS),
        "companions": ["Ronan", "Talos", "Maeve Ashwood", "Torren",
                       "Corwin", "Eleanor", "Ragash"],
        "anchor_showcases": ["The Sundered Span", "The Forge Stand", "The Lost Howl"],
        "finale": "The Corruption Avatar",
        "howl_goal": "rescued",           # Ronan's climax: save, don't slay
        "finale_goal": "cleansed",        # the region is cleansed
    }
