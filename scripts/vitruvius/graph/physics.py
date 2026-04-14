"""Sprint PHYS — Statistical mechanics / graph physics overlays.

Every helper here is additive to the Phase 8 GraphSnapshot contract
and gated behind the corresponding ``features.phys_*`` flag in live
callers. The module itself is importable under any configuration — the
flag check lives at the call site.

Stream PHYS.1 — PageRank statutory authority engine
Stream PHYS.2 — System energy / Boltzmann promotion gate / VF2 motif
                matcher (the last one absorbs the orphan Stream O task
                from the statistical-architectural-upgrade per governing
                plan §4.4).
Stream PHYS.3 — Shannon entropy adaptive sampler + Kolmogorov delta
                dedup for similar-text ordinance pairs.
Stream PHYS.4 — Eigenvector centrality + cascade simulator +
                impact-radius finder.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import networkx as nx
from networkx.algorithms import isomorphism

from .contract import GraphEdge, GraphNode, GraphSnapshot


# ---------------------------------------------------------------------------
# Stream PHYS.1 — PageRank Statutory Authority
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PageRankReport:
    """Ranking snapshot produced by :func:`compute_pagerank`.

    ``scores`` maps node id → PageRank score. ``alpha`` is the damping
    factor used. Scores always sum to ~1.0 (within numerical noise) when
    the snapshot is non-empty.
    """

    scores: dict[str, float]
    alpha: float


def _build_directed_graph(snapshot: GraphSnapshot) -> nx.DiGraph:
    """Collapse parallel edges by summing their weights.

    ``GraphSnapshot.edges`` is a list where the same ``(from_id, to_id)``
    pair can appear multiple times under different evidence ids. A
    simple ``DiGraph`` would overwrite the weight each time, losing
    the citation-count signal. We instead start each pair at weight 0
    and increment by 1 per edge so the PageRank computation sees the
    true citation multiplicity.
    """
    graph: nx.DiGraph = nx.DiGraph()
    for node in snapshot.nodes:
        graph.add_node(node.id)
    for edge in snapshot.edges:
        if graph.has_edge(edge.from_id, edge.to_id):
            graph[edge.from_id][edge.to_id]["weight"] += 1.0
        else:
            graph.add_edge(edge.from_id, edge.to_id, weight=1.0)
    return graph


def compute_pagerank(
    snapshot: GraphSnapshot,
    *,
    alpha: float = 0.85,
    max_iter: int = 200,
    tol: float = 1.0e-8,
) -> PageRankReport:
    """Compute PageRank over every node in ``snapshot``.

    Empty snapshots return an empty-scores report without calling
    NetworkX. For non-empty snapshots the directed edges define the
    citation topology: an edge ``A → B`` means "A cites B", so B
    accumulates authority from A's weight. The default damping factor
    ``alpha=0.85`` matches Brin-Page and is the same default NetworkX
    uses.
    """
    if not snapshot.nodes:
        return PageRankReport(scores={}, alpha=alpha)

    graph = _build_directed_graph(snapshot)
    raw = nx.pagerank(graph, alpha=alpha, max_iter=max_iter, tol=tol)
    # Preserve deterministic ordering by node id so callers can rely on
    # dict iteration yielding the same order each run.
    scores = {node_id: float(raw.get(node_id, 0.0)) for node_id in sorted(raw)}
    return PageRankReport(scores=scores, alpha=alpha)


def resolve_conflict_by_pagerank(
    snapshot: GraphSnapshot,
    *,
    node_a: str,
    node_b: str,
    alpha: float = 0.85,
) -> str:
    """Return whichever of ``node_a`` / ``node_b`` has the higher
    PageRank score in ``snapshot``.

    Ties break deterministically on node id (alphabetical first). The
    caller is responsible for checking ``features.phys_pagerank`` — the
    function itself is pure.
    """
    report = compute_pagerank(snapshot, alpha=alpha)
    score_a = report.scores.get(node_a, 0.0)
    score_b = report.scores.get(node_b, 0.0)
    if score_a > score_b:
        return node_a
    if score_b > score_a:
        return node_b
    return min(node_a, node_b)


# ---------------------------------------------------------------------------
# Stream PHYS.2 — System Energy + Boltzmann Gate + VF2 Motif Matcher
#
# PHYS.2 absorbs the orphan Stream O tasks (VF2 motif matcher +
# Boltzmann promotion gate) from the statistical-architectural-upgrade
# plan per governing plan §4.4.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SystemEnergy:
    """Aggregate measurement of "how much is unresolved" in a snapshot.

    Higher energy = more unresolved contradictions and unverified
    claims; the caller feeds this into
    :func:`should_promote_boltzmann` to decide whether to promote new
    edges or freeze the gate.
    """

    energy: float
    unresolved_edge_count: int
    unverified_node_count: int


def compute_system_energy(snapshot: GraphSnapshot) -> SystemEnergy:
    """Compute the scalar "energy" of a graph snapshot.

    Contributions:
      * Every edge with ``status`` other than ``"verified"`` /
        ``"spatially_verified"`` adds 1.0 to the energy.
      * Every node with ``trust_level == "unverified"`` adds 0.5
        (nodes weigh less than edges because a node without an
        attached relationship is cheap to either verify or discard).
    """
    unresolved_edges = sum(
        1
        for edge in snapshot.edges
        if edge.status not in {"verified", "spatially_verified"}
    )
    unverified_nodes = sum(
        1 for node in snapshot.nodes if node.trust_level == "unverified"
    )
    energy = float(unresolved_edges) + 0.5 * float(unverified_nodes)
    return SystemEnergy(
        energy=energy,
        unresolved_edge_count=unresolved_edges,
        unverified_node_count=unverified_nodes,
    )


@dataclass(frozen=True)
class BoltzmannVerdict:
    probability: float
    promote: bool


def should_promote_boltzmann(
    *,
    energy: float,
    temperature: float,
    boltzmann_k: float = 1.0,
    promotion_threshold: float = 0.5,
) -> BoltzmannVerdict:
    """Return a Boltzmann-distribution promotion verdict.

    Uses ``P(s) = exp(-E / (k*T))`` with ``k*T`` the thermal energy. A
    zero-temperature system is a hard gate: any positive energy state
    has probability 0, so only ``energy == 0`` can promote.

    A state "promotes" when its Boltzmann probability is at least
    ``promotion_threshold`` (default 0.5). Callers can raise the
    threshold for "cryogenic consistency" mode or lower it for
    exploratory runs.
    """
    if temperature <= 0.0:
        probability = 1.0 if energy == 0.0 else 0.0
    else:
        probability = math.exp(-energy / (boltzmann_k * temperature))
    return BoltzmannVerdict(
        probability=float(probability),
        promote=bool(probability >= promotion_threshold),
    )


# ---------------------------------------------------------------------------
# Stream PHYS.4 — Eigenvector centrality + cascade simulator + impact radius
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EigenvectorReport:
    scores: dict[str, float]


def compute_eigenvector_centrality(
    snapshot: GraphSnapshot,
    *,
    max_iter: int = 200,
    tol: float = 1.0e-6,
) -> EigenvectorReport:
    """Compute eigenvector centrality over ``snapshot``.

    Returns an empty report for empty snapshots. Falls back to
    ``nx.eigenvector_centrality_numpy`` if the power-iteration method
    fails to converge (NetworkX raises PowerIterationFailedConvergence).
    """
    if not snapshot.nodes:
        return EigenvectorReport(scores={})

    graph = _build_directed_graph(snapshot)
    try:
        raw = nx.eigenvector_centrality(
            graph,
            max_iter=max_iter,
            tol=tol,
            weight="weight",
        )
    except nx.PowerIterationFailedConvergence:
        raw = nx.eigenvector_centrality_numpy(graph, weight="weight")
    scores = {node_id: float(raw.get(node_id, 0.0)) for node_id in sorted(raw)}
    return EigenvectorReport(scores=scores)


@dataclass(frozen=True)
class CascadeReport:
    focal_node: str
    affected_nodes: set[str]
    affected_fraction: float


def simulate_cascade(
    snapshot: GraphSnapshot,
    *,
    focal_node: str,
) -> CascadeReport:
    """Simulate a "what breaks if ``focal_node`` changes" sweep.

    Returns the set of nodes structurally connected to ``focal_node``
    in the undirected projection of the graph, plus that set's size as
    a fraction of the total node count. An isolated focal node
    returns just itself.
    """
    if not snapshot.nodes:
        return CascadeReport(
            focal_node=focal_node,
            affected_nodes=set(),
            affected_fraction=0.0,
        )

    graph = _build_directed_graph(snapshot).to_undirected()
    if focal_node not in graph:
        return CascadeReport(
            focal_node=focal_node,
            affected_nodes=set(),
            affected_fraction=0.0,
        )

    affected = set(nx.node_connected_component(graph, focal_node))
    fraction = float(len(affected)) / float(len(snapshot.nodes))
    return CascadeReport(
        focal_node=focal_node,
        affected_nodes=affected,
        affected_fraction=fraction,
    )


def find_impact_radius(
    snapshot: GraphSnapshot,
    *,
    focal_node: str,
    k: int,
) -> list[str]:
    """Return the top-``k`` most influential neighbors of ``focal_node``.

    Influence is measured by eigenvector centrality. The focal node is
    excluded from the returned list. When fewer than ``k`` non-focal
    nodes exist, returns all of them.
    """
    report = compute_eigenvector_centrality(snapshot)
    ranked = sorted(
        ((node_id, score) for node_id, score in report.scores.items() if node_id != focal_node),
        key=lambda kv: (-kv[1], kv[0]),
    )
    return [node_id for node_id, _ in ranked[:k]]


# ---------------------------------------------------------------------------
# Stream PHYS.3 — Shannon entropy adaptive sampler + Kolmogorov delta
# ---------------------------------------------------------------------------


def compute_shannon_entropy(text: str) -> float:
    """Compute the Shannon entropy (bits per symbol) of a text block.

    Uses character-level frequencies so the entropy of a string of
    N equiprobable symbols is ``log2(N)``. Empty strings return 0.0.
    """
    if not text:
        return 0.0
    from collections import Counter

    counts = Counter(text)
    total = float(sum(counts.values()))
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return float(entropy)


def adaptive_window_overlap(
    *,
    entropy: float,
    window_size: int,
    min_overlap: int,
    max_overlap: int,
) -> int:
    """Pick a window overlap from the text's Shannon entropy.

    Nyquist-Shannon intuition: high-entropy sections need a finer
    sampling rate (= more overlap between successive chunks) so
    information on the boundary is not lost. Low-entropy sections
    (lots of repetition) can be sampled coarsely without losing
    signal.

    We linearly interpolate between ``min_overlap`` and ``max_overlap``
    over the entropy range ``[0, log2(256)] = [0, 8]`` — 256 is a
    reasonable upper bound on ASCII character variety in English text.
    The result is always clamped into the caller-specified bounds.
    """
    assert min_overlap <= max_overlap, "min_overlap must be <= max_overlap"
    assert window_size > 0, "window_size must be positive"

    # Normalise entropy into [0, 1] over the reasonable range.
    max_entropy = 8.0
    ratio = max(0.0, min(entropy, max_entropy)) / max_entropy
    span = float(max_overlap - min_overlap)
    scaled = int(round(min_overlap + ratio * span))
    return max(min_overlap, min(max_overlap, scaled))


@dataclass(frozen=True)
class KolmogorovDelta:
    edit_ratio: float
    is_near_duplicate: bool


def compute_kolmogorov_delta(
    base: str,
    modified: str,
    *,
    near_duplicate_threshold: float = 0.25,
) -> KolmogorovDelta:
    """Approximate the Kolmogorov complexity delta between two strings
    using :mod:`difflib`'s sequence ratio.

    True Kolmogorov complexity is uncomputable; the compression-based
    approximation we use here is small edit distance == "short
    description" of the modification. Specifically, we compute
    ``1 - SequenceMatcher.ratio()`` so identical inputs yield 0.0
    and maximally divergent inputs yield ~1.0.

    Any delta below ``near_duplicate_threshold`` (default 0.25) is
    flagged ``is_near_duplicate = True`` — the caller can then store
    the modified text as a delta-against-base rather than a full copy.
    """
    from difflib import SequenceMatcher

    if not base and not modified:
        return KolmogorovDelta(edit_ratio=0.0, is_near_duplicate=True)
    ratio = SequenceMatcher(None, base, modified).ratio()
    edit_ratio = 1.0 - ratio
    return KolmogorovDelta(
        edit_ratio=float(edit_ratio),
        is_near_duplicate=bool(edit_ratio <= near_duplicate_threshold),
    )


def find_violation_motifs(
    snapshot: GraphSnapshot,
    *,
    motif_nodes: list[str],
    motif_edges: list[tuple[str, str]],
) -> list[dict[str, str]]:
    """Stream PHYS.2 (orphan Stream O absorption) — VF2 subgraph
    isomorphism motif matcher.

    Given a tiny motif described by node names and directed edge
    tuples, returns every node-mapping ``{motif_node → snapshot_node_id}``
    that is isomorphic to the motif inside ``snapshot``. Uses the
    :mod:`networkx.algorithms.isomorphism` DiGraphMatcher VF2
    implementation.

    Returns an empty list when the motif is not found. The caller is
    responsible for interpreting matches as "violation" or "compliant"
    patterns; this function is purely structural.
    """
    host = _build_directed_graph(snapshot)

    pattern: nx.DiGraph = nx.DiGraph()
    for name in motif_nodes:
        pattern.add_node(name)
    for src, dst in motif_edges:
        pattern.add_edge(src, dst)

    matcher = isomorphism.DiGraphMatcher(host, pattern)
    matches: list[dict[str, str]] = []
    # subgraph_isomorphisms_iter yields dict[host_node → pattern_node].
    # We flip it so callers get {motif_node → snapshot_node_id}.
    for host_to_pattern in matcher.subgraph_isomorphisms_iter():
        matches.append(
            {pattern_name: host_name for host_name, pattern_name in host_to_pattern.items()}
        )
    return matches
