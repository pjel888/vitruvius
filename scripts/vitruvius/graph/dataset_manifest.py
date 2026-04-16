from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml

from .contract import GraphSnapshot


class DatasetManifestError(ValueError):
    pass


@dataclass(frozen=True)
class DatasetFileEntry:
    path: Path
    relative_path: str
    folder_name: str
    entry_role: str
    authority_tier: str
    variant_family: str
    edition_or_source_note: str
    include_in_m1: bool
    reason: str


@dataclass(frozen=True)
class DatasetRawAnchor:
    folder_name: str
    raw_root: Path
    relative_raw_root: str
    entry_role: str
    authority_tier: str
    variant_family: str
    edition_or_source_note: str
    include_in_m1: bool
    reason: str
    classified_raw_entries: tuple[DatasetFileEntry, ...]


@dataclass(frozen=True)
class DatasetManifest:
    manifest_path: Path
    dataset_id: str
    dataset_kind: str
    raw_slice_anchors: tuple[DatasetRawAnchor, ...]
    source_entries: tuple[DatasetFileEntry, ...]
    concept_entries: tuple[DatasetFileEntry, ...]
    relationship_entries: tuple[DatasetFileEntry, ...]
    graph_output_root: Path
    graph_output_root_rel: str
    run_output_root: Path
    run_output_root_rel: str
    query_snapshot_path_template: str | None
    freshness_policy: dict[str, Any]
    pilot_gate: dict[str, Any]
    scope_notes: tuple[str, ...]


@dataclass(frozen=True)
class DatasetBuildPaths:
    snapshot_path: Path
    snapshot_rel: str
    integrity_path: Path
    integrity_rel: str
    build_report_path: Path
    build_report_rel: str


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise DatasetManifestError(f"unable to read dataset manifest: {path}") from exc
    except yaml.YAMLError as exc:
        raise DatasetManifestError(f"invalid YAML in dataset manifest: {path}") from exc
    if not isinstance(payload, dict):
        raise DatasetManifestError("dataset manifest must be a mapping at the top level")
    return payload


