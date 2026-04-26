from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from vitruvius.kg.backbone_repo_state import git_status_paths, read_repo_state


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (" M api/index.ts", ["api/index.ts"]),
        (
            "?? 006_System-Manifests/aec-mepfs-backbone/run/report.json",
            ["006_System-Manifests/aec-mepfs-backbone/run/report.json"],
        ),
        ("R  old-name.json -> new-name.json", ["new-name.json"]),
        ('?? "docs/path with spaces.md"', ["docs/path with spaces.md"]),
        ("", []),
        (None, []),
    ],
)
def test_git_status_paths_handles_git_short_status_shapes(
    status: str | None,
    expected: list[str],
) -> None:
    assert git_status_paths(status) == expected


def test_read_repo_state_reports_clean_non_git_root(tmp_path: Path) -> None:
    assert read_repo_state(tmp_path) == {
        "generated_evidence_dirty": False,
        "generated_evidence_dirty_path_count": 0,
        "git_head_commit": None,
        "source_dirty_path_count": 0,
        "source_working_tree_dirty": False,
        "working_tree_dirty": False,
    }


def test_read_repo_state_splits_source_dirty_from_generated_evidence_dirty(
    tmp_path: Path,
) -> None:
    source = tmp_path / "api" / "index.ts"
    source.parent.mkdir(parents=True)
    source.write_text("app.get('/v2/backbone', handler);\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "add", "api/index.ts"], cwd=tmp_path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=test@example.test",
            "-c",
            "user.name=Test User",
            "commit",
            "-m",
            "seed",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    generated = (
        tmp_path
        / "006_System-Manifests"
        / "aec-mepfs-backbone"
        / "evidence-manifest"
        / "TEST"
        / "shadow-evidence-manifest-report.json"
    )
    generated.parent.mkdir(parents=True)
    generated.write_text("{}", encoding="utf-8")
    drift = tmp_path / ".ai" / "source-drift.md"
    drift.parent.mkdir()
    drift.write_text("drift", encoding="utf-8")

    state = read_repo_state(tmp_path)

    assert state["git_head_commit"]
    assert state["working_tree_dirty"] is True
    assert state["generated_evidence_dirty"] is True
    assert state["generated_evidence_dirty_path_count"] == 1
    assert state["source_working_tree_dirty"] is True
    assert state["source_dirty_path_count"] == 1
