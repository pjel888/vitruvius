"""Sprint 1B-M3 Task 1 — Rust PDF text-quality spot check.

Compares vitruvius_rust_pdf.extract_pdf_text output against pypdf's
extract_text output on a real PDF. Computes a longest-common-subsequence
ratio as a char-level similarity proxy. If similarity < 0.70, this
script emits NO_GO and exits non-zero so the Tranche 3 execution
halts before we ship a RustPdfParser that regresses text quality.

Rollback gate: this is the guard AD-033 promised. Without it, we'd
be trusting the synthetic-PDF bench to predict quality on real
documents — which is exactly the kind of mistake Sprint HP.3-R's
o(n²) count() regression taught us to guard against.
"""
from __future__ import annotations

import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class QualityCheckResult:
    pdf_path: str
    rust_char_count: int
    pypdf_char_count: int
    lcs_length: int
    similarity_ratio: float
    recommendation: str  # "GO" | "NO_GO"
    notes: str


def _lcs_length(a: str, b: str) -> int:
    """Longest common subsequence length, space-efficient (O(min(m,n))).

    At ~10k char documents this runs in a few seconds and doesn't
    blow memory. For the Tranche 3 quality gate we accept the
    cost — quality validation is a one-shot decision, not a hot
    path.
    """
    if not a or not b:
        return 0
    # Ensure we use the shorter string for the column dimension to minimize memory.
    if len(a) < len(b):
        a, b = b, a
    # a is the longer one; b is shorter.
    prev = [0] * (len(b) + 1)
    curr = [0] * (len(b) + 1)
    for i, ca in enumerate(a, 1):
        for j, cb in enumerate(b, 1):
            if ca == cb:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
        for j in range(len(curr)):
            curr[j] = 0
    return prev[-1]


def run_quality_check(pdf_path: Path) -> QualityCheckResult:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        return QualityCheckResult(
            pdf_path=str(pdf_path),
            rust_char_count=0,
            pypdf_char_count=0,
            lcs_length=0,
            similarity_ratio=0.0,
            recommendation="NO_GO",
            notes=f"reference PDF not found: {pdf_path}",
        )

    try:
        import vitruvius_rust_pdf
    except ImportError as exc:
        return QualityCheckResult(
            pdf_path=str(pdf_path),
            rust_char_count=0,
            pypdf_char_count=0,
            lcs_length=0,
            similarity_ratio=0.0,
            recommendation="NO_GO",
            notes=f"vitruvius_rust_pdf not installed: {exc}",
        )

    try:
        import pypdf
    except ImportError as exc:
        return QualityCheckResult(
            pdf_path=str(pdf_path),
            rust_char_count=0,
            pypdf_char_count=0,
            lcs_length=0,
            similarity_ratio=0.0,
            recommendation="NO_GO",
            notes=f"pypdf not installed: {exc}",
        )

    pdf_bytes = pdf_path.read_bytes()

    try:
        rust_text = vitruvius_rust_pdf.extract_pdf_text(pdf_bytes)
    except ValueError as exc:
        return QualityCheckResult(
            pdf_path=str(pdf_path),
            rust_char_count=0,
            pypdf_char_count=0,
            lcs_length=0,
            similarity_ratio=0.0,
            recommendation="NO_GO",
            notes=f"vitruvius_rust_pdf failed: {exc}",
        )

    try:
        reader = pypdf.PdfReader(str(pdf_path))
        pypdf_pages: list[str] = []
        for page in reader.pages:
            pypdf_pages.append(page.extract_text() or "")
        pypdf_text = "\n\n".join(pypdf_pages)
    except Exception as exc:
        return QualityCheckResult(
            pdf_path=str(pdf_path),
            rust_char_count=len(rust_text),
            pypdf_char_count=0,
            lcs_length=0,
            similarity_ratio=0.0,
            recommendation="NO_GO",
            notes=f"pypdf failed: {exc}",
        )

    # Normalize whitespace so tiny formatting differences don't wreck the LCS.
    import re
    normalized_rust = re.sub(r"\s+", " ", rust_text).strip().lower()
    normalized_pypdf = re.sub(r"\s+", " ", pypdf_text).strip().lower()

    # Truncate both to the first 5000 chars — LCS is O(n*m) and we don't
    # need the full document to judge quality parity on a sample page.
    sample_n = 5000
    rust_sample = normalized_rust[:sample_n]
    pypdf_sample = normalized_pypdf[:sample_n]

    lcs = _lcs_length(rust_sample, pypdf_sample)
    denom = max(len(rust_sample), len(pypdf_sample), 1)
    similarity = lcs / denom

    if similarity >= 0.70:
        recommendation = "GO"
        notes = (
            f"rust/pypdf LCS similarity {similarity:.3f} meets the 0.70 threshold; "
            f"Tranche 3 RustPdfParser is cleared to ship. Sample size: {sample_n} chars."
        )
    else:
        recommendation = "NO_GO"
        notes = (
            f"rust/pypdf LCS similarity {similarity:.3f} below 0.70 threshold; "
            f"Tranche 3 RustPdfParser MUST NOT ship without investigation. "
            f"rust_chars={len(rust_text)}, pypdf_chars={len(pypdf_text)}."
        )

    return QualityCheckResult(
        pdf_path=str(pdf_path),
        rust_char_count=len(rust_text),
        pypdf_char_count=len(pypdf_text),
        lcs_length=lcs,
        similarity_ratio=round(similarity, 4),
        recommendation=recommendation,
        notes=notes,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rust PDF text-quality spot check")
    parser.add_argument(
        "--pdf",
        type=Path,
        default=Path(
            "/Users/philiplewis/vitruvius/001_Raw-Source-Layer/002-History/"
            "History of Architecture Sample Exam.pdf"
        ),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(".ai/10_state/quality_check_rust_pdf_2026-04-15.json"),
    )
    args = parser.parse_args()

    start = time.perf_counter()
    result = run_quality_check(args.pdf)
    elapsed = time.perf_counter() - start

    report = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_seconds": round(elapsed, 3),
        "result": asdict(result),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

    if result.recommendation != "GO":
        sys.exit(1)
    sys.exit(0)
