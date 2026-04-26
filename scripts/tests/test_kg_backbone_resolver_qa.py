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
    assert report["summary"]["cases_total"] == 4
    assert report["summary"]["cases_passed"] == 4
    assert report["summary"]["result_type_counts"] == {
        "composed": 1,
        "conflict": 1,
        "none": 1,
        "single_value": 1,
    }
    assert report["summary"]["required_coverage"] == {
        "composed_deterministic": True,
        "conflict_review_required": True,
        "none_insufficient": True,
        "single_value_deterministic": True,
    }
    assert report["api_route_status"] == {
        "checked": False,
        "path": "api/index.ts",
        "reason": "api index file not present under repo root",
        "resolveRouteMounted": False,
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
    assert report["summary"]["cases_total"] == 4
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
    assert any("/v2/resolve routes must remain unmounted" in error for error in report["errors"])
