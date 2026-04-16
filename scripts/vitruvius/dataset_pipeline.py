from __future__ import annotations

import io
import json
import os
import re
import sys
import webbrowser
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import yaml

from .canonicalize import run_canonicalize_one
from .config import (
    get_ollama_default_model,
    get_ollama_default_parallelism,
    get_ollama_default_timeout,
    resolve_review_preset,
)
from .graph.cli import run_build_graph
from .graph.dataset_manifest import DatasetManifest, DatasetManifestError, load_dataset_manifest, write_json_report
from .ollama_review import run_review_relationships_ollama
from .ontology.cli import run_export_graph_owl
from .promotion import run_promote_inner
from .query.cli import run_query_structured
from .relationships_sections import run_extract_relationships_sections_one_inner
from .source_identity import canonical_source_id_for_relative_path
from .utils import utc_now_stamp


@dataclass(frozen=True)
class StructuredCheck:
    function: str
    subject: str


class DatasetPipelineError(ValueError):
    pass


def _progress_enabled() -> bool:
    return sys.stderr.isatty() or os.getenv("VITRUVIUS_CLI_PROGRESS") == "1"


def _emit_progress(message: str) -> None:
    if _progress_enabled():
        print(f"[vitruvius] {message}", file=sys.stderr, flush=True)


def parse_structured_check(raw: str) -> StructuredCheck:
    try:
        function, subject = raw.split(":", 1)
    except ValueError as exc:
        raise DatasetPipelineError(
            "structured checks must use FUNCTION:SUBJECT format"
        ) from exc
    function = function.strip()
    subject = subject.strip()
    if not function or not subject:
        raise DatasetPipelineError(
            "structured checks must include both function and subject"
        )
    return StructuredCheck(function=function, subject=subject)


def _resolve_manifest_path(dataset_manifest: str, repo_root: Path) -> Path:
    manifest_path = Path(dataset_manifest)
    if not manifest_path.is_absolute():
        manifest_path = repo_root / manifest_path
    return manifest_path


def _load_manifest_or_error(dataset_manifest: str, repo_root: Path) -> tuple[DatasetManifest | None, Path]:
    manifest_path = _resolve_manifest_path(dataset_manifest, repo_root)
    try:
        manifest = load_dataset_manifest(manifest_path, repo_root)
    except DatasetManifestError as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return None, manifest_path
    return manifest, manifest_path


def _resolve_review_runtime_settings(
    *,
    review_preset: str | None = None,
    review_model: str | None = None,
    review_timeout_seconds: int | None = None,
    review_parallelism: int | None = None,
) -> dict[str, int | str | None]:
    settings: dict[str, int | str | None] = {
        "preset": None,
        "model": get_ollama_default_model(),
        "timeout_seconds": get_ollama_default_timeout(),
        "parallelism": get_ollama_default_parallelism(),
        "num_ctx_cap": None,
    }
    if review_preset:
        preset = resolve_review_preset(review_preset)
        if not preset:
            raise DatasetPipelineError(f"unknown review preset: {review_preset}")
        settings.update(preset)
        settings["preset"] = preset
    if review_model is not None:
        settings["model"] = review_model
    if review_timeout_seconds is not None:
        settings["timeout_seconds"] = review_timeout_seconds
    if review_parallelism is not None:
        settings["parallelism"] = review_parallelism
    return settings


def _all_laws_readiness_paths(run_id: str) -> dict[str, Path]:
    base = (
        Path.cwd().resolve()
        / "006_System-Manifests"
        / "runs"
        / "datasets"
        / "all-laws-readiness"
    )
    return {
        "base": base,
        "report": base / f"{run_id}_all_laws_dry_run.json",
    }


def _capture_json_handler(fn) -> tuple[int, dict]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = fn()
    text = buf.getvalue().strip()
    if not text:
        raise DatasetPipelineError("expected JSON output from handler, got empty stdout")
    return rc, json.loads(text)


def _capture_text_handler(fn) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = fn()
    return rc, buf.getvalue()


