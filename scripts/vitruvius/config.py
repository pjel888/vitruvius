from __future__ import annotations

from functools import lru_cache

import yaml

from .paths import get_repo_root


@lru_cache(maxsize=1)
def load_config() -> dict:
    path = get_repo_root() / "config" / "vitruvius.yaml"
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except OSError:
        return {}


def get_ollama_url() -> str:
    cfg = load_config()
    return cfg.get("review", {}).get("ollama", {}).get("url", "http://127.0.0.1:11434")


def get_ollama_model_pool() -> dict[str, str]:
    cfg = load_config()
    pool = cfg.get("review", {}).get("ollama", {}).get("model_pool", {})
    if not isinstance(pool, dict):
        return {}
    return {str(k): str(v) for k, v in pool.items()}


def get_ollama_num_ctx_cap() -> int:
    cfg = load_config()
    raw = cfg.get("review", {}).get("ollama", {}).get("num_ctx_cap", 8192)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return 8192
    return max(1024, min(value, 131072))


def _features_block() -> dict:
    cfg = load_config()
    block = cfg.get("features", {})
    return block if isinstance(block, dict) else {}


def get_ollama_default_model() -> str:
    cfg = load_config()
    raw_default = cfg.get("review", {}).get("ollama", {}).get("default_model", "gemma4:31b")
    if _features_block().get("w_llm_model_pool", False):
        pool = get_ollama_model_pool()
        tier1 = pool.get("tier_1_default")
        if isinstance(tier1, str) and tier1:
            return tier1
    return str(raw_default)


def get_ollama_8gb_safe_model() -> str:
    pool = get_ollama_model_pool()
    tier1 = pool.get("tier_1_default")
    if isinstance(tier1, str) and tier1:
        return tier1
    return "qwen2.5:7b"


def resolve_review_model(*, explicit_model: str | None = None, preset: str | None = None) -> str:
    if isinstance(explicit_model, str) and explicit_model.strip():
        return explicit_model.strip()
    if preset == "8gb-safe":
        return get_ollama_8gb_safe_model()
    return get_ollama_default_model()


def get_ollama_default_timeout() -> int:
    cfg = load_config()
    return int(cfg.get("review", {}).get("ollama", {}).get("default_timeout_seconds", 600))


def get_ollama_max_retries() -> int:
    cfg = load_config()
    return int(cfg.get("review", {}).get("ollama", {}).get("max_retries_per_candidate", 3))


def get_ollama_retry_backoff() -> float:
    cfg = load_config()
    return float(cfg.get("review", {}).get("ollama", {}).get("retry_backoff_seconds", 2))


def get_ollama_default_parallelism() -> int:
    cfg = load_config()
    return int(cfg.get("review", {}).get("ollama", {}).get("default_parallelism", 1))


def get_confidence_threshold() -> float:
    cfg = load_config()
    return float(cfg.get("promotion", {}).get("confidence_threshold", 0.90))


def get_audit_log_name() -> str:
    cfg = load_config()
    return cfg.get("promotion", {}).get("audit_log_name", "latest_promotion_audit.log")
