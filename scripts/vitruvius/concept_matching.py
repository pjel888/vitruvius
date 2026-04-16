from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable

import yaml


_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
_MULTISPACE_RE = re.compile(r"\s+")


def normalize_match_text(text: str) -> str:
    normalized = text.lower().replace("_", " ").replace("-", " ")
    normalized = _NON_ALNUM_RE.sub(" ", normalized)
    normalized = _MULTISPACE_RE.sub(" ", normalized).strip()
    return normalized


def _load_frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    try:
        payload = yaml.safe_load(text[3:end].strip())
    except yaml.YAMLError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _candidate_terms(path: Path) -> list[str]:
    terms = [path.stem.replace("-", " ")]
    frontmatter = _load_frontmatter(path)
    title = frontmatter.get("title")
    if isinstance(title, str) and title.strip():
        terms.append(title.strip())
    aliases = frontmatter.get("aliases")
    if isinstance(aliases, list):
        for alias in aliases:
            if isinstance(alias, str) and alias.strip():
                terms.append(alias.strip())
    return terms


def load_concept_term_map(
    concepts_dir: Path,
    *,
    allowed_paths: Iterable[Path] | None = None,
) -> Dict[str, str]:
    if allowed_paths is None:
        files = sorted(concepts_dir.glob("*.md"))
    else:
        files = sorted(set(Path(path) for path in allowed_paths if Path(path).is_file()))

    term_map: Dict[str, str] = {}
    for file in files:
        slug = file.stem
        concept_id = f"concept-{slug}"
        for raw_term in _candidate_terms(file):
            normalized = normalize_match_text(raw_term)
            if normalized:
                term_map[normalized] = concept_id
    return term_map


def find_concepts_in_text(text: str, concept_map: Dict[str, str]) -> list[str]:
    normalized_text = f" {normalize_match_text(text)} "
    matches: dict[str, tuple[int, int]] = {}
    for phrase, concept_id in concept_map.items():
        pattern = f" {phrase} "
        idx = normalized_text.find(pattern)
        if idx == -1:
            continue
        rank = (idx, -len(phrase))
        existing = matches.get(concept_id)
        if existing is None or rank < existing:
            matches[concept_id] = rank
    return [concept_id for concept_id, _ in sorted(matches.items(), key=lambda item: item[1])]