def run_dataset_graph_pipeline(
    *,
    dataset_manifest: str,
    structured_checks: Sequence[StructuredCheck] = (),
    export_owl: bool = True,
) -> int:
    repo_root = Path.cwd().resolve()
    manifest, manifest_path = _load_manifest_or_error(dataset_manifest, repo_root)
    if manifest is None:
        return 2

    build_rc, build_payload = _capture_json_handler(
        lambda: run_build_graph(dataset_manifest=str(manifest_path))
    )
    if build_rc != 0:
        print(json.dumps(build_payload, indent=2))
        return build_rc

    snapshot_path = Path(build_payload["snapshot_path"])
    if not snapshot_path.is_absolute():
        snapshot_path = repo_root / snapshot_path

    owl_payload: dict[str, str | int] | None = None
    if export_owl:
        owl_path = snapshot_path.with_suffix(".ttl")
        owl_rc, _ = _capture_text_handler(
            lambda: run_export_graph_owl(
                snapshot_path=str(snapshot_path),
                out_path=str(owl_path),
            )
        )
        owl_payload = {
            "rc": owl_rc,
            "path": str(owl_path.relative_to(repo_root)),
        }
        if owl_rc != 0:
            print(json.dumps({"error": "dataset owl export failed", "owl": owl_payload}, indent=2))
            return owl_rc

    check_results: list[dict[str, object]] = []
    for check in structured_checks:
        rc, output = _capture_text_handler(
            lambda: run_query_structured(
                function=check.function,
                subject=check.subject,
                snapshot_path=str(snapshot_path),
            )
        )
        check_results.append(
            {
                "function": check.function,
                "subject": check.subject,
                "rc": rc,
                "output": output.strip(),
            }
        )
        if rc != 0:
            print(json.dumps({"error": "structured check failed", "check": check_results[-1]}, indent=2))
            return rc

    run_id = str(build_payload["run_id"])
    report_path = manifest.run_output_root / f"{run_id}_dataset_pipeline_run_report.json"
    report = {
        "action": "run-dataset-graph",
        "generated_at_utc": utc_now_stamp(),
        "dataset_id": manifest.dataset_id,
        "dataset_kind": manifest.dataset_kind,
        "law_unit_count": len(manifest.law_units),
        "contributing_law_ids": [unit.law_id for unit in manifest.law_units],
        "manifest_path": str(manifest_path.relative_to(repo_root)),
        "run_id": run_id,
        "build": build_payload,
        "owl": owl_payload,
        "structured_checks": check_results,
    }
    write_json_report(report_path, report)

    summary = {
        "action": "run-dataset-graph",
        "dataset_id": manifest.dataset_id,
        "law_unit_count": len(manifest.law_units),
        "contributing_law_ids": [unit.law_id for unit in manifest.law_units],
        "run_id": run_id,
        "snapshot_path": build_payload["snapshot_path"],
        "build_report_path": build_payload.get("build_report_path"),
        "pipeline_report_path": str(report_path.relative_to(repo_root)),
        "owl_path": owl_payload["path"] if owl_payload else None,
        "structured_check_count": len(check_results),
    }
    print(json.dumps(summary, indent=2))
    return 0




def _normalize_refined_markdown_path(relative_path: str) -> str:
    rel = relative_path.strip()
    prefix = '002_Raw-Conversion-Layer/'
    if rel.startswith(prefix):
        return rel[len(prefix):]
    return rel

def _dataset_source_to_graph_paths(manifest: DatasetManifest, run_id: str) -> dict[str, Path]:
    base = manifest.run_output_root / "source_to_graph" / run_id
    return {
        "base": base,
        "derived_manifest": base / "derived_dataset_manifest.yaml",
        "report": base / "source_to_graph_run_report.json",
        "promoted_relationships": base / "promoted_relationships",
        "promotion_audit": base / "promotion_audit.log",
        "source_quality": base / "source_quality",
    }




def _load_frontmatter(path: Path) -> dict[str, object]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)

    if end == -1:
        return {}
    try:
        payload = yaml.safe_load(text[3:end].strip())
    except yaml.YAMLError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _relationship_record_is_graph_admissible(path: Path) -> bool:
    fm = _load_frontmatter(path)
    from_entity = fm.get("from_entity")
    to_entity = fm.get("to_entity")
    rel_type = fm.get("relationship_type")
    if not isinstance(from_entity, str) or not isinstance(to_entity, str) or not isinstance(rel_type, str):
        return False
    source_prefixes = ("law-", "irr-", "source-", "handout-", "reviewer-", "law-section-")
    return from_entity.startswith(source_prefixes) and to_entity.startswith("concept-") and rel_type == "governs"



def _dedupe_generated_relationship_paths(paths: list[tuple[str, str]], *, repo_root: Path) -> list[tuple[str, str]]:
    try:
        from .promotion import _load_existing_record, merge_evidence
    except Exception:
        return paths

    deduped: dict[str, tuple[str, str]] = {}
    for rel_path, folder_name in paths:
        abs_path = repo_root / rel_path
        existing = deduped.get(rel_path)
        if existing is None:
            deduped[rel_path] = (rel_path, folder_name)
            continue
        # same path already recorded; keep once
        deduped[rel_path] = (rel_path, folder_name)
    return list(deduped.values())

