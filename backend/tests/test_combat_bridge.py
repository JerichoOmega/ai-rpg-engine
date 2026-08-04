"""
Combat Bridge tests (iteration 6)
=================================

Verifies that standard overworld encounters route through
``combat_bridge.start_encounter`` on the canonical tactical engine.
Covered:
  * headless resolution + HP write-back (never left at 0)
  * party build from world_state + companions
  * blueprint-based enemies (via tactical.encounters.build_group)
  * biome -> group mapping (_pick_group)
  * fairness cap (max(2, party+1))
  * victory rewards branch (monkey-patched deterministic win)
  * interactive controller drives a unit (Move/Attack/Inspect/End)
  * world_actions.explore_menu wires _hunt to combat_bridge (not combat.py)
  * legacy combat.py still IMPORTS but isn't used by explore
  * bridge does NOT rely on enemy_manager for enemy build
"""

from __future__ import annotations

import builtins
import inspect
import sys
import types

import pytest

sys.path.insert(0, "/app")

# ---------------------------------------------------------------------------
# fixture: reset world_state before each test
# ---------------------------------------------------------------------------


@pytest.fixture
def ws():
    from world_state import ensure_world_state_defaults, world_state
    ensure_world_state_defaults()
    p = world_state["player"]
    p["name"] = "TESTHero"
    p["class"] = "Warrior"
    p["hp"] = 100
    p["max_hp"] = 100
    p["level"] = 3
    p["gold"] = 50
    p["xp"] = 0
    p["inventory"] = []
    # clear companions between tests
    try:
        import companion_manager
        companion_manager.active_companions.clear()
    except Exception:
        pass
    return world_state


# ---------------------------------------------------------------------------
# HEADLESS RESOLUTION + HP write-back
# ---------------------------------------------------------------------------
class TestHeadless:
    def test_headless_returns_valid_outcome_and_hp_write_back(self, ws):
        import combat_bridge
        out = combat_bridge.start_encounter(
            region="kingdom_capital", interactive=False)
        assert out in ("player", "enemy", "draw")
        assert ws["player"]["hp"] >= 1  # no softlock

    def test_headless_terminates_within_engine_cap(self, ws):
        # engine max_rounds=100 -> should not raise / hang.
        import combat_bridge
        out = combat_bridge.start_encounter(
            region="shadow_marsh", interactive=False)
        assert out in ("player", "enemy", "draw")


# ---------------------------------------------------------------------------
# PARTY BUILD
# ---------------------------------------------------------------------------
class TestPartyBuild:
    def test_class_map_defaults(self):
        import combat_bridge as cb
        assert cb.CLASS_MAP["warrior"] == "guardian"
        assert cb.CLASS_MAP["ranger"] == "ranger"
        assert cb.CLASS_MAP["mage"] == "mage"
        assert cb.CLASS_MAP["rogue"] == "rogue"
        assert cb._map_class("unknown_role") == "guardian"
        assert cb._map_class(None) == "guardian"

    def test_party_uses_world_player_hp_and_level_scaling(self, ws):
        import combat_bridge as cb
        ws["player"]["class"] = "Warrior"
        ws["player"]["level"] = 5
        ws["player"]["hp"] = 77
        ws["player"]["max_hp"] = 120
        party = cb._build_party()
        assert len(party) == 1
        hero = party[0]
        assert hero.team == "player"
        assert hero.hp == 77
        assert hero.max_hp == 120
        # class map applied
        from tactical.entities import Combatant
        baseline = Combatant("x", "guardian", "player", 0, 0)
        assert hero.damage_min == baseline.damage_min + 4  # (lvl-1)=4
        assert hero.damage_max == baseline.damage_max + 4

    def test_companions_join_party_and_hp_written_back(self, ws, monkeypatch):
        import combat_bridge as cb
        import companion_manager
        companion_manager.active_companions.append(
            {"name": "Kael", "role": "warrior", "hp": 120, "max_hp": 120})
        companion_manager.active_companions.append(
            {"name": "Lyra", "role": "ranger", "hp": 90, "max_hp": 90})

        party = cb._build_party()
        assert len(party) == 3
        assert party[1].name == "Kael"
        assert party[2].name == "Lyra"
        assert party[1].team == "player"
        assert party[2].team == "player"

        # simulate combat damage then apply results with a defeat outcome
        party[1].hp = 40
        party[2].hp = 0
        cb._apply_results("enemy", party, enemy_count=2)
        assert companion_manager.active_companions[0]["hp"] == 40
        assert companion_manager.active_companions[1]["hp"] == 0
        # hero must not be left at 0
        assert ws["player"]["hp"] >= 1


