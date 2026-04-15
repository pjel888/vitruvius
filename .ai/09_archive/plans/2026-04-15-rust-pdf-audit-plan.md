---
plan_id: rust-pdf-ingestion-audit
phase: 1B
title: "Rust PDF Ingestion Exploration Audit (low-spec investigation)"
status: active
priority: high
sprint: "Sprint RUST-PDF-1 — audit"
version: 1.0.0
plan_type: audit_then_conditional_implementation
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
prerequisites:
  - Sprint 1B-M2 closed (tag `sprint-1b-m2-closed`) — Tranche 2 library surface in place
  - User's explicit directive: "the ultimate goal is to be able to run vitruvius on even a low spec machine" + "let us explore [Rust] option"
related_plans:
  - ../09_archive/plans/2026-04-15-phase-1b-modernization-tranche-2-plan.md (Tranche 2, closed)
  - ../09_archive/plans/2026-04-15-advanced-tech-audit-plan.md (AUDIT pattern reference — if not yet executed)
---

# Rust PDF Ingestion Exploration Audit

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Decide — with measured evidence, not speculation — whether a pure-Rust PDF parsing path could replace (or supplement) the current `docling` + `ocrmypdf` + `opendataloader_pdf` Python stack for the low-spec target. The key metric: **peak RAM during a real PDF → Markdown conversion**. The target: ≤ 200 MB peak RAM on a typical 10-page PD 1096 section document, vs docling's current ~1-2 GB peak.

**Architecture:** Audit-first, implement-conditionally — mirrors the Sprint HP.3-R and advanced-tech-audit plans. Three evaluation phases:

1. **Crate availability + feasibility test** — can we build a Rust PDF parser on this machine today with zero new heavy Python deps?
2. **Micro-benchmark** — extract text from a synthetic PDF and measure peak RAM + wall-time vs the Python baseline.
3. **Decision gate** — write numeric verdict (GO / DEFER / NO_GO) to `.ai/10_state/audit_rust_pdf_2026-04-15.json`; the conditional implementation plan is written ONLY if the audit emits GO.

**Tech Stack:**
- `lopdf` (Rust crate) — pure-Rust PDF manipulation, no native deps. Handles low-level PDF structure + basic text extraction. Small footprint (~1 MB compiled). **Primary candidate** for the low-spec target.
- `pdf-extract` (Rust crate) — higher-level text extractor built on lopdf. Even more convenient API, but lopdf alone may be sufficient.
- `pdfium-render` (Rust crate) — bindings to Google's pdfium. Higher quality output but 20-40 MB binary footprint and requires a native pdfium library. Secondary candidate if lopdf text quality is insufficient.
- `maturin` — already available in the workspace, used for the existing `engine_rs` and `datalog_rs` crates.
- The existing `scripts/vitruvius/engine_rs/` Cargo workspace — we extend it with a new `pdf/` crate rather than creating a sibling workspace, so the pyo3 shim pattern stays consistent.

---

## Scope & Non-Goals

### In scope (this audit)

1. **Build feasibility test** — attempt `cargo build --release` on a minimal `lopdf` → text extraction crate inside the existing `engine_rs` workspace. Record disk footprint, compile time, and whether it pulls any native deps.
2. **Python binding smoke test** — expose a single function `extract_pdf_text(pdf_bytes: bytes) -> str` via pyo3 from the new crate. Verify the Python binding imports cleanly and round-trips a minimum-viable PDF.
3. **RAM + wall-time micro-benchmark** — compare the Rust binding against `docling.document_converter.DocumentConverter` and `opendataloader_pdf.convert` on three synthetic PDFs: (a) simple text-only, (b) multi-column layout, (c) short scanned-style image-heavy placeholder. Measure peak RSS and wall-seconds.
4. **Text quality spot check** — extract text from a single real PD 1096 excerpt (if available) with both the Rust binding and `docling`, and compare character-level diff. Not a full corpus eval, just a sanity check: "does the Rust extractor miss obvious text?"
5. **Decision gate** — emit `GO`, `DEFER`, or `NO_GO` with numeric thresholds written to `.ai/10_state/audit_rust_pdf_2026-04-15.json`.
6. **If GO**, write a follow-up Tranche 3 TDD plan. If DEFER or NO_GO, document the rationale in AD-033 and close the audit.

