from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .canonicalize import extract_section_headers
from .config import get_ollama_default_model, get_ollama_default_parallelism, resolve_review_preset
from .conversion import SUPPORTED_DIRECT_INPUT_EXTENSIONS
from .detection import detect_pdf_type
from .graph.dataset_manifest import DatasetManifestError, load_dataset_manifest, write_json_report
from .paths import build_conversion_relative_paths
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
        folders.append({
            "folder_name": folder_name.strip(),
            "reason": reason.strip() if isinstance(reason, str) else "",
        })
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
    markdown_exists = False
    sidecar_exists = False
    refined_exists = False
    if supported:
        markdown_path_rel, json_path_rel = build_conversion_relative_paths(rel_raw)
        refined_path_rel = _refined_markdown_relative_path(markdown_path_rel)
        markdown_rel = (Path("002_Raw-Conversion-Layer") / markdown_path_rel).as_posix()
        sidecar_rel = (Path("002_Raw-Conversion-Layer") / json_path_rel).as_posix()
        refined_rel = (Path("002_Raw-Conversion-Layer") / refined_path_rel).as_posix()
        markdown_exists = (repo_root / markdown_rel).exists()
        sidecar_exists = (repo_root / sidecar_rel).exists()
        refined_exists = (repo_root / refined_rel).exists()

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
        "raw_markdown_exists": markdown_exists,
        "sidecar_json_exists": sidecar_exists,
        "refined_markdown_exists": refined_exists,
    }


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

    report_path = Path(report_out).resolve() if report_out else _default_report_path(repo_root, run_id)
    guardrail_law_folders = [item["folder_name"] for item in laws if item["structure_guardrails"]]
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

    limitations: list[str] = []
    if manifest_error:
        limitations.append(
            f"Pilot manifest { _relative(manifest_path, repo_root) } could not be parsed for tranche comparison: {manifest_error}"
        )
    guardrail_law_folders = [item["folder_name"] for item in laws if item["structure_guardrails"]]
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
        files = sorted(path for path in folder_root.rglob("*") if path.is_file()) if folder_root.exists() else []
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
