"""Stream Y2.2 — `route_with_moe` domain-aware router tests.

These tests sit alongside the Stream F.2 `route()` tests and verify that
the MoE extension composes with the existing router without touching it.
"""
from __future__ import annotations

from vitruvius.review.domain_classifier import Domain
from vitruvius.review.slm_router import (
    ComplexitySignals,
    MoEVerdict,
    route,
    route_with_moe,
)


def test_geometric_candidate_routes_to_small_model() -> None:
    verdict = route_with_moe(
        candidate={
            "subject": "building",
            "predicate": "has_setback",
            "object": "3m",
            "evidence": "The setback must be 3m.",
        },
        moe_policy={
            Domain.GEOMETRIC: "qwen2.5:3b-instruct-q4_K_M",
            Domain.ADMINISTRATIVE: "qwen2.5:7b-instruct-q4_K_M",
            Domain.OCCUPANCY: "qwen2.5:7b-instruct-q4_K_M",
            Domain.SAFETY: "qwen2.5:7b-instruct-q4_K_M",
            Domain.FEES: "qwen2.5:3b-instruct-q4_K_M",
            Domain.OTHER: "qwen2.5:7b-instruct-q4_K_M",
        },
    )
    assert isinstance(verdict, MoEVerdict)
    assert verdict.model == "qwen2.5:3b-instruct-q4_K_M"
    assert verdict.domain == Domain.GEOMETRIC


def test_administrative_candidate_routes_to_mid_model() -> None:
    verdict = route_with_moe(
        candidate={
            "subject": "construction",
            "predicate": "requires_permit",
            "object": "building official",
        },
        moe_policy={
            Domain.GEOMETRIC: "small",
            Domain.ADMINISTRATIVE: "mid",
            Domain.OCCUPANCY: "mid",
            Domain.SAFETY: "mid",
            Domain.FEES: "small",
            Domain.OTHER: "mid",
        },
    )
    assert verdict.model == "mid"
    assert verdict.domain == Domain.ADMINISTRATIVE


def test_unknown_domain_falls_back_to_other() -> None:
    verdict = route_with_moe(
        candidate={
            "subject": "x",
            "predicate": "relates_to",
            "object": "y",
        },
        moe_policy={
            Domain.GEOMETRIC: "small",
            Domain.ADMINISTRATIVE: "mid",
            Domain.OCCUPANCY: "mid",
            Domain.SAFETY: "mid",
            Domain.FEES: "small",
            Domain.OTHER: "default",
        },
    )
    assert verdict.domain == Domain.OTHER
    assert verdict.model == "default"


def test_legacy_route_unchanged() -> None:
    """The original Stream F.2 `route` function must still work untouched.

    Uses the real ``ComplexitySignals`` signature (dataclass with
    predicate / evidence_char_count / sentence_count / has_negation /
    crf_confidence / regex_pattern_id fields) to verify the legacy
    API is preserved after the Y2.2 append-only extension.
    """
    signals = ComplexitySignals(
        predicate="governs",
        evidence_char_count=50,
        sentence_count=1,
        has_negation=False,
        crf_confidence=0.9,
        regex_pattern_id="pat-1",
    )
    decision = route(signals)
    assert decision.model_name  # non-empty
    assert decision.level in {"simple", "medium", "complex"}


# ---------------------------------------------------------------------------
# Stream Y2.4 — select_review_model flag-gated hook in ollama_review.py
# ---------------------------------------------------------------------------
from pathlib import Path
from unittest.mock import patch


def test_select_review_model_falls_back_when_moe_flag_off(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_domain_routing_moe": False})
    monkeypatch.setattr(cfgmod, "get_ollama_default_model", lambda: "baseline")

    model = orv.select_review_model(
        candidate={"subject": "x", "predicate": "has_setback", "object": "3m"},
    )
    assert model == "baseline"


def test_select_review_model_uses_moe_when_flag_on(monkeypatch, tmp_path: Path) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    policy_file = tmp_path / "moe.yaml"
    policy_file.write_text(
        "geometric: small-model\nadministrative: mid-model\noccupancy: mid-model\n"
        "safety: mid-model\nfees: small-model\nother: mid-model\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_domain_routing_moe": True})

    model = orv.select_review_model(
        candidate={"subject": "building", "predicate": "has_setback", "object": "3m"},
        moe_policy_path=policy_file,
    )
    assert model == "small-model"


def test_select_review_model_administrative_routes_to_mid(monkeypatch, tmp_path: Path) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv

    policy_file = tmp_path / "moe.yaml"
    policy_file.write_text(
        "geometric: small-model\nadministrative: mid-model\noccupancy: mid-model\n"
        "safety: mid-model\nfees: small-model\nother: mid-model\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"y_domain_routing_moe": True})

    model = orv.select_review_model(
        candidate={"subject": "construction", "predicate": "requires_permit", "object": "building official"},
        moe_policy_path=policy_file,
    )
    assert model == "mid-model"