def _require_str(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DatasetManifestError(f"dataset manifest field {key!r} must be a non-empty string")
    return value.strip()


def _require_bool(payload: dict[str, Any], key: str) -> bool:
    value = payload.get(key)
    if not isinstance(value, bool):
        raise DatasetManifestError(f"dataset manifest field {key!r} must be a boolean")
    return value


def _require_list(payload: dict[str, Any], key: str) -> list[Any]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise DatasetManifestError(f"dataset manifest field {key!r} must be a list")
    return value


def _optional_notes(payload: dict[str, Any], key: str) -> tuple[str, ...]:
    raw = payload.get(key)
    if raw is None:
        return ()
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise DatasetManifestError(f"dataset manifest field {key!r} must be a list of strings")
    return tuple(item.strip() for item in raw if item.strip())


def _resolve_repo_relative_path(repo_root: Path, raw_path: str, *, what: str) -> tuple[Path, str]:
    rel = raw_path.strip()
    if not rel:
        raise DatasetManifestError(f"{what} path must be non-empty")
    abs_path = (repo_root / rel).resolve()
    try:
        abs_path.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise DatasetManifestError(f"{what} path escapes repo root: {raw_path}") from exc
    return abs_path, rel


def _parse_file_entry(repo_root: Path, payload: dict[str, Any], *, what: str) -> DatasetFileEntry:
    raw_path = _require_str(payload, "path")
    path, relative_path = _resolve_repo_relative_path(repo_root, raw_path, what=what)
    if not path.exists() or not path.is_file():
        raise DatasetManifestError(f"{what} file does not exist: {relative_path}")
    return DatasetFileEntry(
        path=path,
        relative_path=relative_path,
        folder_name=_require_str(payload, "folder_name"),
        entry_role=_require_str(payload, "entry_role"),
        authority_tier=_require_str(payload, "authority_tier"),
        variant_family=_require_str(payload, "variant_family"),
        edition_or_source_note=_require_str(payload, "edition_or_source_note"),
        include_in_m1=_require_bool(payload, "include_in_m1"),
        reason=_require_str(payload, "reason"),
    )


def _parse_raw_anchor(repo_root: Path, payload: dict[str, Any]) -> DatasetRawAnchor:
    raw_root_value = _require_str(payload, "raw_root")
    raw_root, raw_root_rel = _resolve_repo_relative_path(
        repo_root, raw_root_value, what=f"raw_slice_anchor {raw_root_value!r}"
    )
    if not raw_root.exists() or not raw_root.is_dir():
        raise DatasetManifestError(f"raw_slice_anchor root does not exist: {raw_root_rel}")
    classified_entries = payload.get("classified_raw_entries", [])
    if not isinstance(classified_entries, list):
        raise DatasetManifestError("raw_slice_anchor field 'classified_raw_entries' must be a list")
    parsed_entries: list[DatasetFileEntry] = []
    for entry in classified_entries:
        if not isinstance(entry, dict):
            raise DatasetManifestError(
                f"classified raw entry in {raw_root_rel} must be a mapping"
            )
        parsed_entries.append(
            _parse_file_entry(repo_root, entry, what=f"classified raw entry in {raw_root_rel}")
        )
    return DatasetRawAnchor(
        folder_name=_require_str(payload, "folder_name"),
        raw_root=raw_root,
        relative_raw_root=raw_root_rel,
        entry_role=_require_str(payload, "entry_role"),
        authority_tier=_require_str(payload, "authority_tier"),
        variant_family=_require_str(payload, "variant_family"),
        edition_or_source_note=_require_str(payload, "edition_or_source_note"),
        include_in_m1=_require_bool(payload, "include_in_m1"),
        reason=_require_str(payload, "reason"),
        classified_raw_entries=tuple(parsed_entries),
    )


def _require_manifest_section(payload: dict[str, Any], key: str) -> dict[str, Any]:
    section = payload.get(key)
    if not isinstance(section, dict):
        raise DatasetManifestError(f"dataset manifest field {key!r} must be a mapping")
    return section


def _parse_entry_list(
    repo_root: Path,
    items: list[Any],
    *,
    what: str,
) -> tuple[DatasetFileEntry, ...]:
    parsed: list[DatasetFileEntry] = []
    for item in items:
        if not isinstance(item, dict):
            raise DatasetManifestError(f"each {what} entry must be a mapping")
        parsed.append(_parse_file_entry(repo_root, item, what=f"{what} entry"))
    return tuple(parsed)


def _frontmatter_for(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data = yaml.safe_load(text[3:end].strip())
    return data if isinstance(data, dict) else {}


def _id_for(path: Path) -> str | None:
    frontmatter = _frontmatter_for(path)
    node_id = frontmatter.get("id")
    return node_id if isinstance(node_id, str) and node_id.strip() else None


def _relative_paths(entries: Iterable[DatasetFileEntry]) -> list[str]:
    return [entry.relative_path for entry in entries if entry.include_in_m1]


def load_dataset_manifest(manifest_path: Path, repo_root: Path) -> DatasetManifest:
    manifest_path = manifest_path.resolve()
    payload = _load_yaml(manifest_path)
    raw_slice = payload.get("raw_slice_anchors")
    if not isinstance(raw_slice, list) or not raw_slice:
        raise DatasetManifestError("dataset manifest requires a non-empty raw_slice_anchors list")

    canonical = _require_manifest_section(payload, "canonical_input_manifest")
    relationships = _require_manifest_section(payload, "relationship_input_manifest")
    freshness_policy = _require_manifest_section(payload, "freshness_policy")
    pilot_gate = _require_manifest_section(payload, "pilot_gate")

    graph_output_root_rel = _require_str(payload, "graph_output_root")
    run_output_root_rel = _require_str(payload, "run_output_root")
    graph_output_root, _ = _resolve_repo_relative_path(repo_root, graph_output_root_rel, what="graph_output_root")
    run_output_root, _ = _resolve_repo_relative_path(repo_root, run_output_root_rel, what="run_output_root")

    raw_anchor_items: list[DatasetRawAnchor] = []
    for item in raw_slice:
        if not isinstance(item, dict):
            raise DatasetManifestError("each raw_slice_anchor entry must be a mapping")
        raw_anchor_items.append(_parse_raw_anchor(repo_root, item))
    raw_anchors = tuple(raw_anchor_items)

    source_entries = _parse_entry_list(
        repo_root,
        _require_list(canonical, "sources"),
        what="canonical source",
    )
    concept_entries = _parse_entry_list(
        repo_root,
        _require_list(canonical, "concepts"),
        what="canonical concept",
    )
    relationship_entries = _parse_entry_list(
        repo_root,
        _require_list(relationships, "relationships"),
        what="relationship input",
    )

    if not any(entry.include_in_m1 for entry in source_entries):
        raise DatasetManifestError("dataset manifest must include at least one canonical source entry for M1")
    if not any(entry.include_in_m1 for entry in relationship_entries):
        raise DatasetManifestError("dataset manifest must include at least one relationship input entry for M1")

    return DatasetManifest(
        manifest_path=manifest_path,
        dataset_id=_require_str(payload, "dataset_id"),
        dataset_kind=_require_str(payload, "dataset_kind"),
        raw_slice_anchors=raw_anchors,
        source_entries=source_entries,
        concept_entries=concept_entries,
        relationship_entries=relationship_entries,
        graph_output_root=graph_output_root,
        graph_output_root_rel=graph_output_root_rel,
        run_output_root=run_output_root,
        run_output_root_rel=run_output_root_rel,
        query_snapshot_path_template=(
            payload.get("query_snapshot_path_template").strip()
            if isinstance(payload.get("query_snapshot_path_template"), str)
            and payload.get("query_snapshot_path_template").strip()
            else None
        ),
        freshness_policy=freshness_policy,
        pilot_gate=pilot_gate,
        scope_notes=_optional_notes(payload, "scope_notes"),
    )


def manifest_hash(manifest: DatasetManifest) -> str:
    return hashlib.sha256(manifest.manifest_path.read_bytes()).hexdigest()


def selected_source_paths(manifest: DatasetManifest) -> tuple[Path, ...]:
    return tuple(entry.path for entry in manifest.source_entries if entry.include_in_m1)


def selected_concept_paths(manifest: DatasetManifest) -> tuple[Path, ...]:
    return tuple(entry.path for entry in manifest.concept_entries if entry.include_in_m1)


def selected_relationship_paths(manifest: DatasetManifest) -> tuple[Path, ...]:
    return tuple(entry.path for entry in manifest.relationship_entries if entry.include_in_m1)


def selected_input_paths(manifest: DatasetManifest) -> tuple[Path, ...]:
    return (
        selected_source_paths(manifest)
        + selected_concept_paths(manifest)
        + selected_relationship_paths(manifest)
    )


def input_fingerprint(manifest: DatasetManifest, repo_root: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    combined = hashlib.sha256()
    for path in sorted(selected_input_paths(manifest)):
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        rel = str(path.relative_to(repo_root))
        stat = path.stat()
        files.append({
            "path": rel,
            "sha256": digest,
            "size_bytes": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
        })
        combined.update(rel.encode("utf-8"))
        combined.update(b"\0")
        combined.update(digest.encode("utf-8"))
        combined.update(b"\0")
    return {
        "combined_sha256": combined.hexdigest(),
        "file_count": len(files),
        "files": files,
    }


def build_run_paths(manifest: DatasetManifest, *, repo_root: Path, run_id: str) -> DatasetBuildPaths:
    snapshot_rel = (
        manifest.query_snapshot_path_template.format(run_id=run_id)
        if manifest.query_snapshot_path_template is not None
        else f"{manifest.graph_output_root_rel}/{run_id}_graph_snapshot.json"
    )
    snapshot_path, snapshot_rel = _resolve_repo_relative_path(
        repo_root, snapshot_rel, what="dataset snapshot output"
    )
    integrity_rel = f"{manifest.graph_output_root_rel}/{run_id}_graph_integrity_report.json"
    integrity_path, integrity_rel = _resolve_repo_relative_path(
        repo_root, integrity_rel, what="dataset integrity output"
    )
    build_report_rel = f"{manifest.run_output_root_rel}/{run_id}_build_graph_dataset_report.json"
    build_report_path, build_report_rel = _resolve_repo_relative_path(
        repo_root, build_report_rel, what="dataset build report output"
    )
    return DatasetBuildPaths(
        snapshot_path=snapshot_path,
        snapshot_rel=snapshot_rel,
        integrity_path=integrity_path,
        integrity_rel=integrity_rel,
        build_report_path=build_report_path,
        build_report_rel=build_report_rel,
    )


def snapshot_metadata(
    manifest: DatasetManifest,
    *,
    repo_root: Path,
    run_id: str,
    snapshot_rel: str,
    integrity_rel: str,
) -> dict[str, Any]:
    manifest_rel = str(manifest.manifest_path.relative_to(repo_root))
    return {
        "dataset_id": manifest.dataset_id,
        "dataset_kind": manifest.dataset_kind,
        "run_id": run_id,
        "manifest_path": manifest_rel,
        "manifest_hash": manifest_hash(manifest),
        "input_fingerprint": input_fingerprint(manifest, repo_root),
        "upstream_artifact_refs": {
            "canonical_sources": _relative_paths(manifest.source_entries),
            "canonical_concepts": _relative_paths(manifest.concept_entries),
            "relationship_inputs": _relative_paths(manifest.relationship_entries),
        },
        "scope_notes": list(manifest.scope_notes),
        "freshness_policy": manifest.freshness_policy,
        "pilot_gate": manifest.pilot_gate,
        "selected_snapshot_path": snapshot_rel,
        "selected_integrity_report_path": integrity_rel,
    }


def _node_folder_map(manifest: DatasetManifest) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for entry in (*manifest.source_entries, *manifest.concept_entries):
        if not entry.include_in_m1:
            continue
        node_id = _id_for(entry.path)
        if node_id:
            mapping[node_id] = entry.folder_name
    return mapping


def _relationship_folder_map(manifest: DatasetManifest) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for entry in manifest.relationship_entries:
        if not entry.include_in_m1:
            continue
        evidence_id = _id_for(entry.path)
        if evidence_id:
            mapping[evidence_id] = entry.folder_name
    return mapping


def coverage_rows(manifest: DatasetManifest, snapshot: GraphSnapshot) -> list[dict[str, Any]]:
    node_folder_map = _node_folder_map(manifest)
    relationship_folder_map = _relationship_folder_map(manifest)
    rows: list[dict[str, Any]] = []

    for anchor in manifest.raw_slice_anchors:
        raw_file_count = len([p for p in anchor.raw_root.glob("*") if p.is_file()])
        canonical_count = sum(
            1
            for entry in (*manifest.source_entries, *manifest.concept_entries)
            if entry.include_in_m1 and entry.folder_name == anchor.folder_name
        )
        relationship_count = sum(
            1
            for entry in manifest.relationship_entries
            if entry.include_in_m1 and entry.folder_name == anchor.folder_name
        )
        node_count = sum(1 for node in snapshot.nodes if node_folder_map.get(node.id) == anchor.folder_name)

        edge_count = 0
        for edge in snapshot.edges:
            folders: set[str] = set()
            evidence_folder = relationship_folder_map.get(edge.evidence_id)
            if evidence_folder:
                folders.add(evidence_folder)
            from_folder = node_folder_map.get(edge.from_id)
            to_folder = node_folder_map.get(edge.to_id)
            if from_folder:
                folders.add(from_folder)
            if to_folder:
                folders.add(to_folder)
            if anchor.folder_name in folders:
                edge_count += 1

        if edge_count > 0:
            status = "covered"
            notes = "selected truth-bearing inputs contributed nodes/edges"
        elif node_count > 0:
            status = "partial"
            notes = "selected truth-bearing inputs contributed source/concept nodes only; no relationship-backed edges yet"
        elif canonical_count > 0 or relationship_count > 0:
            status = "partial"
            notes = "selected inputs exist but contributed no edges/nodes in this run"
        elif anchor.include_in_m1:
            status = "blocked"
            notes = "no canonical or approved relationship inputs selected for this folder"
        else:
            status = "deferred"
            notes = anchor.reason

        rows.append({
            "folder_name": anchor.folder_name,
            "raw_file_count": raw_file_count,
            "converted_count": None,
            "refined_count": None,
            "canonical_count": canonical_count,
            "approved_relationship_input_count": relationship_count,
            "node_count_contributed": node_count,
            "edge_count_contributed": edge_count,
            "status": status,
            "notes": notes,
        })
    return rows


def thin_graph_metrics(snapshot: GraphSnapshot, coverage: list[dict[str, Any]]) -> dict[str, Any]:
    adjacency: dict[str, set[str]] = {node.id: set() for node in snapshot.nodes}
    for edge in snapshot.edges:
        adjacency.setdefault(edge.from_id, set()).add(edge.to_id)
        adjacency.setdefault(edge.to_id, set()).add(edge.from_id)

    visited: set[str] = set()
    components = 0
    for node_id in sorted(adjacency):
        if node_id in visited:
            continue
        components += 1
        stack = [node_id]
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            stack.extend(sorted(adjacency.get(current, set()) - visited))

    isolated_nodes = sorted(node_id for node_id, neighbors in adjacency.items() if not neighbors)
    edge_types = sorted({edge.type for edge in snapshot.edges})
    return {
        "connected_component_count": components,
        "isolated_node_count": len(isolated_nodes),
        "isolated_node_rate": (
            round(len(isolated_nodes) / len(snapshot.nodes), 6) if snapshot.nodes else 0.0
        ),
        "edge_type_diversity": {
            "count": len(edge_types),
            "types": edge_types,
        },
        "per_folder_node_edge_balance": {
            row["folder_name"]: {
                "node_count_contributed": row["node_count_contributed"],
                "edge_count_contributed": row["edge_count_contributed"],
                "status": row["status"],
            }
            for row in coverage
        },
    }


def incomplete_from_coverage(coverage: list[dict[str, Any]]) -> bool:
    return any(row["status"] in {"partial", "blocked", "deferred"} for row in coverage)


def dataset_build_report(
    manifest: DatasetManifest,
    *,
    repo_root: Path,
    run_id: str,
    dry_run: bool,
    snapshot: GraphSnapshot,
    integrity_payload: dict[str, Any],
    snapshot_rel: str,
    integrity_rel: str,
) -> dict[str, Any]:
    coverage = coverage_rows(manifest, snapshot)
    thin_metrics = thin_graph_metrics(snapshot, coverage)
    report = {
        "action": "build-graph",
        "mode": "dataset",
        "dry_run": dry_run,
        "dataset_id": manifest.dataset_id,
        "dataset_kind": manifest.dataset_kind,
        "run_id": run_id,
        "manifest_path": str(manifest.manifest_path.relative_to(repo_root)),
        "manifest_hash": manifest_hash(manifest),
        "snapshot_path": snapshot_rel,
        "integrity_report_path": integrity_rel,
        "node_count": snapshot.node_count,
        "edge_count": snapshot.edge_count,
        "integrity": integrity_payload,
        "coverage": coverage,
        "thin_graph_metrics": thin_metrics,
        "incomplete": incomplete_from_coverage(coverage),
        "artifact_metadata": snapshot.metadata,
    }
    return report


def write_json_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False)
    path.write_text(text + "\n", encoding="utf-8")


def provenance_for_snapshot(snapshot: GraphSnapshot, *, snapshot_path: str) -> dict[str, Any] | None:
    metadata = snapshot.metadata or {}
    dataset_id = metadata.get("dataset_id")
    run_id = metadata.get("run_id")
    manifest_hash_value = metadata.get("manifest_hash")
    if not dataset_id and not run_id and not manifest_hash_value:
        return None
    return {
        "snapshot_path": snapshot_path,
        "dataset_id": dataset_id,
        "run_id": run_id,
        "manifest_hash": manifest_hash_value,
    }


def render_query_provenance(provenance: dict[str, Any] | None) -> str:
    if provenance is None:
        return ""
    lines = ["Snapshot provenance:"]
    for key in ("snapshot_path", "dataset_id", "run_id", "manifest_hash"):
        value = provenance.get(key)
        if value:
            lines.append(f"  {key}: {value}")
    return "\n".join(lines) + "\n\n"
