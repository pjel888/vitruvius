from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from vitruvius.kg.backbone_parity_runner import (
    CommandExecution,
    run_parity_fixture,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "aec_mepfs_backbone"
S3_FIXTURE = FIXTURE_DIR / "valid_integration_readiness_s3.json"
CASE_FIXTURE = FIXTURE_DIR / "api-explorer-parity-cases.json"
EXPECTED_PARITY_COMMAND_COUNT = 6


def _executor(exit_codes: list[int]) -> Any:
    calls: list[str] = []

    def run(command: str, cwd: Path, timeout_seconds: int) -> CommandExecution:
        del cwd
        del timeout_seconds
        calls.append(command)
        exit_code = exit_codes[len(calls) - 1]
        return CommandExecution(
            command=command,
            exit_code=exit_code,
            duration_seconds=0.01,
            stdout=f"stdout for {command}",
            stderr="" if exit_code == 0 else "failure",
        )

    run.calls = calls
    return run


def _write_fixture(tmp_path: Path, mutation: Any) -> Path:
    payload = json.loads(S3_FIXTURE.read_text(encoding="utf-8"))
    mutation(payload)
    fixture_path = tmp_path / "fixture.json"
    fixture_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return fixture_path


def _prepare_repo_root(tmp_path: Path, case_mutation: Any | None = None) -> Path:
    payload = json.loads(CASE_FIXTURE.read_text(encoding="utf-8"))
    if case_mutation is not None:
        case_mutation(payload)

    target_dir = tmp_path / "scripts" / "tests" / "fixtures" / "aec_mepfs_backbone"
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "api-explorer-parity-cases.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    return tmp_path


def test_parity_runner_writes_report_for_successful_commands(tmp_path: Path) -> None:
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/parity/TEST_RUN"
    ) / "api-explorer-parity-report.json"
    executor = _executor([0] * EXPECTED_PARITY_COMMAND_COUNT)

    report = run_parity_fixture(
        S3_FIXTURE,
        repo_root=_prepare_repo_root(tmp_path),
        run_id="TEST_RUN",
        output_path=output_path,
        executor=executor,
    )

    saved = json.loads((tmp_path / output_path).read_text(encoding="utf-8"))
    assert report == saved
    assert report["ok"] is True
    assert report["run_id"] == "TEST_RUN"
    assert report["commands_run"] == EXPECTED_PARITY_COMMAND_COUNT
    assert report["commands_passed"] == EXPECTED_PARITY_COMMAND_COUNT
    assert report["cases_declared"] == len(report["case_results"])
    assert report["cases_passed"] == report["cases_declared"]
    assert report["surfaces"] == ["v1", "v2"]
    assert all(result["passed"] for result in report["command_results"])
    assert all(result["passed"] for result in report["case_results"])
    assert executor.calls == report["commands_declared"]


def test_parity_runner_fails_report_when_command_fails(tmp_path: Path) -> None:
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/parity/TEST_RUN"
    ) / "api-explorer-parity-report.json"

    report = run_parity_fixture(
        S3_FIXTURE,
        repo_root=_prepare_repo_root(tmp_path),
        run_id="TEST_RUN",
        output_path=output_path,
        executor=_executor([0, 1, 0, 0, 0, 0]),
    )

    assert report["ok"] is False
    assert report["commands_run"] == EXPECTED_PARITY_COMMAND_COUNT
    assert report["commands_passed"] == EXPECTED_PARITY_COMMAND_COUNT - 1
    assert report["cases_passed"] < report["cases_declared"]
    assert any(error.startswith("command failed:") for error in report["errors"])


def test_parity_runner_skips_commands_when_fixture_validation_fails(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload.pop("integration_parity_runner_plan"),
    )
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/parity/TEST_RUN"
    ) / "api-explorer-parity-report.json"
    executor = _executor([0] * EXPECTED_PARITY_COMMAND_COUNT)

    report = run_parity_fixture(
        fixture_path,
        repo_root=_prepare_repo_root(tmp_path),
        run_id="TEST_RUN",
        output_path=output_path,
        executor=executor,
    )

    assert report["ok"] is False
    assert report["commands_run"] == 0
    assert executor.calls == []
    assert (
        "integration_parity_runner_plan: required when integration readiness sections "
        "are present"
    ) in report["errors"]


