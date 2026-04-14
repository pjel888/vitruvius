from __future__ import annotations

from functools import lru_cache

import yaml

from .paths import get_repo_root


@lru_cache(maxsize=1)
def load_config() -> dict:
    path = get_repo_root() / "config" / "vitruvius.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_ollama_url() -> str:
    cfg = load_config()
    return cfg.get("review", {}).get("ollama", {}).get("url", "http://127.0.0.1:11434")


def get_ollama_default_model() -> str:
    cfg = load_config()
    return cfg.get("review", {}).get("ollama", {}).get("default_model", "gemma4:31b")


def get_ollama_default_timeout() -> int:
    cfg = load_config()
    return int(cfg.get("review", {}).get("ollama", {}).get("default_timeout_seconds", 600))


def get_confidence_threshold() -> float:
    cfg = load_config()
    return float(cfg.get("promotion", {}).get("confidence_threshold", 0.90))


def get_audit_log_name() -> str:
    cfg = load_config()
    return cfg.get("promotion", {}).get("audit_log_name", "latest_promotion_audit.log")
