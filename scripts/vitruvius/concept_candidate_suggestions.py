from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

from .concept_matching import load_concept_term_map, normalize_match_text

_QUOTED_MEANS_RE = re.compile(r'"(?P<term>[^"]{2,120}?)"\s+means\b', re.IGNORECASE)
_BULLET_ENUM_RE = r'(?:\([a-z]{1,3}\)|[a-z]{1,3}\))\s*'
_BULLET_QUOTED_MEANS_RE = re.compile(rf'^\s*[-*]\s*(?:{_BULLET_ENUM_RE})?"(?P<term>[^"]{{2,120}}?)"\s+means\b', re.IGNORECASE)
_BARE_MEANS_RE = re.compile(rf'^\s*[-*]?\s*(?:{_BULLET_ENUM_RE})?(?P<term>[A-Z][A-Za-z0-9/\- ]{{2,120}}?)\s+means\b', re.IGNORECASE)
_DEFINED_AS_RE = re.compile(rf'^\s*[-*]?\s*(?:{_BULLET_ENUM_RE})?(?P<term>[A-Z][A-Za-z0-9/\- ]{{2,120}}?)\s+(?:are|is)\s+(?:hereby\s+)?defined\s+as\b', re.IGNORECASE)

_STOP_TERMS = {
    'section', 'title', 'scope', 'declaration of policy', 'definition of terms', 'definition',
    'any and all',
}


def _normalize_candidate_term(term: str) -> str | None:
    cleaned = re.sub(r'\s+', ' ', term.replace('“', '"').replace('”', '"')).strip(' .;,:-"')
    if not cleaned:
        return None
    lowered = cleaned.lower()
    if lowered in _STOP_TERMS:
        return None
    if len(cleaned) < 3:
        return None
    return cleaned


def extract_definition_style_terms(text: str) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        for pattern in (_BULLET_QUOTED_MEANS_RE, _QUOTED_MEANS_RE, _DEFINED_AS_RE, _BARE_MEANS_RE):
            match = pattern.search(line)
            if match is None:
                continue
            candidate = _normalize_candidate_term(match.group('term'))
            if candidate is None:
                continue
            key = candidate.lower()
            if key in seen:
                continue
            seen.add(key)
            candidates.append(candidate)
            break
    return candidates


def suggest_concept_candidates(*, repo_root: Path, refined_markdown_path: str, top_n: int = 25) -> dict[str, object]:
    refined_path = repo_root / '002_Raw-Conversion-Layer' / refined_markdown_path
    text = refined_path.read_text(encoding='utf-8')
    concepts_dir = repo_root / '003_Canonical-Knowledge-Layer' / 'shared' / 'concepts'
    concept_map = load_concept_term_map(concepts_dir)
    raw_candidates = extract_definition_style_terms(text)

    matched_existing: list[dict[str, str]] = []
    unmatched_candidates: list[dict[str, str]] = []
    for term in raw_candidates:
        normalized = normalize_match_text(term)
        concept_id = concept_map.get(normalized)
        record = {
            'term': term,
            'normalized_term': normalized,
        }
        if concept_id:
            matched_existing.append({**record, 'concept_id': concept_id})
        else:
            unmatched_candidates.append({
                **record,
                'suggested_concept_id': f"concept-{normalized.replace(' ', '-')}",
            })

    return {
        'action': 'suggest-concept-candidates-from-refined',
        'refined_markdown_path': refined_markdown_path,
        'candidate_count': len(raw_candidates),
        'matched_existing_count': len(matched_existing),
        'unmatched_candidate_count': len(unmatched_candidates),
        'matched_existing': matched_existing[:top_n],
        'unmatched_candidates': unmatched_candidates[:top_n],
    }


def run_suggest_concept_candidates(*, refined_markdown_path: str, top_n: int = 25) -> int:
    payload = suggest_concept_candidates(repo_root=Path.cwd().resolve(), refined_markdown_path=refined_markdown_path, top_n=top_n)
    print(json.dumps(payload, indent=2))
    return 0
