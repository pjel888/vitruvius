"""Stream Y1.4 — priming identity flows into the ontology prompt builder."""
from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("sentence_transformers")

from vitruvius.priming.context_vector import SourceIdentity
from vitruvius.review.ontology_prompt_builder import (
    GraphEdgeSummary,
    build_neighborhood_prompt,
)


def _edges() -> list[GraphEdgeSummary]:
    return [
        GraphEdgeSummary(from_id="building", to_id="setback", predicate="has_setback"),
    ]


def _fake_identity() -> SourceIdentity:
    return SourceIdentity(
        fingerprint="abc123",
        prose="This is PD 1096, a national law under the jurisdiction of PH.",
        vector=np.zeros(384, dtype=np.float32),
    )


def test_prompt_omits_identity_when_none_passed() -> None:
    out = build_neighborhood_prompt(
        candidate_subject="building",
        candidate_object="setback",
        edges=_edges(),
    )
    assert "SOURCE_IDENTITY" not in out.rendered_text


def test_prompt_prepends_identity_prefix_when_passed() -> None:
    out = build_neighborhood_prompt(
        candidate_subject="building",
        candidate_object="setback",
        edges=_edges(),
        source_identity=_fake_identity(),
    )
    assert "SOURCE_IDENTITY[abc123]" in out.rendered_text
    assert "PD 1096" in out.rendered_text
    # The existing neighborhood sections must still be rendered below.
    assert "Subject neighborhood" in out.rendered_text


def test_prompt_without_identity_is_byte_identical_to_legacy() -> None:
    """Flag-OFF (source_identity=None) must produce the exact same
    rendered_text as the pre-Y1.4 call path."""
    baseline = build_neighborhood_prompt(
        candidate_subject="building",
        candidate_object="setback",
        edges=_edges(),
    )
    with_none = build_neighborhood_prompt(
        candidate_subject="building",
        candidate_object="setback",
        edges=_edges(),
        source_identity=None,
    )
    assert baseline.rendered_text == with_none.rendered_text
