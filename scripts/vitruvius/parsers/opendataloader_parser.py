from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .base_parser import BaseParser, ParseResult, ParserTelemetry


class OpenDataLoaderParser(BaseParser):
    """Wraps opendataloader_pdf.convert behind the Phase 1B BaseParser interface.

    Lazy-imports opendataloader_pdf inside parse() so constructing the class
    doesn't force the dependency on callers who only want the types.
    """

    parser_id = "opendataloader_pdf"
    parser_version = "0.1.0"

    def _build_failure_telemetry(
        self,
        *,
        duration_ms: int,
        error: str,
        file_type: str = "",
    ) -> ParserTelemetry:
        return ParserTelemetry(
            parser_id=self.parser_id,
            attempt_index=0,
            duration_ms=duration_ms,
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
            confidence=0.0,
            valid=False,
            error=error,
        )

    def _build_success_telemetry(
        self,
        *,
        duration_ms: int,
        markdown_text: str,
        sidecar_json: dict[str, Any],
    ) -> ParserTelemetry:
        pages_total = int(
            sidecar_json.get("pages_total", sidecar_json.get("page_count", 0))
        )
        pages_processed = int(sidecar_json.get("pages_processed", pages_total))
        page_coverage_ratio = pages_processed / pages_total if pages_total > 0 else 0.0
        text_length = int(sidecar_json.get("text_length", 0))
        md_length = len(markdown_text)
        headers = sum(
            1 for line in markdown_text.splitlines() if line.lstrip().startswith("#")
        )
        tables = sum(
            1
            for line in markdown_text.splitlines()
            if "|" in line and all(c in "| :-" for c in line.strip())
        )
        images = markdown_text.count("![")
        return ParserTelemetry(
            parser_id=self.parser_id,
            attempt_index=0,
            duration_ms=duration_ms,
            pages_total=pages_total,
            pages_processed=pages_processed,
            page_coverage_ratio=page_coverage_ratio,
            text_length=text_length,
            md_length=md_length,
            headers=headers,
            tables=tables,
            images=images,
            captions=0,
            ocr_applied=False,
            confidence=1.0,
            valid=True,
            error=None,
        )

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        start = time.monotonic()
        work_dir.mkdir(parents=True, exist_ok=True)

        import opendataloader_pdf  # noqa: PLC0415

        try:
            opendataloader_pdf.convert(
                input_path=[str(source_path)],
                output_dir=str(work_dir),
                format="markdown,json",
            )
        except Exception as exc:
            duration_ms = int((time.monotonic() - start) * 1000)
            return ParseResult(
                markdown_text="",
                telemetry=self._build_failure_telemetry(
                    duration_ms=duration_ms,
                    error=str(exc),
                ),
                sidecar_metadata={
                    "file_type": source_path.suffix.lstrip(".").lower()
                },
            )

        md_path = work_dir / f"{source_path.stem}.md"
        json_path = work_dir / f"{source_path.stem}.json"

        if not md_path.exists() or not json_path.exists():
            duration_ms = int((time.monotonic() - start) * 1000)
            return ParseResult(
                markdown_text="",
                telemetry=self._build_failure_telemetry(
                    duration_ms=duration_ms,
                    error=(
                        f"opendataloader_pdf did not produce expected outputs:"
                        f" {md_path}, {json_path}"
                    ),
                ),
                sidecar_metadata={
                    "file_type": source_path.suffix.lstrip(".").lower()
                },
            )

        markdown_text = md_path.read_text(encoding="utf-8")
        sidecar_json = json.loads(json_path.read_text(encoding="utf-8"))
        duration_ms = int((time.monotonic() - start) * 1000)

        return ParseResult(
            markdown_text=markdown_text,
            telemetry=self._build_success_telemetry(
                duration_ms=duration_ms,
                markdown_text=markdown_text,
                sidecar_json=sidecar_json,
            ),
            sidecar_metadata={
                "file_type": source_path.suffix.lstrip(".").lower(),
                "raw_sidecar": sidecar_json,
            },
        )