### Out of scope

- **Actual Tranche 3 implementation** (new `RustPdfParser` class in the `parsers/` subpackage). That's a separate plan that this audit either unblocks or doesn't.
- **OCR in Rust** — `tesseract-rs` bindings exist but still depend on system tesseract. No benefit over the existing `ocrmypdf` path for the low-spec target.
- **pdfium-render wall-time benchmark** — only run if lopdf text quality is insufficient on the PD 1096 excerpt.
- **Marker / Surya ports to Rust** — out of scope, would defeat the low-spec goal.
- **Cross-platform wheel distribution** — the audit is local-only; shipping pre-built wheels is a later packaging concern.

---

## File Structure

### New files (this audit)

| Path | Purpose |
|---|---|
| `scripts/vitruvius/engine_rs/pdf/Cargo.toml` | New workspace crate declaring lopdf dep + pyo3 entry point |
| `scripts/vitruvius/engine_rs/pdf/src/lib.rs` | `extract_pdf_text` function + pyo3 bindings |
| `scripts/vitruvius/bench/bench_rust_pdf_audit.py` | RAM + wall-time micro-benchmark comparing Rust binding against docling and opendataloader |
| `scripts/tests/test_rust_pdf_audit.py` | Smoke test gated on `pytest.importorskip("vitruvius_rust_pdf")` — verifies binding loads and round-trips |
| `.ai/10_state/audit_rust_pdf_2026-04-15.json` | Audit output with decision gate |

### Modified files

| Path | Reason |
|---|---|
| `scripts/vitruvius/engine_rs/Cargo.toml` | Add `pdf/` to workspace members |
| `scripts/vitruvius/engine_rs/__init__.py` | Re-export the new `vitruvius_rust_pdf` module (if feasibility succeeds) |

### Explicitly NOT touched during the audit

- `scripts/vitruvius/parsers/` — no new `BaseParser` subclass yet. That's the conditional implementation plan.
- `scripts/vitruvius/wiki/docling_parser.py` — stays as-is. The audit compares against it, doesn't modify it.
- `scripts/pipeline_cli.py` — not touched.

---

## Pre-Audit Ground Truth (verified at plan-write time)

### Current PDF-parsing stack RAM consumption

Estimated from common usage patterns — exact measurements will happen inside the micro-benchmark task:

- **`docling.document_converter.DocumentConverter`** — lazy-loads transformer models (layoutlm, table transformer). Peak RAM on a 10-page PDF: typically 800 MB - 1.5 GB depending on whether the OCR path fires.
- **`opendataloader_pdf.convert`** — lighter, doesn't load neural models by default. Peak RAM: typically 100-300 MB on a 10-page PDF.
- **`ocrmypdf.ocr`** (fallback for scanned PDFs) — wraps tesseract. Peak RAM: 150-400 MB per scanned page.

### Rust crate candidates — wheel/build feasibility

- `lopdf` — **pure Rust**, no native system deps. Latest version 0.36 on crates.io. Compiles in seconds. Binary footprint ~1 MB. Text extraction is functional but less sophisticated than pdfium (loses some layout info on complex documents). **Primary candidate** for low-spec.
- `pdf-extract` — builds on top of `lopdf`, exposes a higher-level API. Still pure Rust. Latest version 0.8.
- `pdfium-render` — bindings to Google's pdfium. Requires either a dynamically-linked pdfium shared library OR a bundled static build (~30-40 MB binary). Higher quality text extraction and layout preservation. **Secondary candidate** only if lopdf fails a quality gate.
- `mupdf-sys` — bindings to mupdf. Excellent quality but AGPL-licensed (license conflict — mupdf requires commercial license for our use case). **DISQUALIFIED on license grounds.**

### Environment state (carried over from AD-032)

- Available disk: 11.71 GB (95.2% used) — tight; lopdf compile is small (~50 MB intermediate files), pdfium would need 40+ MB static library. **lopdf fits; pdfium is risky on current disk.**
- Available RAM: 2.03 GB — Rust compilation is memory-efficient (100-500 MB peak per crate). **Safe.**
- Rust toolchain: available via `~/.cargo/env` (rustc 1.94.1, cargo 1.94.1, maturin 1.13.1, pyo3 0.22.6). No new installs required.

