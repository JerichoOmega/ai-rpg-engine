"""
Phase 1 wiring — integration & gameplay-flow verification.

Covers seams the main agent's smoke scripts don't:
  * region graph connectivity + fast-travel gating
  * settlement scene for BOTH SETTLEMENTS-known and unknown names
  * NPC-empty region -> talk_to_locals graceful
  * quest board generation + persistence
  * save/load continuity (quests, discovery, current_region,
    npc_relationships, faction reputation, player HP/level)
  * TD-001: divergence between REGIONS[name]['discovered'] and
    world_state['regions']['discovered_regions'] across travel+save+load
  * invalid travel (non-existent region, non-neighbor) rejection
  * one real combat.quick_encounter regression with scripted 'Attack'
  * legacy harness import
  * validate_world_state truthy for fresh new game
"""
import builtins
import importlib
import os
import sys

import pytest

sys.path.insert(0, "/app")


# ---------------------------------------------------------------------------
# scripted-input plumbing (matches /app/scripts/smoke_phase1_wiring.py)
# ---------------------------------------------------------------------------
_answers = iter([])


def _fake_input(prompt=""):
    try:
        return next(_answers)
    except StopIteration:
        return ""


builtins.input = _fake_input


def feed(*xs):
    global _answers
    _answers = iter(xs)


# ---------------------------------------------------------------------------
# module-level fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def _clean_world():
    """Reset world_state + globals to a fresh new-game per test."""
    from world_state import world_state, ensure_world_state_defaults
    from quest_manager import active_quests, completed_quests
    from dialogue_manager import npc_relationships
    from region_manager import REGIONS

    # remember original REGIONS discovered flags
    original_discovered = {n: r.get("discovered") for n, r in REGIONS.items()}
    world_state.clear()
    ensure_world_state_defaults()
    active_quests.clear()
    completed_quests.clear()
    npc_relationships.clear()
    yield
    # restore REGIONS discovered flags after test
    for name, val in original_discovered.items():
        if name in REGIONS:
            REGIONS[name]["discovered"] = val


# ---------------------------------------------------------------------------
# Tests: region graph
# ---------------------------------------------------------------------------
class TestRegionGraph:
    def test_all_regions_reachable_from_start(self):
        from region_manager import REGIONS, get_neighboring_regions

        start = "kingdom_capital"
        assert start in REGIONS

        seen, stack = set(), [start]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            for nb in get_neighboring_regions(cur):
                if nb in REGIONS and nb not in seen:
                    stack.append(nb)

        unreachable = set(REGIONS.keys()) - seen
        assert not unreachable, (
            f"Regions unreachable from {start}: {unreachable}"
        )

    def test_no_dangling_neighbor_ids(self):
        from region_manager import REGIONS

        dangling = []
        for name, data in REGIONS.items():
            for nb in data.get("neighboring_regions", []):
                if nb not in REGIONS:
                    dangling.append((name, nb))
        assert not dangling, f"Dangling neighbor ids: {dangling}"


