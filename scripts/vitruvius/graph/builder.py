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


def _primary_evidence_entry(fm: dict[str, Any]) -> dict[str, Any] | None:
    raw = fm.get("evidence")
    if not isinstance(raw, list):
        return None
    entries = [entry for entry in raw if isinstance(entry, dict)]
    if not entries:
        return None

    def _sort_key(entry: dict[str, Any]) -> tuple[float, int]:
        confidence_raw = entry.get("reviewer_confidence")
        try:
            confidence = float(confidence_raw)
        except (TypeError, ValueError):
            confidence = -1.0
        return (confidence, -len(str(entry.get("evidence_snippet") or "")))

    return max(entries, key=_sort_key)


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


def walk_relationships(relationships_dir: Path) -> list[GraphEdge]:
    edges: list[GraphEdge] = []
    for path in _iter_md_files(relationships_dir):
        fm = _load_frontmatter(path)
        if not fm:
            continue
        status_raw = fm.get("canonical_status")
        if status_raw not in _PROMOTED_STATUSES:
            continue
        evidence_id = fm.get("id")
        if not isinstance(evidence_id, str) or not evidence_id.startswith("rel-"):
            continue
        from_id = fm.get("from_entity") or fm.get("from_id")
        to_id = fm.get("to_entity") or fm.get("to_id")
        predicate = fm.get("relationship_type") or fm.get("predicate")
        if not (isinstance(from_id, str) and isinstance(to_id, str) and isinstance(predicate, str)):
            continue
        edge_status = "verified" if status_raw == "verified" else "unverified"
        governing = fm.get("is_governing_standard")
        if isinstance(governing, bool):
            governing_value: bool | None = governing
        else:
            governing_value = None
        evidence = _primary_evidence_entry(fm)
        reviewer_confidence: float | None = None
        if evidence is not None:
            try:
                reviewer_confidence = float(evidence.get("reviewer_confidence"))
            except (TypeError, ValueError):
                reviewer_confidence = None
        edge = GraphEdge(
            from_id=from_id,
            to_id=to_id,
            type=predicate,
            evidence_id=evidence_id,
            status=edge_status,
            evidence_source_id=(
                str(evidence.get("source_id")) if evidence and evidence.get("source_id") else None
            ),
            evidence_source_section_id=(
                str(evidence.get("source_section_id"))
                if evidence and evidence.get("source_section_id")
                else None
            ),
            evidence_snippet=(
                str(evidence.get("evidence_snippet"))
                if evidence and evidence.get("evidence_snippet")
                else None
            ),
            reviewer_confidence=reviewer_confidence,
            is_governing_standard=governing_value,
        )
        try:
            validate_edge(edge)
        except ValueError:
            continue
        edges.append(edge)
    edges.sort(key=lambda e: (e.from_id, e.type, e.to_id, e.evidence_id))
    return edges


def build_snapshot(
    canonical_root: Path,
    *,
    schema_version: str = "1.0.0",
    now: str | None = None,
) -> GraphSnapshot:
    sources = walk_sources(canonical_root / "sources")
    concepts = walk_concepts(canonical_root / "concepts")
    edges = walk_relationships(canonical_root / "relationships")

    nodes = sources + concepts
    nodes.sort(key=lambda n: n.id)
    edges = sorted(edges, key=lambda e: (e.from_id, e.type, e.to_id, e.evidence_id))

    generated_at_utc = now or datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return GraphSnapshot(
        schema_version=schema_version,
        generated_at_utc=generated_at_utc,
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )
