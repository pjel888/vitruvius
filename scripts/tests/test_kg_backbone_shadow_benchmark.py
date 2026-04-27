from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_shadow_benchmark import run_shadow_benchmark


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "aec_mepfs_backbone"
S3_FIXTURE = FIXTURE_DIR / "valid_integration_readiness_s3.json"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_shadow_inputs(tmp_path: Path) -> dict[str, Path]:
    api_index = tmp_path / "api" / "index.ts"
    api_index.parent.mkdir(parents=True, exist_ok=True)
    api_index.write_text(
        "app.get('/v2/backbone', handler);\n"
        "app.get('/v2/backbone/taxonomy', handler);\n"
        "app.get('/v2/backbone/node/:id', handler);\n"
        "app.get('/v2/search', handler);\n"
        "app.get('/v2/sources/:source_id', handler);\n"
        "app.get('/v2/backbone/placement-qa', handler);\n"
        "app.get('/v2/backbone/evidence', handler);\n",
        encoding="utf-8",
    )

    report_root = tmp_path / "006_System-Manifests" / "aec-mepfs-backbone"
    consumer = report_root / "shadow-staging" / "TEST" / "shadow-staging-consumer-report.json"
    graph = report_root / "shadow-staging" / "TEST" / "shadow-backbone-graph.json"
    placement = report_root / "placement-qa" / "TEST" / "placement-qa-report.json"
    resolver = report_root / "resolver-qa" / "TEST" / "resolver-qa-report.json"
    parity = report_root / "parity" / "TEST" / "api-explorer-parity-report.json"
    boundary = report_root / "boundary-audit" / "TEST" / "shadow-boundary-audit-report.json"

    _write_json(consumer, {"ok": True, "run_id": "TEST"})
    _write_json(
        graph,
        {
            "counts": {"edges": 1, "max_depth": 1, "nodes": 1, "roots": 1},
            "nodes": [{"id": "VTN-DOM-1"}],
            "edges": [],
        },
    )
    _write_json(placement, {"ok": True, "summary": {"cases_passed": 1, "cases_total": 1}})
    _write_json(resolver, {"ok": True, "summary": {"cases_passed": 1, "cases_total": 1}})
    _write_json(parity, {"ok": True, "commands_passed": 1, "commands_run": 1})
    _write_json(boundary, {"ok": True, "summary": {"checks_passed": 1, "checks_total": 1}})

    return {
        "api_index": api_index,
        "consumer": consumer,
        "graph": graph,
        "placement": placement,
        "resolver": resolver,
        "parity": parity,
        "boundary": boundary,
    }


def _write_fixture(tmp_path: Path, mutation: Any) -> Path:
    payload = json.loads(S3_FIXTURE.read_text(encoding="utf-8"))
    mutation(payload)
    fixture_path = tmp_path / "fixture.json"
    fixture_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return fixture_path


def _run(tmp_path: Path, paths: dict[str, Path], fixture: Path | None = None) -> dict[str, Any]:
    fixture_path = fixture or _write_fixture(tmp_path, lambda payload: None)
    return run_shadow_benchmark(
        fixture_path,
        repo_root=tmp_path,
        run_id="TEST_BENCH",
        consumer_report_path=paths["consumer"].relative_to(tmp_path),
        shadow_graph_path=paths["graph"].relative_to(tmp_path),
        placement_qa_report_path=paths["placement"].relative_to(tmp_path),
        resolver_qa_report_path=paths["resolver"].relative_to(tmp_path),
        parity_report_path=paths["parity"].relative_to(tmp_path),
        boundary_audit_report_path=paths["boundary"].relative_to(tmp_path),
        api_index_path=paths["api_index"].relative_to(tmp_path),
    )


