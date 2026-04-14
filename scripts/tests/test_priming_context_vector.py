"""Stream Y1.1 — deterministic source-identity vector builder tests."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

# The sentence_transformers model load is a real network-free op once the
# all-MiniLM-L6-v2 weights are cached — roughly 22 MB on disk. If the
# package isn't installed we skip the whole module cleanly.
pytest.importorskip("sentence_transformers")

from vitruvius.priming.context_vector import (
    SourceIdentity,
    build_source_identity,
    identity_to_prose,
)


def test_identity_is_deterministic_for_identical_frontmatter() -> None:
    fm = {
        "title": "PD 1096 - National Building Code",
        "jurisdiction": "PH",
        "document_type": "national_law",
        "issuing_body": "Congress of the Philippines",
        "issue_date": "1977-02-19",
    }
    ident_a = build_source_identity(fm, text_preview="Section 1. Title.")
    ident_b = build_source_identity(fm, text_preview="Section 1. Title.")
    assert ident_a.fingerprint == ident_b.fingerprint
    assert np.allclose(ident_a.vector, ident_b.vector)


def test_identity_prose_is_stable_plain_english() -> None:
    fm = {
        "title": "PD 1096 - National Building Code",
        "jurisdiction": "PH",
        "document_type": "national_law",
        "issuing_body": "Congress",
        "issue_date": "1977-02-19",
    }
    ident = build_source_identity(fm, text_preview="Section 1.")
    prose = identity_to_prose(ident)
    assert "PD 1096" in prose
    assert "national law" in prose.lower() or "national_law" in prose
    assert "PH" in prose or "Philippines" in prose


def test_vector_dimension_matches_config() -> None:
    fm = {
        "title": "x",
        "jurisdiction": "PH",
        "document_type": "national_law",
        "issuing_body": "y",
        "issue_date": "1970-01-01",
    }
    ident = build_source_identity(fm, text_preview="hello")
    assert ident.vector.shape == (384,)
    assert ident.vector.dtype == np.float32


def test_fingerprint_changes_when_jurisdiction_changes() -> None:
    fm_ph = {
        "title": "X",
        "jurisdiction": "PH",
        "document_type": "law",
        "issuing_body": "Y",
        "issue_date": "2000-01-01",
    }
    fm_us = dict(fm_ph, jurisdiction="US")
    a = build_source_identity(fm_ph, text_preview="same text")
    b = build_source_identity(fm_us, text_preview="same text")
    assert a.fingerprint != b.fingerprint
