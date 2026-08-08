"""Region One (Frontier) NPC population test suite.

Tests the reusable NPC content model and that Region One's inhabitants react to
the player's deeds, the region's state, and the Corruption Avatar outcome —
using the existing deed/regional-memory systems (no meter, no simulation).
Covers the 21 required checks; tests narrative paths, not just schema.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tactical import frontier
from tactical.living_world import npcs as N, frontier_overlay
from tactical.living_world.region import RegionContent
from tactical.living_world.world import LivingWorld

COMPANIONS = {"Maeve Ashwood", "Corwin", "Talos", "Torren", "Eleanor",
              "Ragash", "Ronan"}


def _region():
    return RegionContent.from_manifest("frontier_region")


def _fresh_world(region):
    """A brand-new Region One: nothing done yet (threatened/corrupted)."""
    return LivingWorld.from_content(region.locations)


def _completed_world():
    """A fully-cleansed Frontier with all major deeds recorded."""
    golden = frontier.run_frontier(seed=7, decider=frontier.golden_decider)
    overlay, world = frontier_overlay.build_overlay(golden, seed=7)
    return world, overlay["epilogue_flags"]


# 1. All NPC definitions load
def test_all_npcs_load():
    npcs = _region().npcs
    assert len(npcs) >= 8
    assert all("id" in n and "name" in n and "role" in n for n in npcs)


# 2. Unique ids
def test_npc_ids_unique():
    ids = [n["id"] for n in _region().npcs]
    assert len(ids) == len(set(ids))


# 3-9. All references resolve (locations, events, relationships, companions)
def test_all_references_resolve():
    region = _region()
    assert N.resolve_references(region.npcs, region) == []


def test_contract_validates():
    assert _region().validate() == []


# 4. Every NPC location resolves to a real location
def test_npc_locations_resolve():
    region = _region()
    loc_ids = {l["id"] for l in region.locations}
    assert all(n["location_id"] in loc_ids for n in region.npcs)


# 5. Every NPC yields a non-empty contextual line in every world state
def test_every_npc_has_dialogue_in_fresh_and_completed():
    region = _region()
    fresh = _fresh_world(region)
    done, flags = _completed_world()
    for npc in region.npcs:
        assert N.contextual_dialogue(npc, fresh, {}), npc["id"]
        assert N.contextual_dialogue(npc, done, flags), npc["id"]


# 10. NPC snapshot is deterministic
def test_describe_is_deterministic():
    region = _region()
    done, flags = _completed_world()
    npc = N.find(region.npcs, "campmother_alna")
    a = N.describe(npc, done, party=list(COMPANIONS), flags=flags)
    b = N.describe(npc, done, party=list(COMPANIONS), flags=flags)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


# 11 + 16. NPC memory/deed reactions + Corruption Avatar acknowledgement
def test_npcs_remember_deeds_and_dialogue_changes_after_events():
    region = _region()
    fresh = _fresh_world(region)
    done, flags = _completed_world()
    alna = N.find(region.npcs, "campmother_alna")
    # before: no deeds remembered, threatened/fearful line
    assert N.remembered_deeds(alna, fresh) == []
    before = N.contextual_dialogue(alna, fresh, {})
    # after: remembers helping refugees + breaking the avatar; line differs
    remembered = N.remembered_deeds(alna, done)
    assert "helped_refugees" in remembered and "broke_the_avatar" in remembered
    after = N.contextual_dialogue(alna, done, flags)
    assert before != after


# 16b. Corruption's true source stays unresolved (Scholar Nain)
def test_corruption_mystery_preserved():
    region = _region()
    done, flags = _completed_world()
    nain = N.find(region.npcs, "scholar_nain")
    line = N.contextual_dialogue(nain, done, flags)
    assert "did not die with it" in line or "does not close" in line.lower() \
        or "don't close" in line.lower()


# 14. Fresh Region One initializes correctly (fearful/threatened tone)
def test_fresh_region_one_npc_state():
    region = _region()
    fresh = _fresh_world(region)
    alna = N.find(region.npcs, "campmother_alna")
    fenn = N.find(region.npcs, "elder_fenn")
    assert N.presence(alna, fresh) == "fearful"          # camp threatened
    assert N.presence(fenn, fresh) == "fearful"          # greenhollow corrupted


# 15 + 17. Completed/restored Frontier changes NPC presence & dialogue
def test_restored_frontier_npc_changes():
    region = _region()
    done, flags = _completed_world()
    fenn = N.find(region.npcs, "elder_fenn")
    merra = N.find(region.npcs, "merra_merchant")
    fresh = _fresh_world(region)
    assert N.presence(fenn, done) == "present"           # no longer fearful
    # his line reacts to the cleansing (differs from his corrupted warning)
    corrupted_line = N.contextual_dialogue(fenn, fresh, {})
    restored_line = N.contextual_dialogue(fenn, done, flags)
    assert restored_line != corrupted_line
    assert "quiet now" in restored_line or "green" in restored_line.lower()
    # Merra's shop reopens language when restored
    assert N.presence(merra, done) == "present"


# 12 + 13. NPC memory survives save/load (derived from persisted deeds)
def test_npc_memory_survives_save_load_roundtrip():
    region = _region()
    done, flags = _completed_world()
    alna = N.find(region.npcs, "campmother_alna")
    before = N.remembered_deeds(alna, done)
    reloaded = LivingWorld.from_state(json.loads(json.dumps(done.to_state())))
    after = N.remembered_deeds(alna, reloaded)
    assert before == after and before  # non-empty and identical


# 7. Event references resolve to real event templates
def test_event_references_resolve():
    region = _region()
    event_ids = {e["id"] for e in region.event_templates}
    for npc in region.npcs:
        for ev in npc.get("events", []):
            assert ev in event_ids, f"{npc['id']} -> {ev}"


# 9. Companion hooks resolve and reactions gate on party presence
def test_companion_reactions_gate_on_party():
    region = _region()
    ordo = N.find(region.npcs, "huntsman_ordo")  # beast + belonging hooks
    with_ragash = N.companion_reactions(ordo, ["Ragash"])
    assert any(r["companion"] == "Ragash" for r in with_ragash)
    without = N.companion_reactions(ordo, ["Talos"])
    assert without == []


# 8 + 18. Companions are referenced, never redefined as NPCs (canon safety)
def test_companions_are_not_redefined_as_npcs():
    region = _region()
    npc_ids = {n["id"] for n in region.npcs}
    npc_names = {n["name"] for n in region.npcs}
    for c in COMPANIONS:
        assert c not in npc_names          # no NPC IS a companion
        assert c.lower().replace(" ", "_") not in npc_ids
    # but companions ARE referenced through relationships / hooks
    referenced = set()
    for n in region.npcs:
        for rel in n.get("relationships", []):
            if rel.get("with") in COMPANIONS:
                referenced.add(rel["with"])
    assert COMPANIONS & referenced  # at least some companions are referenced


# 19. No orphaned NPC content (every NPC placed in the region)
def test_no_orphaned_npcs():
    region = _region()
    for n in region.npcs:
        assert n.get("location_id") and n.get("category") in N.CATEGORIES


# 20. No Region Two leakage
def test_no_region_two_leakage():
    region = _region()
    assert all(n.get("region_id") == "the_frontier" for n in region.npcs)


# categories coverage — a believable mix of inhabitants
def test_category_mix_is_believable():
    cats = {n["category"] for n in _region().npcs}
    # major named characters + service/atmosphere + defenders + civilians
    assert {"major", "guard", "merchant", "civilian", "ambient"} <= cats


# every settlement is inhabited; remote wilderness is not overpopulated
def test_settlements_inhabited_wilderness_sparse():
    region = _region()
    inhabited = {}
    for n in region.npcs:
        inhabited[n["location_id"]] = inhabited.get(n["location_id"], 0) + 1
    for l in region.locations:
        if l.get("kind") == "settlement":
            assert inhabited.get(l["id"], 0) >= 1, f"empty settlement {l['id']}"
    # the boss arena / blight heart has no residents
    assert inhabited.get("blight_heart", 0) == 0
