from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from .contract import GraphSnapshot


class InsufficientJurisdictionsError(ValueError):
    """Raised when the snapshot has fewer than MIN_JURISDICTIONS distinct
    jurisdictions. Tensor factorisation is meaningless otherwise."""


MIN_JURISDICTIONS = 2


@dataclass(frozen=True)
class TensorFactorisationReport:
    n_jurisdictions: int
    tensor_shape: tuple[int, int, int, int]
    singular_values: tuple[float, ...]
    explained_variance_ratio: tuple[float, ...]


def _infer_jurisdiction(evidence_id: str) -> str:
    # Stopgap until Stream K: all current rel-* IDs are treated as national.
    return "national"


def factorise_snapshot(
    snapshot: GraphSnapshot,
    *,
    top_k: int = 16,
    classifier: Callable[[str], str] = _infer_jurisdiction,
) -> TensorFactorisationReport:
    all_node_ids = sorted({n.id for n in snapshot.nodes})
    subjects = all_node_ids
    objects = all_node_ids
    predicates = sorted({e.type for e in snapshot.edges})
    jurisdictions = sorted({classifier(e.evidence_id) for e in snapshot.edges})

    if len(jurisdictions) < MIN_JURISDICTIONS:
        raise InsufficientJurisdictionsError(
            f"tensor factorisation requires at least {MIN_JURISDICTIONS} "
            f"jurisdictions; got {len(jurisdictions)}"
        )

    subj_idx = {s: i for i, s in enumerate(subjects)}
    pred_idx = {p: i for i, p in enumerate(predicates)}
    obj_idx = {o: i for i, o in enumerate(objects)}
    jur_idx = {j: i for i, j in enumerate(jurisdictions)}

    shape = (len(subjects), len(predicates), len(objects), len(jurisdictions))
    tensor = np.zeros(shape, dtype=float)
    for edge in snapshot.edges:
        tensor[
            subj_idx[edge.from_id],
            pred_idx[edge.type],
            obj_idx[edge.to_id],
            jur_idx[classifier(edge.evidence_id)],
        ] += 1.0

    # Mode-1 unfolding: flatten modes 2..4 into one column dimension.
    mode1 = tensor.reshape(shape[0], -1)
    singular = np.linalg.svd(mode1, compute_uv=False)

    k = min(top_k, singular.shape[0])
    top = singular[:k]
    total = float(np.sum(top * top))
    if total <= 0.0:
        ratios = tuple(0.0 for _ in top)
    else:
        ratios = tuple(float(v * v / total) for v in top)

    return TensorFactorisationReport(
        n_jurisdictions=len(jurisdictions),
        tensor_shape=shape,
        singular_values=tuple(float(v) for v in top),
        explained_variance_ratio=ratios,
    )
