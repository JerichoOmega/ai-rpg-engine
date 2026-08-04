import builtins, sys
sys.path.insert(0, "/app")

from world_state import ensure_world_state_defaults, world_state as WS
ensure_world_state_defaults()
WS["player"]["hp"] = 100; WS["player"]["max_hp"] = 100
WS["player"]["level"] = 3; WS["player"]["gold"] = 50
WS["player"]["class"] = "Warrior"
xp0 = WS["player"].get("xp", 0); gold0 = WS["player"]["gold"]

import combat_bridge

print("========== HEADLESS (AI vs AI) ==========")
out = combat_bridge.start_encounter(region="kingdom_capital", interactive=False)
print("OUTCOME:", out)
print("player hp:", WS["player"]["hp"], "| xp:", WS["player"].get("xp"),
      "| gold:", WS["player"]["gold"])
assert out in ("player", "enemy", "draw")
assert WS["player"]["hp"] >= 1
print("headless OK")

print("\n========== INTERACTIVE (scripted input) ==========")
_answers = iter(["1", "5 2", "5"])   # Move to (5,2), then End turn; then EOF->end
def _fake(prompt=""):
    try: return next(_answers)
    except StopIteration: return ""
builtins.input = _fake

WS["player"]["hp"] = 100
out2 = combat_bridge.start_encounter(region="shadow_marsh", interactive=True)
print("OUTCOME:", out2)
assert out2 in ("player", "enemy", "draw")
print("interactive OK (completed, no exceptions)")

print("\n========== biome->group mapping ==========")
for r in ["kingdom_capital", "shadow_marsh"]:
    from region_manager import REGIONS
    g, b = combat_bridge._pick_group(r)
    print(f"{r}: biome={b} -> group={g}")

print("\nBRIDGE SMOKE COMPLETE (no exceptions).")
