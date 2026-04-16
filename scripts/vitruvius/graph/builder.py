from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

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


def _iter_md_files(
    directory: Path,
    *,
    allowed_paths: Iterable[Path] | None = None,
    constrain_to_directory: bool = True,
) -> list[Path]:
    if allowed_paths is not None:
        resolved_dir = directory.resolve()
        normalized: list[Path] = []
        for path in allowed_paths:
            resolved = Path(path).resolve()
            if constrain_to_directory:
                try:
                    resolved.relative_to(resolved_dir)
                except ValueError:
                    continue
            if resolved.is_file() and resolved.suffix == ".md":
                normalized.append(resolved)
        return sorted(set(normalized))
    if not directory.exists() or not directory.is_dir():
        return []
    return sorted(p.resolve() for p in directory.glob("*.md") if p.is_file())


def _slugify_id(value: str) -> str:
    return value.replace("_", "-")


def _iter_frontmatter_relationships(fm: dict[str, Any]) -> list[tuple[str, str]]:
    raw = fm.get("relationships")
    if not isinstance(raw, list):
        return []
    pairs: list[tuple[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        for predicate, target in item.items():
            if not (isinstance(predicate, str) and isinstance(target, str)):
                continue
            if not predicate.strip() or not target.strip():
                continue
            pairs.append((predicate, target))
    return pairs


def _collect_unresolved_frontmatter_source_ids(
    sources_dir: Path,
    *,
    referenced_node_ids: set[str],
    valid_target_ids: set[str],
    allowed_paths: Iterable[Path] | None = None,
) -> set[str]:
    unresolved_ids: set[str] = set()
    for path in _iter_md_files(sources_dir, allowed_paths=allowed_paths):
        fm = _load_frontmatter(path)
        if not fm:
            continue
        node_id = fm.get("id")
        if not isinstance(node_id, str) or not node_id or node_id in referenced_node_ids:
            continue
        relationships = _iter_frontmatter_relationships(fm)
        if not relationships:
            continue
        if any(target_id in valid_target_ids for _, target_id in relationships):
            continue
        unresolved_ids.add(node_id)
    return unresolved_ids


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


def walk_sources(
    sources_dir: Path,
    *,
    referenced_node_ids: set[str] | None = None,
    allowed_paths: Iterable[Path] | None = None,
) -> list[GraphNode]:
    nodes: list[GraphNode] = []
    for path in _iter_md_files(sources_dir, allowed_paths=allowed_paths):
        fm = _load_frontmatter(path)
        if not fm:
            continue
        node_id = fm.get("id")
        if not isinstance(node_id, str) or not node_id:
            continue
        if referenced_node_ids is not None and node_id not in referenced_node_ids:
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


def walk_concepts(
    concepts_dir: Path,
    *,
    referenced_node_ids: set[str] | None = None,
    allowed_paths: Iterable[Path] | None = None,
) -> list[GraphNode]:
    nodes: list[GraphNode] = []
    for path in _iter_md_files(concepts_dir, allowed_paths=allowed_paths):
        fm = _load_frontmatter(path)
        if not fm:
            continue
        node_id = fm.get("id")
        if not isinstance(node_id, str) or not node_id:
            continue
        if referenced_node_ids is not None:
            has_regulatory_basis = isinstance(fm.get("regulatory_basis"), list) and bool(
                fm.get("regulatory_basis")
            )
            if node_id not in referenced_node_ids and not has_regulatory_basis:
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


def walk_relationships(
    relationships_dir: Path,
    *,
    allowed_paths: Iterable[Path] | None = None,
) -> list[GraphEdge]:
    edges: list[GraphEdge] = []
    for path in _iter_md_files(
        relationships_dir,
        allowed_paths=allowed_paths,
        constrain_to_directory=False,
    ):
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


def walk_source_relationship_edges(
    sources_dir: Path,
    *,
    valid_target_ids: set[str],
    allowed_paths: Iterable[Path] | None = None,
) -> list[GraphEdge]:
    edges: list[GraphEdge] = []
    for path in _iter_md_files(sources_dir, allowed_paths=allowed_paths):
        fm = _load_frontmatter(path)
        if not fm:
            continue
        source_id = fm.get("id")
        if not isinstance(source_id, str) or not source_id:
            continue
        for predicate, target_id in _iter_frontmatter_relationships(fm):
            if target_id not in valid_target_ids:
                continue
            evidence_id = (
                f"rel-meta-{_slugify_id(source_id)}-"
                f"{_slugify_id(predicate)}-{_slugify_id(target_id)}"
            )
            edge = GraphEdge(
                from_id=source_id,
                to_id=target_id,
                type=predicate,
                evidence_id=evidence_id,
                status="verified",
                evidence_source_id=source_id,
                evidence_snippet=f"frontmatter relationship: {predicate}",
            )
            try:
                validate_edge(edge)
            except ValueError:
                continue
            edges.append(edge)
    edges.sort(key=lambda e: (e.from_id, e.type, e.to_id, e.evidence_id))
    return edges


def walk_concept_basis_edges(
    concepts_dir: Path,
    *,
    valid_source_ids: set[str],
    allowed_paths: Iterable[Path] | None = None,
) -> list[GraphEdge]:
    edges: list[GraphEdge] = []
    for path in _iter_md_files(concepts_dir, allowed_paths=allowed_paths):
        fm = _load_frontmatter(path)
        if not fm:
            continue
        concept_id = fm.get("id")
        if not isinstance(concept_id, str) or not concept_id:
            continue
        raw_basis = fm.get("regulatory_basis")
        if not isinstance(raw_basis, list):
            continue
        for entry in raw_basis:
            if not isinstance(entry, dict):
                continue
            source_id = entry.get("source_id")
            if not isinstance(source_id, str) or source_id not in valid_source_ids:
                continue
            section_id = entry.get("section_id")
            section_slug = (
                _slugify_id(section_id)
                if isinstance(section_id, str) and section_id.strip()
                else "no-section"
            )
            edge = GraphEdge(
                from_id=source_id,
                to_id=concept_id,
                type="defines",
                evidence_id=(
                    f"rel-basis-{_slugify_id(source_id)}-"
                    f"{_slugify_id(concept_id)}-{section_slug}"
                ),
                status="verified",
                evidence_source_id=source_id,
                evidence_source_section_id=(
                    section_id if isinstance(section_id, str) and section_id.strip() else None
                ),
                evidence_snippet=(
                    str(entry.get("evidence_snippet"))
                    if entry.get("evidence_snippet")
                    else None
                ),
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
    source_paths: Iterable[Path] | None = None,
    concept_paths: Iterable[Path] | None = None,
    relationship_paths: Iterable[Path] | None = None,
    metadata: dict[str, Any] | None = None,
) -> GraphSnapshot:
    raw_sources = walk_sources(canonical_root / "sources", allowed_paths=source_paths)
    raw_concepts = walk_concepts(canonical_root / "concepts", allowed_paths=concept_paths)
    valid_source_ids = {node.id for node in raw_sources}
    valid_concept_ids = {node.id for node in raw_concepts}
    source_id_counts: dict[str, int] = {}
    concept_id_counts: dict[str, int] = {}
    for node in raw_sources:
        source_id_counts[node.id] = source_id_counts.get(node.id, 0) + 1
    for node in raw_concepts:
        concept_id_counts[node.id] = concept_id_counts.get(node.id, 0) + 1

    relationship_edges = walk_relationships(
        canonical_root / "relationships",
        allowed_paths=relationship_paths,
    )
    source_relationship_edges = walk_source_relationship_edges(
        canonical_root / "sources",
        valid_target_ids=valid_source_ids | valid_concept_ids,
        allowed_paths=source_paths,
    )
    concept_basis_edges = walk_concept_basis_edges(
        canonical_root / "concepts",
        valid_source_ids=valid_source_ids,
        allowed_paths=concept_paths,
    )
    edges = relationship_edges + source_relationship_edges + concept_basis_edges
    referenced_node_ids = {edge.from_id for edge in edges} | {edge.to_id for edge in edges}
    referenced_node_ids.update(
        {node_id for node_id, count in source_id_counts.items() if count > 1}
    )
    referenced_node_ids.update(
        {node_id for node_id, count in concept_id_counts.items() if count > 1}
    )
    unresolved_frontmatter_source_ids = _collect_unresolved_frontmatter_source_ids(
        canonical_root / "sources",
        referenced_node_ids=referenced_node_ids,
        valid_target_ids=valid_source_ids | valid_concept_ids,
        allowed_paths=source_paths,
    )

    sources = [
        node
        for node in raw_sources
        if not (
            node.id in unresolved_frontmatter_source_ids
            and source_id_counts.get(node.id, 0) == 1
        )
    ]
    concepts = walk_concepts(
        canonical_root / "concepts",
        referenced_node_ids=referenced_node_ids,
        allowed_paths=concept_paths,
    )

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
        metadata=metadata,
    )
