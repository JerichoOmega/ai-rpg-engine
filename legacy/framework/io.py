"""
I/O adapter
===========

Every reusable framework talks to the player through an :class:`IOAdapter`
instead of calling ``print`` / ``input`` directly. This is the single seam
that lets the *same* quest content run in three ways:

* :class:`InteractiveIO`  -- a real player at the terminal.
* :class:`ScriptedIO`     -- the automated harness / regression tests, which
                             feed pre-recorded decisions and forced check
                             outcomes so every branch can be validated
                             non-interactively.
* Developer tools reuse :class:`ScriptedIO` to jump straight to a decision.

Framework code should depend only on the small surface defined here:
``say``, ``choose``, ``speech_outcome`` and ``roll``.
"""

from __future__ import annotations

import random
from typing import Any, Dict, List, Optional


class Option:
    """A single selectable choice presented by :meth:`IOAdapter.choose`."""

    def __init__(self, key: str, label: str, available: bool = True,
                 note: str = ""):
        self.key = key
        self.label = label
        self.available = available
        # ``note`` explains *why* an option is locked/unlocked (affinity,
        # reputation, a speech check, a world flag...). Shown to the player.
        self.note = note

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"Option({self.key!r}, available={self.available})"


class IOAdapter:
    """Base interface. Subclasses implement the actual transport."""

    def say(self, text: str, speaker: Optional[str] = None) -> None:
        raise NotImplementedError

    def choose(self, prompt: str, options: List[Option],
               key: Optional[str] = None, default: Optional[str] = None
               ) -> str:
        """Present ``options`` and return the ``key`` of the chosen one.

        ``key`` identifies this decision point so scripted runs can target
        it. ``default`` is the fallback option key when no script entry
        exists. Only ``available`` options may be returned.
        """
        raise NotImplementedError

    def speech_outcome(self, check_id: str, probability: float) -> bool:
        """Return True if a speech check succeeds. ``probability`` is the
        computed 0..1 success chance (already includes bonuses)."""
        raise NotImplementedError

    def roll(self, sides: int = 100) -> int:
        """Return a die roll in ``1..sides`` (seedable via the RNG)."""
        raise NotImplementedError


class InteractiveIO(IOAdapter):
    """Terminal adapter for a live player."""

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def say(self, text: str, speaker: Optional[str] = None) -> None:
        if speaker:
            print(f"\n{speaker}:")
            print(f'  "{text}"')
        else:
            print(f"\n{text}")

    def choose(self, prompt: str, options: List[Option],
               key: Optional[str] = None, default: Optional[str] = None
               ) -> str:
        available = [o for o in options if o.available]
        print(f"\n{prompt}")
        for index, option in enumerate(available, start=1):
            suffix = f"  ({option.note})" if option.note else ""
            print(f"  {index}. {option.label}{suffix}")
        # Also list locked options so the player can see what preparation
        # would have unlocked -- this is core to the "preparation is
        # rewarded, never a hard gate" philosophy.
        for option in options:
            if not option.available:
                note = option.note or "requires preparation"
                print(f"  -  {option.label}  [locked: {note}]")

        while True:
            raw = input("\nChoose: ").strip()
            if not raw and default:
                return default
            try:
                choice = available[int(raw) - 1]
                return choice.key
            except (ValueError, IndexError):
                print("Invalid choice.")

    def speech_outcome(self, check_id: str, probability: float) -> bool:
        return self.rng.random() < probability

    def roll(self, sides: int = 100) -> int:
        return self.rng.randint(1, sides)


class ScriptedIO(IOAdapter):
    """Non-interactive adapter driven by a recorded script.

    Used by the automated harness, regression tests, and developer tools.
    The script is a plain dict so tests can express exactly which branch
    they intend to exercise::

        ScriptedIO({
            "choices": {"debt.negotiation.approach": "mediate"},
            "speech":  {"debt.grakkor.insight": True},
            "seed": 7,
        })

    * ``choices`` maps a decision ``key`` to the chosen option ``key``.
    * ``speech``  forces a speech check result (True/False) by ``check_id``.
    * unmatched decisions fall back to the ``default`` (or first available).
    """

    def __init__(self, script: Optional[Dict[str, Any]] = None,
                 verbose: bool = False):
        script = script or {}
        self.choices: Dict[str, str] = dict(script.get("choices", {}))
        self.speech: Dict[str, bool] = dict(script.get("speech", {}))
        self.verbose = verbose
        self.rng = random.Random(script.get("seed", 1234))
        self.transcript: List[str] = []

    def say(self, text: str, speaker: Optional[str] = None) -> None:
        line = f"{speaker}: {text}" if speaker else text
        self.transcript.append(line)
        if self.verbose:
            print(line)

    def choose(self, prompt: str, options: List[Option],
               key: Optional[str] = None, default: Optional[str] = None
               ) -> str:
        available = [o for o in options if o.available]
        available_keys = {o.key for o in available}

        chosen = None
        if key and key in self.choices:
            candidate = self.choices[key]
            if candidate in available_keys:
                chosen = candidate
        if chosen is None and default in available_keys:
            chosen = default
        if chosen is None and available:
            chosen = available[0].key

        self.transcript.append(f"[choice {key}] -> {chosen}")
        if self.verbose:
            print(f"[choice {key}] -> {chosen}")
        return chosen

    def speech_outcome(self, check_id: str, probability: float) -> bool:
        if check_id in self.speech:
            return self.speech[check_id]
        return self.rng.random() < probability

    def roll(self, sides: int = 100) -> int:
        return self.rng.randint(1, sides)


# ---------------------------------------------------------------------------
# Ambient adapter
# ---------------------------------------------------------------------------
# Framework functions default to this adapter when a caller does not pass one
# explicitly. Interactive play uses the default; the harness and dev tools
# swap it out with `set_io`.
_active_io: IOAdapter = InteractiveIO()


def get_io() -> IOAdapter:
    return _active_io


def set_io(adapter: IOAdapter) -> IOAdapter:
    """Install ``adapter`` as the ambient IO and return the previous one so
    callers can restore it (harness/dev tools do this)."""
    global _active_io
    previous = _active_io
    _active_io = adapter
    return previous
