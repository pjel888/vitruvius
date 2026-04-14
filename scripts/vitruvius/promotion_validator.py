from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from .paths import get_repo_root


from typing import Any


@lru_cache(maxsize=1)
def load_registry() -> dict:
    path = get_repo_root() / "scripts" / "vitruvius" / "rules" / "relationship_registry.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _parse_frontmatter(md_text: str) -> dict[str, Any]:
    if not md_text.startswith("---"):
        return {}
    end = md_text.find("\n---", 3)
    if end == -1:
        return {}
    raw = md_text[3:end].strip()
    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}


def build_canonical_index(repo_root: Path) -> dict[str, dict[str, Any]]:
    """Walk 003_Canonical-Knowledge-Layer/shared/{sources,concepts} and return
    an ID-keyed index for referential-integrity checks."""
    index: dict[str, dict[str, Any]] = {}

    base = Path(repo_root) / "003_Canonical-Knowledge-Layer" / "shared"
    for entity_type, subdir in (("source", "sources"), ("concept", "concepts")):
        directory = base / subdir
        if not directory.exists():
            continue
        for md_path in sorted(directory.glob("*.md")):
            fm = _parse_frontmatter(md_path.read_text(encoding="utf-8"))
            entity_id = fm.get("id")
            if not entity_id:
                continue
            index[entity_id] = {
                "type": entity_type,
                "path": md_path,
                "canonical_status": fm.get("canonical_status", "unknown"),
                "trust_level": fm.get("trust_level"),
            }

    return index
