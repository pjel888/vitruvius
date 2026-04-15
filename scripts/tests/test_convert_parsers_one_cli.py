"""Sprint PIPELINE-CLI Task 3 — pipeline_cli.py convert-parsers-one smoke tests.

Verifies the new subparser registration + dispatch wiring without
reaching into any real PDF kernels. The handler-level tests in
test_parser_cli_handler.py cover the stub-orchestrator contract;
this file's job is to confirm:

1. ``convert-parsers-one --help`` succeeds (argparse wiring + lazy
   import contract)
2. The subparser path (build_parser) does not eagerly import any
   heavy parser modules
3. The dispatch branch in main() does not eagerly import the
   handler at module import time (only when the command runs)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent.parent
CLI = SCRIPTS_DIR / "pipeline_cli.py"
REPO_ROOT = SCRIPTS_DIR.parent


def _run_cli(args: list[str]) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": str(SCRIPTS_DIR)}
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
    )


def test_convert_parsers_one_help_works() -> None:
    """The new subcommand must register cleanly and print help."""
    result = _run_cli(["convert-parsers-one", "--help"])
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "convert-parsers-one" in result.stdout
    assert "relative_pdf_path" in result.stdout


def test_convert_parsers_one_help_does_not_eager_import_handler() -> None:
    """Importing pipeline_cli at module scope must not pull in
    cli_handler, factory, or any heavy parser deps. Same lazy-import
    contract enforced in test_cli_lazy_imports.py for the existing
    convert command (per AD-015).
    """
    env = {**os.environ, "PYTHONPATH": str(SCRIPTS_DIR)}
    script = (
        "import sys;"
        "import importlib.util;"
        "spec = importlib.util.spec_from_file_location("
        "'pipeline_cli', r'" + str(CLI) + "');"
        "mod = importlib.util.module_from_spec(spec);"
        "spec.loader.exec_module(mod);"
        "forbidden = {"
        "'vitruvius.parsers.cli_handler',"
        "'vitruvius.parsers.factory',"
        "'vitruvius.parsers.docling_parser',"
        "'vitruvius.parsers.opendataloader_parser',"
        "'vitruvius.parsers.libreoffice_preprocessor',"
        "'vitruvius.parsers.ocr_preprocessor',"
        "'vitruvius.parsers.rust_pdf_parser',"
        "'opendataloader_pdf', 'docling', 'ocrmypdf', 'vitruvius_rust_pdf'"
        "};"
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
    assert "CLEAN" in result.stdout, (
        "convert-parsers-one wiring eagerly imports parser modules: "
        f"{result.stdout}"
    )


def test_convert_parsers_one_missing_source_returns_1(tmp_path: Path) -> None:
    """End-to-end: invoke the new subcommand on a path that doesn't
    exist; the handler must return 1 and print an error. Uses an
    isolated cwd so it never touches the real Raw-Source-Layer."""
    raw = tmp_path / "001_Raw-Source-Layer"
    raw.mkdir()

    cfg = tmp_path / "config" / "vitruvius.yaml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text("project_name: Vitruvius\nfeatures: {}\n", encoding="utf-8")

    env = {
        **os.environ,
        "PYTHONPATH": str(SCRIPTS_DIR),
        "VITRUVIUS_CONFIG": str(cfg),
    }
    result = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "convert-parsers-one",
            "001-Laws/PD-1096/missing.pdf",
        ],
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        env=env,
    )
    # Note: the handler resolves the source via vitruvius.paths.get_repo_root
    # which returns the *real* repo root, not tmp_path. So the file lookup
    # will (correctly) miss in the real Raw-Source-Layer too. Either way
    # the exit code must be 1 and stderr/stdout must report a clear error.
    assert result.returncode == 1
    combined = result.stdout + result.stderr
    assert "ERROR" in combined or "error" in combined