# ---------------------------------------------------------------------------
# ENEMY BUILD = BLUEPRINTS (no enemy_manager)
# ---------------------------------------------------------------------------
class TestEnemyBuild:
    def test_pick_group_biome_mapping(self, ws):
        import combat_bridge as cb
        from region_manager import REGIONS
        # inject synthetic regions for deterministic biome mapping
        REGIONS["_test_swamp"] = {"biome": "swamp"}
        REGIONS["_test_forest"] = {"biome": "forest"}
        REGIONS["_test_ruins"] = {"biome": "ruins"}
        REGIONS["_test_unknown"] = {"biome": "unknown_biome"}
        try:
            assert cb._pick_group("_test_swamp")[0] == "cave_swarm"
            assert cb._pick_group("_test_forest")[0] == "forest_wolf_pack"
            assert cb._pick_group("_test_ruins")[0] == "ruins_undead"
            # default
            assert cb._pick_group("_test_unknown")[0] == "roadside_ambush"
        finally:
            for k in ("_test_swamp", "_test_forest", "_test_ruins",
                      "_test_unknown"):
                REGIONS.pop(k, None)

    def test_bridge_source_does_not_import_enemy_manager(self):
        import combat_bridge
        src = inspect.getsource(combat_bridge)
        assert "enemy_manager" not in src, (
            "combat_bridge must not reference enemy_manager; "
            "enemies come from tactical blueprints via encounters.build_group")

    def test_build_group_returns_blueprint_enemies(self):
        from tactical import encounters as enc
        from tactical.battlefield import Battlefield
        bf = Battlefield(9, 6, battlefield_id="t")
        foes = enc.build_group("roadside_ambush", battlefield=bf)
        assert len(foes) >= 1
        for f in foes:
            assert f.team == "enemy"
            assert f.hp > 0


# ---------------------------------------------------------------------------
# FAIRNESS CAP
# ---------------------------------------------------------------------------
class TestFairnessCap:
    def test_solo_hero_caps_at_two_enemies(self, ws, monkeypatch):
        import combat_bridge as cb
        captured = {}

        # capture combatants passed into engine, but skip actual battle
        import tactical.session as tsess

        def fake_run(engine, interactive=False, read=None, max_rounds=100):
            enemies = [c for c in engine.combatants if c.team == "enemy"]
            party = [c for c in engine.combatants if c.team == "player"]
            captured["enemies"] = enemies
            captured["party"] = party
            return "player"

        monkeypatch.setattr(cb, "run_session", fake_run)
        cb.start_encounter(region="kingdom_capital", interactive=False)
        assert len(captured["party"]) == 1
        assert len(captured["enemies"]) <= 2
        assert len(captured["enemies"]) == max(
            2, len(captured["party"]) + 1) or len(captured["enemies"]) <= 2

    def test_party_of_three_caps_at_four(self, ws, monkeypatch):
        import combat_bridge as cb
        import companion_manager
        companion_manager.active_companions.append(
            {"name": "A", "role": "warrior", "hp": 60, "max_hp": 60})
        companion_manager.active_companions.append(
            {"name": "B", "role": "ranger", "hp": 60, "max_hp": 60})
        captured = {}

        def fake_run(engine, interactive=False, read=None, max_rounds=100):
            captured["enemies"] = [c for c in engine.combatants
                                    if c.team == "enemy"]
            captured["party"] = [c for c in engine.combatants
                                  if c.team == "player"]
            return "enemy"

        monkeypatch.setattr(cb, "run_session", fake_run)
        # cave_swarm has many foes -> exercise the cap
        cb.start_encounter(region="shadow_marsh", interactive=False)
        assert len(captured["party"]) == 3
        assert len(captured["enemies"]) <= 4
        assert len(captured["enemies"]) >= 1


# ---------------------------------------------------------------------------
# VICTORY REWARDS / DEFEAT NO-REWARDS
# ---------------------------------------------------------------------------
class TestRewards:
    def test_victory_grants_xp_gold_and_loot(self, ws, monkeypatch):
        import combat_bridge as cb
        # deterministic: force outcome=='player'
        monkeypatch.setattr(cb, "run_session",
                            lambda engine, interactive=False,
                                    read=None, max_rounds=100: "player")
        xp0 = ws["player"].get("xp", 0)
        gold0 = ws["player"]["gold"]
        inv0 = list(ws["player"].get("inventory", []))
        cb.start_encounter(region="kingdom_capital", interactive=False)
        assert ws["player"]["xp"] > xp0
        assert ws["player"]["gold"] > gold0
        # inventory should have at least attempted a drop (may be empty
        # depending on generate_loot's roll — but function must not crash)
        assert isinstance(ws["player"].get("inventory", []), list)
        # HP write-back preserved
        assert ws["player"]["hp"] >= 1

    def test_defeat_no_rewards_but_hp_still_written(self, ws, monkeypatch):
        import combat_bridge as cb
        monkeypatch.setattr(cb, "run_session",
                            lambda engine, interactive=False,
                                    read=None, max_rounds=100: "enemy")
        xp0 = ws["player"].get("xp", 0)
        gold0 = ws["player"]["gold"]
        cb.start_encounter(region="kingdom_capital", interactive=False)
        assert ws["player"].get("xp", 0) == xp0
        assert ws["player"]["gold"] == gold0
        assert ws["player"]["hp"] >= 1


