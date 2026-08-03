"""
legacy.quests
=============

The three approved Legacy Questlines. Each module exposes:

    build()            -> a fully-loaded ``Quest`` (parsed from its JSON).
    register_banter()  -> registers the quest's companion banter lines.

Quest *content* lives in ``legacy/data/<quest>.json``; these modules are the
thin registration layer. A future Legacy Questline is added by dropping in a
new JSON file, writing an equivalent module, and listing it in
``legacy.framework.registry.register_all``.
"""

import json
import os

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_quest_data(filename: str) -> dict:
    """Load and parse a quest JSON file from ``legacy/data``."""
    with open(os.path.join(_DATA_DIR, filename), "r", encoding="utf-8") as fh:
        return json.load(fh)
