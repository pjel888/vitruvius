"""Tension point analyzer — disagreement detection and log handling (Task F.5)."""

from __future__ import annotations

import dataclasses
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from vitruvius.review.tension_analyzer import (
    ReviewVerdict,
    TensionPoint,
    append_tension_to_log,
    detect_tension,
    read_tension_log,
)


FIXED_NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def _verdict(model: str, decision: str, confidence: float, reason: str = "r") -> ReviewVerdict:
    return ReviewVerdict(model_name=model, decision=decision, confidence=confidence, reason=reason)


def test_decision_disagreement_detected():
    t1 = _verdict("gemma", "keep", 0.9)
    t2 = _verdict("qwen", "reject", 0.85)
    result = detect_tension(candidate_id="c1", tier_one=t1, tier_two=t2, now=FIXED_NOW)
    assert result is not None
    assert result.disagreement_type == "decision"
    assert result.candidate_id == "c1"


def test_confidence_disagreement_detected():
    t1 = _verdict("gemma", "keep", 0.95)
    t2 = _verdict("qwen", "keep", 0.5)
    result = detect_tension(candidate_id="c2", tier_one=t1, tier_two=t2, now=FIXED_NOW)
    assert result is not None
    assert result.disagreement_type == "confidence"


def test_no_disagreement_returns_none():
    t1 = _verdict("gemma", "keep", 0.9)
    t2 = _verdict("qwen", "keep", 0.88)
    result = detect_tension(candidate_id="c3", tier_one=t1, tier_two=t2, now=FIXED_NOW)
    assert result is None


def test_reason_only_difference_returns_none():
    t1 = _verdict("gemma", "keep", 0.9, reason="matches pattern A")
    t2 = _verdict("qwen", "keep", 0.92, reason="matches pattern B")
    # same decision, tiny confidence diff, only the reasons differ - return None for now
    result = detect_tension(candidate_id="c4", tier_one=t1, tier_two=t2, now=FIXED_NOW)
    assert result is None


def test_append_and_read_roundtrip(tmp_path: Path):
    log = tmp_path / "tension.jsonl"
    t1 = _verdict("gemma", "keep", 0.9)
    t2 = _verdict("qwen", "reject", 0.8)
    tension = detect_tension(candidate_id="c5", tier_one=t1, tier_two=t2, now=FIXED_NOW)
    assert tension is not None
    append_tension_to_log(tension, log)
    assert log.exists()
    read = read_tension_log(log)
    assert len(read) == 1
    assert read[0].candidate_id == "c5"
    assert read[0].disagreement_type == "decision"


def test_read_empty_log_returns_empty_list(tmp_path: Path):
    log = tmp_path / "empty.jsonl"
    log.write_text("")
    assert read_tension_log(log) == []


def test_malformed_line_skipped(tmp_path: Path):
    log = tmp_path / "mixed.jsonl"
    t1 = _verdict("gemma", "keep", 0.9)
    t2 = _verdict("qwen", "reject", 0.8)
    tension = detect_tension(candidate_id="c6", tier_one=t1, tier_two=t2, now=FIXED_NOW)
    assert tension is not None
    append_tension_to_log(tension, log)
    # append a malformed line
    with log.open("a") as f:
        f.write("this is not json\n")
        f.write("{\"incomplete\":")
    entries = read_tension_log(log)
    assert len(entries) == 1


def test_tension_dataclasses_frozen():
    v = ReviewVerdict(model_name="m", decision="keep", confidence=0.9, reason="r")
    with pytest.raises(dataclasses.FrozenInstanceError):
        v.decision = "reject"  # type: ignore[misc]

    t = TensionPoint(
        candidate_id="c",
        tier_one=v,
        tier_two=v,
        disagreement_type="decision",
        logged_at_utc="2026-01-01T12:00:00+00:00",
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        t.candidate_id = "other"  # type: ignore[misc]


def test_deterministic_json_shape(tmp_path: Path):
    log = tmp_path / "deterministic.jsonl"
    t1 = _verdict("gemma", "keep", 0.9, reason="r1")
    t2 = _verdict("qwen", "reject", 0.8, reason="r2")
    tension = detect_tension(candidate_id="c7", tier_one=t1, tier_two=t2, now=FIXED_NOW)
    assert tension is not None
    append_tension_to_log(tension, log)
    content = log.read_text().strip()
    parsed = json.loads(content)
    # keys must be sorted deterministically
    keys_order = list(parsed.keys())
    assert keys_order == sorted(keys_order)


def test_log_parent_dir_created(tmp_path: Path):
    nested = tmp_path / "a" / "b" / "c" / "log.jsonl"
    t1 = _verdict("gemma", "keep", 0.9)
    t2 = _verdict("qwen", "reject", 0.8)
    tension = detect_tension(candidate_id="c8", tier_one=t1, tier_two=t2, now=FIXED_NOW)
    assert tension is not None
    append_tension_to_log(tension, nested)
    assert nested.exists()
