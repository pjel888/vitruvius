from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .graph.dataset_manifest import DatasetManifestError, load_dataset_manifest, write_json_report
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


def run_all_laws_dry_run(
    *,
    pilot_manifest: str = "config/datasets/laws-core-bundle-m1.yaml",
    review_model: str,
    review_model_preset: str | None = None,
    report_out: str | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    run_id = utc_now_stamp().replace("-", "").replace(":", "").replace("+0000", "Z")

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
        pilot_covered = pilot_unit is not None
        if pilot_covered:
            pilot_covered_count += 1
        else:
            inventory_only_count += 1
        admitted_source_count = len(pilot_unit.admitted_source_paths) if pilot_unit else 0
        admitted_concept_count = len(pilot_unit.admitted_concept_paths) if pilot_unit else 0
        admitted_relationship_count = len(pilot_unit.admitted_relationship_paths) if pilot_unit else 0
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
        laws.append(
            {
                "folder_name": folder_name,
                "law_id": folder_name.lower(),
                "pilot_covered": pilot_covered,
                "status": status,
                "raw_source_present": folder_name in raw_source_dirs,
                "refined_markdown_count": refined_counts.get(folder_name, 0),
                "raw_markdown_count": raw_markdown_counts.get(folder_name, 0),
                "sidecar_json_count": sidecar_counts.get(folder_name, 0),
                "admitted_source_count": admitted_source_count,
                "admitted_concept_count": admitted_concept_count,
                "admitted_relationship_count": admitted_relationship_count,
                "next_step": next_step,
            }
        )

    report_path = Path(report_out).resolve() if report_out else _default_report_path(repo_root, run_id)
    report = {
        "action": "run-all-laws-dry-run",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "phase_11_generic_expansion_gated": True,
        "review_model": review_model,
        "review_model_preset": review_model_preset,
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
        "limitations": limitations,
        "laws": laws,
    }
    write_json_report(report_path, report)

    summary = {
        "action": "run-all-laws-dry-run",
        "run_id": run_id,
        "phase_11_generic_expansion_gated": True,
        "review_model": review_model,
        "review_model_preset": review_model_preset,
        "pilot_manifest_path": _relative(manifest_path, repo_root),
        "pilot_manifest_law_count": len(pilot_units_by_folder),
        "pilot_covered_law_count": pilot_covered_count,
        "inventory_only_law_count": inventory_only_count,
        "discovered_law_folder_count": len(all_law_names),
        "limitations": limitations,
        "report_path": _relative(report_path, repo_root),
    }
    print(json.dumps(summary, indent=2))
    return 0
