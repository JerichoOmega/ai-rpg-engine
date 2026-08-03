"""
Split Party Framework
=====================

Some beats divide the party: the player takes one group forward while
others stay behind (evacuation, holding a line, a second objective). "What
the Forest Carries" is the first user -- Corwin accompanies the player while
two companions aid the evacuation -- but the framework is generic.

Guarantees:

* The split is **never mandatory** for completion. If the recommended
  companion is absent, the main group simply proceeds without them.
* The secondary group's outcome is influenced by **who** goes and their
  **affinity** (preparation reward), producing better/worse -- never
  failing -- evacuation results that feed Living-World consequences.
* Regrouping triggers **reunion dialogue / banter**.

State is stored under ``world_state["legacy"]["split_party"]`` so an
interrupted session can resume mid-split.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from world_state import world_state
from event_bus import emit
from .io import get_io
from . import companion_affinity


@dataclass
class SplitPartyPlan:
    id: str
    main_companion: Optional[str]          # accompanies the player
    evacuation_group: List[str]            # stay behind to help
    reunion_context: str = ""              # banter context for regrouping


@dataclass
class SplitPartyOutcome:
    id: str
    evacuation_quality: str                # "exemplary" | "steady" | "costly"
    saved: int
    notes: List[str] = field(default_factory=list)


def _split_store() -> Dict:
    legacy = world_state.setdefault("legacy", {})
    return legacy.setdefault("split_party", {})


def execute_split(plan: SplitPartyPlan, io=None) -> SplitPartyPlan:
    """Announce and record the split. Returns the (possibly adjusted) plan;
    absent companions are silently dropped so the main path is unaffected."""
    io = io or get_io()
    present = set(companion_affinity._active_party_names())

    main = plan.main_companion if plan.main_companion in present else None
    evac = [c for c in plan.evacuation_group if c in present]

    plan.main_companion = main
    plan.evacuation_group = evac

    _split_store()[plan.id] = {
        "main_companion": main, "evacuation_group": evac, "resolved": False}

    if main:
        io.say(f"{main.title()} moves forward with you.")
    else:
        io.say("You press forward alone; the way is harder without a guide.")
    if evac:
        io.say(f"{', '.join(c.title() for c in evac)} stay to shield the "
               f"evacuation.")
    else:
        io.say("No companions remain behind; the evacuation must fend for "
               "itself.")

    emit("party_split", plan_id=plan.id, main=main, evacuation=evac)
    return plan


def resolve_evacuation(plan: SplitPartyPlan, base_saved: int = 20,
                       io=None) -> SplitPartyOutcome:
    """Compute the evacuation result from group composition and affinity.

    More companions and higher affinity => more people saved and a better
    quality band. Zero companions still saves ``base_saved`` (a floor):
    the world continues either way.
    """
    io = io or get_io()
    saved = base_saved
    for companion in plan.evacuation_group:
        saved += 10 + companion_affinity.get_affinity(companion) // 10

    if saved >= base_saved + 30:
        quality = "exemplary"
    elif saved > base_saved:
        quality = "steady"
    else:
        quality = "costly"

    outcome = SplitPartyOutcome(plan.id, quality, saved)
    record = _split_store().setdefault(plan.id, {})
    record.update({"resolved": True, "quality": quality, "saved": saved})

    io.say(f"[Evacuation] {quality}: {saved} led to safety.")
    emit("evacuation_resolved", plan_id=plan.id, quality=quality, saved=saved)
    return outcome


def reunite(plan: SplitPartyPlan, io=None) -> None:
    """Regroup the party and play reunion banter."""
    io = io or get_io()
    io.say("The groups regroup.")
    if plan.reunion_context:
        companion_affinity.trigger_banter(plan.reunion_context, io=io)
    # Reuniting after a shared trial warms the whole active party a little.
    for companion in ([plan.main_companion] + plan.evacuation_group):
        if companion:
            companion_affinity.adjust_affinity(companion, 3)
    emit("party_reunited", plan_id=plan.id)


def from_dict(data: Dict) -> SplitPartyPlan:
    return SplitPartyPlan(
        id=data["id"],
        main_companion=data.get("main_companion"),
        evacuation_group=list(data.get("evacuation_group", [])),
        reunion_context=data.get("reunion_context", ""),
    )