def test_parity_runner_uses_fixture_report_path_with_run_id(tmp_path: Path) -> None:
    report = run_parity_fixture(
        S3_FIXTURE,
        repo_root=_prepare_repo_root(tmp_path),
        run_id="UNIT_SAFE_RUN",
        executor=_executor([0] * EXPECTED_PARITY_COMMAND_COUNT),
    )

    report_path = Path(report["report_path"])
    assert report_path == Path(
        "006_System-Manifests/aec-mepfs-backbone/parity"
    ) / "UNIT_SAFE_RUN" / "api-explorer-parity-report.json"
    assert (tmp_path / report_path).is_file()


def test_parity_runner_rejects_unsafe_run_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="run_id must contain only"):
        run_parity_fixture(
            S3_FIXTURE,
            repo_root=_prepare_repo_root(tmp_path),
            run_id="../unsafe",
            output_path=Path(
                "006_System-Manifests/aec-mepfs-backbone/parity/TEST_RUN"
            ) / "api-explorer-parity-report.json",
            executor=_executor([0] * EXPECTED_PARITY_COMMAND_COUNT),
        )


def test_parity_runner_rejects_output_outside_parity_report_root(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="parity report directory"):
        run_parity_fixture(
            S3_FIXTURE,
            repo_root=_prepare_repo_root(tmp_path),
            run_id="TEST_RUN",
            output_path=Path(".ai/ACTIVE_WORK.md"),
            executor=_executor([0] * EXPECTED_PARITY_COMMAND_COUNT),
        )


def test_parity_runner_requires_run_scoped_report_path(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="current parity run id"):
        run_parity_fixture(
            S3_FIXTURE,
            repo_root=_prepare_repo_root(tmp_path),
            run_id="TEST_RUN",
            output_path=Path(
                "006_System-Manifests/aec-mepfs-backbone/parity"
            ) / "api-explorer-parity-report.json",
            executor=_executor([0] * EXPECTED_PARITY_COMMAND_COUNT),
        )


def test_parity_runner_rejects_mismatched_output_run_id(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="current parity run id"):
        run_parity_fixture(
            S3_FIXTURE,
            repo_root=_prepare_repo_root(tmp_path),
            run_id="TEST_RUN",
            output_path=Path(
                "006_System-Manifests/aec-mepfs-backbone/parity/OTHER_RUN"
            ) / "api-explorer-parity-report.json",
            executor=_executor([0] * EXPECTED_PARITY_COMMAND_COUNT),
        )


def test_parity_runner_rejects_unknown_default_command(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["integration_parity_runner_plan"].__setitem__(
            "commands",
            ["unknown parity command"],
        ),
    )
    repo_root = _prepare_repo_root(
        tmp_path,
        lambda payload: [
            case.__setitem__("covered_by_command", "unknown parity command")
            for case in payload["api_explorer_parity_cases"]
        ],
    )

    report = run_parity_fixture(
        fixture_path,
        repo_root=repo_root,
        run_id="TEST_RUN",
        output_path=Path(
            "006_System-Manifests/aec-mepfs-backbone/parity/TEST_RUN"
        ) / "api-explorer-parity-report.json",
    )

    assert report["ok"] is False
    assert report["commands_run"] == 1
    assert "command failed: unknown parity command" in report["errors"]
    assert (
        report["command_results"][0]["stderr_tail"]
        == "command is not in the allowed parity command registry"
    )


def test_parity_runner_requires_cases_fixture(tmp_path: Path) -> None:
    fixture_path = _write_fixture(
        tmp_path,
        lambda payload: payload["integration_parity_runner_plan"].__setitem__(
            "fixtures_path",
            "scripts/tests/fixtures/aec_mepfs_backbone/missing-cases.json",
        ),
    )
    executor = _executor([0] * EXPECTED_PARITY_COMMAND_COUNT)

    report = run_parity_fixture(
        fixture_path,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_path=Path(
            "006_System-Manifests/aec-mepfs-backbone/parity/TEST_RUN"
        ) / "api-explorer-parity-report.json",
        executor=executor,
    )

    assert report["ok"] is False
    assert report["commands_run"] == 0
    assert executor.calls == []
    assert any("fixtures_path: file not found" in error for error in report["errors"])


