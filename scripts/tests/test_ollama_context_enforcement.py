"""Stream W1.2 — num_ctx hard cap in Ollama request body."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from vitruvius.ollama_review import _build_ollama_request_body


def test_request_body_omits_num_ctx_when_flag_off(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_llm_num_ctx_enforcement": False})
    body = _build_ollama_request_body(
        model="qwen2.5:7b",
        prompt="hello",
    )
    assert "options" not in body or "num_ctx" not in body.get("options", {})


def test_request_body_injects_num_ctx_when_flag_on(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_llm_num_ctx_enforcement": True})
    monkeypatch.setattr(cfgmod, "get_ollama_num_ctx_cap", lambda: 4096)
    body = _build_ollama_request_body(
        model="qwen2.5:7b",
        prompt="hello",
    )
    assert body["options"]["num_ctx"] == 4096


def test_request_body_still_contains_model_and_prompt(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_llm_num_ctx_enforcement": True})
    monkeypatch.setattr(cfgmod, "get_ollama_num_ctx_cap", lambda: 8192)
    body = _build_ollama_request_body(
        model="qwen2.5:7b",
        prompt="classify this candidate",
    )
    assert body["model"] == "qwen2.5:7b"
    assert body["prompt"] == "classify this candidate"
    assert body["format"] == "json"
    assert body["stream"] is False


def test_num_ctx_cap_defaults_to_8192_when_missing(monkeypatch, tmp_path: Path) -> None:
    cfg = tmp_path / "config" / "vitruvius.yaml"
    cfg.parent.mkdir(parents=True)
    cfg.write_text(
        "review:\n"
        "  ollama:\n"
        "    url: http://127.0.0.1:11434\n"
        "    default_model: gemma4:31b\n",
        encoding="utf-8",
    )
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "get_repo_root", lambda: tmp_path)
    cfgmod.load_config.cache_clear()

    assert cfgmod.get_ollama_num_ctx_cap() == 8192


def test_request_body_uses_deterministic_options_when_flag_off(monkeypatch) -> None:
    """Flag-OFF path keeps deterministic settings with enough JSON budget."""
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_llm_num_ctx_enforcement": False})
    body = _build_ollama_request_body(
        model="qwen2.5:7b",
        prompt="hello",
    )
    assert body["options"]["temperature"] == 0
    assert body["options"]["num_predict"] == 700


# ---------------------------------------------------------------------------
# Stream W1.3 — pre-call context budget guard
# ---------------------------------------------------------------------------
from vitruvius.ollama_review import (
    ContextBudgetExceeded,
    _enforce_context_budget,
    _estimate_prompt_tokens,
)


def test_estimate_tokens_is_characters_over_four() -> None:
    prompt = "abcd" * 1000  # 4000 chars
    assert _estimate_prompt_tokens(prompt) == 1000


def test_enforce_budget_passes_under_cap(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_llm_context_budget_guard": True})
    monkeypatch.setattr(cfgmod, "get_ollama_num_ctx_cap", lambda: 4096)
    _enforce_context_budget("abcd" * 100)  # ~100 tokens


def test_enforce_budget_raises_over_cap(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_llm_context_budget_guard": True})
    monkeypatch.setattr(cfgmod, "get_ollama_num_ctx_cap", lambda: 1024)
    huge_prompt = "abcd" * 5000  # ~5000 tokens, cap is 1024
    with pytest.raises(ContextBudgetExceeded, match="5000"):
        _enforce_context_budget(huge_prompt)


def test_enforce_budget_is_noop_when_flag_off(monkeypatch) -> None:
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_llm_context_budget_guard": False})
    monkeypatch.setattr(cfgmod, "get_ollama_num_ctx_cap", lambda: 1024)
    # Flag off → don't raise even on a 20000-token prompt
    _enforce_context_budget("abcd" * 20000)
