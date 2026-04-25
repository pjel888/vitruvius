"""Quality report helpers for KG v2 snapshots."""

from __future__ import annotations

from collections import Counter
from typing import Any

from .json_evidence_store import KgV2Snapshot


STRUCTURAL_RELATIONSHIP_TYPES = {
    "BELONGS_TO",
    "HAS_CHILD",
    "DEFINED_BY",
    "SUPPORTED_BY",
}

GENERIC_RULE_DISPLAY_LABELS = {
    "general rule",
    "occupancy rule",
    "building rule",
}


def _all_endpoint_ids(snapshot: KgV2Snapshot) -> set[str]:
    endpoint_ids = {node.id for node in snapshot.canonical_nodes}
    endpoint_ids.update(span.id for span in snapshot.evidence_spans)
    for doc_version in snapshot.document_versions:
        endpoint_ids.add(doc_version.id)
        endpoint_ids.add(doc_version.document_id)
    return endpoint_ids


def _contains_truncation_marker(value: str | None) -> bool:
    return bool(value and ("..." in value or "…" in value))


def build_kg_quality_report(snapshot: KgV2Snapshot) -> dict[str, Any]:
    """Return deterministic quality signals for a KG v2 snapshot."""
    endpoint_ids = _all_endpoint_ids(snapshot)
    missing_assertion_targets: list[dict[str, str]] = []
    supported_by_to_evidence = 0
    supported_by_total = 0

    assertion_edge_types: Counter[str] = Counter()
    semantic_edge_types: Counter[str] = Counter()
    validation_states: Counter[str] = Counter()
    review_states: Counter[str] = Counter()

    for assertion in snapshot.relationship_assertions:
        edge_type = assertion.edge_type.value
        assertion_edge_types[edge_type] += 1
        if edge_type not in STRUCTURAL_RELATIONSHIP_TYPES:
            semantic_edge_types[edge_type] += 1
        validation_states[assertion.validation_status.value] += 1
        review_states[assertion.review_state] += 1
        if assertion.edge_type.value == "SUPPORTED_BY":
            supported_by_total += 1
            if assertion.to_node_id.startswith(("span-", "docv-", "doc-")):
                supported_by_to_evidence += 1
        if assertion.from_node_id not in endpoint_ids:
            missing_assertion_targets.append(
                {"assertion_id": assertion.id, "field": "from_node_id", "node_id": assertion.from_node_id}
            )
        if assertion.to_node_id not in endpoint_ids:
            missing_assertion_targets.append(
                {"assertion_id": assertion.id, "field": "to_node_id", "node_id": assertion.to_node_id}
            )

    fast_edge_types = Counter(str(edge.get("edge_type", "")) for edge in snapshot.fast_edges)
    node_type_counts = Counter(node.type.value for node in snapshot.canonical_nodes)

    rules = [node for node in snapshot.canonical_nodes if node.type.value == "rule"]
    rule_display_counts = Counter((node.display_label or "").strip() for node in rules)
    duplicate_rule_display_labels = sorted(
        label for label, count in rule_display_counts.items() if label and count > 1
    )
    generic_rule_display_labels = sorted(
        label for label in rule_display_counts if label.strip().lower() in GENERIC_RULE_DISPLAY_LABELS
    )
    truncated_rule_labels = [
        node.id
        for node in rules
        if _contains_truncation_marker(node.display_label)
    ]

    taxonomy_nodes = [node for node in snapshot.canonical_nodes if node.type.value == "taxonomy"]
    taxonomy_path_nodes = [
        node for node in snapshot.canonical_nodes
        if node.type.value != "taxonomy" and node.taxonomy_path
    ]
    placed_node_ids = {placement.node_id for placement in snapshot.placement_assertions}
    placement_missing_nodes = sorted(
        node.id for node in taxonomy_path_nodes if node.id not in placed_node_ids
    )

    warnings: list[str] = []
    if missing_assertion_targets:
        warnings.append("relationship_assertions_have_missing_endpoints")
    if supported_by_total and supported_by_to_evidence != supported_by_total:
        warnings.append("supported_by_assertions_do_not_all_target_evidence")
    if taxonomy_nodes and taxonomy_path_nodes and not snapshot.placement_assertions:
        warnings.append("taxonomy_paths_exist_without_placement_assertions")
    if duplicate_rule_display_labels:
        warnings.append("duplicate_rule_display_labels")
    if generic_rule_display_labels:
        warnings.append("generic_rule_display_labels")
    if truncated_rule_labels:
        warnings.append("truncated_rule_labels")

    return {
        "entity_counts": snapshot.entity_counts(),
        "node_type_counts": dict(sorted(node_type_counts.items())),
        "assertion_edge_type_counts": dict(sorted(assertion_edge_types.items())),
        "semantic_relationship_quality": {
            "semantic_assertion_count": sum(semantic_edge_types.values()),
            "semantic_edge_type_counts": dict(sorted(semantic_edge_types.items())),
            "semantic_edge_type_diversity": len(semantic_edge_types),
        },
        "fast_edge_type_counts": dict(sorted(fast_edge_types.items())),
        "validation_state_counts": dict(sorted(validation_states.items())),
        "review_state_counts": dict(sorted(review_states.items())),
        "relationship_endpoint_quality": {
            "missing_endpoint_count": len(missing_assertion_targets),
            "missing_endpoints": missing_assertion_targets[:50],
            "supported_by_total": supported_by_total,
            "supported_by_to_evidence": supported_by_to_evidence,
        },
        "rule_title_quality": {
            "rule_count": len(rules),
            "duplicate_display_labels": duplicate_rule_display_labels,
            "generic_display_labels": generic_rule_display_labels,
            "truncated_rule_label_ids": truncated_rule_labels[:50],
        },
        "taxonomy_quality": {
            "taxonomy_node_count": len(taxonomy_nodes),
            "nodes_with_taxonomy_path": len(taxonomy_path_nodes),
            "placement_assertion_count": len(snapshot.placement_assertions),
            "missing_placement_count": len(placement_missing_nodes),
            "missing_placement_node_ids": placement_missing_nodes[:50],
        },
        "warnings": warnings,
    }