def test_shadow_benchmark_writes_report_for_file_backed_operations(tmp_path: Path) -> None:
    paths = _write_shadow_inputs(tmp_path)

    report = _run(tmp_path, paths)

    saved = json.loads(
        (
            tmp_path
            / "006_System-Manifests"
            / "aec-mepfs-backbone"
            / "benchmarks"
            / "TEST_BENCH"
            / "benchmark-report.json"
        ).read_text(encoding="utf-8")
    )
    assert saved == report
    assert report["ok"] is True
    assert set(report["input_file_hashes_sha256"]) == {
        "api_index",
        "boundary_audit_report",
        "consumer_report",
        "parity_report",
        "placement_qa_report",
        "resolver_qa_report",
        "shadow_graph",
    }
    assert all(len(digest) == 64 for digest in report["input_file_hashes_sha256"].values())
    assert report["repo_state"] == {
        "generated_evidence_dirty": False,
        "generated_evidence_dirty_path_count": 0,
        "git_head_commit": None,
        "source_dirty_path_count": 0,
        "source_working_tree_dirty": False,
        "working_tree_dirty": False,
    }
    assert report["benchmark_scope"] == {
        "api_server_calls": False,
        "explorer_runtime_calls": False,
        "feature_flag_cutover": False,
        "kg_rebuild": False,
        "neo4j_queries": False,
        "protected_content_ingest": False,
        "runtime_resolver_invocation": False,
        "runtime_thresholds_evaluated": False,
        "shadow_file_backed_only": True,
    }
    assert report["plan"]["repetitions"] == 5
    assert report["plan"]["runtime_threshold_disposition"] == "not_evaluated_shadow_file_backed_only"
    assert len(report["operations"]) == 5
    expected_operations = {
        "api_route_static_scan",
        "contract_validation",
        "input_hash_scan",
        "shadow_evidence_json_read",
        "shadow_graph_shape_scan",
    }
    assert {operation["name"] for operation in report["operations"]} == expected_operations
    assert report["operation_coverage"] == {
        "all_operations_ok": True,
        "all_required_operations_present": True,
        "missing_required_operations": [],
        "operations_passed": 5,
        "operations_total": 5,
        "required_operations": [
            "contract_validation",
            "shadow_evidence_json_read",
            "shadow_graph_shape_scan",
            "api_route_static_scan",
            "input_hash_scan",
        ],
        "unexpected_operations": [],
    }
    assert report["runtime_threshold_evidence"] == {
        "blocked_runtime_scope": [
            "runtime_resolver_invocation",
            "api_server_calls",
            "explorer_runtime_calls",
            "neo4j_queries",
        ],
        "declared_command_count": 3,
        "declared_threshold_count": 4,
        "declared_thresholds_evaluated": False,
        "disposition": "not_evaluated_shadow_file_backed_only",
        "future_runtime_command_count": 2,
        "future_runtime_commands_declared": [
            "future shadow resolver benchmark command",
            "future API/Explorer parity benchmark command",
        ],
        "runtime_thresholds_evaluated": False,
    }
    assert all(operation["ok"] for operation in report["operations"])
    assert all(operation["repetitions"] == 5 for operation in report["operations"])
    assert all(operation["p95_ms"] >= 0 for operation in report["operations"])
    assert any("runtime benchmark commands" in warning for warning in report["warnings"])


def test_shadow_benchmark_fails_if_resolver_route_is_mounted(tmp_path: Path) -> None:
    paths = _write_shadow_inputs(tmp_path)
    paths["api_index"].write_text(
        paths["api_index"].read_text(encoding="utf-8")
        + "app.post('/v2/resolve', handler);\n",
        encoding="utf-8",
    )

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    api_operation = next(
        operation for operation in report["operations"] if operation["name"] == "api_route_static_scan"
    )
    assert api_operation["ok"] is False
    assert any("unauthorized /v2/resolve must remain unmounted" in error for error in report["errors"])


def test_shadow_benchmark_fails_if_shadow_graph_shape_drifts(tmp_path: Path) -> None:
    paths = _write_shadow_inputs(tmp_path)
    graph = json.loads(paths["graph"].read_text(encoding="utf-8"))
    graph["nodes"] = []
    graph["counts"]["nodes"] = 0
    _write_json(paths["graph"], graph)

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert any("shadow graph must contain at least one node" in error for error in report["errors"])


