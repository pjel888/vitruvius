"""Ollama env config helper — version-gated env var emission (Task F.7)."""

from __future__ import annotations

import pytest

from vitruvius.review.ollama_config import (
    EnvExport,
    OllamaEnvConfig,
    build_ollama_env,
    parse_ollama_version,
)


def test_default_config_emits_num_parallel():
    config = OllamaEnvConfig()
    result = build_ollama_env(config, ollama_version="0.3.0")
    assert "OLLAMA_NUM_PARALLEL" in result.env_vars
    assert result.env_vars["OLLAMA_NUM_PARALLEL"] == "4"


def test_kv_cache_skipped_below_0_4():
    config = OllamaEnvConfig()
    result = build_ollama_env(config, ollama_version="0.3.9")
    assert "OLLAMA_KV_CACHE_TYPE" not in result.env_vars
    assert any("KV_CACHE" in note for note in result.notes)


def test_flash_attention_skipped_below_0_4():
    config = OllamaEnvConfig()
    result = build_ollama_env(config, ollama_version="0.3.0")
    assert "OLLAMA_FLASH_ATTENTION" not in result.env_vars
    assert any("FLASH_ATTENTION" in note for note in result.notes)


def test_kv_cache_and_flash_attention_emitted_at_0_4():
    config = OllamaEnvConfig()
    result = build_ollama_env(config, ollama_version="0.4.0")
    assert result.env_vars["OLLAMA_KV_CACHE_TYPE"] == "q8_0"
    assert result.env_vars["OLLAMA_FLASH_ATTENTION"] == "1"


def test_speculative_skipped_below_0_6():
    config = OllamaEnvConfig(
        speculative_decoding=True,
        draft_model="qwen2.5:0.5b",
    )
    result = build_ollama_env(config, ollama_version="0.5.9")
    assert "OLLAMA_SPEC_DECODE" not in result.env_vars
    assert "OLLAMA_DRAFT_MODEL" not in result.env_vars


def test_speculative_emitted_at_0_6_with_draft_model():
    config = OllamaEnvConfig(
        speculative_decoding=True,
        draft_model="qwen2.5:0.5b",
    )
    result = build_ollama_env(config, ollama_version="0.6.0")
    assert result.env_vars["OLLAMA_SPEC_DECODE"] == "1"
    assert result.env_vars["OLLAMA_DRAFT_MODEL"] == "qwen2.5:0.5b"


def test_speculative_without_draft_model_is_skipped():
    config = OllamaEnvConfig(
        speculative_decoding=True,
        draft_model=None,
    )
    result = build_ollama_env(config, ollama_version="0.6.0")
    assert "OLLAMA_SPEC_DECODE" not in result.env_vars


def test_version_none_emits_everything():
    config = OllamaEnvConfig(
        speculative_decoding=True,
        draft_model="qwen2.5:0.5b",
    )
    result = build_ollama_env(config, ollama_version=None)
    assert "OLLAMA_NUM_PARALLEL" in result.env_vars
    assert "OLLAMA_KV_CACHE_TYPE" in result.env_vars
    assert "OLLAMA_FLASH_ATTENTION" in result.env_vars
    assert "OLLAMA_SPEC_DECODE" in result.env_vars
    assert "OLLAMA_DRAFT_MODEL" in result.env_vars


def test_parse_ollama_version_happy_path():
    assert parse_ollama_version("0.4.2") == (0, 4, 2)
    assert parse_ollama_version("1.0.0") == (1, 0, 0)


def test_parse_ollama_version_garbage_raises():
    with pytest.raises(ValueError):
        parse_ollama_version("not-a-version")
    with pytest.raises(ValueError):
        parse_ollama_version("0.4")


def test_env_export_is_dict_like():
    config = OllamaEnvConfig()
    result = build_ollama_env(config, ollama_version="0.4.0")
    assert isinstance(result, EnvExport)
    assert isinstance(result.env_vars, dict)
    assert isinstance(result.notes, tuple)
