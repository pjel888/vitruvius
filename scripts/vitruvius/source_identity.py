from __future__ import annotations

from pathlib import Path

import yaml

from .canonicalize import (
    build_canonical_id,
    build_plan,
    find_rule,
    load_rules,
    map_source_type_to_prefix,
    normalize_title,
)
from .paths import get_repo_root
from .source_paths import logical_source_key_for_relative_path


def _canonical_source_id_from_existing_sources(
    relative_path: str,
    *,
    repo_root: Path | None = None,
) -> str | None:
    repo_root = repo_root or get_repo_root()
    sources_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    if not sources_dir.exists():
        return None

    normalized_path = Path(relative_path).as_posix()
    logical_source_key = logical_source_key_for_relative_path(normalized_path)
    for source_file in sorted(sources_dir.glob("*.md")):
        text = source_file.read_text(encoding="utf-8", errors="ignore")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        try:
            fm = yaml.safe_load(text[3:end].strip())
        except yaml.YAMLError:
            continue
        if not isinstance(fm, dict):
            continue
        source_relative_markdown_path = fm.get("source_relative_markdown_path")
        canonical_id = fm.get("id")
        if (
            isinstance(source_relative_markdown_path, str)
            and (
                Path(source_relative_markdown_path).as_posix() == normalized_path
                or logical_source_key_for_relative_path(source_relative_markdown_path) == logical_source_key
            )
            and isinstance(canonical_id, str)
            and canonical_id.strip()
        ):
            return canonical_id
    return None


def _base_canonical_source_id_for_relative_path(relative_path: str) -> str | None:
    rules = load_rules()
    rule = find_rule(rules, relative_path)
    source_type = "unknown"
    if rule:
        source_type = rule.get("classification", {}).get("source_type", "unknown")
    title = normalize_title(relative_path, rule)
    prefix = map_source_type_to_prefix(source_type)
    return build_canonical_id(prefix, title)


def canonical_source_id_for_relative_path(
    relative_path: str,
    *,
    repo_root: Path | None = None,
) -> str:
    existing_canonical_id = _canonical_source_id_from_existing_sources(
        relative_path,
        repo_root=repo_root,
    )
    if existing_canonical_id is not None:
        return existing_canonical_id

    path_lower = str(relative_path).lower()
    stem = Path(relative_path).stem.lower()
    if "ra9514" in path_lower or "ra-9514" in path_lower:
        return "irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines"
    if "bp220" in path_lower or "bp-220" in path_lower:
        return "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220"
    if "bp344" in path_lower or "bp-344" in path_lower:
        return "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344"

    try:
        base_canonical_id = _base_canonical_source_id_for_relative_path(relative_path)
        if base_canonical_id:
            return base_canonical_id
    except Exception:
        pass

    try:
        plan = build_plan(relative_path)
        canonical_id = plan.get("canonical_id")
        if isinstance(canonical_id, str) and canonical_id.strip():
            return canonical_id
    except Exception:
        pass

    if "irr" in stem:
        return "irr-implementing-rules-and-regulations-of-the-national-building-code"
    return "law-national-building-code-of-the-philippines"
