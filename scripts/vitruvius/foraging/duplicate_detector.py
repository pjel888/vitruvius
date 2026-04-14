"""Stream O.3 — SHA-256 content-hash duplicate detector stub.

Tiny helper that future foraging fetchers will call before committing
a newly downloaded document to the raw layer. When a hit is found
the caller should skip the download. Staying pure-hash (no
embeddings, no fuzzy match) keeps the check cheap and deterministic.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class DuplicateReport:
    is_duplicate: bool
    matched_path: Optional[Path]
    incoming_digest: str


def hash_document_content(content: bytes) -> str:
    """Return the hex SHA-256 digest of ``content``."""
    return hashlib.sha256(content).hexdigest()


def find_duplicate(
    incoming: bytes,
    corpus_paths: Iterable[Path],
) -> DuplicateReport:
    """Search ``corpus_paths`` for a file whose SHA-256 matches
    ``incoming``. Returns the first match (deterministic order is the
    caller's responsibility — pass a sorted list if determinism is
    required).
    """
    incoming_digest = hash_document_content(incoming)
    for path in corpus_paths:
        path = Path(path)
        if not path.is_file():
            continue
        existing_digest = hash_document_content(path.read_bytes())
        if existing_digest == incoming_digest:
            return DuplicateReport(
                is_duplicate=True,
                matched_path=path,
                incoming_digest=incoming_digest,
            )
    return DuplicateReport(
        is_duplicate=False,
        matched_path=None,
        incoming_digest=incoming_digest,
    )
