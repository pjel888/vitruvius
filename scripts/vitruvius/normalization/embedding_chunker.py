"""Hybrid semantic-structural chunker — Task C.3.

Extends `ast_chunker` by wrapping every emitted Chunk in an
`EmbeddedChunk` that carries a 384-dim sentence-transformers vector
computed from the chunk body. The transformer model
(`all-MiniLM-L6-v2`) is loaded lazily on first call — importing this
module does NOT touch the network or pull ~200MB of weights.

Empty / whitespace-only bodies produce a zero vector rather than being
skipped, so downstream MCMC / similarity / outlier code never has to
reason about missing chunks. Determinism is inherited from
sentence-transformers: identical inputs (same model, same batch size)
produce byte-identical vectors.

Feature flag: `features.c_hybrid_chunking`. The gate lives at the call
site — this module is always safe to import and `embed_chunks` is
always callable. That keeps unit tests simple and keeps the lazy-load
contract enforceable.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

from .ast_chunker import Chunk

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer  # noqa: F401


EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
DEFAULT_BATCH_SIZE = 32

_ZERO_VECTOR: tuple[float, ...] = (0.0,) * EMBEDDING_DIM


@dataclass(frozen=True)
class EmbeddedChunk:
    """A Chunk paired with its 384-dim sentence-transformers embedding.

    `embedding` is a frozen `tuple[float, ...]` of length `EMBEDDING_DIM`
    so the record is hashable and safely comparable. Empty-body chunks
    carry `_ZERO_VECTOR` rather than being dropped.
    """

    chunk: Chunk
    embedding: tuple[float, ...]


@lru_cache(maxsize=1)
def _load_model() -> "SentenceTransformer":
    """Load the sentence-transformers model. Cached across calls.

    This import is deliberately inside the function so importing
    `embedding_chunker` at module level never triggers a model load.
    The `lru_cache(maxsize=1)` ensures the model is constructed exactly
    once per process (tests can `.cache_clear()` to reset).
    """
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def embed_chunks(
    chunks: list[Chunk],
    *,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> list[EmbeddedChunk]:
    """Compute embeddings for every chunk body.

    Lazy-loads the model on first call. Processes bodies in batches of
    `batch_size` (default 32, the 8GB M2 RAM safety margin). Chunks
    with empty / whitespace-only bodies short-circuit to a zero vector
    without touching the model — that keeps zero-body chunks cheap and
    ensures downstream similarity math handles them naturally.

    Returns a list of `EmbeddedChunk` in the same order as `chunks`.
    """
    if not chunks:
        return []

    non_empty_indices: list[int] = []
    non_empty_bodies: list[str] = []
    for idx, chunk in enumerate(chunks):
        if chunk.body and chunk.body.strip():
            non_empty_indices.append(idx)
            non_empty_bodies.append(chunk.body)

    embeddings: list[tuple[float, ...]] = [_ZERO_VECTOR] * len(chunks)

    if non_empty_bodies:
        model = _load_model()
        vectors = model.encode(
            non_empty_bodies,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        for idx, vec in zip(non_empty_indices, vectors):
            embeddings[idx] = tuple(float(x) for x in vec)

    return [
        EmbeddedChunk(chunk=chunk, embedding=emb)
        for chunk, emb in zip(chunks, embeddings)
    ]
