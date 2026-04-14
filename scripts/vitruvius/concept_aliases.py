"""Deterministic alias miner (Phase 3C Task 2).

Mines alternate names for a concept from a source text using two patterns:
- Parenthetical abbreviations: "National Building Code (NBC)"
- Explicit "also known as" / "also called" / "or" phrases

Zero LLM calls. Pure regex.
"""

from __future__ import annotations

import re


_MAX_ALIASES = 5
_MIN_ALIAS_LEN = 2

_STOPWORDS = {
    "the", "and", "or", "of", "a", "an", "this", "that", "it",
    "code", "act", "law", "section", "chapter", "article", "part",
}


def _normalize(phrase: str) -> str:
    phrase = phrase.strip().lower()
    phrase = re.sub(r"[.,;:\"']", "", phrase)
    phrase = re.sub(r"\s+", " ", phrase)
    return phrase.strip()


def _is_meaningful(alias: str) -> bool:
    if len(alias) < _MIN_ALIAS_LEN:
        return False
    if alias in _STOPWORDS:
        return False
    if alias.isdigit():
        return False
    if re.match(r"^[a-z]$", alias):
        return False
    return True


# Parenthetical abbreviation pattern:
# A multi-word phrase (including optional lowercase connectors like "of",
# "and", "the") ending in a Title-Cased word, followed by a parenthesized
# abbreviation. Examples matched:
#   "National Building Code (NBC)"
#   "Department of Public Works and Highways (DPWH)"
#   "Fire Code of the Philippines (F.C.P.)"
_PAREN_ABBREV = re.compile(
    r"((?:\b[A-Z][A-Za-z\-]{1,}|\b(?:of|and|the|for|in|on|to|&))(?:\s+(?:[A-Z][A-Za-z\-]{1,}|of|and|the|for|in|on|to|&)){1,7})\s*\(\s*([A-Z][A-Za-z0-9.\-]{1,10}?)\.?\s*\)",
)

# Leading words to strip from long-form matches so "The National Building
# Code" normalizes to "national building code" when the test expects it.
_LEADING_STRIP = {"the", "a", "an"}


def parenthetical_abbreviations(text: str) -> list[tuple[str, str]]:
    """Return deduplicated (long_form, abbreviation) pairs.

    Long forms have leading articles ('the', 'a', 'an') stripped and are
    lowercased. Abbreviations have dots stripped and are lowercased.
    """
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str]] = []
    for match in _PAREN_ABBREV.finditer(text):
        long_form = _normalize(match.group(1))
        # Strip leading articles
        long_words = long_form.split()
        while long_words and long_words[0] in _LEADING_STRIP:
            long_words = long_words[1:]
        long_form = " ".join(long_words)

        abbrev = _normalize(match.group(2))
        if not _is_meaningful(abbrev):
            continue
        if not _is_meaningful(long_form):
            continue
        key = (long_form, abbrev)
        if key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


_ALSO_KNOWN_AS = re.compile(
    r"(?:also known as|also called|also referred to as)\s+([a-zA-Z][a-zA-Z\s\-]{2,60}?)(?:[.,;]|\s+(?:and|or|which|that|is)|\s*$)",
    re.IGNORECASE,
)


def _also_known_as_phrases(text: str) -> list[str]:
    out: list[str] = []
    for match in _ALSO_KNOWN_AS.finditer(text):
        phrase = _normalize(match.group(1))
        if _is_meaningful(phrase):
            out.append(phrase)
    return out


def mine_aliases_for_concept(
    text: str,
    *,
    concept_title: str,
) -> list[str]:
    """Return a deduplicated, cap-5 list of alias strings for the concept."""
    if not text:
        return []

    concept_normalized = _normalize(concept_title)
    out: list[str] = []
    seen: set[str] = set()

    def _add(alias: str) -> None:
        if not _is_meaningful(alias):
            return
        if alias == concept_normalized:
            return
        if alias in seen:
            return
        seen.add(alias)
        out.append(alias)

    # Pattern 1: parenthetical abbreviations whose long form overlaps the concept title.
    for long_form, abbrev in parenthetical_abbreviations(text):
        if concept_normalized in long_form or long_form in concept_normalized:
            _add(abbrev)

    # Pattern 2: also-known-as phrases (not concept-gated).
    for phrase in _also_known_as_phrases(text):
        _add(phrase)

    return out[:_MAX_ALIASES]