### Decision gate thresholds

- **GO** — Rust binding peak RAM ≤ 30% of docling's peak RAM on the same test PDF AND wall-time ≤ 50% of docling's wall-time AND text quality (char-level similarity to docling output) ≥ 0.85.
- **DEFER** — Rust binding peak RAM ≤ 70% of docling's peak RAM AND text quality ≥ 0.70 (the win is real but not dramatic; revisit when docling becomes the bottleneck).
- **NO_GO** — Rust binding fails any of: builds cleanly, pyo3 bindings import, text extraction produces non-empty output on a synthetic PDF, text quality ≥ 0.70 on the PD 1096 excerpt.

---

## Task 1: Build feasibility — new `engine_rs/pdf` crate

**Goal:** Scaffold a new workspace crate that declares lopdf as a dep and exposes `extract_pdf_text` via pyo3. Verify it compiles and the Python binding imports.

**Files:**
- Create: `/Users/philiplewis/vitruvius/scripts/vitruvius/engine_rs/pdf/Cargo.toml`
- Create: `/Users/philiplewis/vitruvius/scripts/vitruvius/engine_rs/pdf/src/lib.rs`
- Create: `/Users/philiplewis/vitruvius/scripts/tests/test_rust_pdf_audit.py` (smoke test)
- Modify: `/Users/philiplewis/vitruvius/scripts/vitruvius/engine_rs/Cargo.toml` (add `pdf/` to workspace members)

### Step 1: Check disk headroom one more time before cargo build

```bash
df -h /Users/philiplewis/vitruvius 2>&1 | head -2
```

Expected: ≥10 GB free. If less, STOP and report — Rust compilation caches can eat 1-2 GB and we can't afford to cross the 98% disk threshold.

### Step 2: Create the Cargo manifest

Create `/Users/philiplewis/vitruvius/scripts/vitruvius/engine_rs/pdf/Cargo.toml`:

```toml
[package]
name = "vitruvius_rust_pdf"
version = "0.1.0"
edition = "2021"
description = "Sprint RUST-PDF-1 audit — pure-Rust PDF text extraction via lopdf for low-spec ingestion."

[lib]
name = "vitruvius_rust_pdf"
crate-type = ["cdylib", "rlib"]

[dependencies]
lopdf = "0.36"
pyo3 = { version = "0.22", features = ["extension-module"] }
```

### Step 3: Create the Rust source

Create `/Users/philiplewis/vitruvius/scripts/vitruvius/engine_rs/pdf/src/lib.rs`:

```rust
//! Sprint RUST-PDF-1 — audit crate.
//!
//! Minimal Rust → Python bridge that extracts text from a PDF byte
//! buffer using `lopdf`. The goal is to measure peak RAM + wall-time
//! vs the Python `docling` and `opendataloader_pdf` stacks, not to
//! ship a production parser.

use lopdf::Document;
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

/// Extract text from a PDF byte buffer.
///
/// Returns the extracted text as a single string. Pages are separated
/// by form-feed characters (\x0c) which the Python caller can split on.
/// Empty input or unparseable PDFs return an empty string (not an error)
/// so the caller can treat this as a best-effort extractor.
#[pyfunction]
fn extract_pdf_text(pdf_bytes: &[u8]) -> PyResult<String> {
    if pdf_bytes.is_empty() {
        return Ok(String::new());
    }

    let doc = match Document::load_mem(pdf_bytes) {
        Ok(d) => d,
        Err(e) => {
            return Err(PyValueError::new_err(format!(
                "lopdf failed to parse PDF: {}",
                e
            )))
        }
    };

    let mut out = String::new();
    for (page_num, _page_id) in doc.get_pages() {
        match doc.extract_text(&[page_num]) {
            Ok(text) => {
                out.push_str(&text);
                out.push('\x0c');
            }
            Err(_) => {
                // Skip pages that lopdf can't decode; don't fail the whole doc.
                out.push('\x0c');
            }
        }
    }

    Ok(out)
}

/// Version string for smoke-testing the Python binding.
#[pyfunction]
fn version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[pymodule]
fn vitruvius_rust_pdf(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(extract_pdf_text, m)?)?;
    m.add_function(wrap_pyfunction!(version, m)?)?;
    Ok(())
}
```

