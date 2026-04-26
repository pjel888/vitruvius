from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg import backbone_placement_qa as placement_qa
from vitruvius.kg.backbone_contracts import BackboneContractReport
from vitruvius.kg.backbone_placement_qa import run_placement_qa_fixture


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "aec_mepfs_backbone"
S2_FIXTURE = FIXTURE_DIR / "valid_readiness_s2.json"


def _write_fixture(tmp_path: Path, mutation: Any) -> Path:
    payload = json.loads(S2_FIXTURE.read_text(encoding="utf-8"))
    mutation(payload)
    fixture_path = tmp_path / "fixture.json"
    fixture_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return fixture_path


def test_placement_qa_writes_report_for_valid_authoring_cases(tmp_path: Path) -> None:
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/placement-qa/TEST_RUN"
    ) / "placement-qa-report.json"

    report = run_placement_qa_fixture(
        S2_FIXTURE,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_path=output_path,
    )

    saved = json.loads((tmp_path / output_path).read_text(encoding="utf-8"))
    assert saved == report
    assert report["ok"] is True
    assert report["run_id"] == "TEST_RUN"
    assert report["summary"]["cases_total"] == 3
    assert report["summary"]["cases_passed"] == 3
    assert report["summary"]["auto_accept_cases"] == 1
    assert report["summary"]["case_type_counts"] == {
        "l1_human_review": 1,
        "l3_leaf_auto_accept": 1,
        "legacy_label_alias": 1,
    }
    assert report["summary"]["proposed_by_counts"] == {"ai": 1, "human": 2}
    assert report["summary"]["workflow_counts"] == {
        "LD-8 PlacementAssertion": 1,
        "legacy_migration_workbook": 1,
        "steward_review": 1,
    }
    assert report["summary"]["required_coverage"] == {
        "case_id_present": True,
        "input_context_present": True,
        "l1_l2_human_review": True,
        "l3_l4_ld8_auto_accept": True,
        "ld8_auto_accept_rationale": True,
        "legacy_label_alias": True,
        "legacy_label_rationale": True,
        "owner_present": True,
        "proposal_level_present": True,
        "review_status_candidate": True,
        "source_evidence_ids_present": True,
    }
    assert report["safety_boundaries"] == {
        "canonical_content_admission": False,
        "explorer_default_adoption": False,
        "feature_flag_cutover": False,
        "file_backed_only": True,
        "kg_rebuild": False,
        "live_neo4j_writes": False,
        "protected_content_ingest": False,
        "shadow_only": True,
    }


def test_placement_qa_contract_gates_invalid_auto_accept_threshold(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["authoring_migration_cases"][0].__setitem__(
            "confidence",
            0.91,
        ),
    )

    report = run_placement_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is False
    assert report["ok"] is False
    assert report["summary"]["cases_total"] == 0
    assert report["summary"]["cases_failed"] == 0
    assert any("auto_accept requires confidence >= 0.92" in error for error in report["errors"])
    assert "placement QA skipped because readiness fixture failed validation" in report["warnings"]


def test_placement_qa_runner_keeps_independent_auto_accept_threshold_guard(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["authoring_migration_cases"][0].__setitem__(
            "confidence",
            0.91,
        ),
    )

    monkeypatch.setattr(
        placement_qa,
        "validate_backbone_contract_file",
        lambda _fixture: BackboneContractReport(ok=True),
    )

    report = run_placement_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert report["summary"]["cases_total"] == 3
    assert report["summary"]["cases_failed"] == 1
    assert any("auto_accept requires confidence >= 0.92" in error for error in report["errors"])


def test_placement_qa_catches_runner_specific_auto_accept_queue_drift(
    tmp_path: Path,
) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["authoring_migration_cases"][0]["expected_output"].__setitem__(
            "review_queue",
            "manual_review",
        ),
    )

    report = run_placement_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert report["summary"]["cases_total"] == 3
    assert report["summary"]["cases_failed"] == 1
    assert any(
        "auto_accept cases must route to auto_accept_sampling_audit" in error
        for error in report["errors"]
    )


def test_placement_qa_catches_missing_input_context(tmp_path: Path) -> None:
    def mutate(payload: dict[str, Any]) -> None:
        payload["authoring_migration_cases"][0]["input"].pop("label")

    fixture_path = _write_fixture(tmp_path, mutate)

    report = run_placement_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "authoring migration cases must carry label or legacy_label input context" in error
        for error in report["errors"]
    )


def test_placement_qa_catches_blank_source_evidence_id(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["authoring_migration_cases"][0].__setitem__(
            "source_evidence",
            [""],
        ),
    )

    report = run_placement_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "authoring migration cases must carry non-empty source_evidence IDs" in error
        for error in report["errors"]
    )


def test_placement_qa_catches_non_candidate_review_status(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["authoring_migration_cases"][0].__setitem__(
            "review_status",
            "accepted",
        ),
    )

    report = run_placement_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "authoring migration cases must remain candidate review_status" in error
        for error in report["errors"]
    )


def test_placement_qa_catches_auto_accept_rationale_drift(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["authoring_migration_cases"][0].__setitem__(
            "rationale",
            "A high-confidence placement is returned.",
        ),
    )

    report = run_placement_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "auto_accept cases must explain LD-8 auto-accept rationale" in error
        for error in report["errors"]
    )


def test_placement_qa_catches_legacy_alias_rationale_drift(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["authoring_migration_cases"][2].__setitem__(
            "rationale",
            "A migration workbook row is reviewed.",
        ),
    )

    report = run_placement_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["contract_validation"]["ok"] is True
    assert report["ok"] is False
    assert any(
        "legacy alias cases must explain alias and canonical label handling" in error
        for error in report["errors"]
    )


def test_placement_qa_fails_when_l1_ai_authoring_is_present(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["authoring_migration_cases"][1].__setitem__(
            "proposed_by",
            "ai",
        ),
    )

    report = run_placement_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["ok"] is False
    assert any("AI-authored L1 changes are blocked" in error for error in report["errors"])
    assert report["summary"]["cases_total"] == 0


def test_placement_qa_requires_legacy_alias_coverage(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload.__setitem__(
            "authoring_migration_cases",
            [
                case
                for case in payload["authoring_migration_cases"]
                if case["case_type"] != "legacy_label_alias"
            ],
        ),
    )

    report = run_placement_qa_fixture(fixture_path, repo_root=tmp_path, run_id="TEST_RUN")

    assert report["ok"] is False
    assert report["summary"]["cases_total"] == 2
    assert any(
        "missing required QA coverage" in error and "legacy_label_alias" in error
        for error in report["errors"]
    )


def test_placement_qa_rejects_unsafe_run_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="run_id must contain only"):
        run_placement_qa_fixture(S2_FIXTURE, repo_root=tmp_path, run_id="../unsafe")


def test_placement_qa_rejects_output_outside_report_root(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="placement QA report directory"):
        run_placement_qa_fixture(
            S2_FIXTURE,
            repo_root=tmp_path,
            run_id="TEST_RUN",
            output_path=Path(".ai/ACTIVE_WORK.md"),
        )
