"""Sprint 1B-M2 Task 3 — Golden Corpus benchmark tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.bench.golden_corpus import (
    GoldenCorpusResult,
    run_golden_corpus_benchmark,
)


def test_golden_corpus_runs_with_stub_parsers(tmp_path: Path) -> None:
    """Exercises the harness end-to-end with stub parsers and synthetic
    fixtures. Asserts the shape of the result, not specific numbers.
    """
    result = run_golden_corpus_benchmark(work_dir=tmp_path)
    assert isinstance(result, GoldenCorpusResult)
    assert result.total_documents >= 3
    assert result.successful_documents <= result.total_documents
    assert result.total_duration_ms >= 0
    assert isinstance(result.per_class_results, dict)
    assert len(result.per_class_results) >= 1


def test_golden_corpus_gate_pass_rate(tmp_path: Path) -> None:
    """With the default stub parser configuration, the harness
    should produce a 100% gate pass rate — the stub always emits
    markdown that clears GATE-001 through GATE-004.
    """
    result = run_golden_corpus_benchmark(work_dir=tmp_path)
    assert result.gate_pass_rate == pytest.approx(1.0, abs=0.01)
