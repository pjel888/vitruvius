"""Stream Y1.1 — deterministic source-identity vector builder.

Produces a :class:`SourceIdentity` record combining:
  * A stable SHA-256 fingerprint over
    ``(jurisdiction, document_type, issuing_body, issue_date, title)``.
  * A canonical plain-English prose summary of the frontmatter.
  * A 384-dim ``float32`` embedding of the prose + a short body preview
    (produced by the shared ``all-MiniLM-L6-v2`` SentenceTransformer
    loaded lazily on first call).

The vector is consumed by :mod:`vitruvius.priming.prompt_prefix` (Y1.2)
to prime LLM prompts and by :mod:`vitruvius.priming.drift_detector`
(Y1.3) to measure response drift.

Lazy loading: importing this module does NOT load ``sentence_transformers``.
The model is instantiated inside ``_get_embedder`` and cached across calls.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Mapping, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer  # noqa: F401

_EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
_EMBEDDING_DIM = 384

_EMBEDDER = None  # lazy singleton


def _get_embedder() -> "SentenceTransformer":
    global _EMBEDDER
    if _EMBEDDER is None:
        from sentence_transformers import SentenceTransformer

        _EMBEDDER = SentenceTransformer(_EMBEDDING_MODEL_NAME)
    return _EMBEDDER


@dataclass(frozen=True)
class SourceIdentity:
    fingerprint: str       # sha256 hex truncated to 16 chars
    prose: str             # canonical plain-English summary
    vector: np.ndarray     # float32 [384]


def identity_to_prose(identity: SourceIdentity) -> str:
    return identity.prose


def build_source_identity(
    frontmatter: Mapping[str, Any],
    *,
    text_preview: str,
) -> SourceIdentity:
    """Build a deterministic source-identity record for a document.

    Parameters
    ----------
    frontmatter :
        Parsed source-layer frontmatter. Expected keys: ``title``,
        ``jurisdiction``, ``document_type``, ``issuing_body``,
        ``issue_date``. Missing keys default to the empty string.
    text_preview :
        First few hundred characters of the body. Used to nudge the
        vector (so the same-metadata-different-body case still
        produces a responsive vector) but NOT included in the
        fingerprint — so a document whose body changes between
        versions stays keyed to the same identity.
    """
    title = str(frontmatter.get("title", "")).strip()
    jurisdiction = str(frontmatter.get("jurisdiction", "")).strip()
    doc_type = str(frontmatter.get("document_type", "")).strip()
    issuer = str(frontmatter.get("issuing_body", "")).strip()
    issue_date = str(frontmatter.get("issue_date", "")).strip()

    fp_material = "|".join([jurisdiction, doc_type, issuer, issue_date, title])
    fingerprint = hashlib.sha256(fp_material.encode("utf-8")).hexdigest()[:16]

    prose = (
        f"This document is '{title}', a {doc_type.replace('_', ' ')} "
        f"issued by {issuer} on {issue_date} under the jurisdiction of {jurisdiction}. "
        f"All legal logic must be interpreted within {jurisdiction}'s regulatory context."
    )

    embedder = _get_embedder()
    body_sample = (text_preview or "")[:512]
    vector = embedder.encode(
        [prose + " CONTEXT: " + body_sample],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )[0].astype(np.float32)

    return SourceIdentity(fingerprint=fingerprint, prose=prose, vector=vector)
