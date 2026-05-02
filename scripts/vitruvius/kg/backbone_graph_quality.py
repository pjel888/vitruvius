"""File-backed quality metrics and guards for AEC-MEPFS Backbone graphs."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict, deque
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

REPORT_SCHEMA_VERSION = "aec-mepfs-backbone-graph-quality-report/v1"
DEFAULT_FIXTURE_PATH = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/graph-quality")
REPORT_FILENAME = "graph-quality-report.json"
DUPLICATE_LABEL_CONTEXT_FILENAME = "duplicate-label-context-index.json"
RAW_SOURCE_ROOT = Path("001_Raw-Source-Layer")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
PLACEHOLDER_RE = re.compile(r"\b(example|generic|placeholder|sample|tbd|future relationship|miscellaneous)\b", re.I)
GENERIC_RELATIONS = {"related_to", "connected_to", "similar_to", "affects"}
REQUIRED_ENRICHED_EDGE_FIELDS = {
    "relation_type",
    "relation_category",
    "relation_nature",
    "direction",
    "weight",
    "confidence_score",
    "discipline",
    "lifecycle_phase",
    "source_family_ids",
    "rationale",
    "provenance_note",
}
ALLOWED_DISCIPLINES = {
    "accessibility",
    "aec",
    "architecture",
    "civil",
    "commissioning",
    "compliance",
    "construction",
    "cultural_history",
    "digital_delivery",
    "electrical",
    "fire_safety",
    "geotechnical",
    "materials",
    "mechanical",
    "operations",
    "performance",
    "plumbing",
    "smart_systems",
    "structural",
    "sustainability",
}
ALLOWED_LIFECYCLE = {
    "planning",
    "design",
    "construction",
    "inspection",
    "commissioning",
    "handover",
    "operation",
    "maintenance",
    "reuse",
}
ALLOWED_RELATION_CATEGORIES = {
    "civil_hydraulic_flow",
    "construction_process",
    "coordination",
    "dependency",
    "functional_service",
    "information_management",
    "lifecycle_process",
    "material_behavior",
    "performance",
    "performance_sustainability",
    "physical_composition",
    "regulatory_authority",
    "risk",
    "risk_failure",
    "site_condition",
    "spatial_topological",
    "structural_load_path",
    "system_flow",
    "taxonomy",
}


def analyze_backbone_graph_quality(
    payload: dict[str, Any],
    *,
    introduced_generation_method: str | None = None,
    source_rights_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    records = _dict_list(payload.get("records"))
    relationships = _dict_list(payload.get("relationships"))
    nodes = [row for row in records if row.get("record_type") == "BackboneNode"]
    node_ids = {str(row.get("id") or "") for row in nodes}
    node_ids.discard("")
    relationship_endpoints = {
        str(row.get("from_id") or "") for row in relationships
    } | {str(row.get("to_id") or "") for row in relationships}
    relationship_endpoints.discard("")
    path_by_id = {str(row.get("id") or ""): str(row.get("path_code") or "") for row in nodes}
    label_counts = Counter(_norm(row.get("label")) for row in nodes if _norm(row.get("label")))
    labels_by_parent = defaultdict(list)
    for row in nodes:
        normalized_label = _norm(row.get("label"))
        if not normalized_label:
            continue
        labels_by_parent[(str(row.get("parent_path_code") or ""), normalized_label)].append(row)
    introduced_edges = [
        row
        for row in relationships
        if introduced_generation_method is None
        or row.get("generation_method") == introduced_generation_method
    ]
    introduced_node_ids = {
        str(row.get("id") or "")
        for row in nodes
        if introduced_generation_method is None
        or row.get("generation_method") == introduced_generation_method
    }
    source_ids = _source_ids(source_rights_payload)

    errors: list[str] = []
    warnings: list[str] = []
    for node in nodes:
        node_id = str(node.get("id") or "")
        label = str(node.get("label") or "")
        definition = str(node.get("definition") or "")
        if PLACEHOLDER_RE.search(label):
            errors.append(f"node {node_id}: placeholder-like label {label!r}")
        if node_id in introduced_node_ids and PLACEHOLDER_RE.search(definition):
            errors.append(f"node {node_id}: placeholder-like definition")
        if node_id in introduced_node_ids and len(definition.strip()) < 20:
            errors.append(f"node {node_id}: introduced node requires a substantive definition")
        if source_ids is not None:
            missing_node_sources = sorted(set(_string_list(node.get("source_family_ids"))) - source_ids)
            if missing_node_sources:
                errors.append(f"node {node_id}: source_family_ids not in registry {missing_node_sources}")

    for index, rel in enumerate(relationships):
        from_id = str(rel.get("from_id") or "")
        to_id = str(rel.get("to_id") or "")
        predicate = str(rel.get("predicate") or rel.get("edge_type") or "")
        if from_id not in node_ids:
            errors.append(f"relationships[{index}].from_id: missing BackboneNode {from_id!r}")
        if to_id not in node_ids:
            errors.append(f"relationships[{index}].to_id: missing BackboneNode {to_id!r}")
        if predicate in GENERIC_RELATIONS and bool(rel.get("governed", True)):
            errors.append(f"relationships[{index}].predicate: generic governed relationship {predicate!r} is blocked")
        if (
            from_id
            and to_id
            and from_id == to_id
        ):
            errors.append(f"relationships[{index}]: self-loop is blocked for governed Backbone relationships")
        if source_ids is not None:
            missing_sources = sorted(set(_string_list(rel.get("source_family_ids"))) - source_ids)
            if missing_sources:
                errors.append(f"relationship {_relationship_key(rel)}: source_family_ids not in registry {missing_sources}")

    for rel in introduced_edges:
        key = _relationship_key(rel)
        for field in sorted(REQUIRED_ENRICHED_EDGE_FIELDS):
            if not _has_value(rel.get(field)):
                errors.append(f"relationship {key}: missing enriched metadata field {field}")
        for number_field in ("weight", "confidence_score"):
            value = _as_float(rel.get(number_field))
            if value is None or value < 0 or value > 1:
                errors.append(f"relationship {key}: {number_field} must be between 0 and 1")
        disciplines = _string_list(rel.get("discipline"))
        unknown_disciplines = sorted(set(disciplines) - ALLOWED_DISCIPLINES)
        if unknown_disciplines:
            errors.append(f"relationship {key}: unsupported disciplines {unknown_disciplines}")
        lifecycle = _string_list(rel.get("lifecycle_phase"))
        unknown_lifecycle = sorted(set(lifecycle) - ALLOWED_LIFECYCLE)
        if unknown_lifecycle:
            errors.append(f"relationship {key}: unsupported lifecycle phases {unknown_lifecycle}")
        relation_category = str(rel.get("relation_category") or "")
        if relation_category and relation_category not in ALLOWED_RELATION_CATEGORIES:
            errors.append(f"relationship {key}: unsupported relation_category {relation_category!r}")
        if len(str(rel.get("rationale") or "").strip()) < 30:
            errors.append(f"relationship {key}: rationale is too short")
        if PLACEHOLDER_RE.search(str(rel.get("rationale") or "")):
            errors.append(f"relationship {key}: placeholder-like rationale")

    duplicate_triples = [
        key for key, count in Counter(_relationship_key(row) for row in relationships).items()
        if count > 1
    ]
    if duplicate_triples:
        errors.append(f"duplicate relationship triples detected: {duplicate_triples[:10]}")

    duplicate_labels = {label: count for label, count in label_counts.items() if count > 1}
    if duplicate_labels:
        warnings.append(f"duplicate normalized labels present: {len(duplicate_labels)}")
    same_parent_duplicate_labels = {
        f"{parent_path or '<root>'}:{label}": rows
        for (parent_path, label), rows in labels_by_parent.items()
        if len(rows) > 1
    }
    if same_parent_duplicate_labels:
        errors.append(
            "same-parent duplicate normalized labels detected: "
            f"{list(same_parent_duplicate_labels)[:10]}"
        )
    introduced_label_counts = Counter(
        _norm(row.get("label"))
        for row in nodes
        if introduced_generation_method is not None
        and str(row.get("id") or "") in introduced_node_ids
        and _norm(row.get("label"))
    )
    introduced_duplicate_labels = sorted(
        label for label, count in introduced_label_counts.items() if count > 1
    )
    if introduced_duplicate_labels:
        errors.append(f"introduced duplicate normalized labels detected: {introduced_duplicate_labels[:10]}")
    hierarchy_cycles = _cycle_count(relationships, "broader_than")
    part_of_cycles = _cycle_count(relationships, "part_of")
    if hierarchy_cycles:
        errors.append(f"broader_than hierarchy cycles detected: {hierarchy_cycles}")
    if part_of_cycles:
        errors.append(f"part_of cycles detected: {part_of_cycles}")

    non_hierarchy_endpoints = {
        str(row.get("from_id") or "") for row in relationships if row.get("predicate") != "broader_than"
    } | {
        str(row.get("to_id") or "") for row in relationships if row.get("predicate") != "broader_than"
    }
    orphan_nodes = sorted(node_id for node_id in node_ids if node_id not in relationship_endpoints)
    introduced_orphans = sorted(node_id for node_id in introduced_node_ids if node_id not in non_hierarchy_endpoints)
    if introduced_orphans:
        errors.append(f"introduced nodes without non-hierarchy relationships: {introduced_orphans[:10]}")

    relation_type_counts = Counter(str(row.get("relation_type") or "") for row in relationships if row.get("relation_type"))
    self_loop_relationships = [
        row
        for row in relationships
        if str(row.get("from_id") or "") and str(row.get("from_id") or "") == str(row.get("to_id") or "")
    ]
    source_coverage = sum(1 for row in relationships if _string_list(row.get("source_family_ids")))
    introduced_source_coverage = sum(1 for row in introduced_edges if _string_list(row.get("source_family_ids")))
    duplicate_label_context_summary = _duplicate_label_context_summary(nodes, duplicate_labels)
    discipline_counts = Counter(
        item
        for row in relationships
        for item in _string_list(row.get("discipline"))
    )
    lifecycle_counts = Counter(
        item
        for row in relationships
        for item in _string_list(row.get("lifecycle_phase"))
    )
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "ok": not errors,
        "generated_at_utc": _utc_now(),
        "metrics": {
            "node_count": len(nodes),
            "relationship_count": len(relationships),
            "orphan_node_count": len(orphan_nodes),
            "introduced_non_hierarchy_orphan_count": len(introduced_orphans),
            "generic_relationship_count": sum(
                1
                for row in relationships
                if str(row.get("predicate") or row.get("edge_type") or "") in GENERIC_RELATIONS
            ),
            "relationship_source_family_coverage": {
                "present": source_coverage,
                "total": len(relationships),
                "ratio": round(source_coverage / len(relationships), 4) if relationships else 1.0,
            },
            "introduced_relationship_source_family_coverage": {
                "present": introduced_source_coverage,
                "total": len(introduced_edges),
                "ratio": round(introduced_source_coverage / len(introduced_edges), 4) if introduced_edges else 1.0,
            },
            "introduced_node_count": len(introduced_node_ids),
            "introduced_relationship_count": len(introduced_edges),
            "duplicate_relationship_triple_count": len(duplicate_triples),
            "relation_type_count": len(relation_type_counts),
            "top_relation_types": dict(relation_type_counts.most_common(25)),
            "discipline_coverage": dict(sorted(discipline_counts.items())),
            "lifecycle_coverage": dict(sorted(lifecycle_counts.items())),
            "hierarchy_cycle_count": hierarchy_cycles,
            "part_of_cycle_count": part_of_cycles,
            "duplicate_normalized_label_group_count": len(duplicate_labels),
            "duplicate_normalized_label_count": len(duplicate_labels),
            "duplicate_normalized_label_node_count": sum(duplicate_labels.values()),
            "duplicate_normalized_label_excess_count": sum(count - 1 for count in duplicate_labels.values()),
            "same_parent_duplicate_normalized_label_count": len(same_parent_duplicate_labels),
            "duplicate_normalized_label_context_summary": duplicate_label_context_summary,
            "self_loop_count": len(self_loop_relationships),
            "self_loop_relationship_count": len(self_loop_relationships),
            "sample_duplicate_normalized_labels": _duplicate_label_samples(nodes, duplicate_labels),
            "sample_same_parent_duplicate_labels": _duplicate_same_parent_label_samples(same_parent_duplicate_labels),
            "sample_self_loop_relationships": _relationship_samples(self_loop_relationships, path_by_id),
            "sample_orphan_path_codes": [path_by_id[node_id] for node_id in orphan_nodes[:20]],
            "sample_introduced_non_hierarchy_orphan_path_codes": [
                path_by_id[node_id] for node_id in introduced_orphans[:20]
            ],
        },
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }


def run_graph_quality_report(
    fixture_path: str | Path = DEFAULT_FIXTURE_PATH,
    *,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_path: str | Path | None = None,
    introduced_generation_method: str | None = None,
    source_rights_registry_path: str | Path | None = None,
) -> dict[str, Any]:
    root = _repo_root(repo_root)
    fixture = _resolve_file(root, Path(fixture_path))
    resolved_run_id = _run_id(run_id)
    report_path = _resolve_report_path(root, resolved_run_id, Path(output_path) if output_path else None)
    payload = _load_json_object(fixture)
    source_payload = _load_json_object(_resolve_file(root, Path(source_rights_registry_path))) if source_rights_registry_path else None
    report = analyze_backbone_graph_quality(
        payload,
        introduced_generation_method=introduced_generation_method,
        source_rights_payload=source_payload,
    )
    report["run_id"] = resolved_run_id
    report["fixture_path"] = _relative_to_root(fixture, root)
    report["report_path"] = _relative_to_root(report_path, root)
    duplicate_index = _duplicate_label_context_index(payload)
    duplicate_index_path = report_path.with_name(DUPLICATE_LABEL_CONTEXT_FILENAME)
    _write_json(duplicate_index_path, duplicate_index)
    report["duplicate_label_context_index_path"] = _relative_to_root(duplicate_index_path, root)
    report["metrics"]["duplicate_normalized_label_context_index_group_count"] = duplicate_index["group_count"]
    report["metrics"]["duplicate_normalized_label_context_index_node_count"] = duplicate_index["node_count"]
    _write_json(report_path, report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run file-backed Backbone graph quality checks.")
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE_PATH))
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--introduced-generation-method", default=None)
    parser.add_argument("--source-rights-registry", default=None)
    args = parser.parse_args(argv)
    try:
        report = run_graph_quality_report(
            args.fixture,
            repo_root=args.repo_root,
            run_id=args.run_id,
            output_path=args.output,
            introduced_generation_method=args.introduced_generation_method,
            source_rights_registry_path=args.source_rights_registry,
        )
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def _cycle_count(rows: list[dict[str, Any]], predicate: str) -> int:
    outgoing: dict[str, list[str]] = defaultdict(list)
    incoming_count: Counter[str] = Counter()
    nodes: set[str] = set()
    for row in rows:
        if row.get("predicate") != predicate:
            continue
        start = str(row.get("from_id") or "")
        end = str(row.get("to_id") or "")
        if not start or not end:
            continue
        outgoing[start].append(end)
        incoming_count[end] += 1
        nodes.update({start, end})
    queue = deque(node for node in nodes if incoming_count[node] == 0)
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for child in outgoing.get(node, []):
            incoming_count[child] -= 1
            if incoming_count[child] == 0:
                queue.append(child)
    return max(0, len(nodes) - visited)


def _relationship_key(row: dict[str, Any]) -> str:
    return f"{row.get('from_id')}--{row.get('predicate') or row.get('edge_type')}--{row.get('to_id')}"


def _duplicate_label_samples(
    nodes: list[dict[str, Any]],
    duplicate_labels: dict[str, int],
    *,
    limit: int = 20,
    nodes_per_label: int = 6,
) -> list[dict[str, Any]]:
    if not duplicate_labels:
        return []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in nodes:
        label = _norm(row.get("label"))
        if label in duplicate_labels:
            grouped[label].append(row)
    samples: list[dict[str, Any]] = []
    for label, rows in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0]))[:limit]:
        samples.append(
            {
                "normalized_label": label,
                "count": len(rows),
                "sample_nodes": [
                    {
                        "id": str(row.get("id") or ""),
                        "path_code": str(row.get("path_code") or ""),
                        "label": str(row.get("label") or ""),
                        "parent_path_code": str(row.get("parent_path_code") or ""),
                    }
                    for row in rows[:nodes_per_label]
                ],
            }
        )
    return samples


def _duplicate_same_parent_label_samples(
    duplicate_groups: dict[str, list[dict[str, Any]]],
    *,
    limit: int = 20,
    nodes_per_label: int = 6,
) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    for key, rows in sorted(duplicate_groups.items(), key=lambda item: item[0])[:limit]:
        parent_path, _, normalized_label = key.partition(":")
        samples.append(
            {
                "parent_path_code": "" if parent_path == "<root>" else parent_path,
                "normalized_label": normalized_label,
                "count": len(rows),
                "sample_nodes": [
                    {
                        "id": str(row.get("id") or ""),
                        "path_code": str(row.get("path_code") or ""),
                        "label": str(row.get("label") or ""),
                    }
                    for row in rows[:nodes_per_label]
                ],
            }
        )
    return samples


def _duplicate_label_context_summary(
    nodes: list[dict[str, Any]],
    duplicate_labels: dict[str, int],
) -> dict[str, Any]:
    groups = _duplicate_label_context_groups(nodes, duplicate_labels)
    review_counts = Counter(str(group.get("review_class") or "") for group in groups)
    scope_counts = Counter(str(group.get("duplicate_scope") or "") for group in groups)
    return {
        "group_count": len(groups),
        "node_count": sum(len(group["nodes"]) for group in groups),
        "review_class_counts": dict(sorted(review_counts.items())),
        "duplicate_scope_counts": dict(sorted(scope_counts.items())),
    }


def _duplicate_label_context_index(payload: dict[str, Any]) -> dict[str, Any]:
    records = _dict_list(payload.get("records"))
    nodes = [row for row in records if row.get("record_type") == "BackboneNode"]
    label_counts = Counter(_norm(row.get("label")) for row in nodes if _norm(row.get("label")))
    duplicate_labels = {label: count for label, count in label_counts.items() if count > 1}
    groups = _duplicate_label_context_groups(nodes, duplicate_labels)
    return {
        "schema_version": "aec-mepfs-backbone-duplicate-label-context-index/v1",
        "generated_at_utc": _utc_now(),
        "description": (
            "Non-destructive duplicate normalized-label context index. "
            "Canonical labels and prefLabels are not renamed here; same-parent "
            "duplicates remain blocking errors in graph-quality validation."
        ),
        "group_count": len(groups),
        "node_count": sum(len(group["nodes"]) for group in groups),
        "groups": groups,
    }


def _duplicate_label_context_groups(
    nodes: list[dict[str, Any]],
    duplicate_labels: dict[str, int],
) -> list[dict[str, Any]]:
    if not duplicate_labels:
        return []
    by_path = {str(row.get("path_code") or ""): row for row in nodes}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in nodes:
        label = _norm(row.get("label"))
        if label in duplicate_labels:
            grouped[label].append(row)

    groups: list[dict[str, Any]] = []
    for normalized_label, rows in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        roots = {str(row.get("path_code") or "").split(".", 1)[0] for row in rows if row.get("path_code")}
        same_parent = any(len(parent_rows) > 1 for parent_rows in _group_rows_by_parent(rows).values())
        if same_parent:
            review_class = "same_parent_blocker"
            duplicate_scope = "same_parent"
        elif len(roots) > 1:
            review_class = "contextual_duplicate"
            duplicate_scope = "cross_root"
        else:
            review_class = "contextual_duplicate"
            duplicate_scope = "cross_parent"
        parent_group_count = len({(str(row.get("parent_path_code") or ""), normalized_label) for row in rows})
        groups.append(
            {
                "normalized_label": normalized_label,
                "label": str(rows[0].get("label") or ""),
                "count": len(rows),
                "excess_count": len(rows) - 1,
                "duplicate_scope": duplicate_scope,
                "review_class": review_class,
                "root_scopes": sorted(roots),
                "parent_group_count": parent_group_count,
                "nodes": [
                    _duplicate_context_node(row, by_path)
                    for row in sorted(rows, key=lambda item: str(item.get("path_code") or ""))
                ],
            }
        )
    return groups


def _group_rows_by_parent(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("parent_path_code") or "")].append(row)
    return grouped


def _duplicate_context_node(row: dict[str, Any], by_path: dict[str, dict[str, Any]]) -> dict[str, str]:
    path_code = str(row.get("path_code") or "")
    parent_path_code = str(row.get("parent_path_code") or "")
    parent_label = str(by_path.get(parent_path_code, {}).get("label") or "")
    label = str(row.get("label") or "")
    display_context = parent_label or parent_path_code or path_code
    return {
        "id": str(row.get("id") or ""),
        "path_code": path_code,
        "root_path_code": path_code.split(".", 1)[0] if path_code else "",
        "label": label,
        "parent_path_code": parent_path_code,
        "parent_label": parent_label,
        "display_hint": f"{label} - {display_context}" if display_context else label,
        "review_note": (
            "Contextual duplicate; use path_code/canonical id for disambiguation "
            "before any steward-approved rename or alias merge."
        ),
    }


def _relationship_samples(
    rows: list[dict[str, Any]],
    path_by_id: dict[str, str],
    *,
    limit: int = 20,
) -> list[dict[str, Any]]:
    return [
        {
            "key": _relationship_key(row),
            "from_id": str(row.get("from_id") or ""),
            "to_id": str(row.get("to_id") or ""),
            "from_path_code": path_by_id.get(str(row.get("from_id") or ""), ""),
            "to_path_code": path_by_id.get(str(row.get("to_id") or ""), ""),
            "predicate": str(row.get("predicate") or row.get("edge_type") or ""),
            "relation_type": str(row.get("relation_type") or ""),
            "generation_method": str(row.get("generation_method") or ""),
        }
        for row in rows[:limit]
    ]


def _norm(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().casefold())


def _has_value(value: Any) -> bool:
    if isinstance(value, list):
        return bool(value)
    return value is not None and str(value).strip() != ""


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value is None:
        return []
    text = str(value).strip()
    return [text] if text else []


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _dict_list(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _source_ids(payload: dict[str, Any] | None) -> set[str] | None:
    if payload is None:
        return None
    rows = _dict_list(payload.get("source_rights_registry"))
    return {str(row.get("source_id") or "") for row in rows if row.get("source_id")}


def _load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _resolve_file(root: Path, path: Path) -> Path:
    resolved = path if path.is_absolute() else root / path
    resolved = resolved.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{path}: path must stay inside repository root") from exc
    if not resolved.is_file():
        raise FileNotFoundError(f"{path}: file does not exist")
    return resolved


def _resolve_report_path(root: Path, run_id: str, output_path: Path | None) -> Path:
    target = output_path if output_path is not None else REPORT_ROOT / run_id / REPORT_FILENAME
    resolved = target if target.is_absolute() else root / target
    resolved = resolved.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{target}: output path must stay inside repository root") from exc
    _reject_raw_source_output(root, resolved, target)
    expected_root = (root / REPORT_ROOT).resolve()
    try:
        resolved.relative_to(expected_root)
    except ValueError as exc:
        raise ValueError(f"{target}: output path must stay inside {REPORT_ROOT.as_posix()}") from exc
    if resolved.name != REPORT_FILENAME:
        raise ValueError(f"{target}: output filename must be {REPORT_FILENAME}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def _reject_raw_source_output(root: Path, resolved: Path, target: Path) -> None:
    raw_root = (root / RAW_SOURCE_ROOT).resolve()
    try:
        resolved.relative_to(raw_root)
    except ValueError:
        return
    raise ValueError(f"{target}: output path must not be inside immutable raw source custody layer {RAW_SOURCE_ROOT.as_posix()}")


def _repo_root(repo_root: str | Path | None) -> Path:
    return Path(repo_root).resolve() if repo_root is not None else Path.cwd().resolve()


def _run_id(run_id: str | None) -> str:
    value = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not RUN_ID_RE.match(value):
        raise ValueError("run_id contains unsupported characters")
    return value


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
