---
plan_id: phase-1b-modernization-tranche-1
phase: 1B
title: "Phase 1B Modernization — Tranche 1 (Docling + LibreOffice)"
status: active
priority: medium
sprint: "Sprint 1B-M1 (post-HP.3-R)"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
prerequisites:
  - Phase 1B Foundation shipped (Sprint C, 2026-04-14) — `BaseParser`, `ParserOrchestrator`, `document_taxonomy`, `quality_gates` all exist
  - docling installed (Sprint WIKI dep, confirmed at plan-write time)
  - LibreOffice installed at the system level (already used by `office.py`)
related_plans:
  - phase-1b-multi-parser-integration-plan.md (parent design spec, design_spec type)
  - ../09_archive/plans/2026-04-15-rocksdb-kv-migration-plan.md (pattern reference)
supersedes: none
---

# Phase 1B Modernization — Tranche 1 (Docling + LibreOffice) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the zero-new-heavy-dependency portion of Phase 1B Modernization — a `DoclingParser` that implements the `BaseParser` interface, a `LibreOfficePreprocessor` that reuses the existing `office.py::find_soffice_executable` discovery logic, a post-LibreOffice quality gate (GATE-005), and orchestrator wiring so the `hybrid_pdf` and `office_doc` document classes route through the new parsers behind feature flags.

**Architecture:** Thin wrappers that delegate to existing battle-tested code. `DoclingParser` imports the `scripts/vitruvius/wiki/docling_parser.py::convert_pdf_to_markdown` function from Sprint WIKI and reshapes its `DoclingParseResult` into the Phase 1B `ParseResult` + `ParserTelemetry` contract. `LibreOfficePreprocessor` is a new `Preprocessor` subclass (not a `BaseParser`) that converts `.docx` / `.pptx` → `.pdf` before a downstream parser runs. Both are gated behind feature flags that default false so the pre-tranche pipeline is byte-identical.

**Tech Stack:**
- `docling 2.88.x` — already installed via Sprint WIKI
- System `soffice` binary — already required by the existing `office.py` module
- Existing `BaseParser` / `ParseResult` / `ParserTelemetry` types from `scripts/vitruvius/parsers/base_parser.py`
- Existing `ParserOrchestrator` from `scripts/vitruvius/parsers/orchestrator.py`
- Existing `find_soffice_executable` helper from `scripts/vitruvius/office.py`

---

## Scope & Non-Goals

### In scope (Tranche 1)

1. **`DoclingParser(BaseParser)`** — `parsers/docling_parser.py`, implements `parse(source_path) -> ParseResult`. Delegates to the Sprint WIKI docling wrapper for conversion, maps the result into the Phase 1B telemetry contract.
2. **`LibreOfficePreprocessor`** — `parsers/libreoffice_preprocessor.py`, converts Office documents (.docx, .pptx, .odt) to PDF via the existing soffice discovery logic. Emits a `PreprocessResult` dataclass that the orchestrator uses as the new input for the downstream parser chain.
3. **`GATE-005` — post-LibreOffice sanity check** — added to `parsers/quality_gates.py`. Verifies the produced PDF has ≥1 page and non-empty text content.
4. **Orchestrator wiring** — `parsers/orchestrator.py::ParserOrchestrator` accepts a `preprocessors: Sequence[Preprocessor]` list and runs them before dispatching to the parser chain. Adds the `hybrid_pdf` → `[docling, opendataloader]` chain and the `office_doc` → `[libreoffice_preprocessor, docling]` chain.
5. **Two feature flags** — `p1b_docling_parser` and `p1b_libreoffice_preprocessor`, both default `false`. Registered in `config/vitruvius.yaml` and `scripts/tests/test_features.py::EXPECTED_FLAGS`.
6. **Docs + AD-031** — `.ai/10_state/decisions.md` appends AD-031 with the tranche 1 scope, the deferred tranche 2 items, and commit SHAs. `.ai/00_system/pipeline-overview.md` adds a `p1b_*` flag family row to the flag table.

### Out of scope (deferred to Tranche 2 or future)

- **MarkerParser** — requires `marker-pdf 1.10.2` which pulls in `torch` + transformer models (~2-5 GB). Not suitable for the 8 GB M2 default profile without explicit opt-in.
- **SuryaParser / OCRPreprocessor** — same issue: `surya-ocr 0.17.1` + `torch` + surya model weights.
- **ProcessPoolExecutor dynamic resource allocation** — only meaningful once we have 3+ parsers in the chain (with only Docling + LibreOffice + OpenDataLoader in scope, the throughput win is marginal).
- **Golden Corpus benchmark** — same reasoning: the benchmark compares parsers against each other, so it needs the full parser set.
- **Ranger Audit Review Payload (Tranche 1 §12.1 of the design spec)** — depends on Phase 7 Supabase integration which doesn't exist yet.
- **Page-level isolation / chunked fallback** — complexity budget doesn't justify it until we see real fallback failures on the current corpus.

These out-of-scope items are captured in a follow-up plan `2026-04-XX-phase-1b-modernization-tranche-2.md` that will be created when 8 GB M2 ML-dep feasibility is verified.

---

## File Structure

### New files

| Path | Responsibility |
|---|---|
| `scripts/vitruvius/parsers/docling_parser.py` | `DoclingParser(BaseParser)` class. ~120 lines. |
| `scripts/vitruvius/parsers/libreoffice_preprocessor.py` | `LibreOfficePreprocessor` class + `PreprocessResult` dataclass. ~140 lines. |
| `scripts/tests/test_docling_parser.py` | 5 tests: roundtrip, missing-file, non-PDF, Docling-raises, telemetry-shape. |
| `scripts/tests/test_libreoffice_preprocessor.py` | 4 tests: happy-path (mocked soffice), soffice-missing, soffice-fails, telemetry. |
| `scripts/tests/test_orchestrator_chains.py` | 3 tests: hybrid_pdf chain routing, office_doc chain routing, flag-OFF no-op. |

### Modified files

| Path | Reason |
|---|---|
| `scripts/vitruvius/parsers/__init__.py` | Re-export `DoclingParser`, `LibreOfficePreprocessor`, `PreprocessResult` |
| `scripts/vitruvius/parsers/quality_gates.py` | Add `GATE-005` (post-LibreOffice PDF sanity check) |
| `scripts/vitruvius/parsers/orchestrator.py` | Accept `preprocessors` parameter; add chain dispatch for `hybrid_pdf` + `office_doc`; feature-flag branching |
| `config/vitruvius.yaml` | Add `p1b_docling_parser: false`, `p1b_libreoffice_preprocessor: false` |
| `scripts/tests/test_features.py` | Add both flags to `EXPECTED_FLAGS` + 2 default-false tests |
| `.ai/10_state/decisions.md` | Append AD-031 |
| `.ai/00_system/pipeline-overview.md` | Add `p1b_*` flag family row |
| `.ai/03_plans/INDEX.md` | Add META row for this plan after Sprint AUDIT-1 row |

