from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

CLI = Path(__file__).resolve().parent.parent / 'pipeline_cli.py'
REPO_ROOT = CLI.resolve().parent.parent


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, 'PYTHONPATH': 'scripts'}
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=env,
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def test_canonicalize_plan_one_cli_accepts_pipeline_keyword_shape(tmp_path: Path) -> None:
    _write(
        tmp_path / '002_Raw-Conversion-Layer' / '001-Laws' / 'raw_markdown' / 'RA-9514' / 'ra9514.md',
        '# Fire Code\n',
    )
    result = _run_cli(
        ['canonicalize-plan-one', '001-Laws/raw_markdown/RA-9514/ra9514.md'],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert 'canonicalize-plan-one complete.' in result.stdout
    assert 'Title:' in result.stdout
    assert 'ID:' in result.stdout