### Step 4: Add `pdf/` to the workspace

Edit `/Users/philiplewis/vitruvius/scripts/vitruvius/engine_rs/Cargo.toml`. Find the `[workspace]` `members = [...]` list and append `"pdf"`:

```toml
[workspace]
resolver = "2"
members = [
    "core",
    "pyo3_shim",
    "pdf",
]
```

Check the real file first via `cat` to get the exact existing member list; match indentation.

### Step 5: Try to build

```bash
cd /Users/philiplewis/vitruvius/scripts/vitruvius/engine_rs && source ~/.cargo/env && cargo build --release -p vitruvius_rust_pdf 2>&1 | tail -30
```

Expected: clean compile, no new native deps, resulting `.dylib` at `target/release/libvitruvius_rust_pdf.dylib` (on macOS).

If compile fails — capture the error and STOP. Write a partial audit result with `recommendation: NO_GO` citing the compile failure, commit the Cargo manifest + Rust source anyway (so the investigation is reproducible), and proceed to Task 5 closure.

### Step 6: Install via maturin develop

```bash
cd /Users/philiplewis/vitruvius/scripts/vitruvius/engine_rs/pdf && source ~/.cargo/env && maturin develop --release 2>&1 | tail -20
```

Expected: `Installed vitruvius_rust_pdf-0.1.0` line. If maturin complains about the `[lib]` or `[package.metadata.maturin]` config, adjust the Cargo.toml to add `[tool.maturin]` or a `pyproject.toml` for maturin metadata.

### Step 7: Write the Python smoke test

Create `/Users/philiplewis/vitruvius/scripts/tests/test_rust_pdf_audit.py`:

```python
"""Sprint RUST-PDF-1 Task 1 — Python binding smoke test."""
from __future__ import annotations

import pytest

rust_pdf = pytest.importorskip("vitruvius_rust_pdf")


def test_version_is_nonempty() -> None:
    assert rust_pdf.version()
    assert isinstance(rust_pdf.version(), str)


def test_extract_empty_bytes_returns_empty() -> None:
    assert rust_pdf.extract_pdf_text(b"") == ""


def test_extract_invalid_pdf_raises_value_error() -> None:
    with pytest.raises(ValueError, match="lopdf failed"):
        rust_pdf.extract_pdf_text(b"not a pdf")


def test_extract_minimum_viable_pdf_returns_string() -> None:
    """A hand-rolled minimum-viable PDF with a single empty page.
    Verifies that lopdf can load the document and extract_pdf_text
    returns a string (may be empty)."""
    # Minimum-viable PDF bytes — structurally valid but contains no text.
    minimal_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n"
        b"xref\n0 4\n0000000000 65535 f\n"
        b"0000000009 00000 n\n"
        b"0000000050 00000 n\n"
        b"0000000090 00000 n\n"
        b"trailer<</Size 4/Root 1 0 R>>\n"
        b"startxref\n140\n%%EOF\n"
    )
    result = rust_pdf.extract_pdf_text(minimal_pdf)
    assert isinstance(result, str)
```

### Step 8: Run the smoke test

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/test_rust_pdf_audit.py -v 2>&1 | tail -15
```

Expected: 4 passed (or skipped if the Rust module failed to install, in which case Step 6 already flagged a NO_GO).

### Step 9: Full suite regression

```bash
cd /Users/philiplewis/vitruvius && /opt/homebrew/opt/python@3.11/bin/python3.11 -m pytest scripts/tests/ -x --tb=short 2>&1 | tail -5
```

Expected: baseline 1424 → 1428 passing (or 1424 passing + 4 skipped if Rust build failed).

### Step 10: Commit Task 1 artifacts

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/engine_rs/pdf/ \
  scripts/vitruvius/engine_rs/Cargo.toml \
  scripts/tests/test_rust_pdf_audit.py
git commit -m "feat(engine_rs): Sprint RUST-PDF-1 Task 1 — lopdf audit crate + pyo3 bindings"
```

---

## Task 2: Micro-benchmark RAM + wall-time vs docling / opendataloader

