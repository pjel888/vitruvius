"""Stream W1.1 — config-driven model pool."""
from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.config import (
    get_ollama_default_model,
    get_ollama_model_pool,
)


def test_model_pool_returns_all_tiers(monkeypatch, tmp_path: Path) -> None:
    cfg = tmp_path / "config" / "vitruvius.yaml"
    cfg.parent.mkdir(parents=True)
    cfg.write_text(
        "review:\n"
        "  ollama:\n"
        "    url: http://127.0.0.1:11434\n"
        "    model_pool:\n"
        "      tier_1_default: qwen2.5:7b\n"
        "      tier_2_heavy: gemma4:31b\n"
        "      tier_0_draft: phi3:mini\n"
        "    default_model: qwen2.5:7b\n"
        "features:\n"
        "  w_llm_model_pool: true\n",
        encoding="utf-8",
    )
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "get_repo_root", lambda: tmp_path)
    cfgmod.load_config.cache_clear()

    pool = get_ollama_model_pool()
    assert pool["tier_1_default"] == "qwen2.5:7b"
    assert pool["tier_2_heavy"] == "gemma4:31b"
    assert pool["tier_0_draft"] == "phi3:mini"


def test_default_model_respects_pool_when_flag_on(monkeypatch, tmp_path: Path) -> None:
    cfg = tmp_path / "config" / "vitruvius.yaml"
    cfg.parent.mkdir(parents=True)
    cfg.write_text(
        "review:\n"
        "  ollama:\n"
        "    url: http://127.0.0.1:11434\n"
        "    default_model: gemma4:31b\n"
        "    model_pool:\n"
        "      tier_1_default: qwen2.5:7b\n"
        "features:\n"
        "  w_llm_model_pool: true\n",
        encoding="utf-8",
    )
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "get_repo_root", lambda: tmp_path)
    cfgmod.load_config.cache_clear()

    assert get_ollama_default_model() == "qwen2.5:7b"


def test_default_model_ignores_pool_when_flag_off(monkeypatch, tmp_path: Path) -> None:
    cfg = tmp_path / "config" / "vitruvius.yaml"
    cfg.parent.mkdir(parents=True)
    cfg.write_text(
        "review:\n"
        "  ollama:\n"
        "    url: http://127.0.0.1:11434\n"
        "    default_model: gemma4:31b\n"
        "    model_pool:\n"
        "      tier_1_default: qwen2.5:7b\n"
        "features:\n"
        "  w_llm_model_pool: false\n",
        encoding="utf-8",
    )
    from vitruvius import config as cfgmod
    monkeypatch.setattr(cfgmod, "get_repo_root", lambda: tmp_path)
    cfgmod.load_config.cache_clear()

    assert get_ollama_default_model() == "gemma4:31b"


def test_model_pool_missing_returns_empty_dict(monkeypatch, tmp_path: Path) -> None:
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

    assert get_ollama_model_pool() == {}
