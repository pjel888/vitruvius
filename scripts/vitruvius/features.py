"""Feature-flag loader for the Statistical & Architectural Upgrade streams.

Every new module in Streams A-K gates its behaviour on a feature flag. Flags
are stored under `features:` in config/vitruvius.yaml and default to False.

This module is deliberately minimal — it owns exactly one config key
(`features`) and fails safe: missing file, missing block, malformed YAML,
and unknown flags all return False. The returned Features is frozen to
prevent accidental mutation after load.

See .ai/03_plans/statistical-architectural-upgrade-plan.md §3.5 for the
canonical flag list and the non-breaking contract that depends on
default-False behaviour.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

import yaml


@dataclass(frozen=True)
class Features:
    """Frozen mapping of feature flag name → bool."""

    flags: Mapping[str, bool]

    def is_enabled(self, name: str) -> bool:
        """Return True if `name` is explicitly set truthy in the config.

        Unknown flags always return False. The return is always a bool,
        never a raw truthy value from the YAML.
        """
        return bool(self.flags.get(name, False))


def load_features(config_path: Path) -> Features:
    """Load the `features:` block from a vitruvius.yaml file.

    Fails safe: returns an empty Features (all flags disabled) if the file
    is missing, the YAML is malformed, or the `features` block is absent
    or not a dict.
    """
    if not config_path.exists():
        return Features(flags=MappingProxyType({}))
    try:
        raw = yaml.safe_load(config_path.read_text()) or {}
    except yaml.YAMLError:
        return Features(flags=MappingProxyType({}))
    if not isinstance(raw, dict):
        return Features(flags=MappingProxyType({}))
    block = raw.get("features")
    if not isinstance(block, dict):
        return Features(flags=MappingProxyType({}))
    coerced: dict[str, bool] = {str(k): bool(v) for k, v in block.items()}
    return Features(flags=MappingProxyType(coerced))
