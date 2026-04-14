"""Stream W2 — wire Stream F scaffolds into ollama_review.py."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


def _candidate() -> dict:
    return {
        "from": "law-pd-1096",
        "type": "governs",
        "to": "concept-building-permit",
        "occurrences": 3,
        "sections": ["sec-302"],
        "examples": [{"snippet": "No building permit shall be issued unless..."}],
        "char_distance": 12,
    }


def test_pre_filter_called_when_flag_on(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_review_nb_prefilter": True})

    mock_filter = MagicMock(return_value=("auto_accept", 0.98))
    monkeypatch.setattr(orv, "_run_nb_pre_filter", mock_filter)

    decision = orv._maybe_pre_filter(_candidate())
    assert decision is not None
    assert decision["action"] == "auto_accept"
    assert decision["confidence"] == 0.98
    mock_filter.assert_called_once()


def test_pre_filter_not_called_when_flag_off(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_review_nb_prefilter": False})

    mock_filter = MagicMock(return_value=("auto_accept", 0.98))
    monkeypatch.setattr(orv, "_run_nb_pre_filter", mock_filter)

    decision = orv._maybe_pre_filter(_candidate())
    assert decision is None
    mock_filter.assert_not_called()


def test_pre_filter_returns_none_on_forward(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_review_nb_prefilter": True})

    mock_filter = MagicMock(return_value=("forward_to_llm", 0.6))
    monkeypatch.setattr(orv, "_run_nb_pre_filter", mock_filter)

    decision = orv._maybe_pre_filter(_candidate())
    assert decision is None  # fall through to LLM


# ---------------------------------------------------------------------------
# Stream W2.2 — ontology prompt injection
# ---------------------------------------------------------------------------
def test_ontology_context_injected_when_flag_on(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv
    from vitruvius.review.ontology_prompt_builder import GraphEdgeSummary

    monkeypatch.setattr(
        cfgmod, "_features_block",
        lambda: {"w_review_ontology_prompt": True}
    )
    monkeypatch.setattr(
        orv, "_load_graph_edge_summaries",
        lambda: [
            GraphEdgeSummary(
                from_id="law-pd-1096",
                to_id="concept-building-permit",
                predicate="governs",
            ),
        ]
    )

    prompt = orv.build_prompt(_candidate())
    assert "governs" in prompt
    # Neighborhood block must be present as a distinct section
    assert "neighborhood" in prompt.lower() or "ontology" in prompt.lower()


def test_ontology_context_skipped_when_flag_off(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv
    monkeypatch.setattr(
        cfgmod, "_features_block",
        lambda: {"w_review_ontology_prompt": False}
    )
    mock_loader = MagicMock(return_value=[])
    monkeypatch.setattr(orv, "_load_graph_edge_summaries", mock_loader)

    orv.build_prompt(_candidate())
    mock_loader.assert_not_called()


# ---------------------------------------------------------------------------
# Stream W2.3 — SLM complexity router
# ---------------------------------------------------------------------------
def test_slm_router_chooses_draft_for_simple_candidate(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv
    monkeypatch.setattr(
        cfgmod, "_features_block",
        lambda: {"w_review_slm_routing": True, "w_llm_model_pool": True},
    )
    monkeypatch.setattr(
        cfgmod, "get_ollama_model_pool",
        lambda: {
            "tier_0_draft": "phi3:mini",
            "tier_1_default": "qwen2.5:7b",
            "tier_2_heavy": "gemma4:31b",
        },
    )

    simple = {
        "from": "law-pd-1096",
        "type": "governs",
        "to": "concept-x",
        "char_distance": 10,
        "examples": [{"snippet": "short snippet."}],
    }
    assert orv._choose_tier_model(simple) == "phi3:mini"


def test_slm_router_chooses_default_for_complex_candidate(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv
    monkeypatch.setattr(
        cfgmod, "_features_block",
        lambda: {"w_review_slm_routing": True, "w_llm_model_pool": True},
    )
    monkeypatch.setattr(
        cfgmod, "get_ollama_model_pool",
        lambda: {
            "tier_0_draft": "phi3:mini",
            "tier_1_default": "qwen2.5:7b",
        },
    )

    complex_cand = {
        "from": "law-pd-1096",
        "type": "affects",
        "to": "concept-y",
        "char_distance": 800,
        "examples": [{"snippet": "a" * 600}],
    }
    assert orv._choose_tier_model(complex_cand) == "qwen2.5:7b"


def test_slm_router_returns_default_when_flag_off(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    from vitruvius import ollama_review as orv
    monkeypatch.setattr(
        cfgmod, "_features_block",
        lambda: {"w_review_slm_routing": False},
    )
    monkeypatch.setattr(cfgmod, "get_ollama_default_model", lambda: "gemma4:31b")

    simple = {"from": "law-pd-1096", "type": "governs", "to": "concept-x", "char_distance": 10, "examples": []}
    assert orv._choose_tier_model(simple) == "gemma4:31b"
