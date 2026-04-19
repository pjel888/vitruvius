"""Tests for EmbeddingClient."""

from __future__ import annotations

from typing import Any

import pytest

from vitruvius.kg.embeddings import EmbeddingClient


class TestCosineSimilarity:
    def test_identical_vectors(self) -> None:
        a = [1.0, 2.0, 3.0]
        b = [1.0, 2.0, 3.0]
        assert EmbeddingClient.cosine_similarity(a, b) == pytest.approx(1.0, abs=1e-6)

    def test_orthogonal_vectors(self) -> None:
        a = [1.0, 0.0, 0.0]
        b = [0.0, 1.0, 0.0]
        assert EmbeddingClient.cosine_similarity(a, b) == pytest.approx(0.0, abs=1e-6)

    def test_opposite_vectors(self) -> None:
        a = [1.0, 0.0, 0.0]
        b = [-1.0, 0.0, 0.0]
        assert EmbeddingClient.cosine_similarity(a, b) == pytest.approx(-1.0, abs=1e-6)

    def test_zero_vector(self) -> None:
        a = [0.0, 0.0, 0.0]
        b = [1.0, 2.0, 3.0]
        assert EmbeddingClient.cosine_similarity(a, b) == 0.0




class TestEmbedTextsFallback:
    """Mock Ollama failure and verify sentence-transformers fallback."""

    def test_empty_list(self) -> None:
        client = EmbeddingClient(fallback=True)
        assert client.embed_texts([]) == []

    def test_ollama_failure_falls_back(self, monkeypatch: Any) -> None:
        """Force Ollama to raise, then verify fallback produces vectors."""
        client = EmbeddingClient(model="nomic-embed-text", fallback=True)

        # Force Ollama to fail
        def failing_ollama(*args: Any, **kwargs: Any) -> Any:
            raise ConnectionError("Ollama down")

        monkeypatch.setattr(client, "_embed_ollama", failing_ollama)

        # Mock sentence-transformers to avoid a ~6s model load in CI.
        class FakeST:
            def encode(self, texts, **kw):
                import numpy as np
                return np.array([[0.1] * 384, [0.2] * 384], dtype=float)

        monkeypatch.setattr(client, "_st", FakeST())

        vectors = client.embed_texts(["hello world", "test sentence"])
        assert len(vectors) == 2
        assert all(isinstance(v, list) for v in vectors)
        assert all(len(v) == 384 for v in vectors)
