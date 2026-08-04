# Legacy Quest Authoring Toolkit

> A future developer should be able to author a complete Legacy Questline
> using **only** this document plus an existing quest as a reference. No
> engine code is required to add a quest — only JSON, dialogue, encounter
> and consequence design.

See also: [`legacy_quest_framework.md`](legacy_quest_framework.md) (architecture)
and the three shipped quests in `legacy/data/` (worked examples).

---

## 1. Workflow to author a new quest

1. Create `legacy/data/<quest_id>.json` (schema below).
2. Create `legacy/quests/<quest_id>.py`:
   ```python
   from legacy.framework.quest_framework import load_quest, Quest
   from legacy.framework import companion_affinity
   from legacy.quests import load_quest_data

   def build() -> Quest:
       return load_quest(load_quest_data("<quest_id>.json"))

   def register_banter() -> None:
       companion_affinity.register_banter("<context>", "<companion>", "line")
   ```
3. Add the module to `legacy.framework.registry.register_all`.
4. Run `python legacy/validator.py` (must be error-free), then add a
   `Scenario` to `legacy/harness.py`.

---

## 2. Quest JSON schema

### Top level (required unless noted)

| Field | Type | Notes |
|---|---|---|
| `id` | str | Unique quest id. |
| `name` | str | Display name. |
| `civilization` | str | Owning civilization (optional). |
| `featured_companion` | str | Recommended companion (optional, never required). |
| `theme` | str | One-line theme (optional). |
| `signature_encounter` | str | Name of the signature encounter (optional). |
| `start_stage` | str | Defaults to the first stage. |
| `stages` | list | Ordered list of stage objects. |
| `consequences` | list | Applied once on completion (optional). |

### Stage

| Field | Type | Notes |
|---|---|---|
| `id` | str | Unique within the quest. |
| `title` | str | |
| `description` | str | Optional intro narration. |
| `objectives` | list | `{id, description, optional?}`. |
| `steps` | list | Executed in order (see step types). |
| `next` | str \| null | Default next stage. `null` ends the quest. |

### Steps (`type` values)

| Type | Required fields | Optional |
|---|---|---|
| `narrate` | `text` | `speaker` |
| `banter` | `context` | |
| `dialogue` | `tree` | `on_outcome` (outcome→effects) |
| `speech_check` | `id`, `skill` | `difficulty`, `prompt`, `preparation_flags`, `companion_insight`, `civilization`, `on_success`, `on_failure` |
| `choice` | `key`, `options` | `prompt` |
| `effects` | `effects` | |
| `complete_objective` | `objective` | |
| `encounter` | `spec` | |
| `split_party` | `plan` | `resolve`, `base_saved` |
| `resolve_evacuation` | — | `base_saved` |
| `reunite` | — | |
| `puzzle` | `puzzle` | |

### Choice option

```json
{"key": "mediate", "label": "Mediate the dispute.",
 "available_if": {"flag": "...", "companion": "...", "affinity_tier": "trusted",
                  "standing": {"civ": "stonefang", "min": 25}},
 "locked_note": "why it's locked", "effects": [ ...effects... ]}
```
> **Rule:** every `choice` step and every non-terminal dialogue node MUST
> have at least one option with no gate, so the main path is always
> reachable. The validator enforces this.

### Effects (used by `choice`, `speech_check` branches, `dialogue.on_outcome`, `effects`)

| `type` | Fields |
|---|---|
| `flag` | `name`, `value?` |
| `counter` | `name`, `amount` |
| `affinity` | `companion`, `amount` |
| `standing` | `civ`, `amount` |
| `relationship` | `civ_a`, `civ_b`, `amount` |
| `reputation` | `faction`, `amount` |
| `complete_objective` | `objective` |
| `goto_stage` | `stage` (branch to another stage) |

---

## 3. Worked examples

### Dialogue tree (gated + check-driven)
```json
{"type": "dialogue",
 "tree": {"id": "q.elder", "start": "root", "nodes": [
   {"id": "root", "speaker": "Elder", "text": "Why should I trust you?",
    "choices": [
      {"key": "listen", "label": "I came to listen.", "goto": "info"},
      {"key": "insight", "label": "[Insight] The trouble began upstream, didn't it?",
       "check": {"id": "q.elder.insight", "skill": "insight", "difficulty": "medium",
                 "companion_insight": {"companion": "corwin", "tier": "warming"}},
       "on_success_goto": "trust", "on_failure_goto": "info"}]},
   {"id": "trust", "speaker": "Elder", "text": "You see clearly.",
    "choices": [{"key": "ok", "label": "Then let us begin.", "goto": "end",
                 "effects": [{"type": "flag", "name": "q_elder_trust"}]}]},
   {"id": "info", "speaker": "Elder", "text": "Very well.",
    "choices": [{"key": "ok", "label": "Continue.", "goto": "end"}]},
   {"id": "end", "outcome": "briefed"}]},
 "on_outcome": {"briefed": [{"type": "complete_objective", "objective": "meet_elder"}]}}
```

