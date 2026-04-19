"""Tests for ExtractionEngine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.extraction_engine import ExtractionEngine
from vitruvius.kg.schemas import Chunk, ExtractionResult, KnowledgeUnitCandidate


class FakeLLMClient:
    """In-memory stand-in for StructuredLLMClient."""

    def __init__(self, responses: list[Any] | None = None) -> None:
        self.responses = responses or []
        self.call_index = 0
        self.calls: list[tuple[str, type]] = []
        self.ollama_model = "fake-model"

    def extract(self, prompt: str, model_cls: type, **kwargs: Any) -> Any:
        self.calls.append((prompt, model_cls))
        # Return responses round-robin, or empty default
        if self.call_index < len(self.responses):
            resp = self.responses[self.call_index]
            self.call_index += 1
            return resp
        return self._default_response()

    @staticmethod
    def _default_response():
        class FakeResponse:
            candidates = []
        return FakeResponse()


def _make_chunk(text: str, chunk_id: str = "chk-test-001") -> Chunk:
    return Chunk(
        id=chunk_id,
        section_id="sec-test-001",
        document_version_id="docv-test-v1",
        text=text,
        char_start=0,
        char_end=len(text),
    )


class TestExtractFromChunk:
    def test_skips_short_chunks(self) -> None:
        llm = FakeLLMClient()
        engine = ExtractionEngine(llm=llm, min_chunk_chars=100)
        chunk = _make_chunk("short")
        result = engine.extract_from_chunk(chunk, "concept")
        assert result.error == "chunk_too_short"
        assert result.candidates == []
        assert len(llm.calls) == 0

    def test_extracts_concept(self) -> None:
        class FakeCandidate:
            def __init__(self, label: str, text: str, confidence: float) -> None:
                self.label = label
                self.text = text
                self.confidence = confidence

        class FakeResponse:
            candidates = [FakeCandidate("Permit", "A building permit is required.", 0.95)]

        llm = FakeLLMClient(responses=[FakeResponse()])
        engine = ExtractionEngine(llm=llm)
        chunk = _make_chunk("A building permit is required for all construction projects in the city.")
        result = engine.extract_from_chunk(chunk, "concept", run_id="run-test-001", span_ids=["span-test-001"])

        assert result.error is None
        assert len(result.candidates) == 1
        assert result.candidates[0].label == "Permit"
        assert result.candidates[0].text == "A building permit is required."
        assert result.candidates[0].unit_type == "concept"
        assert result.candidates[0].chunk_id == chunk.id
        assert 0 <= result.candidates[0].confidence <= 1.0

    def test_filters_empty_candidates(self) -> None:
        class FakeCandidate:
            def __init__(self, label: str, text: str, confidence: float = 0.0) -> None:
                self.label = label
                self.text = text
                self.confidence = confidence

        class FakeResponse:
            candidates = [
                FakeCandidate("Valid", "Has text", 0.9),
                FakeCandidate("", "Missing label", 0.5),
                FakeCandidate("NoText", "", 0.5),
            ]

        llm = FakeLLMClient(responses=[FakeResponse()])
        engine = ExtractionEngine(llm=llm)
        chunk = _make_chunk("Some chunk text here for extraction purposes with sufficient length.")
        result = engine.extract_from_chunk(chunk, "rule", run_id="run-test-002", span_ids=["span-test-002"])

        assert len(result.candidates) == 1
        assert result.candidates[0].label == "Valid"

    def test_prompt_contains_chunk_text(self) -> None:
        llm = FakeLLMClient(responses=[None])
        engine = ExtractionEngine(llm=llm)
        chunk = _make_chunk("Unique marker XYZ123 for prompt verification and sufficient length here.")
        engine.extract_from_chunk(chunk, "definition", run_id="run-test-003", span_ids=["span-test-003"])

        assert len(llm.calls) == 1
        prompt, _ = llm.calls[0]
        assert "Unique marker XYZ123" in prompt

    def test_all_unit_types_have_prompts(self) -> None:
        engine = ExtractionEngine(llm=FakeLLMClient())
        for ut in ("concept", "definition", "rule", "procedure", "exception"):
            assert ut in engine._prompts, f"Missing prompt for {ut}"


class TestExtractFromSnapshot:
    def test_empty_snapshot_returns_empty(self) -> None:
        from vitruvius.kg.json_evidence_store import KgV2Snapshot

        llm = FakeLLMClient()
        engine = ExtractionEngine(llm=llm)
        snapshot = KgV2Snapshot()
        results = engine.extract_from_snapshot(snapshot)
        assert results == []

    def test_processes_all_chunks_and_types(self) -> None:
        from vitruvius.kg.json_evidence_store import KgV2Snapshot

        llm = FakeLLMClient()
        engine = ExtractionEngine(llm=llm)
        snapshot = KgV2Snapshot()
        snapshot.chunks.append(_make_chunk("Chunk one text here with enough characters to pass the minimum threshold."))
        snapshot.chunks.append(_make_chunk("Chunk two text here with enough characters to pass the minimum threshold."))
        results = engine.extract_from_snapshot(snapshot, unit_types=["concept", "rule"])

        # 2 chunks × 2 unit types = 4 calls
        assert len(results) == 4
        assert len(llm.calls) == 4