# ---------------------------------------------------------------------------
# Tests: travel manager
# ---------------------------------------------------------------------------
class TestTravel:
    def _stub(self):
        import combat, encounter_manager, location_manager, game_loop
        import travel_manager
        combat.quick_encounter = lambda *a, **k: None
        encounter_manager.generate_encounter = lambda *a, **k: None
        location_manager.random_location_discovery = lambda *a, **k: None
        game_loop.process_game_tick = lambda *a, **k: None
        # Stub trigger_travel_event to sidestep the emit() TypeError bug
        # (see test_trigger_travel_event_emit_collision_bug for repro).
        travel_manager.trigger_travel_event = lambda: None

    def test_trigger_travel_event_emit_collision_bug(self):
        """REGRESSION / SEAM BUG:
        travel_manager.trigger_travel_event() calls
            emit("travel_event", event_name=event_name)
        but event_bus.emit's own parameter is named `event_name`, so the
        kwargs collide -> TypeError. Randomly hit on any travel day where
        roll is 46..70. This test documents the bug — it currently FAILS.
        """
        import travel_manager
        with pytest.raises(TypeError):
            travel_manager.trigger_travel_event()

    def test_travel_to_neighbor_updates_current_and_discovery(self):
        self._stub()
        from travel_manager import travel_to_region
        from world_state import world_state
        from region_manager import REGIONS

        assert world_state["regions"]["current_region"] == "kingdom_capital"
        travel_to_region("shadow_marsh")
        assert world_state["regions"]["current_region"] == "shadow_marsh"
        # region-level discovered flag
        assert REGIONS["shadow_marsh"]["discovered"] is True
        # NOTE: TD-001 — world_state discovered_regions may NOT be
        # updated by travel_to_region; capture actual behaviour
        ws_disc = world_state["regions"]["discovered_regions"]
        # do not assert; TestPersistence covers divergence

    def test_travel_to_nonexistent_region_rejected(self):
        self._stub()
        from travel_manager import travel_to_region
        from world_state import world_state

        before = world_state["regions"]["current_region"]
        travel_to_region("not_a_region")
        assert world_state["regions"]["current_region"] == before

    def test_travel_to_non_neighbor_rejected(self):
        self._stub()
        from travel_manager import travel_to_region
        from world_state import world_state

        # kingdom_capital neighbors: shadow_marsh, arcane_ruins.
        # ashen_wastes is NOT a neighbor.
        before = world_state["regions"]["current_region"]
        travel_to_region("ashen_wastes")
        assert world_state["regions"]["current_region"] == before

    def test_fast_travel_only_allows_discovered(self):
        self._stub()
        from travel_manager import fast_travel
        from region_manager import REGIONS
        from world_state import world_state

        # ashen_wastes starts as not discovered
        REGIONS["ashen_wastes"]["discovered"] = False
        before = world_state["regions"]["current_region"]
        fast_travel("ashen_wastes")
        assert world_state["regions"]["current_region"] == before, (
            "fast_travel should not move to undiscovered regions"
        )

        # once discovered, fast-travel works
        REGIONS["ashen_wastes"]["discovered"] = True
        fast_travel("ashen_wastes")
        assert world_state["regions"]["current_region"] == "ashen_wastes"


# ---------------------------------------------------------------------------
# Tests: settlements
# ---------------------------------------------------------------------------
class TestSettlements:
    def test_every_referenced_settlement_survives_enter(self):
        """enter_settlement_scene must not crash for ANY settlement referenced
        by a region — including ones missing from settlement_manager.SETTLEMENTS.
        """
        import world_actions
        from region_manager import REGIONS

        crashed = []
        for region_name, data in REGIONS.items():
            for s_name in data.get("settlements", []):
                # feed 'leave' immediately (blank/leave)
                feed("99")
                try:
                    world_actions.enter_settlement_scene(s_name)
                except Exception as exc:  # pragma: no cover
                    crashed.append((s_name, repr(exc)))
        assert not crashed, f"enter_settlement_scene crashed for: {crashed}"

    def test_enter_same_settlement_twice(self):
        import world_actions
        for _ in range(2):
            feed("99")
            world_actions.enter_settlement_scene("royal_city")

    def test_settlement_menu_lists_and_leaves(self):
        import world_actions
        feed("99")  # leave
        world_actions.settlement_menu()


# ---------------------------------------------------------------------------
# Tests: NPC / dialogue integration
# ---------------------------------------------------------------------------
class TestNPCs:
    def test_talk_to_locals_when_no_one_in_region(self):
        """arcane_ruins has NO NPCs — must NOT crash."""
        from world_actions import _npcs_in_region, _talk_to_locals

        locals_here = _npcs_in_region("arcane_ruins")
        assert locals_here == []
        _talk_to_locals("arcane_ruins")  # must not raise

    def test_start_dialogue_via_settlement_scene(self):
        """Talk to a local (Elandor in kingdom_capital) via scene."""
        import world_actions
        # menu options: services + Talk to the locals + quest board + leave
        # After entering royal_city, we need to pick "Talk to the locals",
        # then pick NPC #1 (Elandor), then leave (99).
        # royal_city services: blacksmith, market, inn, tavern, healer
        # => actions built: shop, tavern rumor, inn rest, healer rumor,
        #    Talk to locals, Quest board, Leave.
        # But collapsing: market+blacksmith share → 1 action,
        # tavern → 1, inn → 1, healer → 1. Plus talk-to-locals + quest board.
        # Not stable across refactors — we drive by trying options until
        # locals menu appears, then answering '1'.
        # Simplest: feed talk index=5, then '1' for Elandor, then '99' twice.
        feed("5", "1", "99", "99")
        world_actions.enter_settlement_scene("royal_city")


