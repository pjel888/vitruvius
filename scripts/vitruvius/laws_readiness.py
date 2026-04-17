from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any
from contextlib import redirect_stdout

import yaml

from .canonicalize import build_plan, build_structured_source_file, extract_section_headers, slugify
from .config import get_ollama_default_model, get_ollama_default_parallelism, resolve_review_preset
from .constants import CONVERSION_LAYER_NAME, RAW_LAYER_NAME
from .conversion import SUPPORTED_DIRECT_INPUT_EXTENSIONS, convert_pdf_at_path, run_convert_one
from .detection import detect_pdf_type
from .graph.dataset_manifest import DatasetManifestError, load_dataset_manifest, write_json_report
from .normalization.refine import run_refine_one
from .paths import build_conversion_relative_paths, build_ocr_pdf_relative_path
from .utils import utc_now_stamp


_CONVERSION_LAWS_ROOT = Path("002_Raw-Conversion-Layer") / "001-Laws"
_REFINED_ROOT = _CONVERSION_LAWS_ROOT / "refined_markdown"
_RAW_MARKDOWN_ROOT = _CONVERSION_LAWS_ROOT / "raw_markdown"
_SIDECAR_ROOT = _CONVERSION_LAWS_ROOT / "sidecar_json"
_RAW_SOURCE_ROOT = Path("001_Raw-Source-Layer") / "001-Laws"
_IGNORED_FOLDERS = {"test", "__pycache__"}


def _iter_law_dirs(root: Path) -> list[Path]:
    if not root.exists() or not root.is_dir():
        return []
    return sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and path.name not in _IGNORED_FOLDERS and not path.name.startswith(".")
    )


