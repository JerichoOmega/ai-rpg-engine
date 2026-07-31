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

        self.status_effects = []

# =========================
# GLOBAL PLAYER INSTANCE
# =========================

player = Player()

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
    player.level        = ws.get("level",         player.level)
    player.gold         = ws.get("gold",          player.gold)