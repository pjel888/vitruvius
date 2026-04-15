---
plan_id: phase-1b-modernization-tranche-3
phase: 1B
title: "Phase 1B Modernization — Tranche 3 (RustPdfParser + quality gate)"
status: active
priority: high
sprint: "Sprint 1B-M3"
version: 1.0.0
plan_type: implementation_tdd
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
prerequisites:
  - Sprint RUST-PDF-1 closed (tag `sprint-rust-pdf-1-closed`) — AD-033 GO verdict, vitruvius_rust_pdf crate + pyo3 bindings installed
  - Sprint 1B-M2 closed (tag `sprint-1b-m2-closed`) — Tranche 2 library surface in place
related_plans:
  - ../09_archive/plans/2026-04-15-rust-pdf-audit-plan.md (the audit that said GO)
  - ../09_archive/plans/2026-04-15-phase-1b-modernization-tranche-2-plan.md (Tranche 2)
---

# Phase 1B Modernization — Tranche 3 (RustPdfParser + quality gate)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `RustPdfParser(BaseParser)` as the primary entry in the `text_pdf_simple` and `hybrid_pdf` parser chains, backed by the `vitruvius_rust_pdf` (lopdf) crate that AD-033 cleared with a 48×/625× RAM/wall win over docling. Ship a real-text quality gate that compares lopdf output against a known-good reference on a representative sample to catch quality regressions. Keep docling as the fallback.

**Architecture:** Thin adapter — `RustPdfParser` reshapes the Rust binding's output (page-delimited text with `\x0c` form-feeds) into the Phase 1B `ParseResult` + `ParserTelemetry` contract. Adds `GATE-006` that asserts a minimum char-count per page to catch lopdf failures on encrypted/malformed PDFs. The orchestrator pre-registration (`parser_chains` dict) gets new entries for `text_pdf_simple` → `[rust_pdf, opendataloader, docling]` and `hybrid_pdf` → `[rust_pdf, docling]`, putting the Rust parser first. Feature flag `p1b_rust_pdf_parser` defaults **false** until a real-PDF quality spot-check confirms parity with docling on a PD 1096 excerpt — that check is Task 1 before we ship anything else.

**Tech Stack:**
- `vitruvius_rust_pdf 0.1.0` — already installed via the Sprint RUST-PDF-1 audit
- Existing Phase 1B types: `BaseParser`, `ParseResult`, `ParserTelemetry`, `ParserOrchestrator`
- `pypdf 6.10.0` — already installed, used for the reference extraction in the quality spot-check

---

## Scope & Non-Goals

### In scope

