"""Sprint PIPELINE-CLI Task 2 — convert-parsers-one CLI handler.

Single-document Phase 1B parser-chain CLI entry point. Lives in the
parsers package so ``pipeline_cli.py`` can stay a pure dispatch shim
(per AD-015 lazy-import pattern: heavy parser/preprocessor modules
import only when this handler runs).

Output convention (matches the existing convert-one + Phase 1C
refine layout):

* Markdown → ``002_Raw-Conversion-Layer/<top_category>/refined_markdown/<...>/<stem>.md``
* Telemetry sidecar → ``006_System-Manifests/runs/latest_convert_parsers.json``

Exit codes:
* ``0`` — terminal_status is AUTO_ACCEPTED or AUTO_REFINED
* ``1`` — source missing OR terminal_status is FALLBACK_EXHAUSTED

Perf call: this handler sits **above the Rust Line** per AD-036.
Pure CLI orchestration: classify-by-extension, factory dispatch,
file write, exit-code mapping. The expensive work happens inside
:meth:`ParserOrchestrator.process` which routes to whichever parser
the factory registered (lopdf / docling / opendataloader / etc.).
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from vitruvius.parsers.document_taxonomy import (
    DocumentClass,
    DocumentFeatures,
    classify_document,
)
from vitruvius.parsers.factory import build_default_orchestrator
from vitruvius.parsers.orchestrator import (
    AttemptRecord,
    OrchestratorResult,
    TerminalStatus,
)
from vitruvius.paths import get_repo_root


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

_RAW_LAYER_NAME = "001_Raw-Source-Layer"
_CONVERSION_LAYER_NAME = "002_Raw-Conversion-Layer"
_MANIFESTS_NAME = "006_System-Manifests"
_RUNS_NAME = "runs"
_REFINED_DIR = "refined_markdown"
_TELEMETRY_FILENAME = "latest_convert_parsers.json"


def _get_repo_root() -> Path:
    """Indirection so tests can monkeypatch the root without
    monkey-patching the global :func:`vitruvius.paths.get_repo_root`."""
    return get_repo_root()


def _build_refined_path(repo_root: Path, relative_pdf_path: Path) -> Path:
    """Map ``001-Laws/PD-1096/doc.pdf`` →
    ``002_Raw-Conversion-Layer/001-Laws/refined_markdown/PD-1096/doc.md``.

    Mirrors the convention from
    :func:`vitruvius.normalization.refine.build_refined_paths` and the
    existing convert-one output layout.
    """
    parts = relative_pdf_path.parts
    if len(parts) < 2:
        raise ValueError(
            f"relative_pdf_path {relative_pdf_path} must have at least "
            "two path components: <top_category>/.../<stem>.<ext>"
        )
    top_category = parts[0]
    nested = parts[1:-1]
    stem = relative_pdf_path.stem
    return (
        repo_root
        / _CONVERSION_LAYER_NAME
        / top_category
        / _REFINED_DIR
        / Path(*nested)
        / f"{stem}.md"
    )


def _build_sidecar_path(repo_root: Path) -> Path:
    return repo_root / _MANIFESTS_NAME / _RUNS_NAME / _TELEMETRY_FILENAME


# ---------------------------------------------------------------------------
# Document classification (extension-only — no PDF inspection)
# ---------------------------------------------------------------------------

def _classify_by_extension(source_path: Path) -> DocumentClass:
    """Build a minimal :class:`DocumentFeatures` from the file extension
    and run it through :func:`classify_document`.

    No PDF inspection: we don't run pypdf or pdfminer at this layer
    because the Phase 1B parser chain itself handles fallback if the
    classification under-specifies (e.g. a TEXT_PDF_SIMPLE that turns
    out to be hybrid will trip GATE-006 and fall through to the next
    parser in the chain).
    """
    features = DocumentFeatures(extension=source_path.suffix.lower())
    return classify_document(features)


# ---------------------------------------------------------------------------
# Sidecar serialisation
# ---------------------------------------------------------------------------

def _attempt_to_dict(attempt: AttemptRecord) -> dict[str, Any]:
    parse_result = attempt.parse_result
    parse_summary: dict[str, Any] | None
    if parse_result is None:
        parse_summary = None
    else:
        parse_summary = {
            "telemetry": asdict(parse_result.telemetry),
            "sidecar_metadata": parse_result.sidecar_metadata,
        }
    gate_report = attempt.gate_report
    gate_summary: dict[str, Any] | None
    if gate_report is None:
        gate_summary = None
    else:
        gate_summary = {
            "passed": gate_report.passed,
            "results": [
                {
                    "gate_id": r.gate_id,
                    "gate_name": r.gate_name,
                    "status": r.status.value,
                    "reason": r.reason,
                }
                for r in gate_report.results
            ],
        }
    return {
        "parser_id": attempt.parser_id,
        "attempt_index": attempt.attempt_index,
        "exception": attempt.exception,
        "parse_result": parse_summary,
        "gate_report": gate_summary,
    }


def _build_sidecar_payload(
    *,
    relative_pdf_path: Path,
    doc_class: DocumentClass,
    result: OrchestratorResult,
) -> dict[str, Any]:
    return {
        "relative_pdf_path": str(relative_pdf_path),
        "doc_class": doc_class.value,
        "terminal_status": result.terminal_status.value,
        "successful_parser_id": result.successful_parser_id,
        "attempts": [_attempt_to_dict(a) for a in result.attempts],
    }


def _write_sidecar(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_convert_parsers_one(*, relative_pdf_path: str | Path) -> int:
    """Run the Phase 1B parser chain on a single document.

    Args:
        relative_pdf_path: Path relative to ``001_Raw-Source-Layer``.
            E.g. ``"001-Laws/PD-1096/doc.pdf"``.

    Returns:
        Exit code: 0 on AUTO_ACCEPTED/AUTO_REFINED, 1 on missing source
        or FALLBACK_EXHAUSTED.
    """
    rel = Path(relative_pdf_path)
    repo_root = _get_repo_root()
    source_path = repo_root / _RAW_LAYER_NAME / rel

    if not source_path.exists():
        print(f"ERROR: source file not found: {source_path}")
        return 1

    try:
        doc_class = _classify_by_extension(source_path)
    except Exception as exc:
        print(f"ERROR: classification failed for {source_path}: {exc}")
        return 1

    try:
        orchestrator = build_default_orchestrator()
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    work_dir = repo_root / _CONVERSION_LAYER_NAME / "_p1b_work" / rel.stem
    work_dir.mkdir(parents=True, exist_ok=True)

    try:
        result = orchestrator.process(
            source_path=source_path,
            doc_class=doc_class,
            work_dir=work_dir,
        )
    except KeyError as exc:
        print(
            f"ERROR: no parser chain registered for doc_class "
            f"{doc_class.value!r}: {exc}"
        )
        return 1

    sidecar_path = _build_sidecar_path(repo_root)
    payload = _build_sidecar_payload(
        relative_pdf_path=rel,
        doc_class=doc_class,
        result=result,
    )
    _write_sidecar(sidecar_path, payload)

    if result.terminal_status in {
        TerminalStatus.AUTO_ACCEPTED,
        TerminalStatus.AUTO_REFINED,
    }:
        if result.final_parse_result is None:
            # Defensive: should never happen for a non-fallback status.
            print(
                f"ERROR: terminal_status={result.terminal_status.value} but "
                "final_parse_result is None"
            )
            return 1
        markdown = result.final_parse_result.markdown_text
        refined_path = _build_refined_path(repo_root, rel)
        refined_path.parent.mkdir(parents=True, exist_ok=True)
        refined_path.write_text(markdown, encoding="utf-8")
        print(
            f"OK: status={result.terminal_status.value} "
            f"parser={result.successful_parser_id} "
            f"out={refined_path}"
        )
        return 0

    # FALLBACK_EXHAUSTED — print the first attempt's error if any.
    first_error = next(
        (a.exception for a in result.attempts if a.exception),
        "no attempt errors recorded",
    )
    print(
        f"ERROR: parser chain exhausted for {rel} "
        f"(doc_class={doc_class.value}): {first_error}"
    )
    return 1
