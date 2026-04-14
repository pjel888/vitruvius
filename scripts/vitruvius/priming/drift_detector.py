"""Stream Y1.3 — cosine-similarity drift check between a source-identity
vector and an LLM response vector.

Stream F's reflection_parser asks the model to self-report confidence.
This module adds an independent measurement: embed the model's
natural-language response with the same sentence-transformer used for
the source identity (see :mod:`vitruvius.priming.context_vector`),
then measure cosine similarity. If the response strays too far,
escalate to second-pass review.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .context_vector import SourceIdentity


@dataclass(frozen=True)
class DriftReport:
    cosine_similarity: float
    drift: float            # 1.0 − cosine
    vector_norm_response: float


def measure_drift(
    *,
    identity: SourceIdentity,
    response_vector: np.ndarray,
) -> DriftReport:
    """Compute cosine similarity and 1-minus-cosine drift between the
    identity vector and an embedding of the model's response.

    Both vectors should be L2-normalised; this function normalises
    ``response_vector`` defensively and records its pre-normalisation
    norm. A zero-norm response returns cosine=0, drift=1.
    """
    norm_r = float(np.linalg.norm(response_vector))
    if norm_r < 1e-9:
        return DriftReport(cosine_similarity=0.0, drift=1.0, vector_norm_response=0.0)
    r = response_vector / norm_r
    sim = float(np.dot(identity.vector, r))
    return DriftReport(
        cosine_similarity=sim,
        drift=1.0 - sim,
        vector_norm_response=norm_r,
    )


def is_drift_excessive(report: DriftReport, *, threshold_cosine: float) -> bool:
    """Return True when cosine similarity is strictly below
    ``threshold_cosine`` (i.e. drift is excessive and the caller
    should escalate).
    """
    return report.cosine_similarity < threshold_cosine