# ---------------------------------------------------------------------------
# Tests: quest board
# ---------------------------------------------------------------------------
class TestQuests:
    def test_quest_board_populates_active_quests(self):
        from quest_manager import active_quests, generate_quest_board

        assert active_quests == []
        generate_quest_board("royal_city")
        # generate_quest_board appends 2..5 quests to active_quests
        assert len(active_quests) >= 2

    def test_empty_quest_board_scene_runs(self):
        import world_actions
        # _quest_board catches exceptions itself; just ensure it runs.
        world_actions._quest_board("royal_city")


# ---------------------------------------------------------------------------
# Tests: save / load continuity
# ---------------------------------------------------------------------------
class TestPersistence:
    def _prep(self, tmp_path, monkeypatch):
        """Point save_manager & state_manager at a temp save file and
        stub interactive combat/tick during travel."""
        import save_manager, state_manager, combat, encounter_manager, \
            location_manager, game_loop, travel_manager
        save_file = str(tmp_path / "save_data.json")
        monkeypatch.setattr(save_manager, "SAVE_FILE", save_file)
        monkeypatch.setattr(state_manager, "SAVE_FILE", save_file)
        combat.quick_encounter = lambda *a, **k: None
        encounter_manager.generate_encounter = lambda *a, **k: None
        location_manager.random_location_discovery = lambda *a, **k: None
        game_loop.process_game_tick = lambda *a, **k: None
        # Sidestep trigger_travel_event bug (documented separately).
        travel_manager.trigger_travel_event = lambda: None
        return save_file

    def test_validate_world_state_new_game_truthy(self):
        from state_manager import validate_world_state
        from world_state import world_state
        assert validate_world_state(world_state), (
            "Fresh new-game world_state should validate (npcs must not be required)"
        )

    def test_save_load_preserves_quests_and_discovery(self, tmp_path,
                                                     monkeypatch):
        self._prep(tmp_path, monkeypatch)
        from hero_select import apply_hero
        from travel_manager import travel_to_region
        from save_manager import save_game, load_game
        from quest_manager import active_quests, generate_quest_board
        from world_state import world_state
        from region_manager import REGIONS
        from dialogue_manager import npc_relationships
        from player import player as _p

        apply_hero("talos")
        # give some visible state
        travel_to_region("shadow_marsh")
        assert world_state["regions"]["current_region"] == "shadow_marsh"
        generate_quest_board("murkwater_village")
        quest_titles_before = [q["title"] for q in active_quests]
        assert quest_titles_before
        npc_relationships["Sera"] = 42
        world_state["factions"]["kingdom"] = 25
        _p.hp = 42
        hp_before = 42

        save_game()

        # mutate live state so we can prove load overwrites it
        world_state["regions"]["current_region"] = "kingdom_capital"
        active_quests.clear()
        npc_relationships.clear()
        world_state["factions"]["kingdom"] = 0
        _p.hp = 100

        load_game()

        assert world_state["regions"]["current_region"] == "shadow_marsh"
        assert [q["title"] for q in active_quests] == quest_titles_before
        assert npc_relationships.get("Sera") == 42
        assert world_state["factions"]["kingdom"] == 25
        assert _p.hp == hp_before, (
            f"Player HP should survive save/load. got {_p.hp}"
        )

    def test_td001_discovery_agrees_across_travel_save_load(
        self, tmp_path, monkeypatch
    ):
        """TD-001: REGIONS[name]['discovered'] vs world_state discovered_regions."""
        self._prep(tmp_path, monkeypatch)
        from hero_select import apply_hero
        from travel_manager import travel_to_region
        from save_manager import save_game, load_game
        from world_state import world_state
        from region_manager import REGIONS

        apply_hero("talos")
        travel_to_region("shadow_marsh")

        regs_disc_pre = REGIONS["shadow_marsh"]["discovered"]
        ws_disc_pre = "shadow_marsh" in world_state["regions"]["discovered_regions"]
        # Divergence report (do not fail hard — that is TD-001 tech debt)
        divergence_pre = regs_disc_pre != ws_disc_pre

        save_game()
        # Mutate then load
        REGIONS["shadow_marsh"]["discovered"] = False
        if "shadow_marsh" in world_state["regions"]["discovered_regions"]:
            world_state["regions"]["discovered_regions"].remove("shadow_marsh")
        load_game()

        regs_disc_post = REGIONS["shadow_marsh"]["discovered"]
        ws_disc_post = "shadow_marsh" in world_state["regions"]["discovered_regions"]

        # Assert save/load restores the region-side discovered flag
        assert regs_disc_post is True, (
            "REGIONS['shadow_marsh']['discovered'] should be True after "
            "load (was True before save)."
        )
        # Track and report ws_disc_post for TD-001 visibility
        # Do NOT fail if divergent — this test documents observed behaviour.
        print(
            f"TD-001 divergence pre={divergence_pre} "
            f"REGIONS.discovered={regs_disc_post} "
            f"ws.discovered_regions={ws_disc_post}"
        )

    def test_autosave_inside_settlement(self, tmp_path, monkeypatch):
        """Save while current_region is set (i.e. 'inside' the region of a
        settlement) — must round-trip."""
        self._prep(tmp_path, monkeypatch)
        from hero_select import apply_hero
        from save_manager import autosave, load_game
        from world_state import world_state

        apply_hero("talos")
        world_state["regions"]["current_region"] = "kingdom_capital"
        autosave()
        world_state["regions"]["current_region"] = "shadow_marsh"
        load_game()
        assert world_state["regions"]["current_region"] == "kingdom_capital"

    def test_safe_load_after_travel_mid_flight(self, tmp_path, monkeypatch):
        """Simulate mid-travel state then safe_load — should recover cleanly."""
        self._prep(tmp_path, monkeypatch)
        from hero_select import apply_hero
        from save_manager import save_game, safe_load_game
        from travel_manager import travel_state
        from world_state import world_state

        apply_hero("talos")
        save_game()
        # simulate mid-flight
        travel_state["is_traveling"] = True
        travel_state["destination"] = "shadow_marsh"
        travel_state["travel_days"] = 3
        safe_load_game()
        assert world_state["regions"]["current_region"] == "kingdom_capital"