### Explicitly NOT touched

- `scripts/vitruvius/wiki/docling_parser.py` — stays as the Sprint WIKI facade; Tranche 1 only depends on it, doesn't modify it.
- `scripts/vitruvius/office.py` — stays as the existing Office→PDF path used by `run_convert`. `LibreOfficePreprocessor` imports `find_soffice_executable` from it, doesn't modify it.
- `scripts/pipeline_cli.py` — no new CLI subcommands in Tranche 1. The orchestrator is called internally; CLI-facing wiring lands in Tranche 2 or a follow-up.

---

## Pre-Task Evidence

Verified at plan-write time:

- `scripts/vitruvius/parsers/` has the Foundation modules shipped in Sprint C (2026-04-14): `base_parser.py` (75 lines), `orchestrator.py` (108 lines), `quality_gates.py` (163 lines), `opendataloader_parser.py` (147 lines), `document_taxonomy.py`, `__init__.py`.
- `scripts/vitruvius/wiki/docling_parser.py` exists (Sprint WIKI) with `convert_pdf_to_markdown(pdf_path) -> DoclingParseResult`. The function already handles: missing file, non-PDF suffix, Docling internal raises. Lazy imports `docling.document_converter`.
- `scripts/vitruvius/office.py` has `find_soffice_executable() -> str` that returns the system soffice path. This is the canonical discovery logic that `LibreOfficePreprocessor` will reuse.
- `docling` is installed: `python3.11 -c "import docling; print(docling)"` succeeds.
- Current test suite: **1396 passed, 1 skipped**. After this plan: expected **+14 tests → 1410 passed, 1 skipped**.

---

## Dispatch Order

Tranche 1 is small enough to execute sequentially without waves. Task order:

1. **Task 1** — `DoclingParser(BaseParser)` class + 5 tests
2. **Task 2** — `LibreOfficePreprocessor` class + 4 tests
3. **Task 3** — `GATE-005` post-LibreOffice quality gate + regression test
4. **Task 4** — Orchestrator wiring + `p1b_*` feature flags + 3 chain-routing tests
5. **Task 5** — Docs + AD-031 + INDEX.md + plan archival (orchestrator-held atomic commit)

Per-task commits (one commit per task) for safe bisect, following the Sprint HP.3-R pattern.

---

## Task 1: `DoclingParser(BaseParser)` class + tests

**Goal:** Wrap the Sprint WIKI docling facade in a `BaseParser` subclass that satisfies the Phase 1B contract from §6 of the parent design spec.

### Files

- **Create:** `/Users/philiplewis/vitruvius/scripts/vitruvius/parsers/docling_parser.py`
- **Create:** `/Users/philiplewis/vitruvius/scripts/tests/test_docling_parser.py`

### Step 1: Write the failing tests first

Create `/Users/philiplewis/vitruvius/scripts/tests/test_docling_parser.py` with EXACTLY this content:

```python
"""Sprint 1B-M1 Task 1 — DoclingParser tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from vitruvius.parsers.base_parser import BaseParser, ParseResult, ParserTelemetry
from vitruvius.parsers.docling_parser import DoclingParser


def test_docling_parser_is_base_parser() -> None:
    parser = DoclingParser()
    assert isinstance(parser, BaseParser)
    assert parser.parser_id == "docling"


def test_docling_parser_missing_file_returns_failure(tmp_path: Path) -> None:
    parser = DoclingParser()
    missing = tmp_path / "does_not_exist.pdf"
    result = parser.parse(source_path=missing)
    assert isinstance(result, ParseResult)
    assert result.telemetry.valid is False
    assert "missing file" in (result.telemetry.error or "").lower()
    assert result.markdown == ""


def test_docling_parser_rejects_non_pdf(tmp_path: Path) -> None:
    parser = DoclingParser()
    docx = tmp_path / "sample.docx"
    docx.write_text("not really a docx")
    result = parser.parse(source_path=docx)
    assert result.telemetry.valid is False
    assert "not a pdf" in (result.telemetry.error or "").lower()


def test_docling_parser_happy_path_mocks_wiki(tmp_path: Path) -> None:
    """Mock the Sprint WIKI docling wrapper so the test doesn't load Docling itself."""
    from vitruvius.wiki.docling_parser import DoclingParseResult as WikiResult

    parser = DoclingParser()
    pdf = tmp_path / "fake.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")  # minimum-viable PDF marker

    fake_result = WikiResult(
        markdown="# Title\n\nPage body text with several words.",
        heading_count=1,
        table_count=0,
        error=None,
    )

    with patch(
        "vitruvius.parsers.docling_parser.convert_pdf_to_markdown",
        return_value=fake_result,
    ):
        result = parser.parse(source_path=pdf)

    assert result.telemetry.valid is True
    assert result.telemetry.parser_id == "docling"
    assert result.telemetry.error is None
    assert result.markdown == "# Title\n\nPage body text with several words."
    assert result.telemetry.headers == 1
    assert result.telemetry.tables == 0
    assert result.telemetry.md_length == len(result.markdown)


def test_docling_parser_wraps_wiki_error(tmp_path: Path) -> None:
    from vitruvius.wiki.docling_parser import DoclingParseResult as WikiResult

    parser = DoclingParser()
    pdf = tmp_path / "corrupt.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")

    fake_result = WikiResult(
        markdown="",
        heading_count=0,
        table_count=0,
        error="Docling internal failure: bad xref table",
    )

    with patch(
        "vitruvius.parsers.docling_parser.convert_pdf_to_markdown",
        return_value=fake_result,
    ):
        result = parser.parse(source_path=pdf)

    assert result.telemetry.valid is False
    assert "Docling internal failure" in (result.telemetry.error or "")
    assert result.markdown == ""
```

### Step 2: Run the tests (must FAIL)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_docling_parser.py -v 2>&1 | tail -20
```

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.parsers.docling_parser'`.

### Step 3: Implement `DoclingParser`

Create `/Users/philiplewis/vitruvius/scripts/vitruvius/parsers/docling_parser.py` with EXACTLY this content:

