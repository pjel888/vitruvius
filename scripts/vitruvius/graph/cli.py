from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .builder import build_snapshot
from .dataset_manifest import (
    DatasetManifestError,
    build_run_paths,
    dataset_build_report,
    load_dataset_manifest,
    provenance_for_snapshot,
    selected_concept_paths,
    selected_relationship_paths,
    selected_source_paths,
    snapshot_metadata,
    write_json_report,
)
from .integrity import check_integrity
from .snapshot import read_snapshot, write_snapshot
from .traverse import evidence_joined_paths


_CANONICAL_RELPATH = Path("003_Canonical-Knowledge-Layer") / "shared"
_SNAPSHOT_RELPATH = (
    Path("005_Operational-Intelligence-Layer") / "graph" / "latest_graph_snapshot.json"
)
_INTEGRITY_RELPATH = (
    Path("005_Operational-Intelligence-Layer")
    / "graph"
    / "latest_graph_integrity_report.json"
)


def _repo_root() -> Path:
    return Path.cwd()


def _utc_run_id() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _resolve_snapshot_path(snapshot_path: str | None) -> tuple[Path, str]:
    if snapshot_path is None:
        return _repo_root() / _SNAPSHOT_RELPATH, str(_SNAPSHOT_RELPATH)
    path = Path(snapshot_path)
    if not path.is_absolute():
        path = _repo_root() / path
    try:
        display_path = str(path.relative_to(_repo_root()))
    except ValueError:
        display_path = str(path)
    return path, display_path


def _integrity_payload(report) -> dict:
    return {
        "passed": report.passed,
        "warning_count": report.warning_count,
        "error_count": report.error_count,
        "findings": [asdict(f) for f in report.findings],
    }


def run_build_graph(*, dry_run: bool = False, dataset_manifest: str | None = None) -> int:
    repo_root = _repo_root()
    if dataset_manifest is not None:
        manifest_path = Path(dataset_manifest)
        if not manifest_path.is_absolute():
            manifest_path = repo_root / manifest_path
        try:
            manifest = load_dataset_manifest(manifest_path, repo_root)
        except DatasetManifestError as exc:
            print(json.dumps({"error": str(exc)}, indent=2))
            return 2

        run_id = _utc_run_id()
        out_paths = build_run_paths(manifest, repo_root=repo_root, run_id=run_id)
        metadata = snapshot_metadata(
            manifest,
            repo_root=repo_root,
            run_id=run_id,
            snapshot_rel=out_paths.snapshot_rel,
            integrity_rel=out_paths.integrity_rel,
        )
        snapshot = build_snapshot(
            repo_root / _CANONICAL_RELPATH,
            source_paths=selected_source_paths(manifest),
            concept_paths=selected_concept_paths(manifest),
            relationship_paths=selected_relationship_paths(manifest),
            metadata=metadata,
        )
        report = check_integrity(snapshot)
        integrity_payload = _integrity_payload(report)
        summary = dataset_build_report(
            manifest,
            repo_root=repo_root,
            run_id=run_id,
            dry_run=dry_run,
            snapshot=snapshot,
            integrity_payload=integrity_payload,
            snapshot_rel=out_paths.snapshot_rel,
            integrity_rel=out_paths.integrity_rel,
        )

        if not dry_run:
            write_snapshot(snapshot, out_paths.snapshot_path)
            write_json_report(
                out_paths.integrity_path,
                {
                    "artifact_metadata": snapshot.metadata,
                    "integrity": integrity_payload,
                },
            )
            write_json_report(out_paths.build_report_path, summary)
            summary["build_report_path"] = out_paths.build_report_rel

        print(json.dumps(summary, indent=2))
        return 0 if report.passed else 1

    canonical_root = repo_root / _CANONICAL_RELPATH
    snapshot = build_snapshot(canonical_root)
    report = check_integrity(snapshot)
    integrity_payload = _integrity_payload(report)

    summary = {
        "action": "build-graph",
        "dry_run": dry_run,
        "node_count": snapshot.node_count,
        "edge_count": snapshot.edge_count,
        "integrity": integrity_payload,
    }

    if not dry_run:
        out_path = repo_root / _SNAPSHOT_RELPATH
        write_snapshot(snapshot, out_path)
        integrity_out = repo_root / _INTEGRITY_RELPATH
        integrity_out.parent.mkdir(parents=True, exist_ok=True)
        integrity_out.write_text(
            json.dumps(integrity_payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        summary["snapshot_path"] = str(_SNAPSHOT_RELPATH)
        summary["integrity_report_path"] = str(_INTEGRITY_RELPATH)

    print(json.dumps(summary, indent=2))
    return 0 if report.passed else 1


def run_query_graph(
    *,
    from_id: str,
    to_id: str,
    max_depth: int = 3,
    snapshot_path: str | None = None,
) -> int:
    in_path, display_path = _resolve_snapshot_path(snapshot_path)
    if not in_path.exists():
        print(json.dumps({
            "error": "no snapshot found",
            "expected_path": display_path,
            "hint": "run `build-graph` first",
        }, indent=2))
        return 2
    snapshot = read_snapshot(in_path)
    paths = evidence_joined_paths(
        snapshot, from_id, to_id, max_depth=max_depth
    )
    payload = {
        "from": from_id,
        "to": to_id,
        "max_depth": max_depth,
        "path_count": len(paths),
        "paths": [
            [asdict(edge) for edge in path]
            for path in paths
        ],
    }
    provenance = provenance_for_snapshot(snapshot, snapshot_path=display_path)
    if provenance is not None:
        payload["snapshot_provenance"] = provenance
    print(json.dumps(payload, indent=2))
    return 0 if paths else 1


def run_export_graph_snapshot(*, fmt: str = "json", snapshot_path: str | None = None) -> int:
    in_path, display_path = _resolve_snapshot_path(snapshot_path)
    if not in_path.exists():
        print(json.dumps({
            "error": "no snapshot found",
            "expected_path": display_path,
            "hint": "run `build-graph` first",
        }, indent=2))
        return 2
    if fmt != "json":
        print(json.dumps({"error": f"unsupported format: {fmt}"}, indent=2))
        return 2
    print(in_path.read_text(encoding="utf-8"), end="")
    return 0
