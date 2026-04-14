from __future__ import annotations

import math
import string
from collections import Counter
from typing import Literal

EntropyClass = Literal["clean", "noisy", "garbled"]

_NOISY_THRESHOLD = 4.5
_GARBLED_THRESHOLD = 5.0
_NOISE_PENALTY_WEIGHT = 4.0

_PLAIN_CHARS = frozenset(
    string.ascii_letters + string.digits + " \t\n\r.,;:-'\"()"
)


def character_entropy(text: str) -> float:
    """Shannon entropy (bits/char) of `text`."""
    if not text:
        return 0.0
    counts = Counter(text)
    total = len(text)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy


def _effective_entropy(text: str) -> float:
    if not text:
        return 0.0
    base = character_entropy(text.lower())
    noise = sum(1 for c in text if c not in _PLAIN_CHARS)
    return base + (noise / len(text)) * _NOISE_PENALTY_WEIGHT


def is_garbled(text: str, *, threshold: float = _NOISY_THRESHOLD) -> bool:
    """True when effective entropy exceeds `threshold`."""
    return _effective_entropy(text) > threshold


def classify_by_entropy(text: str) -> EntropyClass:
    """Map effective entropy to 'clean' (<4.5), 'noisy' (<5.0), 'garbled' (>=5.0)."""
    score = _effective_entropy(text)
    if score < _NOISY_THRESHOLD:
        return "clean"
    if score < _GARBLED_THRESHOLD:
        return "noisy"
    return "garbled"