def test_shadow_benchmark_fails_if_expected_preview_route_disappears(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_inputs(tmp_path)
    paths["api_index"].write_text(
        "app.get('/v2/backbone', handler);\n"
        "app.get('/v2/backbone/taxonomy', handler);\n"
        "app.get('/v2/backbone/node/:id', handler);\n"
        "app.get('/v2/search', handler);\n"
        "app.get('/v2/sources/:source_id', handler);\n",
        encoding="utf-8",
    )

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert any("missing expected preview routes" in error for error in report["errors"])


def test_shadow_benchmark_fails_when_fixture_benchmark_plan_is_invalid(
    tmp_path: Path,
) -> None:
    paths = _write_shadow_inputs(tmp_path)
    fixture = _write_fixture(
        tmp_path,
        lambda payload: payload["integration_benchmark_plan"].__setitem__("repetitions", 2),
    )

    report = _run(tmp_path, paths, fixture)

    assert report["ok"] is False
    assert report["operations"] == []
    assert any("repetitions: must be >= 3" in error for error in report["errors"])


def test_shadow_benchmark_rejects_unsafe_run_id(tmp_path: Path) -> None:
    paths = _write_shadow_inputs(tmp_path)
    fixture = _write_fixture(tmp_path, lambda payload: None)

    with pytest.raises(ValueError, match="run_id must contain only"):
        run_shadow_benchmark(
            fixture,
            repo_root=tmp_path,
            run_id="../unsafe",
            consumer_report_path=paths["consumer"].relative_to(tmp_path),
            shadow_graph_path=paths["graph"].relative_to(tmp_path),
            placement_qa_report_path=paths["placement"].relative_to(tmp_path),
            resolver_qa_report_path=paths["resolver"].relative_to(tmp_path),
            parity_report_path=paths["parity"].relative_to(tmp_path),
            boundary_audit_report_path=paths["boundary"].relative_to(tmp_path),
            api_index_path=paths["api_index"].relative_to(tmp_path),
        )


def test_shadow_benchmark_rejects_output_outside_report_root(tmp_path: Path) -> None:
    paths = _write_shadow_inputs(tmp_path)
    fixture = _write_fixture(tmp_path, lambda payload: None)

    with pytest.raises(ValueError, match="benchmark report directory"):
        run_shadow_benchmark(
            fixture,
            repo_root=tmp_path,
            run_id="TEST_BENCH",
            output_path=Path(".ai/ACTIVE_WORK.md"),
            consumer_report_path=paths["consumer"].relative_to(tmp_path),
            shadow_graph_path=paths["graph"].relative_to(tmp_path),
            placement_qa_report_path=paths["placement"].relative_to(tmp_path),
            resolver_qa_report_path=paths["resolver"].relative_to(tmp_path),
            parity_report_path=paths["parity"].relative_to(tmp_path),
            boundary_audit_report_path=paths["boundary"].relative_to(tmp_path),
            api_index_path=paths["api_index"].relative_to(tmp_path),
        )


def test_shadow_benchmark_rejects_output_for_other_run_id(tmp_path: Path) -> None:
    paths = _write_shadow_inputs(tmp_path)
    fixture = _write_fixture(tmp_path, lambda payload: None)

    with pytest.raises(ValueError, match="current benchmark run id"):
        run_shadow_benchmark(
            fixture,
            repo_root=tmp_path,
            run_id="TEST_BENCH",
            output_path=(
                Path("006_System-Manifests")
                / "aec-mepfs-backbone"
                / "benchmarks"
                / "OTHER_RUN"
                / "benchmark-report.json"
            ),
            consumer_report_path=paths["consumer"].relative_to(tmp_path),
            shadow_graph_path=paths["graph"].relative_to(tmp_path),
            placement_qa_report_path=paths["placement"].relative_to(tmp_path),
            resolver_qa_report_path=paths["resolver"].relative_to(tmp_path),
            parity_report_path=paths["parity"].relative_to(tmp_path),
            boundary_audit_report_path=paths["boundary"].relative_to(tmp_path),
            api_index_path=paths["api_index"].relative_to(tmp_path),
        )


def test_shadow_benchmark_fails_if_input_file_is_missing(tmp_path: Path) -> None:
    paths = _write_shadow_inputs(tmp_path)
    paths["boundary"].unlink()

    with pytest.raises(FileNotFoundError, match="boundary audit report not found"):
        _run(tmp_path, paths)


def test_shadow_benchmark_reports_invalid_evidence_json(tmp_path: Path) -> None:
    paths = _write_shadow_inputs(tmp_path)
    paths["parity"].write_text("{not json", encoding="utf-8")

    report = _run(tmp_path, paths)

    assert report["ok"] is False
    assert any("shadow_evidence_json_read" in error for error in report["errors"])