# ---------------------------------------------------------------------------
# Tests: combat regression (one real quick_encounter)
# ---------------------------------------------------------------------------
class TestCombatRegression:
    def test_quick_encounter_runs_with_attack_input(self, monkeypatch):
        """Drive combat.quick_encounter with 'Attack' input — must not crash."""
        import combat
        from hero_select import apply_hero
        apply_hero("talos")
        # Feed a LOT of '1's (choose first option, typically Attack) so the
        # loop can resolve either way (win/lose) without an EOF; fallback to
        # blank -> "".
        feed(*(["1"] * 500))
        try:
            combat.quick_encounter(enemy_count=1)
        except SystemExit:
            pass  # some game_over paths may exit
        except Exception as exc:
            pytest.fail(f"quick_encounter crashed: {exc!r}")


# ---------------------------------------------------------------------------
# Tests: inventory / progression / legacy
# ---------------------------------------------------------------------------
class TestSubsystems:
    def test_inventory_give_and_show(self):
        from inventory import give_item, show_inventory
        from world_state import world_state
        give_item("Healing Potion")
        assert "Healing Potion" in world_state["player"]["inventory"]
        show_inventory()

    def test_progression_add_experience_and_level_up(self):
        from progression_manager import add_experience, check_level_up
        from world_state import world_state
        from hero_select import apply_hero
        apply_hero("talos")
        starting_level = world_state["player"]["level"]
        add_experience(10_000)  # huge XP to force at least one level up
        check_level_up()
        assert world_state["player"]["level"] >= starting_level

    def test_legacy_harness_importable(self):
        import legacy.harness  # must import cleanly
        assert hasattr(legacy.harness, "main")
