"""
Facing & Flanking (Phase A of the R-01 gameplay-canon migration)
================================================================

Additive tactical mechanics layered onto the verified combat engine. A
combatant's ``facing`` is set whenever it moves or attacks; a unit that has not
yet acted has ``facing is None`` and is treated as facing every attacker
(``front``) so existing behaviour is preserved until a unit actually commits a
direction.

Attacks resolve against the defender's facing:

* **front** — no modifier.
* **side**  — flanking: +hit.
* **rear**  — flanking: +hit and bonus damage.

These modifiers flow through the shared ``compute_hit_chance`` so the player and
the AI read the exact same information (no hidden values).
"""

from __future__ import annotations

from typing import Optional, Tuple

XY = Tuple[int, int]

DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}

# Flanking modifiers (Gameplay Canon: position beats stats).
FACING_HIT = {"front": 0.0, "side": 0.10, "rear": 0.20}
FACING_DMG = {"front": 1.0, "side": 1.0, "rear": 1.25}


def dir_from_to(a: XY, b: XY) -> str:
    """Cardinal direction from tile ``a`` toward tile ``b``."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    if abs(dx) >= abs(dy):
        if dx > 0:
            return "E"
        if dx < 0:
            return "W"
        return "S" if dy > 0 else "N"
    return "S" if dy > 0 else "N"


def relative_arc(defender, attacker_pos: XY) -> str:
    """Which arc of ``defender`` the attacker is in: front / side / rear.

    A defender that has not committed a facing (``None``) is considered to face
    the attacker, i.e. ``front`` (preserves pre-Phase-A behaviour)."""
    facing: Optional[str] = getattr(defender, "facing", None)
    if facing is None:
        return "front"
    fdx, fdy = DIRS[facing]
    dx = attacker_pos[0] - defender.x
    dy = attacker_pos[1] - defender.y
    dot = dx * fdx + dy * fdy
    if dot > 0:
        return "front"
    if dot < 0:
        return "rear"
    return "side"


def is_flanking(defender, attacker_pos: XY) -> bool:
    return relative_arc(defender, attacker_pos) in ("side", "rear")