1. **Text-quality spot check** — a one-off Task 1 that extracts text from a real PD 1096 section (or, if none is available in the repo, a known-good public-domain PDF) with both `vitruvius_rust_pdf.extract_pdf_text` and `pypdf.PdfReader.extract_text`, computes character-level similarity (normalized Levenshtein or LCS), and records the result in a JSON file. **Rollback gate:** if similarity < 0.70 on the sample, STOP and defer Tranche 3 with the evidence.
2. **`RustPdfParser(BaseParser)` class** — wraps `vitruvius_rust_pdf.extract_pdf_text`, maps the output to `ParseResult` + `ParserTelemetry` with heading count from naive `#`-line parsing, table count = 0 (lopdf doesn't detect tables).
3. **`GATE-006` — minimum char per page** — post-extraction gate that rejects outputs where the average chars-per-page is below a threshold (default 20 chars/page). Catches encrypted PDFs, empty-stream PDFs, and lopdf decode failures that still return a non-error empty string.
4. **Orchestrator pre-registration** — new entries in the default `ParserOrchestrator` factory for `text_pdf_simple` and `hybrid_pdf` chains with the Rust parser first. Only activated when `p1b_rust_pdf_parser` is true.
5. **Feature flag** — `p1b_rust_pdf_parser` default **false**. Will be flipped to `true` in a follow-up commit once the real-PD-1096 quality check on live corpus ingestion confirms no regression.
6. **Docs + AD-034** — decisions.md AD-034 records the quality spot-check result, the Tranche 3 deliverables, and the rollback condition that would revert the default flip.

### Out of scope

- **Flipping the `p1b_rust_pdf_parser` default to true.** That's a separate follow-up commit gated on real-corpus validation.
- **Layout-aware extraction** — lopdf's default `extract_text` loses multi-column ordering. Advanced layout preservation is a Tranche 4 topic, not Tranche 3.
- **OCR fallback integration** — the existing `OCRPreprocessor` (Tranche 2) already handles scanned PDFs. No change here.
- **`pipeline_cli.py` integration** — still deferred. Tranche 3 ships the orchestrator-level plumbing only.

---

## File Structure

### New files

| Path | Purpose |
|---|---|
| `scripts/vitruvius/parsers/rust_pdf_parser.py` | `RustPdfParser(BaseParser)` class |
| `scripts/vitruvius/bench/quality_check_rust_pdf.py` | Task 1 text-quality spot check harness + `QualityCheckResult` dataclass |
| `scripts/tests/test_rust_pdf_parser.py` | 5 tests (shape, missing file, empty bytes, round-trip, telemetry) |
| `scripts/tests/test_gate_006.py` | 3 tests for the char-per-page gate |
| `.ai/10_state/quality_check_rust_pdf_2026-04-15.json` | Task 1 output — char-similarity scores + verdict |

### Modified files

| Path | Reason |
|---|---|
| `scripts/vitruvius/parsers/quality_gates.py` | Add `check_gate_006_min_chars_per_page` |
| `scripts/vitruvius/parsers/orchestrator.py` | Add default-chain-factory helper that uses `p1b_rust_pdf_parser` flag |
| `scripts/vitruvius/parsers/__init__.py` | Re-export `RustPdfParser` |
| `config/vitruvius.yaml` | Add `p1b_rust_pdf_parser: false` |
| `scripts/tests/test_features.py` | Add flag to `EXPECTED_FLAGS` + default-false test |
| `.ai/10_state/decisions.md` | Append AD-034 |
| `.ai/03_plans/INDEX.md` | Add row for this plan |

### Explicitly NOT touched

- `scripts/vitruvius/engine_rs/pdf/` — stays frozen. The Rust crate is already tested via the Sprint RUST-PDF-1 smoke tests.
- `scripts/vitruvius/wiki/docling_parser.py` — stays as the Sprint WIKI facade. Tranche 3 makes DoclingParser the fallback, not a replacement.
- `scripts/pipeline_cli.py` — deferred.

---

## Dispatch Order

1. **Task 1** — Text-quality spot check on a sample PDF. Rollback gate. **If this task emits NO_GO, STOP and defer Tranche 3.**
2. **Task 2** — `RustPdfParser(BaseParser)` class + 5 tests
3. **Task 3** — `GATE-006` min-chars-per-page + 3 tests
4. **Task 4** — Feature flag + orchestrator pre-registration helper
5. **Task 5** — Docs + AD-034 + archival

---

## Task 1: Text-quality spot check (ROLLBACK GATE)

**Goal:** Before we ship any BaseParser wrapping lopdf, verify that lopdf's text extraction is within 30% character-similarity of a reference extraction on a real PDF. If similarity < 0.70, STOP the tranche — the synthetic bench numbers from AD-033 don't tell us anything about real text quality.

**Files:**
- Create: `scripts/vitruvius/bench/quality_check_rust_pdf.py`
- Create: `.ai/10_state/quality_check_rust_pdf_2026-04-15.json`

### Step 1: Find a reference PDF

The repo contains PD 1096 content in `002_Raw-Conversion-Layer/001-Laws/` — use any `.pdf` that's present. Run:

```bash
find /Users/philiplewis/vitruvius/001_Raw-Source-Layer /Users/philiplewis/vitruvius/002_Raw-Conversion-Layer -name '*.pdf' -type f 2>&1 | head -5
```

Pick the first PDF that returns. If no PDF exists in the repo (possible — the raw layer is git-ignored), fall back to a hand-crafted quality check using a `pypdf`-generated PDF with known text content.

### Step 2: Implement the quality check harness

Create `scripts/vitruvius/bench/quality_check_rust_pdf.py` with a `run_quality_check(pdf_path)` function that:

1. Reads the PDF bytes
2. Extracts text via `vitruvius_rust_pdf.extract_pdf_text(pdf_bytes)`
3. Extracts text via `pypdf.PdfReader(pdf_path).pages[i].extract_text() for i in ...`
4. Computes character-level similarity: `len(lcs(rust_text, pypdf_text)) / max(len(rust_text), len(pypdf_text))` where `lcs` is the longest common subsequence length. Implement LCS via a space-efficient DP (O(min(m, n)) memory).
5. Emits a `QualityCheckResult` frozen dataclass with: `pdf_path`, `rust_char_count`, `pypdf_char_count`, `lcs_length`, `similarity_ratio`, `recommendation: "GO" | "NO_GO"`, `notes`
6. Writes the result to `.ai/10_state/quality_check_rust_pdf_2026-04-15.json`
7. **Returns non-zero exit code if `similarity_ratio < 0.70`** so the bash caller can detect the rollback condition.

### Step 3: Run the spot check

```bash
cd /Users/philiplewis/vitruvius && PYTHONPATH=scripts /opt/homebrew/opt/python@3.11/bin/python3.11 -m vitruvius.bench.quality_check_rust_pdf
```

Read the JSON output. **If `recommendation == "NO_GO"`, STOP execution** — write an abbreviated AD-034 entry recording the failure, and close the tranche without shipping the BaseParser. Do NOT commit any of the in-progress Tranche 3 code.

If `recommendation == "GO"`, commit the harness + JSON and proceed to Task 2.

### Step 4: Commit Task 1

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/bench/quality_check_rust_pdf.py \
  .ai/10_state/quality_check_rust_pdf_2026-04-15.json
git commit -m "feat(bench): Sprint 1B-M3 Task 1 — Rust PDF text-quality spot check"
```

---

## Task 2: `RustPdfParser(BaseParser)` class + 5 tests

**Goal:** Adapt the Rust binding to the Phase 1B `BaseParser` contract. Emit telemetry. Handle edge cases (empty input, lopdf errors) without raising through normal use.

### Step 1: Write failing tests

Create `scripts/tests/test_rust_pdf_parser.py` with 5 tests:
1. `test_rust_pdf_parser_is_base_parser` — verify `parser_id == "rust_pdf"` and is-a `BaseParser`
2. `test_rust_pdf_parser_missing_file_returns_failure` — missing file returns valid=False
3. `test_rust_pdf_parser_empty_file_returns_failure` — 0-byte file returns valid=False
4. `test_rust_pdf_parser_happy_path` — pypdf-generated blank PDF returns non-error ParseResult with telemetry populated
5. `test_rust_pdf_parser_wraps_lopdf_error` — invalid bytes passed to the parser result in a non-raising failure with a descriptive error message

### Step 2: Run tests (fail)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_rust_pdf_parser.py -v
```

Expected: `ModuleNotFoundError: No module named 'vitruvius.parsers.rust_pdf_parser'`.

### Step 3: Implement `RustPdfParser`

Create `scripts/vitruvius/parsers/rust_pdf_parser.py`. Pattern:

```python
"""Sprint 1B-M3 Task 2 — RustPdfParser(BaseParser).

Thin adapter around vitruvius_rust_pdf.extract_pdf_text that reshapes
the lopdf output into the Phase 1B BaseParser contract. Emits telemetry
with header count derived from naive line-level parsing (Rust side
doesn't detect headings today) and tables count = 0 (lopdf can't
detect tables either).
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from vitruvius.parsers.base_parser import BaseParser, ParseResult, ParserTelemetry


class RustPdfParser(BaseParser):
    parser_id = "rust_pdf"
    parser_version = "vitruvius_rust_pdf-0.1.0"

    def parse(self, source_path: Path, work_dir: Path) -> ParseResult:
        start = time.perf_counter()
        source_path = Path(source_path)

        if not source_path.exists():
            return self._failure(
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"missing file: {source_path}",
            )

        try:
            pdf_bytes = source_path.read_bytes()
        except OSError as exc:
            return self._failure(
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"read error: {exc}",
            )

        if len(pdf_bytes) == 0:
            return self._failure(
                duration_ms=int((time.perf_counter() - start) * 1000),
                error="empty file (0 bytes)",
            )

        try:
            import vitruvius_rust_pdf
        except ImportError as exc:
            return self._failure(
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"vitruvius_rust_pdf not installed: {exc}",
            )

        try:
            text = vitruvius_rust_pdf.extract_pdf_text(pdf_bytes)
        except ValueError as exc:
            return self._failure(
                duration_ms=int((time.perf_counter() - start) * 1000),
                error=f"lopdf extraction failed: {exc}",
            )

        duration_ms = int((time.perf_counter() - start) * 1000)
        pages_total = text.count("\x0c") if text else 0
        md_pages = text.split("\x0c")
        markdown = "\n\n".join(p for p in md_pages if p.strip())
        headers = sum(1 for line in markdown.splitlines() if line.startswith("#"))

        telemetry = ParserTelemetry(
            parser_id=self.parser_id,
            attempt_index=0,
            duration_ms=duration_ms,
            pages_total=pages_total,
            pages_processed=pages_total,
            page_coverage_ratio=1.0 if pages_total > 0 else 0.0,
            text_length=len(text),
            md_length=len(markdown),
            headers=headers,
            tables=0,
            images=0,
            captions=0,
            ocr_applied=False,
            confidence=1.0 if markdown else 0.0,
            valid=bool(markdown),
            error=None if markdown else "empty extraction",
        )

        sidecar: dict[str, Any] = {
            "parser_id": self.parser_id,
            "parser_version": self.parser_version,
            "page_count": pages_total,
            "bytes_in": len(pdf_bytes),
        }
        return ParseResult(
            markdown_text=markdown,
            telemetry=telemetry,
            sidecar_metadata=sidecar,
        )

    def _failure(self, *, duration_ms: int, error: str) -> ParseResult:
        return ParseResult(
            markdown_text="",
            telemetry=ParserTelemetry(
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
            ),
            sidecar_metadata={},
        )
```

Re-export from `scripts/vitruvius/parsers/__init__.py`.

### Step 4: Run tests (pass)

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_rust_pdf_parser.py -v 2>&1 | tail -12
```

Expected: 5 passed.

### Step 5: Full suite + commit

Expected baseline after Task 1: 1428 + 0 (Task 1 adds the JSON output, not tests) = 1428. After Task 2: 1433.

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -5
git add scripts/vitruvius/parsers/rust_pdf_parser.py scripts/vitruvius/parsers/__init__.py scripts/tests/test_rust_pdf_parser.py
git commit -m "feat(parsers): Sprint 1B-M3 Task 2 — RustPdfParser(BaseParser) wraps lopdf"
```

---

## Task 3: `GATE-006` min-chars-per-page

**Goal:** Post-extraction gate that rejects outputs where the average chars-per-page is below a threshold (default 20). Catches encrypted PDFs and lopdf decode failures that return non-error empty strings.

### Step 1: Write failing tests in `scripts/tests/test_gate_006.py`

Three tests:
- `test_gate_006_accepts_sufficient_char_density` — parse result with 100 chars and 1 page passes
- `test_gate_006_rejects_insufficient_char_density` — parse result with 5 chars and 1 page fails
- `test_gate_006_handles_zero_pages` — parse result with 0 pages returns FAILED (not division-by-zero)

### Step 2: Add the gate to `scripts/vitruvius/parsers/quality_gates.py`

Append:

```python
def check_gate_006_min_chars_per_page(
    parse_result: ParseResult,
    *,
    min_chars_per_page: int = 20,
) -> GateResult:
    """GATE-006 — minimum characters per extracted page.

    Catches silent failures where a parser returns non-error but
    empty (or near-empty) text — typical for encrypted PDFs and
    lopdf decode failures on non-standard font dictionaries.
    """
    telemetry = parse_result.telemetry
    if telemetry.pages_total == 0:
        return GateResult(
            gate_id="GATE-006",
            gate_name="min_chars_per_page",
            status=GateStatus.FAILED,
            reason=f"zero pages extracted; parser_id={telemetry.parser_id!r}",
        )
    avg = telemetry.md_length / telemetry.pages_total
    if avg < min_chars_per_page:
        return GateResult(
            gate_id="GATE-006",
            gate_name="min_chars_per_page",
            status=GateStatus.FAILED,
            reason=(
                f"average chars per page {avg:.1f} below threshold "
                f"{min_chars_per_page} ({telemetry.md_length} chars / "
                f"{telemetry.pages_total} pages)"
            ),
        )
    return GateResult(
        gate_id="GATE-006",
        gate_name="min_chars_per_page",
        status=GateStatus.PASSED,
        reason=f"{avg:.1f} chars/page >= {min_chars_per_page}",
    )
```

**Note:** do NOT add `check_gate_006_min_chars_per_page` to `run_quality_gates`'s aggregator unless you want it to run on every ParseResult. For Tranche 3 we keep it opt-in — callers who want the extra check run it explicitly on `RustPdfParser` output.

### Step 3: Run tests + commit

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_gate_006.py -v
git add scripts/vitruvius/parsers/quality_gates.py scripts/tests/test_gate_006.py
git commit -m "feat(parsers): Sprint 1B-M3 Task 3 — GATE-006 min-chars-per-page quality gate"
```

Expected full suite: 1436 passed.

---

## Task 4: Feature flag + orchestrator pre-registration

**Goal:** Wire `p1b_rust_pdf_parser` into the feature flag registry. Default false until real-corpus validation in a follow-up commit.

### Step 1: Flag plumbing

Add to `config/vitruvius.yaml` under the existing p1b block:

```yaml
  p1b_rust_pdf_parser: false  # Sprint 1B-M3 — primary rust_pdf parser; off until real-corpus quality validation
```

Add to `scripts/tests/test_features.py::EXPECTED_FLAGS`:

```python
    "p1b_rust_pdf_parser",
```

Add a default-false test.

### Step 2: Full suite + commit

Expected: 1437 passed.

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -3
git add config/vitruvius.yaml scripts/tests/test_features.py
git commit -m "feat(flags): Sprint 1B-M3 Task 4 — p1b_rust_pdf_parser flag (default false)"
```

---

## Task 5: Docs + AD-034 + plan archival

**Goal:** Close the tranche with an AD-034 entry that records the Task 1 quality spot-check result + the ship decision + commit SHAs. Archive this plan.

### Step 1: Write AD-034

Append to `.ai/10_state/decisions.md` (before Decision Process footer). Fields to fill:

- Task 1 similarity_ratio from `.ai/10_state/quality_check_rust_pdf_2026-04-15.json`
- 4 commit SHAs (one per task)
- Real-corpus rollback gate language: "If the live PD 1096 ingestion (when pipeline_cli.py integration lands) shows similarity < 0.70 vs docling's output on any section, flip `p1b_rust_pdf_parser` back to false and open AD-035 documenting the regression."

### Step 2: Update pipeline-overview.md and INDEX.md, then commit

Same pattern as previous closure commits.

### Step 3: Tag

```bash
cd /Users/philiplewis/vitruvius && git tag sprint-1b-m3-closed HEAD -m "Sprint 1B-M3 — RustPdfParser + GATE-006 + p1b_rust_pdf_parser flag"
```

---

## Self-Review

**1. Spec coverage.** AD-033's follow-ups list (a) real-corpus quality spot check, (b) RustPdfParser BaseParser wrap, (c) rollback gate. All three are in scope here.

**2. Rollback safety.** Flag defaults false, so merging Tranche 3 is a no-op for the existing pipeline. The real-corpus validation happens in a separate follow-up commit.

**3. Dep risk.** Zero new pip installs. `vitruvius_rust_pdf` already installed via Sprint RUST-PDF-1 Task 1.

**4. Honest limits.** Lopdf loses layout info on multi-column PDFs. This is documented in the AD-034 follow-ups as a Tranche 4 candidate, not a Tranche 3 blocker.

---

## Execution Handoff

Plan saved. Executable via executing-plans or subagent-driven-development when the user approves.
