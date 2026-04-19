"""Embedding client for the KG transition.

Primary backend: Ollama ``nomic-embed-text`` via ``/api/embeddings``.
Fallback backend: ``sentence-transformers`` ``all-MiniLM-L6-v2`` (already
shipped in the codebase).

Usage::

    from vitruvius.kg.embeddings import EmbeddingClient
    client = EmbeddingClient(model="nomic-embed-text")
    vectors = client.embed_texts(["chunk one", "chunk two"])
"""

from __future__ import annotations

import json
import logging
import math
import urllib.request
from typing import Any

logger = logging.getLogger(__name__)


class EmbeddingClient:
    """Produce vector embeddings for texts.

    Parameters
    ----------
    model:
        Ollama embedding model name (default ``nomic-embed-text``).
    ollama_url:
        Base URL for Ollama (default ``http://127.0.0.1:11434``).
    fallback:
        If ``True`` (default), falls back to sentence-transformers when
        Ollama is unreachable.
    """

    def __init__(
        self,
        model: str = "nomic-embed-text",
        ollama_url: str = "http://127.0.0.1:11434",
        fallback: bool = True,
    ) -> None:
        self.model = model
        self.ollama_url = ollama_url.rstrip("/")
        self.fallback = fallback
        self._st: Any | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding vector per text.

        Raises ``RuntimeError`` if both backends fail.
        """
        if not texts:
            return []

        try:
            return self._embed_ollama(texts)
        except Exception as exc:
            logger.warning("Ollama embedding failed (%s); trying fallback", exc)
            if self.fallback:
                return self._embed_sentence_transformers(texts)
            raise RuntimeError(f"Embedding failed and fallback disabled: {exc}") from exc

    @staticmethod
    def cosine_similarity(a: list[float], b: list[float]) -> float:
        """Cosine similarity between two vectors (-1.0 … 1.0)."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    @staticmethod
    def parse_embedding(value: str | None) -> list[float] | None:
        """Parse an embedding string (JSON list repr) into a float list."""
        if not value:
            return None
        try:
            import ast

            parsed = ast.literal_eval(value)
            if isinstance(parsed, list) and all(isinstance(x, (int, float)) for x in parsed):
                return [float(x) for x in parsed]
        except (ValueError, SyntaxError):
            pass
        return None

    # ------------------------------------------------------------------
    # Backends
    # ------------------------------------------------------------------

    def _embed_ollama(self, texts: list[str]) -> list[list[float]]:
        """Call Ollama ``/api/embeddings``.

        Ollama only accepts one text per call, so we loop.
        """
        vectors: list[list[float]] = []
        for text in texts:
            body = json.dumps(
                {"model": self.model, "prompt": text}
            ).encode("utf-8")
            req = urllib.request.Request(
                f"{self.ollama_url}/api/embeddings",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                embedding = data.get("embedding")
                if not isinstance(embedding, list):
                    raise ValueError(f"Unexpected Ollama response: {data}")
                vectors.append(embedding)
        return vectors

    def _embed_sentence_transformers(self, texts: list[str]) -> list[list[float]]:
        """Fallback using sentence-transformers."""
        if self._st is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError(
                    "sentence-transformers not installed; cannot fall back"
                ) from exc
            self._st = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = self._st.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return [emb.tolist() for emb in embeddings]
