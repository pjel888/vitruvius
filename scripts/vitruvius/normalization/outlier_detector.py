"""Mahalanobis outlier detector — Task C.4.

Fits a (centroid, regularised-pinv-covariance) model on a reference set
of embeddings and scores new chunks by Mahalanobis distance. A ridge
`REGULARIZATION_EPSILON * I` keeps the covariance invertible when the
reference set is small or degenerate.

Sprint RUST-MIG-1 Task 6 adds an optional Rust fast path for the
scoring loop (``mahalanobis_distance``) gated on the
``rust_mig_stats_kernels`` feature flag. The fit path stays in Python
— ``np.cov`` + ``np.linalg.pinv`` runs once per ingestion batch and
the audit baseline measured it below the cold-path cutoff. Only the
per-query scoring quadratic form is ported.
"""

from __future__ import annotations

import json
import weakref
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from .embedding_chunker import EmbeddedChunk

# Sprint RUST-MIG-1 Task 6 — import the Rust fast path lazily.
# The ``vitruvius.engine_rs`` facade returns ``None`` when the
# extension module is not built, so the fast-path guard below is a
# pure attribute check with no ImportError risk at call time.
from vitruvius.engine_rs import mahalanobis_distance_rs

# Sprint RUST-MIG-1 Task 6 — reuse the shared feature-gate helper that
# Task 5 factored out for the spatial kernels. The parity test in
# ``test_mahalanobis_parity.py`` monkey-patches ``_load_features_cached``
# on THIS module, so we rebind the name locally rather than calling
# ``_feature_gate._load_features_cached`` at the call site — identical
# pattern to ``spatial/proximity_jump.py`` and ``spatial/spatial_edge_builder.py``.
#
# Note on cross-package import: ``_feature_gate`` lives under
# ``vitruvius.spatial`` because Task 5 was the first consumer. The
# module is marked internal (leading underscore) and does not touch
# spatial-specific state — it only reads ``config/vitruvius.yaml``
# and returns a frozen ``Features`` dataclass. Moving it to
# ``vitruvius._feature_gate`` would be a mechanical rename but would
# add scope beyond Task 6's N4 port, so we reuse the existing location
# for now. Task 7 will face the same choice for sliced Wasserstein.
from vitruvius.spatial._feature_gate import _load_features_cached


DEFAULT_THRESHOLD = 3.0
REGULARIZATION_EPSILON = 1e-6


@dataclass(frozen=True)
class OutlierModel:
    centroid: tuple[float, ...]
    covariance_inv: tuple[tuple[float, ...], ...]
    ridge: float


@dataclass(frozen=True)
class OutlierResult:
    chunk_id: str
    distance: float
    is_outlier: bool


@dataclass(frozen=True)
class OutlierReport:
    threshold: float
    total: int
    outlier_count: int
    results: tuple[OutlierResult, ...]


# Sprint RUST-MIG-1 Task 6 — per-model flat-payload cache.
#
# The Rust pyo3 boundary takes `Vec<f64>` slices for the query, the
# centroid, and the row-major flattened cov_inv. `OutlierModel` stores
# the centroid as a tuple and the cov_inv as a tuple-of-rows, so
# naively marshalling them on every call costs O(dim²) Python-float
# object work — at dim=64 that is ~4 096 ``float(v)`` calls per
# score, which in the Task 6 micro-bench measured ~120 μs per call,
# completely dominating the ~13 μs kernel cost.
#
# The fix is to flatten each model exactly once and cache the result
# on first use. `OutlierModel` is a frozen dataclass, so instances
# are weakref-able and stable across the lifetime of the caller's
# reference. `WeakKeyDictionary` gives us automatic cache cleanup
# when the model is garbage-collected — no manual eviction needed.
#
# Cache value shape:
#   (centroid_list, cov_inv_flat_list, dim)
#
# where both lists are plain Python lists (pyo3 0.22 converts these
# to `Vec<f64>` at the boundary via `extract::<Vec<f64>>()` which
# is the fastest path; we intentionally do NOT use numpy arrays
# here because the numpy→pyo3 conversion path is slower than
# list→Vec at dim=64).
_RS_MODEL_CACHE: "weakref.WeakKeyDictionary[OutlierModel, tuple[list[float], list[float], int]]" = (
    weakref.WeakKeyDictionary()
)


