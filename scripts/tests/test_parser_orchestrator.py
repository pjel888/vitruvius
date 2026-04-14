from __future__ import annotations

import abc
import dataclasses
from pathlib import Path
from typing import Any

import pytest

from vitruvius.parsers.base_parser import ParseResult, ParserTelemetry
from vitruvius.parsers.base_parser import BaseParser
from vitruvius.parsers.document_taxonomy import DocumentClass
from vitruvius.parsers.orchestrator import (
    AttemptRecord,
    OrchestratorResult,
    ParserOrchestrator,
    TerminalStatus,
)

# ---------------------------------------------------------------------------
# Helpers / stubs
# ---------------------------------------------------------------------------

_DUMMY_PATH = Path("/tmp/dummy.pdf")
_DUMMY_WORK = Path("/tmp/work")


def _make_telemetry(parser_id: str = "stub") -> ParserTelemetry:
    return ParserTelemetry(
        parser_id=parser_id,
        attempt_index=0,
        duration_ms=10,
        pages_total=1,
        pages_processed=1,
        page_coverage_ratio=1.0,
        text_length=5000,
        md_length=2000,
        headers=1,
        tables=0,
        images=0,
        captions=0,
        ocr_applied=False,
        confidence=0.99,
        valid=True,
    )


class _StubParser(BaseParser):
    """Intermediate abstract base for test stubs — stays abstract via abc.abstractmethod."""

    parser_id: str  # type: ignore[assignment]
    parser_version: str  # type: ignore[assignment]

    @abc.abstractmethod
    def parse(self, source_path: Path, work_dir: Path) -> ParseResult: ...


class _PassingParser(_StubParser):
    parser_id = "passing_parser"
    parser_version = "1.0.0"

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        return ParseResult(
            markdown_text="# Valid Document\n\nLorem ipsum " * 100,
            telemetry=_make_telemetry(self.parser_id),
            sidecar_metadata={"file_type": "pdf"},
        )


class _FailingGateParser(_StubParser):
    """Produces output that fails Gate-001 (null bytes)."""

    parser_id = "failing_gate_parser"
    parser_version = "1.0.0"

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        return ParseResult(
            markdown_text="# Header\x00null byte",
            telemetry=_make_telemetry(self.parser_id),
            sidecar_metadata={"file_type": "pdf"},
        )


class _FailingGateParser2(_StubParser):
    """Second distinct failing-gate parser for tests that need two."""

    parser_id = "failing_gate_parser_2"
    parser_version = "1.0.0"

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        return ParseResult(
            markdown_text="\x00bad",
            telemetry=_make_telemetry(self.parser_id),
            sidecar_metadata={"file_type": "pdf"},
        )


class _ExceptionParser(_StubParser):
    """Raises during parse()."""

    parser_id = "exception_parser"
    parser_version = "1.0.0"

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        raise RuntimeError("parser exploded")


class _ExceptionParser2(_StubParser):
    """Second exception-raising parser."""

    parser_id = "exception_parser_2"
    parser_version = "1.0.0"

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        raise ValueError("also exploded")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def orch_passing() -> ParserOrchestrator:
    return ParserOrchestrator(
        parser_chains={DocumentClass.TEXT_PDF_SIMPLE: [_PassingParser()]}
    )


@pytest.fixture()
def orch_fallback_success() -> ParserOrchestrator:
    return ParserOrchestrator(
        parser_chains={
            DocumentClass.TEXT_PDF_SIMPLE: [_FailingGateParser(), _PassingParser()]
        }
    )


# ---------------------------------------------------------------------------
# Test 1: first parser passes → AUTO_ACCEPTED
# ---------------------------------------------------------------------------


def test_first_parser_passes_returns_auto_accepted(
    orch_passing: ParserOrchestrator,
) -> None:
    result = orch_passing.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert result.terminal_status == TerminalStatus.AUTO_ACCEPTED
    assert result.successful_parser_id == "passing_parser"
    assert len(result.attempts) == 1


# ---------------------------------------------------------------------------
# Test 2: fallback parser passes → AUTO_REFINED
# ---------------------------------------------------------------------------


def test_fallback_success_returns_auto_refined(
    orch_fallback_success: ParserOrchestrator,
) -> None:
    result = orch_fallback_success.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert result.terminal_status == TerminalStatus.AUTO_REFINED
    assert result.successful_parser_id == "passing_parser"
    assert len(result.attempts) == 2
    assert result.attempts[0].gate_report is not None
    assert result.attempts[0].gate_report.passed is False


# ---------------------------------------------------------------------------
# Test 3: all parsers fail gates → FALLBACK_EXHAUSTED
# ---------------------------------------------------------------------------


def test_all_parsers_fail_returns_fallback_exhausted() -> None:
    orch = ParserOrchestrator(
        parser_chains={
            DocumentClass.TEXT_PDF_SIMPLE: [
                _FailingGateParser(),
                _FailingGateParser2(),
            ]
        }
    )
    result = orch.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert result.terminal_status == TerminalStatus.FALLBACK_EXHAUSTED
    assert result.successful_parser_id is None
    assert result.final_parse_result is None
    assert len(result.attempts) == 2
    assert all(a.gate_report is not None and a.gate_report.passed is False for a in result.attempts)


# ---------------------------------------------------------------------------
# Test 4: exception advances to next parser → AUTO_REFINED
# ---------------------------------------------------------------------------


def test_parser_exception_advances_to_next() -> None:
    orch = ParserOrchestrator(
        parser_chains={
            DocumentClass.TEXT_PDF_SIMPLE: [_ExceptionParser(), _PassingParser()]
        }
    )
    result = orch.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert result.terminal_status == TerminalStatus.AUTO_REFINED
    first = result.attempts[0]
    assert first.exception == "parser exploded"
    assert first.parse_result is None
    assert first.gate_report is None


