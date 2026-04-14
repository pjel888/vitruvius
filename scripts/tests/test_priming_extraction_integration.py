"""Stream Y1.5 — priming identity propagation into SVO extraction candidates."""
from __future__ import annotations

import pytest

pytest.importorskip("sentence_transformers")
pytest.importorskip("spacy")

from vitruvius.extraction.spacy_dep_parser import extract_svo_triplets
from vitruvius.priming.context_vector import build_source_identity


def test_candidates_carry_source_fingerprint_when_identity_provided() -> None:
    frontmatter = {
        "title": "Test Law",
        "jurisdiction": "PH",
        "document_type": "national_law",
        "issuing_body": "Congress",
        "issue_date": "2000-01-01",
    }
    identity = build_source_identity(
        frontmatter,
        text_preview="Setbacks must be at least 3m.",
    )
    candidates = extract_svo_triplets(
        "The Code requires a building permit.",
        source_identity=identity,
    )
    assert len(candidates) >= 1
    assert all(
        c.source_identity_fingerprint == identity.fingerprint for c in candidates
    )


def test_candidates_have_none_fingerprint_when_identity_omitted() -> None:
    candidates = extract_svo_triplets("The Code requires a building permit.")
    assert all(c.source_identity_fingerprint is None for c in candidates)
