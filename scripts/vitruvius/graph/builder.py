from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .contract import (
    ALLOWED_TRUST_LEVELS,
    GraphEdge,
    GraphNode,
    GraphSnapshot,
    validate_edge,
    validate_node,
)


_PROMOTED_STATUSES = frozenset({"promoted", "verified"})


def _to_iso_string(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        utc = value.astimezone(timezone.utc)
        return utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, str):
        return value
    return None


def _load_frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    try:
        data = yaml.safe_load(text[3:end].strip())
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def _mtime_iso(path: Path) -> str:
    ts = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_date(fm: dict[str, Any], path: Path) -> str:
    for key in ("last_updated_utc", "last_canonicalized_utc", "enriched_at_utc"):
        if key in fm:
            iso = _to_iso_string(fm[key])
            if iso:
                return iso
    return _mtime_iso(path)


def _iter_md_files(directory: Path) -> list[Path]:
    if not directory.exists() or not directory.is_dir():
        return []
    return sorted(p for p in directory.glob("*.md") if p.is_file())


def walk_sources(sources_dir: Path) -> list[GraphNode]:
    nodes: list[GraphNode] = []
    for path in _iter_md_files(sources_dir):
        fm = _load_frontmatter(path)
        if not fm:
            continue
        node_id = fm.get("id")
        if not isinstance(node_id, str) or not node_id:
            continue
        trust_level = fm.get("trust_level") or "tertiary"
        if trust_level not in ALLOWED_TRUST_LEVELS:
            trust_level = "tertiary"
        node = GraphNode(
            id=node_id,
            type="source",
            slug=path.stem,
            trust_level=trust_level,
            last_updated_utc=_resolve_date(fm, path),
        )
        try:
            validate_node(node)
        except ValueError:
            continue
        nodes.append(node)
    nodes.sort(key=lambda n: n.id)
    return nodes


def walk_concepts(concepts_dir: Path) -> list[GraphNode]:
    nodes: list[GraphNode] = []
    for path in _iter_md_files(concepts_dir):
        fm = _load_frontmatter(path)
        if not fm:
            continue
        node_id = fm.get("id")
        if not isinstance(node_id, str) or not node_id:
            continue
        node = GraphNode(
            id=node_id,
            type="concept",
            slug=path.stem,
            trust_level="derived",
            last_updated_utc=_resolve_date(fm, path),
        )
        try:
            validate_node(node)
        except ValueError:
            continue
        nodes.append(node)
    nodes.sort(key=lambda n: n.id)
    return nodes
