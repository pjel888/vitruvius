from __future__ import annotations

from vitruvius.parsers.base_parser import BaseParser, ParseResult, ParserTelemetry
from vitruvius.parsers.document_taxonomy import DocumentClass, DocumentFeatures, classify_document
from vitruvius.parsers.quality_gates import GateReport, GateResult, GateStatus, run_quality_gates
from vitruvius.parsers.orchestrator import (
    AttemptRecord,
    OrchestratorResult,
    ParserOrchestrator,
    TerminalStatus,
)
from vitruvius.parsers.opendataloader_parser import OpenDataLoaderParser
from vitruvius.parsers.docling_parser import DoclingParser
from vitruvius.parsers.libreoffice_preprocessor import (
    LibreOfficePreprocessor,
    PreprocessResult,
)
from vitruvius.parsers.ocr_preprocessor import OCRPreprocessor

__all__ = [
    "BaseParser",
    "ParseResult",
    "ParserTelemetry",
    "DocumentClass",
    "DocumentFeatures",
    "classify_document",
    "GateStatus",
    "GateResult",
    "GateReport",
    "run_quality_gates",
    "TerminalStatus",
    "AttemptRecord",
    "OrchestratorResult",
    "ParserOrchestrator",
    "OpenDataLoaderParser",
    "DoclingParser",
    "LibreOfficePreprocessor",
    "PreprocessResult",
    "OCRPreprocessor",
]
