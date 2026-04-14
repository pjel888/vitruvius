"""Verify pipeline_cli.py does not eagerly import heavy PDF/OCR deps.

The test runs the import in a subprocess so it cannot pollute the parent
pytest process's sys.modules (an earlier in-process approach broke other
test modules by deleting vitruvius.* from sys.modules).
"""

import os
import subprocess
import sys
from pathlib import Path


CLI = Path(__file__).resolve().parent.parent / "pipeline_cli.py"
REPO_ROOT = CLI.resolve().parent.parent


def _run_cli(args):
    env = {**os.environ, "PYTHONPATH": "scripts"}
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
    )


def test_promote_help_does_not_import_conversion():
    """Importing pipeline_cli at module scope must not pull in heavy deps.

    Uses a subprocess so clearing sys.modules cannot affect other tests.
    """
    env = {**os.environ, "PYTHONPATH": "scripts"}
    script = (
        "import sys;"
        "import importlib.util;"
        "spec = importlib.util.spec_from_file_location('pipeline_cli', r'" + str(CLI) + "');"
        "mod = importlib.util.module_from_spec(spec);"
        "spec.loader.exec_module(mod);"
        "forbidden = {'vitruvius.conversion', 'vitruvius.ocr', 'vitruvius.office', "
        "'opendataloader_pdf', 'ocrmypdf', 'pypdf'};"
        "leaked = forbidden & set(sys.modules.keys());"
        "print('LEAKED:' + ','.join(sorted(leaked)) if leaked else 'CLEAN');"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
    )
    assert result.returncode == 0, f"subprocess failed: {result.stderr}"
    assert "CLEAN" in result.stdout, f"CLI eagerly imported heavy modules: {result.stdout}"


def test_promote_help_still_works():
    result = _run_cli(["promote", "--help"])
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "promote" in result.stdout.lower()


def test_refine_help_still_works():
    result = _run_cli(["refine", "--help"])
    assert result.returncode == 0, f"stderr: {result.stderr}"
