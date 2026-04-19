"""Canonicalizer — turn extracted candidates into canonical nodes.

Deterministic deduplication, label normalization, stable ID assignment,
and embedding-aware near-duplicate flagging.

Usage::

    from vitruvius.kg.canonicalizer import Canonicalizer
    canonicalizer = Canonicalizer()
    nodes = canonicalizer.canonicalize(candidates)
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from .embeddings import EmbeddingClient
from .schemas import CanonicalNode, KnowledgeUnitCandidate
from .enums import NodeType, ValidationState


class Canonicalizer:
    """Promote candidates to canonical nodes.

    Parameters
    ----------
    embedder:
        Optional :class:`EmbeddingClient` for near-duplicate detection.
    """

    def __init__(self, embedder: EmbeddingClient | None = None) -> None:
        self.embedder = embedder
        self._seen_ids: set[str] = set()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def canonicalize(
        self,
        candidates: list[KnowledgeUnitCandidate],
    ) -> list[CanonicalNode]:
        """Return deduplicated canonical nodes from *candidates*.

        Exact duplicates (same unit_type, normalized label, normalized text)
        are collapsed to a single node.  The highest-confidence candidate
        wins; span_ids and embeddings are merged.
        """
        if not candidates:
            return []

        # 1. Exact dedupe
        groups = self._dedupe_exact(candidates)

        # 2. Build canonical nodes from groups
        nodes: list[CanonicalNode] = []
        for key, group in groups.items():
            winner = max(group, key=lambda c: c.confidence)
            node = self._candidate_to_node(winner, group)
            nodes.append(node)

        # 3. Near-duplicate flagging (optional)
        if self.embedder:
            nodes = self._flag_near_duplicates(nodes)

        return nodes

    # ------------------------------------------------------------------
    # Deduplication
    # ------------------------------------------------------------------

    def _dedupe_exact(
        self,
        candidates: list[KnowledgeUnitCandidate],
    ) -> dict[tuple[str, str, str], list[KnowledgeUnitCandidate]]:
        """Group candidates by exact match on (unit_type, label, text)."""
        groups: dict[tuple[str, str, str], list[KnowledgeUnitCandidate]] = {}
        for cand in candidates:
            key = (cand.unit_type, self._normalize_label(cand.label), cand.text.strip().lower())
            groups.setdefault(key, []).append(cand)
        return groups

    def _flag_near_duplicates(self, nodes: list[CanonicalNode]) -> list[CanonicalNode]:
        """Flag nodes with high embedding similarity as potential merges.

        Does **not** auto-merge; sets ``status = REVIEW_REQUIRED`` and
        appends a warning to ``summary``.
        """
        if len(nodes) < 2:
            return nodes

        # Collect nodes that have embeddings
        indexed = [(i, n) for i, n in enumerate(nodes) if n.embedding_ref]
        for idx, (i, node_a) in enumerate(indexed):
            for j, node_b in indexed[idx + 1 :]:
                # embedding_ref stores the embedding as a JSON string or is None
                emb_a = self._parse_embedding(node_a.embedding_ref)
                emb_b = self._parse_embedding(node_b.embedding_ref)
                if emb_a and emb_b:
                    sim = EmbeddingClient.cosine_similarity(emb_a, emb_b)
                    if sim >= 0.95:
                        nodes[i] = nodes[i].model_copy(
                            update={
                                "status": ValidationState.REVIEW_REQUIRED,
                                "summary": (
                                    node_a.summary
                                    + f" [NEAR_DUPLICATE: {node_b.id} sim={sim:.3f}]"
                                ).strip(),
                            }
                        )
                        nodes[j] = nodes[j].model_copy(
                            update={
                                "status": ValidationState.REVIEW_REQUIRED,
                                "summary": (
                                    node_b.summary
                                    + f" [NEAR_DUPLICATE: {node_a.id} sim={sim:.3f}]"
                                ).strip(),
                            }
                        )
        return nodes

    # ------------------------------------------------------------------
    # Node building
    # ------------------------------------------------------------------

    def _candidate_to_node(
        self,
        winner: KnowledgeUnitCandidate,
        group: list[KnowledgeUnitCandidate],
    ) -> CanonicalNode:
        """Convert a candidate group into a single CanonicalNode."""
        unit_type = winner.unit_type
        label = winner.label.strip()
        slug = self._slugify(label)
        node_id = self._assign_id(unit_type, slug)

        # Merge span_ids from all candidates in the group
        all_span_ids: list[str] = []
        for c in group:
            all_span_ids.extend(c.span_ids)
        unique_span_ids = list(dict.fromkeys(all_span_ids))

        # Store embedding as JSON string in embedding_ref if available
        embedding_ref: str | None = None
        if winner.embedding:
            embedding_ref = str(winner.embedding)

        return CanonicalNode(
            id=node_id,
            type=self._node_type_from_string(unit_type),
            label=label,
            slug=slug,
            summary=winner.text.strip(),
            taxonomy_path=[],
            aliases=[],
            status=ValidationState.CANDIDATE,
            confidence=winner.confidence,
            version=1,
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
            embedding_ref=embedding_ref,
            primary_assertion_id=None,
        )

    # ------------------------------------------------------------------
    # ID assignment
    # ------------------------------------------------------------------

    def _assign_id(self, unit_type: str, slug: str) -> str:
        """Stable ID with collision suffix."""
        base = f"{unit_type}-{slug}"
        if base not in self._seen_ids:
            self._seen_ids.add(base)
            return base
        # Collision: append -001, -002, ...
        counter = 1
        while True:
            candidate = f"{base}-{counter:03d}"
            if candidate not in self._seen_ids:
                self._seen_ids.add(candidate)
                return candidate
            counter += 1

    # ------------------------------------------------------------------
    # Normalization helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_label(label: str) -> str:
        """Lowercase, strip surrounding whitespace, collapse inner spaces."""
        return " ".join(label.strip().lower().split())

    @staticmethod
    def _slugify(label: str) -> str:
        """Convert label to URL-safe slug."""
        slug = label.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = re.sub(r"-+", "-", slug)
        slug = slug.strip("-")
        return slug or "unknown"

    @staticmethod
    def _node_type_from_string(unit_type: str) -> NodeType:
        mapping = {
            "concept": NodeType.CONCEPT,
            "definition": NodeType.DEFINITION,
            "rule": NodeType.RULE,
            "procedure": NodeType.PROCEDURE,
            "exception": NodeType.EXCEPTION,
        }
        return mapping.get(unit_type, NodeType.CONCEPT)

    @staticmethod
    def _parse_embedding(value: str | None) -> list[float] | None:
        from .embeddings import EmbeddingClient
        return EmbeddingClient.parse_embedding(value)
