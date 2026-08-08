"""Live save-hookup tests for the Living World runtime.

These exercise the *actual* runtime save pathway (`save_manager` /
`state_manager`), not just the persistence layer in isolation — proving that a
real PLAY -> checkpoint/save -> new session -> load sequence restores
LivingWorldState. Every test is isolated from the real /app/save_data.json via a
temp SAVE_FILE and a snapshot/restore of the global world_state.
"""

import copy
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import save_manager
import state_manager
import world_state as ws_mod
from tactical.living_world import runtime, reputation, persistence
from tactical.living_world.region_state import LocationState


class _IsolatedSave:
    """Context manager: temp save file + world_state snapshot + clean runtime."""

    def __init__(self, module):
        self.module = module
        self.tmp = tempfile.mktemp(suffix=".json")
        self.backup = tempfile.mktemp(suffix=".bak.json")

    def __enter__(self):
        self._ws_snapshot = copy.deepcopy(ws_mod.world_state)
        self._orig_file = self.module.SAVE_FILE
        self.module.SAVE_FILE = self.tmp
        self._orig_backup = getattr(self.module, "BACKUP_FILE", None)
        if self._orig_backup is not None:
            self.module.BACKUP_FILE = self.backup
        runtime.clear_active()
        ws_mod.ensure_world_state_defaults()
        return self

    def reset_to_fresh(self):
        """Simulate a new session: world_state back to defaults, memory cleared.

        (The existing load_game overlays saved data onto a live world_state; it
        is not designed for a fully-empty dict, so we reset to a fresh default
        baseline — living_world empty — proving restoration comes from disk.)
        """
        ws_mod.world_state.clear()
        ws_mod.world_state.update(copy.deepcopy(self._ws_snapshot))
        runtime.clear_active()

    def __exit__(self, *exc):
        self.module.SAVE_FILE = self._orig_file
        if self._orig_backup is not None:
            self.module.BACKUP_FILE = self._orig_backup
        ws_mod.world_state.clear()
        ws_mod.world_state.update(self._ws_snapshot)
        runtime.clear_active()
        for f in (self.tmp, self.backup):
            if os.path.exists(f):
                os.remove(f)
        return False


def _seed_changes():
    """Simulate gameplay changing the living world through checkpoint API."""
    runtime.get_active().add_location(
        LocationState("greenhollow", "Greenhollow", kind="settlement",
                      status="corrupted", region_id="the_frontier"))
    runtime.set_region_status("greenhollow", "restored", "cleansed")   # region state
    runtime.record_deed(reputation.Deed(                                # remembered deed
        "saved_greenhollow", "Saved Greenhollow", reputation.RESTORE,
        "Cleansed and rebuilt Greenhollow.", npc_line="You saved us all.",
        location_id="greenhollow", region_id="the_frontier"))
    runtime.resolve_event("evt_merchant")                               # resolved event
    runtime.complete_landmark("Ronan", "greenhollow")                   # landmark moment
    runtime.mark_presence("Maeve Ashwood", "greenhollow")               # presence
    runtime.complete_region("the_frontier", {"status": "complete"})     # milestone


# --- 1. Fresh game ---------------------------------------------------------
def test_fresh_game_hydrates_to_defaults():
    with _IsolatedSave(save_manager):
        world = runtime.hydrate_from_world_state(ws_mod.world_state)
        assert world.to_state() == persistence.default_state()
        assert runtime.is_active()


# --- 2. Existing legacy save (no living_world block) ----------------------
def test_legacy_save_without_living_world_loads_and_backfills():
    with _IsolatedSave(save_manager) as iso:
        save_manager.save_game()  # write a normal save first
        on_disk = json.load(open(iso.tmp))
        on_disk["world_state"].pop("living_world", None)  # simulate pre-feature save
        json.dump(on_disk, open(iso.tmp, "w"))
        iso.reset_to_fresh()
        save_manager.load_game()  # must not crash; must backfill + hydrate
        assert "living_world" in ws_mod.world_state
        assert runtime.get_active().to_state() == persistence.default_state()


