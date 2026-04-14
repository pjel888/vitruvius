from __future__ import annotations

import abc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar


@dataclass(kw_only=True)
class ParserTelemetry:
    parser_id: str
    attempt_index: int
    duration_ms: int
    pages_total: int
    pages_processed: int
    page_coverage_ratio: float
    text_length: int
    md_length: int
    headers: int
    tables: int
    images: int
    captions: int
    assets_extracted: list[str] = field(default_factory=list)
    ocr_applied: bool
    confidence: float
    valid: bool
    error: str | None = field(default=None)


@dataclass
class ParseResult:
    markdown_text: str
    telemetry: ParserTelemetry
    sidecar_metadata: dict[str, Any] = field(default_factory=dict)


class BaseParser(abc.ABC):
    parser_id: ClassVar[str]
    parser_version: ClassVar[str]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if abc.ABC in cls.__bases__:
            return
        parser_id = getattr(cls, "parser_id", None)
        if not parser_id:
            raise TypeError(
                f"{cls.__name__} must define a non-empty class attribute 'parser_id'"
            )
        parser_version = getattr(cls, "parser_version", None)
        if not parser_version:
            raise TypeError(
                f"{cls.__name__} must define a non-empty class attribute 'parser_version'"
            )

    @abc.abstractmethod
    def parse(self, source_path: Path, work_dir: Path) -> ParseResult: ...