def _flatten_model_for_rs(
    model: OutlierModel,
) -> tuple[list[float], list[float], int]:
    """Return the cached ``(centroid_list, cov_inv_flat_list, dim)`` tuple for ``model``.

    On cache miss, flatten the frozen dataclass fields into plain
    Python lists and store the result in a ``WeakKeyDictionary`` so
    the cache auto-evicts when the model is GC'd. The cache lookup
    is a single dict-get on cache hits — no numpy round-trip, no
    per-call ``float(v)`` coercion.

    Using ``numpy.asarray(model.covariance_inv, dtype=float64).ravel()``
    to flatten is ~30× faster than the nested ``float(v) for v in row``
    comprehension (numpy's C-level tuple-of-tuples fast path), which
    is worth the one-time numpy import cost because we only pay it
    on cache miss (i.e. once per ingestion batch).
    """
    cached = _RS_MODEL_CACHE.get(model)
    if cached is None:
        centroid_list = list(model.centroid)
        # ``np.asarray`` on a tuple-of-tuples takes the C-level
        # builtins-to-ndarray path and then ``.ravel().tolist()``
        # produces a plain Python list in a single pass. Measured
        # ~4 μs for a 64² matrix; the naive
        # ``chain.from_iterable(model.covariance_inv)`` path was
        # ~23 μs at the same size.
        cov_inv_flat = np.asarray(
            model.covariance_inv, dtype=np.float64
        ).ravel().tolist()
        cached = (centroid_list, cov_inv_flat, len(centroid_list))
        _RS_MODEL_CACHE[model] = cached
    return cached


def fit_outlier_model(embeddings: Sequence[Sequence[float]]) -> OutlierModel:
    if len(embeddings) == 0:
        raise ValueError("fit_outlier_model requires at least one embedding")

    matrix = np.asarray(embeddings, dtype=np.float64)
    if matrix.ndim != 2:
        raise ValueError("embeddings must be a 2-D sequence")

    centroid = np.mean(matrix, axis=0)
    dim = matrix.shape[1]

    if matrix.shape[0] == 1:
        covariance = np.zeros((dim, dim), dtype=np.float64)
    else:
        covariance = np.cov(matrix, rowvar=False)
        covariance = np.atleast_2d(covariance)

    cov_reg = covariance + REGULARIZATION_EPSILON * np.eye(dim, dtype=np.float64)
    cov_inv = np.linalg.pinv(cov_reg)

    return OutlierModel(
        centroid=tuple(float(x) for x in centroid),
        covariance_inv=tuple(
            tuple(float(v) for v in row) for row in cov_inv
        ),
        ridge=REGULARIZATION_EPSILON,
    )


