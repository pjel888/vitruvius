"""Placement Engine — assign canonical nodes to taxonomy parents.

Three-tier strategy:
1. Rule-based (unit_type → fixed taxonomy path)
2. Embedding similarity to taxonomy node embeddings
3. Ambiguity flag when top-2 similarity is within 0.1

Usage::

    from vitruvius.kg.placement_engine import PlacementEngine
    engine = PlacementEngine(taxonomy_nodes, embedder)
    placements = engine.place(node)
"""

from __future__ import annotations

from .embeddings import EmbeddingClient
from .schemas import CanonicalNode, TaxonomyNode
from .enums import NodeType


class PlacementEngine:
    """Assign canonical nodes to taxonomy parents.

    Parameters
    ----------
    taxonomy_nodes:
        All known :class:`TaxonomyNode` records against which to place.
    embedder:
        Optional :class:`EmbeddingClient` for similarity-based placement.
    """

    # Rule-based mapping from NodeType to preferred taxonomy path segments.
    RULE_PATHS: dict[NodeType, list[str]] = {
        NodeType.CONCEPT: ["concepts"],
        NodeType.DEFINITION: ["concepts", "definitions"],
        NodeType.RULE: ["rules"],
        NodeType.PROCEDURE: ["procedures"],
        NodeType.EXCEPTION: ["exceptions"],
    }

    def __init__(
        self,
        taxonomy_nodes: list[TaxonomyNode],
        embedder: EmbeddingClient | None = None,
    ) -> None:
        self.taxonomy_nodes = taxonomy_nodes
        self.embedder = embedder

        # Index taxonomy nodes by their full path for quick lookup
        self._path_index: dict[str, TaxonomyNode] = {}
        for tn in taxonomy_nodes:
            path_key = self._path_key(tn.path)
            self._path_index[path_key] = tn

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def place(self, node: CanonicalNode) -> list[str]:
        """Return a list of taxonomy paths for *node*.

        Tier 1: rule-based exact match on NodeType.
        Tier 2: embedding similarity if no rule match and embedder present.
        Tier 3: ambiguity flagging handled by caller (near-equal top-2 scores).
        """
        # Tier 1: Rule-based
        rule_paths = self._rule_paths_for(node)
        if rule_paths:
            return rule_paths

        # Tier 2: Embedding-based
        if node.embedding_ref:
            sim_paths = self._similarity_paths_for(node)
            if sim_paths:
                return sim_paths

        # Fallback: root-level placement
        return ["/"]

    def is_ambiguous(self, node: CanonicalNode, paths: list[str]) -> bool:
        """Return ``True`` if the top-2 taxonomy paths are within 0.1 similarity.

        Only meaningful when paths came from the embedding tier.
        """
        if not node.embedding_ref:
            return False
        if len(paths) < 2:
            return False
        return self._top_scores_within(node, paths[0], paths[1], delta=0.1)

    # ------------------------------------------------------------------
    # Tier 1 — Rule-based
    # ------------------------------------------------------------------

    def _rule_paths_for(self, node: CanonicalNode) -> list[str]:
        """Return taxonomy path(s) dictated by the node type rules."""
        segments = self.RULE_PATHS.get(node.type)
        if not segments:
            return []
        # Verify the path exists in taxonomy; if not, return empty so tier 2 can try
        full_path = "/".join(segments)
        if full_path in self._path_index:
            return [full_path]
        return []

    # ------------------------------------------------------------------
    # Tier 2 — Embedding similarity
    # ------------------------------------------------------------------

    def _similarity_paths_for(self, node: CanonicalNode) -> list[str]:
        """Return the best-matching taxonomy path(s) by embedding similarity."""
        node_emb = self._parse_embedding(node.embedding_ref)
        if not node_emb or not self.taxonomy_nodes:
            return []

        scored: list[tuple[float, str]] = []
        for tn in self.taxonomy_nodes:
            if not tn.embedding:
                continue
            sim = EmbeddingClient.cosine_similarity(node_emb, tn.embedding)
            scored.append((sim, self._path_key(tn.path)))

        if not scored:
            return []

        scored.sort(reverse=True, key=lambda x: x[0])
        best_score, best_path = scored[0]
        # Return top match; include second if within ambiguity threshold
        paths = [best_path]
        if len(scored) > 1:
            second_score = scored[1][0]
            if abs(best_score - second_score) <= 0.1:
                paths.append(scored[1][1])
        return paths

    def _top_scores_within(
        self, node: CanonicalNode, path_a: str, path_b: str, delta: float
    ) -> bool:
        """Check if similarity scores for two paths are within *delta*."""
        node_emb = self._parse_embedding(node.embedding_ref)
        if not node_emb:
            return False

        node_a = self._path_index.get(path_a)
        node_b = self._path_index.get(path_b)
        if not node_a or not node_b:
            return False

        sim_a = EmbeddingClient.cosine_similarity(node_emb, node_a.embedding or [])
        sim_b = EmbeddingClient.cosine_similarity(node_emb, node_b.embedding or [])
        return abs(sim_a - sim_b) <= delta

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _path_key(path: list[str]) -> str:
        """Flatten a taxonomy path list to a string key."""
        return "/".join(path)

    @staticmethod
    def _parse_embedding(value: str | None) -> list[float] | None:
        from .embeddings import EmbeddingClient
        return EmbeddingClient.parse_embedding(value)
