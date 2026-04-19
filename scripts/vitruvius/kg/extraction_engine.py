"""Extraction engine — chunk → prompt → LLM → validated candidates.

Orchestrates atomic-knowledge-unit extraction from :class:`Chunk` objects
using :class:`StructuredLLMClient` and prompt templates.

Usage::

    from vitruvius.kg.extraction_engine import ExtractionEngine
    engine = ExtractionEngine(llm=StructuredLLMClient(ollama_model="qwen2.5:3b"))
    result = engine.extract_from_chunk(chunk, unit_type="concept")
"""

from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel

from .embeddings import EmbeddingClient
from .extraction_validator import ExtractionValidator
from .json_evidence_store import KgV2Snapshot
from .schemas import Chunk, ExtractionResult, KnowledgeUnitCandidate

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt registry
# ---------------------------------------------------------------------------

_PROMPT_DIR = Path(__file__).with_suffix("").parent / "prompts"

_UNIT_TYPES: tuple[Literal["concept", "definition", "rule", "procedure", "exception"], ...] = (
    "concept",
    "definition",
    "rule",
    "procedure",
    "exception",
)


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class ExtractionEngine:
    """Extract atomic knowledge units from chunks.

    Parameters
    ----------
    llm:
        A :class:`StructuredLLMClient` instance (already configured with
        ``qwen2.5:3b`` or similar).
    embedder:
        Optional :class:`EmbeddingClient` for candidate deduplication.
    min_chunk_chars:
        Chunks shorter than this are skipped (default 50).
    max_chunk_chars:
        Chunks longer than this are truncated before prompting (default 2048).
    """

    def __init__(
        self,
        llm: Any,
        embedder: EmbeddingClient | None = None,
        validator: ExtractionValidator | None = None,
        min_chunk_chars: int = 50,
        max_chunk_chars: int = 2048,
    ) -> None:
        self.llm = llm
        self.embedder = embedder
        self.validator = validator or ExtractionValidator(strict_traceability=False)
        self.min_chunk_chars = min_chunk_chars
        self.max_chunk_chars = max_chunk_chars
        self._prompts: dict[str, str] = {}
        self._load_prompts()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract_from_chunk(
        self,
        chunk: Chunk,
        unit_type: Literal["concept", "definition", "rule", "procedure", "exception"],
        run_id: str = "",
        span_ids: list[str] | None = None,
    ) -> ExtractionResult:
        """Extract one unit type from a single chunk.

        Parameters
        ----------
        span_ids:
            Evidence span IDs supporting this chunk.  If ``None``, a
            traceability placeholder ``span-<chunk_suffix>`` is generated
            so that candidates are never created without evidence links.
        """
        if len(chunk.text) < self.min_chunk_chars:
            return ExtractionResult(
                unit_type=unit_type,
                chunk_id=chunk.id,
                error="chunk_too_short",
            )

        # Default traceability: derive a span ID from the chunk ID
        if span_ids is None:
            chunk_suffix = chunk.id.replace("chk-", "")
            span_ids = [f"span-{chunk_suffix}"]

        prompt = self._build_prompt(chunk, unit_type, run_id)
        start_ms = int(time.time() * 1000)

        raw_result = self.llm.extract(
            prompt=prompt,
            model_cls=_CandidateList,
            model=self.llm.ollama_model if hasattr(self.llm, "ollama_model") else None,
        )

        duration_ms = int(time.time() * 1000) - start_ms

        if raw_result is None:
            return ExtractionResult(
                unit_type=unit_type,
                chunk_id=chunk.id,
                duration_ms=duration_ms,
                error="llm_extraction_failed",
            )

        candidates = [
            KnowledgeUnitCandidate(
                id=f"cand-{unit_type}-{uuid.uuid4().hex[:12]}",
                unit_type=unit_type,
                label=c.label,
                text=c.text,
                span_ids=list(span_ids),
                chunk_id=chunk.id,
                confidence=max(0.0, min(1.0, c.confidence)),
                extraction_run_id=run_id,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            for c in raw_result.candidates
            if c.label.strip() and c.text.strip()
        ]

        # Validate candidates before embedding / returning
        valid_candidates = self.validator.filter_valid(candidates)
        rejected_count = len(candidates) - len(valid_candidates)
        if rejected_count > 0:
            logger.warning(
                "Extraction validation rejected %d/%d candidates for chunk %s",
                rejected_count,
                len(candidates),
                chunk.id,
            )
            for cand in candidates:
                result = self.validator.validate_candidate(cand)
                if not result.passed:
                    logger.debug(
                        "Rejected candidate %s: %s",
                        cand.id,
                        "; ".join(result.errors),
                    )

        # Compute embeddings if embedder is available
        if self.embedder and valid_candidates:
            texts = [f"{c.label}\n{c.text}" for c in valid_candidates]
            try:
                vectors = self.embedder.embed_texts(texts)
                for cand, vec in zip(valid_candidates, vectors):
                    cand.embedding = vec
            except Exception as exc:
                logger.warning("Embedding failed for chunk %s: %s", chunk.id, exc)

        return ExtractionResult(
            unit_type=unit_type,
            candidates=valid_candidates,
            chunk_id=chunk.id,
            model=getattr(self.llm, "ollama_model", ""),
            duration_ms=duration_ms,
        )

    def extract_from_snapshot(
        self,
        snapshot: KgV2Snapshot,
        unit_types: list[str] | None = None,
        run_id: str = "",
    ) -> list[ExtractionResult]:
        """Extract from every chunk in *snapshot* for every requested unit type.

        Processing is **sequential** to respect the 8 GB M2 RAM envelope.
        """
        if unit_types is None:
            unit_types = list(_UNIT_TYPES)

        # Build chunk_id → evidence_span_ids index for traceability
        chunk_spans: dict[str, list[str]] = {}
        for span in snapshot.evidence_spans:
            # EvidenceSpan.id is typically "span-<chunk-suffix>"; we also
            # match by document_version_id for broader coverage.
            chunk_spans.setdefault(span.id, []).append(span.id)
            # Heuristic: if chunk_id pattern can be derived, index it too
            if span.id.startswith("span-"):
                derived_chunk_id = span.id.replace("span-", "chk-")
                chunk_spans.setdefault(derived_chunk_id, []).append(span.id)

        results: list[ExtractionResult] = []
        for chunk in snapshot.chunks:
            if not chunk.text.strip():
                continue
            span_ids = chunk_spans.get(chunk.id)
            for ut in unit_types:
                if ut not in _UNIT_TYPES:
                    logger.warning("Unknown unit_type %r; skipping", ut)
                    continue
                result = self.extract_from_chunk(chunk, ut, run_id=run_id, span_ids=span_ids)
                results.append(result)
        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_prompts(self) -> None:
        for ut in _UNIT_TYPES:
            path = _PROMPT_DIR / f"extract_{ut}.txt"
            if path.exists():
                self._prompts[ut] = path.read_text(encoding="utf-8")
            else:
                logger.warning("Prompt file missing: %s", path)

    def _build_prompt(
        self,
        chunk: Chunk,
        unit_type: str,
        run_id: str,
    ) -> str:
        template = self._prompts.get(unit_type, "")
        if not template:
            raise ValueError(f"No prompt template for unit_type={unit_type}")

        chunk_text = chunk.text[: self.max_chunk_chars]
        iso_now = datetime.now(timezone.utc).isoformat()
        return (
            template
            .replace("{chunk_text}", chunk_text)
            .replace("<CHUNK_ID>", chunk.id)
            .replace("<RUN_ID>", run_id or "unknown")
            .replace("<ISO8601>", iso_now)
        )


# ---------------------------------------------------------------------------
# Private Pydantic helper for LLM output
# ---------------------------------------------------------------------------

class _RawCandidate(BaseModel):
    """Minimal schema for LLM-returned candidate items."""

    label: str
    text: str
    confidence: float = 0.0


class _CandidateList(BaseModel):
    """Expected JSON schema wrapper for LLM responses."""

    candidates: list[_RawCandidate] = []
