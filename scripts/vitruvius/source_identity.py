from __future__ import annotations

from pathlib import Path

import yaml

from .canonicalize import build_plan
from .paths import get_repo_root


def _canonical_source_id_from_existing_sources(relative_path: str) -> str | None:
    repo_root = get_repo_root()
    sources_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "sources"
    if not sources_dir.exists():
        return None

    normalized_path = Path(relative_path).as_posix()
    for source_file in sources_dir.glob("*.md"):
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
            and Path(source_relative_markdown_path).as_posix() == normalized_path
            and isinstance(canonical_id, str)
            and canonical_id.strip()
        ):
            return canonical_id
    return None


def canonical_source_id_for_relative_path(relative_path: str) -> str:
    existing_canonical_id = _canonical_source_id_from_existing_sources(relative_path)
    if existing_canonical_id is not None:
        return existing_canonical_id

    try:
        plan = build_plan(relative_path)
        canonical_id = plan.get("canonical_id")
        if isinstance(canonical_id, str) and canonical_id.strip():
            return canonical_id
    except Exception:
        pass

    stem = Path(relative_path).stem.lower()
    if "ra9514" in stem or "ra-9514" in stem:
        return "irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines"
    if "bp220" in stem or "bp-220" in stem:
        return "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220"
    if "bp344" in stem or "bp-344" in stem:
        return "irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344"
    if "irr" in stem:
        return "irr-implementing-rules-and-regulations-of-the-national-building-code"
    return "law-national-building-code-of-the-philippines"
