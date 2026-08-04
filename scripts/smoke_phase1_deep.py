import builtins, sys
sys.path.insert(0, "/app")

_answers = iter([])
def _fake_input(prompt=""):
    try:
        return next(_answers)
    except StopIteration:
        return ""
builtins.input = _fake_input
def feed(*xs):
    global _answers; _answers = iter(xs)

from world_state import ensure_world_state_defaults, world_state as WS
ensure_world_state_defaults()

# stub interactive/combat/discovery bits used during travel days
import combat, game_loop, encounter_manager, location_manager, world_actions
combat.quick_encounter = lambda *a, **k: print("[combat stub]")
encounter_manager.generate_encounter = lambda *a, **k: print("[encounter stub]")
location_manager.random_location_discovery = lambda *a, **k: print("[discovery stub]")
game_loop.process_game_tick = lambda *a, **k: print("[world tick stub]")

print("BEFORE region:", WS["regions"]["current_region"])
# Travel to neighbor #1 (shadow_marsh). Blank answers thereafter.
feed("1")
world_actions.travel_menu()
print("AFTER region:", WS["regions"]["current_region"])

# Now in shadow_marsh: talk to a local (dialogue_manager) directly
region = WS["regions"]["current_region"]
locals_here = world_actions._npcs_in_region(region)
print("locals in", region, "->", [n for n, _ in locals_here])
if locals_here:
    feed("1", "1", "1")  # pick local #1, then whatever dialogue asks
    world_actions._talk_to_locals(region)

# Quest board in a settlement of this region
from region_manager import get_region_settlements
s = get_region_settlements(region)
print("settlements:", s)
if s:
    world_actions._quest_board(s[0])

print("\nDEEP PATH CHECKS COMPLETED (no exceptions).")
