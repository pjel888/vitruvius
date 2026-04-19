"""Evidence span seed set — ≥10 spans, 100% resolvable.

This test closes Gate 3 of the KG transition readiness plan by proving
that the selector resolver can resolve every seed span against real text.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from vitruvius.kg.schemas import EvidenceSpan, MarkdownRangeSelector, TextRangeSelector
from vitruvius.kg.selector_resolver import SelectorResolver


SEED_MARKDOWN = """\
---
id: law-pd-1096-national-building-code
title: National Building Code of the Philippines
---

# National Building Code of the Philippines

## Overview

This law governs building construction nationwide.
It applies to all private and public buildings.

## Scope

The code covers structural safety, fire safety, and accessibility.

### Structural Safety

Buildings must withstand dead loads, live loads, and wind loads.

### Fire Safety

Fire exits must be clearly marked and unobstructed.

## Definitions

### Building Permit

A building permit is an official approval issued by the Building Official.

### Occupancy Classification

Groups classified according to use or character of occupancy.

## Requirements

All buildings must comply with the minimum standards set forth herein.
"""


@pytest.fixture
def seed_repo(tmp_path: Path) -> Path:
    """Create a minimal repo with one canonical source for seed spans."""
    raw_dir = tmp_path / "001_Raw-Source-Layer" / "001-Laws" / "PD-1096"
    raw_dir.mkdir(parents=True)
    (raw_dir / "pd-1096-national-building-code.md").write_text(SEED_MARKDOWN, encoding="utf-8")
    return tmp_path


@pytest.fixture
def resolver(seed_repo: Path) -> SelectorResolver:
    return SelectorResolver(seed_repo / "001_Raw-Source-Layer")


# ---------------------------------------------------------------------------
# Seed spans — all use MarkdownRangeSelector with correct heading paths.
# heading_path length = heading level.  line_start/line_end are 1-indexed
# relative to the heading block (line 1 = the heading itself).
# ---------------------------------------------------------------------------

SEED_SPANS = [
    # TextRangeSelector on frontmatter
    EvidenceSpan(
        id="span-seed-001",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=TextRangeSelector(char_start=0, char_end=3, quote="---"),
        quote="---",
        normalized_text="---",
        parser="seed",
        checksum="0a" * 32,
    ),
    # Level-1 heading block
    EvidenceSpan(
        id="span-seed-002",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=MarkdownRangeSelector(
            heading_path=["National Building Code of the Philippines"],
            line_start=1,
            line_end=1,
            quote="National Building Code of the Philippines",
        ),
        quote="# National Building Code of the Philippines",
        normalized_text="# National Building Code of the Philippines",
        parser="seed",
        checksum="0b" * 32,
    ),
    # Level-2 heading: Overview — first content line
    EvidenceSpan(
        id="span-seed-003",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=MarkdownRangeSelector(
            heading_path=["", "Overview"],
            line_start=3,
            line_end=3,
        ),
        quote="This law governs building construction nationwide.",
        normalized_text="This law governs building construction nationwide.",
        parser="seed",
        checksum="0c" * 32,
    ),
    # Level-2 heading: Scope
    EvidenceSpan(
        id="span-seed-004",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=MarkdownRangeSelector(
            heading_path=["", "Scope"],
            line_start=3,
            line_end=3,
        ),
        quote="The code covers structural safety, fire safety, and accessibility.",
        normalized_text="The code covers structural safety, fire safety, and accessibility.",
        parser="seed",
        checksum="0d" * 32,
    ),
    # Level-3 heading: Structural Safety
    EvidenceSpan(
        id="span-seed-005",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=MarkdownRangeSelector(
            heading_path=["", "", "Structural Safety"],
            line_start=3,
            line_end=3,
        ),
        quote="Buildings must withstand dead loads, live loads, and wind loads.",
        normalized_text="Buildings must withstand dead loads, live loads, and wind loads.",
        parser="seed",
        checksum="0e" * 32,
    ),
    # Level-3 heading: Fire Safety
    EvidenceSpan(
        id="span-seed-006",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=MarkdownRangeSelector(
            heading_path=["", "", "Fire Safety"],
            line_start=3,
            line_end=3,
        ),
        quote="Fire exits must be clearly marked and unobstructed.",
        normalized_text="Fire exits must be clearly marked and unobstructed.",
        parser="seed",
        checksum="0f" * 32,
    ),
    # Level-3 heading: Building Permit
    EvidenceSpan(
        id="span-seed-007",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=MarkdownRangeSelector(
            heading_path=["", "", "Building Permit"],
            line_start=3,
            line_end=3,
        ),
        quote="A building permit is an official approval issued by the Building Official.",
        normalized_text="A building permit is an official approval issued by the Building Official.",
        parser="seed",
        checksum="01" * 32,
    ),
    # Level-3 heading: Occupancy Classification
    EvidenceSpan(
        id="span-seed-008",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=MarkdownRangeSelector(
            heading_path=["", "", "Occupancy Classification"],
            line_start=3,
            line_end=3,
        ),
        quote="Groups classified according to use or character of occupancy.",
        normalized_text="Groups classified according to use or character of occupancy.",
        parser="seed",
        checksum="02" * 32,
    ),
    # Level-2 heading: Requirements
    EvidenceSpan(
        id="span-seed-009",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=MarkdownRangeSelector(
            heading_path=["", "Requirements"],
            line_start=3,
            line_end=3,
        ),
        quote="All buildings must comply with the minimum standards set forth herein.",
        normalized_text="All buildings must comply with the minimum standards set forth herein.",
        parser="seed",
        checksum="03" * 32,
    ),
    # Overview second content line
    EvidenceSpan(
        id="span-seed-010",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=MarkdownRangeSelector(
            heading_path=["", "Overview"],
            line_start=4,
            line_end=4,
        ),
        quote="It applies to all private and public buildings.",
        normalized_text="It applies to all private and public buildings.",
        parser="seed",
        checksum="04" * 32,
    ),
    # TextRangeSelector on title inside frontmatter
    EvidenceSpan(
        id="span-seed-011",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=TextRangeSelector(char_start=50, char_end=91, quote="National Building Code of the Philippines"),
        quote="National Building Code of the Philippines",
        normalized_text="National Building Code of the Philippines",
        parser="seed",
        checksum="05" * 32,
    ),
    # Level-2 heading: Definitions — first content line (empty, so line 3)
    EvidenceSpan(
        id="span-seed-012",
        document_id="doc-pd-1096-national-building-code",
        document_version_id="docv-pd-1096-national-building-code-v1",
        selector=MarkdownRangeSelector(
            heading_path=["", "Definitions"],
            line_start=3,
            line_end=3,
        ),
        quote="### Building Permit",
        normalized_text="### Building Permit",
        parser="seed",
        checksum="06" * 32,
    ),
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestSeedSpanResolution:
    """Each seed span must resolve without exception and match its quote."""

    @pytest.mark.parametrize("span", SEED_SPANS, ids=lambda s: s.id)
    def test_span_resolves(self, resolver: SelectorResolver, span: EvidenceSpan) -> None:
        resolved = resolver.resolve(span)
        assert resolved, f"Span {span.id} resolved to empty string"
        # Quote must be present in resolved text (fuzzy match)
        assert span.quote.lower() in resolved.lower(), (
            f"Span {span.id} quote not found in resolved text: {resolved!r}"
        )

    def test_all_spans_resolve(self, resolver: SelectorResolver) -> None:
        """Aggregate gate: every seed span resolves successfully."""
        failures = []
        for span in SEED_SPANS:
            try:
                resolved = resolver.resolve(span)
                if not resolved or span.quote.lower() not in resolved.lower():
                    failures.append((span.id, "quote mismatch", resolved))
            except Exception as exc:
                failures.append((span.id, type(exc).__name__, str(exc)))

        assert not failures, f"Failed spans: {failures}"
        assert len(SEED_SPANS) >= 10, "Seed set must contain at least 10 spans"
