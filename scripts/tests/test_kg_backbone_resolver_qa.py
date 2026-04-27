from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_resolver_qa import run_resolver_qa_fixture


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "aec_mepfs_backbone"
S2_FIXTURE = FIXTURE_DIR / "valid_readiness_s2.json"


def _write_fixture(tmp_path: Path, mutation: Any) -> Path:
    payload = json.loads(S2_FIXTURE.read_text(encoding="utf-8"))
    mutation(payload)
    fixture_path = tmp_path / "fixture.json"
    fixture_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return fixture_path


def test_resolver_qa_writes_report_for_valid_golden_cases(tmp_path: Path) -> None:
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/resolver-qa/TEST_RUN"
    ) / "resolver-qa-report.json"

    report = run_resolver_qa_fixture(
        S2_FIXTURE,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_path=output_path,
    )

    saved = json.loads((tmp_path / output_path).read_text(encoding="utf-8"))
    assert saved == report
    assert report["ok"] is True
    assert report["run_id"] == "TEST_RUN"
    assert report["summary"]["cases_total"] == 7
    assert report["summary"]["cases_passed"] == 7
    assert report["summary"]["result_type_counts"] == {
        "composed": 1,
        "conflict": 1,
        "none": 1,
        "single_value": 4,
    }
    assert report["summary"]["jurisdiction_counts"] == {
        "GLOBAL": 1,
        "PH": 3,
        "PH-EXAMPLE-LGU": 1,
        "PH-QUEZON-CITY": 1,
        "PH-UNMODELED": 1,
    }
    assert report["summary"]["asset_context_counts"] == {
        "domain_classification": 1,
        "equal_force_incompatible": 1,
        "jurisdiction_crosswalk": 1,
        "national_and_local_compatible": 1,
        "no_overlay": 1,
        "overlay_metadata": 1,
        "public_building": 1,
    }
    assert report["summary"]["required_coverage"] == {
        "case_id_present": True,
        "composed_compatible_rationale": True,
        "composed_deterministic": True,
        "conflict_incompatible_rationale": True,
        "conflict_review_required": True,
        "effective_date_present": True,
        "expected_node_refs_present": True,
        "fallback_reason_present": True,
        "jurisdiction_present": True,
        "none_absence_rationale": True,
        "none_insufficient": True,
        "query_asset_context_present": True,
        "query_context_ids_static_contract": True,
        "query_discipline_filters_static_contract": True,
        "query_text_present": True,
        "source_evidence_traceable": True,
        "single_value_deterministic": True,
        "trace_requested_boolean": True,
        "trace_safe_rationale_present": True,
    }
    assert report["error_summary"]["cases_total"] == 5
    assert report["error_summary"]["cases_passed"] == 5
    assert report["error_summary"]["error_type_counts"] == {
        "blocked_runtime_route": 1,
        "deterministic_no_result": 1,
        "invalid_input": 1,
        "malformed_request": 1,
        "missing_fixture_artifact": 1,
    }
    assert all(report["error_summary"]["required_coverage"].values())
    assert report["contract_surface"]["request_shape"] == {
        "deterministic_trace_request_flag": True,
        "optional_context_ids": True,
        "optional_discipline_filters": True,
        "query_text": True,
    }
    assert report["contract_surface"]["error_shape"]["blocked_runtime_route"] is True
    assert report["api_route_status"] == {
        "checked": False,
        "defaultOffResolveRouteDeclared": False,
        "defaultOffTraceRouteDeclared": False,
        "path": "api/index.ts",
        "reason": "api index file not present under repo root",
        "resolverRoutePolicy": "absent",
        "resolveRouteDeclared": False,
        "resolveRouteMounted": False,
        "traceRouteDeclared": False,
        "traceRouteMounted": False,
    }
    assert report["safety_boundaries"] == {
        "canonical_content_admission": False,
        "explorer_default_adoption": False,
        "feature_flag_cutover": False,
        "file_backed_only": True,
        "kg_rebuild": False,
        "live_neo4j_writes": False,
        "live_resolver_invocation": False,
        "llm_hot_path": False,
        "protected_content_ingest": False,
        "shadow_only": True,
    }


