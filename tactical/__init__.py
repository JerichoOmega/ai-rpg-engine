"""
tactical
========

Modular, data-driven tactical combat engine implementing
``Combat_Gameplay_Architecture.md`` (CANON). Every combat -- from the
overworld, a named location, a boss fight or a scripted event -- uses these
same systems, and the AI plays by the same rules as the player.

Quick start::

    from tactical.demo import build_demo
    engine = build_demo()
    outcome = engine.auto_battle()      # headless, AI vs AI
    print("\\n".join(engine.log))
"""

from .tiles import Tile                       # noqa: F401
from .battlefield import Battlefield          # noqa: F401
from .entities import Combatant               # noqa: F401
from .engine import CombatEngine, CombatContext  # noqa: F401

__all__ = ["Tile", "Battlefield", "Combatant", "CombatEngine",
           "CombatContext"]
