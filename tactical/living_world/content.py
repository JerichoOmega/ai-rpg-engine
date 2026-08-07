"""
content — JSON content loader for the Living World (reusable).
==============================================================

Layer Rule 4: *content is data, code is rules.* The reusable frameworks live in
this package's modules; the First Region's actual content (its locations,
companion lines, banter, event templates, environmental details, epilogue
threads, regional-memory descriptors) lives in ``living_world/data/*.json``.

A future region ships new JSON here without touching the framework code.

Engine-agnostic: pure data access. No I/O beyond reading its own content files.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict

_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
_CACHE: Dict[str, Any] = {}


def data_dir() -> str:
    return _DATA_DIR


def load(name: str) -> Any:
    """Load and cache ``data/<name>.json``."""
    if name not in _CACHE:
        path = os.path.join(_DATA_DIR, f"{name}.json")
        with open(path, encoding="utf-8") as fh:
            _CACHE[name] = json.load(fh)
    return _CACHE[name]


def clear_cache() -> None:
    _CACHE.clear()


# Convenience accessors (one per content file) -----------------------------
def locations() -> list:
    return load("frontier_locations")


def companion_presence() -> dict:
    return load("companion_presence")


def companion_landmarks() -> dict:
    return load("companion_landmarks")


def banter() -> dict:
    return load("banter")


def event_templates() -> list:
    return load("event_templates")


def environment_details() -> list:
    return load("environment")


def regional_memory() -> dict:
    return load("regional_memory")


def epilogue_threads() -> dict:
    return load("epilogue_threads")
