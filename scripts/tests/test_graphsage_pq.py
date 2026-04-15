"""Sprint PQ-1 Task 5 — compress_graphsage_report integration tests."""
from __future__ import annotations

import numpy as np

from vitruvius.graph.graphsage import GraphSAGEReport
from vitruvius.graph.graphsage_pq import compress_graphsage_report
from vitruvius.graph.pq_codebook import PQCodebook


def test_compress_graphsage_report_shapes() -> None:
    rng = np.random.default_rng(seed=0)
    embeddings = {
        f"node-{i:03d}": rng.standard_normal(64).astype(np.float32)
        for i in range(200)
    }
    report = GraphSAGEReport(embeddings=embeddings, dim=64)

    codebook, codes, node_ids = compress_graphsage_report(
        report, M=8, k=32, n_iter=5, seed=42
    )

    assert isinstance(codebook, PQCodebook)
    assert codes.shape == (200, 8)
    assert codes.dtype == np.uint8
    assert len(node_ids) == 200
    # Order must be deterministic (sorted by node_id) so the codes[i]
    # always corresponds to node_ids[i].
    assert node_ids == sorted(node_ids)


def test_compress_graphsage_report_empty() -> None:
    report = GraphSAGEReport(embeddings={}, dim=64)
    codebook, codes, node_ids = compress_graphsage_report(
        report, M=8, k=32, n_iter=5, seed=42
    )
    assert codebook is None
    assert codes.shape == (0, 8)
    assert node_ids == []