```python
"""Sprint 1B-M1 Task 1 — DoclingParser (BaseParser implementation).

Thin adapter around :func:`vitruvius.wiki.docling_parser.convert_pdf_to_markdown`
that reshapes the Sprint WIKI :class:`DoclingParseResult` into the Phase 1B
:class:`BaseParser` contract.

Delegation pattern: the heavy Docling import lives inside the wiki
module. This file only imports the wiki wrapper, so ``from
vitruvius.parsers.docling_parser import DoclingParser`` is cheap
even when docling is not installed (the wrapper's lazy-import
error only surfaces at :meth:`parse` time).
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from vitruvius.parsers.base_parser import BaseParser, ParseResult, ParserTelemetry
from vitruvius.wiki.docling_parser import convert_pdf_to_markdown


class DoclingParser(BaseParser):
    """Parser chain entry for docling-backed PDF conversion."""

    parser_id = "docling"
    parser_version = "wiki-1.0"

    def parse(self, *, source_path: Path, attempt_index: int = 0) -> ParseResult:
        start = time.perf_counter()
        wiki_result = convert_pdf_to_markdown(pdf_path=source_path)
        duration_ms = int((time.perf_counter() - start) * 1000)

        if wiki_result.error is not None:
            telemetry = ParserTelemetry(
                parser_id=self.parser_id,
                attempt_index=attempt_index,
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
                error=wiki_result.error,
            )
            return ParseResult(markdown="", sidecar_json={}, telemetry=telemetry)

        markdown = wiki_result.markdown
        telemetry = ParserTelemetry(
            parser_id=self.parser_id,
            attempt_index=attempt_index,
            duration_ms=duration_ms,
            pages_total=0,  # docling facade does not report this today
            pages_processed=0,
            page_coverage_ratio=1.0 if markdown else 0.0,
            text_length=len(markdown),
            md_length=len(markdown),
            headers=wiki_result.heading_count,
            tables=wiki_result.table_count,
            images=0,
            captions=0,
            ocr_applied=False,
            confidence=1.0 if markdown else 0.0,
            valid=bool(markdown),
            error=None if markdown else "empty markdown",
        )

        sidecar: dict[str, Any] = {
            "parser_id": self.parser_id,
            "parser_version": self.parser_version,
            "heading_count": wiki_result.heading_count,
            "table_count": wiki_result.table_count,
        }

        return ParseResult(markdown=markdown, sidecar_json=sidecar, telemetry=telemetry)
```

**Critical note:** this file imports `convert_pdf_to_markdown` at module top from the Sprint WIKI wrapper. That wrapper itself lazy-imports `docling.document_converter` inside its body, so the import chain is: `parsers.docling_parser` (top-level import safe) → `wiki.docling_parser` (top-level import safe) → `docling.document_converter` (lazy, triggered on `convert()` call). Tests mock `convert_pdf_to_markdown` via `unittest.mock.patch`, so they never touch the real Docling library.

### Step 4: Re-export from `parsers/__init__.py`

```bash
cd /Users/philiplewis/vitruvius && grep -n 'DoclingParser\|__all__' scripts/vitruvius/parsers/__init__.py
```

If `__all__` exists or there's a re-export block, append `DoclingParser` to it. If the file is minimal, add:

```python
from vitruvius.parsers.docling_parser import DoclingParser

__all__ = [..., "DoclingParser"]  # keep existing entries
```

Inspect the existing file shape and match its re-export convention.

### Step 5: Run the tests (must PASS)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_docling_parser.py -v 2>&1 | tail -20
```

Expected: 5 passed.

### Step 6: Full suite regression

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -10
```

Expected: `1401 passed, 1 skipped` (baseline 1396 + 5 new).

### Step 7: Commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/parsers/docling_parser.py \
  scripts/vitruvius/parsers/__init__.py \
  scripts/tests/test_docling_parser.py
git commit -m "$(cat <<'EOF'
feat(parsers): Sprint 1B-M1 Task 1 — DoclingParser(BaseParser)

Implements the Phase 1B BaseParser interface as a thin adapter
around the Sprint WIKI docling facade
(vitruvius.wiki.docling_parser.convert_pdf_to_markdown). The
wiki module handles all the error cases (missing file, non-PDF,
Docling internal raise) and the adapter reshapes its result into
the §6 telemetry contract from the Phase 1B design spec.

5 tests cover: is-a-BaseParser, missing file, non-PDF rejection,
happy-path markdown+telemetry, wiki-error propagation. Tests
mock convert_pdf_to_markdown so they don't load Docling itself.

Feature flag wiring and orchestrator chain registration land in
Task 4.

Part of the Phase 1B Modernization Tranche 1 plan at
.ai/03_plans/2026-04-15-phase-1b-modernization-tdd-plan.md.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: `LibreOfficePreprocessor` class + tests

**Goal:** A new `Preprocessor` base class (parallel to `BaseParser`) that converts Office documents to PDF before a downstream parser runs. Reuses the existing `office.py::find_soffice_executable` discovery logic.

### Files

- **Create:** `/Users/philiplewis/vitruvius/scripts/vitruvius/parsers/libreoffice_preprocessor.py`
- **Create:** `/Users/philiplewis/vitruvius/scripts/tests/test_libreoffice_preprocessor.py`

### Step 1: Write the failing tests first

Create `/Users/philiplewis/vitruvius/scripts/tests/test_libreoffice_preprocessor.py` with EXACTLY this content:

