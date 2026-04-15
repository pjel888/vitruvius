"""Sprint 1B-M1 Task 2 — LibreOffice preprocessor.

Converts Office documents (.docx, .pptx, .odt) to PDF via the system
``soffice`` binary so a downstream PDF parser (Docling, OpenDataLoader)
can handle them through the same chain as native PDFs.

Reuses :func:`vitruvius.office.find_soffice_executable` for the
discovery logic — do not duplicate the path-probing here. If soffice
isn't installed, :func:`find_soffice_executable` raises and the
preprocessor surfaces the error in :class:`PreprocessResult.error`
without raising through normal use.

This is NOT a :class:`BaseParser` — it produces a new input for a
parser, not a Markdown output. The orchestrator runs preprocessors
before the parser chain.
"""
from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from vitruvius.office import find_soffice_executable


_OFFICE_EXTENSIONS = frozenset({".docx", ".pptx", ".odt", ".ods", ".odp"})


@dataclass(frozen=True)
class PreprocessResult:
    """Output of a :class:`LibreOfficePreprocessor`.

    ``pdf_path`` is ``None`` on any failure (soffice missing, non-Office
    extension, soffice exit != 0, expected output not found). ``error``
    carries the failure reason in that case.
    """

    pdf_path: Optional[Path]
    duration_ms: int
    error: Optional[str]


class LibreOfficePreprocessor:
    """Office → PDF preprocessor that runs before the parser chain."""

    preprocessor_id = "libreoffice_preprocessor"

    def preprocess(self, *, source_path: Path, workdir: Path) -> PreprocessResult:
        start = time.perf_counter()
        source_path = Path(source_path)

        if source_path.suffix.lower() not in _OFFICE_EXTENSIONS:
            return PreprocessResult(
                pdf_path=None,
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=(
                    f"not an office document: {source_path} "
                    f"(suffix={source_path.suffix!r})"
                ),
            )

        try:
            soffice = find_soffice_executable()
        except FileNotFoundError as exc:
            return PreprocessResult(
                pdf_path=None,
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"soffice not found: {exc}",
            )

        workdir = Path(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        expected_pdf = workdir / (source_path.stem + ".pdf")

        try:
            completed = subprocess.run(
                [
                    soffice,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(workdir),
                    str(source_path),
                ],
                capture_output=True,
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            return PreprocessResult(
                pdf_path=None,
                duration_ms=int((time.perf_counter() - start) * 1000),
                error="soffice conversion timed out after 120s",
            )

        duration_ms = int((time.perf_counter() - start) * 1000)

        if completed.returncode != 0:
            stderr_text = (completed.stderr or b"").decode("utf-8", errors="replace")
            return PreprocessResult(
                pdf_path=None,
                duration_ms=duration_ms,
                error=(
                    f"soffice returned {completed.returncode}: "
                    f"conversion failed. stderr={stderr_text[:500]}"
                ),
            )

        if not expected_pdf.exists():
            return PreprocessResult(
                pdf_path=None,
                duration_ms=duration_ms,
                error=(
                    f"soffice returned 0 but the expected output "
                    f"{expected_pdf} does not exist"
                ),
            )

        return PreprocessResult(
            pdf_path=expected_pdf,
            duration_ms=duration_ms,
            error=None,
        )
