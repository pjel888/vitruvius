"""Sprint PIPELINE-CLI Task 1 — build_default_orchestrator factory.

Single source of truth for "which Phase 1B parsers run for which
DocumentClass under the current feature-flag state". Reads the
`features:` block from `config/vitruvius.yaml` (honouring
``VITRUVIUS_CONFIG`` for hermetic tests) and returns a freshly-built
:class:`ParserOrchestrator` wired with the appropriate parser chains
and preprocessors.

Flag dispatch matrix (all flags default false in
``config/vitruvius.yaml``; each flag is a deployment-readiness marker
that does **nothing** unless it is on AND this factory is called):

* ``p1b_docling_parser``           — registers DoclingParser as the
  primary HYBRID_PDF parser and OpenDataLoaderParser as the primary
  TEXT_PDF_SIMPLE parser. Required for the orchestrator to have any
  parsers registered at all (raises ValueError otherwise).
* ``p1b_libreoffice_preprocessor`` — adds LibreOfficePreprocessor
  for OFFICE_DOC.
* ``p1b_ocr_preprocessor``         — adds OCRPreprocessor for
  SCANNED_PDF_CLEAN and SCANNED_PDF_NOISY.
* ``p1b_process_pool_orchestration`` — reserved for the future
  ProcessPool batch upgrade. Not consumed here yet (the existing
  ``ParserOrchestrator.process_batch`` runs sequentially regardless;
  see Sprint 1B-M2 Task 2). The factory accepts the flag for
  completeness so a future change can switch on it without
  re-touching CLI dispatch.
* ``p1b_rust_pdf_parser``          — promotes RustPdfParser to the
  primary entry of TEXT_PDF_SIMPLE and HYBRID_PDF chains, with the
  Tranche-1 parsers retained as fallbacks.

Perf call: this factory + its flag dispatch sit **above the Rust
Line** per AD-036 — pure CLI orchestration, no compute. The
expensive work (parser ``parse()`` calls, preprocessor ``preprocess()``
calls) happens later, and the kernels those touch (lopdf for Rust,
docling/opendataloader for Python) are already at the right side of
the line.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from vitruvius.features import Features, load_features
from vitruvius.parsers.base_parser import BaseParser
from vitruvius.parsers.document_taxonomy import DocumentClass
from vitruvius.parsers.orchestrator import ParserOrchestrator


def _resolve_config_path() -> Path:
    """Mirror of :func:`vitruvius.spatial.cli._resolve_config_path`.

    Honours ``VITRUVIUS_CONFIG`` for hermetic tests, falls back to
    ``<cwd>/config/vitruvius.yaml``. Kept local so this module does
    not pull in the spatial package on every CLI invocation.
    """
    env_path = os.environ.get("VITRUVIUS_CONFIG")
    if env_path:
        return Path(env_path)
    return Path.cwd() / "config" / "vitruvius.yaml"


@lru_cache(maxsize=1)
def _load_features_cached() -> Features:
    """Load the feature-flag block once per process.

    Tests reset this cache via ``_load_features_cached.cache_clear()``
    after rewriting the temp config file — keep this as a plain
    module-level attribute so monkey-patching keeps working.
    """
    return load_features(_resolve_config_path())


def build_default_orchestrator() -> ParserOrchestrator:
    """Construct a :class:`ParserOrchestrator` from the live flag state.

    Raises:
        ValueError: if no ``p1b_*`` parser flag is enabled — the
            orchestrator would have no chains and any subsequent
            ``process()`` call would raise an unfriendly KeyError.
    """
    features = _load_features_cached()

    docling_on = features.is_enabled("p1b_docling_parser")
    rust_on = features.is_enabled("p1b_rust_pdf_parser")
    libreoffice_on = features.is_enabled("p1b_libreoffice_preprocessor")
    ocr_on = features.is_enabled("p1b_ocr_preprocessor")
    # Reserved — see module docstring.
    _process_pool_on = features.is_enabled("p1b_process_pool_orchestration")

    if not (docling_on or rust_on):
        raise ValueError(
            "no p1b_* parser flags enabled — set features.p1b_docling_parser "
            "(and optionally features.p1b_rust_pdf_parser) to true in "
            "config/vitruvius.yaml before running convert-parsers-one"
        )

    # Lazy-imports so this module stays cheap when callers only want
    # the helpers above. The downstream parser modules pull in
    # opendataloader_pdf / docling / lopdf only when their parse()
    # method runs (per AD-015).
    from vitruvius.parsers.opendataloader_parser import OpenDataLoaderParser

    parser_chains: dict[DocumentClass, list[BaseParser]] = {}

    if rust_on:
        from vitruvius.parsers.rust_pdf_parser import RustPdfParser

        rust_parser = RustPdfParser()
        # text_pdf_simple → Rust first, OpenDataLoader fallback
        text_chain: list[BaseParser] = [rust_parser, OpenDataLoaderParser()]
        # hybrid_pdf → Rust first, Docling fallback (if docling on)
        hybrid_chain: list[BaseParser] = [rust_parser]
        if docling_on:
            from vitruvius.parsers.docling_parser import DoclingParser

            hybrid_chain.append(DoclingParser())
        parser_chains[DocumentClass.TEXT_PDF_SIMPLE] = text_chain
        parser_chains[DocumentClass.HYBRID_PDF] = hybrid_chain
    else:
        # Tranche 1 — Docling on, Rust off.
        from vitruvius.parsers.docling_parser import DoclingParser

        parser_chains[DocumentClass.TEXT_PDF_SIMPLE] = [OpenDataLoaderParser()]
        parser_chains[DocumentClass.HYBRID_PDF] = [DoclingParser()]

    preprocessors: dict[DocumentClass, object] = {}
    if libreoffice_on:
        from vitruvius.parsers.libreoffice_preprocessor import LibreOfficePreprocessor

        preprocessors[DocumentClass.OFFICE_DOC] = LibreOfficePreprocessor()
    if ocr_on:
        from vitruvius.parsers.ocr_preprocessor import OCRPreprocessor

        ocr_pre = OCRPreprocessor()
        preprocessors[DocumentClass.SCANNED_PDF_CLEAN] = ocr_pre
        preprocessors[DocumentClass.SCANNED_PDF_NOISY] = ocr_pre

    return ParserOrchestrator(
        parser_chains=parser_chains,
        preprocessors=preprocessors,
    )
