class Player:

    def __init__(self):

        self.name = "Hero"

        self.hp = 100

        self.max_hp = 100

        self.attack_bonus = 5

        self.defense = 2

        self.evasion = 5

        self.level = 1

        self.gold = 0

        self.magic_power = 0

        self.status_effects = []

# =========================
# GLOBAL PLAYER INSTANCE
# =========================

player = Player()

# =========================
# SYNC WORLD STATE FROM PLAYER
# =========================

def sync_world_state_from_player():
    """Capture combat- and equipment-mutated Player fields into
    world_state["player"] before every save.

    Call once at the very start of every save path so that:
    - Combat HP changes (player.hp -= damage, player.hp += heal)
    - Skill/equipment stat bonuses (player.attack_bonus, .defense,
      .max_hp, .magic_power, .evasion)
    are persisted alongside the world-state-managed fields.

    Only the fields that the Player object owns as its mutation surface
    are written. Fields managed exclusively by world_state helpers
    (gold, inventory, name, class, race, hero_key, xp, resource…) are
    deliberately NOT touched — those are already authoritative in
    world_state["player"] from add_gold / remove_gold / add_item /
    apply_hero etc.

    Field mapping notes
    -------------------
    - player.evasion  →  world_state["player"]["dodge"]
      (reverse of the load-time mapping in sync_player_from_world_state)
    """

    from world_state import world_state

    ws = world_state.get("player")

    if not isinstance(ws, dict):

        return

    # Combat / equipment / skill-mutated fields only.
    # Do NOT overwrite gold, inventory, name, class, race, hero_key,
    # xp, resource — those are authoritative in world_state already.
    ws["hp"]           = player.hp
    ws["max_hp"]       = player.max_hp
    ws["attack_bonus"] = player.attack_bonus
    ws["defense"]      = player.defense
    ws["dodge"]        = player.evasion
    ws["magic_power"]  = player.magic_power
    ws["level"]        = player.level


# =========================
# SYNC FROM WORLD STATE
# =========================

def sync_player_from_world_state():
    """Re-populate the Player object from world_state["player"].

    Must be called after every load operation so that combat.py's
    direct `player.*` attribute reads always reflect the authoritative
    persisted data in world_state["player"].

    Field mapping notes
    -------------------
    - world_state["player"]["dodge"]  →  player.evasion
      (the two names were coined independently; "dodge" is the save-
      persistent key, "evasion" is the Player attribute name)
    """

    from world_state import world_state

    ws = world_state.get("player", {})

    if not isinstance(ws, dict):

        return

    player.name         = ws.get("name",         player.name)
    player.hp           = ws.get("hp",            player.hp)
    player.max_hp       = ws.get("max_hp",        player.max_hp)
    player.attack_bonus = ws.get("attack_bonus",  player.attack_bonus)
    player.defense      = ws.get("defense",       player.defense)
    player.evasion      = ws.get("dodge",         player.evasion)
    player.magic_power  = ws.get("magic_power",   player.magic_power)
    player.level        = ws.get("level",         player.level)
    player.gold         = ws.get("gold",          player.gold)