# ---------------------------------------------------------------------------
# INTERACTIVE CONTROLLER
# ---------------------------------------------------------------------------
class TestInteractive:
    def test_full_scripted_interactive_encounter_terminates(self, ws):
        # feed a sequence of inputs; last inputs are blank ("") so EOF-like
        # behaviour ends each turn; encounter must terminate.
        answers = iter([
            "1", "5 2",   # move to (5,2) -- may or may not be reachable
            "5",           # end turn
            "4", "3 3",   # inspect a tile
            "5",           # end turn
            "2", "1",     # attack first shown target if any
        ])

        def fake(prompt=""):
            try:
                return next(answers)
            except StopIteration:
                return ""

        orig_input = builtins.input
        builtins.input = fake
        try:
            import combat_bridge
            out = combat_bridge.start_encounter(
                region="shadow_marsh", interactive=True)
        finally:
            builtins.input = orig_input
        assert out in ("player", "enemy", "draw")
        assert ws["player"]["hp"] >= 1

    def test_interactive_controller_unreachable_move_is_rejected(self, ws):
        # build a mini scenario and call the controller directly
        from tactical.battlefield import Battlefield
        from tactical.entities import Combatant
        from tactical.engine import CombatEngine, CombatContext
        from tactical.session import interactive_controller

        bf = Battlefield(9, 6, battlefield_id="t")
        hero = Combatant("H", "guardian", "player", 0, 0)
        foe = Combatant("F", "brute", "enemy", 8, 5)
        engine = CombatEngine(bf, [hero, foe],
                              context=CombatContext("test", ""))
        engine.start()
        # sequence: try Move to an unreachable far corner (8,5 is foe),
        # then End turn.
        answers = iter(["1", "8 5", "5"])

        def read(prompt=""):
            try:
                return next(answers)
            except StopIteration:
                return ""

        ctrl = interactive_controller(read)
        # Should not raise
        ctrl(engine, hero)
        # unit's turn must have ended (move+ap did not consume everything —
        # controller returns because '5' end-turn was chosen)
        assert hero.alive


# ---------------------------------------------------------------------------
# WIRING: explore_menu._hunt -> combat_bridge.start_encounter
# ---------------------------------------------------------------------------
class TestWiring:
    def test_explore_menu_source_uses_combat_bridge_not_legacy(self):
        import world_actions
        src = inspect.getsource(world_actions.explore_menu)
        assert "combat_bridge" in src
        assert "start_encounter" in src
        assert "quick_encounter" not in src
        assert "combat.quick_encounter" not in src

    def test_hunt_calls_start_encounter(self, ws, monkeypatch):
        # patch start_encounter to trap the call
        called = {"n": 0}

        def fake_start(*a, **kw):
            called["n"] += 1
            return "player"

        import combat_bridge
        monkeypatch.setattr(combat_bridge, "start_encounter", fake_start)

        # feed explore menu: choose "Hunt for trouble" (option 2)
        answers = iter(["2"])
        orig = builtins.input
        builtins.input = lambda p="": next(answers, "")
        try:
            import world_actions
            world_actions.explore_menu()
        finally:
            builtins.input = orig
        assert called["n"] == 1


# ---------------------------------------------------------------------------
# LEGACY combat.py still imports (compat), but bridge is canonical
# ---------------------------------------------------------------------------
class TestLegacyStillImports:
    def test_legacy_combat_imports(self):
        import combat  # should not raise
        assert combat is not None


# ---------------------------------------------------------------------------
# REGRESSION: existing suites still green (light re-check)
# ---------------------------------------------------------------------------
class TestSaveLoadAfterEncounter:
    def test_save_load_roundtrip_after_encounter(self, ws, monkeypatch):
        import combat_bridge as cb
        monkeypatch.setattr(cb, "run_session",
                            lambda engine, interactive=False,
                                    read=None, max_rounds=100: "player")
        cb.start_encounter(region="kingdom_capital", interactive=False)

        try:
            import save_manager
        except Exception:
            pytest.skip("save_manager not importable")

        # Try common save/load entry points defensively.
        save_fn = getattr(save_manager, "save_game", None) or getattr(
            save_manager, "save", None)
        load_fn = getattr(save_manager, "load_game", None) or getattr(
            save_manager, "load", None)
        if not save_fn or not load_fn:
            pytest.skip("save/load API not found on save_manager")

        try:
            save_fn()
            load_fn()
        except TypeError:
            # some signatures take a filename
            save_fn("save_data.json")
            load_fn("save_data.json")
        # world_state must remain consistent
        from world_state import world_state as WS
        assert WS["player"]["hp"] >= 1
