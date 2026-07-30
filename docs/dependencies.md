# Dependencies

**Purpose:** Documents all runtime and development dependencies for the project.

---

## Overview

The terminal game has **zero external dependencies**. It runs on Python 3 using only the standard library. The Flask web application (`app.py`) requires Flask but is a separate, optional component.

---

## Runtime Dependencies — Terminal Game

| Module | Source | Used by |
|---|---|---|
| `json` | Python standard library | `save_manager.py`, `state_manager.py` |
| `random` | Python standard library | `combat.py`, `loot_manager.py`, `narrative_ai.py`, `llm_bridge.py`, and most game modules |
| `os` | Python standard library | `save_manager.py`, `state_manager.py` (file path operations) |

**No pip packages are required to run the terminal game.**

---

## Runtime Dependencies — Flask Web App (`app.py`)

| Package | Purpose |
|---|---|
| `flask` | Web server framework for the browser interface |

The Flask app is a separate interface prototype. It is not part of the terminal game's runtime.

---

## Python Version

Python 3 is required. The codebase uses:
- f-strings (Python 3.6+)
- Dict subclasses with property descriptors (Python 3.0+)
- Type hints are not yet used in this codebase

Exact minimum Python version is ⚠️ **NOT YET SPECIFIED** — any Python 3.6+ should work.

---

## LLM Integration (Optional, Not Currently Active)

`llm_bridge.py` is designed as a drop-in replacement point for LLM API calls. Currently all functions are mocked. When a real model is integrated:

| Potential dependency | Purpose |
|---|---|
| `openai` | OpenAI API client |
| `anthropic` | Anthropic Claude API client |
| `requests` | Generic HTTP client for self-hosted or alternative APIs |

No LLM package is currently required or installed.

---

## Development Tools

| Tool | Purpose | Required? |
|---|---|---|
| Python 3.6+ | Runtime | Yes |
| Any terminal / shell | Run the game | Yes |
| `py_compile` | Syntax checking (used in CI) | Optional |

---

## Installing Dependencies

### Terminal Game Only
```bash
# No installation needed beyond Python 3
python main.py
```

### With Flask App
```bash
pip install flask
python app.py
```

---

## Future Dependency Considerations

- If real LLM integration is added, an API client library will become a dependency. Document it here and in the relevant system doc when added.
- If a testing framework is adopted (pytest, unittest), add it to this file.
- If a configuration library (pydantic, attrs) is adopted for world_state typed sections, document it here.

---

## Revision History

| Date | Change |
|---|---|
| July 2026 | Initial documentation |
