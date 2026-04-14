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


def test_request_body_preserves_existing_options_when_flag_off(monkeypatch) -> None:
    """Flag-OFF path must keep temperature=0 and num_predict=300 that the
    current call_ollama baseline emits. Otherwise byte-identity regresses."""
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "_features_block", lambda: {"w_llm_num_ctx_enforcement": False})
    body = _build_ollama_request_body(
        model="qwen2.5:7b",
        prompt="hello",
    )
    assert body["options"]["temperature"] == 0
    assert body["options"]["num_predict"] == 300
