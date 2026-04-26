"""Shared repo-state helpers for AEC-MEPFS Backbone shadow reports.

The helpers only inspect local git metadata. They do not call API or Explorer
runtimes, query Neo4j, rebuild KG artifacts, ingest protected content, mutate
feature flags, or promote shadow artifacts.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


GENERATED_EVIDENCE_PREFIX = "006_System-Manifests/aec-mepfs-backbone/"


def read_repo_state(
    root: Path,
    *,
    generated_evidence_prefix: str = GENERATED_EVIDENCE_PREFIX,
) -> dict[str, Any]:
    """Return source-vs-generated git dirtiness metadata for shadow reports."""
    head = _run_git(root, "rev-parse", "HEAD")
    status = _run_git(root, "status", "--short", "--untracked-files=all")
    dirty_paths = git_status_paths(status)
    generated_paths = [
        path for path in dirty_paths if path.startswith(generated_evidence_prefix)
    ]
    source_paths = [path for path in dirty_paths if path not in generated_paths]
    return {
        "git_head_commit": head,
        "working_tree_dirty": bool(status),
        "source_working_tree_dirty": bool(source_paths),
        "generated_evidence_dirty": bool(generated_paths),
        "source_dirty_path_count": len(source_paths),
        "generated_evidence_dirty_path_count": len(generated_paths),
    }


def git_status_paths(status: str | None) -> list[str]:
    """Extract paths from `git status --short` output."""
    if not status:
        return []
    paths: list[str] = []
    for line in status.splitlines():
        if not line:
            continue
        path = line[3:] if len(line) > 3 else line
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[-1]
        paths.append(path.strip().strip('"'))
    return paths


def _run_git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ("git", *args),
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None