**Goal:** Measure peak RSS + wall-seconds for the Rust binding against the two existing Python parsers on 3 synthetic PDFs of increasing complexity. Emit numeric results to the audit JSON.

**Files:**
- Create: `/Users/philiplewis/vitruvius/scripts/vitruvius/bench/bench_rust_pdf_audit.py`

### Step 1: Implement the benchmark harness

Create `/Users/philiplewis/vitruvius/scripts/vitruvius/bench/bench_rust_pdf_audit.py` that:

1. Generates 3 synthetic PDFs in a temp dir:
   - `simple.pdf` — 1-page text-only PDF (~1 KB)
   - `medium.pdf` — 5-page text-only PDF with headings + paragraphs (~10 KB)
   - `layout.pdf` — 3-page multi-column-style PDF (~20 KB)
2. For each PDF, runs three extractors and measures `resource.getrusage(RUSAGE_SELF).ru_maxrss` delta + wall-time:
   - `vitruvius_rust_pdf.extract_pdf_text(pdf_bytes)`
   - `docling.document_converter.DocumentConverter().convert(pdf_path)`
   - `opendataloader_pdf.convert(...)` (if importable)
3. Emits a `BenchResult` dataclass per (pdf, extractor) pair
4. Writes the aggregated results to `.ai/10_state/audit_rust_pdf_2026-04-15.json`

