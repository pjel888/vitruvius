from __future__ import annotations

from functools import lru_cache
from typing import Any

import yaml

from .paths import get_repo_root


_REVIEW_PRESET_ALIASES = {
    "8gb-safe": "m2-8gb-safe",
    "m2-8gb-safe": "m2-8gb-safe",
}


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


def get_ollama_review_preset(name: str) -> dict[str, int | str]:
    preset = resolve_review_preset(name)
    if preset is None:
        return {}
    return {
        key: value
        for key, value in preset.items()
        if key in {"model", "timeout_seconds", "parallelism", "num_ctx_cap"}
    }


def get_review_presets() -> dict[str, dict[str, int | str | bool]]:
    cfg = load_config()
    presets = cfg.get("review", {}).get("ollama", {}).get("presets", {})
    if not isinstance(presets, dict):
        presets = {}

    normalized: dict[str, dict[str, int | str | bool]] = {}
    for raw_name, raw in presets.items():
        if not isinstance(raw_name, str) or not isinstance(raw, dict):
            continue
        name = _REVIEW_PRESET_ALIASES.get(raw_name.strip(), raw_name.strip())
        entry: dict[str, int | str | bool] = {
            "name": name,
            "keeps_phase_11_gated": True,
        }
        model = raw.get("model")
        if isinstance(model, str) and model.strip():
            entry["model"] = model.strip()
        for key in ("timeout_seconds", "parallelism", "num_ctx_cap"):
            value = raw.get(key)
            try:
                parsed = int(value)
            except (TypeError, ValueError):
                continue
            if parsed > 0:
                entry[key] = parsed
        normalized[name] = entry

    if "m2-8gb-safe" not in normalized:
        normalized["m2-8gb-safe"] = {
            "name": "m2-8gb-safe",
            "model": "llama3.1:8b",
            "timeout_seconds": 900,
            "parallelism": 1,
            "num_ctx_cap": 4096,
            "keeps_phase_11_gated": True,
        }
    return normalized


def resolve_review_preset(name: str | None) -> dict[str, int | str | bool] | None:
    if not isinstance(name, str) or not name.strip():
        return None
    presets = get_review_presets()
    canonical = _REVIEW_PRESET_ALIASES.get(name.strip(), name.strip())
    return presets.get(canonical)


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
    preset = resolve_review_preset("m2-8gb-safe")
    model = preset.get("model") if isinstance(preset, dict) else None
    if isinstance(model, str) and model:
        return model
    pool = get_ollama_model_pool()
    tier1 = pool.get("tier_1_default")
    if isinstance(tier1, str) and tier1:
        return tier1
    return "qwen2.5:7b"


def resolve_review_model(*, explicit_model: str | None = None, preset: str | None = None) -> str:
    if isinstance(explicit_model, str) and explicit_model.strip():
        return explicit_model.strip()
    preset_cfg = resolve_review_preset(preset)
    if isinstance(preset_cfg, dict):
        model = preset_cfg.get("model")
        if isinstance(model, str) and model.strip():
            return model.strip()
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


# ---------------------------------------------------------------------------
# Sprint KG — Knowledge Graph transition flag helpers
# ---------------------------------------------------------------------------

def _kg_block() -> dict:
    cfg = load_config()
    block = cfg.get("kg_transition", {})
    return block if isinstance(block, dict) else {}


def is_kg_enabled() -> bool:
    return bool(_kg_block().get("enabled", False))


def is_kg_legacy_snapshot_mode() -> bool:
    return bool(_kg_block().get("legacy_snapshot_mode", True))


def is_kg_neo4j_backend() -> bool:
    return bool(_kg_block().get("neo4j_backend", False))


def is_kg_postgres_registry() -> bool:
    return bool(_kg_block().get("postgres_registry", False))


def is_kg_evidence_graph() -> bool:
    return bool(_kg_block().get("evidence_graph", False))


def is_kg_assertion_layer() -> bool:
    return bool(_kg_block().get("assertion_layer", False))


def is_kg_structured_extraction() -> bool:
    return bool(_kg_block().get("structured_extraction", False))


def is_kg_taxonomy_seeding() -> bool:
    return bool(_kg_block().get("taxonomy_seeding", False))


def is_kg_incremental_updates() -> bool:
    return bool(_kg_block().get("incremental_updates", False))


def is_kg_qdrant_retrieval() -> bool:
    return bool(_kg_block().get("qdrant_retrieval", False))


def get_kg_neo4j_uri() -> str:
    return str(_kg_block().get("neo4j_uri", "bolt://localhost:7687"))


def get_kg_neo4j_user() -> str:
    return str(_kg_block().get("neo4j_user", "neo4j"))


def get_kg_neo4j_password() -> str:
    return str(_kg_block().get("neo4j_password", "password"))


def get_kg_postgres_conninfo() -> str:
    return str(_kg_block().get("postgres_conninfo", "dbname=vitruvius user=postgres password=password host=localhost port=5432"))
