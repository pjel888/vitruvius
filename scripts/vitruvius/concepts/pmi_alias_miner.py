"""Stream D.2 — PMI alias miner.

For each canonical concept slug, scans a sliding window over the corpus and
ranks co-occurring unigrams by pointwise mutual information. Emits a
deterministic JSON report for human review — never auto-updates a concept
file. See .ai/09_archive/plans/statistical-architectural-upgrade-plan.md §8.3
(archived 2026-04-15).
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from ..features import Features


DEFAULT_WINDOW_SIZE = 5
DEFAULT_MIN_PMI = 3.0
DEFAULT_MIN_JOINT_COUNT = 5

_FLAG_NAME = "d_pmi_aliases"
_OUTPUT_FILENAME = "latest_pmi_alias_mining.json"
_TOKEN_RE = re.compile(r"[A-Za-z]+")

# Small English stopword set — aligned with tfidf_matcher._LEGAL_STOPWORDS
# plus the core closed-class function words that dominate regulatory prose.
_STOPWORDS: frozenset[str] = frozenset(
    {
        "a", "an", "and", "are", "as", "at", "be", "been", "being",
        "but", "by", "do", "does", "for", "from", "has", "have", "he",
        "her", "his", "how", "i", "if", "in", "into", "is", "it", "its",
        "me", "must", "my", "no", "not", "of", "on", "or", "our", "out",
        "over", "per", "provided", "pursuant", "section", "shall", "she",
        "so", "such", "than", "that", "the", "their", "them", "there",
        "these", "they", "this", "those", "to", "under", "up", "upon",
        "us", "was", "we", "were", "when", "where", "which", "who",
        "will", "with", "within", "without", "would", "you", "your",
    }
)


@dataclass(frozen=True)
class AliasCandidate:
    concept_slug: str
    candidate: str
    joint_count: int
    pmi: float


@dataclass(frozen=True)
class AliasMiningReport:
    window_size: int
    min_pmi: float
    min_joint_count: int
    candidates: tuple[AliasCandidate, ...]


def _tokenise(corpus: str) -> list[str]:
    return [tok.lower() for tok in _TOKEN_RE.findall(corpus)]


def _slug_tokens(concept_slug: str) -> list[str]:
    return [part.lower() for part in concept_slug.split("-") if part]


def _iter_windows(tokens: list[str], window_size: int) -> list[tuple[str, ...]]:
    if window_size <= 0 or len(tokens) < window_size:
        return [tuple(tokens)] if tokens else []
    return [tuple(tokens[i : i + window_size]) for i in range(0, len(tokens) - window_size + 1)]


def _mine_one_slug(
    *,
    concept_slug: str,
    windows: list[tuple[str, ...]],
    unigram_counts: Counter[str],
    unigram_total: int,
    min_pmi: float,
    min_joint_count: int,
) -> list[AliasCandidate]:
    slug_tokens_set = {t for t in _slug_tokens(concept_slug) if t}
    if not slug_tokens_set or unigram_total == 0 or not windows:
        return []

    slug_count = sum(unigram_counts[t] for t in slug_tokens_set)
    if slug_count == 0:
        return []

    # Joint count = number of windows in which (slug_token, candidate) appear
    # together, summed over all slug tokens present in the window. To stay
    # deterministic and avoid double-counting, a candidate's joint count is
    # the number of distinct windows in which ANY slug token and the
    # candidate co-occur.
    joint_counts: Counter[str] = Counter()
    for window in windows:
        window_set = set(window)
        if not (window_set & slug_tokens_set):
            continue
        for tok in window_set:
            if tok in slug_tokens_set:
                continue
            if tok in _STOPWORDS:
                continue
            joint_counts[tok] += 1

    total_windows = len(windows)
    p_x = slug_count / unigram_total
    if p_x == 0:
        return []

    candidates: list[AliasCandidate] = []
    for cand, joint in joint_counts.items():
        if joint < min_joint_count:
            continue
        cand_count = unigram_counts[cand]
        if cand_count == 0:
            continue
        p_y = cand_count / unigram_total
        p_xy = joint / total_windows
        if p_xy == 0 or p_x * p_y == 0:
            continue
        pmi = math.log2(p_xy / (p_x * p_y))
        if pmi < min_pmi:
            continue
        candidates.append(
            AliasCandidate(
                concept_slug=concept_slug,
                candidate=cand,
                joint_count=joint,
                pmi=pmi,
            )
        )
    return candidates


def _write_report(runs_dir: Path, report: AliasMiningReport) -> None:
    payload = {
        "window_size": report.window_size,
        "min_pmi": report.min_pmi,
        "min_joint_count": report.min_joint_count,
        "candidates": [asdict(c) for c in report.candidates],
    }
    out = runs_dir / _OUTPUT_FILENAME
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def mine_aliases(
    *,
    features: Features,
    concept_slugs: Sequence[str],
    corpus: str,
    window_size: int = DEFAULT_WINDOW_SIZE,
    min_pmi: float = DEFAULT_MIN_PMI,
    min_joint_count: int = DEFAULT_MIN_JOINT_COUNT,
    runs_dir: Path | None = None,
) -> AliasMiningReport:
    """Mine alias candidates for each concept via PMI over a sliding window."""
    if not features.is_enabled(_FLAG_NAME):
        return AliasMiningReport(
            window_size=window_size,
            min_pmi=min_pmi,
            min_joint_count=min_joint_count,
            candidates=(),
        )

    tokens = _tokenise(corpus)
    windows = _iter_windows(tokens, window_size)
    unigram_counts: Counter[str] = Counter(tokens)
    unigram_total = sum(unigram_counts.values())

    all_candidates: list[AliasCandidate] = []
    for slug in concept_slugs:
        all_candidates.extend(
            _mine_one_slug(
                concept_slug=slug,
                windows=windows,
                unigram_counts=unigram_counts,
                unigram_total=unigram_total,
                min_pmi=min_pmi,
                min_joint_count=min_joint_count,
            )
        )

    all_candidates.sort(key=lambda c: (c.concept_slug, -c.pmi, c.candidate))

    report = AliasMiningReport(
        window_size=window_size,
        min_pmi=min_pmi,
        min_joint_count=min_joint_count,
        candidates=tuple(all_candidates),
    )
    if runs_dir is not None:
        _write_report(runs_dir, report)
    return report
