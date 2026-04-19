"""
Feature Flag Wiring — Taxonomy Governance + Vitruvian Context

Reads boolean feature flags from config/vitruvius.yaml and exposes them as
typed, default-safe accessors. All new flags are gated behind this module so
that no feature can be accidentally enabled without explicit config.

Usage:
    from vitruvius.config_flags import flags

    if flags.taxonomy_v2:
        # Serve v2 taxonomy tree

    if flags.vitruvian_context:
        # Enable POST /v2/resolve

Authority: .ai/06_specs/vitruvian-context/04_schema_contract.md
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Default flag values (safety: everything off by default)
# ---------------------------------------------------------------------------

DEFAULT_FLAGS: dict[str, bool] = {
    "k_taxonomy_v2": False,
    "k_jurisdictional_overrides": False,
    "k_standards_mapping": False,
    "k_vitruvian_context": False,
    "k_shadow_read": False,
    "k_backbone_validation": False,
}


# ---------------------------------------------------------------------------
# Flag container
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FeatureFlags:
    """Typed feature flag container."""

    taxonomy_v2: bool = False
    jurisdictional_overrides: bool = False
    standards_mapping: bool = False
    vitruvian_context: bool = False
    shadow_read: bool = False
    backbone_validation: bool = False

    def to_dict(self) -> dict[str, bool]:
        return {
            "k_taxonomy_v2": self.taxonomy_v2,
            "k_jurisdictional_overrides": self.jurisdictional_overrides,
            "k_standards_mapping": self.standards_mapping,
            "k_vitruvian_context": self.vitruvian_context,
            "k_shadow_read": self.shadow_read,
            "k_backbone_validation": self.backbone_validation,
        }


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "vitruvius.yaml"


def _load_raw_config(path: Path | None = None) -> dict[str, Any]:
    """Load the raw YAML config file."""
    config_path = path or _CONFIG_PATH
    if not config_path.exists():
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _extract_flags(raw: dict[str, Any]) -> dict[str, bool]:
    """Extract flag values from raw config, falling back to defaults."""
    features = raw.get("features", {})
    result = {}
    for key, default in DEFAULT_FLAGS.items():
        value = features.get(key)
        if isinstance(value, bool):
            result[key] = value
        else:
            result[key] = default
    return result


def load_flags(path: Path | None = None) -> FeatureFlags:
    """
    Load feature flags from config/vitruvius.yaml.

    Environment variable override: VITRUVIUS_FLAGS=k_taxonomy_v2:true,k_vitruvian_context:true
    """
    raw = _load_raw_config(path)
    flag_dict = _extract_flags(raw)

    # Environment override for CI / local testing
    env_override = os.environ.get("VITRUVIUS_FLAGS", "")
    if env_override:
        for pair in env_override.split(","):
            if ":" not in pair:
                continue
            key, val = pair.split(":", 1)
            key = key.strip()
            val = val.strip().lower()
            if key in DEFAULT_FLAGS:
                flag_dict[key] = val in ("true", "1", "yes", "on")

    return FeatureFlags(
        taxonomy_v2=flag_dict["k_taxonomy_v2"],
        jurisdictional_overrides=flag_dict["k_jurisdictional_overrides"],
        standards_mapping=flag_dict["k_standards_mapping"],
        vitruvian_context=flag_dict["k_vitruvian_context"],
        shadow_read=flag_dict["k_shadow_read"],
        backbone_validation=flag_dict["k_backbone_validation"],
    )


# ---------------------------------------------------------------------------
# Singleton (lazy-loaded)
# ---------------------------------------------------------------------------

_flags: FeatureFlags | None = None


def get_flags() -> FeatureFlags:
    """Return the singleton feature flag instance."""
    global _flags
    if _flags is None:
        _flags = load_flags()
    return _flags


# Module-level convenience accessor
flags = get_flags()
