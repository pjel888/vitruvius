"""Stream D.4 — Contrastive whitening embedding adapter.

Linear PCA-based stand-in for LoRA fine-tuning (deferred — see
FUTURE-ML-01). Fits a variance-weighted orthogonal projection over
positive-pair difference vectors so that domain-aligned embeddings
shrink together while unrelated pairs keep order-of-magnitude distance.
Deterministic, serializable to JSON, CPU-only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from sklearn.decomposition import TruncatedSVD


DEFAULT_MAX_COMPONENTS = 64
REGULARIZATION_EPSILON = 1e-6
_SVD_RANDOM_STATE = 0


@dataclass
class ContrastiveAdapter:
    mean: np.ndarray | None = None
    components: np.ndarray | None = None
    singular_values: np.ndarray | None = None
    n_components: int = 0
    is_fitted: bool = False


def _coerce_pairs(
    positive_pairs: Sequence[tuple[Sequence[float], Sequence[float]]],
) -> tuple[np.ndarray, np.ndarray] | None:
    if not positive_pairs:
        return None
    left_rows: list[np.ndarray] = []
    right_rows: list[np.ndarray] = []
    for a, b in positive_pairs:
        left_rows.append(np.asarray(a, dtype=np.float64))
        right_rows.append(np.asarray(b, dtype=np.float64))
    left = np.stack(left_rows)
    right = np.stack(right_rows)
    if left.shape != right.shape or left.ndim != 2:
        return None
    return left, right


def fit_adapter(
    positive_pairs: Sequence[tuple[Sequence[float], Sequence[float]]],
    *,
    max_components: int = DEFAULT_MAX_COMPONENTS,
) -> ContrastiveAdapter:
    """Fit a whitening adapter on positive pairs of embeddings."""
    coerced = _coerce_pairs(positive_pairs)
    if coerced is None:
        return ContrastiveAdapter()
    left, right = coerced
    n_pairs, dim = left.shape
    n_components = min(max_components, n_pairs - 1, dim)
    if n_components < 1:
        return ContrastiveAdapter()

    mean = np.concatenate([left, right], axis=0).mean(axis=0)
    differences = left - right
    svd = TruncatedSVD(n_components=n_components, random_state=_SVD_RANDOM_STATE)
    svd.fit(differences)

    return ContrastiveAdapter(
        mean=mean,
        components=svd.components_.astype(np.float64),
        singular_values=svd.singular_values_.astype(np.float64),
        n_components=int(n_components),
        is_fitted=True,
    )


def transform(adapter: ContrastiveAdapter, x: Sequence[float]) -> np.ndarray:
    """Apply the adapter to a single embedding; passthrough when unfitted."""
    x_arr = np.asarray(x, dtype=np.float64)
    if not adapter.is_fitted:
        return x_arr
    if adapter.mean is None or adapter.components is None or adapter.singular_values is None:
        return x_arr
    centered = x_arr - adapter.mean
    s_max = float(adapter.singular_values.max())
    weights = adapter.singular_values / (s_max + REGULARIZATION_EPSILON)
    return (centered @ adapter.components.T) * weights


def save_adapter(adapter: ContrastiveAdapter, out_path: Path) -> None:
    """Serialize to JSON — mean as list[float], matrices as list[list[float]]."""
    payload: dict[str, object] = {
        "is_fitted": adapter.is_fitted,
        "n_components": adapter.n_components,
        "mean": adapter.mean.tolist() if adapter.mean is not None else None,
        "components": (
            adapter.components.tolist() if adapter.components is not None else None
        ),
        "singular_values": (
            adapter.singular_values.tolist() if adapter.singular_values is not None else None
        ),
    }
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def load_adapter(path: Path) -> ContrastiveAdapter:
    """Round-trip from save_adapter's JSON output."""
    raw = json.loads(path.read_text())
    mean_raw = raw.get("mean")
    components_raw = raw.get("components")
    singular_raw = raw.get("singular_values")
    return ContrastiveAdapter(
        mean=np.asarray(mean_raw, dtype=np.float64) if mean_raw is not None else None,
        components=(
            np.asarray(components_raw, dtype=np.float64) if components_raw is not None else None
        ),
        singular_values=(
            np.asarray(singular_raw, dtype=np.float64) if singular_raw is not None else None
        ),
        n_components=int(raw.get("n_components", 0)),
        is_fitted=bool(raw.get("is_fitted", False)),
    )