def _count_child_files(root: Path, suffix: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for law_dir in _iter_law_dirs(root):
        counts[law_dir.name] = len(sorted(law_dir.glob(f"*{suffix}")))
    return counts


def _relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _load_pilot_manifest(repo_root: Path, pilot_manifest: str) -> tuple[Any | None, Path, str | None]:
    manifest_path = Path(pilot_manifest)
    if not manifest_path.is_absolute():
        manifest_path = repo_root / manifest_path
    try:
        manifest = load_dataset_manifest(manifest_path, repo_root)
    except DatasetManifestError as exc:
        return None, manifest_path, str(exc)
    return manifest, manifest_path, None


def _default_report_path(repo_root: Path, run_id: str) -> Path:
    return (
        repo_root
        / "006_System-Manifests"
        / "runs"
        / "datasets"
        / "laws-all-readiness"
        / run_id
        / "all_laws_dry_run_report.json"
    )


def _default_tranche_report_path(repo_root: Path, tranche_id: str, run_id: str) -> Path:
    return (
        repo_root
        / "006_System-Manifests"
        / "runs"
        / "datasets"
        / tranche_id
        / run_id
        / "laws_tranche_dry_run_report.json"
    )


def _default_source_prep_report_path(repo_root: Path, tranche_id: str, run_id: str) -> Path:
    return (
        repo_root
        / "006_System-Manifests"
        / "runs"
        / "datasets"
        / tranche_id
        / run_id
        / "laws_tranche_source_prep_dry_run_report.json"
    )


def _default_source_prep_execute_report_path(repo_root: Path, tranche_id: str, run_id: str) -> Path:
    return (
        repo_root
        / "006_System-Manifests"
        / "runs"
        / "datasets"
        / tranche_id
        / run_id
        / "laws_tranche_source_prep_report.json"
    )


def _default_source_admission_report_path(repo_root: Path, tranche_id: str, run_id: str) -> Path:
    return (
        repo_root
        / "006_System-Manifests"
        / "runs"
        / "datasets"
        / tranche_id
        / run_id
        / "laws_tranche_source_admission_dry_run_report.json"
    )


def _default_source_admission_execute_report_path(repo_root: Path, tranche_id: str, run_id: str) -> Path:
    return (
        repo_root
        / "006_System-Manifests"
        / "runs"
        / "datasets"
        / tranche_id
        / run_id
        / "laws_tranche_source_admission_report.json"
    )


def _capture_text_handler(fn) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = fn()
    return rc, buf.getvalue()


def _load_tranche_manifest(repo_root: Path, tranche_manifest: str) -> tuple[dict[str, Any] | None, Path, str | None]:
    manifest_path = Path(tranche_manifest)
    if not manifest_path.is_absolute():
        manifest_path = repo_root / manifest_path
    try:
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    except OSError as exc:
        return None, manifest_path, str(exc)
    if not isinstance(payload, dict):
        return None, manifest_path, "tranche manifest must be a mapping"
    folders_raw = payload.get("candidate_law_folders") or payload.get("candidate_folders")
    if not isinstance(folders_raw, list) or not folders_raw:
        return None, manifest_path, "tranche manifest requires a non-empty candidate_law_folders list"
    folders: list[dict[str, str]] = []
    for item in folders_raw:
        if not isinstance(item, dict):
            return None, manifest_path, "each candidate_law_folders entry must be a mapping"
        folder_name = item.get("folder_name")
        if not isinstance(folder_name, str) or not folder_name.strip():
            return None, manifest_path, "candidate_law_folders entries must include a non-empty folder_name"
        reason = item.get("reason")
        normalized = dict(item)
        normalized["folder_name"] = folder_name.strip()
        normalized["reason"] = reason.strip() if isinstance(reason, str) else ""
        folders.append(normalized)
    payload["candidate_law_folders"] = folders
    return payload, manifest_path, None


def _count_structural_headers(refined_root: Path, folder_name: str) -> int:
    folder = refined_root / folder_name
    if not folder.exists():
        return 0
    count = 0
    for path in sorted(folder.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        count += len(extract_section_headers(text))
    return count


def _structure_guardrails(
    *,
    structural_header_count: int,
    admitted_concept_count: int,
    admitted_relationship_count: int,
) -> list[str]:
    flags: list[str] = []
    if structural_header_count >= 20 and admitted_concept_count <= 1:
        flags.append("rich_structure_low_concept_admission")
    if structural_header_count >= 20 and admitted_relationship_count <= 1:
        flags.append("rich_structure_low_relationship_admission")
    if structural_header_count >= 20 and admitted_concept_count <= 1 and admitted_relationship_count <= 1:
        flags.append("rich_structure_needs_hierarchy_review")
    return flags


def _build_folder_summary(
    *,
    repo_root: Path,
    folder_name: str,
    raw_source_dirs: set[str],
    refined_counts: dict[str, int],
    raw_markdown_counts: dict[str, int],
    sidecar_counts: dict[str, int],
    pilot_unit: Any | None,
    candidate_reason: str | None = None,
) -> dict[str, Any]:
    pilot_covered = pilot_unit is not None
    admitted_source_count = len(pilot_unit.admitted_source_paths) if pilot_unit else 0
    admitted_concept_count = len(pilot_unit.admitted_concept_paths) if pilot_unit else 0
    admitted_relationship_count = len(pilot_unit.admitted_relationship_paths) if pilot_unit else 0
    structural_header_count = _count_structural_headers(repo_root / _REFINED_ROOT, folder_name)
    guardrails = _structure_guardrails(
        structural_header_count=structural_header_count,
        admitted_concept_count=admitted_concept_count,
        admitted_relationship_count=admitted_relationship_count,
    )
    if pilot_covered:
        next_step = (
            "Already admitted inside the bounded pilot; keep generic Phase 11 expansion gated and extend only through a fresh accepted slice."
        )
        status = "pilot-covered"
    elif refined_counts.get(folder_name, 0) > 0:
        next_step = (
            "Inventory exists, but this law is not admitted in the bounded pilot. Require fresh research/audit/plan plus bounded source admission before any review run."
        )
        status = "inventory-only"
    else:
        next_step = (
            "No repo-local refined markdown inventory detected here; do not widen until source/conversion readiness is established."
        )
        status = "not-ready"
    if guardrails:
        next_step = (
            next_step
            + " Automated guardrail triggered: the document has rich section structure relative to current concept/relationship admission and should be reviewed before claiming graph coverage is sufficient."
        )
    return {
        "folder_name": folder_name,
        "law_id": folder_name.lower(),
        "candidate_reason": candidate_reason,
        "pilot_covered": pilot_covered,
        "status": status,
        "raw_source_present": folder_name in raw_source_dirs,
        "refined_markdown_count": refined_counts.get(folder_name, 0),
        "raw_markdown_count": raw_markdown_counts.get(folder_name, 0),
        "sidecar_json_count": sidecar_counts.get(folder_name, 0),
        "admitted_source_count": admitted_source_count,
        "admitted_concept_count": admitted_concept_count,
        "admitted_relationship_count": admitted_relationship_count,
        "structural_header_count": structural_header_count,
        "structure_guardrails": guardrails,
        "next_step": next_step,
    }


def _default_duplicate_report_path(repo_root: Path, scope_id: str, run_id: str) -> Path:
    return (
        repo_root
        / "006_System-Manifests"
        / "runs"
        / "datasets"
        / scope_id
        / run_id
        / "laws_duplicate_dry_run_report.json"
    )


def _pdf_duplicate_clusters(
    *,
    repo_root: Path,
    folder_names: list[str],
) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    from .scanner import _sha256_of_file

    raw_root = repo_root / _RAW_SOURCE_ROOT
    registry_digests: dict[str, str] = {}
    registry_path = repo_root / "006_System-Manifests" / "registries" / "latest_raw_file_registry.csv"
    if registry_path.exists():
        try:
            with registry_path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                for row in reader:
                    relative_path = row.get("relative_path")
                    extension = row.get("extension")
                    sha256 = row.get("sha256")
                    if not isinstance(relative_path, str) or not isinstance(sha256, str):
                        continue
                    if extension != ".pdf":
                        continue
                    parts = Path(relative_path).parts
                    if len(parts) < 2:
                        continue
                    if parts[1] not in folder_names:
                        continue
                    registry_digests[relative_path] = sha256
        except OSError:
            registry_digests = {}
    by_digest: dict[str, list[Path]] = {}
    for folder_name in folder_names:
        folder_root = raw_root / folder_name
        if not folder_root.exists():
            continue
        for path in sorted(
            path for path in folder_root.rglob("*") if path.is_file() and path.suffix.lower() == ".pdf"
        ):
            rel_raw_path = path.relative_to(raw_root.parent).as_posix()
            digest = registry_digests.get(rel_raw_path) or _sha256_of_file(path)
            by_digest.setdefault(digest, []).append(path)

    folder_flags: dict[str, list[str]] = {}
    clusters: list[dict[str, Any]] = []
    for digest, paths in sorted(by_digest.items()):
        if len(paths) < 2:
            continue
        rel_paths = [str(path.relative_to(repo_root)) for path in paths]
        folders = sorted({path.parent.name for path in paths})
        tag_union: set[str] = set()
        for rel_path in rel_paths:
            tag_union.update(_variant_semantic_tags(rel_path))
        semantic_flags: list[str] = []
        if "irr" in tag_union and "lawish" in tag_union:
            semantic_flags.append("conflicting_law_irr_filename_semantics")
        if "study_aid" in tag_union and len(tag_union) > 1:
            semantic_flags.append("study_aid_and_authoritative_variants_mixed")
        cluster = {
            "sha256": digest,
            "file_count": len(rel_paths),
            "law_folder_count": len(folders),
            "law_folders": folders,
            "raw_paths": rel_paths,
            "semantic_flags": semantic_flags,
        }
        clusters.append(cluster)
        for folder_name in folders:
            flags = folder_flags.setdefault(folder_name, [])
            flags.append(f"exact_duplicate_sha256:{digest[:12]}")
            flags.extend(semantic_flags)

    for folder_name, flags in list(folder_flags.items()):
        deduped: list[str] = []
        for flag in flags:
            if flag not in deduped:
                deduped.append(flag)
        folder_flags[folder_name] = deduped
    return clusters, folder_flags


def run_laws_duplicate_dry_run(
    *,
    tranche_manifest: str | None = None,
    report_out: str | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")
    raw_root = repo_root / _RAW_SOURCE_ROOT
    if not raw_root.exists():
        print(json.dumps({"error": f"missing laws raw root: {_relative(raw_root, repo_root)}"}, indent=2))
        return 2

    scope_id = "laws-duplicate-readiness"
    scope_folders = [path.name for path in _iter_law_dirs(raw_root)]
    tranche_manifest_path: Path | None = None
    if tranche_manifest:
        tranche_payload, tranche_manifest_path, tranche_error = _load_tranche_manifest(repo_root, tranche_manifest)
        if tranche_payload is None:
            print(json.dumps({"error": tranche_error or "failed to load tranche manifest"}, indent=2))
            return 2
        scope_id = str(tranche_payload.get("tranche_id") or scope_id)
        scope_folders = [item["folder_name"] for item in tranche_payload["candidate_law_folders"]]

    duplicate_clusters, duplicate_flags_by_folder = _pdf_duplicate_clusters(
        repo_root=repo_root,
        folder_names=scope_folders,
    )
    report_path = (
        Path(report_out).resolve()
        if report_out
        else _default_duplicate_report_path(repo_root, scope_id, run_id)
    )
    report = {
        "action": "run-laws-duplicate-dry-run",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "dry_run": True,
        "phase_11_gate": "gated",
        "scope_id": scope_id,
        "tranche_manifest_path": _relative(tranche_manifest_path, repo_root) if tranche_manifest_path else None,
        "candidate_law_folder_count": len(scope_folders),
        "candidate_law_folders": scope_folders,
        "duplicate_cluster_count": len(duplicate_clusters),
        "duplicate_law_folders": sorted(duplicate_flags_by_folder),
        "duplicate_clusters": duplicate_clusters,
    }
    write_json_report(report_path, report)
    summary = {
        "action": "run-laws-duplicate-dry-run",
        "run_id": run_id,
        "dry_run": True,
        "phase_11_gate": "gated",
        "scope_id": scope_id,
        "candidate_law_folder_count": len(scope_folders),
        "duplicate_cluster_count": len(duplicate_clusters),
        "duplicate_law_folders": sorted(duplicate_flags_by_folder),
        "report_path": _relative(report_path, repo_root),
    }
    print(json.dumps(summary, indent=2))
    return 0


def _tranche_source_to_graph_paths(repo_root: Path, tranche_id: str, run_id: str) -> dict[str, Path]:
    base = (
        repo_root
        / "006_System-Manifests"
        / "runs"
        / "datasets"
        / tranche_id
        / "source_to_graph_dry_run"
        / run_id
    )
    dataset_id = f"{tranche_id}-source-to-graph-dry-run"
    return {
        "base": base,
        "derived_manifest": base / "derived_dataset_manifest.yaml",
        "report": base / "laws_tranche_source_to_graph_dry_run_report.json",
        "dataset_graph_output_root": (
            repo_root
            / "005_Operational-Intelligence-Layer"
            / "graph"
            / "datasets"
            / dataset_id
        ),
        "dataset_run_output_root": (
            repo_root
            / "006_System-Manifests"
            / "runs"
            / "datasets"
            / dataset_id
        ),
    }


def _tranche_source_to_graph_execute_paths(repo_root: Path, tranche_id: str, run_id: str) -> dict[str, Path]:
    base = (
        repo_root
        / "006_System-Manifests"
        / "runs"
        / "datasets"
        / tranche_id
        / "source_to_graph_execute"
        / run_id
    )
    dataset_id = f"{tranche_id}-source-to-graph-execute"
    return {
        "base": base,
        "derived_manifest": base / "derived_dataset_manifest.yaml",
        "report": base / "laws_tranche_source_to_graph_execute_report.json",
        "dataset_graph_output_root": (
            repo_root
            / "005_Operational-Intelligence-Layer"
            / "graph"
            / "datasets"
            / dataset_id
        ),
        "dataset_run_output_root": (
            repo_root
            / "006_System-Manifests"
            / "runs"
            / "datasets"
            / dataset_id
        ),
    }


def _classified_raw_entry(
    *,
    path: str,
    folder_name: str,
    entry_role: str,
    authority_tier: str,
    reason: str,
    note: str,
) -> dict[str, Any]:
    return {
        "path": path,
        "folder_name": folder_name,
        "entry_role": entry_role,
        "authority_tier": authority_tier,
        "variant_family": "tranche-source-to-graph",
        "edition_or_source_note": note,
        "include_in_m1": True,
        "reason": reason,
    }


def _build_tranche_source_to_graph_manifest_payload(
    *,
    repo_root: Path,
    tranche_payload: dict[str, Any],
    run_id: str,
    dataset_id: str,
    graph_output_root_rel: str,
    run_output_root_rel: str,
) -> tuple[dict[str, Any], list[str], list[str]]:
    tranche_id = str(tranche_payload.get("tranche_id") or "laws-tranche")
    staged_entries = [
        item
        for item in tranche_payload["candidate_law_folders"]
        if item.get("source_admission_state") == "admitted"
    ]
    blocked_folders = [
        str(item.get("folder_name"))
        for item in tranche_payload["candidate_law_folders"]
        if item.get("source_admission_state") != "admitted"
    ]
    staged_folders = [str(item.get("folder_name")) for item in staged_entries]

    raw_slice_anchors: list[dict[str, Any]] = []
    canonical_sources: list[dict[str, Any]] = []
    canonical_concepts: list[dict[str, Any]] = []
    relationship_entries: list[dict[str, Any]] = []
    law_units: list[dict[str, Any]] = []
    for item in staged_entries:
        folder_name = str(item["folder_name"])
        reason = str(item.get("reason") or "tranche admitted source")
        raw_anchor_paths = [str(path) for path in item.get("raw_anchor_paths") or [] if isinstance(path, str)]
        authoritative_variant_paths = [str(path) for path in item.get("authoritative_variant_paths") or [] if isinstance(path, str)]
        excluded_variant_paths = [str(path) for path in item.get("excluded_variant_paths") or [] if isinstance(path, str)]
        refined_markdown_paths = [str(path) for path in item.get("refined_markdown_paths") or [] if isinstance(path, str)]
        admitted_source_paths = [str(path) for path in item.get("admitted_source_paths") or [] if isinstance(path, str)]
        admitted_concept_paths = [str(path) for path in item.get("admitted_concept_paths") or [] if isinstance(path, str)]
        admitted_relationship_paths = [str(path) for path in item.get("admitted_relationship_paths") or [] if isinstance(path, str)]
        verification_checks = [str(v) for v in item.get("verification_checks") or [] if isinstance(v, str)]
        scope_notes = [str(v) for v in item.get("scope_notes") or [] if isinstance(v, str)]

        classified_entries: list[dict[str, Any]] = []
        for path in authoritative_variant_paths or raw_anchor_paths:
            classified_entries.append(
                _classified_raw_entry(
                    path=path,
                    folder_name=folder_name,
                    entry_role="authoritative",
                    authority_tier="primary",
                    reason=reason,
                    note="Tranche admitted authoritative source variant for source-to-graph dry-run.",
                )
            )
        for path in excluded_variant_paths:
            classified_entries.append(
                _classified_raw_entry(
                    path=path,
                    folder_name=folder_name,
                    entry_role="reference",
                    authority_tier="adjacent",
                    reason=f"Excluded variant retained for tranche duplicate/source-admission visibility: {reason}",
                    note="Excluded tranche variant retained outside admitted source-to-graph scope.",
                )
            )

        raw_slice_anchors.append(
            {
                "folder_name": folder_name,
                "raw_root": _relative(repo_root / _RAW_SOURCE_ROOT / folder_name, repo_root),
                "entry_role": "authoritative",
                "authority_tier": "primary",
                "variant_family": "tranche-source-to-graph",
                "edition_or_source_note": "Admitted tranche source-to-graph dry-run anchor.",
                "include_in_m1": True,
                "reason": reason,
                "classified_raw_entries": classified_entries,
            }
        )
        for source_path in admitted_source_paths:
            canonical_sources.append(
                {
                    "path": source_path,
                    "folder_name": folder_name,
                    "entry_role": "authoritative",
                    "authority_tier": "primary",
                    "variant_family": "tranche-source-to-graph",
                    "edition_or_source_note": "Admitted tranche canonical source anchor for source-to-graph dry-run.",
                    "include_in_m1": True,
                    "reason": reason,
                }
            )
        for concept_path in admitted_concept_paths:
            canonical_concepts.append(
                {
                    "path": concept_path,
                    "folder_name": folder_name,
                    "entry_role": "derived",
                    "authority_tier": "derived",
                    "variant_family": f"{folder_name.lower()}-canonical-concept",
                    "edition_or_source_note": "Existing shared canonical concept selected explicitly for tranche source-to-graph dry-run staging.",
                    "include_in_m1": True,
                    "reason": "Explicit truth-bearing canonical concept input carried through from tranche admission state.",
                }
            )
        for relationship_path in admitted_relationship_paths:
            relationship_entries.append(
                {
                    "path": relationship_path,
                    "folder_name": folder_name,
                    "entry_role": "authoritative",
                    "authority_tier": "approved",
                    "variant_family": f"{folder_name.lower()}-promoted-relationship",
                    "edition_or_source_note": "Existing approved relationship record selected explicitly for tranche source-to-graph dry-run staging.",
                    "include_in_m1": True,
                    "reason": "Explicit approved relationship input carried through from tranche admission state.",
                }
            )
        law_units.append(
            {
                "law_id": folder_name.lower(),
                "folder_name": folder_name,
                "raw_anchor_paths": raw_anchor_paths or authoritative_variant_paths,
                "refined_markdown_paths": refined_markdown_paths,
                "authoritative_variant_paths": authoritative_variant_paths or raw_anchor_paths,
                "excluded_variant_paths": excluded_variant_paths,
                "admitted_source_paths": admitted_source_paths,
                "admitted_concept_paths": admitted_concept_paths,
                "admitted_relationship_paths": admitted_relationship_paths,
                "verification_checks": verification_checks,
                "scope_notes": scope_notes,
            }
        )

    relationship_dir = repo_root / "003_Canonical-Knowledge-Layer" / "shared" / "relationships"
    fallback_relationship = next(
        (path for path in sorted(relationship_dir.glob("*.md")) if path.is_file()),
        None,
    )
    if fallback_relationship is not None and staged_folders and not relationship_entries:
        relationship_entries.append(
            {
                "path": _relative(fallback_relationship, repo_root),
                "folder_name": staged_folders[0],
                "entry_role": "authoritative",
                "authority_tier": "approved",
                "variant_family": "tranche-source-to-graph",
                "edition_or_source_note": "Shared fallback relationship input required by dataset manifest validation during dry-run staging.",
                "include_in_m1": True,
                "reason": "Validation-only placeholder relationship input for admitted tranche dry-run staging.",
            }
        )

    payload = {
        "dataset_id": dataset_id,
        "dataset_kind": "laws-tranche",
        "scope_notes": [
            f"Derived from {tranche_id} after tranche source admission.",
            "Dry-run only: stage admitted tranche members without unlocking execute.",
            "Blocked tranche members remain explicit outside the staged law-unit list.",
        ],
        "raw_slice_anchors": raw_slice_anchors,
        "canonical_input_manifest": {
            "sources": canonical_sources,
            "concepts": canonical_concepts,
        },
        "relationship_input_manifest": {
            "relationships": relationship_entries,
        },
        "graph_output_root": graph_output_root_rel,
        "run_output_root": run_output_root_rel,
        "query_snapshot_path_template": f"{graph_output_root_rel}/{{run_id}}_graph_snapshot.json",
        "freshness_policy": {"mode": "exact"},
        "pilot_gate": {
            "require_manifest_validation": True,
            "source_to_graph_execute_ready": False,
            "derived_from_tranche_id": tranche_id,
            "derived_run_id": run_id,
        },
        "law_units": law_units,
    }
    return payload, staged_folders, blocked_folders


def _refined_markdown_relative_path(markdown_relative_path: Path) -> Path:
    parts = list(markdown_relative_path.parts)
    if "raw_markdown" not in parts:
        return markdown_relative_path
    parts[parts.index("raw_markdown")] = "refined_markdown"
    return Path(*parts)


def _raw_file_preparation_summary(
    *,
    repo_root: Path,
    file_path: Path,
    sample_pages: int,
) -> dict[str, Any]:
    rel_repo = file_path.relative_to(repo_root).as_posix()
    rel_raw = file_path.relative_to(repo_root / "001_Raw-Source-Layer").as_posix()
    ext = file_path.suffix.lower()
    supported = ext in SUPPORTED_DIRECT_INPUT_EXTENSIONS
    detection: dict[str, Any] | None = None
    detection_error: str | None = None
    if ext == ".pdf":
        try:
            detection = detect_pdf_type(file_path, sample_pages=sample_pages)
        except Exception as exc:  # noqa: BLE001
            detection_error = str(exc)

    markdown_rel: str | None = None
    sidecar_rel: str | None = None
    refined_rel: str | None = None
    ocr_pdf_rel: str | None = None
    markdown_exists = False
    sidecar_exists = False
    refined_exists = False
    ocr_pdf_exists = False
    if supported:
        markdown_path_rel, json_path_rel = build_conversion_relative_paths(rel_raw)
        refined_path_rel = _refined_markdown_relative_path(markdown_path_rel)
        ocr_pdf_path_rel = build_ocr_pdf_relative_path(rel_raw)
        markdown_rel = (Path("002_Raw-Conversion-Layer") / markdown_path_rel).as_posix()
        sidecar_rel = (Path("002_Raw-Conversion-Layer") / json_path_rel).as_posix()
        refined_rel = (Path("002_Raw-Conversion-Layer") / refined_path_rel).as_posix()
        ocr_pdf_rel = (Path("002_Raw-Conversion-Layer") / ocr_pdf_path_rel).as_posix()
        markdown_exists = (repo_root / markdown_rel).exists()
        sidecar_exists = (repo_root / sidecar_rel).exists()
        refined_exists = (repo_root / refined_rel).exists()
        ocr_pdf_exists = (repo_root / ocr_pdf_rel).exists()

    return {
        "raw_path": rel_repo,
        "extension": ext,
        "supported_direct_input": supported,
        "detection_result": detection.get("result") if detection else None,
        "recommended_route": detection.get("recommended_route") if detection else None,
        "detection_error": detection_error,
        "expected_raw_markdown_path": markdown_rel,
        "expected_sidecar_json_path": sidecar_rel,
        "expected_refined_markdown_path": refined_rel,
        "expected_ocr_pdf_path": ocr_pdf_rel,
        "raw_markdown_exists": markdown_exists,
        "sidecar_json_exists": sidecar_exists,
        "refined_markdown_exists": refined_exists,
        "ocr_pdf_exists": ocr_pdf_exists,
    }


def _prepare_raw_file_via_ocr(
    *,
    repo_root: Path,
    file_path: Path,
    rel_repo: str,
    rel_raw: str,
    detection: dict[str, Any] | None,
) -> dict[str, Any]:
    import ocrmypdf

    markdown_path_rel, json_path_rel = build_conversion_relative_paths(rel_raw)
    refined_path_rel = _refined_markdown_relative_path(markdown_path_rel)
    ocr_pdf_path_rel = build_ocr_pdf_relative_path(rel_raw)
    markdown_rel = (Path(CONVERSION_LAYER_NAME) / markdown_path_rel).as_posix()
    sidecar_rel = (Path(CONVERSION_LAYER_NAME) / json_path_rel).as_posix()
    refined_rel = (Path(CONVERSION_LAYER_NAME) / refined_path_rel).as_posix()
    ocr_pdf_rel = (Path(CONVERSION_LAYER_NAME) / ocr_pdf_path_rel).as_posix()
    ocr_abs = repo_root / ocr_pdf_rel

    if ocr_abs.exists() and (repo_root / markdown_rel).exists() and (repo_root / sidecar_rel).exists() and (repo_root / refined_rel).exists():
        return {
            "raw_path": rel_repo,
            "status": "prepared",
            "supported_direct_input": True,
            "detection_result": detection["result"] if detection else None,
            "recommended_route": detection["recommended_route"] if detection else None,
            "expected_raw_markdown_path": markdown_rel,
            "expected_sidecar_json_path": sidecar_rel,
            "expected_refined_markdown_path": refined_rel,
            "expected_ocr_pdf_path": ocr_pdf_rel,
            "ocr_output": "reused existing OCR/conversion/refinement outputs",
            "convert_output": "",
            "refine_output": "",
        }

    try:
        ocr_abs.parent.mkdir(parents=True, exist_ok=True)
        if ocr_abs.exists():
            ocr_abs.unlink()
        ocrmypdf.ocr(
            str(file_path),
            str(ocr_abs),
            languages=["eng"],
            deskew=True,
            skip_text=True,
            progress_bar=False,
        )
    except Exception as exc:  # noqa: BLE001
        return {
            "raw_path": rel_repo,
            "status": "ocr_failed",
            "supported_direct_input": True,
            "detection_result": detection["result"] if detection else None,
            "recommended_route": detection["recommended_route"] if detection else None,
            "expected_raw_markdown_path": markdown_rel,
            "expected_sidecar_json_path": sidecar_rel,
            "expected_refined_markdown_path": refined_rel,
            "expected_ocr_pdf_path": ocr_pdf_rel,
            "error": str(exc),
        }

    try:
        converted = convert_pdf_at_path(
            ocr_abs,
            rel_raw,
            run_command="run-laws-tranche-source-prep",
            detected_pdf_type="OCR_OUTPUT_PDF",
            processing_route="OCR_THEN_OPENDATALOADER",
            output_ocr_pdf_relative_path=ocr_pdf_rel,
        )
    except Exception as exc:  # noqa: BLE001
        return {
            "raw_path": rel_repo,
            "status": "convert_failed",
            "supported_direct_input": True,
            "detection_result": detection["result"] if detection else None,
            "recommended_route": detection["recommended_route"] if detection else None,
            "expected_raw_markdown_path": markdown_rel,
            "expected_sidecar_json_path": sidecar_rel,
            "expected_refined_markdown_path": refined_rel,
            "expected_ocr_pdf_path": ocr_pdf_rel,
            "ocr_output": f"ocrmypdf completed: {ocr_pdf_rel}",
            "error": str(exc),
        }

    refine_rc, refine_output = _capture_text_handler(
        lambda: run_refine_one(relative_markdown_path=markdown_path_rel.as_posix())
    )
    return {
        "raw_path": rel_repo,
        "status": "prepared" if refine_rc == 0 else "refine_failed",
        "supported_direct_input": True,
        "detection_result": detection["result"] if detection else None,
        "recommended_route": detection["recommended_route"] if detection else None,
        "expected_raw_markdown_path": markdown_rel,
        "expected_sidecar_json_path": sidecar_rel,
        "expected_refined_markdown_path": refined_rel,
        "expected_ocr_pdf_path": ocr_pdf_rel,
        "ocr_output": f"ocrmypdf completed: {ocr_pdf_rel}",
        "convert_output": json.dumps(
            {
                "markdown_output_relative": converted["markdown_output_relative"],
                "json_output_relative": converted["json_output_relative"],
            }
        ),
        "refine_output": refine_output.strip(),
    }


def _prepare_raw_file(
    *,
    repo_root: Path,
    file_path: Path,
    sample_pages: int,
    allow_ocr: bool = False,
) -> dict[str, Any]:
    rel_repo = file_path.relative_to(repo_root).as_posix()
    rel_raw = file_path.relative_to(repo_root / RAW_LAYER_NAME).as_posix()
    ext = file_path.suffix.lower()
    if ext not in SUPPORTED_DIRECT_INPUT_EXTENSIONS:
        return {
            "raw_path": rel_repo,
            "status": "unsupported",
            "supported_direct_input": False,
        }

    detection: dict[str, Any] | None = None
    markdown_path_rel, json_path_rel = build_conversion_relative_paths(rel_raw)
    refined_path_rel = _refined_markdown_relative_path(markdown_path_rel)
    ocr_pdf_path_rel = build_ocr_pdf_relative_path(rel_raw)
    markdown_rel = (Path(CONVERSION_LAYER_NAME) / markdown_path_rel).as_posix()
    sidecar_rel = (Path(CONVERSION_LAYER_NAME) / json_path_rel).as_posix()
    refined_rel = (Path(CONVERSION_LAYER_NAME) / refined_path_rel).as_posix()
    ocr_pdf_rel = (Path(CONVERSION_LAYER_NAME) / ocr_pdf_path_rel).as_posix()
    if ext == ".pdf":
        try:
            detection = detect_pdf_type(file_path, sample_pages=sample_pages)
        except Exception as exc:  # noqa: BLE001
            return {
                "raw_path": rel_repo,
                "status": "detection_failed",
                "error": str(exc),
                "supported_direct_input": True,
            }
        if detection["recommended_route"] != "OPENDATALOADER_DIRECT":
            if allow_ocr:
                return _prepare_raw_file_via_ocr(
                    repo_root=repo_root,
                    file_path=file_path,
                    rel_repo=rel_repo,
                    rel_raw=rel_raw,
                    detection=detection,
                )
            return {
                "raw_path": rel_repo,
                "status": "ocr_required",
                "supported_direct_input": True,
                "detection_result": detection["result"],
                "recommended_route": detection["recommended_route"],
                "expected_raw_markdown_path": markdown_rel,
                "expected_sidecar_json_path": sidecar_rel,
                "expected_refined_markdown_path": refined_rel,
                "expected_ocr_pdf_path": ocr_pdf_rel,
            }

    convert_rc, convert_output = _capture_text_handler(
        lambda: run_convert_one(relative_pdf_path=rel_raw)
    )
    if convert_rc != 0:
        return {
            "raw_path": rel_repo,
            "status": "convert_failed",
            "supported_direct_input": True,
            "detection_result": detection["result"] if detection else None,
            "recommended_route": detection["recommended_route"] if detection else None,
            "expected_raw_markdown_path": markdown_rel,
            "expected_sidecar_json_path": sidecar_rel,
            "expected_refined_markdown_path": refined_rel,
            "convert_output": convert_output.strip(),
        }

    refine_rc, refine_output = _capture_text_handler(
        lambda: run_refine_one(relative_markdown_path=markdown_path_rel.as_posix())
    )
    return {
        "raw_path": rel_repo,
        "status": "prepared" if refine_rc == 0 else "refine_failed",
        "supported_direct_input": True,
        "detection_result": detection["result"] if detection else None,
        "recommended_route": detection["recommended_route"] if detection else None,
        "expected_raw_markdown_path": markdown_rel,
        "expected_sidecar_json_path": sidecar_rel,
        "expected_refined_markdown_path": refined_rel,
        "convert_output": convert_output.strip(),
        "refine_output": refine_output.strip(),
    }


def _manifest_scoped_raw_files(
    *,
    repo_root: Path,
    folder_root: Path,
    item: dict[str, Any],
) -> list[Path]:
    if not folder_root.exists():
        return []
    all_files = sorted(path for path in folder_root.rglob("*") if path.is_file())
    requested_relpaths = [
        str(path)
        for path in [*(item.get("authoritative_variant_paths") or []), *(item.get("raw_anchor_paths") or [])]
        if isinstance(path, str)
    ]
    excluded_relpaths = {
        str(path) for path in item.get("excluded_variant_paths") or [] if isinstance(path, str)
    }
    if requested_relpaths:
        requested_abs: list[Path] = []
        for relpath in requested_relpaths:
            abs_path = (repo_root / relpath).resolve()
            if abs_path.is_file() and abs_path not in requested_abs:
                requested_abs.append(abs_path)
        return [path for path in requested_abs if _relative(path, repo_root) not in excluded_relpaths]
    return [path for path in all_files if _relative(path, repo_root) not in excluded_relpaths]


_STUDY_AID_MARKERS = ("illustrated", "slides", "reviewer", "summary", "handout", "lecture")


def _resolve_source_prep_report_path(
    *,
    repo_root: Path,
    tranche_id: str,
    source_prep_report: str | None,
) -> tuple[Path | None, str | None]:
    if source_prep_report:
        report_path = Path(source_prep_report)
        if not report_path.is_absolute():
            report_path = repo_root / report_path
        if not report_path.exists():
            return None, f"source prep report not found: {_relative(report_path, repo_root)}"
        return report_path, None

    base = repo_root / "006_System-Manifests" / "runs" / "datasets" / tranche_id
    candidates = sorted(base.glob("*/laws_tranche_source_prep_report.json"))
    if not candidates:
        return None, (
            f"no source prep execute reports found under {_relative(base, repo_root)}; "
            "run run-laws-tranche-source-prep first or pass --source-prep-report"
        )
    return candidates[-1], None


def _load_source_prep_report(
    *,
    repo_root: Path,
    tranche_id: str,
    source_prep_report: str | None,
) -> tuple[dict[str, Any] | None, Path | None, str | None]:
    report_path, path_error = _resolve_source_prep_report_path(
        repo_root=repo_root,
        tranche_id=tranche_id,
        source_prep_report=source_prep_report,
    )
    if report_path is None:
        return None, None, path_error
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, report_path, str(exc)
    if not isinstance(payload, dict):
        return None, report_path, "source prep report must be a JSON object"
    if payload.get("action") != "run-laws-tranche-source-prep":
        return None, report_path, "source prep report must come from run-laws-tranche-source-prep"
    if str(payload.get("tranche_id") or "") != tranche_id:
        return None, report_path, (
            f"source prep report tranche_id mismatch: expected {tranche_id!r}, "
            f"got {payload.get('tranche_id')!r}"
        )
    folders = payload.get("folders")
    if not isinstance(folders, list):
        return None, report_path, "source prep report requires a folders list"
    return payload, report_path, None


def _normalize_refined_markdown_path(relative_path: str) -> str:
    rel = relative_path.strip()
    prefix = "002_Raw-Conversion-Layer/"
    if rel.startswith(prefix):
        return rel[len(prefix):]
    return rel


def _candidate_source_page_plan(
    *,
    repo_root: Path,
    refined_markdown_path: str,
) -> dict[str, Any]:
    normalized_refined_markdown_path = _normalize_refined_markdown_path(refined_markdown_path)
    plan = build_plan(normalized_refined_markdown_path)
    canonical_relative_path = (
        Path("003_Canonical-Knowledge-Layer")
        / "shared"
        / "sources"
        / f"{slugify(plan['title'])}.md"
    ).as_posix()
    return {
        "refined_markdown_path": refined_markdown_path,
        "normalized_refined_markdown_path": normalized_refined_markdown_path,
        "canonical_title": plan["title"],
        "canonical_id": plan["canonical_id"],
        "canonical_prefix": plan["prefix"],
        "canonical_source_type": plan["source_type"],
        "trust_level": plan["trust"],
        "canonical_source_path": canonical_relative_path,
        "canonical_source_exists": (repo_root / canonical_relative_path).exists(),
        "aliases": list(plan["aliases"]),
        "concepts": list(plan["concepts"]),
        "relationships": list(plan["relationships"]),
    }


def _admission_status_for_folder(
    *,
    candidate_source_pages: list[dict[str, Any]],
    blocked_file_reports: list[dict[str, Any]],
    failed_file_reports: list[dict[str, Any]],
) -> str:
    if candidate_source_pages and blocked_file_reports:
        return "partial_ready_blocked"
    if candidate_source_pages and failed_file_reports:
        return "partial_ready_failed"
    if candidate_source_pages:
        return "ready_for_admission_review"
    if blocked_file_reports:
        return "blocked_pending_ocr"
    if failed_file_reports:
        return "blocked_preparation_failed"
    return "not_ready"


def _is_study_aid_variant(path_value: str | None) -> bool:
    if not isinstance(path_value, str):
        return False
    lowered = path_value.lower()
    return any(marker in lowered for marker in _STUDY_AID_MARKERS)


def _variant_semantic_tags(path_value: str | None) -> set[str]:
    if not isinstance(path_value, str):
        return set()
    lowered = path_value.lower()
    tags: set[str] = set()
    if "irr" in lowered or "implementing rules" in lowered:
        tags.add("irr")
    if any(token in lowered for token in ("decree", "act", "code", "law")):
        tags.add("lawish")
    if _is_study_aid_variant(path_value):
        tags.add("study_aid")
    return tags


def _variant_authority_score(*, raw_path: str | None, refined_markdown_path: str | None) -> int:
    joined = " ".join(part for part in (raw_path, refined_markdown_path) if isinstance(part, str)).lower()
    score = 0
    if "irr" in joined or "implementing rules" in joined:
        score += 40
    if any(token in joined for token in ("decree", "act", "code", "law")):
        score += 20
    if any(token in joined for token in ("revised", "official", "authoritative")):
        score += 5
    if _is_study_aid_variant(joined):
        score -= 100
    return score


def _raw_path_sha256(repo_root: Path, raw_path: str | None) -> str | None:
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None
    abs_path = repo_root / raw_path
    if not abs_path.exists() or not abs_path.is_file():
        return None
    try:
        from .scanner import _sha256_of_file
        return _sha256_of_file(abs_path)
    except OSError:
        return None


def _select_prepared_source_candidates(
    *,
    repo_root: Path,
    prepared_files: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    selected: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    guardrails: list[str] = []
    grouped: dict[str, list[dict[str, Any]]] = {}

    for report in prepared_files:
        raw_path = report.get("raw_path") if isinstance(report.get("raw_path"), str) else None
        refined_path = report.get("expected_refined_markdown_path") if isinstance(report.get("expected_refined_markdown_path"), str) else None
        if _is_study_aid_variant(raw_path) or _is_study_aid_variant(refined_path):
            excluded.append({**report, "excluded_reason": "study_aid_variant"})
            continue
        group_key = _raw_path_sha256(repo_root, raw_path) or f"refined::{refined_path or raw_path or len(grouped)}"
        grouped.setdefault(group_key, []).append(report)

    for group_key in sorted(grouped):
        group = grouped[group_key]
        ordered = sorted(
            group,
            key=lambda report: (
                -_variant_authority_score(
                    raw_path=report.get("raw_path") if isinstance(report.get("raw_path"), str) else None,
                    refined_markdown_path=report.get("expected_refined_markdown_path") if isinstance(report.get("expected_refined_markdown_path"), str) else None,
                ),
                str(report.get("raw_path") or report.get("expected_refined_markdown_path") or ""),
            ),
        )
        primary = ordered[0]
        primary_raw_path = primary.get("raw_path") if isinstance(primary.get("raw_path"), str) else None
        primary_refined_path = primary.get("expected_refined_markdown_path") if isinstance(primary.get("expected_refined_markdown_path"), str) else None
        semantic_tags: set[str] = set()
        for report in group:
            semantic_tags.update(_variant_semantic_tags(report.get("raw_path") if isinstance(report.get("raw_path"), str) else None))
        if len(group) > 1:
            selected_name = Path(primary_raw_path or primary_refined_path or "representative").name
            guardrails.append(
                f"duplicate raw variants collapsed to one representative for sha256 {group_key[:12]}: {selected_name}"
            )
            if "irr" in semantic_tags and "lawish" in semantic_tags:
                guardrails.append(
                    f"same-content raw variants carry conflicting law/IRR filename semantics for sha256 {group_key[:12]}; review aliases before widening execution"
                )

        if not isinstance(primary_refined_path, str) or not primary_refined_path.strip():
            excluded.append({**primary, "excluded_reason": "missing_refined_markdown_path"})
            continue

        candidate = _candidate_source_page_plan(
            repo_root=repo_root,
            refined_markdown_path=primary_refined_path,
        )
        if candidate["canonical_source_type"] == "unknown" or candidate["trust_level"] == "unknown":
            excluded.append({
                **primary,
                "excluded_reason": "requires_canonical_rule",
                "raw_sha256": None if group_key.startswith("refined::") else group_key,
            })
            guardrails.append(
                f"canonical rule missing for prepared variant {Path(primary_refined_path).name}; source admission stays blocked until the rule exists"
            )
            for alias in ordered[1:]:
                excluded.append({
                    **alias,
                    "excluded_reason": "duplicate_sha256_alias_of_unadmitted_variant",
                    "selected_representative_raw_path": primary_raw_path,
                    "raw_sha256": None if group_key.startswith("refined::") else group_key,
                })
            continue

        candidate["raw_path"] = primary_raw_path
        candidate["raw_sha256"] = None if group_key.startswith("refined::") else group_key
        candidate["selected_from_duplicate_group_size"] = len(group)
        candidate["excluded_duplicate_raw_paths"] = [
            alias.get("raw_path")
            for alias in ordered[1:]
            if isinstance(alias.get("raw_path"), str)
        ]
        candidate["selection_reason"] = (
            "selected authoritative representative from duplicate raw-variant cluster"
            if len(group) > 1
            else "selected prepared authoritative candidate"
        )
        selected.append(candidate)

        for alias in ordered[1:]:
            excluded.append({
                **alias,
                "excluded_reason": "duplicate_sha256_alias",
                "selected_representative_raw_path": primary_raw_path,
                "raw_sha256": None if group_key.startswith("refined::") else group_key,
            })

    return selected, excluded, sorted(set(guardrails))


def _next_step_for_admission_status(status: str) -> str:
    if status == "ready_for_admission_review":
        return (
            "Admit the selected canonical source pages now, keep excluded variants explicit, and only then revisit tranche source-to-graph execution."
        )
    if status == "partial_ready_blocked":
        return (
            "Admit only the selected prepared source pages now, keep the OCR-blocked files explicit, and do not treat this law family as uniformly ready yet."
        )
    if status == "partial_ready_failed":
        return (
            "Review the selected source pages separately, but fix failed preparation outputs before claiming truthful admission coverage for this law family."
        )
    if status == "blocked_pending_ocr":
        return "Keep this law family blocked until OCR-first preparation produces refined outputs for admission review."
    if status == "blocked_preparation_failed":
        return "Fix preparation failures before building or admitting canonical source pages for this law family."
    return "No admissible canonical source pages are ready yet; fix duplicate/rule/quality blockers before widening execution."


def _summarize_source_admission_folder(
    *,
    repo_root: Path,
    item: dict[str, str],
    source_prep_folder: dict[str, Any],
) -> dict[str, Any]:
    file_reports = source_prep_folder.get("file_reports")
    if not isinstance(file_reports, list):
        file_reports = []
    prepared_files = [
        report for report in file_reports
        if isinstance(report, dict) and report.get("status") == "prepared"
    ]
    blocked_files = [
        report for report in file_reports
        if isinstance(report, dict) and report.get("status") == "ocr_required"
    ]
    failed_files = [
        report for report in file_reports
        if isinstance(report, dict) and report.get("status") in {"ocr_failed", "convert_failed", "refine_failed", "detection_failed"}
    ]
    explicit_authoritative_paths = {
        str(path) for path in item.get("authoritative_variant_paths") or [] if isinstance(path, str)
    }
    explicit_raw_anchor_paths = {
        str(path) for path in item.get("raw_anchor_paths") or [] if isinstance(path, str)
    }
    explicit_excluded_paths = {
        str(path) for path in item.get("excluded_variant_paths") or [] if isinstance(path, str)
    }

    requested_paths = explicit_authoritative_paths or explicit_raw_anchor_paths
    selected_prepared_files: list[dict[str, Any]] = []
    pre_excluded_files: list[dict[str, Any]] = []
    for report in prepared_files:
        raw_path = str(report.get("raw_path") or "")
        if raw_path in explicit_excluded_paths:
            pre_excluded_files.append({**report, "excluded_reason": "manifest_excluded_variant"})
            continue
        if requested_paths and raw_path not in requested_paths:
            pre_excluded_files.append({**report, "excluded_reason": "not_in_authoritative_variant_set"})
            continue
        selected_prepared_files.append(report)
    candidate_source_pages, excluded_prepared_file_reports, admission_guardrails = _select_prepared_source_candidates(
        repo_root=repo_root,
        prepared_files=selected_prepared_files,
    )
    excluded_prepared_file_reports = [*pre_excluded_files, *excluded_prepared_file_reports]
    status = _admission_status_for_folder(
        candidate_source_pages=candidate_source_pages,
        blocked_file_reports=blocked_files,
        failed_file_reports=failed_files,
    )
    return {
        "folder_name": item["folder_name"],
        "candidate_reason": item.get("reason"),
        "status": status,
        "raw_file_count": int(source_prep_folder.get("raw_file_count") or 0),
        "prepared_count": len(prepared_files),
        "ocr_required_count": len(blocked_files),
        "failed_count": len(failed_files),
        "candidate_source_page_count": len(candidate_source_pages),
        "candidate_source_pages": candidate_source_pages,
        "excluded_prepared_count": len(excluded_prepared_file_reports),
        "excluded_prepared_file_reports": excluded_prepared_file_reports,
        "blocked_file_reports": blocked_files,
        "failed_file_reports": failed_files,
        "source_prep_report_summary": {
            "prepared_count": int(source_prep_folder.get("prepared_count") or 0),
            "ocr_required_count": int(source_prep_folder.get("ocr_required_count") or 0),
            "failed_count": int(source_prep_folder.get("failed_count") or 0),
        },
        "admission_guardrails": admission_guardrails,
        "next_step": _next_step_for_admission_status(status),
    }


def _ready_mixed_blocked_lists(folder_reports: list[dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    ready: list[str] = []
    mixed: list[str] = []
    blocked: list[str] = []
    for folder in folder_reports:
        name = str(folder.get("folder_name") or "")
        status = str(folder.get("status") or "")
        if status == "ready_for_admission_review":
            ready.append(name)
        elif status in {"partial_ready_blocked", "partial_ready_failed"}:
            mixed.append(name)
        else:
            blocked.append(name)
    return ready, mixed, blocked


def _source_to_graph_blockers(folder_reports: list[dict[str, Any]], *, execute: bool) -> list[str]:
    blockers = [
        (
            "tranche source-to-graph execute remains gated until source admission is explicitly executed for ready tranche members"
            if execute
            else "tranche source-to-graph execute remains gated until source admission is explicitly completed for ready tranche members"
        )
    ]
    for folder in folder_reports:
        folder_name = str(folder.get("folder_name") or "")
        status = str(folder.get("status") or "")
        if status in {"partial_ready_blocked", "blocked_pending_ocr"}:
            blockers.append(f"{folder_name} remains blocked pending OCR-first processing")
        if status in {"partial_ready_failed", "blocked_preparation_failed"}:
            blockers.append(f"{folder_name} has failed source-preparation files")
        blockers.extend(str(item) for item in folder.get("admission_guardrails") or [])
    return list(dict.fromkeys(blockers))


def _executed_source_admission_state(folder_report: dict[str, Any]) -> str:
    admitted_count = len(folder_report.get("admitted_source_paths") or [])
    blocked_count = len(folder_report.get("blocked_file_reports") or [])
    failed_count = len(folder_report.get("failed_file_reports") or [])
    if admitted_count and blocked_count:
        return "admitted_subset_blocked"
    if admitted_count and failed_count:
        return "admitted_subset_failed"
    if admitted_count:
        return "admitted"
    if blocked_count:
        return "blocked_pending_ocr"
    if failed_count:
        return "blocked_preparation_failed"
    return "not_admitted"


def _merge_unique_strings(existing: Any, additions: list[str]) -> list[str]:
    merged: list[str] = []
    for value in existing if isinstance(existing, list) else []:
        if isinstance(value, str) and value not in merged:
            merged.append(value)
    for value in additions:
        if isinstance(value, str) and value and value not in merged:
            merged.append(value)
    return merged


def _tranche_variant_visibility(
    *,
    tranche_payload: dict[str, Any],
    staged_law_folders: list[str],
    duplicate_flags_by_folder: dict[str, list[str]],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    staged = set(staged_law_folders)
    visibility_rows: list[dict[str, Any]] = []
    raw_alias_law_folders: list[str] = []
    guardrail_law_folders: list[str] = []

    for item in tranche_payload.get("candidate_law_folders") or []:
        if not isinstance(item, dict):
            continue
        folder_name = str(item.get("folder_name") or "")
        authoritative_variant_paths = [
            str(path) for path in item.get("authoritative_variant_paths") or [] if isinstance(path, str)
        ]
        excluded_variant_paths = [
            str(path) for path in item.get("excluded_variant_paths") or [] if isinstance(path, str)
        ]
        blocked_raw_anchor_paths = [
            str(path) for path in item.get("blocked_raw_anchor_paths") or [] if isinstance(path, str)
        ]
        source_admission_guardrails = [
            str(flag) for flag in item.get("source_admission_guardrails") or [] if isinstance(flag, str)
        ]
        duplicate_guardrails = [
            str(flag) for flag in duplicate_flags_by_folder.get(folder_name) or [] if isinstance(flag, str)
        ]
        if excluded_variant_paths:
            raw_alias_law_folders.append(folder_name)
        if source_admission_guardrails or duplicate_guardrails:
            guardrail_law_folders.append(folder_name)
        visibility_rows.append(
            {
                "folder_name": folder_name,
                "source_admission_state": str(item.get("source_admission_state") or ""),
                "staged_for_source_to_graph": folder_name in staged,
                "authoritative_variant_count": len(authoritative_variant_paths),
                "authoritative_variant_paths": authoritative_variant_paths,
                "excluded_variant_count": len(excluded_variant_paths),
                "excluded_variant_paths": excluded_variant_paths,
                "blocked_raw_anchor_count": len(blocked_raw_anchor_paths),
                "blocked_raw_anchor_paths": blocked_raw_anchor_paths,
                "source_admission_guardrails": source_admission_guardrails,
                "duplicate_guardrails": duplicate_guardrails,
            }
        )

    return visibility_rows, raw_alias_law_folders, guardrail_law_folders


def _write_source_admission_back_to_manifest(
    *,
    manifest_path: Path,
    report_path: Path,
    run_id: str,
    folder_reports: list[dict[str, Any]],
) -> None:
    payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError("tranche manifest must remain a mapping")
    folders = payload.get("candidate_law_folders")
    if not isinstance(folders, list):
        raise ValueError("tranche manifest requires candidate_law_folders list")

    by_folder = {str(folder.get("folder_name") or ""): folder for folder in folder_reports}
    report_relative = _relative(report_path, manifest_path.parent.parent.parent.resolve())

    for entry in folders:
        if not isinstance(entry, dict):
            continue
        folder_name = str(entry.get("folder_name") or "")
        report = by_folder.get(folder_name)
        if report is None:
            continue

        admitted_source_paths = list(report.get("admitted_source_paths") or [])
        admitted_pages = list(report.get("admitted_source_pages") or [])
        admitted_authoritative_variant_paths = [
            str(page["raw_path"])
            for page in admitted_pages
            if isinstance(page, dict) and isinstance(page.get("raw_path"), str)
        ]
        refined_markdown_paths = [
            str(page["refined_markdown_path"])
            for page in admitted_pages
            if isinstance(page, dict) and isinstance(page.get("refined_markdown_path"), str)
        ]
        excluded_variant_paths = [
            str(item["raw_path"])
            for item in report.get("excluded_prepared_file_reports") or []
            if isinstance(item, dict) and isinstance(item.get("raw_path"), str)
        ]
        authoritative_variant_paths = (
            admitted_authoritative_variant_paths
            if admitted_authoritative_variant_paths
            else [str(path) for path in entry.get("authoritative_variant_paths") or [] if isinstance(path, str)]
        )
        raw_anchor_paths = (
            admitted_authoritative_variant_paths
            if admitted_authoritative_variant_paths
            else [str(path) for path in entry.get("raw_anchor_paths") or [] if isinstance(path, str)]
        )
        if excluded_variant_paths:
            excluded_variant_paths = _merge_unique_strings(entry.get("excluded_variant_paths"), excluded_variant_paths)
        else:
            excluded_variant_paths = [str(path) for path in entry.get("excluded_variant_paths") or [] if isinstance(path, str)]
        blocked_raw_anchor_paths = [
            str(item["raw_path"])
            for item in report.get("blocked_file_reports") or []
            if isinstance(item, dict) and isinstance(item.get("raw_path"), str)
        ]

        entry["source_admission_state"] = report.get("executed_source_admission_state")
        entry["source_admission_report_path"] = report_relative
        entry["source_admission_run_id"] = run_id
        entry["authoritative_variant_paths"] = authoritative_variant_paths
        entry["raw_anchor_paths"] = raw_anchor_paths
        entry["refined_markdown_paths"] = refined_markdown_paths
        entry["admitted_source_paths"] = admitted_source_paths
        entry["excluded_variant_paths"] = excluded_variant_paths
        if blocked_raw_anchor_paths:
            entry["blocked_raw_anchor_paths"] = blocked_raw_anchor_paths
        else:
            entry.pop("blocked_raw_anchor_paths", None)
        entry["source_admission_guardrails"] = list(report.get("admission_guardrails") or [])
        entry["verification_checks"] = _merge_unique_strings(
            entry.get("verification_checks"),
            [
                *(
                    ["source admission executed for the selected authoritative prepared variants"]
                    if admitted_source_paths
                    else []
                ),
                *(
                    ["duplicate or study-aid raw variants remain explicit and excluded from canonical admission"]
                    if excluded_variant_paths
                    else []
                ),
                *(
                    ["OCR-blocked raw variants remain explicit and unadmitted"]
                    if blocked_raw_anchor_paths
                    else []
                ),
            ],
        )
        entry["scope_notes"] = _merge_unique_strings(
            entry.get("scope_notes"),
            [
                *(
                    ["Source admission is intentionally conservative and admits only selected authoritative prepared variants."]
                    if admitted_source_paths
                    else []
                ),
                *[str(note) for note in report.get("admission_guardrails") or []],
            ],
        )

    ready_law_folders, mixed_law_folders, blocked_law_folders = _ready_mixed_blocked_lists(folder_reports)
    payload["source_admission"] = {
        "last_run_id": run_id,
        "last_report_path": report_relative,
        "admitted_ready_law_folders": ready_law_folders,
        "mixed_readiness_law_folders": mixed_law_folders,
        "blocked_law_folders": blocked_law_folders,
    }

    manifest_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def run_all_laws_dry_run(
    *,
    pilot_manifest: str = "config/datasets/laws-core-bundle-m1.yaml",
    review_model: str | None = None,
    review_model_preset: str | None = None,
    report_out: str | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")
    preset = resolve_review_preset(review_model_preset)
    effective_model = review_model or (
        preset.get("model") if isinstance(preset, dict) else None
    ) or get_ollama_default_model()
    effective_parallelism = (
        int(preset.get("parallelism"))
        if isinstance(preset, dict) and preset.get("parallelism") is not None
        else get_ollama_default_parallelism()
    )

    refined_counts = _count_child_files(repo_root / _REFINED_ROOT, ".md")
    raw_markdown_counts = _count_child_files(repo_root / _RAW_MARKDOWN_ROOT, ".md")
    sidecar_counts = _count_child_files(repo_root / _SIDECAR_ROOT, ".json")
    raw_source_dirs = {path.name for path in _iter_law_dirs(repo_root / _RAW_SOURCE_ROOT)}

    manifest, manifest_path, manifest_error = _load_pilot_manifest(repo_root, pilot_manifest)
    pilot_units_by_folder: dict[str, Any] = {}
    if manifest is not None:
        pilot_units_by_folder = {unit.folder_name: unit for unit in manifest.law_units}

    all_law_names = sorted(
        set(refined_counts)
        | set(raw_markdown_counts)
        | set(sidecar_counts)
        | raw_source_dirs
        | set(pilot_units_by_folder)
    )
    duplicate_clusters, duplicate_flags_by_folder = _pdf_duplicate_clusters(
        repo_root=repo_root,
        folder_names=all_law_names,
    )

    limitations: list[str] = []
    raw_source_root = repo_root / _RAW_SOURCE_ROOT
    if not raw_source_root.exists():
        limitations.append(
            "001_Raw-Source-Layer/001-Laws is absent in this worktree, so raw-PDF corpus counts cannot be re-verified here."
        )
    if manifest_error:
        limitations.append(
            f"Pilot manifest { _relative(manifest_path, repo_root) } could not be parsed for readiness comparison: {manifest_error}"
        )

    laws: list[dict[str, Any]] = []
    pilot_covered_count = 0
    inventory_only_count = 0
    for folder_name in all_law_names:
        pilot_unit = pilot_units_by_folder.get(folder_name)
        if pilot_unit is not None:
            pilot_covered_count += 1
        else:
            inventory_only_count += 1
        laws.append(
            _build_folder_summary(
                repo_root=repo_root,
                folder_name=folder_name,
                raw_source_dirs=raw_source_dirs,
                refined_counts=refined_counts,
                raw_markdown_counts=raw_markdown_counts,
                sidecar_counts=sidecar_counts,
                pilot_unit=pilot_unit,
            )
        )
        if duplicate_flags_by_folder.get(folder_name):
            laws[-1]["duplicate_guardrails"] = duplicate_flags_by_folder[folder_name]

    report_path = Path(report_out).resolve() if report_out else _default_report_path(repo_root, run_id)
    guardrail_law_folders = [item["folder_name"] for item in laws if item["structure_guardrails"]]
    duplicate_law_folders = sorted(duplicate_flags_by_folder)
    report = {
        "action": "run-laws-all-dry-run",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "dry_run": True,
        "phase_11_generic_expansion_gated": True,
        "phase_11_gate": "gated",
        "review_model": effective_model,
        "review_model_preset": review_model_preset,
        "review_runtime": {
            "model": effective_model,
            "parallelism": effective_parallelism,
            "preset": preset,
        },
        "pilot_manifest_path": _relative(manifest_path, repo_root),
        "pilot_manifest_present": manifest is not None,
        "pilot_manifest_law_count": len(pilot_units_by_folder),
        "pilot_manifest_dataset_id": manifest.dataset_id if manifest is not None else None,
        "inventory_roots": {
            "raw_source_root": _relative(raw_source_root, repo_root),
            "refined_markdown_root": _relative(repo_root / _REFINED_ROOT, repo_root),
            "raw_markdown_root": _relative(repo_root / _RAW_MARKDOWN_ROOT, repo_root),
            "sidecar_json_root": _relative(repo_root / _SIDECAR_ROOT, repo_root),
        },
        "inventory_summary": {
            "discovered_law_folder_count": len(all_law_names),
            "pilot_covered_law_count": pilot_covered_count,
            "inventory_only_law_count": inventory_only_count,
            "refined_markdown_total": sum(refined_counts.values()),
            "raw_markdown_total": sum(raw_markdown_counts.values()),
            "sidecar_json_total": sum(sidecar_counts.values()),
            "raw_source_folder_count": len(raw_source_dirs),
        },
        "structure_guardrail_law_folders": guardrail_law_folders,
        "duplicate_cluster_count": len(duplicate_clusters),
        "duplicate_law_folders": duplicate_law_folders,
        "duplicate_clusters": duplicate_clusters,
        "limitations": limitations,
        "laws": laws,
    }
    write_json_report(report_path, report)

    summary = {
        "action": "run-laws-all-dry-run",
        "run_id": run_id,
        "dry_run": True,
        "phase_11_generic_expansion_gated": True,
        "phase_11_gate": "gated",
        "review_model": effective_model,
        "review_model_preset": review_model_preset,
        "review_runtime": {
            "model": effective_model,
            "parallelism": effective_parallelism,
            "preset": preset,
        },
        "pilot_manifest_path": _relative(manifest_path, repo_root),
        "pilot_manifest_law_count": len(pilot_units_by_folder),
        "bounded_manifest_law_unit_count": len(pilot_units_by_folder),
        "pilot_covered_law_count": pilot_covered_count,
        "inventory_only_law_count": inventory_only_count,
        "discovered_law_folder_count": len(all_law_names),
        "raw_law_folder_count": len(raw_source_dirs),
        "raw_pdf_count": sum(
            1 for path in (repo_root / _RAW_SOURCE_ROOT).rglob("*.pdf")
        ) if (repo_root / _RAW_SOURCE_ROOT).exists() else 0,
        "refined_markdown_count": sum(refined_counts.values()),
        "coverage_gap_law_units": inventory_only_count,
        "structure_guardrail_law_folders": guardrail_law_folders,
        "duplicate_cluster_count": len(duplicate_clusters),
        "duplicate_law_folders": duplicate_law_folders,
        "limitations": limitations,
        "report_path": _relative(report_path, repo_root),
    }
    print(json.dumps(summary, indent=2))
    return 0


def run_laws_tranche_dry_run(
    *,
    tranche_manifest: str,
    pilot_manifest: str = "config/datasets/laws-core-bundle-m1.yaml",
    review_model: str | None = None,
    review_model_preset: str | None = None,
    report_out: str | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    tranche_payload, tranche_manifest_path, tranche_error = _load_tranche_manifest(repo_root, tranche_manifest)
    if tranche_payload is None:
        print(json.dumps({"error": tranche_error or "failed to load tranche manifest"}, indent=2))
        return 2

    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")
    tranche_id = str(tranche_payload.get("tranche_id") or "laws-tranche")
    preset = resolve_review_preset(review_model_preset)
    effective_model = review_model or (
        preset.get("model") if isinstance(preset, dict) else None
    ) or get_ollama_default_model()
    effective_parallelism = (
        int(preset.get("parallelism"))
        if isinstance(preset, dict) and preset.get("parallelism") is not None
        else get_ollama_default_parallelism()
    )

    refined_counts = _count_child_files(repo_root / _REFINED_ROOT, ".md")
    raw_markdown_counts = _count_child_files(repo_root / _RAW_MARKDOWN_ROOT, ".md")
    sidecar_counts = _count_child_files(repo_root / _SIDECAR_ROOT, ".json")
    raw_source_dirs = {path.name for path in _iter_law_dirs(repo_root / _RAW_SOURCE_ROOT)}

    manifest, manifest_path, manifest_error = _load_pilot_manifest(repo_root, pilot_manifest)
    pilot_units_by_folder: dict[str, Any] = {}
    if manifest is not None:
        pilot_units_by_folder = {unit.folder_name: unit for unit in manifest.law_units}

    requested = tranche_payload["candidate_law_folders"]
    requested_names = [item["folder_name"] for item in requested]
    duplicate_clusters, duplicate_flags_by_folder = _pdf_duplicate_clusters(
        repo_root=repo_root,
        folder_names=requested_names,
    )
    laws: list[dict[str, Any]] = []
    pilot_covered_count = 0
    inventory_only_count = 0
    missing_raw_source_count = 0
    for item in requested:
        folder_name = item["folder_name"]
        pilot_unit = pilot_units_by_folder.get(folder_name)
        if pilot_unit is not None:
            pilot_covered_count += 1
        else:
            inventory_only_count += 1
        if folder_name not in raw_source_dirs:
            missing_raw_source_count += 1
        laws.append(
            _build_folder_summary(
                repo_root=repo_root,
                folder_name=folder_name,
                raw_source_dirs=raw_source_dirs,
                refined_counts=refined_counts,
                raw_markdown_counts=raw_markdown_counts,
                sidecar_counts=sidecar_counts,
                pilot_unit=pilot_unit,
                candidate_reason=item.get("reason"),
            )
        )
        if duplicate_flags_by_folder.get(folder_name):
            laws[-1]["duplicate_guardrails"] = duplicate_flags_by_folder[folder_name]

    limitations: list[str] = []
    if manifest_error:
        limitations.append(
            f"Pilot manifest { _relative(manifest_path, repo_root) } could not be parsed for tranche comparison: {manifest_error}"
        )
    guardrail_law_folders = [item["folder_name"] for item in laws if item["structure_guardrails"]]
    duplicate_law_folders = sorted(duplicate_flags_by_folder)
    report_path = Path(report_out).resolve() if report_out else _default_tranche_report_path(repo_root, tranche_id, run_id)
    report = {
        "action": "run-laws-tranche-dry-run",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "dry_run": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "tranche_manifest_path": _relative(tranche_manifest_path, repo_root),
        "review_model": effective_model,
        "review_model_preset": review_model_preset,
        "review_runtime": {
            "model": effective_model,
            "parallelism": effective_parallelism,
            "preset": preset,
        },
        "pilot_manifest_path": _relative(manifest_path, repo_root),
        "pilot_manifest_law_count": len(pilot_units_by_folder),
        "candidate_law_folder_count": len(requested_names),
        "candidate_law_folders": requested_names,
        "pilot_covered_law_count": pilot_covered_count,
        "inventory_only_law_count": inventory_only_count,
        "missing_raw_source_count": missing_raw_source_count,
        "structure_guardrail_law_folders": guardrail_law_folders,
        "duplicate_cluster_count": len(duplicate_clusters),
        "duplicate_law_folders": duplicate_law_folders,
        "duplicate_clusters": duplicate_clusters,
        "laws": laws,
        "limitations": limitations,
    }
    write_json_report(report_path, report)

    summary = {
        "action": "run-laws-tranche-dry-run",
        "run_id": run_id,
        "dry_run": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "review_model": effective_model,
        "review_model_preset": review_model_preset,
        "review_runtime": {
            "model": effective_model,
            "parallelism": effective_parallelism,
            "preset": preset,
        },
        "candidate_law_folder_count": len(requested_names),
        "candidate_law_folders": requested_names,
        "pilot_covered_law_count": pilot_covered_count,
        "inventory_only_law_count": inventory_only_count,
        "missing_raw_source_count": missing_raw_source_count,
        "structure_guardrail_law_folders": guardrail_law_folders,
        "duplicate_cluster_count": len(duplicate_clusters),
        "duplicate_law_folders": duplicate_law_folders,
        "report_path": _relative(report_path, repo_root),
    }
    print(json.dumps(summary, indent=2))
    return 0


def run_laws_tranche_source_prep_dry_run(
    *,
    tranche_manifest: str,
    sample_pages: int = 5,
    report_out: str | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    tranche_payload, tranche_manifest_path, tranche_error = _load_tranche_manifest(repo_root, tranche_manifest)
    if tranche_payload is None:
        print(json.dumps({"error": tranche_error or "failed to load tranche manifest"}, indent=2))
        return 2

    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")
    tranche_id = str(tranche_payload.get("tranche_id") or "laws-tranche")
    raw_root = repo_root / _RAW_SOURCE_ROOT
    if not raw_root.exists():
        print(json.dumps({"error": f"missing laws raw root: {raw_root.relative_to(repo_root)}"}, indent=2))
        return 2

    folders_report: list[dict[str, Any]] = []
    for item in tranche_payload["candidate_law_folders"]:
        folder_name = item["folder_name"]
        folder_root = raw_root / folder_name
        files = _manifest_scoped_raw_files(repo_root=repo_root, folder_root=folder_root, item=item)
        file_reports = [
            _raw_file_preparation_summary(
                repo_root=repo_root,
                file_path=file_path,
                sample_pages=sample_pages,
            )
            for file_path in files
        ]
        folders_report.append(
            {
                "folder_name": folder_name,
                "candidate_reason": item.get("reason"),
                "raw_root_present": folder_root.exists(),
                "raw_file_count": len(files),
                "supported_direct_input_count": sum(1 for report in file_reports if report["supported_direct_input"]),
                "refined_markdown_ready_count": sum(1 for report in file_reports if report["refined_markdown_exists"]),
                "file_reports": file_reports,
            }
        )

    report_path = Path(report_out).resolve() if report_out else _default_source_prep_report_path(repo_root, tranche_id, run_id)
    report = {
        "action": "run-laws-tranche-source-prep-dry-run",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "dry_run": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "tranche_manifest_path": _relative(tranche_manifest_path, repo_root),
        "sample_pages": sample_pages,
        "folders": folders_report,
    }
    write_json_report(report_path, report)
    summary = {
        "action": "run-laws-tranche-source-prep-dry-run",
        "run_id": run_id,
        "dry_run": True,
        "phase_11_gate": "gated",
        "tranche_id": tranche_id,
        "candidate_law_folder_count": len(folders_report),
        "raw_file_count": sum(folder["raw_file_count"] for folder in folders_report),
        "supported_direct_input_count": sum(folder["supported_direct_input_count"] for folder in folders_report),
        "refined_markdown_ready_count": sum(folder["refined_markdown_ready_count"] for folder in folders_report),
        "report_path": _relative(report_path, repo_root),
    }
    print(json.dumps(summary, indent=2))
    return 0


def run_laws_tranche_source_prep(
    *,
    tranche_manifest: str,
    sample_pages: int = 5,
    allow_ocr: bool = False,
    report_out: str | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    tranche_payload, tranche_manifest_path, tranche_error = _load_tranche_manifest(repo_root, tranche_manifest)
    if tranche_payload is None:
        print(json.dumps({"error": tranche_error or "failed to load tranche manifest"}, indent=2))
        return 2

    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")
    tranche_id = str(tranche_payload.get("tranche_id") or "laws-tranche")
    raw_root = repo_root / _RAW_SOURCE_ROOT
    if not raw_root.exists():
        print(json.dumps({"error": f"missing laws raw root: {raw_root.relative_to(repo_root)}"}, indent=2))
        return 2

    folders_report: list[dict[str, Any]] = []
    prepared_count = 0
    ocr_required_count = 0
    failed_count = 0
    for item in tranche_payload["candidate_law_folders"]:
        folder_name = item["folder_name"]
        folder_root = raw_root / folder_name
        files = _manifest_scoped_raw_files(repo_root=repo_root, folder_root=folder_root, item=item)
        file_reports = [
            _prepare_raw_file(
                repo_root=repo_root,
                file_path=file_path,
                sample_pages=sample_pages,
                allow_ocr=allow_ocr,
            )
            for file_path in files
        ]
        prepared_count += sum(1 for report in file_reports if report["status"] == "prepared")
        ocr_required_count += sum(1 for report in file_reports if report["status"] == "ocr_required")
        failed_count += sum(1 for report in file_reports if report["status"] in {"ocr_failed", "convert_failed", "refine_failed", "detection_failed"})
        folders_report.append(
            {
                "folder_name": folder_name,
                "candidate_reason": item.get("reason"),
                "raw_root_present": folder_root.exists(),
                "raw_file_count": len(files),
                "supported_direct_input_count": sum(1 for report in file_reports if report["supported_direct_input"]),
                "prepared_count": sum(1 for report in file_reports if report["status"] == "prepared"),
                "ocr_required_count": sum(1 for report in file_reports if report["status"] == "ocr_required"),
                "failed_count": sum(1 for report in file_reports if report["status"] in {"ocr_failed", "convert_failed", "refine_failed", "detection_failed"}),
                "file_reports": file_reports,
            }
        )

    report_path = Path(report_out).resolve() if report_out else _default_source_prep_execute_report_path(repo_root, tranche_id, run_id)
    report = {
        "action": "run-laws-tranche-source-prep",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "execute": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "tranche_manifest_path": _relative(tranche_manifest_path, repo_root),
        "sample_pages": sample_pages,
        "allow_ocr": allow_ocr,
        "prepared_count": prepared_count,
        "ocr_required_count": ocr_required_count,
        "failed_count": failed_count,
        "folders": folders_report,
    }
    write_json_report(report_path, report)
    summary = {
        "action": "run-laws-tranche-source-prep",
        "run_id": run_id,
        "execute": True,
        "phase_11_gate": "gated",
        "tranche_id": tranche_id,
        "allow_ocr": allow_ocr,
        "candidate_law_folder_count": len(folders_report),
        "raw_file_count": sum(folder["raw_file_count"] for folder in folders_report),
        "supported_direct_input_count": sum(folder["supported_direct_input_count"] for folder in folders_report),
        "prepared_count": prepared_count,
        "ocr_required_count": ocr_required_count,
        "failed_count": failed_count,
        "report_path": _relative(report_path, repo_root),
    }
    print(json.dumps(summary, indent=2))
    return 0 if failed_count == 0 else 1


def run_laws_tranche_source_admission_dry_run(
    *,
    tranche_manifest: str,
    source_prep_report: str | None = None,
    report_out: str | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    tranche_payload, tranche_manifest_path, tranche_error = _load_tranche_manifest(repo_root, tranche_manifest)
    if tranche_payload is None:
        print(json.dumps({"error": tranche_error or "failed to load tranche manifest"}, indent=2))
        return 2

    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")
    tranche_id = str(tranche_payload.get("tranche_id") or "laws-tranche")
    source_prep_payload, source_prep_report_path, source_prep_error = _load_source_prep_report(
        repo_root=repo_root,
        tranche_id=tranche_id,
        source_prep_report=source_prep_report,
    )
    if source_prep_payload is None or source_prep_report_path is None:
        print(json.dumps({"error": source_prep_error or "failed to load source prep report"}, indent=2))
        return 2

    folders_by_name: dict[str, dict[str, Any]] = {}
    for folder in source_prep_payload.get("folders", []):
        if isinstance(folder, dict):
            folders_by_name[str(folder.get("folder_name") or "")] = folder

    folder_reports = [
        _summarize_source_admission_folder(
            repo_root=repo_root,
            item=item,
            source_prep_folder=folders_by_name.get(item["folder_name"]) or {},
        )
        for item in tranche_payload["candidate_law_folders"]
    ]
    ready_law_folders, mixed_law_folders, blocked_law_folders = _ready_mixed_blocked_lists(folder_reports)
    blockers = _source_to_graph_blockers(folder_reports, execute=False)

    report_path = Path(report_out).resolve() if report_out else _default_source_admission_report_path(repo_root, tranche_id, run_id)
    report = {
        "action": "run-laws-tranche-source-admission-dry-run",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "dry_run": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "tranche_manifest_path": _relative(tranche_manifest_path, repo_root),
        "source_prep_report_path": _relative(source_prep_report_path, repo_root),
        "source_prep_run_id": source_prep_payload.get("run_id"),
        "admission_review_ready_law_folders": ready_law_folders,
        "mixed_readiness_law_folders": mixed_law_folders,
        "blocked_law_folders": blocked_law_folders,
        "candidate_source_page_count": sum(folder["candidate_source_page_count"] for folder in folder_reports),
        "excluded_prepared_count": sum(int(folder.get("excluded_prepared_count") or 0) for folder in folder_reports),
        "source_to_graph_execute_ready": False,
        "source_to_graph_execute_blockers": blockers,
        "laws": folder_reports,
    }
    write_json_report(report_path, report)

    summary = {
        "action": "run-laws-tranche-source-admission-dry-run",
        "run_id": run_id,
        "dry_run": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "admission_review_ready_law_folders": ready_law_folders,
        "mixed_readiness_law_folders": mixed_law_folders,
        "blocked_law_folders": blocked_law_folders,
        "candidate_source_page_count": sum(folder["candidate_source_page_count"] for folder in folder_reports),
        "excluded_prepared_count": sum(int(folder.get("excluded_prepared_count") or 0) for folder in folder_reports),
        "source_to_graph_execute_ready": False,
        "source_prep_report_path": _relative(source_prep_report_path, repo_root),
        "report_path": _relative(report_path, repo_root),
    }
    print(json.dumps(summary, indent=2))
    return 0


def run_laws_tranche_source_admission(
    *,
    tranche_manifest: str,
    source_prep_report: str | None = None,
    report_out: str | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    tranche_payload, tranche_manifest_path, tranche_error = _load_tranche_manifest(repo_root, tranche_manifest)
    if tranche_payload is None:
        print(json.dumps({"error": tranche_error or "failed to load tranche manifest"}, indent=2))
        return 2

    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")
    tranche_id = str(tranche_payload.get("tranche_id") or "laws-tranche")
    source_prep_payload, source_prep_report_path, source_prep_error = _load_source_prep_report(
        repo_root=repo_root,
        tranche_id=tranche_id,
        source_prep_report=source_prep_report,
    )
    if source_prep_payload is None or source_prep_report_path is None:
        print(json.dumps({"error": source_prep_error or "failed to load source prep report"}, indent=2))
        return 2

    from .canonical_diff import should_overwrite

    folders_by_name: dict[str, dict[str, Any]] = {}
    for folder in source_prep_payload.get("folders", []):
        if isinstance(folder, dict):
            folders_by_name[str(folder.get("folder_name") or "")] = folder

    folder_reports = [
        _summarize_source_admission_folder(
            repo_root=repo_root,
            item=item,
            source_prep_folder=folders_by_name.get(item["folder_name"]) or {},
        )
        for item in tranche_payload["candidate_law_folders"]
    ]

    canonicalize_failure_count = 0
    admitted_source_page_count = 0
    for folder in folder_reports:
        canonicalize_results: list[dict[str, Any]] = []
        admitted_pages: list[dict[str, Any]] = []
        for candidate in folder["candidate_source_pages"]:
            normalized_refined_markdown_path = str(candidate["normalized_refined_markdown_path"])
            try:
                target_file, content = build_structured_source_file(
                    repo_root=repo_root,
                    relative_markdown_path=normalized_refined_markdown_path,
                )
            except FileNotFoundError as exc:
                rc = 1
                output = str(exc)
                wrote = False
                target_file = repo_root / str(candidate["canonical_source_path"])
            else:
                decision = should_overwrite(target_file, content)
                if decision.allowed:
                    target_file.write_text(content, encoding="utf-8")
                    output = f"canonicalize-one complete. Wrote: {target_file}"
                else:
                    output = f"SKIP ({decision.reason}): {target_file}"
                rc = 0
                wrote = target_file.exists()
            canonicalize_results.append(
                {
                    "raw_path": candidate.get("raw_path"),
                    "refined_markdown_path": candidate["refined_markdown_path"],
                    "canonical_source_path": _relative(target_file, repo_root),
                    "rc": rc,
                    "wrote_or_kept": wrote,
                    "output": output.strip(),
                }
            )
            if wrote:
                admitted_pages.append(candidate)
            else:
                canonicalize_failure_count += 1

        folder["canonicalize_results"] = canonicalize_results
        folder["admitted_source_pages"] = admitted_pages
        folder["admitted_source_paths"] = [page["canonical_source_path"] for page in admitted_pages]
        folder["admitted_source_count"] = len(admitted_pages)
        folder["executed_source_admission_state"] = _executed_source_admission_state(folder)
        admitted_source_page_count += len(admitted_pages)

    ready_law_folders, mixed_law_folders, blocked_law_folders = _ready_mixed_blocked_lists(folder_reports)
    blockers = _source_to_graph_blockers(folder_reports, execute=True)

    report_path = Path(report_out).resolve() if report_out else _default_source_admission_execute_report_path(repo_root, tranche_id, run_id)
    report = {
        "action": "run-laws-tranche-source-admission",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "execute": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "tranche_manifest_path": _relative(tranche_manifest_path, repo_root),
        "source_prep_report_path": _relative(source_prep_report_path, repo_root),
        "source_prep_run_id": source_prep_payload.get("run_id"),
        "admission_review_ready_law_folders": ready_law_folders,
        "mixed_readiness_law_folders": mixed_law_folders,
        "blocked_law_folders": blocked_law_folders,
        "admitted_source_page_count": admitted_source_page_count,
        "canonicalize_failure_count": canonicalize_failure_count,
        "manifest_updated": canonicalize_failure_count == 0,
        "source_to_graph_execute_ready": False,
        "source_to_graph_execute_blockers": blockers,
        "laws": folder_reports,
    }
    write_json_report(report_path, report)
    _write_source_admission_back_to_manifest(
        manifest_path=tranche_manifest_path,
        report_path=report_path,
        run_id=run_id,
        folder_reports=folder_reports,
    )

    summary = {
        "action": "run-laws-tranche-source-admission",
        "run_id": run_id,
        "execute": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "admission_review_ready_law_folders": ready_law_folders,
        "mixed_readiness_law_folders": mixed_law_folders,
        "blocked_law_folders": blocked_law_folders,
        "admitted_source_page_count": admitted_source_page_count,
        "canonicalize_failure_count": canonicalize_failure_count,
        "source_to_graph_execute_ready": False,
        "source_prep_report_path": _relative(source_prep_report_path, repo_root),
        "report_path": _relative(report_path, repo_root),
        "tranche_manifest_path": _relative(tranche_manifest_path, repo_root),
    }
    print(json.dumps(summary, indent=2))
    return 0 if canonicalize_failure_count == 0 else 1


def run_laws_tranche_source_to_graph_dry_run(
    *,
    tranche_manifest: str,
    review_preset: str | None = None,
) -> int:
    from .dataset_pipeline import run_dataset_source_to_graph_pipeline

    repo_root = Path.cwd().resolve()
    tranche_payload, tranche_manifest_path, tranche_error = _load_tranche_manifest(repo_root, tranche_manifest)
    if tranche_payload is None:
        print(json.dumps({"error": tranche_error or "failed to load tranche manifest"}, indent=2))
        return 2

    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")
    tranche_id = str(tranche_payload.get("tranche_id") or "laws-tranche")
    paths = _tranche_source_to_graph_paths(repo_root, tranche_id, run_id)
    paths["base"].mkdir(parents=True, exist_ok=True)

    derived_manifest_payload, staged_law_folders, blocked_law_folders = _build_tranche_source_to_graph_manifest_payload(
        repo_root=repo_root,
        tranche_payload=tranche_payload,
        run_id=run_id,
        dataset_id=f"{tranche_id}-source-to-graph-dry-run",
        graph_output_root_rel=f"005_Operational-Intelligence-Layer/graph/datasets/{tranche_id}-source-to-graph-dry-run",
        run_output_root_rel=f"006_System-Manifests/runs/datasets/{tranche_id}-source-to-graph-dry-run",
    )
    if not staged_law_folders:
        print(json.dumps({
            "error": "no admitted tranche members are available for source-to-graph dry-run staging",
            "blocked_law_folders": blocked_law_folders,
        }, indent=2))
        return 2

    paths["derived_manifest"].write_text(
        yaml.safe_dump(derived_manifest_payload, sort_keys=False),
        encoding="utf-8",
    )
    effective_review_preset = review_preset or str(tranche_payload.get("review_model_preset") or "") or None
    duplicate_clusters, duplicate_flags_by_folder = _pdf_duplicate_clusters(
        repo_root=repo_root,
        folder_names=[str(item["folder_name"]) for item in tranche_payload["candidate_law_folders"]],
    )
    variant_visibility, raw_alias_law_folders, guardrail_law_folders = _tranche_variant_visibility(
        tranche_payload=tranche_payload,
        staged_law_folders=staged_law_folders,
        duplicate_flags_by_folder=duplicate_flags_by_folder,
    )
    inner_rc, inner_output = _capture_text_handler(
        lambda: run_dataset_source_to_graph_pipeline(
            dataset_manifest=str(paths["derived_manifest"]),
            dry_run=True,
            review_preset=effective_review_preset,
        )
    )
    if inner_rc != 0:
        if inner_output.strip():
            print(inner_output.strip())
        return inner_rc
    try:
        inner_summary = json.loads(inner_output)
    except json.JSONDecodeError:
        print(json.dumps({"error": "dataset source-to-graph dry-run returned non-JSON output"}, indent=2))
        return 1

    report = {
        "action": "run-laws-tranche-source-to-graph-dry-run",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "dry_run": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "tranche_manifest_path": _relative(tranche_manifest_path, repo_root),
        "derived_manifest_path": _relative(paths["derived_manifest"], repo_root),
        "review_preset": effective_review_preset,
        "staged_law_folders": staged_law_folders,
        "blocked_law_folders": blocked_law_folders,
        "duplicate_cluster_count": len(duplicate_clusters),
        "duplicate_law_folders": sorted(duplicate_flags_by_folder),
        "duplicate_clusters": duplicate_clusters,
        "raw_alias_law_folders": raw_alias_law_folders,
        "guardrail_law_folders": guardrail_law_folders,
        "law_folder_variant_visibility": variant_visibility,
        "source_to_graph_execute_ready": False,
        "source_to_graph_execute_blockers": [
            "tranche source-to-graph execute remains gated until OCR-blocked and wider tranche risks are resolved",
            *([f"{folder} remains blocked pending OCR-first processing" for folder in blocked_law_folders]),
        ],
        "inner_source_to_graph_summary": inner_summary,
    }
    write_json_report(paths["report"], report)

    summary = {
        "action": "run-laws-tranche-source-to-graph-dry-run",
        "run_id": run_id,
        "dry_run": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "review_preset": effective_review_preset,
        "staged_law_folders": staged_law_folders,
        "blocked_law_folders": blocked_law_folders,
        "duplicate_cluster_count": len(duplicate_clusters),
        "duplicate_law_folders": sorted(duplicate_flags_by_folder),
        "raw_alias_law_folders": raw_alias_law_folders,
        "guardrail_law_folders": guardrail_law_folders,
        "planned_stage_count": inner_summary.get("planned_stage_count"),
        "manual_review_required_count": inner_summary.get("manual_review_required_count"),
        "spot_review_required_count": inner_summary.get("spot_review_required_count"),
        "summary_auto_withheld_count": inner_summary.get("summary_auto_withheld_count"),
        "shallow_representation_count": inner_summary.get("shallow_representation_count"),
        "dataset_pipeline_report_path": inner_summary.get("pipeline_report_path"),
        "derived_manifest_path": _relative(paths["derived_manifest"], repo_root),
        "report_path": _relative(paths["report"], repo_root),
        "source_to_graph_execute_ready": False,
    }
    print(json.dumps(summary, indent=2))
    return 0


def run_laws_tranche_source_to_graph(
    *,
    tranche_manifest: str,
    review_preset: str | None = None,
) -> int:
    from .dataset_pipeline import run_dataset_source_to_graph_pipeline

    repo_root = Path.cwd().resolve()
    tranche_payload, tranche_manifest_path, tranche_error = _load_tranche_manifest(repo_root, tranche_manifest)
    if tranche_payload is None:
        print(json.dumps({"error": tranche_error or "failed to load tranche manifest"}, indent=2))
        return 2

    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")
    tranche_id = str(tranche_payload.get("tranche_id") or "laws-tranche")
    paths = _tranche_source_to_graph_execute_paths(repo_root, tranche_id, run_id)
    paths["base"].mkdir(parents=True, exist_ok=True)

    derived_manifest_payload, staged_law_folders, blocked_law_folders = _build_tranche_source_to_graph_manifest_payload(
        repo_root=repo_root,
        tranche_payload=tranche_payload,
        run_id=run_id,
        dataset_id=f"{tranche_id}-source-to-graph-execute",
        graph_output_root_rel=f"005_Operational-Intelligence-Layer/graph/datasets/{tranche_id}-source-to-graph-execute",
        run_output_root_rel=f"006_System-Manifests/runs/datasets/{tranche_id}-source-to-graph-execute",
    )
    if not staged_law_folders:
        print(json.dumps({
            "error": "no admitted tranche members are available for source-to-graph execute staging",
            "blocked_law_folders": blocked_law_folders,
        }, indent=2))
        return 2

    paths["derived_manifest"].write_text(
        yaml.safe_dump(derived_manifest_payload, sort_keys=False),
        encoding="utf-8",
    )
    effective_review_preset = review_preset or str(tranche_payload.get("review_model_preset") or "") or None
    duplicate_clusters, duplicate_flags_by_folder = _pdf_duplicate_clusters(
        repo_root=repo_root,
        folder_names=[str(item["folder_name"]) for item in tranche_payload["candidate_law_folders"]],
    )
    variant_visibility, raw_alias_law_folders, guardrail_law_folders = _tranche_variant_visibility(
        tranche_payload=tranche_payload,
        staged_law_folders=staged_law_folders,
        duplicate_flags_by_folder=duplicate_flags_by_folder,
    )
    inner_rc, inner_output = _capture_text_handler(
        lambda: run_dataset_source_to_graph_pipeline(
            dataset_manifest=str(paths["derived_manifest"]),
            dry_run=False,
            review_preset=effective_review_preset,
        )
    )
    if inner_rc != 0:
        if inner_output.strip():
            print(inner_output.strip())
        return inner_rc
    try:
        inner_summary = json.loads(inner_output)
    except json.JSONDecodeError:
        print(json.dumps({"error": "dataset source-to-graph execute returned non-JSON output"}, indent=2))
        return 1

    report = {
        "action": "run-laws-tranche-source-to-graph",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "execute": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "tranche_manifest_path": _relative(tranche_manifest_path, repo_root),
        "derived_manifest_path": _relative(paths["derived_manifest"], repo_root),
        "review_preset": effective_review_preset,
        "staged_law_folders": staged_law_folders,
        "blocked_law_folders": blocked_law_folders,
        "duplicate_cluster_count": len(duplicate_clusters),
        "duplicate_law_folders": sorted(duplicate_flags_by_folder),
        "duplicate_clusters": duplicate_clusters,
        "raw_alias_law_folders": raw_alias_law_folders,
        "guardrail_law_folders": guardrail_law_folders,
        "law_folder_variant_visibility": variant_visibility,
        "source_to_graph_execute_completed": True,
        "inner_source_to_graph_summary": inner_summary,
    }
    write_json_report(paths["report"], report)

    summary = {
        "action": "run-laws-tranche-source-to-graph",
        "run_id": run_id,
        "execute": True,
        "phase_11_gate": "gated",
        "phase_11_generic_expansion_gated": True,
        "tranche_id": tranche_id,
        "review_preset": effective_review_preset,
        "staged_law_folders": staged_law_folders,
        "blocked_law_folders": blocked_law_folders,
        "duplicate_cluster_count": len(duplicate_clusters),
        "duplicate_law_folders": sorted(duplicate_flags_by_folder),
        "raw_alias_law_folders": raw_alias_law_folders,
        "guardrail_law_folders": guardrail_law_folders,
        "generated_relationship_count": inner_summary.get("generated_relationship_count"),
        "filtered_relationship_count": inner_summary.get("filtered_relationship_count"),
        "manual_review_required_count": inner_summary.get("manual_review_required_count"),
        "spot_review_required_count": inner_summary.get("spot_review_required_count"),
        "summary_auto_withheld_count": inner_summary.get("summary_auto_withheld_count"),
        "shallow_representation_count": inner_summary.get("shallow_representation_count"),
        "dataset_pipeline_report_path": inner_summary.get("pipeline_report_path"),
        "graph_snapshot_path": inner_summary.get("graph_snapshot_path"),
        "graph_build_report_path": inner_summary.get("graph_build_report_path"),
        "derived_manifest_path": _relative(paths["derived_manifest"], repo_root),
        "report_path": _relative(paths["report"], repo_root),
        "source_to_graph_execute_completed": True,
    }
    print(json.dumps(summary, indent=2))
    return 0
