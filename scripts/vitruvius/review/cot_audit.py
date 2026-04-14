"""Stream Y3.2 — append-only CoT audit trail.

For every verdict that parses through :func:`parse_cot_strict`, the
caller writes a JSON trace via :func:`write_cot_trace`. Traces land
under ``005_Operational-Intelligence-Layer/cot_traces/`` by default;
filenames encode a UTC timestamp + relationship hash so the directory
is append-only, deterministic, and trivially diffable across runs.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .reflection_parser import CotResult


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:32]


def write_cot_trace(
    *,
    out_dir: Path,
    relationship_hash: str,
    cot: CotResult,
    model: str,
    candidate_raw_response: str,
) -> Path:
    """Write a single CoT trace and return the written path.

    The filename is ``<utc-timestamp>_<relationship_hash>.json``; the
    payload is a sorted-keys indent=2 JSON document with the verdict,
    self-confidence, reasoning steps, evidence citation, escalate
    flag, and an SHA-256 truncation of the raw LLM response for
    provenance.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    fname = f"{ts}_{relationship_hash}.json"
    path = out_dir / fname

    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "timestamp_utc": ts,
        "relationship_hash": relationship_hash,
        "model": model,
        "verdict": cot.verdict,
        "self_confidence": cot.self_confidence,
        "reasoning_steps": list(cot.reasoning_steps),
        "evidence_citation": cot.evidence_citation,
        "escalate": cot.escalate,
        "raw_response_sha256": _sha256(candidate_raw_response),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


@dataclass(frozen=True)
class CotAuditSummary:
    total: int
    verdict_counts: dict[str, int]
    mean_self_confidence: float

    @classmethod
    def from_directory(cls, directory: Path) -> "CotAuditSummary":
        """Walk ``directory`` and aggregate every CoT trace JSON found."""
        files = sorted(Path(directory).glob("*.json"))
        total = len(files)
        counts: dict[str, int] = {}
        confidences: list[float] = []
        for f in files:
            data = json.loads(f.read_text(encoding="utf-8"))
            v = str(data.get("verdict", "unknown"))
            counts[v] = counts.get(v, 0) + 1
            confidences.append(float(data.get("self_confidence", 0.0)))
        mean = sum(confidences) / total if total else 0.0
        return cls(total=total, verdict_counts=counts, mean_self_confidence=mean)
