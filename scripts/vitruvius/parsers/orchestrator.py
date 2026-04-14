from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from vitruvius.parsers.base_parser import BaseParser, ParseResult
from vitruvius.parsers.document_taxonomy import DocumentClass
from vitruvius.parsers.quality_gates import GateReport, run_quality_gates


class TerminalStatus(str, Enum):
    AUTO_ACCEPTED = "auto_accepted"
    AUTO_REFINED = "auto_refined"
    FALLBACK_EXHAUSTED = "fallback_exhausted"


@dataclass(kw_only=True, frozen=True)
class AttemptRecord:
    parser_id: str
    attempt_index: int
    parse_result: ParseResult | None
    gate_report: GateReport | None
    exception: str | None


@dataclass(kw_only=True, frozen=True)
class OrchestratorResult:
    terminal_status: TerminalStatus
    successful_parser_id: str | None
    final_parse_result: ParseResult | None
    attempts: tuple[AttemptRecord, ...]


class ParserOrchestrator:
    def __init__(self, parser_chains: dict[DocumentClass, list[BaseParser]]) -> None:
        self._chains = parser_chains

    def process(
        self,
        *,
        source_path: Path,
        doc_class: DocumentClass,
        work_dir: Path,
    ) -> OrchestratorResult:
        if doc_class not in self._chains:
            raise KeyError(
                f"No parser chain registered for DocumentClass {doc_class!r}"
            )
        chain = self._chains[doc_class]
        if not chain:
            raise ValueError(
                f"Parser chain for DocumentClass {doc_class!r} is empty — "
                "register at least one parser"
            )

        attempts: list[AttemptRecord] = []
        winner_index: int | None = None
        winning_parse_result: ParseResult | None = None
        winning_parser_id: str | None = None

        for idx, parser in enumerate(chain):
            try:
                parse_result = parser.parse(
                    source_path=source_path, work_dir=work_dir
                )
            except Exception as exc:
                attempts.append(
                    AttemptRecord(
                        parser_id=parser.parser_id,
                        attempt_index=idx,
                        parse_result=None,
                        gate_report=None,
                        exception=str(exc),
                    )
                )
                continue

            gate_report = run_quality_gates(parse_result)
            attempts.append(
                AttemptRecord(
                    parser_id=parser.parser_id,
                    attempt_index=idx,
                    parse_result=parse_result,
                    gate_report=gate_report,
                    exception=None,
                )
            )

            if gate_report.passed:
                winner_index = idx
                winning_parse_result = parse_result
                winning_parser_id = parser.parser_id
                break

        if winner_index is None:
            terminal_status = TerminalStatus.FALLBACK_EXHAUSTED
        elif winner_index == 0:
            terminal_status = TerminalStatus.AUTO_ACCEPTED
        else:
            terminal_status = TerminalStatus.AUTO_REFINED

        return OrchestratorResult(
            terminal_status=terminal_status,
            successful_parser_id=winning_parser_id,
            final_parse_result=winning_parse_result,
            attempts=tuple(attempts),
        )
