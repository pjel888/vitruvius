"""Stream Y3.3 — end-to-end CoT adjudication hook tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest


VALID_COT = (
    "<think>\n"
    "Step 1: Evidence: 'setback must be at least 3 meters'.\n"
    "Step 2: Candidate aligns with the rule.\n"
    "Self-confidence: 0.88\n"
    "</think>\n"
    "VERDICT: keep"
)


def test_adjudicate_with_cot_flag_off_returns_legacy(monkeypatch, tmp_path: Path) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_thinking_mode_cot": False})
    monkeypatch.setattr(orv, "_legacy_adjudicate", lambda **kwargs: {"verdict": "keep"})

    out = orv.adjudicate_with_cot(
        candidate={"subject": "x", "predicate": "p", "object": "o"},
        raw_llm_response="whatever",
        relationship_hash="abc",
        cot_out_dir=tmp_path,
    )
    assert out == {"verdict": "keep"}
    # Audit dir should be empty when flag is OFF
    assert list(tmp_path.glob("*.json")) == []


def test_adjudicate_with_cot_flag_on_parses_and_writes_trace(
    monkeypatch, tmp_path: Path
) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_thinking_mode_cot": True})

    out = orv.adjudicate_with_cot(
        candidate={"subject": "x", "predicate": "p", "object": "o"},
        raw_llm_response=VALID_COT,
        relationship_hash="abc123",
        cot_out_dir=tmp_path,
        model="fake-model",
    )
    assert out["verdict"] == "keep"
    assert out["escalate"] is False
    traces = list(tmp_path.glob("*.json"))
    assert len(traces) == 1
    assert traces[0].name.endswith("_abc123.json")


def test_adjudicate_with_cot_rejects_missing_think_block(
    monkeypatch, tmp_path: Path
) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_thinking_mode_cot": True})

    out = orv.adjudicate_with_cot(
        candidate={"subject": "x", "predicate": "p", "object": "o"},
        raw_llm_response="VERDICT: keep",
        relationship_hash="abc",
        cot_out_dir=tmp_path,
    )
    assert out["verdict"] == "escalate"
    assert "CotParseError" in out["reason"]


def test_adjudicate_with_cot_escalates_on_low_confidence(
    monkeypatch, tmp_path: Path
) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_thinking_mode_cot": True})

    low_conf_cot = (
        "<think>\n"
        "Step 1: Evidence: 'quoted span that is long enough'.\n"
        "Step 2: unclear alignment.\n"
        "Self-confidence: 0.4\n"
        "</think>\n"
        "VERDICT: keep"
    )
    out = orv.adjudicate_with_cot(
        candidate={"subject": "x", "predicate": "p", "object": "o"},
        raw_llm_response=low_conf_cot,
        relationship_hash="abc",
        cot_out_dir=tmp_path,
    )
    assert out["verdict"] == "escalate"
    assert out["self_confidence"] == pytest.approx(0.4)