def _append_generated_relationships_to_manifest(
    manifest_path: Path,
    *,
    generated_relationship_paths: list[tuple[str, str]],
    out_path: Path,
) -> None:
    payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    rels = payload["relationship_input_manifest"]["relationships"]
    existing = {entry["path"] for entry in rels}
    for rel_path, folder_name in generated_relationship_paths:
        if rel_path in existing:
            continue
        rels.append(
            {
                "path": rel_path,
                "folder_name": folder_name,
                "entry_role": "authoritative",
                "authority_tier": "approved",
                "variant_family": f"{folder_name.lower()}-dataset-generated-relationship",
                "edition_or_source_note": "Dataset-local promoted relationship generated by run-dataset-source-to-graph.",
                "include_in_m1": True,
                "reason": "Bounded source-to-graph automation admitted this dataset-local relationship for the scoped graph run.",
            }
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")




def _source_quality_severity(metrics: dict[str, object]) -> str:
    image_count = int(metrics.get("image_line_count", 0) or 0)
    table_count = int(metrics.get("table_line_count", 0) or 0)
    useful_ratio = float(metrics.get("useful_text_ratio", 0.0) or 0.0)
    noise_count = int(metrics.get("noise_line_count", 0) or 0)
    if useful_ratio < 0.6 or image_count > 500 or table_count > 800:
        return "high"
    if useful_ratio < 0.8 or image_count > 100 or table_count > 100 or noise_count > 50:
        return "medium"
    return "low"



def _source_quality_recommendations(metrics: dict[str, object]) -> list[str]:
    recommendations: list[str] = []
    image_count = int(metrics.get("image_line_count", 0) or 0)
    table_count = int(metrics.get("table_line_count", 0) or 0)
    useful_ratio = float(metrics.get("useful_text_ratio", 0.0) or 0.0)
    structural_heading_count = int(metrics.get("structural_heading_count", 0) or 0)
    if image_count > 100:
        recommendations.append("high image-line count: verify OCR quality or alternate source availability")
    if table_count > 100:
        recommendations.append("high table-line count: verify layout-sensitive extraction and summary hygiene")
    if useful_ratio < 0.8:
        recommendations.append("low useful-text ratio: review source-summary trust before relying on canonical summaries")
    if structural_heading_count < 5:
        recommendations.append("low structural-heading count: verify section detection and source structure fidelity")
    return recommendations


def _source_summary_hygiene_flags(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    first_window = lines[:160]
    flags: list[str] = []
    lowered_window = [line.lower() for line in first_window]
    if any("table of contents" in line for line in lowered_window):
        flags.append("table_of_contents_front_matter")
    if any(line in {"|preface|", "|message|"} for line in lowered_window):
        flags.append("preface_or_message_front_matter")
    if any("foreword" in line or "acknowledgement" in line for line in lowered_window):
        flags.append("preface_or_message_front_matter")
    if any("memorandum circular" in line for line in lowered_window):
        flags.append("administrative_front_matter")
    image_front_matter_count = sum(1 for line in first_window if line.startswith("!["))
    table_front_matter_count = sum(1 for line in first_window if line.startswith("|") and line.endswith("|"))
    if image_front_matter_count >= 3:
        flags.append("image_heavy_front_matter")
    if table_front_matter_count >= 6:
        flags.append("table_heavy_front_matter")
    return list(dict.fromkeys(flags))


def _extraction_trust_level(metrics: dict[str, object]) -> str:
    severity = metrics.get("severity")
    summary_flags = metrics.get("summary_hygiene_flags") or []
    if severity == "high":
        return "review_required"
    if severity == "medium" or summary_flags:
        return "guarded"
    return "trusted"


def _extraction_trust_reasons(metrics: dict[str, object]) -> list[str]:
    reasons: list[str] = []
    severity = metrics.get("severity")
    if severity == "high":
        reasons.append("high extraction difficulty: require manual review before trusting unattended summaries")
    elif severity == "medium":
        reasons.append("moderate extraction difficulty: treat automated summaries as guarded")
    flag_messages = {
        "table_of_contents_front_matter": "front matter includes a table of contents before operative text",
        "preface_or_message_front_matter": "front matter includes preface/message prose that can pollute source summaries",
        "administrative_front_matter": "front matter includes circular or title-page material ahead of operative rules",
        "image_heavy_front_matter": "front matter is image-heavy and may reflect OCR/layout instability",
        "table_heavy_front_matter": "front matter is table-heavy and may reflect layout extraction noise",
    }
    for flag in metrics.get("summary_hygiene_flags", []):
        message = flag_messages.get(flag)
        if message:
            reasons.append(message)
    if metrics.get("manual_review_recommended"):
        reasons.append("benchmark authoritative references before promoting summary claims")
    return reasons



def _benchmark_source_hints(normalized_refined_path: str, source_id: str) -> list[dict[str, str]]:
    rel = normalized_refined_path.lower()
    hints: list[dict[str, str]] = []
    if 'pd-1096' in rel and 'irr' in rel:
        hints.append({
            'label': 'DPWH PD 1096 IRR reference page',
            'url': 'https://www.dpwh.gov.ph/DPWH/references/laws_codes_orders/PD1096',
            'note': 'Official DPWH-hosted IRR reference page useful for cross-checking difficult OCR/layout cases.'
        })
    if 'ra-9514' in rel or 'ra9514' in rel:
        hints.append({
            'label': 'BFP RA 9514 revised IRR page',
            'url': 'https://bfp.gov.ph/revised-irr-of-ra-9514-the-fire-code-of-the-philippines/',
            'note': 'Official BFP page for the revised IRR; useful when scanned/local extraction is noisy.'
        })
    if 'bp-220' in rel or 'bp220' in rel:
        hints.append({
            'label': 'Lawphil BP 220 revised IRR PDF',
            'url': 'https://lawphil.net/statutes/repacts/ra2008/pdf/irr_bp220_2008.pdf',
            'note': 'Lawphil-hosted IRR PDF for cross-checking structure and section layout.'
        })
    if 'bp-344' in rel or 'bp344' in rel:
        hints.append({
            'label': 'NCDA revised BP 344 IRR page',
            'url': 'https://ncda.gov.ph/revised-2024-rules-and-regulations-implementing-batas-pambansa-344/',
            'note': 'NCDA-hosted revised IRR page useful for checking structure when the PDF is hard to extract.'
        })
        hints.append({
            'label': 'Lawphil BP 344 law text',
            'url': 'https://lawphil.net/statutes/bataspam/bp1983/bp_344_1983.html',
            'note': 'Lawphil law text for the underlying statute (not the revised IRR). Useful as a semantic benchmark.'
        })
    return hints

def _compute_refined_markdown_quality(repo_root: Path, normalized_refined_path: str) -> dict[str, object]:
    refined_path = repo_root / "002_Raw-Conversion-Layer" / normalized_refined_path
    text = refined_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    non_empty = [line.strip() for line in lines if line.strip()]
    image_lines = [line for line in non_empty if line.startswith("![")]
    table_lines = [line for line in non_empty if line.startswith("|") and line.endswith("|")]
    markdown_heading_lines = [line for line in non_empty if re.match(r"^#{2,6}\s+", line)]
    structural_heading_lines = [
        line for line in non_empty
        if re.match(r"^(#{2,6}\s+)?(rule|section|chapter|division|appendix|annex|part)\b", line, re.IGNORECASE)
        or re.match(r"^(#{2,6}\s+)?\d+\.\s+", line)
    ]
    noise_lines = [
        line for line in non_empty
        if ('http://' in line.lower() or 'https://' in line.lower() or 'isbn' in line.lower() or 'table of contents' in line.lower() or line.lower().startswith('govph'))
    ]
    useful_lines = [
        line for line in non_empty
        if line not in image_lines and line not in table_lines and line not in noise_lines
    ]
    metrics = {
        "refined_markdown_path": normalized_refined_path,
        "total_line_count": len(lines),
        "non_empty_line_count": len(non_empty),
        "image_line_count": len(image_lines),
        "table_line_count": len(table_lines),
        "markdown_heading_count": len(markdown_heading_lines),
        "structural_heading_count": len(structural_heading_lines),
        "noise_line_count": len(noise_lines),
        "useful_text_line_count": len(useful_lines),
        "useful_text_ratio": round(len(useful_lines) / len(non_empty), 6) if non_empty else 0.0,
    }
    metrics["severity"] = _source_quality_severity(metrics)
    metrics["recommendations"] = _source_quality_recommendations(metrics)
    metrics["benchmark_source_hints"] = _benchmark_source_hints(normalized_refined_path, "")
    metrics["summary_hygiene_flags"] = _source_summary_hygiene_flags(text)
    metrics["manual_review_recommended"] = metrics["severity"] == "high"
    metrics["summary_auto_withheld"] = metrics["severity"] == "high"
    metrics["canonical_summary_action"] = (
        "withhold_auto_summary" if metrics["summary_auto_withheld"] else "allow_auto_summary"
    )
    metrics["extraction_trust_level"] = _extraction_trust_level(metrics)
    metrics["extraction_trust_reasons"] = _extraction_trust_reasons(metrics)
    return metrics




def _source_quality_summary(stage_results: list[dict[str, object]]) -> dict[str, object]:
    counts = {"low": 0, "medium": 0, "high": 0}
    extraction_trust_counts = {"trusted": 0, "guarded": 0, "review_required": 0}
    high_paths: list[str] = []
    manual_review_required_paths: list[str] = []
    summary_auto_withheld_paths: list[str] = []
    high_severity_sources: list[dict[str, object]] = []
    manual_review_required_sources: list[dict[str, object]] = []
    benchmark_hints: dict[str, dict[str, str]] = {}
    for stage in stage_results:
        quality = stage.get("source_quality")
        if not isinstance(quality, dict):
            continue
        severity = quality.get("severity")
        extraction_trust_level = quality.get("extraction_trust_level")
        path = stage.get("normalized_refined_markdown_path") or quality.get("refined_markdown_path")
        raw_recommendations = quality.get("recommendations")
        raw_benchmark_hints = quality.get("benchmark_source_hints")
        stage_summary = {
            "source_id": stage.get("source_id"),
            "refined_markdown_path": path,
            "severity": severity,
            "manual_review_recommended": bool(quality.get("manual_review_recommended")),
            "recommendations": list(raw_recommendations) if isinstance(raw_recommendations, list) else [],
            "difficulty_signals": {
                "image_line_count": int(quality.get("image_line_count", 0) or 0),
                "table_line_count": int(quality.get("table_line_count", 0) or 0),
                "noise_line_count": int(quality.get("noise_line_count", 0) or 0),
                "structural_heading_count": int(quality.get("structural_heading_count", 0) or 0),
                "useful_text_ratio": float(quality.get("useful_text_ratio", 0.0) or 0.0),
            },
            "benchmark_source_hints": list(raw_benchmark_hints) if isinstance(raw_benchmark_hints, list) else [],
        }
        if severity in counts:
            counts[severity] += 1
            if severity == "high" and isinstance(path, str):
                high_paths.append(path)
                high_severity_sources.append(stage_summary)
        if extraction_trust_level in extraction_trust_counts:
            extraction_trust_counts[extraction_trust_level] += 1
        if quality.get("manual_review_recommended") and isinstance(path, str):
            manual_review_required_paths.append(path)
            manual_review_required_sources.append(stage_summary)
        if quality.get("summary_auto_withheld") and isinstance(path, str):
            summary_auto_withheld_paths.append(path)
        for hint in quality.get("benchmark_source_hints", []):
            if isinstance(hint, dict):
                url = hint.get("url")
                if isinstance(url, str) and url:
                    benchmark_hints[url] = hint
    return {
        "severity_counts": counts,
        "extraction_trust_counts": extraction_trust_counts,
        "high_severity_paths": list(dict.fromkeys(high_paths)),
        "high_severity_sources": high_severity_sources,
        "manual_review_required_paths": list(dict.fromkeys(manual_review_required_paths)),
        "manual_review_required_sources": manual_review_required_sources,
        "summary_auto_withheld_paths": list(dict.fromkeys(summary_auto_withheld_paths)),
        "benchmark_source_hints": [benchmark_hints[url] for url in sorted(benchmark_hints)],
    }


def _resolve_admitted_source_anchor(
    *,
    repo_root: Path,
    law_unit,
    expected_source_id: str,
) -> dict[str, object]:
    for rel_path in law_unit.admitted_source_paths:
        frontmatter = _load_frontmatter(repo_root / rel_path)
        source_id = frontmatter.get("id")
        if source_id == expected_source_id:
            return {
                "path": rel_path,
                "id": source_id,
                "trust_level": frontmatter.get("trust_level"),
                "title": frontmatter.get("title"),
            }
    admitted_paths = list(law_unit.admitted_source_paths)
    raise DatasetPipelineError(
        f"law unit {law_unit.law_id!r} has no admitted canonical source anchor for {expected_source_id!r}; "
        "refined source-to-graph execution refuses raw/refined→graph shortcuts without a matching admitted source. "
        f"Admitted source paths: {admitted_paths}"
    )


def run_all_laws_dry_run(
    *,
    bounded_dataset_manifest: str = "config/datasets/laws-core-bundle-m1.yaml",
    review_preset: str | None = None,
    review_model: str | None = None,
    review_timeout_seconds: int | None = None,
    review_parallelism: int | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    raw_root = repo_root / "001_Raw-Source-Layer" / "001-Laws"
    if not raw_root.exists():
        print(json.dumps({"error": f"missing laws raw root: {raw_root.relative_to(repo_root)}"}, indent=2))
        return 2

    try:
        review_settings = _resolve_review_runtime_settings(
            review_preset=review_preset,
            review_model=review_model,
            review_timeout_seconds=review_timeout_seconds,
            review_parallelism=review_parallelism,
        )
    except DatasetPipelineError as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return 2

    manifest, manifest_path = _load_manifest_or_error(bounded_dataset_manifest, repo_root)
    if manifest is None:
        return 2

    _emit_progress(
        f"Loaded bounded coverage manifest {manifest.dataset_id} from {manifest_path.relative_to(repo_root)}"
    )
    _emit_progress("Scanning all law folders for dry-run readiness only")

    run_id = utc_now_stamp().replace('-', '').replace(':', '').replace('+0000', 'Z').replace('T', 'T')
    paths = _all_laws_readiness_paths(run_id)
    paths["base"].mkdir(parents=True, exist_ok=True)

    covered_by_folder = {unit.folder_name: unit for unit in manifest.law_units}
    refined_root = repo_root / "002_Raw-Conversion-Layer" / "001-Laws" / "refined_markdown"
    raw_folders = sorted(path for path in raw_root.iterdir() if path.is_dir())
    folder_summaries: list[dict[str, object]] = []

    for folder in raw_folders:
        pdf_paths = sorted(
            path for path in folder.rglob("*")
            if path.is_file() and path.suffix.lower() == ".pdf"
        )
        refined_dir = refined_root / folder.name
        refined_markdown_paths = (
            sorted(path for path in refined_dir.glob("*.md") if path.is_file())
            if refined_dir.exists()
            else []
        )
        covered_unit = covered_by_folder.get(folder.name)
        folder_summaries.append(
            {
                "folder_name": folder.name,
                "pdf_count": len(pdf_paths),
                "raw_pdf_paths_sample": [
                    str(path.relative_to(repo_root)) for path in pdf_paths[:5]
                ],
                "refined_markdown_count": len(refined_markdown_paths),
                "covered_by_bounded_pilot": covered_unit is not None,
                "bounded_law_id": covered_unit.law_id if covered_unit else None,
                "recommended_next_action": (
                    "keep within bounded manifest until a fresh widening slice is accepted"
                    if covered_unit
                    else "prepare a fresh manifest-backed widening slice before any execute path"
                ),
            }
        )

    covered_folders = [item["folder_name"] for item in folder_summaries if item["covered_by_bounded_pilot"]]
    uncovered_folders = [item["folder_name"] for item in folder_summaries if not item["covered_by_bounded_pilot"]]
    total_pdf_count = sum(int(item["pdf_count"]) for item in folder_summaries)
    total_refined_markdown_count = sum(int(item["refined_markdown_count"]) for item in folder_summaries)

    report = {
        "action": "run-all-laws-dry-run",
        "generated_at_utc": utc_now_stamp(),
        "run_id": run_id,
        "dry_run_only": True,
        "execute_enabled": False,
        "ready_for_full_execute": False,
        "bounded_dataset_manifest_path": str(manifest_path.relative_to(repo_root)),
        "bounded_dataset_id": manifest.dataset_id,
        "review_settings": review_settings,
        "law_folder_count": len(folder_summaries),
        "pdf_count": total_pdf_count,
        "refined_markdown_count": total_refined_markdown_count,
        "covered_folder_count": len(covered_folders),
        "uncovered_folder_count": len(uncovered_folders),
        "covered_folders": covered_folders,
        "uncovered_folders": uncovered_folders,
        "folder_summaries": folder_summaries,
        "notes": [
            "This command is a readiness-only dry-run path for all-laws planning.",
            "It does not execute dataset review, promotion, graph build, visualization, or browser-open flows.",
            "Generic Phase 11 expansion remains gated until a fresh widening slice is accepted.",
        ],
    }
    write_json_report(paths["report"], report)

    print(json.dumps({
        "action": "run-all-laws-dry-run",
        "run_id": run_id,
        "dry_run_only": True,
        "ready_for_full_execute": False,
        "review_settings": review_settings,
        "law_folder_count": len(folder_summaries),
        "pdf_count": total_pdf_count,
        "refined_markdown_count": total_refined_markdown_count,
        "covered_folder_count": len(covered_folders),
        "uncovered_folder_count": len(uncovered_folders),
        "covered_folders": covered_folders,
        "uncovered_folders_sample": uncovered_folders[:10],
        "pipeline_report_path": str(paths["report"].relative_to(repo_root)),
    }, indent=2))
    _emit_progress("Completed all-laws readiness dry-run")
    return 0

def run_dataset_source_to_graph_pipeline(
    *,
    dataset_manifest: str,
    structured_checks: Sequence[StructuredCheck] = (),
    export_owl: bool = True,
    dry_run: bool = False,
    review_preset: str | None = None,
    review_model: str | None = None,
    review_timeout_seconds: int | None = None,
    review_parallelism: int | None = None,
    visualize_graph: bool = False,
    open_browser: bool = False,
    visualization_out_path: str | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    if dry_run and (visualize_graph or open_browser):
        print(json.dumps({
            "error": "--visualize / --open-browser are only available for non-dry-run source-to-graph executions",
        }, indent=2))
        return 2
    manifest, manifest_path = _load_manifest_or_error(dataset_manifest, repo_root)
    if manifest is None:
        return 2
    try:
        review_settings = _resolve_review_runtime_settings(
            review_preset=review_preset,
            review_model=review_model,
            review_timeout_seconds=review_timeout_seconds,
            review_parallelism=review_parallelism,
        )
    except DatasetPipelineError as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return 2
    _emit_progress(
        f"Loaded dataset manifest {manifest.dataset_id} from {manifest_path.relative_to(repo_root)}"
    )

    run_id = utc_now_stamp().replace('-', '').replace(':', '').replace('+0000', 'Z').replace('T', 'T')
    paths = _dataset_source_to_graph_paths(manifest, run_id)
    generated_relationship_paths: list[tuple[str, str]] = []
    filtered_relationship_paths: list[str] = []
    stage_results: list[dict[str, object]] = []
    total_stage_count = sum(len(law_unit.refined_markdown_paths or ()) for law_unit in manifest.law_units)
    stage_index = 0

    for law_unit in manifest.law_units:
        law_base = paths["base"] / law_unit.law_id
        law_base.mkdir(parents=True, exist_ok=True)
        refined_paths = law_unit.refined_markdown_paths or ()

        for refined_path in refined_paths:
            stage_index += 1
            normalized_refined_path = _normalize_refined_markdown_path(refined_path)
            source_id = canonical_source_id_for_relative_path(normalized_refined_path)
            _emit_progress(
                f"[{stage_index}/{total_stage_count}] Inspecting source quality for {law_unit.law_id} :: {Path(normalized_refined_path).name}"
            )
            source_quality = _compute_refined_markdown_quality(repo_root, normalized_refined_path)
            try:
                admitted_source_anchor = _resolve_admitted_source_anchor(
                    repo_root=repo_root,
                    law_unit=law_unit,
                    expected_source_id=source_id,
                )
            except DatasetPipelineError as exc:
                print(json.dumps({
                    "error": str(exc),
                    "law_id": law_unit.law_id,
                    "refined_markdown_path": refined_path,
                    "source_id": source_id,
                }, indent=2))
                return 2
            source_quality_path = paths["source_quality"] / law_unit.law_id / f"{Path(normalized_refined_path).stem}_source_quality.json"
            write_json_report(source_quality_path, source_quality)
            if dry_run:
                stage_results.append(
                    {
                        "law_id": law_unit.law_id,
                        "refined_markdown_path": refined_path,
                        "normalized_refined_markdown_path": normalized_refined_path,
                        "source_id": source_id,
                        "admitted_canonical_source_anchor": admitted_source_anchor,
                        "source_quality": source_quality,
                        "source_quality_path": str(source_quality_path.relative_to(repo_root)),
                        "planned_extract_json": str((law_base / f"{Path(refined_path).stem}_extract.json").relative_to(repo_root)),
                        "planned_review_json": str((law_base / f"{Path(refined_path).stem}_review.json").relative_to(repo_root)),
                        "planned_high_conf_json": str((law_base / f"{Path(refined_path).stem}_high_conf.json").relative_to(repo_root)),
                        "planned_promoted_relationship_dir": str((paths["promoted_relationships"] / law_unit.law_id).relative_to(repo_root)),
                    }
                )
                continue

            _emit_progress(f"[{stage_index}/{total_stage_count}] Canonicalizing {source_id}")
            canonicalize_rc, canonicalize_output = _capture_text_handler(
                lambda rel_path=normalized_refined_path: run_canonicalize_one(relative_markdown_path=rel_path)
            )
            if canonicalize_rc != 0:
                print(json.dumps({
                    "error": "canonicalize-one failed",
                    "law_id": law_unit.law_id,
                    "refined_markdown_path": refined_path,
                    "output": canonicalize_output.strip(),
                }, indent=2))
                return canonicalize_rc

            extract_json = law_base / f"{Path(refined_path).stem}_extract.json"
            extract_txt = law_base / f"{Path(refined_path).stem}_extract.txt"
            _emit_progress(f"[{stage_index}/{total_stage_count}] Extracting relationships for {source_id}")
            extract_rc, extract_output = _capture_text_handler(
                lambda rel_path=normalized_refined_path: run_extract_relationships_sections_one_inner(
                    repo_root=repo_root,
                    relative_markdown_path=rel_path,
                    json_output_path=extract_json,
                    txt_output_path=extract_txt,
                    source_id_override=source_id,
                )
            )
            if extract_rc != 0:
                print(json.dumps({
                    "error": "extract-relationships-sections-one failed",
                    "law_id": law_unit.law_id,
                    "refined_markdown_path": refined_path,
                    "output": extract_output.strip(),
                }, indent=2))
                return extract_rc

            review_json = law_base / f"{Path(refined_path).stem}_review.json"
            review_txt = law_base / f"{Path(refined_path).stem}_review.txt"
            triage_json = law_base / f"{Path(refined_path).stem}_triage.json"
            high_conf_json = law_base / f"{Path(refined_path).stem}_high_conf.json"
            _emit_progress(f"[{stage_index}/{total_stage_count}] Reviewing extracted relationships for {source_id}")
            review_rc, review_output = _capture_text_handler(
                lambda: run_review_relationships_ollama(
                    model=str(review_settings["model"]),
                    timeout_seconds=int(review_settings["timeout_seconds"]),
                    parallelism=int(review_settings["parallelism"]),
                    extraction_report_path=extract_json,
                    review_json_path=review_json,
                    review_txt_path=review_txt,
                    triage_report_path=triage_json,
                    high_confidence_output_path=high_conf_json,
                )
            )
            if review_rc != 0:
                print(json.dumps({
                    "error": "review-relationships-ollama failed",
                    "law_id": law_unit.law_id,
                    "refined_markdown_path": refined_path,
                    "output": review_output.strip(),
                }, indent=2))
                return review_rc

            promoted_dir = paths["promoted_relationships"] / law_unit.law_id
            _emit_progress(f"[{stage_index}/{total_stage_count}] Promoting dataset-local relationships for {source_id}")
            promote_result = run_promote_inner(
                repo_root=repo_root,
                execute=True,
                rollback_batch_id=None,
                high_confidence_input_path=high_conf_json,
                relationships_output_dir=promoted_dir,
                audit_log_path=paths["promotion_audit"],
            )
            if promote_result.get("rejected") or promote_result.get("errors"):
                print(json.dumps({
                    "error": "promote failed",
                    "law_id": law_unit.law_id,
                    "result": promote_result,
                }, indent=2))
                return 1

            admitted_for_graph = 0
            filtered_out = 0
            for rel_file in sorted(promoted_dir.glob("rel-*.md")):
                rel_rel = str(rel_file.relative_to(repo_root))
                if _relationship_record_is_graph_admissible(rel_file):
                    generated_relationship_paths.append((rel_rel, law_unit.folder_name))
                    admitted_for_graph += 1
                else:
                    filtered_relationship_paths.append(rel_rel)
                    filtered_out += 1

            stage_results.append(
                {
                    "law_id": law_unit.law_id,
                    "refined_markdown_path": refined_path,
                    "normalized_refined_markdown_path": normalized_refined_path,
                    "source_id": source_id,
                    "admitted_canonical_source_anchor": admitted_source_anchor,
                    "source_quality": source_quality,
                    "source_quality_path": str(source_quality_path.relative_to(repo_root)),
                    "extract_json": str(extract_json.relative_to(repo_root)),
                    "review_json": str(review_json.relative_to(repo_root)),
                    "high_conf_json": str(high_conf_json.relative_to(repo_root)),
                    "promoted_relationship_dir": str(promoted_dir.relative_to(repo_root)),
                    "promote_result": promote_result,
                    "graph_admitted_relationships": admitted_for_graph,
                    "graph_filtered_relationships": filtered_out,
                }
            )

    if dry_run:
        quality_summary = _source_quality_summary(stage_results)
        report = {
            "action": "run-dataset-source-to-graph",
            "generated_at_utc": utc_now_stamp(),
            "dataset_id": manifest.dataset_id,
            "run_id": run_id,
            "manifest_path": str(manifest_path.relative_to(repo_root)),
            "dry_run": True,
            "review_settings": review_settings,
            "review_runtime": review_settings,
            "source_quality_summary": quality_summary,
            "stage_results": stage_results,
        }
        write_json_report(paths["report"], report)
        print(json.dumps({
            "action": "run-dataset-source-to-graph",
            "dataset_id": manifest.dataset_id,
            "run_id": run_id,
            "dry_run": True,
            "review_model": review_settings["model"],
            "review_preset": review_preset,
            "pipeline_report_path": str(paths["report"].relative_to(repo_root)),
            "review_settings": review_settings,
            "review_runtime": review_settings,
            "planned_stage_count": len(stage_results),
            "manual_review_required_count": len(quality_summary["manual_review_required_paths"]),
            "summary_auto_withheld_count": len(quality_summary["summary_auto_withheld_paths"]),
            "benchmark_hint_count": len(quality_summary["benchmark_source_hints"]),
            "source_quality_summary": quality_summary,
        }, indent=2))
        return 0

    _emit_progress("Building bounded graph snapshot from derived manifest")
    generated_relationship_paths = _dedupe_generated_relationship_paths(generated_relationship_paths, repo_root=repo_root)
    _append_generated_relationships_to_manifest(
        manifest_path,
        generated_relationship_paths=generated_relationship_paths,
        out_path=paths["derived_manifest"],
    )

    graph_rc, graph_output = _capture_text_handler(
        lambda: run_dataset_graph_pipeline(
            dataset_manifest=str(paths["derived_manifest"]),
            structured_checks=structured_checks,
            export_owl=export_owl,
        )
    )
    if graph_rc != 0:
        print(graph_output.strip())
        return graph_rc
    graph_payload = json.loads(graph_output)

    visualization_payload: dict[str, object] | None = None
    browser_opened = False
    if visualize_graph or open_browser:
        from .graph.visualize import run_visualize_graph

        _emit_progress("Rendering browser visualization HTML")
        visualize_rc, visualize_output = _capture_text_handler(
            lambda: run_visualize_graph(
                snapshot_path=graph_payload.get("snapshot_path"),
                out_path=visualization_out_path,
            )
        )
        if visualize_rc != 0:
            print(visualize_output.strip())
            return visualize_rc
        visualization_payload = json.loads(visualize_output)
        if open_browser:
            html_path = Path(visualization_payload["out_path"])
            if not html_path.is_absolute():
                html_path = repo_root / html_path
            _emit_progress(f"Opening browser for {html_path.relative_to(repo_root)}")
            browser_opened = webbrowser.open(html_path.resolve().as_uri())

    quality_summary = _source_quality_summary(stage_results)
    report = {
        "action": "run-dataset-source-to-graph",
        "generated_at_utc": utc_now_stamp(),
        "dataset_id": manifest.dataset_id,
        "run_id": run_id,
        "manifest_path": str(manifest_path.relative_to(repo_root)),
        "derived_manifest_path": str(paths["derived_manifest"].relative_to(repo_root)),
        "review_model": review_settings["model"],
        "review_preset": review_preset,
        "generated_relationship_count": len(generated_relationship_paths),
        "filtered_relationship_count": len(filtered_relationship_paths),
        "filtered_relationship_paths": filtered_relationship_paths,
        "review_settings": review_settings,
        "review_runtime": review_settings,
        "source_quality_summary": quality_summary,
        "stage_results": stage_results,
        "graph": graph_payload,
        "visualization": visualization_payload,
        "browser_opened": browser_opened if open_browser else None,
    }
    write_json_report(paths["report"], report)

    summary = {
        "action": "run-dataset-source-to-graph",
        "dataset_id": manifest.dataset_id,
        "run_id": run_id,
        "derived_manifest_path": str(paths["derived_manifest"].relative_to(repo_root)),
        "review_model": review_settings["model"],
        "review_preset": review_preset,
        "generated_relationship_count": len(generated_relationship_paths),
        "filtered_relationship_count": len(filtered_relationship_paths),
        "review_settings": review_settings,
        "review_runtime": review_settings,
        "manual_review_required_count": len(quality_summary["manual_review_required_paths"]),
        "summary_auto_withheld_count": len(quality_summary["summary_auto_withheld_paths"]),
        "benchmark_hint_count": len(quality_summary["benchmark_source_hints"]),
        "source_quality_summary": quality_summary,
        "pipeline_report_path": str(paths["report"].relative_to(repo_root)),
        "graph_snapshot_path": graph_payload.get("snapshot_path"),
        "graph_build_report_path": graph_payload.get("build_report_path"),
        "visualization_html_path": visualization_payload.get("out_path") if visualization_payload else None,
        "browser_opened": browser_opened if open_browser else None,
    }
    print(json.dumps(summary, indent=2))
    _emit_progress("Completed bounded source-to-graph pipeline")
    return 0
