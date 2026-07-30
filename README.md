# AI-Driven Terminal RPG

A terminal-based role-playing game written in Python, featuring an AI Director that shapes narrative pacing, turn-based combat, quests, factions, economy, companions, and a persistent world state.

---

## Getting Started

```bash
python main.py
```

No external dependencies required. Python 3.6+ only.

---

## If You Are an AI Assistant or New Developer

**Start here, in this order:**

1. **[`AI_START_HERE.md`](AI_START_HERE.md)** — Session startup guide, development rules, and shutdown checklist. Read this before touching anything.
2. **[`docs/handoffs/<latest>.md`](docs/handoffs/)** — What happened in the previous session.
3. **[`PROJECT_MEMORY.md`](PROJECT_MEMORY.md)** — Full project quick-start (under 5 minutes).
4. **[`PROJECT_STATE.md`](PROJECT_STATE.md)** — Current health: completion %, bugs, priorities.
5. **[`PROJECT_CONSTITUTION.md`](PROJECT_CONSTITUTION.md)** — Governing principles and rules.

---

## Project Structure

```
main.py                    ← entry point
game_loop.py               ← command dispatcher
world_state.py             ← all mutable game state
event_bus.py               ← cross-module communication
dm_brain.py                ← AI Director / narrative pacing
llm_bridge.py              ← LLM abstraction layer (mocked)
combat.py                  ← turn-based combat
quests.py                  ← quest system
faction_manager.py         ← faction reputation
save_manager.py            ← manual save/load
state_manager.py           ← auto-save
[28 more modules...]

docs/                      ← full documentation suite
├── GAME_BIBLE.md          ← game design canon
├── AI_CONTINUATION_GUIDE.md
├── architecture.md
├── coding_standards.md
├── known_issues.md
├── roadmap.md
├── systems/               ← per-system deep dives
└── handoffs/              ← session handoff records

app.py                     ← separate Flask UI prototype (not the game)
```

---

## Documentation

Full documentation index: [`docs/README.md`](docs/README.md)

| Document | Purpose |
|---|---|
| [`AI_START_HERE.md`](AI_START_HERE.md) | Session startup and shutdown guide |
| [`PROJECT_CONSTITUTION.md`](PROJECT_CONSTITUTION.md) | Governing principles |
| [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md) | Quick-start overview |
| [`PROJECT_STATE.md`](PROJECT_STATE.md) | Current project health |
| [`DESIGN_DECISIONS.md`](DESIGN_DECISIONS.md) | Architectural decisions |
| [`CHANGELOG.md`](CHANGELOG.md) | Development history |
| [`docs/GAME_BIBLE.md`](docs/GAME_BIBLE.md) | Game design canon |

---

## Current Status

**v0.4 — Integration Complete / Documentation Complete**

~58% overall. Playable core engine with combat, quests, factions, save/load, and AI pacing. Content and polish incomplete. LLM calls are mocked. See [`PROJECT_STATE.md`](PROJECT_STATE.md) for the full breakdown.

---

## Flask App

`app.py` and `ui_mockup/` are a separate browser-based interface prototype. They do not share code with the terminal game engine and can be run independently with `python app.py`.