def test_resolver_qa_catches_conflict_confidence_drift(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["resolver_golden_cases"][2].__setitem__(
            "expected_confidence",
            "deterministic",
        ),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert report["summary"]["cases_total"] == 7
    assert report["summary"]["cases_failed"] == 1
    assert any("conflict cases must require review" in error for error in report["errors"])


def test_resolver_qa_catches_none_confidence_drift(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["resolver_golden_cases"][3].__setitem__(
            "expected_confidence",
            "review_required",
        ),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert report["summary"]["cases_failed"] == 1
    assert any("none cases must be insufficient" in error for error in report["errors"])


def test_resolver_qa_requires_concept_id(tmp_path: Path) -> None:
    def mutate(payload: dict[str, Any]) -> None:
        payload["resolver_golden_cases"][0]["query"].pop("concept_id")

    fixture_path = _write_fixture(tmp_path, mutate)

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "resolver golden cases must identify a concept_id" in error
        for error in report["errors"]
    )


def test_resolver_qa_requires_case_id(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["resolver_golden_cases"][0].__setitem__("case_id", ""),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is False
    assert report["ok"] is False
    assert any(
        "resolver_golden_cases[0].case_id: required field missing" in error
        for error in report["errors"]
    )
    assert "resolver QA skipped because readiness fixture failed validation" in report["warnings"]


def test_resolver_qa_requires_asset_context(tmp_path: Path) -> None:
    def mutate(payload: dict[str, Any]) -> None:
        payload["resolver_golden_cases"][0]["query"].pop("asset_context")

    fixture_path = _write_fixture(tmp_path, mutate)

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "resolver golden cases must identify query.asset_context" in error
        for error in report["errors"]
    )


def test_resolver_qa_requires_query_text(tmp_path: Path) -> None:
    def mutate(payload: dict[str, Any]) -> None:
        payload["resolver_golden_cases"][0]["query"].pop("text")

    fixture_path = _write_fixture(tmp_path, mutate)

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is False
    assert report["ok"] is False
    assert any(
        "resolver_golden_cases[0].query.text: required field missing" in error
        for error in report["errors"]
    )


def test_resolver_qa_requires_static_node_refs_for_non_none(tmp_path: Path) -> None:
    def mutate(payload: dict[str, Any]) -> None:
        payload["resolver_golden_cases"][0]["expected_node_refs"] = []

    fixture_path = _write_fixture(tmp_path, mutate)

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "resolver golden cases must carry canonical expected_node_refs" in error
        for error in report["errors"]
    )