# ---------------------------------------------------------------------------
# Test 5: all parsers raise → FALLBACK_EXHAUSTED
# ---------------------------------------------------------------------------


def test_all_parsers_raise_returns_fallback_exhausted() -> None:
    orch = ParserOrchestrator(
        parser_chains={
            DocumentClass.TEXT_PDF_SIMPLE: [_ExceptionParser(), _ExceptionParser2()]
        }
    )
    result = orch.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert result.terminal_status == TerminalStatus.FALLBACK_EXHAUSTED
    assert all(a.exception is not None for a in result.attempts)


# ---------------------------------------------------------------------------
# Test 6: attempt trail records every parser in order
# ---------------------------------------------------------------------------


def test_attempt_trail_records_every_attempt_in_order() -> None:
    orch = ParserOrchestrator(
        parser_chains={
            DocumentClass.TEXT_PDF_SIMPLE: [
                _FailingGateParser(),
                _ExceptionParser(),
                _PassingParser(),
            ]
        }
    )
    result = orch.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert [a.parser_id for a in result.attempts] == [
        "failing_gate_parser",
        "exception_parser",
        "passing_parser",
    ]
    assert [a.attempt_index for a in result.attempts] == [0, 1, 2]


# ---------------------------------------------------------------------------
# Test 7: attempt_index values are 0-based
# ---------------------------------------------------------------------------


def test_attempt_indexes_are_zero_based(orch_fallback_success: ParserOrchestrator) -> None:
    result = orch_fallback_success.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert result.attempts[0].attempt_index == 0
    assert result.attempts[1].attempt_index == 1


# ---------------------------------------------------------------------------
# Test 8: empty chain raises ValueError
# ---------------------------------------------------------------------------


def test_empty_chain_raises_value_error() -> None:
    orch = ParserOrchestrator(
        parser_chains={DocumentClass.TEXT_PDF_SIMPLE: []}
    )
    with pytest.raises(ValueError, match="empty"):
        orch.process(
            source_path=_DUMMY_PATH,
            doc_class=DocumentClass.TEXT_PDF_SIMPLE,
            work_dir=_DUMMY_WORK,
        )


# ---------------------------------------------------------------------------
# Test 9: missing DocumentClass raises KeyError
# ---------------------------------------------------------------------------


def test_missing_document_class_raises_key_error() -> None:
    orch = ParserOrchestrator(
        parser_chains={DocumentClass.TEXT_PDF_SIMPLE: [_PassingParser()]}
    )
    with pytest.raises(KeyError):
        orch.process(
            source_path=_DUMMY_PATH,
            doc_class=DocumentClass.HYBRID_PDF,
            work_dir=_DUMMY_WORK,
        )


# ---------------------------------------------------------------------------
# Test 10: successful first parse short-circuits the chain
# ---------------------------------------------------------------------------


def test_successful_parse_short_circuits_chain(orch_passing: ParserOrchestrator) -> None:
    orch = ParserOrchestrator(
        parser_chains={
            DocumentClass.TEXT_PDF_SIMPLE: [_PassingParser(), _FailingGateParser()]
        }
    )
    result = orch.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert len(result.attempts) == 1


# ---------------------------------------------------------------------------
# Test 11: OrchestratorResult is frozen
# ---------------------------------------------------------------------------


def test_orchestrator_result_is_frozen(orch_passing: ParserOrchestrator) -> None:
    result = orch_passing.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.terminal_status = TerminalStatus.FALLBACK_EXHAUSTED  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Test 12: AttemptRecord is frozen
# ---------------------------------------------------------------------------


def test_attempt_record_is_frozen(orch_passing: ParserOrchestrator) -> None:
    result = orch_passing.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    attempt = result.attempts[0]
    with pytest.raises(dataclasses.FrozenInstanceError):
        attempt.parser_id = "hacked"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Test 13: final_parse_result is the winning parse result
# ---------------------------------------------------------------------------


def test_final_parse_result_is_the_winning_parse_result(
    orch_fallback_success: ParserOrchestrator,
) -> None:
    result = orch_fallback_success.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert result.terminal_status == TerminalStatus.AUTO_REFINED
    assert result.final_parse_result is result.attempts[-1].parse_result


# ---------------------------------------------------------------------------
# Test 14: process() requires keyword arguments
# ---------------------------------------------------------------------------


def test_process_signature_requires_keyword_args(orch_passing: ParserOrchestrator) -> None:
    with pytest.raises(TypeError):
        orch_passing.process(_DUMMY_PATH, DocumentClass.TEXT_PDF_SIMPLE, _DUMMY_WORK)  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# Test 15: AUTO_ACCEPTED only when the first attempt wins
# ---------------------------------------------------------------------------


def test_auto_accepted_only_when_first_attempt_wins() -> None:
    orch_single = ParserOrchestrator(
        parser_chains={DocumentClass.TEXT_PDF_SIMPLE: [_PassingParser()]}
    )
    r1 = orch_single.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert r1.terminal_status == TerminalStatus.AUTO_ACCEPTED

    orch_fallback = ParserOrchestrator(
        parser_chains={
            DocumentClass.TEXT_PDF_SIMPLE: [_FailingGateParser(), _PassingParser()]
        }
    )
    r2 = orch_fallback.process(
        source_path=_DUMMY_PATH,
        doc_class=DocumentClass.TEXT_PDF_SIMPLE,
        work_dir=_DUMMY_WORK,
    )
    assert r2.terminal_status == TerminalStatus.AUTO_REFINED
    assert r2.terminal_status != TerminalStatus.AUTO_ACCEPTED
