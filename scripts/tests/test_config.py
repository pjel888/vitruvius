from pathlib import Path
from vitruvius.config import load_config, get_ollama_url, get_confidence_threshold


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
