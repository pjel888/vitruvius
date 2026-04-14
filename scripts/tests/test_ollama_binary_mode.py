"""Stream W1.4 — binary-mode prompt that asks a small model True/False."""
from __future__ import annotations

import pytest

from vitruvius.ollama_review import (
    _build_binary_prompt,
    build_prompt,
)


def _candidate():
    return {
        "from": "law-pd-1096",
        "type": "governs",
        "to": "concept-building-permit",
        "occurrences": 3,
        "sections": ["sec-302"],
        "examples": [{"snippet": "No building permit shall be issued unless..."}],
    }


def test_binary_prompt_uses_true_false_schema() -> None:
    prompt = _build_binary_prompt(_candidate())
    assert "True" in prompt
    assert "False" in prompt
    assert "governs" in prompt
    assert "building permit" in prompt or "building-permit" in prompt


def test_binary_prompt_is_shorter_than_verbose_prompt() -> None:
    binary = _build_binary_prompt(_candidate())
    verbose = build_prompt(_candidate())
    # Binary should be substantially shorter — aim for <50% the verbose length.
    assert len(binary) < len(verbose) * 0.5, (
        f"binary prompt is not compact: binary={len(binary)} verbose={len(verbose)}"
    )


def test_build_prompt_dispatches_to_binary_when_flag_on(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_llm_binary_mode": True})
    prompt = build_prompt(_candidate())
    # Binary marker: must contain the word "True" uppercase as a schema token
    assert "True" in prompt and "False" in prompt


def test_build_prompt_is_verbose_when_flag_off(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_llm_binary_mode": False})
    prompt = build_prompt(_candidate())
    assert '"task"' in prompt  # verbose JSON task envelope
