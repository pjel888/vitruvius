"""Concept enrichment helpers — Stream D modules (TF-IDF, PMI, FCA, etc.).

Historically this was a flat ``concepts.py`` module exposing ``slugify``,
``build_id``, and ``run_canonicalize_concept_one``. Stream D.1 converts it
to a package so submodules (``tfidf_matcher``, ``pmi_aliases``, ...) can
live alongside without touching call-sites — the legacy symbols are
re-exported below so ``from vitruvius.concepts import run_canonicalize_concept_one``
continues to work byte-for-byte.
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..paths import get_repo_root
from ..utils import slugify


VALID_PREFIX = "concept"


def build_id(name: str) -> str:
    return f"{VALID_PREFIX}-{slugify(name)}"


def run_canonicalize_concept_one(*, concept_name: str) -> int:
    name = concept_name
    repo_root = get_repo_root()

    slug = slugify(name)
    target = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "concepts"
    target.mkdir(parents=True, exist_ok=True)

    file = target / f"{slug}.md"

    if file.exists():
        print(f"SKIP: Concept already exists -> {file}")
        return 0

    lines = [
        "---",
        f"id: {build_id(name)}",
        f"title: {name.title()}",
        "page_type: concept",
        "canonical_status: placeholder",
        "concept_status: placeholder",
        f"last_canonicalized_utc: {datetime.now(timezone.utc).isoformat()}",
        "---\n",
        f"# {name.title()}",
        "\n## Definition\n",
        f"{name.title()} is a defined concept within the Vitruvius system.",
    ]

    file.write_text("\n".join(lines), encoding="utf-8")

    print("canonicalize-concept-one complete.")
    print(f"Created: {file}")

    return 0


__all__ = ["VALID_PREFIX", "slugify", "build_id", "run_canonicalize_concept_one"]
