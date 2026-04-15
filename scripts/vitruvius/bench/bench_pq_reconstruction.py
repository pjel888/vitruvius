"""Sprint PQ-1 Task 6 — Reconstruction-error benchmark for PQ embeddings.

Builds a synthetic ``GraphSnapshot`` modelled after the GraphSAGE test
fixture, runs :func:`compute_graphsage_embeddings` to get real 64-d
float32 vectors, compresses them via :func:`compress_graphsage_report`,
and reports:

* original byte size (N * 64 * 4)
* PQ byte size (N * M)
* compression ratio
* average L2 reconstruction error per node
* average **cosine similarity delta** vs the original (downstream
  loopholes-detector tolerance gate)

Writes ``.ai/10_state/bench_pq_reconstruction_2026-04-15.json`` as an
evidence artifact.

Rust Line: every operation here is a numpy primitive or an existing
GraphSAGE call. Pure orchestration. Python.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from vitruvius.graph.contract import GraphEdge, GraphNode, GraphSnapshot
from vitruvius.graph.graphsage import (
    GraphSAGEReport,
    compute_graphsage_embeddings,
)
from vitruvius.graph.graphsage_pq import compress_graphsage_report
from vitruvius.graph.pq_codebook import PQCodebook, decode_from_pq


REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = REPO_ROOT / ".ai" / "10_state" / "bench_pq_reconstruction_2026-04-15.json"


def _make_node(id_: str, type_: str = "concept") -> GraphNode:
    return GraphNode(
        id=id_,
        type=type_,
        slug=id_.split("-", 1)[-1] or "x",
        trust_level="derived",
        last_updated_utc="2026-04-14T00:00:00Z",
    )


def _make_edge(from_id: str, to_id: str, evidence: str) -> GraphEdge:
    return GraphEdge(
        from_id=from_id,
        to_id=to_id,
        type="governs",
        evidence_id=evidence,
        status="verified",
    )


def _build_synthetic_snapshot(num_nodes: int = 500, seed: int = 0) -> GraphSnapshot:
    """Construct a connected synthetic snapshot with ``num_nodes`` nodes.

    Each node has 2-4 outgoing edges drawn from a deterministic RNG,
    forming a sparse graph reminiscent of the production knowledge
    graph topology.
    """
    rng = np.random.default_rng(seed=seed)
    types = ("concept", "rule", "term")
    nodes = [_make_node(f"node-{i:04d}", types[i % len(types)]) for i in range(num_nodes)]
    edges: list[GraphEdge] = []
    for i in range(num_nodes):
        # Each node points to 2-4 others (deterministic).
        deg = int(rng.integers(2, 5))
        targets = rng.choice(num_nodes, size=deg, replace=False)
        for j, t in enumerate(targets):
            if int(t) == i:
                continue
            edges.append(
                _make_edge(
                    nodes[i].id,
                    nodes[int(t)].id,
                    f"ev-{i:04d}-{j}",
                )
            )
    return GraphSnapshot(
        schema_version="1.0.0",
        generated_at_utc="2026-04-14T00:00:00Z",
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


def _reconstruction_metrics(
    original: np.ndarray,
    reconstructed: np.ndarray,
) -> tuple[float, float, float]:
    """Return ``(avg_rel_l2, avg_cosine_sim, avg_cosine_delta)``.

    ``avg_cosine_delta`` is the mean of ``1 - cos(orig_i, recon_i)``
    across all rows — the gate the plan defines for downstream
    loopholes-detector tolerance (target <= 0.02).
    """
    diff_norms = np.linalg.norm(original - reconstructed, axis=1)
    orig_norms = np.linalg.norm(original, axis=1)
    avg_rel_l2 = float((diff_norms / np.maximum(orig_norms, 1e-8)).mean())

    recon_norms = np.linalg.norm(reconstructed, axis=1)
    denom = np.maximum(orig_norms * recon_norms, 1e-12)
    cos_sim = np.sum(original * reconstructed, axis=1) / denom
    avg_cos_sim = float(cos_sim.mean())
    avg_cos_delta = float((1.0 - cos_sim).mean())
    return avg_rel_l2, avg_cos_sim, avg_cos_delta


def run_bench(
    num_nodes: int = 500,
    M: int = 8,
    k: int = 256,
    n_iter: int = 25,
    seed: int = 42,
) -> dict:
    """Run the benchmark and return a JSON-serialisable result dict."""
    snapshot = _build_synthetic_snapshot(num_nodes=num_nodes, seed=0)
    report: GraphSAGEReport = compute_graphsage_embeddings(
        snapshot, dim=64, num_layers=2, random_state=seed
    )
    n = len(report.embeddings)
    if n == 0:
        raise RuntimeError("synthetic snapshot produced zero embeddings")

    codebook, codes, node_ids = compress_graphsage_report(
        report, M=M, k=k, n_iter=n_iter, seed=seed
    )
    assert isinstance(codebook, PQCodebook)

    stacked = np.stack([report.embeddings[nid] for nid in node_ids], axis=0)
    reconstructed = decode_from_pq(codes, codebook)

    avg_rel_l2, avg_cos_sim, avg_cos_delta = _reconstruction_metrics(
        stacked, reconstructed
    )

    original_bytes = n * 64 * 4  # float32
    pq_bytes = n * M  # uint8 per sub-quantizer
    ratio = original_bytes / pq_bytes if pq_bytes else 0.0

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sprint": "Sprint PQ-1",
        "task": "Task 6 — reconstruction benchmark",
        "config": {
            "num_nodes": n,
            "embedding_dim": 64,
            "M": M,
            "k": k,
            "n_iter": n_iter,
            "seed": seed,
        },
        "compression": {
            "original_bytes_total": original_bytes,
            "pq_bytes_total": pq_bytes,
            "original_bytes_per_node": 64 * 4,
            "pq_bytes_per_node": M,
            "ratio": ratio,
        },
        "quality": {
            "avg_relative_l2_error": avg_rel_l2,
            "avg_cosine_similarity": avg_cos_sim,
            "avg_cosine_delta": avg_cos_delta,
            "cosine_delta_target": 0.02,
            "cosine_delta_within_tolerance": avg_cos_delta <= 0.02,
        },
    }


def main() -> int:
    result = run_bench()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
