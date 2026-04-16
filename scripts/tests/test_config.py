from pathlib import Path
from vitruvius.config import (
    get_confidence_threshold,
    get_ollama_url,
    get_review_presets,
    load_config,
    resolve_review_preset,
)


def test_load_config_returns_dict():
    cfg = load_config()
    assert isinstance(cfg, dict)
    assert "review" in cfg
    assert "promotion" in cfg


def test_get_ollama_url_reads_config():
    url = get_ollama_url()
    assert url.startswith("http://")
    assert "11434" in url


def test_get_confidence_threshold_is_point_nine():
    assert get_confidence_threshold() == 0.90


def test_ollama_review_uses_config_url():
    from vitruvius import ollama_review
    import inspect
    src = inspect.getsource(ollama_review.call_ollama)
    assert "get_ollama_url" in src, "call_ollama must read URL from config module"


def test_review_presets_include_m2_8gb_safe():
    presets = get_review_presets()
    assert "m2-8gb-safe" in presets
    assert presets["m2-8gb-safe"]["parallelism"] == 1


def test_resolve_review_preset_returns_named_payload():
    preset = resolve_review_preset("m2-8gb-safe")
    assert preset is not None
    assert preset["name"] == "m2-8gb-safe"
    assert preset["keeps_phase_11_gated"] is True
