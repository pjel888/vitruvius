"""Deterministic definition extractor (Phase 3C Task 1).

Scans canonical source bodies for definition anchors like "X shall mean Y"
or "X is defined as Y", and emits DefinitionCandidate records for concepts
present in a known set. Zero LLM calls — pure regex pattern matching.

The confidence ladder reflects anchor strength:
- "shall mean" / "is defined as"     -> 0.95
- "means"                             -> 0.90
- "refers to"                         -> 0.85
- "<Term> is the"                     -> 0.70 (weakest)
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class DefinitionCandidate:
    concept_slug: str      # e.g., "occupancy-classification"
    source_id: str         # e.g., "law-pd-1096"
    source_section_id: str # e.g., "sec-701" — "" if no section context
    snippet: str           # verbatim sentence containing the anchor
    anchor: str            # the anchor phrase that matched
    confidence: float      # 0.0-1.0 per the ladder above


# Anchor patterns — ordered from strongest to weakest.
_ANCHORS: list[tuple[str, float]] = [
    ("shall mean", 0.95),
    ("is defined as", 0.95),
    ("means", 0.90),
    ("refers to", 0.85),
    ("is the", 0.70),
]


def _build_anchor_pattern(anchor: str) -> re.Pattern:
    """Build a regex that matches '<concept-phrase> <anchor>...'."""
    return re.compile(
        rf"\b([A-Z][A-Za-z\-\s]{{2,80}}?)\s+{re.escape(anchor)}\b",
        re.IGNORECASE,
    )


def _normalize_phrase(phrase: str) -> str:
    phrase = phrase.strip().lower()
    # Strip hyphens, underscores, and punctuation so aliases like
    # "exits and occupant" match normalized titles like
    # "stairs, exits, and occupant loads".
    phrase = re.sub(r"[\-_]+", " ", phrase)
    phrase = re.sub(r"[,;:.\"'()]", "", phrase)
    phrase = re.sub(r"\s+", " ", phrase)
    return phrase.strip()


def _slug_from_phrase(phrase: str) -> str:
    normalized = _normalize_phrase(phrase)
    return normalized.replace(" ", "-")


def _snippet_around(text: str, start: int, end: int, radius: int = 150) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    snippet = text[left:right].strip()
    snippet = re.sub(r"\s+", " ", snippet)
    return snippet


def _detect_section_id(text: str, match_pos: int) -> str:
    """Walk backwards from match_pos looking for the nearest Section header."""
    window = text[max(0, match_pos - 2000):match_pos]
    matches = list(re.finditer(
        r"\b(?:SECTION|SEC\.?)\s+(\d+[A-Z]?)",
        window,
        re.IGNORECASE,
    ))
    if not matches:
        return ""
    last = matches[-1]
    return f"sec-{last.group(1).lower()}"


def extract_definitions_from_text(
    text: str,
    *,
    source_id: str,
    known_slugs: set[str],
) -> list[DefinitionCandidate]:
    """Scan text for definition anchors. Returns candidates whose left-hand
    phrase slugifies to a known concept slug (exact or suffix match).
    """
    candidates: list[DefinitionCandidate] = []

    for anchor, confidence in _ANCHORS:
        pattern = _build_anchor_pattern(anchor)
        for match in pattern.finditer(text):
            phrase = match.group(1)
            slug_candidate = _slug_from_phrase(phrase)
            matched_slug = None
            if slug_candidate in known_slugs:
                matched_slug = slug_candidate
            else:
                for known in known_slugs:
                    if slug_candidate.endswith(known):
                        matched_slug = known
                        break
            if not matched_slug:
                continue

            section_id = _detect_section_id(text, match.start())
            snippet = _snippet_around(text, match.start(), match.end())
            candidates.append(DefinitionCandidate(
                concept_slug=matched_slug,
                source_id=source_id,
                source_section_id=section_id,
                snippet=snippet,
                anchor=anchor,
                confidence=confidence,
            ))

    return candidates


def pick_best_definition(
    candidates: list[DefinitionCandidate],
) -> DefinitionCandidate | None:
    """Return the highest-confidence candidate. Ties broken by earliest
    section_id, then by shortest snippet (cleaner evidence).
    """
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda c: (-c.confidence, c.source_section_id or "zzz", len(c.snippet)),
    )


# --------------------------------------------------
# SECTION-TITLE-BASED EXTRACTION (fallback when anchors miss)
# --------------------------------------------------

_SECTION_HEADER = re.compile(
    r"(?:^|\n)#{0,6}\s*(?:SECTION|SEC\.?)\s+(\d+[A-Z]?)\s*[-—\.]\s*([^\n]+)",
    re.IGNORECASE,
)


# Section-title alias dictionary: slug -> list of alternate phrasings that
# can appear in a real section title. Each alternate is matched as a
# substring of the normalized (lowercase, dehyphenated) title.
#
# Add new entries when a real PD 1096 section title uses a phrasing that
# the naive slug match misses. This is deliberately conservative — overly
# broad aliases produce false matches. Every entry below is grounded in a
# real SECTION title seen in the refined PD 1096 text.
SECTION_TITLE_ALIASES: dict[str, list[str]] = {
    "building-height": [
        "maximum height of buildings",
        "building height",
        "height of buildings",
        "height regulations",
    ],
    "lot-occupancy": [
        "lot occupancy",
        "site occupancy",
        "percentage of site occupancy",
        "measurement of site occupancy",
    ],
    "fire-resistive-construction": [
        "fire-resistive construction",
        "fire-resistive regulations",
        "fire resistive",
        "type of construction",
    ],
    "open-courts": [
        "open courts",
        "size and dimensions of courts",
        "dimensions of courts",
    ],
    "projections-over-public-ways": [
        "projections over public ways",
        "projection of balconies",
        "projection of appendages",
        "projection over streets",
    ],
    "occupancy-load": [
        "occupancy load",
        "occupant load",
        "occupant loads",
    ],
    "means-of-egress": [
        "means of egress",
        "egress",
        # Sec 1207 "Stairs, Exits, and Occupant Loads" also covers egress.
        # With multi-concept section matching, stairs/doors-and-exits/
        # occupancy-load/means-of-egress all legitimately claim this section.
        "exits and occupant",
    ],
    "yards": [
        "yards",
    ],
    "doors-and-exits": [
        "doors and exits",
        "doors",
        "exits",
    ],
    "exit-width": [
        "exit width",
        "width of exits",
    ],
    "parking-and-loading-spaces": [
        "parking and loading spaces",
        "parking",
        "loading spaces",
    ],
    "setbacks": [
        "setbacks",
        "required setbacks",
        "setback requirements",
    ],
    "occupancy-separation": [
        "occupancy separation",
        "separation of occupancies",
        # Sec 703 "Mixed Occupancy" body describes occupancy separation
        # rules ("building shall be subject to the most restrictive
        # requirement"). mixed-occupancy and occupancy-separation both
        # legitimately claim sec-703 via multi-concept matching.
        "mixed occupancy",
    ],
    "occupancy-classification": [
        "occupancy classification",
        "occupancy classified",
        "classification of occupancy",
    ],
}


def _section_title_to_concepts(title: str, known_slugs: set[str]) -> list[tuple[str, float]]:
    """Match a section title to a LIST of known concept slugs.

    A single section title like "Stairs, Exits, and Occupant Loads"
    legitimately covers multiple concepts (stairs, doors-and-exits,
    occupancy-load). Returning only the first match drops the others.

    Match passes (all passes run; duplicates deduped):
    1. Exact slug match of the entire title          -> 0.85
    2. Title contains any known concept phrase verbatim -> 0.75
    3. Title contains an alias from SECTION_TITLE_ALIASES -> 0.75
    """
    normalized = _normalize_phrase(title)
    title_slug = normalized.replace(" ", "-")

    found: dict[str, float] = {}

    # 1. Exact slug match — highest confidence
    if title_slug in known_slugs:
        found[title_slug] = 0.85

    # 2. Containing phrase match — each slug that appears in the title
    for known in known_slugs:
        if known in found:
            continue
        concept_phrase = known.replace("-", " ")
        if concept_phrase in normalized:
            found[known] = 0.75

    # 3. Alias dictionary match — each alias-matched slug
    for slug, aliases in SECTION_TITLE_ALIASES.items():
        if slug not in known_slugs or slug in found:
            continue
        for alias in aliases:
            if alias in normalized:
                found[slug] = 0.75
                break

    return [(slug, conf) for slug, conf in found.items()]


def _section_title_to_concept(title: str, known_slugs: set[str]) -> tuple[str | None, float]:
    """Back-compat wrapper returning the first match only. New callers
    should use `_section_title_to_concepts`.
    """
    matches = _section_title_to_concepts(title, known_slugs)
    if not matches:
        return None, 0.0
    return matches[0]


def extract_definitions_from_sections(
    text: str,
    *,
    source_id: str,
    known_slugs: set[str],
    max_snippet_chars: int = 500,
) -> list[DefinitionCandidate]:
    """Extract definitions by matching section titles against known concepts.

    Walks the text for `SECTION NNN — Title` headers. For each header, if
    the title normalizes to or contains a known concept slug, claims the
    section body (up to max_snippet_chars) as the definition.

    Complements `extract_definitions_from_text` for corpora (like PD 1096)
    that structure definitions section-by-section rather than with explicit
    "shall mean" anchors.
    """
    matches = list(_SECTION_HEADER.finditer(text))
    if not matches:
        return []

    candidates: list[DefinitionCandidate] = []
    for i, match in enumerate(matches):
        section_num = match.group(1).lower()
        title = match.group(2).strip()

        # One section title may cover multiple concepts — emit a candidate
        # for each. This is essential for compound titles like
        # "Stairs, Exits, and Occupant Loads" which legitimately cover
        # stairs + doors-and-exits + occupancy-load.
        slug_matches = _section_title_to_concepts(title, known_slugs)
        if not slug_matches:
            continue

        body_start = match.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else min(len(text), body_start + max_snippet_chars * 4)
        body = text[body_start:body_end].strip()
        body = re.sub(r"\s+", " ", body)
        snippet = body[:max_snippet_chars]

        for slug, confidence in slug_matches:
            candidates.append(DefinitionCandidate(
                concept_slug=slug,
                source_id=source_id,
                source_section_id=f"sec-{section_num}",
                snippet=snippet,
                anchor=f"section_title: {title}",
                confidence=confidence,
            ))

    return candidates
