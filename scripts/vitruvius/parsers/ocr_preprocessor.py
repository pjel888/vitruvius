"""Sprint 1B-M2 Task 1 — OCRPreprocessor.

Routes scanned PDFs through ``ocrmypdf`` (already installed via
Phase 1A) to produce a text-layered PDF that downstream parsers
can consume through the same code path as native text PDFs.

Duck-typed to match :class:`LibreOfficePreprocessor` from Tranche 1 —
exposes ``preprocessor_id`` + ``preprocess(*, source_path, workdir)``
returning a :class:`PreprocessResult`.

Low-spec note: ocrmypdf wraps tesseract (system binary, ~50 MB
install, runs in ~200 MB RAM for typical scanned pages). No torch,
no transformers, no model weights. Safe for the 8 GB M2 profile
and fits the long-term low-spec target.
"""
from __future__ import annotations

import time
from pathlib import Path

import ocrmypdf

from vitruvius.parsers.libreoffice_preprocessor import PreprocessResult


class OCRPreprocessor:
    """OCR preprocessor that wraps ocrmypdf.

    Use for :attr:`DocumentClass.SCANNED_PDF_CLEAN` and
    :attr:`DocumentClass.SCANNED_PDF_NOISY` chains. Produces a
    text-layered PDF in ``workdir`` suffixed ``.ocr.pdf``.
    """

    preprocessor_id = "ocr_preprocessor"

    def preprocess(self, *, source_path: Path, workdir: Path) -> PreprocessResult:
        start = time.perf_counter()
        source_path = Path(source_path)

        if not source_path.exists():
            return PreprocessResult(
                pdf_path=None,
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"source file does not exist: {source_path}",
            )
        if source_path.suffix.lower() != ".pdf":
            return PreprocessResult(
                pdf_path=None,
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=(
                    f"not a PDF: {source_path} "
                    f"(suffix={source_path.suffix!r})"
                ),
            )

        workdir = Path(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        output = workdir / (source_path.stem + ".ocr.pdf")

        try:
            ocrmypdf.ocr(
                str(source_path),
                str(output),
                skip_text=False,
                force_ocr=False,
                deskew=True,
                clean=True,
                progress_bar=False,
            )
        except Exception as exc:
            return PreprocessResult(
                pdf_path=None,
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"ocrmypdf failed: {exc}",
            )

        duration_ms = int((time.perf_counter() - start) * 1000)

        if not output.exists():
            return PreprocessResult(
                pdf_path=None,
                duration_ms=duration_ms,
                error=f"ocrmypdf returned without creating output: {output}",
            )

        return PreprocessResult(
            pdf_path=output,
            duration_ms=duration_ms,
            error=None,
        )
