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
