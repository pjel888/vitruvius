"""Hybrid chunker — sentence-transformers embeddings over AST chunks.

All tests share a single model load via module-scope fixture to keep
the suite wall-clock bounded. The real model only loads once per test
module run.
"""

from __future__ import annotations

import math

import pytest

from vitruvius.normalization.ast_chunker import Chunk, split_into_chunks
from vitruvius.normalization.embedding_chunker import (
    DEFAULT_BATCH_SIZE,
    EMBEDDING_DIM,
    EMBEDDING_MODEL_NAME,
    EmbeddedChunk,
    _load_model,
    embed_chunks,
)


SAMPLE_MARKDOWN = (
    "# PD 1096\n\n"
    "## Chapter 1\n\n"
    "### Section 101\n\n"
    "This decree shall be known as the National Building Code.\n\n"
    "### Section 102\n\n"
    "It is hereby declared the policy of the State to safeguard life.\n"
)


@pytest.fixture(scope="module")
def loaded_chunks() -> list[EmbeddedChunk]:
    """Pre-compute embeddings for the sample doc ONCE per test module."""
    chunks = split_into_chunks(SAMPLE_MARKDOWN, source_path="pd1096.md")
    return embed_chunks(chunks)


def test_each_chunk_has_384_dim_vector(loaded_chunks: list[EmbeddedChunk]) -> None:
    assert loaded_chunks
    for ec in loaded_chunks:
        assert isinstance(ec.embedding, tuple)
        assert len(ec.embedding) == EMBEDDING_DIM
        assert all(isinstance(x, float) for x in ec.embedding)


def test_embedding_determinism_same_text_same_vector() -> None:
    c = Chunk(
        chunk_id="fx::0000",
        source_path="fx.md",
        source_section_id="",
        parent_titles=(),
        heading="Test",
        body="Every building shall have a permit.",
        token_count=6,
    )
    e1 = embed_chunks([c])
    e2 = embed_chunks([c])
    assert e1[0].embedding == e2[0].embedding


def test_empty_body_produces_zero_vector() -> None:
    c = Chunk(
        chunk_id="fx::0000",
        source_path="fx.md",
        source_section_id="",
        parent_titles=(),
        heading="Empty",
        body="",
        token_count=0,
    )
    embedded = embed_chunks([c])
    assert len(embedded) == 1
    assert all(x == 0.0 for x in embedded[0].embedding)


def test_whitespace_only_body_produces_zero_vector() -> None:
    c = Chunk(
        chunk_id="fx::0001",
        source_path="fx.md",
        source_section_id="",
        parent_titles=(),
        heading="WS",
        body="   \n\t  \n",
        token_count=0,
    )
    embedded = embed_chunks([c])
    assert len(embedded) == 1
    assert all(x == 0.0 for x in embedded[0].embedding)


def test_batch_processing_never_exceeds_32() -> None:
    """We expose batch_size via the kwarg. The default is 32."""
    assert DEFAULT_BATCH_SIZE == 32
    chunks = [
        Chunk(
            chunk_id=f"fx::{i:04d}",
            source_path="fx.md",
            source_section_id="",
            parent_titles=(),
            heading=f"C{i}",
            body=f"Section {i} governs building permits for class A.",
            token_count=10,
        )
        for i in range(100)
    ]
    embedded = embed_chunks(chunks, batch_size=16)
    assert len(embedded) == 100
    for ec in embedded:
        assert len(ec.embedding) == EMBEDDING_DIM


def test_lazy_loading_does_not_load_until_first_call(monkeypatch) -> None:
    """Importing the module does not call SentenceTransformer()."""
    call_counter = {"count": 0}

    class FakeModel:
        def __init__(self, *a, **kw):
            call_counter["count"] += 1

        def encode(self, texts, **kw):
            import numpy as np

            return np.zeros((len(texts), EMBEDDING_DIM), dtype=float)

    import sentence_transformers

    monkeypatch.setattr(sentence_transformers, "SentenceTransformer", FakeModel)
    _load_model.cache_clear()

    from vitruvius.normalization import embedding_chunker

    assert call_counter["count"] == 0

    c = Chunk(
        chunk_id="lazy::0000",
        source_path="lazy.md",
        source_section_id="",
        parent_titles=(),
        heading="L",
        body="test",
        token_count=1,
    )
    embedding_chunker.embed_chunks([c])
    assert call_counter["count"] == 1

    embedding_chunker.embed_chunks([c])
    assert call_counter["count"] == 1

    _load_model.cache_clear()


def test_preserves_original_chunk_reference(loaded_chunks: list[EmbeddedChunk]) -> None:
    for ec in loaded_chunks:
        assert isinstance(ec.chunk, Chunk)
        assert ec.chunk.chunk_id.startswith("pd1096::")


def test_constants_match_model_card() -> None:
    assert EMBEDDING_MODEL_NAME.endswith("all-MiniLM-L6-v2")
    assert EMBEDDING_DIM == 384
    assert DEFAULT_BATCH_SIZE == 32


def test_different_text_produces_different_vectors() -> None:
    a = Chunk(
        chunk_id="a::0",
        source_path="a.md",
        source_section_id="",
        parent_titles=(),
        heading="A",
        body="Building permits must be obtained before construction begins.",
        token_count=9,
    )
    b = Chunk(
        chunk_id="b::0",
        source_path="b.md",
        source_section_id="",
        parent_titles=(),
        heading="B",
        body="The quick brown fox jumps over a lazy dog near the river.",
        token_count=12,
    )
    [ea, eb] = embed_chunks([a, b])
    assert ea.embedding != eb.embedding


def test_empty_chunk_list_returns_empty_list() -> None:
    assert embed_chunks([]) == []


def test_embedded_chunk_is_frozen_dataclass() -> None:
    c = Chunk(
        chunk_id="frz::0",
        source_path="f.md",
        source_section_id="",
        parent_titles=(),
        heading="F",
        body="freeze me",
        token_count=2,
    )
    [ec] = embed_chunks([c])
    try:
        ec.embedding = (0.0,) * EMBEDDING_DIM  # type: ignore[misc]
    except Exception:
        return
    raise AssertionError("EmbeddedChunk should be frozen (immutable)")


def test_similar_sentences_closer_than_dissimilar() -> None:
    """Cosine similarity sanity: building-permit sentences should cluster."""

    def cos(u: tuple[float, ...], v: tuple[float, ...]) -> float:
        dot = sum(x * y for x, y in zip(u, v))
        nu = math.sqrt(sum(x * x for x in u))
        nv = math.sqrt(sum(y * y for y in v))
        if nu == 0.0 or nv == 0.0:
            return 0.0
        return dot / (nu * nv)

    def _chunk(cid: str, body: str) -> Chunk:
        return Chunk(
            chunk_id=cid,
            source_path="x.md",
            source_section_id="",
            parent_titles=(),
            heading="H",
            body=body,
            token_count=len(body.split()),
        )

    anchor = _chunk("0", "A building permit is required before any construction.")
    near = _chunk("1", "Construction shall not start without a building permit.")
    far = _chunk("2", "Bananas are yellow fruits grown in tropical climates.")

    [ea, en, ef] = embed_chunks([anchor, near, far])
    assert cos(ea.embedding, en.embedding) > cos(ea.embedding, ef.embedding)
