from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .graph.cli import run_build_graph
from .graph.dataset_manifest import DatasetManifestError, load_dataset_manifest, write_json_report
from .ontology.cli import run_export_graph_owl
from .query.cli import run_query_structured
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
    manifest_path = Path(dataset_manifest)
    if not manifest_path.is_absolute():
        manifest_path = repo_root / manifest_path
    try:
        manifest = load_dataset_manifest(manifest_path, repo_root)
    except DatasetManifestError as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
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
        "run_id": run_id,
        "snapshot_path": build_payload["snapshot_path"],
        "build_report_path": build_payload.get("build_report_path"),
        "pipeline_report_path": str(report_path.relative_to(repo_root)),
        "owl_path": owl_payload["path"] if owl_payload else None,
        "structured_check_count": len(check_results),
    }
    print(json.dumps(summary, indent=2))
    return 0
