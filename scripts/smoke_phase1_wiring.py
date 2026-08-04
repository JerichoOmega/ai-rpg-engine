import builtins, sys
sys.path.insert(0, "/app")

# --- feed scripted input to the interactive menus ---
_answers = iter([])
def _fake_input(prompt=""):
    try:
        return next(_answers)
    except StopIteration:
        return ""      # default -> "back/stay/leave" in every menu
builtins.input = _fake_input

def feed(*xs):
    global _answers
    _answers = iter(xs)

import importlib
import world_state
from world_state import ensure_world_state_defaults, world_state as WS

# 0) world_state defaults present
ensure_world_state_defaults()
print("current_region:", WS["regions"]["current_region"])

# 1) save validation fix (npcs not required) + player sync exist
import state_manager, player
ok = state_manager.validate_world_state(WS)
print("validate_world_state(new game) ->", ok, "(expected truthy / no rejection)")
player.sync_world_state_from_player()
player.sync_player_from_world_state()
print("player sync round-trip OK; player.level=", player.player.level)

# stub out combat + world tick so menus don't block or fight
import combat, game_loop, world_actions
combat.quick_encounter = lambda *a, **k: print("[combat] quick_encounter() would run (stubbed)")
game_loop.process_game_tick = lambda *a, **k: print("[world] tick (stubbed)")
# world_actions imports process_game_tick lazily from game_loop, so patch there too
import types

# 2) world map (non-interactive display)
print("\n--- WORLD MAP ---")
world_actions.world_map_menu()

# 3) explore agency menu: choose 'Search' then check it dispatches
print("\n--- EXPLORE (choose Search=1) ---")
feed("1")
world_actions.explore_menu()

print("\n--- EXPLORE (choose Hunt=2 -> stubbed combat) ---")
feed("2")
world_actions.explore_menu()

# 4) settlement menu: enter first settlement, then leave immediately
print("\n--- SETTLEMENTS (enter #1, then leave) ---")
feed("1", "99")   # pick settlement 1, then 99 -> leave scene
world_actions.settlement_menu()

# 5) settlement scene: talk to locals path
print("\n--- SETTLEMENT SCENE talk-to-locals then leave ---")
from region_manager import get_region_settlements
s = get_region_settlements(WS["regions"]["current_region"])
if s:
    # find the 'Talk to the locals' index dynamically is hard; feed several
    feed("1", "99", "99")  # try an action, then leave
    world_actions.enter_settlement_scene(s[0])

# 6) travel menu: stay put (blank) — just verify it lists neighbors w/o error
print("\n--- TRAVEL (list + stay) ---")
feed("")   # stay here
world_actions.travel_menu()

print("\nALL SMOKE CHECKS COMPLETED (no exceptions).")
