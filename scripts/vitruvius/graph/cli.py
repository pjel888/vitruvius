from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .builder import build_snapshot
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


def _integrity_payload(report) -> dict:
    return {
        "passed": report.passed,
        "warning_count": report.warning_count,
        "error_count": report.error_count,
        "findings": [asdict(f) for f in report.findings],
    }


def run_build_graph(*, dry_run: bool = False) -> int:
    repo_root = _repo_root()
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


def run_query_graph(*, from_id: str, to_id: str, max_depth: int = 3) -> int:
    repo_root = _repo_root()
    in_path = repo_root / _SNAPSHOT_RELPATH
    if not in_path.exists():
        print(json.dumps({
            "error": "no snapshot found",
            "expected_path": str(_SNAPSHOT_RELPATH),
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
    print(json.dumps(payload, indent=2))
    return 0 if paths else 1


def run_export_graph_snapshot(*, fmt: str = "json") -> int:
    repo_root = _repo_root()
    in_path = repo_root / _SNAPSHOT_RELPATH
    if not in_path.exists():
        print(json.dumps({
            "error": "no snapshot found",
            "expected_path": str(_SNAPSHOT_RELPATH),
            "hint": "run `build-graph` first",
        }, indent=2))
        return 2
    if fmt != "json":
        print(json.dumps({"error": f"unsupported format: {fmt}"}, indent=2))
        return 2
    print(in_path.read_text(encoding="utf-8"), end="")
    return 0