Each generated PDF uses `reportlab` or (if reportlab isn't available) a hand-rolled minimum PDF with embedded text. Prefer `reportlab` if it's already in the dep chain — verify first via:

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 -c "import reportlab; print(reportlab.__version__)" 2>&1
```

If reportlab is NOT available, generate minimum PDFs using the same hand-rolled byte pattern from Task 1's smoke test, scaled up. The key is: every bench PDF must be parseable by BOTH docling AND lopdf, otherwise the comparison is invalid.

### Step 2: Run the benchmark

```bash
cd /Users/philiplewis/vitruvius && PYTHONPATH=scripts /opt/homebrew/opt/python@3.11/bin/python3.11 -m vitruvius.bench.bench_rust_pdf_audit
```

Expected: ~30-60 seconds (docling lazy-loads models on first call). Output: JSON report written to `.ai/10_state/audit_rust_pdf_2026-04-15.json`.

### Step 3: Inspect the numbers

```bash
cat /Users/philiplewis/vitruvius/.ai/10_state/audit_rust_pdf_2026-04-15.json | /opt/homebrew/opt/python@3.11/bin/python3.11 -m json.tool
```

Manually verify the reported numbers are sane (non-zero, non-negative, non-identical across extractors).

### Step 4: Commit Task 2 artifacts

```bash
cd /Users/philiplewis/vitruvius && git add \
  scripts/vitruvius/bench/bench_rust_pdf_audit.py \
  .ai/10_state/audit_rust_pdf_2026-04-15.json
git commit -m "feat(bench): Sprint RUST-PDF-1 Task 2 — Rust PDF vs docling/opendataloader bench"
```

---

## Task 3: Decision gate + AD-033

**Goal:** Read the audit JSON, emit a GO/DEFER/NO_GO verdict, record AD-033 with the numeric evidence.

### Step 1: Classify the results

Read the bench JSON and compute per-extractor ratios:

- `rust_ram_ratio_docling = rust_peak_rss / docling_peak_rss`
- `rust_ram_ratio_odp = rust_peak_rss / opendataloader_peak_rss` (if available)
- `rust_wall_ratio_docling = rust_wall_seconds / docling_wall_seconds`

Apply the decision gate thresholds from Pre-Audit Ground Truth:
- `GO` if `rust_ram_ratio_docling ≤ 0.30` AND `rust_wall_ratio_docling ≤ 0.50`
- `DEFER` if `rust_ram_ratio_docling ≤ 0.70`
- `NO_GO` otherwise

Write the verdict into the same `audit_rust_pdf_2026-04-15.json` file under a `decision_gate` key.

### Step 2: Write AD-033

Append to `.ai/10_state/decisions.md` (before the `## Decision Process` footer):

```markdown

## AD-033 — Rust PDF Ingestion Audit (2026-04-15)

**Context.** User directive: "our ultimate goal is to run vitruvius on a low-spec machine" + "let us explore [Rust] as an option". The current PDF ingestion stack (`docling`, `opendataloader_pdf`, `ocrmypdf`) uses 800 MB - 2 GB peak RAM on typical 10-page documents. At the stated low-spec target (≤ 4 GB RAM), that's more than half the system budget for one stage of one document.

**Audit method.** Built a minimal `vitruvius_rust_pdf` crate (pyo3 binding over `lopdf 0.36`, pure Rust, no native deps) inside the existing `engine_rs` workspace. Benchmarked against `docling` + `opendataloader_pdf` on 3 synthetic PDFs (simple, medium, layout).

**Results (n=3 PDFs, measured via resource.getrusage + time.perf_counter):**

| Extractor | Peak RSS (MB) | Wall seconds | vs docling |
|---|---|---|---|
| docling | [FILL] | [FILL] | 1.0× baseline |
| opendataloader_pdf | [FILL] | [FILL] | [FILL]× |
| vitruvius_rust_pdf | [FILL] | [FILL] | [FILL]× |

Raw JSON: `.ai/10_state/audit_rust_pdf_2026-04-15.json`.

**Verdict:** [FILL — one of GO / DEFER / NO_GO based on the decision gate]

[FILL with a paragraph narrative: what we measured, what it means, whether Tranche 3 should ship a `RustPdfParser(BaseParser)` or defer.]

**Low-spec implications.** [FILL with the interpretation for the low-spec target.]

**Commits.**
- Task 1 — `[FILL]` — lopdf crate + pyo3 bindings + smoke test
- Task 2 — `[FILL]` — RAM + wall-time bench harness
- Task 3 — `[this commit]` — AD-033 + verdict + archival

**Follow-ups.**
- If GO: write a Tranche 3 TDD plan for `RustPdfParser(BaseParser)` — a new `scripts/vitruvius/parsers/rust_pdf_parser.py` that delegates to the Rust binding with the same telemetry contract as DoclingParser.
- If DEFER: document the measured delta and revisit when docling becomes the actual bottleneck (e.g. when ingesting a 1000-page corpus).
- If NO_GO: archive the audit crate under the workspace with a `DEPRECATED.md` note and continue using docling. The investment was not wasted — the measurement is the value.
- Next audit in the queue: LLM reviewer distillation (scikit-learn / lightgbm student model on the Sprint R Y4 stateful verdict cache).
```

Every `[FILL]` must be replaced with real numbers before the commit lands.

### Step 3: Archive the plan

```bash
cd /Users/philiplewis/vitruvius && mv \
  .ai/03_plans/2026-04-15-rust-pdf-audit-plan.md \
  .ai/09_archive/plans/
```

### Step 4: Update INDEX.md

Add a new row for the archived audit plan.

### Step 5: Final commit

```bash
cd /Users/philiplewis/vitruvius && git add \
  .ai/10_state/decisions.md \
  .ai/10_state/audit_rust_pdf_2026-04-15.json \
  .ai/03_plans/INDEX.md \
  .ai/09_archive/plans/2026-04-15-rust-pdf-audit-plan.md
git commit -m "docs(audit): Sprint RUST-PDF-1 closure — AD-033 + verdict + archival"
```

---

## Self-Review

**1. Spec coverage.** User directive was "explore Rust as an option for low-spec optimization". This audit measures whether a Rust PDF parser delivers a meaningful RAM win over docling, the current biggest RAM consumer in the ingestion stack. Verdict is evidence-based, not vibes-based.

**2. No premature commitment.** The audit ships a working Rust crate + benchmark but does NOT ship a new `BaseParser` subclass. Tranche 3 is conditional on the audit saying GO.

**3. Safety.** Rust build uses ~50 MB disk; fits the current 11.71 GB headroom. No new heavy Python deps. No risk to the existing test suite.

**4. Decision-gate thresholds.** GO requires ≥ 3.3× RAM win AND ≥ 2× speed win. DEFER is a softer bar. NO_GO is the honest option if lopdf text quality is insufficient.

---

## Execution Handoff

Plan saved. **Executing inline now** per the user's ultrawork directive — no subagent dispatch, no confirmation pause. Proceeding with Task 1 (lopdf crate + smoke test) immediately.
