"""Sprint PIPELINE-CLI Task 1 — tests for build_default_orchestrator factory.

The factory reads `features._features_block()` (via VITRUVIUS_CONFIG)
and returns a ParserOrchestrator wired with parser chains and
preprocessors that match the on-flag state. With every p1b_* flag
off the factory MUST raise ValueError so callers get a clear message
instead of building an empty orchestrator.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from vitruvius.parsers.document_taxonomy import DocumentClass
from vitruvius.parsers.opendataloader_parser import OpenDataLoaderParser


def _write_config(path: Path, *, flags: dict[str, bool]) -> None:
    lines = ["project_name: Vitruvius", "features:"]
    for name, value in flags.items():
        lines.append(f"  {name}: {'true' if value else 'false'}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


@pytest.fixture
def isolated_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Yield a (path, write_flags) pair with VITRUVIUS_CONFIG and the
    factory cache reset between tests so each test starts clean."""
    cfg = tmp_path / "vitruvius.yaml"
    _write_config(cfg, flags={})
    monkeypatch.setenv("VITRUVIUS_CONFIG", str(cfg))

    # Reset the lru_cache on the helper so the new env var takes effect.
    from vitruvius.parsers import factory as factory_module

    factory_module._load_features_cached.cache_clear()

    def writer(flags: dict[str, bool]) -> None:
        _write_config(cfg, flags=flags)
        factory_module._load_features_cached.cache_clear()

    yield cfg, writer

    factory_module._load_features_cached.cache_clear()


def test_factory_raises_when_all_p1b_flags_off(isolated_config) -> None:
    _, write = isolated_config
    write({
        "p1b_docling_parser": False,
        "p1b_libreoffice_preprocessor": False,
        "p1b_ocr_preprocessor": False,
        "p1b_process_pool_orchestration": False,
        "p1b_rust_pdf_parser": False,
    })

    from vitruvius.parsers.factory import build_default_orchestrator

    with pytest.raises(ValueError) as excinfo:
        build_default_orchestrator()

    assert "p1b_docling_parser" in str(excinfo.value)
    assert "config/vitruvius.yaml" in str(excinfo.value)


def test_factory_tranche1_chains_when_docling_flag_on(isolated_config) -> None:
    """With p1b_docling_parser on and rust off, hybrid_pdf gets DoclingParser
    and text_pdf_simple gets OpenDataLoaderParser as the only chain entry."""
    _, write = isolated_config
    write({
        "p1b_docling_parser": True,
        "p1b_libreoffice_preprocessor": False,
        "p1b_ocr_preprocessor": False,
        "p1b_process_pool_orchestration": False,
        "p1b_rust_pdf_parser": False,
    })

    from vitruvius.parsers.docling_parser import DoclingParser
    from vitruvius.parsers.factory import build_default_orchestrator

    orch = build_default_orchestrator()

    text_chain = orch._chains[DocumentClass.TEXT_PDF_SIMPLE]
    hybrid_chain = orch._chains[DocumentClass.HYBRID_PDF]

    assert len(text_chain) == 1
    assert isinstance(text_chain[0], OpenDataLoaderParser)
    assert len(hybrid_chain) == 1
    assert isinstance(hybrid_chain[0], DoclingParser)


def test_factory_tranche3_puts_rust_parser_first(isolated_config) -> None:
    """With p1b_rust_pdf_parser on, RustPdfParser is the primary entry
    in both text_pdf_simple and hybrid_pdf chains; the Tranche-1
    parsers stay as fallbacks."""
    _, write = isolated_config
    write({
        "p1b_docling_parser": True,
        "p1b_libreoffice_preprocessor": False,
        "p1b_ocr_preprocessor": False,
        "p1b_process_pool_orchestration": False,
        "p1b_rust_pdf_parser": True,
    })

    from vitruvius.parsers.docling_parser import DoclingParser
    from vitruvius.parsers.factory import build_default_orchestrator
    from vitruvius.parsers.rust_pdf_parser import RustPdfParser

    orch = build_default_orchestrator()

    text_chain = orch._chains[DocumentClass.TEXT_PDF_SIMPLE]
    hybrid_chain = orch._chains[DocumentClass.HYBRID_PDF]

    assert isinstance(text_chain[0], RustPdfParser)
    assert any(isinstance(p, OpenDataLoaderParser) for p in text_chain[1:])
    assert isinstance(hybrid_chain[0], RustPdfParser)
    assert any(isinstance(p, DoclingParser) for p in hybrid_chain[1:])


def test_factory_registers_libreoffice_preprocessor_when_flag_on(
    isolated_config,
) -> None:
    _, write = isolated_config
    write({
        "p1b_docling_parser": True,
        "p1b_libreoffice_preprocessor": True,
        "p1b_ocr_preprocessor": False,
        "p1b_process_pool_orchestration": False,
        "p1b_rust_pdf_parser": False,
    })

    from vitruvius.parsers.factory import build_default_orchestrator
    from vitruvius.parsers.libreoffice_preprocessor import LibreOfficePreprocessor

    orch = build_default_orchestrator()

    assert DocumentClass.OFFICE_DOC in orch._preprocessors
    assert isinstance(
        orch._preprocessors[DocumentClass.OFFICE_DOC], LibreOfficePreprocessor
    )


def test_factory_registers_ocr_preprocessor_for_both_scanned_classes(
    isolated_config,
) -> None:
    _, write = isolated_config
    write({
        "p1b_docling_parser": True,
        "p1b_libreoffice_preprocessor": False,
        "p1b_ocr_preprocessor": True,
        "p1b_process_pool_orchestration": False,
        "p1b_rust_pdf_parser": False,
    })

    from vitruvius.parsers.factory import build_default_orchestrator
    from vitruvius.parsers.ocr_preprocessor import OCRPreprocessor

    orch = build_default_orchestrator()

    assert isinstance(
        orch._preprocessors[DocumentClass.SCANNED_PDF_CLEAN], OCRPreprocessor
    )
    assert isinstance(
        orch._preprocessors[DocumentClass.SCANNED_PDF_NOISY], OCRPreprocessor
    )
