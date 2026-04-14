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
]
