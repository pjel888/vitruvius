"""Sprint HP Stream HP.5 — Knowledge Graph Representation Learning (GraphSAGE).

Structural node embeddings using GraphSAGE aggregators and a complementary
"structural loopholes" detector that finds pairs of nodes which are
topologically distant (long BFS path) but semantically similar (close in
sentence-transformer cosine space). Those pairs are candidate hidden
contradictions — two ordinances saying nearly-the-same-thing in places the
citation graph would never bring into contact.

Design notes
------------
* Lazy imports: we pull in ``torch`` / ``torch_geometric`` inside the
  implementation so importing this module is cheap. Hosts without
  ``torch_geometric`` can still import this module and call
  :func:`find_structural_loopholes` (which doesn't need pyG); only
  :func:`compute_graphsage_embeddings` raises at call time.
* Determinism: we seed ``torch``, ``numpy``, and ``random`` with
  ``random_state`` before constructing the SAGE model, run a fixed number
  of deterministic forward passes (no stochastic sampling), and return
  ``np.float32`` arrays. Calling twice with the same seed yields identical
  embeddings.
* Feature matrix: we use a simple 8-dim identity feature per node formed
  from a one-hot over a small fixed node-type vocabulary plus a numeric
  trust-level slot. This is enough to make two nodes of different types
  start with distinct representations, while still letting the SAGE
  aggregators learn structure-level differences during message passing.
* No training: we do a pure forward pass. SAGE with mean aggregator is
  already a well-defined structural smoother even with random init weights,
  and the plan explicitly asks for *structural* embeddings rather than a
  task-trained model. Re-running with the same seed reproduces the exact
  same tensors, which is the acceptance-test property we care about.

The companion :func:`find_structural_loopholes` is pure Python — it uses
NetworkX for BFS and the same ``all-MiniLM-L6-v2`` sentence-transformer used
by :mod:`vitruvius.priming.context_vector`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from .contract import GraphSnapshot

if TYPE_CHECKING:  # pragma: no cover - type-only
    import networkx as _nx  # noqa: F401


# ---------------------------------------------------------------------------
# Stream HP.5.1 — GraphSAGE structural embeddings
# ---------------------------------------------------------------------------


_NODE_TYPE_VOCAB: tuple[str, ...] = (
    "concept",
    "clause",
    "ordinance",
    "law",
    "rule",
    "document",
    "entity",
)
"""Fixed small vocabulary of node ``type`` values used to build a one-hot
feature slice. Unknown types fall into a single catch-all bucket, which is
deterministic and stable across runs."""


_TRUST_LEVEL_SCORE: dict[str, float] = {
    "authoritative": 1.0,
    "verified": 0.75,
    "derived": 0.5,
    "provisional": 0.25,
    "unknown": 0.0,
}


_FEATURE_DIM: int = len(_NODE_TYPE_VOCAB) + 1  # one-hot type + trust scalar


@dataclass(frozen=True)
class GraphSAGEReport:
    """Result of :func:`compute_graphsage_embeddings`.

    ``embeddings`` maps ``GraphNode.id`` → a ``float32`` numpy array of
    shape ``(dim,)``. Empty snapshots return an empty dict but still
    report the requested ``dim`` so downstream callers can size their
    vector stores without special-casing.
    """

    embeddings: dict[str, np.ndarray]
    dim: int


def _build_feature_matrix(snapshot: GraphSnapshot) -> np.ndarray:
    """Construct a dense ``(num_nodes, _FEATURE_DIM)`` float32 matrix.

    Column layout:
      * columns 0 .. len(_NODE_TYPE_VOCAB)-1 : one-hot over known types
        (unknown types leave all type columns zero — deterministic and
        order-independent).
      * final column                        : numeric trust score.
    """
    num_nodes = len(snapshot.nodes)
    features = np.zeros((num_nodes, _FEATURE_DIM), dtype=np.float32)
    type_index = {name: i for i, name in enumerate(_NODE_TYPE_VOCAB)}
    for row, node in enumerate(snapshot.nodes):
        col = type_index.get(node.type)
        if col is not None:
            features[row, col] = 1.0
        features[row, -1] = float(
            _TRUST_LEVEL_SCORE.get(node.trust_level, 0.0)
        )
    return features


def _build_edge_index(
    snapshot: GraphSnapshot,
    id_to_row: dict[str, int],
) -> np.ndarray:
    """Build a ``(2, 2*E)`` int64 edge index suitable for torch_geometric.

    Each graph edge contributes *two* columns — one in each direction —
    so message passing is symmetric, which is what SAGE expects for
    undirected structural smoothing.
    """
    src: list[int] = []
    dst: list[int] = []
    for edge in snapshot.edges:
        u = id_to_row.get(edge.from_id)
        v = id_to_row.get(edge.to_id)
        if u is None or v is None:
            continue
        src.append(u)
        dst.append(v)
        src.append(v)
        dst.append(u)
    if not src:
        return np.zeros((2, 0), dtype=np.int64)
    return np.asarray([src, dst], dtype=np.int64)


def compute_graphsage_embeddings(
    snapshot: GraphSnapshot,
    *,
    dim: int = 64,
    num_layers: int = 2,
    random_state: int = 42,
) -> GraphSAGEReport:
    """Compute GraphSAGE-style structural embeddings for every node.

    Parameters
    ----------
    snapshot :
        The graph whose nodes we should embed.
    dim :
        Output embedding dimension. Each column of the final SAGE layer
        has ``dim`` features.
    num_layers :
        Number of SAGE convolution layers to stack. ``2`` is the plan
        default and gives nodes access to their 2-hop neighborhood. Must
        be ``>= 1``.
    random_state :
        Seed passed to ``torch``, ``numpy``, and ``random`` before the
        model is constructed. Reusing the same seed reproduces the exact
        same embeddings.

    Returns
    -------
    GraphSAGEReport
        Frozen dataclass with ``embeddings: dict[node_id, np.ndarray]``
        and the selected ``dim``. Empty snapshots yield an empty dict
        and the requested ``dim``.
    """
    if num_layers < 1:
        raise ValueError(
            f"num_layers must be >= 1, got {num_layers}"
        )
    if dim < 1:
        raise ValueError(f"dim must be >= 1, got {dim}")

    if not snapshot.nodes:
        return GraphSAGEReport(embeddings={}, dim=dim)

    # Lazy heavy imports — keep this module cheap to import.
    import random

    import torch  # type: ignore[import-not-found]
    from torch_geometric.nn import SAGEConv  # type: ignore[import-not-found]

    # Deterministic seeding across every RNG the model might touch.
    random.seed(random_state)
    np.random.seed(random_state)
    torch.manual_seed(random_state)
    if hasattr(torch, "use_deterministic_algorithms"):
        try:  # pragma: no cover - environment-dependent
            torch.use_deterministic_algorithms(True, warn_only=True)
        except Exception:  # pragma: no cover - best effort only
            pass

    id_to_row = {node.id: i for i, node in enumerate(snapshot.nodes)}

    features = _build_feature_matrix(snapshot)
    edge_index_np = _build_edge_index(snapshot, id_to_row)

    x = torch.from_numpy(features)
    edge_index = torch.from_numpy(edge_index_np).to(torch.long)

    in_dim = _FEATURE_DIM
    layers: list[SAGEConv] = []
    for layer_ix in range(num_layers):
        out_dim = dim
        layers.append(SAGEConv(in_dim, out_dim, aggr="mean"))
        in_dim = out_dim

    torch_module_list = torch.nn.ModuleList(layers)
    torch_module_list.eval()

    # Deterministic forward pass — no dropout, no training loop. The
    # plan wants structural smoothing, not a trained prediction head,
    # and the caller is free to fine-tune on top of these if they want.
    with torch.no_grad():
        h = x
        for i, conv in enumerate(torch_module_list):
            h = conv(h, edge_index)
            if i < len(torch_module_list) - 1:
                h = torch.nn.functional.relu(h)
        embeddings_np = h.detach().cpu().numpy().astype(np.float32)

    embeddings: dict[str, np.ndarray] = {}
    for node_id, row in id_to_row.items():
        embeddings[node_id] = np.ascontiguousarray(embeddings_np[row])
    return GraphSAGEReport(embeddings=embeddings, dim=dim)


# ---------------------------------------------------------------------------
# Stream HP.5.3 — Structural Loopholes Detector
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LoopholesReport:
    """Report from :func:`find_structural_loopholes`.

    Each entry in ``pairs`` is a tuple ``(node_a, node_b,
    semantic_similarity, topological_distance)`` describing a candidate
    hidden contradiction — two nodes that live far apart on the citation
    graph but whose supplied text descriptions are near-identical under
    sentence-transformer cosine similarity.

    The list is sorted by descending semantic similarity so the highest-
    confidence contradictions appear first. ``node_a`` and ``node_b`` are
    always ordered lexicographically so the same pair always serialises
    the same way regardless of iteration order.
    """

    pairs: list[tuple[str, str, float, int]]


def _to_undirected_networkx(snapshot: GraphSnapshot):
    """Build an undirected NetworkX graph from ``snapshot``.

    Lazy ``networkx`` import keeps module import cheap; identical pattern
    to :mod:`vitruvius.graph.community`.
    """
    import networkx as nx

    g: "_nx.Graph" = nx.Graph()
    for node in snapshot.nodes:
        g.add_node(node.id)
    for edge in snapshot.edges:
        g.add_edge(edge.from_id, edge.to_id)
    return g


def _cosine_similarity_matrix(
    vectors: np.ndarray,
) -> np.ndarray:
    """Row-wise cosine similarity on an already-L2-normalised matrix.

    ``sentence_transformers`` normalises when ``normalize_embeddings=True``
    so the cosine reduces to a matmul. We still defensively renormalise
    for numerical safety.
    """
    if vectors.size == 0:
        return np.zeros((0, 0), dtype=np.float32)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms = np.where(norms == 0.0, 1.0, norms)
    unit = vectors / norms
    return (unit @ unit.T).astype(np.float32)


def find_structural_loopholes(
    snapshot: GraphSnapshot,
    *,
    concept_text_by_id: dict[str, str],
    semantic_similarity_threshold: float = 0.80,
    topological_distance_min: int = 3,
    max_pairs: int = 50,
) -> LoopholesReport:
    """Find node pairs that are topologically distant but semantically similar.

    The "loophole" hypothesis: if two ordinances describe the same thing
    using nearly-identical language but the citation / governance graph
    never brings them within ``topological_distance_min`` hops of each
    other, they are candidate hidden contradictions that a text-search
    baseline would miss.

    Parameters
    ----------
    snapshot :
        The graph whose nodes we should search.
    concept_text_by_id :
        Mapping from ``GraphNode.id`` to the plain-text description used
        for semantic comparison. Nodes without a text entry are silently
        skipped — you can't compute cosine similarity without input.
    semantic_similarity_threshold :
        Minimum cosine similarity (inclusive) for a pair to count as a
        loophole. Default ``0.80`` matches the plan.
    topological_distance_min :
        Minimum BFS shortest-path length (inclusive) between the two
        nodes, in the undirected graph. Pairs in the same connected
        component but closer than this are ignored; pairs in different
        components are treated as infinite distance and always qualify.
        Default ``3`` matches the plan.
    max_pairs :
        Hard cap on returned pairs; we keep the top-K by descending
        semantic similarity.

    Returns
    -------
    LoopholesReport
        Frozen dataclass with the sorted pair list.
    """
    if semantic_similarity_threshold < 0.0 or semantic_similarity_threshold > 1.0:
        raise ValueError(
            f"semantic_similarity_threshold must be in [0, 1], "
            f"got {semantic_similarity_threshold}"
        )
    if topological_distance_min < 1:
        raise ValueError(
            f"topological_distance_min must be >= 1, got {topological_distance_min}"
        )
    if max_pairs < 1:
        raise ValueError(f"max_pairs must be >= 1, got {max_pairs}")

    # Only nodes both in the snapshot AND in concept_text_by_id are
    # eligible. Preserve snapshot order for determinism.
    snapshot_ids = {node.id for node in snapshot.nodes}
    eligible_ids: list[str] = [
        node.id
        for node in snapshot.nodes
        if node.id in concept_text_by_id and concept_text_by_id[node.id]
    ]
    if len(eligible_ids) < 2:
        return LoopholesReport(pairs=[])

    # Sentence-transformer — lazy import shared with context_vector.
    from sentence_transformers import SentenceTransformer  # type: ignore[import-not-found]

    # Reuse the same 384-dim model the rest of the pipeline uses.
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [concept_text_by_id[nid] for nid in eligible_ids]
    raw = embedder.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    vectors = np.asarray(raw, dtype=np.float32)
    sim = _cosine_similarity_matrix(vectors)

    # Build BFS index.
    import networkx as nx

    graph = _to_undirected_networkx(snapshot)
    # For each eligible node, compute shortest path lengths to every
    # other eligible node. Missing entries mean "different component"
    # and are treated as infinite distance (always >= min).
    bfs_cache: dict[str, dict[str, int]] = {}
    for nid in eligible_ids:
        if nid in snapshot_ids:
            # Use BFS single-source shortest-path lengths; unreachable
            # nodes are absent from the dict.
            bfs_cache[nid] = dict(
                nx.single_source_shortest_path_length(graph, nid)
            )
        else:  # pragma: no cover - eligible always in snapshot
            bfs_cache[nid] = {}

    INFINITE_DISTANCE = 10**6

    candidates: list[tuple[str, str, float, int]] = []
    num = len(eligible_ids)
    for i in range(num):
        a = eligible_ids[i]
        for j in range(i + 1, num):
            b = eligible_ids[j]
            score = float(sim[i, j])
            if score < semantic_similarity_threshold:
                continue
            dist_raw = bfs_cache[a].get(b, INFINITE_DISTANCE)
            if dist_raw < topological_distance_min:
                continue
            # Lexicographically order the pair so stable serialisation.
            lo, hi = (a, b) if a < b else (b, a)
            candidates.append((lo, hi, score, int(dist_raw)))

    # Deterministic ordering: primary by descending similarity, secondary
    # by ascending (lo, hi) pair.
    candidates.sort(key=lambda item: (-item[2], item[0], item[1]))
    return LoopholesReport(pairs=candidates[:max_pairs])
