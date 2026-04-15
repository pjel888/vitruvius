from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Sequence

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


@dataclass(kw_only=True, frozen=True)
class BatchJob:
    """Sprint 1B-M2 Task 2 — a single document job for
    :meth:`ParserOrchestrator.process_batch`.
    """
    source_path: Path
    doc_class: DocumentClass
    work_dir: Path


class ParserOrchestrator:
    def __init__(
        self,
        parser_chains: dict[DocumentClass, list[BaseParser]],
        preprocessors: dict[DocumentClass, object] | None = None,
    ) -> None:
        self._chains = {k: list(v) for k, v in parser_chains.items()}
        self._preprocessors: dict[DocumentClass, object] = dict(preprocessors or {})

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

        # Sprint 1B-M1 Task 4 — run the registered preprocessor for
        # this doc_class first (if any). A failed preprocessor short-
        # circuits to FALLBACK_EXHAUSTED with the preprocessor's error
        # captured as the only AttemptRecord. A successful preprocessor
        # replaces source_path with its output (typically an
        # Office → PDF conversion) before the parser chain runs.
        current_source = source_path
        pre_attempts: list[AttemptRecord] = []
        preprocessor = self._preprocessors.get(doc_class)
        if preprocessor is not None:
            pre_result = preprocessor.preprocess(
                source_path=current_source, workdir=work_dir
            )
            pre_attempts.append(
                AttemptRecord(
                    parser_id=getattr(
                        preprocessor, "preprocessor_id", "preprocessor"
                    ),
                    attempt_index=-1,
                    parse_result=None,
                    gate_report=None,
                    exception=pre_result.error,
                )
            )
            if pre_result.pdf_path is None:
                return OrchestratorResult(
                    terminal_status=TerminalStatus.FALLBACK_EXHAUSTED,
                    successful_parser_id=None,
                    final_parse_result=None,
                    attempts=tuple(pre_attempts),
                )
            current_source = pre_result.pdf_path

        attempts: list[AttemptRecord] = list(pre_attempts)
        winner_index: int | None = None
        winning_parse_result: ParseResult | None = None
        winning_parser_id: str | None = None

        for idx, parser in enumerate(chain):
            try:
                parse_result = parser.parse(
                    source_path=current_source, work_dir=work_dir
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

    def process_batch(
        self,
        *,
        jobs: Sequence[BatchJob],
        max_workers: int | None = None,
    ) -> tuple[OrchestratorResult, ...]:
        """Sprint 1B-M2 Task 2 — batch-process multiple documents.

        Returns results in input order. ``max_workers`` is accepted
        for API compatibility with a future ProcessPoolExecutor
        implementation; the current implementation runs jobs
        sequentially because :class:`BaseParser` subclasses hold
        non-pickleable lazy-imported state (docling, ocrmypdf) that
        can't currently cross a process boundary. The sequential
        loop still benefits from the factory / chain pre-registration
        at construction time — the slowdown is I/O-bound work, not
        CPU-bound.

        Upgrade path: once all parsers are pickle-safe, swap the
        loop body for a :class:`concurrent.futures.ProcessPoolExecutor`
        invocation. The public API stays the same.
        """
        _ = max_workers  # reserved for future ProcessPool upgrade
        if not jobs:
            return ()
        results = tuple(
            self.process(
                source_path=job.source_path,
                doc_class=job.doc_class,
                work_dir=job.work_dir,
            )
            for job in jobs
        )
        return results
