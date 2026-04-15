"""Sprint CLEANUP-1 Stream C3.1 — per-page OOM/timeout isolation tests.

This test file pins the ``failed_pages`` surface on :class:`ParseResult`
and — once the Rust wheel is rebuilt — the ``p1b_page_isolation``
flag-gated path through :class:`RustPdfParser` that routes through
``vitruvius_rust_pdf.extract_pdf_text_with_errors``.

Why the 3rd test starts skipped: the ``(String, Vec<i64>)``-returning
Rust entry point lands in the same commit as this file, but the test
harness may run the first two tests before the wheel rebuild completes
during local development. Un-skip once the wheel is confirmed installed.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.parsers.base_parser import ParseResult, ParserTelemetry


def _make_telemetry(**overrides: object) -> ParserTelemetry:
    """Build a minimal :class:`ParserTelemetry` for these tests.

    The real class has many non-default fields (see ``base_parser.py``);
    this helper centralises the fixture so individual tests only need
    to override what they care about.
    """
    base: dict[str, object] = dict(
        parser_id="fake",
        attempt_index=0,
        duration_ms=1,
        pages_total=0,
        pages_processed=0,
        page_coverage_ratio=0.0,
        text_length=0,
        md_length=0,
        headers=0,
        tables=0,
        images=0,
        captions=0,
        ocr_applied=False,
        confidence=1.0,
        valid=True,
    )
    base.update(overrides)
    return ParserTelemetry(**base)  # type: ignore[arg-type]


def test_parseresult_has_failed_pages_field() -> None:
    """Default :class:`ParseResult` exposes an empty ``failed_pages`` list."""
    telemetry = _make_telemetry()
    result = ParseResult(
        markdown_text="abc",
        telemetry=telemetry,
        sidecar_metadata={},
    )
    assert result.failed_pages == []
    assert isinstance(result.failed_pages, list)


def test_parseresult_accepts_failed_pages_list() -> None:
    """Callers may populate ``failed_pages`` via kw-only construction."""
    telemetry = _make_telemetry(
        pages_total=5,
        pages_processed=3,
        page_coverage_ratio=0.6,
    )
    result = ParseResult(
        markdown_text="abc",
        telemetry=telemetry,
        sidecar_metadata={},
        failed_pages=[3, 7],
    )
    assert result.failed_pages == [3, 7]


def test_rust_pdf_parser_reports_failed_pages_when_flag_on(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Flag-on path — :class:`RustPdfParser` populates ``failed_pages``.

    Blank pages decode cleanly, so ``failed_pages`` should be empty on
    the happy path. The test's real value is pinning the contract that
    the field is populated (even if empty) when the flag is on — a
    regression guard for the ``p1b_page_isolation`` dispatch.
    """
    pytest.importorskip("vitruvius_rust_pdf")
    if not hasattr(
        pytest.importorskip("vitruvius_rust_pdf"),
        "extract_pdf_text_with_errors",
    ):
        pytest.skip("extract_pdf_text_with_errors not in installed wheel yet")
    pypdf = pytest.importorskip("pypdf")

    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.add_blank_page(width=72, height=72)
    pdf_path = tmp_path / "two_pages.pdf"
    with open(pdf_path, "wb") as fh:
        writer.write(fh)

    from vitruvius.parsers import rust_pdf_parser as _rpp

    class _FlagsOn:
        def is_enabled(self, name: str) -> bool:
            return name == "p1b_page_isolation"

    monkeypatch.setattr(
        _rpp,
        "_load_features_cached",
        lambda: _FlagsOn(),
        raising=False,
    )

    parser = _rpp.RustPdfParser()
    result = parser.parse(pdf_path, work_dir=tmp_path)

    assert isinstance(result.failed_pages, list)
    # Blank pages decode cleanly — failed_pages should be empty
    assert result.failed_pages == []
    assert isinstance(result.markdown_text, str)