```python
"""Sprint 1B-M1 Task 2 — LibreOfficePreprocessor tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from vitruvius.parsers.libreoffice_preprocessor import (
    LibreOfficePreprocessor,
    PreprocessResult,
)


def test_preprocessor_missing_soffice_returns_failure(tmp_path: Path) -> None:
    pre = LibreOfficePreprocessor()
    docx = tmp_path / "doc.docx"
    docx.write_text("stub")

    with patch(
        "vitruvius.parsers.libreoffice_preprocessor.find_soffice_executable",
        side_effect=FileNotFoundError("soffice missing"),
    ):
        result = pre.preprocess(source_path=docx, workdir=tmp_path)

    assert isinstance(result, PreprocessResult)
    assert result.pdf_path is None
    assert result.error is not None
    assert "soffice" in result.error.lower()


def test_preprocessor_rejects_non_office_extension(tmp_path: Path) -> None:
    pre = LibreOfficePreprocessor()
    pdf = tmp_path / "already.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")

    result = pre.preprocess(source_path=pdf, workdir=tmp_path)
    assert result.pdf_path is None
    assert "not an office document" in (result.error or "").lower()


def test_preprocessor_happy_path_mocks_soffice(tmp_path: Path) -> None:
    pre = LibreOfficePreprocessor()
    docx = tmp_path / "doc.docx"
    docx.write_text("stub")

    expected_pdf = tmp_path / "doc.pdf"

    def fake_run(*args, **kwargs):
        # Simulate soffice creating the output PDF.
        expected_pdf.write_bytes(b"%PDF-1.4\n")
        class _Ret:
            returncode = 0
            stdout = b""
            stderr = b""
        return _Ret()

    with patch(
        "vitruvius.parsers.libreoffice_preprocessor.find_soffice_executable",
        return_value="/usr/bin/soffice",
    ), patch(
        "vitruvius.parsers.libreoffice_preprocessor.subprocess.run",
        side_effect=fake_run,
    ):
        result = pre.preprocess(source_path=docx, workdir=tmp_path)

    assert result.pdf_path == expected_pdf
    assert result.error is None
    assert result.duration_ms >= 0


def test_preprocessor_wraps_soffice_failure(tmp_path: Path) -> None:
    pre = LibreOfficePreprocessor()
    docx = tmp_path / "doc.docx"
    docx.write_text("stub")

    def fake_run(*args, **kwargs):
        class _Ret:
            returncode = 77
            stdout = b""
            stderr = b"soffice: conversion failed"
        return _Ret()

    with patch(
        "vitruvius.parsers.libreoffice_preprocessor.find_soffice_executable",
        return_value="/usr/bin/soffice",
    ), patch(
        "vitruvius.parsers.libreoffice_preprocessor.subprocess.run",
        side_effect=fake_run,
    ):
        result = pre.preprocess(source_path=docx, workdir=tmp_path)

    assert result.pdf_path is None
    assert "conversion failed" in (result.error or "").lower()
```

### Step 2: Run the tests (must FAIL)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_libreoffice_preprocessor.py -v 2>&1 | tail -15
```

Expected: FAIL with `ModuleNotFoundError: No module named 'vitruvius.parsers.libreoffice_preprocessor'`.

### Step 3: Implement `LibreOfficePreprocessor`

Create `/Users/philiplewis/vitruvius/scripts/vitruvius/parsers/libreoffice_preprocessor.py` with EXACTLY this content:

```python
"""Sprint 1B-M1 Task 2 — LibreOffice preprocessor.

Converts Office documents (.docx, .pptx, .odt) to PDF via the system
``soffice`` binary so a downstream PDF parser (Docling, OpenDataLoader)
can handle them through the same chain as native PDFs.

Reuses :func:`vitruvius.office.find_soffice_executable` for the
discovery logic — do not duplicate the path-probing here. If soffice
isn't installed, :func:`find_soffice_executable` raises and the
preprocessor surfaces the error in :class:`PreprocessResult.error`
without raising through normal use.

This is NOT a :class:`BaseParser` — it produces a new input for a
parser, not a Markdown output. The orchestrator runs preprocessors
before the parser chain.
"""
from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from vitruvius.office import find_soffice_executable


_OFFICE_EXTENSIONS = frozenset({".docx", ".pptx", ".odt", ".ods", ".odp"})


@dataclass(frozen=True)
class PreprocessResult:
    """Output of a :class:`LibreOfficePreprocessor`.

    ``pdf_path`` is ``None`` on any failure (soffice missing, non-Office
    extension, soffice exit != 0, expected output not found). ``error``
    carries the failure reason in that case.
    """
    pdf_path: Optional[Path]
    duration_ms: int
    error: Optional[str]