def test_resolver_qa_requires_jurisdiction(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["resolver_golden_cases"][0].__setitem__(
            "jurisdiction",
            "",
        ),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is False
    assert report["ok"] is False
    assert any(
        "resolver_golden_cases[0].jurisdiction: required field missing" in error
        for error in report["errors"]
    )
    assert "resolver QA skipped because readiness fixture failed validation" in report["warnings"]


def test_resolver_qa_requires_effective_date(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["resolver_golden_cases"][0].__setitem__(
            "effective_date",
            "",
        ),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is False
    assert report["ok"] is False
    assert any(
        "resolver_golden_cases[0].effective_date: required field missing" in error
        for error in report["errors"]
    )
    assert "resolver QA skipped because readiness fixture failed validation" in report["warnings"]


def test_resolver_qa_rejects_blank_source_evidence_id(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["resolver_golden_cases"][0].__setitem__(
            "source_evidence",
            ["   "],
        ),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "resolver golden cases must carry non-empty source_evidence IDs" in error
        for error in report["errors"]
    )


def test_resolver_qa_catches_composed_rationale_drift(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["resolver_golden_cases"][1].__setitem__(
            "rationale",
            "Two values are returned.",
        ),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "composed cases must explain compatible composed requirements" in error
        for error in report["errors"]
    )


def test_resolver_qa_catches_conflict_rationale_drift(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["resolver_golden_cases"][2].__setitem__(
            "rationale",
            "A decision is deferred.",
        ),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "conflict cases must explain the incompatible equal-force condition" in error
        for error in report["errors"]
    )


def test_resolver_qa_catches_none_rationale_drift(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["resolver_golden_cases"][3].__setitem__(
            "rationale",
            "The result is deferred.",
        ),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "none cases must explain the missing or unmodeled applicability" in error
        for error in report["errors"]
    )


def test_resolver_qa_requires_result_type_coverage(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload.__setitem__(
            "resolver_golden_cases",
            [
                case
                for case in payload["resolver_golden_cases"]
                if case["expected_result_type"] != "conflict"
            ],
        ),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["ok"] is False
    assert report["summary"]["cases_total"] == 0
    assert any("missing result-type coverage (conflict)" in error for error in report["errors"])
    assert "resolver QA skipped because readiness fixture failed validation" in report["warnings"]


def test_resolver_qa_requires_error_case_coverage(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload.__setitem__(
            "resolver_error_cases",
            [
                case
                for case in payload["resolver_error_cases"]
                if case["expected_error_type"] != "blocked_runtime_route"
            ],
        ),
    )

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["ok"] is False
    assert report["summary"]["cases_total"] == 0
    assert any(
        "missing error-type coverage (blocked_runtime_route)" in error
        for error in report["errors"]
    )
    assert "resolver QA skipped because readiness fixture failed validation" in report["warnings"]


def test_resolver_qa_rejects_malformed_error_request(tmp_path: Path) -> None:
    def mutate(payload: dict[str, Any]) -> None:
        payload["resolver_error_cases"][1]["request"]["context_ids"] = ["VTN-CON-0000002"]

    fixture_path = _write_fixture(tmp_path, mutate)

    report = run_resolver_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "malformed request cases must model malformed context_ids" in error
        for error in report["errors"]
    )


def test_resolver_qa_rejects_unsafe_run_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="run_id must contain only"):
        run_resolver_qa_fixture(S2_FIXTURE, repo_root=tmp_path, run_id="../unsafe")


def test_resolver_qa_rejects_output_outside_report_root(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="resolver QA report directory"):
        run_resolver_qa_fixture(
            S2_FIXTURE,
            repo_root=tmp_path,
            run_id="TEST_RUN",
            output_path=Path(".ai/ACTIVE_WORK.md"),
        )


def test_resolver_qa_fails_if_resolver_api_route_is_mounted(tmp_path: Path) -> None:
    api_dir = tmp_path / "api"
    api_dir.mkdir()
    (api_dir / "index.ts").write_text(
        "app.post( '/v2/resolve', handler);\n"
        "app.get('/v2/resolve/trace/:trace_id', handler);\n",
        encoding="utf-8",
    )

    report = run_resolver_qa_fixture(S2_FIXTURE, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["ok"] is False
    assert report["api_route_status"]["checked"] is True
    assert report["api_route_status"]["resolveRouteMounted"] is True
    assert report["api_route_status"]["traceRouteMounted"] is True
    assert any("unauthorized /v2/resolve routes must remain unmounted" in error for error in report["errors"])


def test_resolver_qa_allows_default_off_guarded_resolver_api_routes(tmp_path: Path) -> None:
    api_dir = tmp_path / "api"
    api_dir.mkdir()
    (api_dir / "index.ts").write_text(
        "if (isAecMepfsResolverRuntimeEnabled()) {\n"
        "  app.post('/v2/resolve', handler);\n"
        "  app.get('/v2/resolve/trace/:trace_id', handler);\n"
        "}\n"
        "app.get('/v2/backbone', handler);\n"
        "app.get('/v2/backbone/taxonomy', handler);\n"
        "app.get('/v2/backbone/node/:id', handler);\n"
        "app.get('/v2/search', handler);\n"
        "app.get('/v2/sources/:source_id', handler);\n"
        "app.get('/v2/backbone/placement-qa', handler);\n"
        "app.get('/v2/backbone/evidence', handler);\n",
        encoding="utf-8",
    )

    report = run_resolver_qa_fixture(S2_FIXTURE, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["ok"] is True
    assert report["api_route_status"]["checked"] is True
    assert report["api_route_status"]["resolveRouteDeclared"] is True
    assert report["api_route_status"]["defaultOffResolveRouteDeclared"] is True
    assert report["api_route_status"]["resolveRouteMounted"] is False
    assert report["api_route_status"]["traceRouteMounted"] is False
    assert report["preview_route_status"]["resolveRouteDeclared"] is True
    assert report["preview_route_status"]["defaultOffResolveRouteDeclared"] is True
