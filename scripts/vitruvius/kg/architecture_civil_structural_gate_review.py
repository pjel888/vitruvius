"""Gated follow-up review for Architecture/Civil/Structural Backbone gaps.

This module does not admit protected source payloads, project/AHJ numerical
criteria, or live graph promotion. It makes the remaining externally gated gaps
explicit and machine-checkable:

* duplicate-label merge candidates are exported for steward review only;
* project/AHJ criteria packets are validated before any future admission path;
* production/live promotion remains blocked unless credentials and rollback
  proof are present.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

DEFAULT_BACKBONE_PATH = Path("scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json")
REPORT_ROOT = Path("006_System-Manifests/aec-mepfs-backbone/architecture-civil-structural-gated-review")
REPORT_FILENAME = "architecture-civil-structural-gated-review-report.json"
DUPLICATE_REVIEW_FILENAME = "duplicate-merge-review-candidates.json"
STEWARD_APPLY_PLAN_FILENAME = "steward-duplicate-apply-plan-dry-run.json"
STEWARD_PRESERVE_PACKET_SKELETON_FILENAME = "steward-preserve-packet-skeleton.json"
CRITERIA_PACKET_SKELETON_FILENAME = "criteria-packet-skeleton.json"
AUTHORITY_LEDGER_SKELETON_FILENAME = "authority-ledger-skeleton.json"
PROTECTED_PAYLOAD_MANIFEST_SKELETON_FILENAME = "protected-payload-manifest-skeleton.json"
LIVE_PROMOTION_PLAN_SKELETON_FILENAME = "live-promotion-plan-skeleton.json"
ROLLBACK_HASH_CHAIN_MANIFEST_FILENAME = "rollback-hash-chain-manifest-skeleton.json"
READINESS_BUNDLE_FILENAME = "external-gate-readiness-bundle.json"
RAW_SOURCE_ROOT = Path("001_Raw-Source-Layer")
REPORT_SCHEMA_VERSION = "aec-mepfs-architecture-civil-structural-gated-review/v1"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")
PRODUCTION_NEO4J_CREDENTIAL_NAMES = (
    "VITRUVIUS_PRODUCTION_NEO4J_URI",
    "VITRUVIUS_PRODUCTION_NEO4J_USER",
    "VITRUVIUS_PRODUCTION_NEO4J_PASSWORD",
)
AUTHORITY_TYPES = {
    "ahj",
    "legal",
    "steward",
    "source_rights",
    "project_owner",
    "professional_record",
}
STEWARD_DECISION_ACTIONS = {
    "preserve_contextual_duplicate",
    "add_display_disambiguation",
    "add_contextual_alias_after_source_review",
    "select_survivor_node",
    "retire_duplicate_node_with_migration_record",
    "add_alias_to_survivor_after_source_review",
}
SAFE_GLOBAL_DUPLICATE_ACTIONS = {
    "preserve_contextual_duplicate",
    "add_display_disambiguation",
}
P0_PRIORITY_NORMALIZED_LABELS = {
    "concrete",
    "reinforced concrete",
}
PROTECTED_PAYLOAD_EXPOSURE_POLICIES = {
    "hash_only",
    "metadata_only",
    "non_public_internal_reference",
}
FORBIDDEN_PAYLOAD_KEYS = {
    "clause_text",
    "design_flood_elevation",
    "design_wind_speed",
    "formula",
    "live_load_value",
    "numeric_criteria",
    "protected_payload",
    "quote",
    "raw_source_path",
    "secret",
    "source_text",
    "standard_text",
    "table_text",
    "token",
    "password",
}
NUMERIC_CRITERION_REQUIRED_FIELDS = {
    "criterion_name",
    "concept_path_code",
    "value",
    "units",
    "source_id",
    "adopted_edition",
    "ahj_basis",
    "effective_date",
    "source_rights_clearance_state",
}


def run_gated_review(
    *,
    backbone_path: str | Path = DEFAULT_BACKBONE_PATH,
    steward_decision_packet_path: str | Path | None = None,
    criteria_packet_path: str | Path | None = None,
    authority_ledger_path: str | Path | None = None,
    protected_payload_manifest_path: str | Path | None = None,
    live_promotion_plan_path: str | Path | None = None,
    rollback_proof_path: str | Path | None = None,
    repo_root: str | Path | None = None,
    run_id: str | None = None,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = _repo_root(repo_root)
    resolved_run_id = _run_id(run_id)
    backbone_file = _resolve_existing_file(root, Path(backbone_path))
    target_dir = _resolve_output_dir(root, output_dir, resolved_run_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    report_path = target_dir / REPORT_FILENAME
    duplicate_review_path = target_dir / DUPLICATE_REVIEW_FILENAME
    steward_apply_plan_path = target_dir / STEWARD_APPLY_PLAN_FILENAME

    backbone_payload = _load_json_object(backbone_file)
    duplicate_review = _duplicate_merge_review(backbone_payload)
    _write_json(duplicate_review_path, duplicate_review)

    steward_decision_review = _steward_duplicate_decision_review(
        root,
        steward_decision_packet_path=steward_decision_packet_path,
        duplicate_review=duplicate_review,
    )
    _write_json(steward_apply_plan_path, steward_decision_review["apply_plan"])
    criteria_review = _criteria_packet_review(
        root,
        criteria_packet_path=criteria_packet_path,
        backbone_payload=backbone_payload,
    )
    authority_review = _authority_ledger_review(root, authority_ledger_path=authority_ledger_path)
    protected_payload_review = _protected_payload_manifest_review(
        root,
        protected_payload_manifest_path=protected_payload_manifest_path,
    )
    payload_leak_review = _payload_leak_review(
        root,
        named_payloads={"backbone": backbone_payload},
        optional_paths={
            "steward_decision_packet": steward_decision_packet_path,
            "criteria_packet": criteria_packet_path,
            "authority_ledger": authority_ledger_path,
            "protected_payload_manifest": protected_payload_manifest_path,
            "live_promotion_plan": live_promotion_plan_path,
            "rollback_proof": rollback_proof_path,
        },
    )
    live_promotion_review = _live_promotion_review(
        root,
        rollback_proof_path=rollback_proof_path,
        live_promotion_plan_path=live_promotion_plan_path,
    )
    boundaries = {
        "file_backed_only": True,
        "shadow_only": True,
        "canonical_label_mutation": False,
        "numeric_criteria_admission": False,
        "protected_payload_ingest": False,
        "live_neo4j_writes": False,
        "production_promotion": False,
        "batch_merge_blocked": True,
        "non_destructive_batch_only": True,
    }
    readiness_artifact_paths = _write_readiness_artifacts(
        root=root,
        target_dir=target_dir,
        report_path=report_path,
        duplicate_review_path=duplicate_review_path,
        duplicate_review=duplicate_review,
        steward_decision_review=steward_decision_review,
        criteria_review=criteria_review,
        authority_review=authority_review,
        protected_payload_review=protected_payload_review,
        live_promotion_review=live_promotion_review,
        boundaries=boundaries,
    )

    errors = [
        *steward_decision_review["errors"],
        *criteria_review["errors"],
        *authority_review["errors"],
        *protected_payload_review["errors"],
        *payload_leak_review["errors"],
        *live_promotion_review["errors"],
    ]
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "run_id": resolved_run_id,
        "generated_at_utc": _utc_now(),
        "ok": not errors,
        "status": "safe_file_backed_gate_review_complete" if not errors else "gate_review_failed",
        "errors": errors,
        "warnings": [
            *duplicate_review["warnings"],
            *steward_decision_review["warnings"],
            *criteria_review["warnings"],
            *authority_review["warnings"],
            *protected_payload_review["warnings"],
            *payload_leak_review["warnings"],
            *live_promotion_review["warnings"],
        ],
        "boundaries": boundaries,
        "backbone_path": _relative_to_root(backbone_file, root),
        "report_path": _relative_to_root(report_path, root),
        "duplicate_merge_review_path": _relative_to_root(duplicate_review_path, root),
        "steward_duplicate_apply_plan_path": _relative_to_root(steward_apply_plan_path, root),
        "readiness_artifact_paths": readiness_artifact_paths,
        "duplicate_merge_review": duplicate_review["summary"],
        "steward_duplicate_decision_gate": steward_decision_review["summary"],
        "criteria_admission_gate": criteria_review["summary"],
        "external_authority_ledger_gate": authority_review["summary"],
        "protected_payload_manifest_gate": protected_payload_review["summary"],
        "payload_leak_audit": payload_leak_review["summary"],
        "live_promotion_gate": live_promotion_review["summary"],
    }
    _write_json(report_path, report)
    return report


def _duplicate_merge_review(payload: dict[str, Any]) -> dict[str, Any]:
    records = [
        row
        for row in _dict_list(payload.get("records"))
        if row.get("record_type") == "BackboneNode" and row.get("path_code") and row.get("label")
    ]
    by_path = {str(row.get("path_code")): row for row in records}
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        groups[_norm(row.get("label"))].append(row)

    candidates: list[dict[str, Any]] = []
    same_parent_count = 0
    cross_parent_count = 0
    cross_root_count = 0
    for normalized_label, rows in sorted(groups.items()):
        if len(rows) < 2:
            continue
        parent_paths = {str(row.get("parent_path_code") or "") for row in rows}
        root_paths = {str(row.get("path_code") or "").split(".", 1)[0] for row in rows}
        if len(parent_paths) == 1:
            duplicate_scope = "same_parent"
            review_class = "same_parent_blocker"
            same_parent_count += 1
        elif len(root_paths) > 1:
            duplicate_scope = "cross_root"
            review_class = "contextual_duplicate_steward_review_required"
            cross_root_count += 1
        else:
            duplicate_scope = "cross_parent"
            review_class = "contextual_duplicate_steward_review_required"
            cross_parent_count += 1
        is_p0 = normalized_label in P0_PRIORITY_NORMALIZED_LABELS
        candidates.append(
            {
                "normalized_label": normalized_label,
                "node_count": len(rows),
                "duplicate_scope": duplicate_scope,
                "review_class": review_class,
                "recommended_action": (
                    "block_until_steward_merge_decision"
                    if duplicate_scope == "same_parent"
                    else "preserve_canonical_labels_and_review_alias_or_display_disambiguation"
                ),
                "canonical_label_mutation_performed": False,
                "auto_merge_allowed": False,
                "batch_merge_blocked": True,
                "default_action": (
                    "steward_select_survivor_and_alias_or_retire_duplicate_node"
                    if duplicate_scope == "same_parent"
                    else "preserve_canonical_labels"
                ),
                "allowed_steward_actions": (
                    [
                        "select_survivor_node",
                        "retire_duplicate_node_with_migration_record",
                        "add_alias_to_survivor_after_source_review",
                    ]
                    if duplicate_scope == "same_parent"
                    else [
                        "preserve_contextual_duplicate",
                        "add_display_disambiguation",
                        "add_contextual_alias_after_source_review",
                    ]
                ),
                "alias_or_display_disambiguation_options": [
                    f"{row.get('label')} ({row.get('path_code')})" for row in rows[:5]
                ],
                "requires_steward_decision": True,
                "requires_explicit_steward_decision": is_p0,
                "priority": "P0" if is_p0 else None,
                "safety_critical": is_p0,
                "nodes": [_duplicate_node_context(row, by_path) for row in rows],
            }
        )

    return {
        "summary": {
            "candidate_group_count": len(candidates),
            "candidate_node_count": sum(candidate["node_count"] for candidate in candidates),
            "same_parent_blocker_group_count": same_parent_count,
            "cross_parent_contextual_group_count": cross_parent_count,
            "cross_root_contextual_group_count": cross_root_count,
            "canonical_label_mutation_performed": False,
            "auto_merge_allowed": False,
            "steward_review_required": len(candidates) > 0,
        },
        "warnings": (
            [f"duplicate merge review candidates require steward decision: {len(candidates)} groups"]
            if candidates
            else []
        ),
        "candidates": candidates,
    }


def _steward_duplicate_decision_review(
    root: Path,
    *,
    steward_decision_packet_path: str | Path | None,
    duplicate_review: dict[str, Any],
) -> dict[str, Any]:
    candidate_count = int(duplicate_review["summary"]["candidate_group_count"])
    same_parent_count = int(duplicate_review["summary"]["same_parent_blocker_group_count"])
    if steward_decision_packet_path is None:
        return {
            "summary": {
                "status": "blocked_missing_steward_decision_packet",
                "candidate_group_count": candidate_count,
                "validated_decision_count": 0,
                "canonical_label_mutation_performed": False,
                "alias_application_performed": False,
                "migration_write_performed": False,
                "auto_merge_allowed": False,
                "required_external_evidence": [
                    "packet_id",
                    "steward",
                    "decision_date",
                    "authority_record_id",
                    "decision_scope_or_decisions",
                    "rationale",
                    "evidence_paths",
                ],
            },
            "apply_plan": _steward_apply_plan(
                status="blocked_missing_steward_decision_packet",
                validated_decision_count=0,
                candidate_count=candidate_count,
                operations=[],
            ),
            "warnings": ["steward duplicate decision packet not provided; canonical duplicate apply pass remains blocked"],
            "errors": [],
        }

    packet_file = _resolve_existing_file(root, Path(steward_decision_packet_path))
    packet = _load_json_object(packet_file)
    packet_sha256 = _sha256_json(packet)
    errors: list[str] = []
    warnings: list[str] = []
    for field in ("packet_id", "steward", "decision_date", "authority_record_id", "rationale"):
        if not _has_value(packet.get(field)):
            errors.append(f"steward_decision_packet.{field}: required field missing")
    _validate_evidence_paths(root, _list_strings(packet.get("evidence_paths")), "steward_decision_packet.evidence_paths", errors)

    candidates_by_label = {
        str(candidate.get("normalized_label") or ""): candidate for candidate in _dict_list(duplicate_review.get("candidates"))
    }
    validated_count = 0
    decision_scope = str(packet.get("decision_scope") or "")
    default_action = str(packet.get("default_action") or "")
    if decision_scope == "all_current_duplicate_candidates":
        if default_action not in SAFE_GLOBAL_DUPLICATE_ACTIONS:
            errors.append(
                "steward_decision_packet.default_action: global duplicate decisions may only preserve or display-disambiguate"
            )
        if same_parent_count:
            errors.append("steward_decision_packet.decision_scope: same-parent blockers require explicit per-group decisions")
        if not errors:
            validated_count = candidate_count
            warnings.append(
                "global steward decision validates current duplicate candidates but does not mutate canonical labels or aliases"
            )
    else:
        decisions = _dict_list(packet.get("decisions"))
        if not decisions:
            errors.append("steward_decision_packet.decisions: expected non-empty list or decision_scope=all_current_duplicate_candidates")
        for index, decision in enumerate(decisions):
            prefix = f"steward_decision_packet.decisions[{index}]"
            action = str(decision.get("action") or "")
            normalized_label = str(decision.get("normalized_label") or "")
            if action not in STEWARD_DECISION_ACTIONS:
                errors.append(f"{prefix}.action: unsupported steward action '{action}'")
            candidate = candidates_by_label.get(normalized_label)
            if not candidate:
                errors.append(f"{prefix}.normalized_label: duplicate candidate not found")
            if not _has_value(decision.get("rationale")):
                errors.append(f"{prefix}.rationale: required field missing")
            _validate_evidence_paths(root, _list_strings(decision.get("evidence_paths")), f"{prefix}.evidence_paths", errors)
            if action in {
                "select_survivor_node",
                "retire_duplicate_node_with_migration_record",
                "add_alias_to_survivor_after_source_review",
            }:
                if not _list_strings(decision.get("source_rights_ids")):
                    errors.append(f"{prefix}.source_rights_ids: required for merge/alias/retire actions")
                if not _has_value(decision.get("survivor_node_id")):
                    errors.append(f"{prefix}.survivor_node_id: required for merge/alias/retire actions")
                _validate_evidence_paths(
                    root,
                    _list_strings(decision.get("migration_evidence_paths")),
                    f"{prefix}.migration_evidence_paths",
                    errors,
                )
            if candidate and action:
                validated_count += 1
        if validated_count and validated_count < candidate_count:
            warnings.append("steward decision packet validates partially; unaddressed duplicate groups remain review-only")
        elif validated_count == candidate_count:
            warnings.append("steward decision packet covers all current duplicate groups without mutating graph data")

    return {
        "summary": {
            "status": "validated_not_applied" if not errors else "rejected",
            "steward_decision_packet_path": _relative_to_root(packet_file, root),
            "candidate_group_count": candidate_count,
            "validated_decision_count": validated_count if not errors else 0,
            "canonical_label_mutation_performed": False,
            "alias_application_performed": False,
            "migration_write_performed": False,
            "auto_merge_allowed": False,
        },
        "apply_plan": _steward_apply_plan(
            status="validated_not_applied" if not errors else "rejected",
            validated_decision_count=validated_count if not errors else 0,
            candidate_count=candidate_count,
            operations=_steward_apply_operations(packet, duplicate_review) if not errors else [],
            packet_path=_relative_to_root(packet_file, root),
            packet_sha256=packet_sha256,
        ),
        "warnings": warnings,
        "errors": errors,
    }


def _steward_apply_plan(
    *,
    status: str,
    validated_decision_count: int,
    candidate_count: int,
    operations: list[dict[str, Any]],
    packet_path: str | None = None,
    packet_sha256: str | None = None,
) -> dict[str, Any]:
    linked_ops = _link_hash_chain(operations)
    final_hash = linked_ops[-1]["operation_hash"] if linked_ops else None
    return {
        "schema_version": "aec-mepfs-steward-duplicate-apply-plan-dry-run/v1",
        "status": status,
        "packet_path": packet_path,
        "packet_sha256": packet_sha256,
        "candidate_group_count": candidate_count,
        "validated_decision_count": validated_decision_count,
        "operation_count": len(linked_ops),
        "operations": linked_ops,
        "hash_chain_final_hash": final_hash,
        "boundaries": {
            "dry_run_only": True,
            "canonical_label_mutation_performed": False,
            "alias_application_performed": False,
            "migration_write_performed": False,
            "auto_merge_allowed": False,
            "batch_merge_blocked": True,
            "non_destructive_batch_only": True,
        },
    }


def _steward_apply_operations(packet: dict[str, Any], duplicate_review: dict[str, Any]) -> list[dict[str, Any]]:
    candidate_labels = [
        str(candidate.get("normalized_label") or "") for candidate in _dict_list(duplicate_review.get("candidates"))
    ]
    if str(packet.get("decision_scope") or "") == "all_current_duplicate_candidates":
        action = str(packet.get("default_action") or "")
        return [
            {
                "normalized_label": label,
                "action": action,
                "dry_run_only": True,
                "canonical_label_mutation_performed": False,
                "alias_application_performed": False,
                "migration_write_performed": False,
            }
            for label in candidate_labels
        ]
    operations: list[dict[str, Any]] = []
    for decision in _dict_list(packet.get("decisions")):
        operations.append(
            {
                "normalized_label": decision.get("normalized_label"),
                "action": decision.get("action"),
                "survivor_node_id": decision.get("survivor_node_id"),
                "dry_run_only": True,
                "canonical_label_mutation_performed": False,
                "alias_application_performed": False,
                "migration_write_performed": False,
            }
        )
    return operations


def _link_hash_chain(operations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prev_hash = "0" * 64
    for op in operations:
        op["previous_hash"] = prev_hash
        payload = {k: v for k, v in op.items() if k not in ("previous_hash", "operation_hash")}
        op["operation_hash"] = _sha256_json(payload)
        prev_hash = op["operation_hash"]
    return operations


def _write_readiness_artifacts(
    *,
    root: Path,
    target_dir: Path,
    report_path: Path,
    duplicate_review_path: Path,
    duplicate_review: dict[str, Any],
    steward_decision_review: dict[str, Any],
    criteria_review: dict[str, Any],
    authority_review: dict[str, Any],
    protected_payload_review: dict[str, Any],
    live_promotion_review: dict[str, Any],
    boundaries: dict[str, bool],
) -> dict[str, str]:
    artifact_payloads = {
        "steward_preserve_packet_skeleton": (
            target_dir / STEWARD_PRESERVE_PACKET_SKELETON_FILENAME,
            _steward_preserve_packet_skeleton(root, duplicate_review_path, duplicate_review),
        ),
        "criteria_packet_skeleton": (target_dir / CRITERIA_PACKET_SKELETON_FILENAME, _criteria_packet_skeleton()),
        "authority_ledger_skeleton": (target_dir / AUTHORITY_LEDGER_SKELETON_FILENAME, _authority_ledger_skeleton()),
        "protected_payload_manifest_skeleton": (
            target_dir / PROTECTED_PAYLOAD_MANIFEST_SKELETON_FILENAME,
            _protected_payload_manifest_skeleton(),
        ),
        "live_promotion_plan_skeleton": (
            target_dir / LIVE_PROMOTION_PLAN_SKELETON_FILENAME,
            _live_promotion_plan_skeleton(),
        ),
        "rollback_hash_chain_manifest_skeleton": (
            target_dir / ROLLBACK_HASH_CHAIN_MANIFEST_FILENAME,
            _rollback_hash_chain_manifest_skeleton(),
        ),
    }
    paths: dict[str, str] = {}
    for key, (path, payload) in artifact_payloads.items():
        _write_json(path, payload)
        paths[key] = _relative_to_root(path, root)

    bundle_path = target_dir / READINESS_BUNDLE_FILENAME
    _write_json(
        bundle_path,
        _external_gate_readiness_bundle(
            root=root,
            report_path=report_path,
            readiness_artifact_paths=paths,
            steward_decision_review=steward_decision_review,
            criteria_review=criteria_review,
            authority_review=authority_review,
            protected_payload_review=protected_payload_review,
            live_promotion_review=live_promotion_review,
            boundaries=boundaries,
        ),
    )
    paths["external_gate_readiness_bundle"] = _relative_to_root(bundle_path, root)
    return paths


def _steward_preserve_packet_skeleton(
    root: Path,
    duplicate_review_path: Path,
    duplicate_review: dict[str, Any],
) -> dict[str, Any]:
    summary = duplicate_review["summary"]
    same_parent_count = int(summary["same_parent_blocker_group_count"])
    can_global_preserve = same_parent_count == 0
    candidate_set_sha256 = _sha256_json(_dict_list(duplicate_review.get("candidates")))
    return {
        "schema_version": "aec-mepfs-steward-preserve-packet-skeleton/v1",
        "status": "draft_requires_steward_authority",
        "draft_only": True,
        "not_valid_without_steward_fields": [
            "packet_id",
            "steward",
            "decision_date",
            "authority_record_id",
            "rationale",
            "evidence_paths",
        ],
        "packet_id": None,
        "steward": None,
        "decision_date": None,
        "authority_record_id": None,
        "rationale": None,
        "evidence_paths": [],
        "decision_scope": "all_current_duplicate_candidates" if can_global_preserve else None,
        "default_action": "preserve_contextual_duplicate" if can_global_preserve else None,
        "requires_explicit_per_group_decisions": not can_global_preserve,
        "repo_derived_context": {
            "duplicate_review_path": _relative_to_root(duplicate_review_path, root),
            "candidate_group_count": summary["candidate_group_count"],
            "candidate_node_count": summary["candidate_node_count"],
            "same_parent_blocker_group_count": same_parent_count,
            "candidate_set_sha256": candidate_set_sha256,
        },
        "boundaries": _draft_boundary_flags(),
    }


def _criteria_packet_skeleton() -> dict[str, Any]:
    return {
        "schema_version": "aec-mepfs-criteria-packet-skeleton/v1",
        "status": "draft_requires_project_ahj_authority",
        "draft_only": True,
        "packet_id": None,
        "project_id": None,
        "jurisdiction_id": None,
        "ahj_authority": None,
        "steward_approval_id": None,
        "adopted_sources": [],
        "criteria": [],
        "required_criterion_fields": sorted(NUMERIC_CRITERION_REQUIRED_FIELDS),
        "cannot_autofill": [
            "project identity",
            "jurisdiction and AHJ adoption basis",
            "adopted source editions",
            "criterion values with units and effective dates",
            "source-rights clearance",
            "steward approval",
        ],
        "validation_command_hint": (
            "python -m vitruvius.kg.architecture_civil_structural_gate_review "
            "--criteria-packet <path-to-completed-packet>"
        ),
        "boundaries": _draft_boundary_flags(),
    }


def _authority_ledger_skeleton() -> dict[str, Any]:
    return {
        "schema_version": "aec-mepfs-authority-ledger-skeleton/v1",
        "status": "draft_requires_external_authority",
        "draft_only": True,
        "authority_records": [],
        "allowed_authority_types": sorted(AUTHORITY_TYPES),
        "required_record_fields": [
            "authority_id",
            "authority_type",
            "scope",
            "decision_status",
            "steward",
            "decision_date",
            "evidence_paths",
        ],
        "cannot_autofill": [
            "legal or steward identity",
            "authority decision status",
            "authority scope",
            "supporting evidence files",
            "source-rights identifiers for approved or admitted decisions",
        ],
        "validation_command_hint": (
            "python -m vitruvius.kg.architecture_civil_structural_gate_review "
            "--authority-ledger <path-to-completed-ledger>"
        ),
        "boundaries": _draft_boundary_flags(),
    }


def _protected_payload_manifest_skeleton() -> dict[str, Any]:
    return {
        "schema_version": "aec-mepfs-protected-payload-manifest-skeleton/v1",
        "status": "draft_requires_source_rights_authority",
        "draft_only": True,
        "manifest_id": None,
        "steward": None,
        "decision_date": None,
        "authority_record_ids": [],
        "evidence_paths": [],
        "payloads": [],
        "required_payload_fields": [
            "payload_id",
            "source_id",
            "source_rights_id",
            "content_sha256",
            "admitted_use",
            "exposure_policy",
        ],
        "allowed_exposure_policies": sorted(PROTECTED_PAYLOAD_EXPOSURE_POLICIES),
        "cannot_autofill": [
            "source-rights decision",
            "rights-cleared content hash",
            "admitted use",
            "safe exposure policy",
            "supporting evidence files",
        ],
        "validation_command_hint": (
            "python -m vitruvius.kg.architecture_civil_structural_gate_review "
            "--protected-payload-manifest <path-to-completed-manifest>"
        ),
        "boundaries": _draft_boundary_flags(),
    }


def _live_promotion_plan_skeleton() -> dict[str, Any]:
    return {
        "schema_version": "aec-mepfs-live-promotion-plan-skeleton/v1",
        "status": "draft_requires_credentials_backup_restore_and_rollback",
        "draft_only": True,
        "plan_id": None,
        "approved_by": None,
        "approved_at": None,
        "target_environment": "production",
        "backup_artifact_path": None,
        "restore_test_artifact_path": None,
        "rollback_transcript_path": None,
        "required_environment_variable_names": list(PRODUCTION_NEO4J_CREDENTIAL_NAMES),
        "credential_values_stored": False,
        "cannot_autofill": [
            "production credential values",
            "backup artifact",
            "restore-test artifact",
            "rollback transcript",
            "live promotion approval",
        ],
        "validation_command_hint": (
            "python -m vitruvius.kg.architecture_civil_structural_gate_review "
            "--live-promotion-plan <path-to-completed-plan>"
        ),
        "boundaries": _draft_boundary_flags(),
    }


def _rollback_hash_chain_manifest_skeleton() -> dict[str, Any]:
    return {
        "schema_version": "aec-mepfs-rollback-hash-chain-manifest-skeleton/v1",
        "status": "draft_requires_rollback_evidence",
        "draft_only": True,
        "manifest_id": None,
        "steward": None,
        "decision_date": None,
        "chain": [
            {
                "link_type": "backup_artifact",
                "artifact_path": None,
                "content_sha256": None,
                "previous_hash": "0" * 64,
                "link_hash": None,
            },
            {
                "link_type": "restore_test_artifact",
                "artifact_path": None,
                "content_sha256": None,
                "previous_hash": None,
                "link_hash": None,
            },
            {
                "link_type": "rollback_transcript",
                "artifact_path": None,
                "content_sha256": None,
                "previous_hash": None,
                "link_hash": None,
            },
        ],
        "cannot_autofill": [
            "backup artifact content hash",
            "restore-test artifact content hash",
            "rollback transcript content hash",
            "cryptographic chain linkage",
        ],
        "boundaries": _draft_boundary_flags(),
    }


def _external_gate_readiness_bundle(
    *,
    root: Path,
    report_path: Path,
    readiness_artifact_paths: dict[str, str],
    steward_decision_review: dict[str, Any],
    criteria_review: dict[str, Any],
    authority_review: dict[str, Any],
    protected_payload_review: dict[str, Any],
    live_promotion_review: dict[str, Any],
    boundaries: dict[str, bool],
) -> dict[str, Any]:
    gate_statuses = {
        "steward_duplicate_decision": steward_decision_review["summary"]["status"],
        "project_ahj_criteria": criteria_review["summary"]["status"],
        "external_authority_ledger": authority_review["summary"]["status"],
        "protected_payload_manifest": protected_payload_review["summary"]["status"],
        "live_promotion_credentials_and_rollback": live_promotion_review["summary"]["status"],
    }
    return {
        "schema_version": "aec-mepfs-external-gate-readiness-bundle/v1",
        "status": "external_inputs_required",
        "draft_only": True,
        "report_path": _relative_to_root(report_path, root),
        "readiness_artifact_paths": readiness_artifact_paths,
        "gate_statuses": gate_statuses,
        "blocked_categories": [
            {
                "category": "steward_duplicate_decision",
                "current_status": gate_statuses["steward_duplicate_decision"],
                "generated_skeleton": readiness_artifact_paths["steward_preserve_packet_skeleton"],
                "cannot_autofill": ["steward identity", "authority record", "evidence paths", "final rationale"],
            },
            {
                "category": "project_ahj_criteria",
                "current_status": gate_statuses["project_ahj_criteria"],
                "generated_skeleton": readiness_artifact_paths["criteria_packet_skeleton"],
                "cannot_autofill": ["AHJ adoption basis", "source editions", "values", "units", "effective dates"],
            },
            {
                "category": "external_authority_ledger",
                "current_status": gate_statuses["external_authority_ledger"],
                "generated_skeleton": readiness_artifact_paths["authority_ledger_skeleton"],
                "cannot_autofill": ["legal/source-rights/steward authority", "decision evidence"],
            },
            {
                "category": "protected_payload_manifest",
                "current_status": gate_statuses["protected_payload_manifest"],
                "generated_skeleton": readiness_artifact_paths["protected_payload_manifest_skeleton"],
                "cannot_autofill": ["rights-cleared content hashes", "admitted use", "evidence files"],
            },
            {
                "category": "live_promotion_credentials_and_rollback",
                "current_status": gate_statuses["live_promotion_credentials_and_rollback"],
                "generated_skeleton": readiness_artifact_paths["live_promotion_plan_skeleton"],
                "cannot_autofill": ["secret credential values", "backup proof", "restore proof", "rollback transcript"],
            },
        ],
        "operations_not_performed": {
            "canonical_label_mutation": True,
            "alias_application": True,
            "migration_write": True,
            "numeric_admission": True,
            "protected_payload_ingest": True,
            "live_neo4j_write": True,
            "production_promotion": True,
        },
        "boundaries": boundaries,
    }


def _draft_boundary_flags() -> dict[str, bool]:
    return {
        "draft_only": True,
        "canonical_label_mutation_performed": False,
        "alias_application_performed": False,
        "migration_write_performed": False,
        "numeric_criteria_admission_performed": False,
        "protected_payload_ingest_performed": False,
        "public_payload_exposure_performed": False,
        "live_neo4j_write_performed": False,
        "production_promotion_performed": False,
    }


def _authority_ledger_review(root: Path, *, authority_ledger_path: str | Path | None) -> dict[str, Any]:
    if authority_ledger_path is None:
        return {
            "summary": {
                "status": "blocked_missing_external_authority_ledger",
                "validated_authority_record_count": 0,
                "admission_authorized": False,
                "required_external_evidence": [
                    "authority_id",
                    "authority_type",
                    "scope",
                    "decision_status",
                    "steward",
                    "decision_date",
                    "evidence_paths",
                    "source_rights_ids_for_protected_or_numeric_claims",
                ],
            },
            "warnings": ["external authority ledger not provided; externally gated admissions remain blocked"],
            "errors": [],
        }

    ledger_file = _resolve_existing_file(root, Path(authority_ledger_path))
    ledger = _load_json_object(ledger_file)
    records = _dict_list(ledger.get("authority_records"))
    errors: list[str] = []
    if not records:
        errors.append("authority_ledger.authority_records: expected non-empty list")

    validated_count = 0
    for index, record in enumerate(records):
        record_errors: list[str] = []
        for field in ("authority_id", "authority_type", "scope", "decision_status", "steward", "decision_date"):
            if not _has_value(record.get(field)):
                record_errors.append(f"authority_ledger.authority_records[{index}].{field}: required field missing")
        authority_type = str(record.get("authority_type") or "")
        if authority_type and authority_type not in AUTHORITY_TYPES:
            record_errors.append(
                f"authority_ledger.authority_records[{index}].authority_type: unsupported authority type '{authority_type}'"
            )
        evidence_paths = _list_strings(record.get("evidence_paths"))
        if not evidence_paths:
            record_errors.append(f"authority_ledger.authority_records[{index}].evidence_paths: expected non-empty list")
        for path_index, evidence_path in enumerate(evidence_paths):
            try:
                _resolve_existing_file(root, Path(evidence_path))
            except FileNotFoundError:
                record_errors.append(
                    f"authority_ledger.authority_records[{index}].evidence_paths[{path_index}]: evidence path not found"
                )
        if str(record.get("decision_status") or "") in {"approved", "admitted"}:
            if not _list_strings(record.get("source_rights_ids")):
                record_errors.append(
                    f"authority_ledger.authority_records[{index}].source_rights_ids: "
                    "required for approved/admitted external authority records"
                )
        if not record_errors:
            validated_count += 1
        errors.extend(record_errors)

    return {
        "summary": {
            "status": "validated_not_admitted" if not errors else "rejected",
            "authority_ledger_path": _relative_to_root(ledger_file, root),
            "validated_authority_record_count": validated_count if not errors else 0,
            "admission_authorized": False,
            "graph_write_performed": False,
        },
        "warnings": ["authority ledger validates structurally, but this reviewer performs no admission"] if not errors else [],
        "errors": errors,
    }


def _protected_payload_manifest_review(
    root: Path,
    *,
    protected_payload_manifest_path: str | Path | None,
) -> dict[str, Any]:
    if protected_payload_manifest_path is None:
        return {
            "summary": {
                "status": "blocked_missing_protected_payload_manifest",
                "validated_payload_reference_count": 0,
                "protected_payload_ingest_performed": False,
                "public_payload_exposure_performed": False,
                "required_external_evidence": [
                    "manifest_id",
                    "steward",
                    "decision_date",
                    "authority_record_ids",
                    "payloads.source_id",
                    "payloads.source_rights_id",
                    "payloads.content_sha256",
                    "payloads.exposure_policy",
                ],
            },
            "warnings": ["protected payload manifest not provided; protected payload admission remains blocked"],
            "errors": [],
        }

    manifest_file = _resolve_existing_file(root, Path(protected_payload_manifest_path))
    manifest = _load_json_object(manifest_file)
    errors: list[str] = []
    for field in ("manifest_id", "steward", "decision_date"):
        if not _has_value(manifest.get(field)):
            errors.append(f"protected_payload_manifest.{field}: required field missing")
    if not _list_strings(manifest.get("authority_record_ids")):
        errors.append("protected_payload_manifest.authority_record_ids: expected non-empty list")
    _validate_evidence_paths(root, _list_strings(manifest.get("evidence_paths")), "protected_payload_manifest.evidence_paths", errors)

    payloads = _dict_list(manifest.get("payloads"))
    if not payloads:
        errors.append("protected_payload_manifest.payloads: expected non-empty list")
    validated_count = 0
    for index, payload in enumerate(payloads):
        prefix = f"protected_payload_manifest.payloads[{index}]"
        for field in ("payload_id", "source_id", "source_rights_id", "content_sha256", "admitted_use", "exposure_policy"):
            if not _has_value(payload.get(field)):
                errors.append(f"{prefix}.{field}: required field missing")
        content_sha256 = str(payload.get("content_sha256") or "")
        if content_sha256 and not SHA256_RE.match(content_sha256):
            errors.append(f"{prefix}.content_sha256: expected sha256 hex digest")
        exposure_policy = str(payload.get("exposure_policy") or "")
        if exposure_policy and exposure_policy not in PROTECTED_PAYLOAD_EXPOSURE_POLICIES:
            errors.append(f"{prefix}.exposure_policy: unsupported or unsafe exposure policy '{exposure_policy}'")
        if bool(payload.get("payload_text_included")):
            errors.append(f"{prefix}.payload_text_included: protected payload content is blocked")
        forbidden_hits = _forbidden_key_hits(payload, prefix=prefix)
        errors.extend(forbidden_hits)
        if not forbidden_hits:
            validated_count += 1

    return {
        "summary": {
            "status": "validated_not_ingested" if not errors else "rejected",
            "protected_payload_manifest_path": _relative_to_root(manifest_file, root),
            "validated_payload_reference_count": validated_count if not errors else 0,
            "protected_payload_ingest_performed": False,
            "public_payload_exposure_performed": False,
            "graph_write_performed": False,
        },
        "warnings": ["protected payload manifest validates hash-only metadata, but no payload content was ingested"]
        if not errors
        else [],
        "errors": errors,
    }


def _payload_leak_review(
    root: Path,
    *,
    named_payloads: dict[str, Any],
    optional_paths: dict[str, str | Path | None],
) -> dict[str, Any]:
    errors: list[str] = []
    scanned_payload_count = 0
    hit_count = 0

    for payload_name, payload in named_payloads.items():
        scanned_payload_count += 1
        hits = _forbidden_key_hits(payload, prefix=payload_name)
        hit_count += len(hits)
        errors.extend(hits)

    for payload_name, maybe_path in optional_paths.items():
        if maybe_path is None:
            continue
        file_path = _resolve_existing_file(root, Path(maybe_path))
        try:
            payload = _load_json_object(file_path)
        except json.JSONDecodeError:
            continue
        except ValueError:
            continue
        else:
            scanned_payload_count += 1
            hits = _forbidden_key_hits(payload, prefix=payload_name)
            hit_count += len(hits)
            errors.extend(hits)

    return {
        "summary": {
            "status": "passed" if not errors else "rejected_for_forbidden_payload_keys",
            "scanned_payload_count": scanned_payload_count,
            "forbidden_payload_key_hit_count": hit_count,
            "forbidden_keys": sorted(FORBIDDEN_PAYLOAD_KEYS),
        },
        "warnings": [],
        "errors": errors,
    }


def _forbidden_key_hits(value: Any, *, prefix: str) -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            child_prefix = f"{prefix}.{key_text}"
            if key_text.lower() in FORBIDDEN_PAYLOAD_KEYS:
                hits.append(f"{child_prefix}: forbidden protected/numeric/source-payload key")
            hits.extend(_forbidden_key_hits(child, prefix=child_prefix))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(_forbidden_key_hits(child, prefix=f"{prefix}[{index}]"))
    return hits


def _duplicate_node_context(row: dict[str, Any], by_path: dict[str, dict[str, Any]]) -> dict[str, Any]:
    parent_path = str(row.get("parent_path_code") or "")
    parent = by_path.get(parent_path, {})
    return {
        "id": row.get("id"),
        "label": row.get("label"),
        "path_code": row.get("path_code"),
        "parent_path_code": parent_path or None,
        "parent_label": parent.get("label"),
        "display_hint": f"{row.get('label')} · {row.get('path_code')}",
    }


def _criteria_packet_review(
    root: Path,
    *,
    criteria_packet_path: str | Path | None,
    backbone_payload: dict[str, Any],
) -> dict[str, Any]:
    if criteria_packet_path is None:
        return {
            "summary": {
                "status": "blocked_missing_project_ahj_packet",
                "admitted_numeric_criteria_count": 0,
                "validation_only": True,
                "required_external_evidence": [
                    "project_id",
                    "jurisdiction_id",
                    "ahj_authority",
                    "steward_approval_id",
                    "adopted_sources",
                    "source_rights_clearance_for_criteria",
                    "criteria_with_units_and_effective_dates",
                ],
            },
            "warnings": ["project/AHJ numerical criteria remain blocked because no admission packet was provided"],
            "errors": [],
        }

    packet_file = _resolve_existing_file(root, Path(criteria_packet_path))
    packet = _load_json_object(packet_file)
    errors: list[str] = []
    warnings: list[str] = []
    for field in ("packet_id", "project_id", "jurisdiction_id", "ahj_authority", "steward_approval_id"):
        if not _has_value(packet.get(field)):
            errors.append(f"criteria_packet.{field}: required field missing")
    adopted_sources = _dict_list(packet.get("adopted_sources"))
    if not adopted_sources:
        errors.append("criteria_packet.adopted_sources: expected non-empty list")
    criteria = _dict_list(packet.get("criteria"))
    if not criteria:
        errors.append("criteria_packet.criteria: expected non-empty list")

    known_paths = {
        str(row.get("path_code") or "")
        for row in _dict_list(backbone_payload.get("records"))
        if row.get("path_code")
    }
    admitted_count = 0
    for index, criterion in enumerate(criteria):
        criterion_errors: list[str] = []
        missing = sorted(field for field in NUMERIC_CRITERION_REQUIRED_FIELDS if not _has_value(criterion.get(field)))
        for field in missing:
            criterion_errors.append(f"criteria_packet.criteria[{index}].{field}: required field missing")
        concept_path = str(criterion.get("concept_path_code") or "")
        if concept_path and concept_path not in known_paths:
            criterion_errors.append(f"criteria_packet.criteria[{index}].concept_path_code: unknown Backbone path '{concept_path}'")
        if criterion.get("source_rights_clearance_state") != "cleared_for_declared_use":
            criterion_errors.append(
                f"criteria_packet.criteria[{index}].source_rights_clearance_state: "
                "must be cleared_for_declared_use before numerical criteria admission"
            )
        if bool(criterion.get("protected_payload_included")):
            criterion_errors.append(f"criteria_packet.criteria[{index}].protected_payload_included: protected payloads are blocked")
        if not criterion_errors:
            admitted_count += 1
        errors.extend(criterion_errors)

    status = "validated_not_admitted" if not errors else "rejected"
    if not errors:
        warnings.append("criteria packet validates structurally, but this reviewer performs no graph write or numeric admission")
    return {
        "summary": {
            "status": status,
            "criteria_packet_path": _relative_to_root(packet_file, root),
            "admitted_numeric_criteria_count": 0,
            "validated_criteria_count": admitted_count if not errors else 0,
            "validation_only": True,
            "graph_write_performed": False,
        },
        "warnings": warnings,
        "errors": errors,
    }


def _live_promotion_review(
    root: Path,
    *,
    rollback_proof_path: str | Path | None,
    live_promotion_plan_path: str | Path | None,
) -> dict[str, Any]:
    missing_credentials = [name for name in PRODUCTION_NEO4J_CREDENTIAL_NAMES if not os.environ.get(name)]
    errors: list[str] = []
    plan_file: Path | None = None
    plan: dict[str, Any] | None = None
    if live_promotion_plan_path is not None:
        plan_file = _resolve_existing_file(root, Path(live_promotion_plan_path))
        plan = _load_json_object(plan_file)
        for field in ("plan_id", "approved_by", "approved_at", "target_environment"):
            if not _has_value(plan.get(field)):
                errors.append(f"live_promotion_plan.{field}: required field missing")
        if str(plan.get("target_environment") or "") != "production":
            errors.append("live_promotion_plan.target_environment: must be production for this gate")
        for field in ("backup_artifact_path", "restore_test_artifact_path", "rollback_transcript_path"):
            value = str(plan.get(field) or "")
            if not value:
                errors.append(f"live_promotion_plan.{field}: required field missing")
                continue
            try:
                _resolve_existing_file(root, Path(value))
            except FileNotFoundError:
                errors.append(f"live_promotion_plan.{field}: evidence path not found")
    rollback_path: Path | None = None
    if rollback_proof_path is not None:
        rollback_path = _resolve_existing_file(root, Path(rollback_proof_path))
    elif plan is not None and _has_value(plan.get("rollback_transcript_path")):
        try:
            rollback_path = _resolve_existing_file(root, Path(str(plan.get("rollback_transcript_path"))))
        except FileNotFoundError:
            rollback_path = None
    missing_rollback = rollback_path is None
    missing_plan = plan_file is None
    blocked = bool(missing_credentials or missing_rollback or missing_plan or errors)
    return {
        "summary": {
            "status": "blocked_missing_credentials_rollback_or_plan"
            if blocked
            else "credentials_rollback_and_plan_present_dry_run_only",
            "missing_credential_names": missing_credentials,
            "live_promotion_plan_path": _relative_to_root(plan_file, root) if plan_file is not None else None,
            "missing_live_promotion_plan": missing_plan,
            "rollback_proof_path": _relative_to_root(rollback_path, root) if rollback_path is not None else None,
            "live_write_performed": False,
            "production_promotion_performed": False,
        },
        "warnings": (
            ["production/live promotion remains blocked or dry-run only; no Neo4j writes were attempted"]
            if blocked
            else ["credentials and rollback proof are present, but this review remains dry-run only"]
        ),
        "errors": errors,
    }


def _resolve_output_dir(root: Path, output_dir: str | Path | None, run_id: str) -> Path:
    path = root / REPORT_ROOT / run_id if output_dir is None else _resolve_under_root(root, Path(output_dir))
    if _is_relative_to(path, root / RAW_SOURCE_ROOT):
        raise ValueError("refusing to write gated review artifacts inside immutable raw source custody layer")
    if not _is_relative_to(path, root / REPORT_ROOT):
        raise ValueError("refusing to write gated review artifacts outside the System-Manifests gated-review report root")
    return path


def _resolve_existing_file(root: Path, path: Path) -> Path:
    resolved = _resolve_under_root(root, path)
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    return resolved


def _resolve_under_root(root: Path, path: Path) -> Path:
    resolved = path if path.is_absolute() else root / path
    resolved = resolved.resolve()
    if not _is_relative_to(resolved, root):
        raise ValueError(f"path escapes repository root: {path}")
    return resolved


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _load_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [row for row in value if isinstance(row, dict)]


def _list_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item.strip()]


def _validate_evidence_paths(root: Path, paths: list[str], field_path: str, errors: list[str]) -> None:
    if not paths:
        errors.append(f"{field_path}: expected non-empty list")
        return
    for index, evidence_path in enumerate(paths):
        try:
            _resolve_existing_file(root, Path(evidence_path))
        except FileNotFoundError:
            errors.append(f"{field_path}[{index}]: evidence path not found")


def _has_value(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    return value is not None


def _norm(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _sha256_json(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _repo_root(repo_root: str | Path | None) -> Path:
    return Path(repo_root or ".").resolve()


def _relative_to_root(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _run_id(run_id: str | None) -> str:
    value = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    if not RUN_ID_RE.match(value):
        raise ValueError(f"run_id contains unsupported characters: {value}")
    return value


def _utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run safe gated ACS follow-up review.")
    parser.add_argument("--backbone", default=str(DEFAULT_BACKBONE_PATH))
    parser.add_argument("--steward-decision-packet", default=None)
    parser.add_argument("--criteria-packet", default=None)
    parser.add_argument("--authority-ledger", default=None)
    parser.add_argument("--protected-payload-manifest", default=None)
    parser.add_argument("--live-promotion-plan", default=None)
    parser.add_argument("--rollback-proof", default=None)
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args(argv)
    report = run_gated_review(
        backbone_path=args.backbone,
        steward_decision_packet_path=args.steward_decision_packet,
        criteria_packet_path=args.criteria_packet,
        authority_ledger_path=args.authority_ledger,
        protected_payload_manifest_path=args.protected_payload_manifest,
        live_promotion_plan_path=args.live_promotion_plan,
        rollback_proof_path=args.rollback_proof,
        repo_root=args.repo_root,
        run_id=args.run_id,
        output_dir=args.output_dir,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
