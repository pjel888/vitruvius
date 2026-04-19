"""Tests for CandidateStore."""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.kg.candidate_store import CandidateStore
from vitruvius.kg.schemas import ExtractionResult, KnowledgeUnitCandidate


def _make_candidate(label: str, text: str, embedding: list[float] | None = None) -> KnowledgeUnitCandidate:
    return KnowledgeUnitCandidate(
        id=f"cand-test-{label.lower().replace(' ', '-')}",
        unit_type="concept",
        label=label,
        text=text,
        span_ids=["span-001"],
        chunk_id="chk-001",
        confidence=0.9,
        embedding=embedding,
        created_at="2026-01-01T00:00:00Z",
    )


def _make_result(candidates: list[KnowledgeUnitCandidate]) -> ExtractionResult:
    return ExtractionResult(
        unit_type="concept",
        candidates=candidates,
        chunk_id="chk-001",
        model="qwen2.5:3b",
        duration_ms=100,
    )


class TestSaveAndLoad:
    def test_roundtrip(self, tmp_path: Path) -> None:
        store = CandidateStore(base_dir=tmp_path)
        cand = _make_candidate("Permit", "A building permit is required.")
        result = _make_result([cand])
        path = store.save([result], run_id="test-run")

        assert path.exists()
        loaded = store.load(path)
        assert len(loaded) == 1
        assert loaded[0].candidates[0].label == "Permit"
        assert loaded[0].candidates[0].text == "A building permit is required."

    def test_checksum_is_stable(self, tmp_path: Path) -> None:
        store = CandidateStore(base_dir=tmp_path)
        result = _make_result([_make_candidate("X", "Y")])
        path = store.save([result])
        cs1 = store.checksum(path)
        cs2 = store.checksum(path)
        assert cs1 == cs2
        assert len(cs1) == 64

    def test_multiple_results(self, tmp_path: Path) -> None:
        store = CandidateStore(base_dir=tmp_path)
        results = [
            _make_result([_make_candidate("A", "Text A")]),
            _make_result([_make_candidate("B", "Text B"), _make_candidate("C", "Text C")]),
        ]
        path = store.save(results)
        loaded = store.load(path)
        assert len(loaded) == 2
        assert len(loaded[1].candidates) == 2


class TestDedupeByEmbedding:
    def test_removes_exact_duplicates(self, tmp_path: Path) -> None:
        store = CandidateStore(base_dir=tmp_path)
        c1 = _make_candidate("A", "Text A", embedding=[1.0, 0.0, 0.0])
        c2 = _make_candidate("A", "Text A", embedding=[1.0, 0.0, 0.0])
        cands = [c1, c2]
        deduped = store.dedupe_by_embedding(cands, threshold=0.99)
        assert len(deduped) == 1

    def test_keeps_distinct_candidates(self, tmp_path: Path) -> None:
        store = CandidateStore(base_dir=tmp_path)
        c1 = _make_candidate("A", "Text A", embedding=[1.0, 0.0, 0.0])
        c2 = _make_candidate("B", "Text B", embedding=[0.0, 1.0, 0.0])
        cands = [c1, c2]
        deduped = store.dedupe_by_embedding(cands, threshold=0.99)
        assert len(deduped) == 2

    def test_preserves_no_embedding(self, tmp_path: Path) -> None:
        store = CandidateStore(base_dir=tmp_path)
        c1 = _make_candidate("A", "Text A", embedding=None)
        c2 = _make_candidate("B", "Text B", embedding=None)
        cands = [c1, c2]
        deduped = store.dedupe_by_embedding(cands, threshold=0.99)
        assert len(deduped) == 2

    def test_threshold_boundary(self, tmp_path: Path) -> None:
        store = CandidateStore(base_dir=tmp_path)
        c1 = _make_candidate("A", "Text A", embedding=[1.0, 0.0, 0.0])
        c2 = _make_candidate("B", "Text B", embedding=[0.95, 0.31, 0.0])  # cos_sim ≈ 0.95
        cands = [c1, c2]
        deduped_high = store.dedupe_by_embedding(cands, threshold=0.99)
        deduped_low = store.dedupe_by_embedding(cands, threshold=0.90)
        assert len(deduped_high) == 2
        assert len(deduped_low) == 1