### Speech check (preparation rewarded, never a hard fail)
```json
{"type": "speech_check", "id": "q.negotiation", "skill": "diplomacy",
 "difficulty": "hard", "prompt": "You press for a lasting peace.",
 "preparation_flags": ["q_evidence", "q_elder_trust"],
 "on_success": [{"type": "flag", "name": "q_peace"}],
 "on_failure": [{"type": "flag", "name": "q_uneasy_truce"}]}
```

### Companion integration
```json
{"type": "choice", "key": "q.finale", "prompt": "How do you close the rite?",
 "options": [
   {"key": "companion", "label": "Let Corwin speak the word of rest.",
    "available_if": {"companion": "corwin", "affinity_tier": "warming"},
    "locked_note": "needs Corwin, warmed to you",
    "effects": [{"type": "affinity", "companion": "corwin", "amount": 5}]},
   {"key": "self", "label": "Stand in silent respect.",
    "effects": [{"type": "standing", "civ": "mossroot", "amount": 5}]}]}
```

### Timed / ritual encounter (ends on success, not elimination)
```json
{"type": "encounter", "spec": {
  "id": "q.ritual", "name": "The Defense", "type": "ritual_defense",
  "signature": true, "rounds": 8, "base_threat": 50, "threat_step": 7,
  "success_flag": "q_ritual_done",
  "escalation": ["Round 1 note", "...", "Round 8 note"],
  "optional_objectives": [
    {"id": "extra", "description": "Protect the saplings.",
     "requires": {"companion": "corwin", "tier": "trusted", "strength": 95},
     "flag_if_met": "q_saplings_saved"}],
  "on_complete_flags": ["q_defended"]}}
```

### Multi-stage encounter
```json
{"type": "encounter", "spec": {
  "id": "q.battle", "name": "The Assault", "type": "multi_stage", "signature": true,
  "waves": [
    {"name": "Wave 1", "threat": 55, "banter_context": "q.battle", "setback_flag": "q_wave1_loss"},
    {"name": "Wave 2", "threat": 70}],
  "on_complete_flags": ["q_held"]}}
```

### Environmental / engineering puzzle
```json
{"type": "puzzle", "puzzle": {
  "id": "q.lift", "title": "Restore the Lift", "description": "...",
  "on_solve_flags": ["q_lift_restored"],
  "steps": [
    {"id": "s1", "prompt": "What first?",
     "actions": [{"key": "prime", "label": "Prime the reservoirs."},
                 {"key": "force", "label": "Force it by hand."}],
     "correct": "prime", "hint": "Feed a machine before forcing it.",
     "reveal_companion": "talos", "reveal_tier": "warming",
     "reveal_line": "Feed the reservoirs first."}]}}
```

### Split party
```json
{"type": "split_party", "resolve": true, "base_saved": 25,
 "plan": {"id": "q.split", "main_companion": "corwin",
          "evacuation_group": ["kael", "lyra"], "reunion_context": "q.reunion"}}
```
Follow with a `reunite` step later to play reunion banter.

### Living-World consequences (branch-gated)
```json
"consequences": [
  {"type": "flag", "name": "region_at_peace"},
  {"type": "counter", "name": "refugees_settled", "amount": 40},
  {"type": "relationship", "civ_a": "humans", "civ_b": "stonefang",
   "amount": 30, "requires": "q_peace"},
  {"type": "future_hook", "name": "future_thing", "canon_pending": true}
]
```
To make a consequence drive a visible world change (merchants, patrols,
rumors, prosperity...), add the flag to
`legacy/data/living_world_reactions.json` — no code needed.

---

## 4. Best practices

* **Preparation over gates.** Use `preparation_flags` and `companion_insight`
  to *improve odds*, not to lock the only path.
* **Always leave an ungated fallback** in every choice/dialogue node.
* **Consequences read branch flags** via `requires` — set those flags during
  play so the world reflects how the quest went.
* **One signature encounter** per Legacy Questline; keep other combat lean.
* **Never invent canon.** Unknown names/lore → `CANON_PENDING` note; future
  content → `future_hook` (inert, never surfaced).
* **Validate early.** Run `python legacy/validator.py` after every edit.

## 5. Common mistakes

* A dialogue node with choices that are *all* gated → soft-lock (validator errors).
* A non-optional objective that is never `complete_objective`d on any path.
* A `next`/`goto_stage`/dialogue goto pointing at a missing id.
* A consequence `requires` flag that no branch ever sets (validator warns).
* Forgetting the terminal stage (`next: null`) or dialogue terminal node
  (`outcome`) → the validator flags the loop risk.
* Referencing an unknown `skill` or `difficulty` in a speech check.
