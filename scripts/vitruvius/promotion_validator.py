from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from .paths import get_repo_root


@lru_cache(maxsize=1)
def load_registry() -> dict:
    path = get_repo_root() / "scripts" / "vitruvius" / "rules" / "relationship_registry.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
