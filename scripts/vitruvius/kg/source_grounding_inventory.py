"""No-write source-grounding inventory for the AEC-MEPFS backbone.

This module reads the governed AEC backbone, resource-layer registries, and
optional pending relationship-improvement overlays. It writes only inventory
reports under the requested output directory; it never mutates active graph
files or review/admission artifacts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable


SCHEMA_VERSION = "aec-source-grounding-inventory/v1"
DEFAULT_INPUT_PATH = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
DEFAULT_OUTPUT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/source-grounding-inventory")
DEFAULT_RESOURCE_LAYER_ROOT = Path("006_System-Manifests/resource-layer")
DEFAULT_SEMANTIC_OVERLAY_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/semantic-overlays")

ACCEPTED_RESOURCE_LINK_STATUSES = {"accepted", "human_reviewed"}
DOMAIN_SYNTHESIS_STATUSES = {"steward_admitted", "admitted", "accepted", "human_reviewed"}
REJECTED_STATUSES = {"rejected", "blocked", "deprecated"}
HIGH_IMPACT_PREDICATES = {
    "applicable_in_jurisdiction",
    "conflicts_with",
    "constrains",
    "evidenced_by",
    "governs",
    "maps_to_external_standard",
    "requires",
    "supersedes",
}
STOPWORDS = {
    "a",
    "an",
    "and",
    "architecture",
    "architectural",
    "are",
    "as",
    "at",
    "building",
    "buildings",
    "built",
    "by",
    "code",
    "codes",
    "compliance",
    "covering",
    "design",
    "engineering",
    "environment",
    "for",
    "from",
    "guidance",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "professional",
    "national",
    "requirement",
    "requirements",
    "response",
    "safety",
    "standard",
    "standards",
    "system",
    "systems",
    "the",
    "to",
    "transportation",
    "with",
}


@dataclass(frozen=True)
class SourceGroundingInventoryConfig:
    input_path: Path = DEFAULT_INPUT_PATH
    output_root: Path = DEFAULT_OUTPUT_ROOT
    run_id: str | None = None
    resource_layer_root: Path = DEFAULT_RESOURCE_LAYER_ROOT
    semantic_overlay_root: Path = DEFAULT_SEMANTIC_OVERLAY_ROOT
    relationship_run_id: str | None = "latest"
    max_gap_examples: int = 50
    write_gap_workqueue: bool = True
    max_workqueue_items: int = 500
    max_resource_proposals_per_item: int = 5
    min_resource_proposal_score: float = 0.08
    print_summary: bool = True


@dataclass(frozen=True)
class SourceGroundingInventorySummary:
    run_id: str
    output_dir: str
    report_path: str
    summary_path: str
    node_count: int
    relationship_count: int
    node_source_backed_count: int
    relationship_source_backed_count: int
    pending_relationship_overlay_count: int
    pending_node_consolidation_overlay_count: int
    workqueue_path: str | None = None
    source_link_proposals_path: str | None = None
    workqueue_item_count: int = 0
    source_link_proposal_count: int = 0

    def to_record(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "output_dir": self.output_dir,
            "report_path": self.report_path,
            "summary_path": self.summary_path,
            "node_count": self.node_count,
            "relationship_count": self.relationship_count,
            "node_source_backed_count": self.node_source_backed_count,
            "relationship_source_backed_count": self.relationship_source_backed_count,
            "pending_relationship_overlay_count": self.pending_relationship_overlay_count,
            "pending_node_consolidation_overlay_count": self.pending_node_consolidation_overlay_count,
            "workqueue_path": self.workqueue_path,
            "source_link_proposals_path": self.source_link_proposals_path,
            "workqueue_item_count": self.workqueue_item_count,
            "source_link_proposal_count": self.source_link_proposal_count,
            "pending_only": True,
            "active_graph_mutation": False,
        }


def utc_now_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_run_id(prefix: str = "source_grounding_inventory") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def read_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def read_json_array_file(path: Path, key: str) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = read_json_object(path)
    value = payload.get(key, [])
    if not isinstance(value, list):
        raise ValueError(f"{path}.{key} must be an array")
    return [item for item in value if isinstance(item, dict)]


def read_jsonl_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists():
        return records
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                records.append(value)
    return records


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def edge_key(edge: dict[str, Any]) -> str:
    return f"{edge.get('from_id', '')}--{edge.get('predicate', '')}--{edge.get('to_id', '')}"


def edge_key_from_overlay(record: dict[str, Any]) -> str | None:
    value = record.get("final_edge_key") or record.get("edge_key")
    if isinstance(value, str) and value:
        return value
    from_id = record.get("from_id")
    predicate = record.get("predicate")
    to_id = record.get("to_id")
    if all(isinstance(part, str) and part for part in (from_id, predicate, to_id)):
        return f"{from_id}--{predicate}--{to_id}"
    return None


def source_family_ids(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return []


def count_by(items: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def bounded_append(items: list[dict[str, Any]], item: dict[str, Any], limit: int) -> None:
    if len(items) < limit:
        items.append(item)


def is_accepted_link(link: dict[str, Any]) -> bool:
    return str(link.get("reviewStatus") or link.get("review_status") or "") in ACCEPTED_RESOURCE_LINK_STATUSES


def sanitize_excerpt(value: Any, limit: int = 240) -> str:
    text = str(value or "")
    for marker in ("reasoning_content", "Authorization", "Bearer ", "DEEPSEEK_API_KEY", "KIMI_API_KEY", "MOONSHOT_API_KEY"):
        text = text.replace(marker, "[REDACTED]")
    text = re.sub(r"\bsk-[A-Za-z0-9_-]+", "[REDACTED]", text)
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


def stable_id(prefix: str, *parts: Any) -> str:
    digest = hashlib.sha256("||".join(str(part or "") for part in parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def scalar_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(scalar_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(scalar_text(item) for item in value)
    return str(value or "")


def tokenize(value: Any) -> set[str]:
    text = scalar_text(value).lower().replace("_", " ").replace("-", " ")
    tokens = {token for token in re.findall(r"[a-z0-9]+", text) if len(token) > 1 and token not in STOPWORDS}
    return tokens


def node_text(record: dict[str, Any]) -> str:
    return scalar_text(
        [
            record.get("id"),
            record.get("label"),
            record.get("pref_label"),
            record.get("aliases"),
            record.get("definition"),
            record.get("description"),
            record.get("path_code"),
            record.get("domain"),
            record.get("discipline"),
        ]
    )


def resource_text(resource: dict[str, Any]) -> str:
    return scalar_text(
        [
            resource.get("id"),
            resource.get("title"),
            resource.get("subtitle"),
            resource.get("organization"),
            resource.get("publisher"),
            resource.get("resourceType"),
            resource.get("sourceAuthority"),
            resource.get("disciplineTags"),
            resource.get("taxonomyTags"),
            resource.get("keywords"),
            resource.get("abstractOrSummary"),
            resource.get("sourceFamilyIds"),
        ]
    )


def resource_is_proposable(resource: dict[str, Any]) -> bool:
    status_values = [
        resource.get("reviewStatus"),
        resource.get("review_status"),
        resource.get("admissionStatus"),
        resource.get("admission_status"),
        resource.get("verificationStatus"),
    ]
    return not any(str(value or "").lower() in REJECTED_STATUSES for value in status_values)


def resource_authority_bonus(resource: dict[str, Any]) -> float:
    bonus = 0.0
    try:
        tier = int(resource.get("authorityTier") or 0)
    except (TypeError, ValueError):
        tier = 0
    if tier == 1:
        bonus += 0.12
    elif tier == 2:
        bonus += 0.08
    elif tier == 3:
        bonus += 0.04
    authority = str(resource.get("sourceAuthority") or "").lower()
    if authority in {"official", "government", "standards_body", "professional_body"}:
        bonus += 0.08
    verification = str(resource.get("verificationStatus") or "").lower()
    if verification in {"content_verified", "link_verified", "metadata_checked"}:
        bonus += 0.08
    access = str(resource.get("accessType") or "").lower()
    if access in {"public_web", "open_access", "public", "official_public"}:
        bonus += 0.04
    return bonus


def suggest_resource_relationship(resource: dict[str, Any]) -> str:
    resource_type = str(resource.get("resourceType") or "").lower()
    if resource_type in {"code", "standard", "regulation", "law"}:
        return "governs"
    if resource_type in {"government_guidance", "professional_guidance", "guidance"}:
        return "provides_design_guidance"
    if resource_type in {"book", "textbook", "handbook", "manual"}:
        return "explains"
    return "supports"


def build_resource_candidates(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for resource in resources:
        resource_id = str(resource.get("id") or "")
        if not resource_id or not resource_is_proposable(resource):
            continue
        candidates.append(
            {
                "resource": resource,
                "resource_id": resource_id,
                "tokens": tokenize(resource_text(resource)),
                "authority_bonus": resource_authority_bonus(resource),
            }
        )
    return candidates


def score_resource_candidates(
    query_tokens: set[str],
    resource_candidates: list[dict[str, Any]],
    min_score: float,
    limit: int,
) -> list[dict[str, Any]]:
    if not query_tokens or limit <= 0:
        return []
    scored: list[dict[str, Any]] = []
    for candidate in resource_candidates:
        resource_tokens = candidate["tokens"]
        overlap_tokens = sorted(query_tokens & resource_tokens)
        if len(overlap_tokens) < 2:
            continue
        overlap_score = len(overlap_tokens) / max(len(query_tokens), 8)
        score = round(min(1.0, overlap_score + float(candidate["authority_bonus"])), 6)
        if score < min_score:
            continue
        resource = candidate["resource"]
        scored.append(
            {
                "resource_id": candidate["resource_id"],
                "title": sanitize_excerpt(resource.get("title"), 160),
                "score": score,
                "matched_terms": overlap_tokens[:12],
                "suggested_relationship": suggest_resource_relationship(resource),
                "resource_type": resource.get("resourceType"),
                "source_authority": resource.get("sourceAuthority"),
                "authority_tier": resource.get("authorityTier"),
                "verification_status": resource.get("verificationStatus"),
                "access_type": resource.get("accessType"),
            }
        )
    scored.sort(key=lambda item: (-float(item["score"]), str(item["resource_id"])))
    return scored[:limit]


def build_node_degree(relationships: list[dict[str, Any]]) -> dict[str, int]:
    degree: dict[str, int] = {}
    for edge in relationships:
        for key in ("from_id", "to_id"):
            node_id = str(edge.get(key) or "")
            if node_id:
                degree[node_id] = degree.get(node_id, 0) + 1
    return degree


def workqueue_priority_score(
    item_type: str,
    classification: str,
    resource_matches: list[dict[str, Any]],
    degree: int,
    predicate: str | None = None,
) -> float:
    top_match = float(resource_matches[0]["score"]) if resource_matches else 0.0
    score = top_match * 70.0
    score += min(max(degree, 0), 30) * 0.25
    if classification == "unsupported":
        score += 8.0
    elif classification == "domain_synthesis":
        score += 4.0
    if item_type == "relationship_source_gap":
        score += 3.0
    if predicate in HIGH_IMPACT_PREDICATES:
        score += 24.0
    elif predicate in {"broader_than", "narrower_than"}:
        score -= 10.0
    return round(score, 6)


def build_source_gap_workqueue(
    *,
    run_id: str,
    records: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
    node_classifications: dict[str, str],
    relationship_classifications: dict[str, str],
    resource_candidates: list[dict[str, Any]],
    max_items: int,
    max_resource_proposals_per_item: int,
    min_resource_proposal_score: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    created_at = utc_now_z()
    nodes_by_id = {str(record.get("id") or ""): record for record in records if record.get("id")}
    degree = build_node_degree(relationships)
    raw_items: list[dict[str, Any]] = []

    for record in records:
        node_id = str(record.get("id") or "")
        classification = node_classifications.get(node_id, "unsupported")
        if not node_id or classification == "source_backed":
            continue
        matches = score_resource_candidates(
            tokenize(node_text(record)),
            resource_candidates,
            min_resource_proposal_score,
            max_resource_proposals_per_item,
        )
        priority_score = workqueue_priority_score("node_resource_gap", classification, matches, degree.get(node_id, 0))
        raw_items.append(
            {
                "schema_version": "aec-source-grounding-gap-workqueue/v1",
                "workqueue_id": stable_id("sgwq", run_id, "node", node_id),
                "created_at_utc": created_at,
                "item_type": "node_resource_gap",
                "source_backing_status": classification,
                "node_id": node_id,
                "node_label": sanitize_excerpt(record.get("pref_label") or record.get("label"), 160),
                "path_code": record.get("path_code"),
                "degree": degree.get(node_id, 0),
                "classification": classification,
                "suggested_resources": matches,
                "priority_score": priority_score,
                "proposal_ids": [],
                "final_action": "review_source_link_proposals",
                "pending_only": True,
                "auto_admit": False,
                "active_graph_mutation": False,
                "resource_layer_mutation": False,
            }
        )

    for edge in relationships:
        key = edge_key(edge)
        classification = relationship_classifications.get(key, "unsupported")
        if classification == "source_backed":
            continue
        from_id = str(edge.get("from_id") or "")
        to_id = str(edge.get("to_id") or "")
        from_node = nodes_by_id.get(from_id, {})
        to_node = nodes_by_id.get(to_id, {})
        predicate = str(edge.get("predicate") or "")
        query_tokens = tokenize([node_text(from_node), predicate, node_text(to_node)])
        matches = score_resource_candidates(
            query_tokens,
            resource_candidates,
            min_resource_proposal_score,
            max_resource_proposals_per_item,
        )
        edge_degree = degree.get(from_id, 0) + degree.get(to_id, 0)
        priority_score = workqueue_priority_score(
            "relationship_source_gap",
            classification,
            matches,
            edge_degree,
            predicate,
        )
        raw_items.append(
            {
                "schema_version": "aec-source-grounding-gap-workqueue/v1",
                "workqueue_id": stable_id("sgwq", run_id, "relationship", key),
                "created_at_utc": created_at,
                "item_type": "relationship_source_gap",
                "source_backing_status": classification,
                "edge_key": key,
                "from_id": from_id,
                "from_label": sanitize_excerpt(from_node.get("pref_label") or from_node.get("label"), 120),
                "predicate": predicate,
                "to_id": to_id,
                "to_label": sanitize_excerpt(to_node.get("pref_label") or to_node.get("label"), 120),
                "degree": edge_degree,
                "classification": classification,
                "suggested_resources": matches,
                "priority_score": priority_score,
                "proposal_ids": [],
                "final_action": "review_source_link_proposals",
                "pending_only": True,
                "auto_admit": False,
                "active_graph_mutation": False,
                "resource_layer_mutation": False,
            }
        )

    raw_items.sort(
        key=lambda item: (
            -float(item["priority_score"]),
            str(item["item_type"]),
            str(item.get("node_id") or item.get("edge_key") or ""),
        )
    )
    items = raw_items[: max(0, max_items)]
    proposals: list[dict[str, Any]] = []
    for rank, item in enumerate(items, start=1):
        item["priority_rank"] = rank
        proposal_ids: list[str] = []
        for resource_match in item.get("suggested_resources", []):
            target_key = item.get("node_id") or item.get("edge_key")
            proposal_id = stable_id("sgprop", run_id, item["item_type"], target_key, resource_match["resource_id"])
            proposal_ids.append(proposal_id)
            proposal = {
                "schema_version": "aec-source-link-proposal/v1",
                "proposal_id": proposal_id,
                "created_at_utc": created_at,
                "target_type": "node" if item["item_type"] == "node_resource_gap" else "relationship",
                "node_id": item.get("node_id"),
                "edge_key": item.get("edge_key"),
                "from_id": item.get("from_id"),
                "predicate": item.get("predicate"),
                "to_id": item.get("to_id"),
                "resource_id": resource_match["resource_id"],
                "title": resource_match["title"],
                "score": resource_match["score"],
                "matched_terms": resource_match["matched_terms"],
                "suggested_relationship": resource_match["suggested_relationship"],
                "rationale": (
                    "Deterministic metadata overlap between the graph target and an existing Resource Layer record. "
                    "Review before creating any source link."
                ),
                "review_status": "candidate",
                "pending_only": True,
                "auto_admit": False,
                "active_graph_mutation": False,
                "resource_layer_mutation": False,
            }
            proposals.append(proposal)
        item["proposal_ids"] = proposal_ids
    return items, proposals


def resolve_latest_overlay_run(root: Path) -> Path | None:
    if not root.exists():
        return None
    candidates = [
        path for path in root.iterdir()
        if path.is_dir() and (path / "relationship-improvement-report.json").exists()
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def resolve_overlay_run(root: Path, relationship_run_id: str | None) -> Path | None:
    if relationship_run_id in (None, "", "none", "off"):
        return None
    if relationship_run_id == "latest":
        return resolve_latest_overlay_run(root)
    explicit = Path(relationship_run_id)
    if explicit.exists():
        return explicit
    candidate = root / relationship_run_id
    return candidate if candidate.exists() else None


def build_resource_indexes(resource_layer_root: Path) -> dict[str, Any]:
    resources = read_json_array_file(resource_layer_root / "resources.json", "resources")
    links = read_json_array_file(resource_layer_root / "node-resource-links.json", "nodeResourceLinks")
    source_families = read_json_array_file(resource_layer_root / "source-families.json", "sourceFamilies")
    resources_by_id = {str(resource.get("id")): resource for resource in resources if resource.get("id")}
    accepted_links = [link for link in links if is_accepted_link(link)]
    accepted_links_by_node: dict[str, list[dict[str, Any]]] = {}
    accepted_links_by_edge: dict[str, list[dict[str, Any]]] = {}
    for link in accepted_links:
        node_id = str(link.get("nodeId") or link.get("node_id") or "")
        if node_id:
            accepted_links_by_node.setdefault(node_id, []).append(link)
        for supported_edge in link.get("supportsEdgeIds") or link.get("supports_edge_ids") or []:
            if supported_edge:
                accepted_links_by_edge.setdefault(str(supported_edge), []).append(link)
    return {
        "resources": resources,
        "links": links,
        "source_families": source_families,
        "resources_by_id": resources_by_id,
        "accepted_links": accepted_links,
        "accepted_links_by_node": accepted_links_by_node,
        "accepted_links_by_edge": accepted_links_by_edge,
    }


def classify_node(record: dict[str, Any], accepted_links_by_node: dict[str, list[dict[str, Any]]]) -> str:
    node_id = str(record.get("id") or "")
    if accepted_links_by_node.get(node_id):
        return "source_backed"
    if str(record.get("review_status") or record.get("reviewStatus") or "") in DOMAIN_SYNTHESIS_STATUSES:
        return "domain_synthesis"
    return "unsupported"


def classify_relationship(edge: dict[str, Any], accepted_links_by_edge: dict[str, list[dict[str, Any]]]) -> str:
    key = edge_key(edge)
    if accepted_links_by_edge.get(key):
        return "source_backed"
    if source_family_ids(edge.get("source_family_ids") or edge.get("sourceFamilyIds")):
        return "source_backed"
    if edge.get("governed") is True or str(edge.get("review_status") or "") in DOMAIN_SYNTHESIS_STATUSES:
        return "domain_synthesis"
    return "unsupported"


def overlay_counts(overlay_dir: Path | None) -> dict[str, Any]:
    if overlay_dir is None:
        return {
            "available": False,
            "run_id": None,
            "output_dir": None,
            "accepted_relationship_count": 0,
            "candidate_relationship_count": 0,
            "pending_relationship_overlay_count": 0,
            "accepted_node_consolidation_count": 0,
            "candidate_node_consolidation_count": 0,
            "pending_node_consolidation_overlay_count": 0,
            "proposal_only_count": 0,
            "source_backed_count": 0,
        }
    accepted_relationships = read_jsonl_records(overlay_dir / "accepted-relationships.jsonl")
    candidate_relationships = read_jsonl_records(overlay_dir / "candidate-relationships.jsonl")
    accepted_nodes = read_jsonl_records(overlay_dir / "accepted-node-consolidations.jsonl")
    candidate_nodes = read_jsonl_records(overlay_dir / "node-consolidation-candidates.jsonl")
    relationship_records = accepted_relationships + candidate_relationships
    node_records = accepted_nodes + candidate_nodes
    source_backed = sum(
        1 for record in relationship_records
        if source_family_ids(record.get("source_family_ids") or record.get("sourceFamilyIds"))
    )
    return {
        "available": True,
        "run_id": overlay_dir.name,
        "output_dir": str(overlay_dir.resolve()),
        "accepted_relationship_count": len(accepted_relationships),
        "candidate_relationship_count": len(candidate_relationships),
        "pending_relationship_overlay_count": len(relationship_records),
        "accepted_node_consolidation_count": len(accepted_nodes),
        "candidate_node_consolidation_count": len(candidate_nodes),
        "pending_node_consolidation_overlay_count": len(node_records),
        "proposal_only_count": len(relationship_records) + len(node_records),
        "source_backed_count": source_backed,
        "latest_accepted_edge_keys": [key for key in (edge_key_from_overlay(record) for record in accepted_relationships[:10]) if key],
    }


def build_summary_text(report: dict[str, Any]) -> str:
    coverage = report["coverage"]
    overlay = report["pending_overlay_summary"]
    workqueue = report.get("source_gap_workqueue", {})
    lines = [
        "AEC Source-Grounding Inventory",
        f"Run ID: {report['run_id']}",
        f"Generated: {report['generated_at_utc']}",
        f"Input: {report['input_path']}",
        "",
        "Safety:",
        "- No active graph mutation was performed.",
        "- No Neo4j or Postgres writes were performed.",
        "- Pending relationship and node-consolidation overlays remain proposals only.",
        "",
        "Coverage:",
        f"- Nodes: {coverage['nodes']['source_backed']} source-backed / {coverage['nodes']['total']} total",
        f"- Relationships: {coverage['relationships']['source_backed']} source-backed / {coverage['relationships']['total']} total",
        f"- Pending relationship overlays: {overlay['pending_relationship_overlay_count']}",
        f"- Pending node-consolidation overlays: {overlay['pending_node_consolidation_overlay_count']}",
        "",
        "Source Gap Workqueue:",
        f"- Enabled: {workqueue.get('enabled', False)}",
        f"- Workqueue items: {workqueue.get('workqueue_item_count', 0)}",
        f"- Source-link proposals: {workqueue.get('source_link_proposal_count', 0)}",
        f"- Workqueue path: {workqueue.get('workqueue_path') or 'not written'}",
        f"- Proposal path: {workqueue.get('source_link_proposals_path') or 'not written'}",
        "",
        "Next use:",
        "- Use the Explorer Context tab or POST /v2/answer/context to inspect graph paths with resource selectors.",
        "- Review source-grounding-gap-workqueue.jsonl before creating any Resource Layer link packet.",
        "- Treat proposal-only edges as review aids until a separate steward admission workflow accepts them.",
    ]
    return "\n".join(lines) + "\n"


def run_source_grounding_inventory(config: SourceGroundingInventoryConfig) -> SourceGroundingInventorySummary:
    input_path = Path(config.input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"AEC backbone input does not exist: {input_path}")
    resource_layer_root = Path(config.resource_layer_root)
    semantic_overlay_root = Path(config.semantic_overlay_root)
    run_id = config.run_id or safe_run_id()
    output_dir = Path(config.output_root) / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    graph_payload = read_json_object(input_path)
    records = [record for record in graph_payload.get("records", []) if isinstance(record, dict)]
    relationships = [edge for edge in graph_payload.get("relationships", []) if isinstance(edge, dict)]
    resource_indexes = build_resource_indexes(resource_layer_root)
    accepted_links_by_node = resource_indexes["accepted_links_by_node"]
    accepted_links_by_edge = resource_indexes["accepted_links_by_edge"]

    node_classifications = {str(record.get("id")): classify_node(record, accepted_links_by_node) for record in records}
    relationship_classifications = {edge_key(edge): classify_relationship(edge, accepted_links_by_edge) for edge in relationships}

    max_examples = max(0, int(config.max_gap_examples))
    node_gap_examples: list[dict[str, Any]] = []
    for record in records:
        node_id = str(record.get("id") or "")
        if node_classifications.get(node_id) == "source_backed":
            continue
        bounded_append(
            node_gap_examples,
            {
                "node_id": node_id,
                "label": sanitize_excerpt(record.get("pref_label") or record.get("label")),
                "path_code": record.get("path_code"),
                "classification": node_classifications.get(node_id, "unsupported"),
            },
            max_examples,
        )

    relationship_gap_examples: list[dict[str, Any]] = []
    for edge in relationships:
        key = edge_key(edge)
        if relationship_classifications.get(key) == "source_backed":
            continue
        bounded_append(
            relationship_gap_examples,
            {
                "edge_key": key,
                "from_id": edge.get("from_id"),
                "predicate": edge.get("predicate"),
                "to_id": edge.get("to_id"),
                "classification": relationship_classifications.get(key, "unsupported"),
            },
            max_examples,
        )

    overlay_dir = resolve_overlay_run(semantic_overlay_root, config.relationship_run_id)
    overlay = overlay_counts(overlay_dir)
    node_counts = count_by(node_classifications.values())
    relationship_counts = count_by(relationship_classifications.values())
    source_family_distribution = count_by(
        str(family_id)
        for edge in relationships
        for family_id in source_family_ids(edge.get("source_family_ids") or edge.get("sourceFamilyIds"))
    )
    workqueue_path: Path | None = None
    source_link_proposals_path: Path | None = None
    workqueue_items: list[dict[str, Any]] = []
    source_link_proposals: list[dict[str, Any]] = []
    if config.write_gap_workqueue:
        resource_candidates = build_resource_candidates(resource_indexes["resources"])
        workqueue_items, source_link_proposals = build_source_gap_workqueue(
            run_id=run_id,
            records=records,
            relationships=relationships,
            node_classifications=node_classifications,
            relationship_classifications=relationship_classifications,
            resource_candidates=resource_candidates,
            max_items=int(config.max_workqueue_items),
            max_resource_proposals_per_item=int(config.max_resource_proposals_per_item),
            min_resource_proposal_score=float(config.min_resource_proposal_score),
        )
        workqueue_path = output_dir / "source-grounding-gap-workqueue.jsonl"
        source_link_proposals_path = output_dir / "source-link-proposals.jsonl"
        write_jsonl(workqueue_path, workqueue_items)
        write_jsonl(source_link_proposals_path, source_link_proposals)

    report = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "generated_at_utc": utc_now_z(),
        "input_path": str(input_path.resolve()),
        "output_dir": str(output_dir.resolve()),
        "resource_layer_root": str(resource_layer_root.resolve()),
        "semantic_overlay_root": str(semantic_overlay_root.resolve()),
        "selected_semantic_overlay_run_id": overlay.get("run_id"),
        "pending_only": True,
        "no_write": True,
        "graph": {
            "node_count": len(records),
            "relationship_count": len(relationships),
        },
        "resource_layer": {
            "resource_count": len(resource_indexes["resources"]),
            "node_resource_link_count": len(resource_indexes["links"]),
            "accepted_node_resource_link_count": len(resource_indexes["accepted_links"]),
            "source_family_count": len(resource_indexes["source_families"]),
        },
        "coverage": {
            "nodes": {
                "total": len(records),
                "source_backed": node_counts.get("source_backed", 0),
                "domain_synthesis": node_counts.get("domain_synthesis", 0),
                "unsupported": node_counts.get("unsupported", 0),
                "source_backed_rate": round(node_counts.get("source_backed", 0) / max(len(records), 1), 6),
            },
            "relationships": {
                "total": len(relationships),
                "source_backed": relationship_counts.get("source_backed", 0),
                "domain_synthesis": relationship_counts.get("domain_synthesis", 0),
                "unsupported": relationship_counts.get("unsupported", 0),
                "source_backed_rate": round(relationship_counts.get("source_backed", 0) / max(len(relationships), 1), 6),
                "source_family_distribution": source_family_distribution,
            },
        },
        "pending_overlay_summary": overlay,
        "source_gap_workqueue": {
            "enabled": bool(config.write_gap_workqueue),
            "schema_version": "aec-source-grounding-gap-workqueue/v1",
            "proposal_schema_version": "aec-source-link-proposal/v1",
            "workqueue_path": str(workqueue_path.resolve()) if workqueue_path else None,
            "source_link_proposals_path": str(source_link_proposals_path.resolve()) if source_link_proposals_path else None,
            "workqueue_item_count": len(workqueue_items),
            "source_link_proposal_count": len(source_link_proposals),
            "max_workqueue_items": int(config.max_workqueue_items),
            "max_resource_proposals_per_item": int(config.max_resource_proposals_per_item),
            "min_resource_proposal_score": float(config.min_resource_proposal_score),
            "top_priorities": [
                {
                    "priority_rank": item.get("priority_rank"),
                    "priority_score": item.get("priority_score"),
                    "item_type": item.get("item_type"),
                    "node_id": item.get("node_id"),
                    "edge_key": item.get("edge_key"),
                    "suggested_resource_count": len(item.get("suggested_resources", [])),
                }
                for item in workqueue_items[:10]
            ],
            "pending_only": True,
            "auto_admit": False,
            "active_graph_mutation": False,
            "resource_layer_mutation": False,
        },
        "gap_examples": {
            "nodes_without_accepted_resources": node_gap_examples,
            "relationships_without_source_support": relationship_gap_examples,
        },
        "safety": {
            "active_graph_mutation": False,
            "resource_layer_mutation": False,
            "neo4j_writes": False,
            "postgres_writes": False,
            "protected_payload_included": False,
            "pending_overlay_admission": False,
        },
    }
    report_path = output_dir / "source-grounding-inventory-report.json"
    summary_path = output_dir / "source-grounding-inventory-summary.txt"
    write_json(report_path, report)
    summary_path.write_text(build_summary_text(report), encoding="utf-8")

    return SourceGroundingInventorySummary(
        run_id=run_id,
        output_dir=str(output_dir.resolve()),
        report_path=str(report_path.resolve()),
        summary_path=str(summary_path.resolve()),
        node_count=len(records),
        relationship_count=len(relationships),
        node_source_backed_count=node_counts.get("source_backed", 0),
        relationship_source_backed_count=relationship_counts.get("source_backed", 0),
        pending_relationship_overlay_count=int(overlay.get("pending_relationship_overlay_count") or 0),
        pending_node_consolidation_overlay_count=int(overlay.get("pending_node_consolidation_overlay_count") or 0),
        workqueue_path=str(workqueue_path.resolve()) if workqueue_path else None,
        source_link_proposals_path=str(source_link_proposals_path.resolve()) if source_link_proposals_path else None,
        workqueue_item_count=len(workqueue_items),
        source_link_proposal_count=len(source_link_proposals),
    )
