"""
hero_roster.py
==============

Canonical data for every predefined playable hero.

Each entry is a plain dict whose keys map directly onto
world_state["player"] fields (PlayerState) plus two extras:

  "race"         — display-only; persisted in player["race"]
  "key_trait"    — one-line character hook shown on the selection screen

All hero logic lives here as data. hero_select.py reads this dict and
writes the chosen entry into world_state["player"]. No per-hero
conditional logic should appear anywhere else in the codebase.

Source of truth: docs/PLAYER_SYSTEM.md, docs/characters/, docs/heroes/
"""

# =========================
# HERO ROSTER
# =========================
# Five confirmed heroes (Phase 1 — Predefined Hero Roster).
# Keys are the stable hero identifiers used in save files.

HERO_ROSTER = {

    "talos": {

        # ── Identity ───────────────────────────────────
        "name":           "Talos",
        "race":           "Elf",
        "player_class":   "Knight",
        "key_trait":      "Jaded veteran. Protective. Warm underneath.",

        # ── Stats ──────────────────────────────────────
        "hp":             120,
        "max_hp":         120,
        "attack_bonus":   6,
        "defense":        5,
        "dodge":          3,

        # ── Resource ───────────────────────────────────
        "resource_name":  "Stamina",
        "resource":       100,
        "max_resource":   100,

        # ── Economy ────────────────────────────────────
        "gold":           30,

        # ── Equipment ──────────────────────────────────
        # starting_equipment: slot → item display name (must match ITEM_DATABASE keys)
        # These items are moved into equipment slots at hero selection;
        # attack_bonus/defense already include their contributions.
        "equipped_weapon":    "Longsword",
        "weapon_bonus":       4,
        "starting_equipment": {"weapon": "Longsword", "armor": "Knight's Shield"},
        "inventory":          ["Longsword", "Knight's Shield"],

        # ── Progression ────────────────────────────────
        "level":          1,
        "xp":             0,
        "xp_to_next_level": 100,
    },

    "eleanor": {

        # ── Identity ───────────────────────────────────
        "name":           "Eleanor",
        "race":           "Human",
        "player_class":   "Mage",
        "key_trait":      "Young and optimistic. Unusually strong elemental bond.",

        # ── Stats ──────────────────────────────────────
        "hp":             75,
        "max_hp":         75,
        "attack_bonus":   10,
        "defense":        1,
        "dodge":          6,

        # ── Resource ───────────────────────────────────
        "resource_name":  "Mana",
        "resource":       120,
        "max_resource":   120,

        # ── Economy ────────────────────────────────────
        "gold":           20,

        # ── Equipment ──────────────────────────────────
        "equipped_weapon":    "Apprentice's Staff",
        "weapon_bonus":       6,
        "starting_equipment": {"weapon": "Apprentice's Staff"},
        "inventory":          ["Apprentice's Staff", "Healing Potion"],

        # ── Progression ────────────────────────────────
        "level":          1,
        "xp":             0,
        "xp_to_next_level": 100,
    },

    "ragash": {

        # ── Identity ───────────────────────────────────
        "name":           "Ragash",
        "race":           "Orc",
        "player_class":   "Houndmaster",
        "key_trait":      "Blunt and proud. Devoted to her hounds above all.",

        # ── Stats ──────────────────────────────────────
        "hp":             105,
        "max_hp":         105,
        "attack_bonus":   8,
        "defense":        3,
        "dodge":          5,

        # ── Resource ───────────────────────────────────
        "resource_name":  "Stamina",
        "resource":       100,
        "max_resource":   100,

        # ── Economy ────────────────────────────────────
        "gold":           15,

        # ── Equipment ──────────────────────────────────
        "equipped_weapon":    "Longsword",
        "weapon_bonus":       4,
        "starting_equipment": {"weapon": "Longsword"},
        "inventory":          ["Longsword", "Healing Potion"],

        # ── Progression ────────────────────────────────
        "level":          1,
        "xp":             0,
        "xp_to_next_level": 100,
    },

    "ronan": {

        # ── Identity ───────────────────────────────────
        "name":           "Ronan",
        "race":           "Human",
        "player_class":   "Werewolf",
        "key_trait":      "Cursed drifter. Seeks a cure. Fears losing control.",

        # ── Stats ──────────────────────────────────────
        "hp":             90,
        "max_hp":         90,
        "attack_bonus":   7,
        "defense":        2,
        "dodge":          10,

        # ── Resource ───────────────────────────────────
        "resource_name":  "Stamina",
        "resource":       100,
        "max_resource":   100,

        # ── Economy ────────────────────────────────────
        "gold":           10,

        # ── Equipment ──────────────────────────────────
        "equipped_weapon":    "Short Sword",
        "weapon_bonus":       3,
        "starting_equipment": {"weapon": "Short Sword"},
        "inventory":          ["Short Sword", "Short Sword"],

        # ── Progression ────────────────────────────────
        "level":          1,
        "xp":             0,
        "xp_to_next_level": 100,
    },

    "torren": {

        # ── Identity ───────────────────────────────────
        "name":           "Torren",
        "race":           "Human",
        "player_class":   "Master Blacksmith",
        "key_trait":      "Calm and reliable. Builds what endures.",

        # ── Stats ──────────────────────────────────────
        "hp":             115,
        "max_hp":         115,
        "attack_bonus":   7,
        "defense":        4,
        "dodge":          2,

        # ── Resource ───────────────────────────────────
        "resource_name":  "Stamina",
        "resource":       100,
        "max_resource":   100,

        # ── Economy ────────────────────────────────────
        "gold":           40,

        # ── Equipment ──────────────────────────────────
        "equipped_weapon":    "Forging Hammer",
        "weapon_bonus":       5,
        "starting_equipment": {"weapon": "Forging Hammer"},
        "inventory":          ["Forging Hammer", "Repair Kit"],

        # ── Progression ────────────────────────────────
        "level":          1,
        "xp":             0,
        "xp_to_next_level": 100,
    },
}

# Ordered list for display (selection screen iterates this).
HERO_ORDER = ["talos", "eleanor", "ragash", "ronan", "torren"]