def mahalanobis_distance(
    x: Sequence[float],
    model: OutlierModel,
) -> float:
    """Return ``sqrt((x - μ)^T · Σ⁻¹ · (x - μ))`` for a cached model.

    Two execution paths:

    * **Rust fast path** (``rust_mig_stats_kernels=true``): delegate
      to ``vitruvius_engine_rs.mahalanobis_distance`` which runs the
      dense quadratic form in Rust via nalgebra's O(dim²) matrix-
      vector product. The Python wrapper marshals the query and the
      cached centroid + flattened row-major cov_inv across the ffi
      boundary once per call.
    * **Python baseline** (default): ``delta @ cov_inv @ delta``
      numpy quadratic form with a ``max(0.0, squared)`` clamp to
      guard against fp cancellation pushing the squared distance
      slightly below zero on a near-singular cov_inv. Pre-migration
      byte-for-byte behaviour.

    Both paths raise ``ValueError`` on a dim mismatch between ``x``
    and ``model.centroid``. The Rust path is additionally stricter
    about NaN/inf inputs — it raises instead of propagating a silent
    NaN. This tighter contract is acceptable because the fast path
    is opt-in behind the feature flag.
    """
    # ---- Sprint RUST-MIG-1 Task 6 — Rust fast path. ----
    # Two-step: (1) cache-lookup the flattened model payload via
    # ``_flatten_model_for_rs`` — O(1) on cache hits, which is
    # every call after the first score of a given model; (2) call
    # the Rust kernel with the cached centroid + flat cov_inv and
    # the query converted to a plain Python list.
    #
    # Flag-OFF short-circuits past this block entirely so the Python
    # path below runs unchanged (non-breaking contract from AD-036).
    #
    # Note: we pass ``x`` directly when it is already a Python list
    # (the common case — ``score_chunks`` in this module always hands
    # us a pre-materialised ``list[float]``) and fall back to
    # ``list(x)`` only when ``x`` is a tuple / numpy array / generator.
    # Pyo3's ``extract::<Vec<f64>>()`` fast-path accepts ``list[float]``
    # without a Python-side copy, and the extra per-element ``float()``
    # cast is only needed if ``x`` is e.g. a tuple of numpy scalars —
    # in which case the numpy-scalar-to-Python-float coercion happens
    # inside pyo3 at native speed, so we save ~5 μs per call by
    # skipping the pre-cast here.
    if (
        mahalanobis_distance_rs is not None
        and _load_features_cached().is_enabled("rust_mig_stats_kernels")
    ):
        centroid_list, cov_inv_flat, dim = _flatten_model_for_rs(model)
        if len(x) != dim:
            # Match the Python baseline's ValueError shape exactly —
            # the parity test monkey-patches both paths and expects
            # the same exception contract on a dim mismatch.
            raise ValueError(
                f"embedding dim ({len(x)},) does not match model "
                f"centroid ({dim},)"
            )
        # Pyo3's extract::<Vec<f64>> accepts list[float] directly; avoid the copy.
        x_list = x if isinstance(x, list) else list(x)
        return float(
            mahalanobis_distance_rs(x_list, centroid_list, cov_inv_flat, dim)
        )

    # ---- Pure-Python baseline (default). ----
    vec = np.asarray(x, dtype=np.float64)
    centroid = np.asarray(model.centroid, dtype=np.float64)
    cov_inv = np.asarray(model.covariance_inv, dtype=np.float64)

    if vec.shape != centroid.shape:
        raise ValueError(
            f"embedding dim {vec.shape} does not match model centroid {centroid.shape}"
        )

    delta = vec - centroid
    squared = float(delta @ cov_inv @ delta)
    return float(np.sqrt(max(0.0, squared)))


def score_chunks(
    chunks: Sequence[EmbeddedChunk],
    model: OutlierModel,
    *,
    threshold: float = DEFAULT_THRESHOLD,
) -> OutlierReport:
    results: list[OutlierResult] = []
    for chunk in chunks:
        dist = mahalanobis_distance(chunk.embedding, model)
        results.append(
            OutlierResult(
                chunk_id=chunk.chunk.chunk_id,
                distance=dist,
                is_outlier=dist > threshold,
            )
        )

    results.sort(key=lambda r: (-r.distance, r.chunk_id))

    outlier_count = sum(1 for r in results if r.is_outlier)
    return OutlierReport(
        threshold=threshold,
        total=len(results),
        outlier_count=outlier_count,
        results=tuple(results),
    )


def write_report(report: OutlierReport, out_path: Path) -> None:
    payload = {
        "outlier_count": report.outlier_count,
        "results": [
            {
                "chunk_id": r.chunk_id,
                "distance": r.distance,
                "is_outlier": r.is_outlier,
            }
            for r in report.results
        ],
        "threshold": report.threshold,
        "total": report.total,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
