"""Sprint PQ-1 Task 5 — GraphSAGEReport → PQ compression helper.

One-call convenience that takes a :class:`GraphSAGEReport` from
:mod:`vitruvius.graph.graphsage`, trains a PQ codebook on its
embeddings, encodes each embedding to its compressed code, and returns
the deterministic ``(codebook, codes, node_ids)`` triple ready for
persistence by an upstream caller.

Rust Line: pure orchestration around already-native primitives in
:mod:`pq_codebook`. No new hot loops introduced. Python.
"""
from __future__ import annotations

from typing import Optional

import numpy as np

from vitruvius.graph.graphsage import GraphSAGEReport
from vitruvius.graph.pq_codebook import (
    PQCodebook,
    encode_to_pq,
    train_pq_codebook,
)


def compress_graphsage_report(
    report: GraphSAGEReport,
    *,
    M: int = 8,
    k: int = 256,
    n_iter: int = 25,
    seed: int = 0,
) -> tuple[Optional[PQCodebook], np.ndarray, list[str]]:
    """Train a PQ codebook on ``report.embeddings`` and encode them.

    Returns ``(codebook, codes, node_ids)`` where ``codes[i]`` is the
    PQ encoding of ``node_ids[i]``'s embedding. Empty reports return
    ``(None, empty_array, [])``.

    Node IDs are returned in sorted order so the codes array is
    deterministic regardless of dict insertion order.
    """
    if not report.embeddings:
        return None, np.zeros((0, M), dtype=np.uint8), []

    node_ids = sorted(report.embeddings.keys())
    stacked = np.stack(
        [report.embeddings[nid] for nid in node_ids],
        axis=0,
    ).astype(np.float32, copy=False)

    codebook = train_pq_codebook(
        stacked, M=M, k=k, n_iter=n_iter, seed=seed
    )
    codes = encode_to_pq(stacked, codebook)
    return codebook, codes, node_ids
