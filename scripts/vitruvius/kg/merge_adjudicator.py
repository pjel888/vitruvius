"""Merge Adjudicator — propose merges for exact duplicate canonical nodes.

Does **not** auto-merge.  Creates :class:`MergeAssertion` records for
human review.  Only exact matches on (type, normalized_label) are proposed.

Usage::

    from vitruvius.kg.merge_adjudicator import MergeAdjudicator
    adjudicator = MergeAdjudicator()
    merges = adjudicator.propose(nodes)
"""

from __future__ import annotations

from datetime import datetime, timezone

from .schemas import CanonicalNode, MergeAssertion
from .enums import ValidationState


class MergeAdjudicator:
    """Propose merge candidates among canonical nodes.

    Exact-match strategy: same ``type`` + same normalized label.
    """

    def __init__(self, similarity_threshold: float = 1.0) -> None:
        self.similarity_threshold = similarity_threshold

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def propose(self, nodes: list[CanonicalNode]) -> list[MergeAssertion]:
        """Return proposed merges for *nodes*.

        Only pairs with identical (type, normalized_label) are proposed.
        """
        if len(nodes) < 2:
            return []

        # Index by normalized label per type
        buckets: dict[tuple[str, str], list[CanonicalNode]] = {}
        for node in nodes:
            key = (node.type.value, self._normalize(node.label))
            buckets.setdefault(key, []).append(node)

        merges: list[MergeAssertion] = []
        for _key, group in buckets.items():
            if len(group) < 2:
                continue
            # Generate pairwise merge assertions for all pairs in the bucket
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    merge = self._build_assertion(group[i], group[j])
                    if merge is not None:
                        merges.append(merge)
        return merges

    # ------------------------------------------------------------------
    # Assertion building
    # ------------------------------------------------------------------

    def _build_assertion(
        self,
        node_a: CanonicalNode,
        node_b: CanonicalNode,
    ) -> MergeAssertion | None:
        """Construct a MergeAssertion for two duplicate nodes.

        Returns ``None`` if neither node carries evidence, because an
        evidence-less merge assertion would violate the architectural
        invariant that every assertion must be backed by evidence.
        """
        ts = datetime.now(timezone.utc).isoformat()
        # Merge evidence from both nodes
        merged_evidence = list(dict.fromkeys(
            (node_a.primary_assertion_id or "").split(",") +
            (node_b.primary_assertion_id or "").split(",")
        ))
        merged_evidence = [e for e in merged_evidence if e]
        if not merged_evidence:
            return None
        return MergeAssertion(
            id=f"assert-merge-{node_a.id}-into-{node_b.id}",
            from_node_id=node_a.id,
            to_node_id=node_b.id,
            reasoning_summary=f"Identical type={node_a.type.value} and normalized label='{self._normalize(node_a.label)}'",
            confidence=1.0,
            validation_status=ValidationState.REVIEW_REQUIRED,
            evidence_ids=merged_evidence,
            created_at=ts,
            version=1,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize(label: str) -> str:
        """Lowercase and collapse whitespace."""
        return " ".join(label.strip().lower().split())
