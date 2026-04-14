from __future__ import annotations

import hashlib
import re

from .utils import utc_now_stamp


_SLUG_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    value = value.lower()
    value = _SLUG_NON_ALNUM.sub("-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]


def build_relationship_id(from_entity: str, predicate: str, to_entity: str) -> str:
    slug = slugify(f"{from_entity}-{predicate}-{to_entity}")
    return f"rel-{slug}"


def build_promotion_batch_id() -> str:
    stamp = utc_now_stamp()
    return f"{stamp}_{short_hash(stamp)}"


def evidence_fingerprint(evidence_entry: dict) -> str:
    key = "|".join([
        str(evidence_entry.get("source_id", "")),
        str(evidence_entry.get("source_section_id", "")),
        short_hash(str(evidence_entry.get("evidence_snippet", ""))),
    ])
    return key


def merge_evidence(existing: list[dict], new: list[dict]) -> list[dict]:
    seen = {evidence_fingerprint(e): e for e in existing}
    for entry in new:
        fp = evidence_fingerprint(entry)
        if fp not in seen:
            seen[fp] = entry
    return list(seen.values())


def min_confidence(evidence: list[dict]) -> float:
    scores = [float(e.get("reviewer_confidence", 0.0)) for e in evidence]
    return min(scores) if scores else 0.0