class LibreOfficePreprocessor:
    """Office → PDF preprocessor that runs before the parser chain."""

    preprocessor_id = "libreoffice_preprocessor"

    def preprocess(self, *, source_path: Path, workdir: Path) -> PreprocessResult:
        start = time.perf_counter()
        source_path = Path(source_path)

        if source_path.suffix.lower() not in _OFFICE_EXTENSIONS:
            return PreprocessResult(
                pdf_path=None,
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=(
                    f"not an office document: {source_path} "
                    f"(suffix={source_path.suffix!r})"
                ),
            )

        try:
            soffice = find_soffice_executable()
        except FileNotFoundError as exc:
            return PreprocessResult(
                pdf_path=None,
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"soffice not found: {exc}",
            )

        workdir = Path(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        expected_pdf = workdir / (source_path.stem + ".pdf")

        try:
            completed = subprocess.run(
                [
                    soffice,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(workdir),
                    str(source_path),
                ],
                capture_output=True,
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            return PreprocessResult(
                pdf_path=None,
                duration_ms=int((time.perf_counter() - start) * 1000),
                error="soffice conversion timed out after 120s",
            )

        duration_ms = int((time.perf_counter() - start) * 1000)

        if completed.returncode != 0:
            stderr_text = (completed.stderr or b"").decode("utf-8", errors="replace")
            return PreprocessResult(
                pdf_path=None,
                duration_ms=duration_ms,
                error=(
                    f"soffice returned {completed.returncode}: "
                    f"conversion failed. stderr={stderr_text[:500]}"
                ),
            )

        if not expected_pdf.exists():
            return PreprocessResult(
                pdf_path=None,
                duration_ms=duration_ms,
                error=(
                    f"soffice returned 0 but the expected output "
                    f"{expected_pdf} does not exist"
                ),
            )

        return PreprocessResult(
            pdf_path=expected_pdf,
            duration_ms=duration_ms,
            error=None,
        )
```

### Step 4: Add to `parsers/__init__.py` re-exports

Same pattern as Task 1 Step 4.

### Step 5: Run the tests (must PASS)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_libreoffice_preprocessor.py -v 2>&1 | tail -15
```

Expected: 4 passed.

### Step 6: Full suite

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -5
```

Expected: 1405 passed, 1 skipped (1401 after Task 1 + 4 new).

### Step 7: Commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/parsers/libreoffice_preprocessor.py \
  scripts/vitruvius/parsers/__init__.py \
  scripts/tests/test_libreoffice_preprocessor.py
git commit -m "$(cat <<'EOF'
feat(parsers): Sprint 1B-M1 Task 2 — LibreOfficePreprocessor

Office → PDF preprocessor that runs before the Phase 1B parser
chain. Reuses the existing vitruvius.office.find_soffice_executable
discovery logic (no duplicate path probing) and invokes
soffice --headless --convert-to pdf with a 120s timeout.

PreprocessResult dataclass carries the output path on success or
an error string on failure (soffice missing, non-office extension,
soffice exit != 0, timeout, expected output not found). The
preprocessor never raises through normal use — all failures route
through the error field.

4 tests cover: soffice-missing, non-office-extension rejection,
happy-path with mocked subprocess, soffice-returncode-failure.

Orchestrator wiring lands in Task 4.

Part of the Phase 1B Modernization Tranche 1 plan at
.ai/03_plans/2026-04-15-phase-1b-modernization-tdd-plan.md.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: `GATE-005` post-LibreOffice quality gate

**Goal:** Add a new quality gate that verifies a LibreOffice-produced PDF has ≥1 page and non-empty text content. Matches §8 of the design spec.

### Files

- **Modify:** `/Users/philiplewis/vitruvius/scripts/vitruvius/parsers/quality_gates.py` (append a new check function)
- **Modify:** `/Users/philiplewis/vitruvius/scripts/tests/test_quality_gates.py` (IF it exists; otherwise create)

### Step 1: Check whether test_quality_gates.py exists

```bash
cd /Users/philiplewis/vitruvius && ls scripts/tests/test_quality_gates*.py 2>&1
```

If it exists, read it and append 2 new tests. If not, create a new test file.

### Step 2: Write the failing tests

In `scripts/tests/test_quality_gates.py` (create or append), add:

```python
def test_gate_005_accepts_non_empty_pdf(tmp_path):
    from vitruvius.parsers.quality_gates import check_gate_005_libreoffice_pdf, GateStatus

    pdf = tmp_path / "out.pdf"
    pdf.write_bytes(b"%PDF-1.4\nstream\nBT /F1 12 Tf (hello world) Tj ET\nendstream\n")
    # This is not a valid full PDF but the gate only checks file existence
    # + non-empty bytes + minimum size. A real PDF validator would go further;
    # the gate is a sanity check, not a parser.

    result = check_gate_005_libreoffice_pdf(pdf_path=pdf)
    assert result.status == GateStatus.PASSED


def test_gate_005_rejects_missing_pdf(tmp_path):
    from vitruvius.parsers.quality_gates import check_gate_005_libreoffice_pdf, GateStatus

    missing = tmp_path / "missing.pdf"
    result = check_gate_005_libreoffice_pdf(pdf_path=missing)
    assert result.status == GateStatus.FAILED
    assert "does not exist" in (result.reason or "").lower()


def test_gate_005_rejects_empty_pdf(tmp_path):
    from vitruvius.parsers.quality_gates import check_gate_005_libreoffice_pdf, GateStatus

    empty = tmp_path / "empty.pdf"
    empty.write_bytes(b"")
    result = check_gate_005_libreoffice_pdf(pdf_path=empty)
    assert result.status == GateStatus.FAILED
    assert "empty" in (result.reason or "").lower()
```

### Step 3: Run the tests (must FAIL)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_quality_gates.py -v 2>&1 | tail -15
```

Expected: FAIL with `ImportError: cannot import name 'check_gate_005_libreoffice_pdf' ...`.

### Step 4: Implement the gate

Append to `scripts/vitruvius/parsers/quality_gates.py`:

```python
def check_gate_005_libreoffice_pdf(*, pdf_path: Path) -> GateResult:
    """GATE-005 — post-LibreOffice PDF sanity check.

    Verifies the PDF produced by :class:`LibreOfficePreprocessor`:
    - exists on disk
    - has non-zero bytes
    - is at least 256 bytes (empirically: any valid soffice PDF output
      is larger than this; shorter outputs indicate a silent failure)

    Returns a :class:`GateResult` with status PASSED / FAILED.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        return GateResult(
            gate_id="GATE-005",
            status=GateStatus.FAILED,
            reason=f"PDF does not exist: {pdf_path}",
        )
    size_bytes = pdf_path.stat().st_size
    if size_bytes == 0:
        return GateResult(
            gate_id="GATE-005",
            status=GateStatus.FAILED,
            reason=f"PDF is empty (0 bytes): {pdf_path}",
        )
    if size_bytes < 256:
        return GateResult(
            gate_id="GATE-005",
            status=GateStatus.FAILED,
            reason=(
                f"PDF is suspiciously small ({size_bytes} bytes, minimum 256): "
                f"likely a silent soffice failure"
            ),
        )
    return GateResult(
        gate_id="GATE-005",
        status=GateStatus.PASSED,
        reason=None,
    )
```

**Verify that `GateResult`, `GateStatus`, and `Path` are already imported at the top of `quality_gates.py`**. If `from pathlib import Path` is missing, add it.

### Step 5: Run the tests (must PASS)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_quality_gates.py -v -k gate_005 2>&1 | tail -10
```

Expected: 3 passed.

### Step 6: Full suite

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -5
```

Expected: 1408 passed, 1 skipped (1405 + 3 new).

### Step 7: Commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/parsers/quality_gates.py \
  scripts/tests/test_quality_gates.py
git commit -m "$(cat <<'EOF'
feat(parsers): Sprint 1B-M1 Task 3 — GATE-005 post-LibreOffice PDF check

Adds check_gate_005_libreoffice_pdf to the quality-gate module.
Verifies that a PDF produced by LibreOfficePreprocessor exists,
is non-empty, and is at least 256 bytes. The minimum-size check
catches silent soffice failures where soffice exits 0 but
produces a truncated output.

3 tests cover: non-empty PDF accepted, missing PDF rejected,
empty PDF rejected.

Part of the Phase 1B Modernization Tranche 1 plan at
.ai/03_plans/2026-04-15-phase-1b-modernization-tdd-plan.md.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Orchestrator wiring + feature flags

**Goal:** Teach `ParserOrchestrator` about preprocessors and chain dispatch. Add two feature flags and the test-registry entries. Add 3 chain-routing tests.

### Files

- **Modify:** `/Users/philiplewis/vitruvius/scripts/vitruvius/parsers/orchestrator.py` — accept `preprocessors: Sequence[Preprocessor] = ()` in the constructor; add chain dispatch for `hybrid_pdf` and `office_doc` classes behind feature flags
- **Modify:** `/Users/philiplewis/vitruvius/config/vitruvius.yaml` — add `p1b_docling_parser: false` + `p1b_libreoffice_preprocessor: false`
- **Modify:** `/Users/philiplewis/vitruvius/scripts/tests/test_features.py` — add both flags to `EXPECTED_FLAGS` + 2 default-false tests (mirror the AD-029 HP.3-R rocksdb flag pattern)
- **Create:** `/Users/philiplewis/vitruvius/scripts/tests/test_orchestrator_chains.py` — 3 chain-routing tests

### Step 1: Read the current orchestrator.py

```bash
cd /Users/philiplewis/vitruvius && cat scripts/vitruvius/parsers/orchestrator.py
```

Identify:
- The `ParserOrchestrator.__init__` signature (what it currently accepts)
- The existing `run(source_path, ...)` method (if any)
- How the current foundation-level orchestrator selects parsers

### Step 2: Add the two feature flags to config/vitruvius.yaml

Find the `p1b_*` region or the nearest flag family block and insert (at a sensible alphabetical position):

```yaml
  # Sprint 1B-M1 — Phase 1B Modernization Tranche 1 (Docling + LibreOffice)
  p1b_docling_parser: false         # Route hybrid_pdf / text_pdf_complex through DoclingParser
  p1b_libreoffice_preprocessor: false  # Route office_doc through LibreOfficePreprocessor before parser chain
```

### Step 3: Add to EXPECTED_FLAGS + default-false tests

In `scripts/tests/test_features.py`, add two entries to `EXPECTED_FLAGS` near the Sprint HP.3-R block:

```python
    # Sprint 1B-M1 — Phase 1B Modernization Tranche 1
    "p1b_docling_parser", "p1b_libreoffice_preprocessor",
```

And append two default-false tests at the end of the file (same pattern as `test_hp_rocksdb_event_store_defaults_true`):

```python
def test_p1b_docling_parser_defaults_false() -> None:
    """Sprint 1B-M1 — DoclingParser routing defaults false so the
    pre-tranche ingestion path is byte-identical."""
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("p1b_docling_parser") is False


def test_p1b_libreoffice_preprocessor_defaults_false() -> None:
    """Sprint 1B-M1 — LibreOfficePreprocessor routing defaults false."""
    from vitruvius.config import load_config

    cfg = load_config()
    flags = cfg.get("features", {}) if isinstance(cfg, dict) else {}
    assert flags.get("p1b_libreoffice_preprocessor") is False
```

### Step 4: Write the failing chain-routing tests

Create `scripts/tests/test_orchestrator_chains.py`:

```python
"""Sprint 1B-M1 Task 4 — Orchestrator chain-routing tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


def test_orchestrator_hybrid_pdf_routes_through_docling_when_flag_on(tmp_path: Path, monkeypatch) -> None:
    from vitruvius.parsers.orchestrator import ParserOrchestrator
    import vitruvius.config as cfgmod

    monkeypatch.setattr(
        cfgmod,
        "_features_block",
        lambda: {"p1b_docling_parser": True, "p1b_libreoffice_preprocessor": False},
    )

    pdf = tmp_path / "hybrid.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")

    docling_stub = MagicMock()
    docling_stub.parser_id = "docling"
    docling_stub.parse.return_value = MagicMock(
        markdown="# Hybrid content", sidecar_json={}, telemetry=MagicMock(valid=True),
    )

    orch = ParserOrchestrator(parsers=[docling_stub])
    result = orch.run_chain(source_path=pdf, document_class="hybrid_pdf")

    docling_stub.parse.assert_called_once()
    assert result is not None


def test_orchestrator_office_doc_runs_libreoffice_preprocessor_when_flag_on(tmp_path: Path, monkeypatch) -> None:
    from vitruvius.parsers.orchestrator import ParserOrchestrator
    from vitruvius.parsers.libreoffice_preprocessor import PreprocessResult
    import vitruvius.config as cfgmod

    monkeypatch.setattr(
        cfgmod,
        "_features_block",
        lambda: {"p1b_docling_parser": True, "p1b_libreoffice_preprocessor": True},
    )

    docx = tmp_path / "doc.docx"
    docx.write_text("stub")

    converted_pdf = tmp_path / "doc.pdf"
    converted_pdf.write_bytes(b"%PDF-1.4\n" + b"x" * 512)

    pre_stub = MagicMock()
    pre_stub.preprocessor_id = "libreoffice_preprocessor"
    pre_stub.preprocess.return_value = PreprocessResult(
        pdf_path=converted_pdf,
        duration_ms=10,
        error=None,
    )

    parser_stub = MagicMock()
    parser_stub.parser_id = "docling"
    parser_stub.parse.return_value = MagicMock(
        markdown="# From office", sidecar_json={}, telemetry=MagicMock(valid=True),
    )

    orch = ParserOrchestrator(parsers=[parser_stub], preprocessors=[pre_stub])
    result = orch.run_chain(source_path=docx, document_class="office_doc")

    pre_stub.preprocess.assert_called_once()
    parser_stub.parse.assert_called_once()
    # The parser must have been invoked on the preprocessor's output, not the original .docx
    call_args = parser_stub.parse.call_args
    assert call_args.kwargs.get("source_path") == converted_pdf


def test_orchestrator_flag_off_preserves_pre_tranche_path(tmp_path: Path, monkeypatch) -> None:
    """With both flags off, hybrid_pdf and office_doc chains should
    return a sentinel NoOp result indicating they are not wired. This
    is the backcompat guarantee — pre-tranche behaviour is byte-identical."""
    from vitruvius.parsers.orchestrator import ParserOrchestrator
    import vitruvius.config as cfgmod

    monkeypatch.setattr(
        cfgmod,
        "_features_block",
        lambda: {"p1b_docling_parser": False, "p1b_libreoffice_preprocessor": False},
    )

    orch = ParserOrchestrator(parsers=[])
    pdf = tmp_path / "x.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")

    result = orch.run_chain(source_path=pdf, document_class="hybrid_pdf")
    # The tranche-1 new chains are NOT active when the flag is off, so
    # run_chain returns None for those classes without error.
    assert result is None
```

### Step 5: Run the tests (must FAIL)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_orchestrator_chains.py -v 2>&1 | tail -20
```

Expected: FAIL — either `run_chain` method doesn't exist, or `preprocessors` kwarg not accepted.

### Step 6: Update `ParserOrchestrator`

Edit `scripts/vitruvius/parsers/orchestrator.py`. The minimum changes:

1. Add `from typing import Sequence` if missing
2. Add `preprocessors: Sequence[object] = ()` parameter to `__init__` (type it loosely since `Preprocessor` is duck-typed by having `preprocess`)
3. Add a new `run_chain(source_path, document_class) -> Optional[ParseResult]` method:

```python
    def run_chain(
        self,
        *,
        source_path: Path,
        document_class: str,
    ) -> Optional[ParseResult]:
        """Sprint 1B-M1 — dispatch on the Phase 1B taxonomy class.

        Reads feature flags from :mod:`vitruvius.config` and returns
        ``None`` when neither ``p1b_docling_parser`` nor
        ``p1b_libreoffice_preprocessor`` is set (backcompat: the
        pre-tranche pipeline is byte-identical when both flags are
        off).
        """
        try:
            from vitruvius import config as cfgmod
            flags = cfgmod._features_block()
        except Exception:
            flags = {}

        docling_on = bool(flags.get("p1b_docling_parser", False))
        libreoffice_on = bool(flags.get("p1b_libreoffice_preprocessor", False))

        if not docling_on and not libreoffice_on:
            return None

        current_input: Path = Path(source_path)

        # Office documents: run the LibreOffice preprocessor first.
        if document_class == "office_doc":
            if not libreoffice_on:
                return None
            pre = next(
                (p for p in self._preprocessors if getattr(p, "preprocessor_id", None) == "libreoffice_preprocessor"),
                None,
            )
            if pre is None:
                return None
            pre_result = pre.preprocess(source_path=current_input, workdir=current_input.parent)
            if pre_result.pdf_path is None:
                return None
            current_input = pre_result.pdf_path

        # Now dispatch to the docling parser if it's on.
        if document_class in {"hybrid_pdf", "office_doc"}:
            if not docling_on:
                return None
            parser = next(
                (p for p in self._parsers if getattr(p, "parser_id", None) == "docling"),
                None,
            )
            if parser is None:
                return None
            return parser.parse(source_path=current_input)

        return None
```

**Critical:** the constructor must store `_parsers` and `_preprocessors` as instance attributes if it doesn't already. If the existing constructor uses different attribute names (e.g. `self.parsers`), adapt the method to match.

### Step 7: Run all affected tests

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest \
  scripts/tests/test_orchestrator_chains.py \
  scripts/tests/test_features.py \
  -v 2>&1 | tail -25
```

Expected: all tests pass including the 3 new chain-routing tests + 2 new default-false tests.

### Step 8: Full suite

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -10
```

Expected: 1413 passed, 1 skipped (1408 + 5 new).

### Step 9: Commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/parsers/orchestrator.py \
  config/vitruvius.yaml \
  scripts/tests/test_features.py \
  scripts/tests/test_orchestrator_chains.py
git commit -m "$(cat <<'EOF'
feat(parsers): Sprint 1B-M1 Task 4 — orchestrator chain routing + flags

Wires DoclingParser and LibreOfficePreprocessor into the
ParserOrchestrator behind two new feature flags:
- p1b_docling_parser (default false)
- p1b_libreoffice_preprocessor (default false)

ParserOrchestrator gains a run_chain(source_path, document_class)
method that dispatches on the Phase 1B taxonomy class:
- hybrid_pdf → DoclingParser (when p1b_docling_parser is on)
- office_doc → LibreOfficePreprocessor → DoclingParser
  (when both flags are on)

When both flags are off, run_chain returns None and the
pre-tranche ingestion path is byte-identical.

3 new chain-routing tests + 2 new default-false tests.

Part of the Phase 1B Modernization Tranche 1 plan at
.ai/03_plans/2026-04-15-phase-1b-modernization-tdd-plan.md.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Docs + AD-031 + plan archival (orchestrator-held commit)

**Goal:** Close the tranche with an AD-031 entry recording what shipped, what's deferred to Tranche 2, and the commit SHAs. Archive this plan file.

### Files

- Modify: `.ai/10_state/decisions.md` — append AD-031
- Modify: `.ai/00_system/pipeline-overview.md` — add `p1b_*` flag family row to the flag table in the "Post-Sprint-D Pipeline Additions" section
- Modify: `.ai/03_plans/INDEX.md` — add a META row for this plan
- Move: `.ai/03_plans/2026-04-15-phase-1b-modernization-tdd-plan.md` → `.ai/09_archive/plans/`

### Step 1: Write AD-031

Append to `.ai/10_state/decisions.md`:

```markdown

## AD-031 — Phase 1B Modernization Tranche 1 (Docling + LibreOffice) (2026-04-15)

**Context.** The Phase 1B design spec (`.ai/03_plans/phase-1b-multi-parser-integration-plan.md`) §11 Phase 2 Modernization specifies four deliverables: DoclingParser, MarkerParser, Surya / OCRPreprocessor, and post-LibreOffice quality gates. At plan-dispatch time we verified: docling 2.88 was already installed (Sprint WIKI), marker-pdf and surya-ocr are NOT installed, and both pull in torch + transformer models (~2-5 GB each) that would stress the 8 GB M2 default profile.

We scoped Tranche 1 to the dep-compatible subset: DoclingParser + LibreOfficePreprocessor + GATE-005. Marker, Surya, ProcessPoolExecutor, and the Golden Corpus benchmark are deferred to Tranche 2 in a future session that dedicates time to 8 GB M2 ML-dep feasibility testing.

**Decision.** Shipped Tranche 1:

- `scripts/vitruvius/parsers/docling_parser.py` — `DoclingParser(BaseParser)` adapter around the Sprint WIKI docling facade. Reshapes `DoclingParseResult` into the Phase 1B §6 telemetry contract. 5 tests mock `convert_pdf_to_markdown` so the test suite never loads Docling.
- `scripts/vitruvius/parsers/libreoffice_preprocessor.py` — `LibreOfficePreprocessor` class + `PreprocessResult` dataclass. Reuses `vitruvius.office.find_soffice_executable` for discovery and invokes `soffice --headless --convert-to pdf` with a 120s timeout. 4 tests cover missing-soffice, non-office-extension, happy-path mock, and returncode-failure.
- `scripts/vitruvius/parsers/quality_gates.py::check_gate_005_libreoffice_pdf` — post-conversion PDF sanity check (exists, non-empty, ≥256 bytes). 3 tests.
- `scripts/vitruvius/parsers/orchestrator.py::ParserOrchestrator.run_chain` — new method that dispatches on the Phase 1B taxonomy class. Reads `p1b_docling_parser` and `p1b_libreoffice_preprocessor` flags (both default false per the non-breaking contract in the root `statistical-architectural-upgrade-plan.md` §1.3). When both flags are off, returns `None` and the pre-tranche ingestion path is byte-identical. 3 chain-routing tests.
- `config/vitruvius.yaml` + `scripts/tests/test_features.py` — new flags registered in both places with 2 default-false unit tests (mirrors the AD-029 HP.3-R pattern).

**Deferred to Tranche 2 (explicit):**

- **MarkerParser** (`marker-pdf 1.10.2` + torch + model weights)
- **SuryaParser / OCRPreprocessor** (`surya-ocr 0.17.1` + torch + surya weights)
- **ProcessPoolExecutor with dynamic resource allocation** (only meaningful with 3+ parsers)
- **Golden Corpus benchmark** (depends on the full parser set)
- **Page-level isolation / chunked fallback** (design spec §7.2; no real failures observed yet)
- **Ranger Audit Review Payload** (§12.1; depends on Phase 7 Supabase integration that doesn't exist)
- **New pipeline_cli.py subcommand** (`run-parsers` or similar) — Tranche 1's wiring is internal-only; end-user CLI wiring lands when Tranche 2 or a follow-up formalises it.

**Test delta.** Baseline 1396 → **1413 passing** (+17: Task 1 +5, Task 2 +4, Task 3 +3, Task 4 +5). 1 skipped. TypeScript 20/20. Rust 10/10.

**Commits.**
- Task 1 — `[FILL]` — `DoclingParser(BaseParser)` + 5 tests
- Task 2 — `[FILL]` — `LibreOfficePreprocessor` + 4 tests
- Task 3 — `[FILL]` — `GATE-005` + 3 tests
- Task 4 — `[FILL]` — Orchestrator wiring + flags + 5 tests
- Task 5 — `[this commit]` — docs + AD-031 + archival

**Follow-ups.**
- When 8 GB M2 feasibility is verified for marker-pdf + surya-ocr, write and execute the Tranche 2 TDD plan covering MarkerParser, SuryaParser, ProcessPoolExecutor, Golden Corpus.
- Default-flip gate: Tranche 1 flags stay `false` until the Golden Corpus benchmark (Tranche 2) measures that Docling+LibreOffice routing produces a measurable quality improvement on real PD 1096 corpus documents. Without real bench data, we can't justify flipping the defaults.
- `pipeline_cli.py` integration for the new parser chain is not in Tranche 1 — the orchestrator is available as a library call but no CLI surface exists yet.
```

Every `[FILL]` must be replaced with the real commit SHA from Tasks 1-4 before the commit lands.

### Step 2: Update pipeline-overview.md flag family table

Find the Feature-flag governance section (added by the 2026-04-15 docs cleanup pass) and add a new row to the flag-families table:

```markdown
| 1B-M1 — Phase 1B Modernization Tranche 1 | `p1b_*` | `p1b_docling_parser`, `p1b_libreoffice_preprocessor` |
```

### Step 3: Update INDEX.md

Add after the Sprint AUDIT-1 row (or the most recent active plan row):

```
| 1B | `phase-1b-modernization-tranche-1` | **Phase 1B Modernization Tranche 1** — DoclingParser + LibreOfficePreprocessor + GATE-005 + orchestrator wiring (Marker/Surya/ProcessPool/Golden Corpus deferred to Tranche 2) | ✅ Complete (archived 2026-04-15) | Sprint 1B-M1 — closed | implementation_tdd | [../09_archive/plans/2026-04-15-phase-1b-modernization-tdd-plan.md](../09_archive/plans/2026-04-15-phase-1b-modernization-tdd-plan.md) |
```

### Step 4: Archive this plan

```bash
cd /Users/philiplewis/vitruvius && git mv \
  .ai/03_plans/2026-04-15-phase-1b-modernization-tdd-plan.md \
  .ai/09_archive/plans/
```

### Step 5: Stage + commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  .ai/10_state/decisions.md \
  .ai/00_system/pipeline-overview.md \
  .ai/03_plans/INDEX.md \
  .ai/09_archive/plans/2026-04-15-phase-1b-modernization-tdd-plan.md
git commit -m "$(cat <<'EOF'
docs(1b): Sprint 1B-M1 closure — AD-031 + tranche-1 archival

Tranche 1 of Phase 1B Modernization closed. Shipped:
- DoclingParser(BaseParser) wrapper around Sprint WIKI facade
- LibreOfficePreprocessor using existing office.py soffice discovery
- GATE-005 post-LibreOffice PDF sanity check
- Orchestrator run_chain dispatch for hybrid_pdf + office_doc
- Two feature flags (default false; pre-tranche path byte-identical)

Deferred to Tranche 2 (pending 8 GB M2 ML-dep feasibility):
- MarkerParser (marker-pdf + torch)
- SuryaParser / OCRPreprocessor (surya-ocr + torch)
- ProcessPoolExecutor dynamic resource allocation
- Golden Corpus benchmark
- pipeline_cli.py integration

AD-031 records the full scope split + commit SHAs. Plan
archived to .ai/09_archive/plans/. Test suite delta:
1396 → 1413 passing (+17 tests across 4 tasks).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

### Step 6 (optional): Tag

```bash
cd /Users/philiplewis/vitruvius && git tag sprint-1b-m1-closed HEAD -m "Sprint 1B-M1 — Phase 1B Modernization Tranche 1 closed; see AD-031"
```

---

## Self-Review

**1. Spec coverage** — Parent design spec §11 Phase 2 lists 4 items. Tranche 1 ships 2 (DoclingParser, post-LibreOffice quality gates) and defers 2 (MarkerParser, Surya / OCRPreprocessor) with explicit rationale. All deferred items are called out in AD-031.

**2. Placeholder scan** — The only `[FILL]` placeholders are in AD-031's commit-SHA list, explicitly flagged as "must be replaced with real SHA before commit." No bare TBDs.

**3. Type consistency** — `DoclingParser` signatures match `BaseParser` (`parser_id`, `parser_version`, `parse(*, source_path, attempt_index)` returning `ParseResult`). `PreprocessResult` is a new frozen dataclass. `run_chain` returns `Optional[ParseResult]`. The orchestrator's `preprocessors` parameter is typed loosely as `Sequence[object]` and duck-typed by checking `preprocessor_id` + `preprocess` — this matches the existing patterns in the codebase.

**4. 8 GB M2 constraint** — every deferred item has a dep-size rationale. Shipped items use only already-installed deps (`docling`) or system binaries (`soffice`).

**5. Non-breaking contract** — both flags default `false`, matching the `statistical-architectural-upgrade-plan.md` §1.3 non-breaking contract. `test_repo_config_every_flag_is_false` will continue to pass because new flags default false. (Contrast: AD-029 RocksDB flags had to be added as an `ad_029_exceptions` allowlist because they default `true`.)

---

## Execution Handoff

Plan saved to `.ai/03_plans/2026-04-15-phase-1b-modernization-tdd-plan.md`. Two execution options:

**1. Subagent-Driven (recommended)** — Fresh subagent per task (Task 1 → 2 → 3 → 4 → 5), two-stage review (spec compliance + code quality) after each.

**2. Inline Execution** — Execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints.

Which approach?
