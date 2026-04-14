"""Parametric Constraint NER — Task B.4 of Stream B."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Parameter:
    entity: str
    operator: str
    value: float
    unit: str
    start: int
    end: int
    evidence: str


_MIN_ANCHORS = r"minimum|min\.|at\s+least|not\s+less\s+than|no\s+less\s+than"
_MAX_ANCHORS = (
    r"maximum|max\.|at\s+most|not\s+more\s+than|no\s+more\s+than"
)
_EQ_ANCHORS = r"exactly|equal\s+to"

_VERB_PHRASE = r"shall\s+be|must\s+be|are|is|be"

_ENTITY = r"(?P<entity>[A-Za-z][A-Za-z\s\-]{0,60}?)"

_VALUE = r"(?P<value>\d+(?:\.\d+)?)"

_UNIT_ALTERNATIVES = (
    r"square\s+meters|square\s+feet|sq\s*m|sq\s*ft|sqm|sqft|"
    r"meters|meter|centimeters|centimeter|millimeters|millimeter|"
    r"percent|persons|people|occupants|stories|story|floors|floor|"
    r"hours|hour|minutes|minute|"
    r"cm|mm|m|%"
)
_UNIT = rf"(?P<unit>{_UNIT_ALTERNATIVES})"

_POSTFIX_ANCHOR_PATTERN = re.compile(
    rf"\b{_ENTITY}\s+(?:{_VERB_PHRASE})\s+"
    rf"(?P<anchor>{_MIN_ANCHORS}|{_MAX_ANCHORS}|{_EQ_ANCHORS})\s+"
    rf"{_VALUE}(?:\s*{_UNIT})?",
    re.IGNORECASE,
)

_PREFIX_ANCHOR_PATTERN = re.compile(
    rf"(?P<anchor>{_MIN_ANCHORS}|{_MAX_ANCHORS}|{_EQ_ANCHORS})\s+"
    rf"{_ENTITY}\s+(?:{_VERB_PHRASE})\s+"
    rf"{_VALUE}(?:\s*{_UNIT})?",
    re.IGNORECASE,
)

_UNIT_MAP: dict[str, str] = {
    "m": "meters",
    "meter": "meters",
    "meters": "meters",
    "cm": "centimeters",
    "centimeter": "centimeters",
    "centimeters": "centimeters",
    "mm": "millimeters",
    "millimeter": "millimeters",
    "millimeters": "millimeters",
    "%": "percent",
    "percent": "percent",
    "sqm": "sqm",
    "sq m": "sqm",
    "square meters": "sqm",
    "sq ft": "sqft",
    "sqft": "sqft",
    "square feet": "sqft",
    "persons": "occupants",
    "people": "occupants",
    "occupants": "occupants",
    "stories": "floors",
    "story": "floors",
    "floors": "floors",
    "floor": "floors",
    "hours": "hours",
    "hour": "hours",
    "minutes": "minutes",
    "minute": "minutes",
}

_NOISE_ENTITY_TOKENS = frozenset(
    {"the", "a", "an", "of", "for", "shall", "allowable", "allowed"}
)


def _normalise_unit(raw: str) -> str:
    key = re.sub(r"\s+", " ", raw.strip().lower())
    if key in _UNIT_MAP:
        return _UNIT_MAP[key]
    compact = key.replace(" ", "")
    if compact in _UNIT_MAP:
        return _UNIT_MAP[compact]
    return key


def _operator_for_anchor(anchor: str) -> str:
    normalised = re.sub(r"\s+", " ", anchor.strip().lower())
    if re.match(_MIN_ANCHORS, normalised, re.IGNORECASE):
        return ">="
    if re.match(_MAX_ANCHORS, normalised, re.IGNORECASE):
        return "<="
    return "=="


def _clean_entity(raw: str) -> str:
    tokens = [t for t in raw.strip().split() if t]
    while tokens and tokens[0].lower() in _NOISE_ENTITY_TOKENS:
        tokens.pop(0)
    while tokens and tokens[-1].lower() in _NOISE_ENTITY_TOKENS:
        tokens.pop()
    return " ".join(tokens)


def extract_parameters(text: str) -> list[Parameter]:
    """Regex-scan `text` for parametric constraints and return Parameter records.

    Multiple matches return in document order. No match → empty list.
    """
    seen: set[tuple[int, int]] = set()
    results: list[Parameter] = []

    for pattern in (_PREFIX_ANCHOR_PATTERN, _POSTFIX_ANCHOR_PATTERN):
        for match in pattern.finditer(text):
            span = match.span()
            if span in seen:
                continue
            seen.add(span)

            entity = _clean_entity(match.group("entity"))
            if not entity:
                continue

            operator = _operator_for_anchor(match.group("anchor"))
            value = float(match.group("value"))
            raw_unit = match.group("unit")
            unit = _normalise_unit(raw_unit) if raw_unit else ""

            results.append(
                Parameter(
                    entity=entity,
                    operator=operator,
                    value=value,
                    unit=unit,
                    start=span[0],
                    end=span[1],
                    evidence=match.group(0),
                )
            )

    results.sort(key=lambda p: p.start)
    return results
