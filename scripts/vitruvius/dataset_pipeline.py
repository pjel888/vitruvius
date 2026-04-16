from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import yaml

from .canonicalize import run_canonicalize_one
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


def run_dataset_source_to_graph_pipeline(
    *,
    dataset_manifest: str,
    structured_checks: Sequence[StructuredCheck] = (),
    export_owl: bool = True,
    dry_run: bool = False,
    review_model: str = "gemma4:31b",
    review_timeout_seconds: int = 600,
    review_parallelism: int | None = None,
) -> int:
    repo_root = Path.cwd().resolve()
    manifest, manifest_path = _load_manifest_or_error(dataset_manifest, repo_root)
    if manifest is None:
        return 2

    run_id = utc_now_stamp().replace('-', '').replace(':', '').replace('+0000', 'Z').replace('T', 'T')
    paths = _dataset_source_to_graph_paths(manifest, run_id)
    generated_relationship_paths: list[tuple[str, str]] = []
    filtered_relationship_paths: list[str] = []
    stage_results: list[dict[str, object]] = []

    for law_unit in manifest.law_units:
        law_base = paths["base"] / law_unit.law_id
        law_base.mkdir(parents=True, exist_ok=True)
        refined_paths = law_unit.refined_markdown_paths or ()

        for refined_path in refined_paths:
            normalized_refined_path = _normalize_refined_markdown_path(refined_path)
            if dry_run:
                stage_results.append(
                    {
                        "law_id": law_unit.law_id,
                        "refined_markdown_path": refined_path,
                        "normalized_refined_markdown_path": normalized_refined_path,
                        "source_id": canonical_source_id_for_relative_path(normalized_refined_path),
                        "planned_extract_json": str((law_base / f"{Path(refined_path).stem}_extract.json").relative_to(repo_root)),
                        "planned_review_json": str((law_base / f"{Path(refined_path).stem}_review.json").relative_to(repo_root)),
                        "planned_high_conf_json": str((law_base / f"{Path(refined_path).stem}_high_conf.json").relative_to(repo_root)),
                        "planned_promoted_relationship_dir": str((paths["promoted_relationships"] / law_unit.law_id).relative_to(repo_root)),
                    }
                )
                continue

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
            source_id = canonical_source_id_for_relative_path(normalized_refined_path)
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
            review_rc, review_output = _capture_text_handler(
                lambda: run_review_relationships_ollama(
                    model=review_model,
                    timeout_seconds=review_timeout_seconds,
                    parallelism=review_parallelism,
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
        report = {
            "action": "run-dataset-source-to-graph",
            "generated_at_utc": utc_now_stamp(),
            "dataset_id": manifest.dataset_id,
            "run_id": run_id,
            "manifest_path": str(manifest_path.relative_to(repo_root)),
            "dry_run": True,
            "stage_results": stage_results,
        }
        write_json_report(paths["report"], report)
        print(json.dumps({
            "action": "run-dataset-source-to-graph",
            "dataset_id": manifest.dataset_id,
            "run_id": run_id,
            "dry_run": True,
            "pipeline_report_path": str(paths["report"].relative_to(repo_root)),
            "planned_stage_count": len(stage_results),
        }, indent=2))
        return 0

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

    report = {
        "action": "run-dataset-source-to-graph",
        "generated_at_utc": utc_now_stamp(),
        "dataset_id": manifest.dataset_id,
        "run_id": run_id,
        "manifest_path": str(manifest_path.relative_to(repo_root)),
        "derived_manifest_path": str(paths["derived_manifest"].relative_to(repo_root)),
        "generated_relationship_count": len(generated_relationship_paths),
        "filtered_relationship_count": len(filtered_relationship_paths),
        "filtered_relationship_paths": filtered_relationship_paths,
        "stage_results": stage_results,
        "graph": graph_payload,
    }
    write_json_report(paths["report"], report)

    summary = {
        "action": "run-dataset-source-to-graph",
        "dataset_id": manifest.dataset_id,
        "run_id": run_id,
        "derived_manifest_path": str(paths["derived_manifest"].relative_to(repo_root)),
        "generated_relationship_count": len(generated_relationship_paths),
        "filtered_relationship_count": len(filtered_relationship_paths),
        "pipeline_report_path": str(paths["report"].relative_to(repo_root)),
        "graph_snapshot_path": graph_payload.get("snapshot_path"),
        "graph_build_report_path": graph_payload.get("build_report_path"),
    }
    print(json.dumps(summary, indent=2))
    return 0
