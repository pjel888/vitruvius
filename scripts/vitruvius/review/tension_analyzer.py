"""Tension point analyzer — two-tier verdict disagreement detection (Task F.5)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


CONFIDENCE_DIFF_THRESHOLD = 0.3
CONFIDENCE_MATCH_EPSILON = 0.1


@dataclass(frozen=True)
class ReviewVerdict:
    model_name: str
    decision: str
    confidence: float
    reason: str


@dataclass(frozen=True)
class TensionPoint:
    candidate_id: str
    tier_one: ReviewVerdict
    tier_two: ReviewVerdict
    disagreement_type: str
    logged_at_utc: str


def detect_tension(
    *,
    candidate_id: str,
    tier_one: ReviewVerdict,
    tier_two: ReviewVerdict,
    now: datetime | None = None,
) -> TensionPoint | None:
    if now is None:
        now = datetime.now(timezone.utc)
    stamp = now.isoformat()

    if tier_one.decision != tier_two.decision:
        return TensionPoint(
            candidate_id=candidate_id,
            tier_one=tier_one,
            tier_two=tier_two,
            disagreement_type="decision",
            logged_at_utc=stamp,
        )

    conf_diff = abs(tier_one.confidence - tier_two.confidence)
    if conf_diff > CONFIDENCE_DIFF_THRESHOLD:
        return TensionPoint(
            candidate_id=candidate_id,
            tier_one=tier_one,
            tier_two=tier_two,
            disagreement_type="confidence",
            logged_at_utc=stamp,
        )

    # Decisions match and confidences within epsilon — reason_only is deferred
    return None


def _tension_to_json(tension: TensionPoint) -> str:
    payload = asdict(tension)
    return json.dumps(payload, sort_keys=True)


def append_tension_to_log(tension: TensionPoint, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    line = _tension_to_json(tension)
    with log_path.open("a") as handle:
        handle.write(line + "\n")


def _verdict_from_dict(payload: dict) -> ReviewVerdict:
    return ReviewVerdict(
        model_name=payload["model_name"],
        decision=payload["decision"],
        confidence=float(payload["confidence"]),
        reason=payload["reason"],
    )


def read_tension_log(log_path: Path) -> list[TensionPoint]:
    if not log_path.exists():
        return []
    results: list[TensionPoint] = []
    for raw_line in log_path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
            results.append(
                TensionPoint(
                    candidate_id=payload["candidate_id"],
                    tier_one=_verdict_from_dict(payload["tier_one"]),
                    tier_two=_verdict_from_dict(payload["tier_two"]),
                    disagreement_type=payload["disagreement_type"],
                    logged_at_utc=payload["logged_at_utc"],
                )
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            continue
    return results