# --- 3-9. Full PLAY -> save -> new session -> load restores everything ----
def test_full_cycle_restores_all_living_world_state_via_save_manager():
    with _IsolatedSave(save_manager) as iso:
        runtime.hydrate_from_world_state(ws_mod.world_state)
        _seed_changes()  # 3. quest/world-state change at checkpoints

        save_manager.save_game()  # 4. save checkpoint (real pathway)
        assert os.path.exists(iso.tmp)
        disk = json.load(open(iso.tmp))["world_state"]["living_world"]
        assert any(d["id"] == "saved_greenhollow" for d in disk["deeds"])

        iso.reset_to_fresh()            # 5. new session (memory + world reset)
        save_manager.load_game()        # reload

        active = runtime.get_active()
        assert any(d.id == "saved_greenhollow" for d in active.deeds)   # 6. deed survived
        assert active.location("greenhollow").status == "restored"      # 7. region state
        assert "evt_merchant" in active.events_seen                      # 8. resolved event
        assert active.landmark_seen("Ronan", "greenhollow")             # 9. landmark
        assert "Maeve Ashwood@greenhollow" in active.presence_seen      # 9. presence
        assert active.region_progression("the_frontier")["status"] == "complete"
        # world_state mirror stays consistent with the runtime
        assert ws_mod.world_state["living_world"] == active.to_state()


# --- also proves the transition history (regional memory) survived --------
def test_region_transition_history_survives_save_load():
    with _IsolatedSave(save_manager) as iso:
        runtime.hydrate_from_world_state(ws_mod.world_state)
        runtime.get_active().add_location(
            LocationState("greenhollow", "Greenhollow", status="corrupted"))
        runtime.set_region_status("greenhollow", "restored", "cleansed")
        save_manager.save_game()
        iso.reset_to_fresh()
        save_manager.load_game()
        hist = runtime.get_active().location("greenhollow").history
        assert hist and hist[-1]["to"] == "restored" and hist[-1]["reason"] == "cleansed"


# --- 10. Multiple save/load cycles are stable -----------------------------
def test_multiple_save_load_cycles_are_stable():
    with _IsolatedSave(save_manager) as _iso:
        runtime.hydrate_from_world_state(ws_mod.world_state)
        _seed_changes()
        save_manager.save_game()
        target = runtime.get_active().to_state()
        for _ in range(3):
            _iso.reset_to_fresh()
            save_manager.load_game()
            assert runtime.get_active().to_state() == target
            save_manager.save_game()


# --- state_manager (second authoritative save system) also carries it -----
def test_full_cycle_via_state_manager():
    with _IsolatedSave(state_manager) as _iso:
        runtime.hydrate_from_world_state(ws_mod.world_state)
        _seed_changes()
        assert state_manager.save_game() is True
        _iso.reset_to_fresh()
        assert state_manager.load_game() is True
        active = runtime.get_active()
        assert any(d.id == "saved_greenhollow" for d in active.deeds)
        assert active.location("greenhollow").status == "restored"
        assert active.region_progression("the_frontier")["status"] == "complete"


# --- inactive session leaves save behaviour unchanged ---------------------
def test_inactive_session_does_not_alter_save_flow():
    with _IsolatedSave(save_manager) as iso:
        runtime.clear_active()  # no living world touched this session
        assert runtime.sync_into_world_state(ws_mod.world_state) is False
        save_manager.save_game()  # must still succeed
        assert os.path.exists(iso.tmp)


# --- real save_data.json is never touched by these tests ------------------
def test_real_save_file_untouched():
    real = "/app/save_data.json"
    before = os.path.getmtime(real) if os.path.exists(real) else None
    with _IsolatedSave(save_manager):
        runtime.hydrate_from_world_state(ws_mod.world_state)
        _seed_changes()
        save_manager.save_game()
    after = os.path.getmtime(real) if os.path.exists(real) else None
    assert before == after
