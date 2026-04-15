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


@dataclass(kw_only=True)
class ParseResult:
    markdown_text: str
    telemetry: ParserTelemetry
    sidecar_metadata: dict[str, Any] = field(default_factory=dict)
    # Sprint CLEANUP-1 C3.1 — per-page failure indices (1-indexed). Empty
    # by default so existing callers pass through unchanged; the
    # ``p1b_page_isolation`` flag opts RustPdfParser into surfacing the
    # page numbers lopdf could not decode.
    failed_pages: list[int] = field(default_factory=list)


class BaseParser(abc.ABC):
    parser_id: ClassVar[str]
    parser_version: ClassVar[str]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Skip the check for any class that is still abstract: either it
        # declares new abstractmethods of its own, or it inherits unresolved
        # ones from a parent (note: __abstractmethods__ is not yet set on cls
        # at __init_subclass__ time, so we must compute this ourselves).
        own_abstracts = {
            name
            for name, val in cls.__dict__.items()
            if getattr(val, "__isabstractmethod__", False)
        }
        inherited_abstracts: frozenset[str] = frozenset().union(
            *(getattr(base, "__abstractmethods__", frozenset()) for base in cls.__mro__[1:])
        )
        resolved = {
            name
            for name in inherited_abstracts
            if name in cls.__dict__
            and not getattr(cls.__dict__[name], "__isabstractmethod__", False)
        }
        if own_abstracts or (inherited_abstracts - resolved):
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
