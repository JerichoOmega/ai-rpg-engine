"""
Text rendering & on-tile indicators
====================================

Terminal realisation of the spec's on-tile icons. A future graphical client
would render sprites from the same tile data; here we draw an ASCII map plus
a legend so information is always visible on the battlefield itself.
"""

from __future__ import annotations


def tile_icon(engine, x: int, y: int) -> str:
    """A single glyph summarising the tile (occupant takes priority)."""
    tile = engine.bf.tile(x, y)
    unit = engine.unit_at((x, y))
    if unit:
        initial = unit.cls[0].upper()
        return initial if unit.team == "player" else initial.lower()
    if tile.env.get("burning"):
        return "*"
    if "smoke" in tile.status_effects:
        return "%"
    icons = {
        "water": "~", "ice": "=", "oil_slick": "o", "scorched": ".",
        "hill": "^", "cliff_top": "A", "forest": "t", "rubble": ":",
        "road": "-", "plains": ".",
    }
    if any(o == "boulder" for o in tile.objects):
        return "O"
    if any(o == "wall_segment" for o in tile.objects):
        return "W"
    if any(o == "oil_barrel" for o in tile.objects):
        return "B"
    if any(o == "bridge_plank" for o in tile.objects):
        return "="
    if any(o == "pine_tree" for o in tile.objects):
        return "t"
    return icons.get(tile.terrain, ".")


LEGEND = (
    "Legend: UPPER=your units, lower=enemies | t tree(cover) O boulder "
    "W wall B barrel = bridge ^ hill A cliff ~ water = ice o oil * fire "
    "% smoke . open"
)


def render_battlefield(engine) -> str:
    rows = []
    header = "   " + " ".join(f"{x:>2}" for x in range(engine.bf.width))
    rows.append(header)
    for y in range(engine.bf.height):
        cells = " ".join(f"{tile_icon(engine, x, y):>2}"
                         for x in range(engine.bf.width))
        rows.append(f"{y:>2} {cells}")
    rows.append(LEGEND)
    living_p = ", ".join(f"{u.name}({u.hp}/{u.max_hp})"
                         for u in engine.living('player'))
    living_e = ", ".join(f"{u.name}({u.hp}/{u.max_hp})"
                         for u in engine.living('enemy'))
    rows.append(f"Allies: {living_p}")
    rows.append(f"Enemies: {living_e}")
    return "\n".join(rows)
