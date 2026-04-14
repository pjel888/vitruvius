"""Tier C — destructive, audited, feature-flag gated normalization rules.

Tier C rules mutate text in ways that cannot be bit-exactly reversed (they
replace OCR typos, rewrite units, etc.). Every change is logged to an audit
list so operators can trace the mutation chain back through the pipeline.

This module ships the first Tier C rule: Jaro-Winkler OCR typo correction.
It is wired OFF by default and gated on ``features.c_tier_c_ocr_fix``. With
the flag off the rule is a byte-identical passthrough.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import yaml
from rapidfuzz.distance import JaroWinkler

from ..features import Features


RULE_NAME = "jaro_winkler_ocr_fix"
FEATURE_FLAG = "c_tier_c_ocr_fix"

DEFAULT_MIN_SIMILARITY = 0.92
DEFAULT_MIN_TOKEN_LENGTH = 4
DEFAULT_STOPWORDS = frozenset(
    {
        "the", "and", "for", "not", "shall", "must", "is", "are", "be",
        "in", "on", "of", "to", "a", "an", "as", "at", "by", "or",
        "with", "from", "this", "that", "it", "its", "such",
    }
)

_TOKEN_PATTERN = re.compile(r"\b[\w'-]+\b", re.UNICODE)
_FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)


def _expand_vocabulary_tokens(vocabulary: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    tokens: list[str] = []
    for phrase in vocabulary:
        for token in _TOKEN_PATTERN.findall(phrase):
            key = token.lower()
            if key in seen:
                continue
            seen.add(key)
            tokens.append(token)
    return tokens


def _best_match(
    token_lower: str,
    canonical_tokens: list[str],
    min_similarity: float,
) -> tuple[str, float] | None:
    best_token: str | None = None
    best_score = 0.0
    for canonical in canonical_tokens:
        canonical_lower = canonical.lower()
        if canonical_lower == token_lower:
            return canonical, 1.0
        score = JaroWinkler.normalized_similarity(token_lower, canonical_lower)
        if score > best_score:
            best_score = score
            best_token = canonical
    if best_token is None or best_score < min_similarity:
        return None
    return best_token, best_score


def correct_ocr_typos(
    text: str,
    *,
    features: Features,
    vocabulary: Iterable[str],
    min_similarity: float = DEFAULT_MIN_SIMILARITY,
    min_token_length: int = DEFAULT_MIN_TOKEN_LENGTH,
    stopwords: frozenset[str] = DEFAULT_STOPWORDS,
) -> tuple[str, list[dict]]:
    """Scan text and replace OCR-garbled tokens near a canonical concept."""
    if not features.is_enabled(FEATURE_FLAG):
        return text, []

    canonical_tokens = _expand_vocabulary_tokens(vocabulary)
    if not canonical_tokens:
        return text, []

    canonical_lookup = {tok.lower() for tok in canonical_tokens}

    audit: list[dict] = []
    out_parts: list[str] = []
    cursor = 0

    for match in _TOKEN_PATTERN.finditer(text):
        start, end = match.span()
        out_parts.append(text[cursor:start])
        cursor = end

        token = match.group(0)
        token_lower = token.lower()

        if len(token) < min_token_length:
            out_parts.append(token)
            continue
        if token_lower in stopwords:
            out_parts.append(token)
            continue
        if token_lower in canonical_lookup:
            out_parts.append(token)
            continue

        result = _best_match(token_lower, canonical_tokens, min_similarity)
        if result is None:
            out_parts.append(token)
            continue

        replacement, score = result
        out_parts.append(replacement)
        audit.append(
            {
                "rule": RULE_NAME,
                "original": token,
                "replaced": replacement,
                "similarity": float(score),
                "position": start,
            }
        )

    out_parts.append(text[cursor:])
    return "".join(out_parts), audit


def build_vocabulary_from_concepts(concepts_dir: Path) -> list[str]:
    """Read the YAML frontmatter ``title`` from every .md in concepts_dir."""
    titles: set[str] = set()
    for md_path in sorted(concepts_dir.glob("*.md")):
        raw = md_path.read_text(encoding="utf-8")
        fm_match = _FRONTMATTER_PATTERN.match(raw)
        if fm_match is None:
            continue
        try:
            meta = yaml.safe_load(fm_match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(meta, dict):
            continue
        title = meta.get("title")
        if isinstance(title, str) and title.strip():
            titles.add(title.strip())
    return sorted(titles)
