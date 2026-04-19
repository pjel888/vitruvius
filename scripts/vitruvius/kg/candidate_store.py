"""Candidate store — file-native JSONL persistence for extracted knowledge units.

All candidates are stored as newline-delimited JSON in
``006_System-Manifests/runs/kg_candidates/``.

Usage::

    from vitruvius.kg.candidate_store import CandidateStore
    store = CandidateStore()
    path = store.save(results)
    loaded = store.load(path)
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from vitruvius.paths import get_repo_root

from .schemas import ExtractionResult, KnowledgeUnitCandidate

logger = logging.getLogger(__name__)


class CandidateStore:
    """Persist and load :class:`ExtractionResult` records as JSONL.

    Parameters
    ----------
    base_dir:
        Directory for candidate files.  Defaults to
        ``006_System-Manifests/runs/kg_candidates/`` under repo root.
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        if base_dir is None:
            base_dir = (
                get_repo_root()
                / "006_System-Manifests"
                / "runs"
                / "kg_candidates"
            )
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def save(self, results: list[ExtractionResult], run_id: str = "") -> Path:
        """Write *results* to a timestamped JSONL file.

        Returns the path written.
        """
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        rid = run_id or ts
        path = self.base_dir / f"{rid}_candidates.jsonl"

        with path.open("w", encoding="utf-8") as f:
            for result in results:
                f.write(json.dumps(result.model_dump(mode="json"), ensure_ascii=False) + "\n")

        logger.info("Wrote %d results to %s", len(results), path)
        return path

    def load(self, path: Path) -> list[ExtractionResult]:
        """Read JSONL file and return list of :class:`ExtractionResult`."""
        results: list[ExtractionResult] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    results.append(ExtractionResult.model_validate(data))
                except (json.JSONDecodeError, Exception) as exc:
                    logger.warning("Skipping malformed line in %s: %s", path, exc)
        return results

    def dedupe_by_embedding(
        self,
        candidates: list[KnowledgeUnitCandidate],
        threshold: float = 0.92,
    ) -> list[KnowledgeUnitCandidate]:
        """Remove near-duplicate candidates by embedding cosine similarity.

        Keeps the first occurrence of each duplicate cluster.
        Candidates without embeddings are preserved unchanged.
        """
        kept: list[KnowledgeUnitCandidate] = []
        for cand in candidates:
            if cand.embedding is None:
                kept.append(cand)
                continue
            is_duplicate = False
            for existing in kept:
                if existing.embedding is None:
                    continue
                sim = self._cosine_similarity(cand.embedding, existing.embedding)
                if sim >= threshold:
                    is_duplicate = True
                    break
            if not is_duplicate:
                kept.append(cand)
        return kept

    def checksum(self, path: Path) -> str:
        """SHA-256 of file contents — deterministic integrity check."""
        h = hashlib.sha256()
        h.update(path.read_bytes())
        return h.hexdigest()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        import math

        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
