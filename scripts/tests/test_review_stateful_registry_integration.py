"""Stream Y4.2 + Y4.4 — stateful registry wired into ollama_review."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch


def test_cache_miss_calls_llm(monkeypatch, tmp_path: Path) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_stateful_registry": True})

    db = tmp_path / "reg.sqlite"
    with patch(
        "vitruvius.ollama_review._call_llm",
        return_value={"verdict": "keep", "self_confidence": 0.9},
    ) as mock_llm:
        out = orv.review_with_cache(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            source_hash="src1",
            relationship_hash="rel1",
            model_version="m:v1",
            db_path=db,
        )
    assert out["verdict"] == "keep"
    assert out["cache_hit"] is False
    assert mock_llm.call_count == 1


def test_cache_hit_skips_llm(monkeypatch, tmp_path: Path) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_stateful_registry": True})

    db = tmp_path / "reg.sqlite"
    with patch(
        "vitruvius.ollama_review._call_llm",
        return_value={"verdict": "keep", "self_confidence": 0.9},
    ) as mock_llm:
        # First call populates cache
        orv.review_with_cache(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            source_hash="src1", relationship_hash="rel1", model_version="m:v1",
            db_path=db,
        )
        # Second call should hit cache and not re-invoke
        out = orv.review_with_cache(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            source_hash="src1", relationship_hash="rel1", model_version="m:v1",
            db_path=db,
        )
    assert out["verdict"] == "keep"
    assert out["cache_hit"] is True
    assert mock_llm.call_count == 1


def test_flag_off_skips_cache_entirely(monkeypatch, tmp_path: Path) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_stateful_registry": False})

    db = tmp_path / "reg.sqlite"
    with patch(
        "vitruvius.ollama_review._call_llm",
        return_value={"verdict": "keep", "self_confidence": 0.9},
    ) as mock_llm:
        orv.review_with_cache(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            source_hash="src1", relationship_hash="rel1", model_version="m:v1",
            db_path=db,
        )
        orv.review_with_cache(
            candidate={"subject": "x", "predicate": "p", "object": "o"},
            source_hash="src1", relationship_hash="rel1", model_version="m:v1",
            db_path=db,
        )
    assert mock_llm.call_count == 2  # no cache → called twice
    assert not db.exists()  # cache file never created when flag is off


def test_resume_after_crash_skips_completed_candidates(
    monkeypatch, tmp_path: Path
) -> None:
    """Stream Y4.4 — Phase 6A Resume gap regression lock.

    Simulate: run review on 3 candidates, crash after 2, resume — only the
    3rd should invoke the LLM on the resumed run.
    """
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_stateful_registry": True})

    db = tmp_path / "reg.sqlite"
    candidates = [
        ({"subject": "a", "predicate": "p", "object": "o"}, "rel1"),
        ({"subject": "b", "predicate": "p", "object": "o"}, "rel2"),
        ({"subject": "c", "predicate": "p", "object": "o"}, "rel3"),
    ]

    # First run: succeed on 2 of 3 (simulate crash between)
    with patch(
        "vitruvius.ollama_review._call_llm",
        return_value={"verdict": "keep", "self_confidence": 0.9},
    ) as mock:
        for cand, rh in candidates[:2]:
            orv.review_with_cache(
                candidate=cand,
                source_hash="src1",
                relationship_hash=rh,
                model_version="m:v1",
                db_path=db,
            )
        assert mock.call_count == 2

    # Resume: run all 3 — only rel3 should be invoked
    with patch(
        "vitruvius.ollama_review._call_llm",
        return_value={"verdict": "keep", "self_confidence": 0.9},
    ) as mock:
        for cand, rh in candidates:
            orv.review_with_cache(
                candidate=cand,
                source_hash="src1",
                relationship_hash=rh,
                model_version="m:v1",
                db_path=db,
            )
        assert mock.call_count == 1  # only rel3 was new
