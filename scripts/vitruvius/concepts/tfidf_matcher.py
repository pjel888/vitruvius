"""Stream D.1 — TF-IDF concept matcher.

Matches unenriched concept slugs (e.g. ``exit-width``) to the most statistically
relevant sections of the refined PD 1096 markdown. Uses an n-gram TF-IDF
vectorizer over section bodies and ranks sections by cosine-like score.

Emits JSON candidates for human review — never auto-enriches.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer

from ..features import Features


_SECTION_SNIPPET_LEN = 200
# Legal-boilerplate extension to sklearn's ENGLISH_STOP_WORDS. These tokens
# appear in nearly every section and carry no discriminative power for
# concept matching.
_LEGAL_STOPWORDS = frozenset({"shall", "provided", "section", "pursuant"})
_STOPWORDS = ENGLISH_STOP_WORDS | _LEGAL_STOPWORDS
_HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
_OUTPUT_FILENAME = "latest_tfidf_concept_match.json"
_FLAG_NAME = "d_tfidf_concepts"


@dataclass(frozen=True)
class ConceptCandidate:
    """One (concept, section) candidate with its TF-IDF score."""

    concept_slug: str
    section_title: str
    section_body_snippet: str
    score: float
    source_path: str


@dataclass(frozen=True)
class MatchReport:
    """Result of matching a batch of concept slugs against the corpus.

    ``all_candidates`` is the full top-K browsable list for every input slug,
    regardless of threshold; ``matched`` is the subset whose score cleared
    ``threshold``. Callers that want unmatched concepts must filter
    ``all_candidates`` themselves.
    """

    threshold: float
    matched: list[ConceptCandidate]
    all_candidates: list[ConceptCandidate]


def split_into_sections(markdown: str) -> list[tuple[str, str]]:
    """Split refined markdown into (heading, body) pairs on ATX ##/### boundaries."""
    sections: list[tuple[str, str]] = []
    current_title: str | None = None
    current_body: list[str] = []
    for line in markdown.splitlines():
        match = _HEADING_RE.match(line)
        if match:
            if current_title is not None:
                sections.append((current_title, "\n".join(current_body).strip()))
            current_title = match.group(2).strip()
            current_body = []
        else:
            if current_title is not None:
                current_body.append(line)
    if current_title is not None:
        sections.append((current_title, "\n".join(current_body).strip()))
    return sections


def build_tfidf_matrix(sections: list[tuple[str, str]]):
    """Fit a ``TfidfVectorizer(ngram_range=(1,3))`` with legal-extended stopwords."""
    bodies = [body for _title, body in sections]
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words=list(_STOPWORDS))
    matrix = vectorizer.fit_transform(bodies)
    return vectorizer, matrix


def _slug_to_query(concept_slug: str) -> str:
    return " ".join(part for part in concept_slug.split("-") if part)


def _slug_informativeness(concept_slug: str) -> float:
    """Return the fraction of slug tokens that are NOT stopwords (0.0–1.0)."""
    tokens = [t.lower() for t in concept_slug.split("-") if t]
    if not tokens:
        return 0.0
    meaningful = [t for t in tokens if t not in _STOPWORDS]
    return len(meaningful) / len(tokens)


def score_concept(
    *,
    concept_slug: str,
    vectorizer,
    matrix,
    sections: list[tuple[str, str]],
    source_path: str,
    top_k: int = 3,
) -> list[ConceptCandidate]:
    """Return the top-K ConceptCandidate records for one concept slug."""
    query = _slug_to_query(concept_slug)
    query_vec = vectorizer.transform([query])
    scores_matrix = query_vec @ matrix.T
    scores = scores_matrix.toarray().ravel().tolist()
    informativeness = _slug_informativeness(concept_slug)

    candidates: list[ConceptCandidate] = []
    for (title, body), raw_score in zip(sections, scores):
        snippet = body[:_SECTION_SNIPPET_LEN]
        candidates.append(
            ConceptCandidate(
                concept_slug=concept_slug,
                section_title=title,
                section_body_snippet=snippet,
                score=float(raw_score) * informativeness,
                source_path=source_path,
            )
        )
    # Sort by score desc, stable tie-break on section_title asc.
    candidates.sort(key=lambda c: (-c.score, c.section_title))
    return candidates[:top_k]


def _candidate_to_dict(cand: ConceptCandidate) -> dict[str, Any]:
    return asdict(cand)


def _write_report(runs_dir: Path, report: MatchReport) -> None:
    payload = {
        "threshold": report.threshold,
        "matched": [_candidate_to_dict(c) for c in report.matched],
        "all_candidates": [_candidate_to_dict(c) for c in report.all_candidates],
    }
    out = runs_dir / _OUTPUT_FILENAME
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def match_concepts(
    *,
    features: Features,
    concept_slugs: list[str],
    markdown_paths: list[Path],
    threshold: float = 0.15,
    runs_dir: Path | None = None,
) -> MatchReport:
    """Score concept slugs against the TF-IDF corpus built from all markdown files.

    Returns an empty MatchReport and writes nothing when the feature flag is OFF.
    """
    if not features.is_enabled(_FLAG_NAME):
        return MatchReport(threshold=threshold, matched=[], all_candidates=[])

    # Build the unified corpus: every section from every file gets one row.
    sections: list[tuple[str, str]] = []
    section_sources: list[str] = []
    for path in markdown_paths:
        text = path.read_text()
        file_sections = split_into_sections(text)
        sections.extend(file_sections)
        section_sources.extend([str(path.name)] * len(file_sections))

    if not sections:
        report = MatchReport(threshold=threshold, matched=[], all_candidates=[])
        if runs_dir is not None:
            _write_report(runs_dir, report)
        return report

    vectorizer, matrix = build_tfidf_matrix(sections)

    all_candidates: list[ConceptCandidate] = []
    for slug in concept_slugs:
        query = _slug_to_query(slug)
        query_vec = vectorizer.transform([query])
        scores = (query_vec @ matrix.T).toarray().ravel().tolist()
        informativeness = _slug_informativeness(slug)

        per_slug: list[ConceptCandidate] = []
        for (title, body), source, raw_score in zip(sections, section_sources, scores):
            snippet = body[:_SECTION_SNIPPET_LEN]
            per_slug.append(
                ConceptCandidate(
                    concept_slug=slug,
                    section_title=title,
                    section_body_snippet=snippet,
                    score=float(raw_score) * informativeness,
                    source_path=source,
                )
            )
        per_slug.sort(key=lambda c: (-c.score, c.section_title))
        all_candidates.extend(per_slug[:3])

    # Deterministic global ordering for the report.
    all_candidates.sort(key=lambda c: (c.concept_slug, -c.score, c.section_title))
    matched = [c for c in all_candidates if c.score >= threshold]

    report = MatchReport(threshold=threshold, matched=matched, all_candidates=list(all_candidates))
    if runs_dir is not None:
        _write_report(runs_dir, report)
    return report