def test_parity_runner_preserves_report_when_cases_fixture_is_invalid_json(
    tmp_path: Path,
) -> None:
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/parity/TEST_RUN"
    ) / "api-explorer-parity-report.json"
    target_dir = tmp_path / "scripts" / "tests" / "fixtures" / "aec_mepfs_backbone"
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "api-explorer-parity-cases.json").write_text("{not-json", encoding="utf-8")
    executor = _executor([0] * EXPECTED_PARITY_COMMAND_COUNT)

    report = run_parity_fixture(
        S3_FIXTURE,
        repo_root=tmp_path,
        run_id="TEST_RUN",
        output_path=output_path,
        executor=executor,
    )

    saved = json.loads((tmp_path / output_path).read_text(encoding="utf-8"))
    assert saved == report
    assert report["ok"] is False
    assert report["commands_run"] == 0
    assert executor.calls == []
    assert any("api_explorer_parity_cases_file: failed to load" in error for error in report["errors"])


def test_parity_runner_requires_required_case_categories(tmp_path: Path) -> None:
    def remove_required_category(payload: dict[str, Any]) -> None:
        payload["api_explorer_parity_cases"] = [
            case
            for case in payload["api_explorer_parity_cases"]
            if case["parity_category"] != "invalid_node_id"
        ]

    report = run_parity_fixture(
        S3_FIXTURE,
        repo_root=_prepare_repo_root(tmp_path, remove_required_category),
        run_id="TEST_RUN",
        output_path=Path(
            "006_System-Manifests/aec-mepfs-backbone/parity/TEST_RUN"
        ) / "api-explorer-parity-report.json",
        executor=_executor([0] * EXPECTED_PARITY_COMMAND_COUNT),
    )

    assert report["ok"] is False
    assert report["commands_run"] == 0
    assert any("missing required parity categories (invalid_node_id)" in error for error in report["errors"])


def test_parity_runner_requires_declared_commands_to_have_case_coverage(
    tmp_path: Path,
) -> None:
    def remove_contract_command_case(payload: dict[str, Any]) -> None:
        payload["api_explorer_parity_cases"] = [
            case
            for case in payload["api_explorer_parity_cases"]
            if case["parity_category"] != "shadow_backbone_contract_validation"
        ]

    report = run_parity_fixture(
        S3_FIXTURE,
        repo_root=_prepare_repo_root(tmp_path, remove_contract_command_case),
        run_id="TEST_RUN",
        output_path=Path(
            "006_System-Manifests/aec-mepfs-backbone/parity/TEST_RUN"
        ) / "api-explorer-parity-report.json",
        executor=_executor([0] * EXPECTED_PARITY_COMMAND_COUNT),
    )

    assert report["ok"] is False
    assert report["commands_run"] == 0
    assert any(
        "declared commands without parity case coverage "
        "(PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q)"
        in error
        for error in report["errors"]
    )


def test_parity_runner_reports_timeout_without_losing_artifact(tmp_path: Path) -> None:
    output_path = Path(
        "006_System-Manifests/aec-mepfs-backbone/parity/TEST_RUN"
    ) / "api-explorer-parity-report.json"
    calls: list[str] = []

    def timeout_then_pass(command: str, cwd: Path, timeout_seconds: int) -> CommandExecution:
        del cwd
        calls.append(command)
        if len(calls) == 1:
            raise subprocess.TimeoutExpired(
                cmd=command,
                timeout=timeout_seconds,
                output="partial output",
                stderr="timed out",
            )
        return CommandExecution(command=command, exit_code=0, duration_seconds=0.01)

    report = run_parity_fixture(
        S3_FIXTURE,
        repo_root=_prepare_repo_root(tmp_path),
        run_id="TEST_RUN",
        output_path=output_path,
        executor=timeout_then_pass,
    )

    saved = json.loads((tmp_path / output_path).read_text(encoding="utf-8"))
    assert saved == report
    assert report["ok"] is False
    assert report["commands_run"] == EXPECTED_PARITY_COMMAND_COUNT
    assert report["command_results"][0]["exit_code"] == 124
    assert report["command_results"][0]["stderr_tail"] == "timed out"
