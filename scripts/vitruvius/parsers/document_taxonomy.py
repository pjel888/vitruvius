from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..features import Features


class DocumentClass(str, Enum):
    TEXT_PDF_SIMPLE = "text_pdf_simple"
    TEXT_PDF_COMPLEX = "text_pdf_complex"
    SCANNED_PDF_CLEAN = "scanned_pdf_clean"
    SCANNED_PDF_NOISY = "scanned_pdf_noisy"
    HYBRID_PDF = "hybrid_pdf"
    OFFICE_DOC = "office_doc"
    OFFICE_SLIDE = "office_slide"
    SPREADSHEET_STRUCTURED = "spreadsheet_structured"
    SPREADSHEET_UNSTRUCTURED = "spreadsheet_unstructured"


@dataclass(kw_only=True, frozen=True)
class DocumentFeatures:
    extension: str                    # e.g. ".pdf", ".docx", ".xlsx", ".csv"
    text_density: float = 0.0         # chars / visual_area
    image_density: float = 0.0
    vector_density: float = 0.0
    ocr_confidence: float | None = None  # None when OCR was never run (text-embedded PDF)
    table_clues: float = 0.0
    garbled_ratio: float = 0.0
    non_empty_col_ratio: float = 0.0  # spreadsheets: ratio of non-empty cols in first 5 rows


def classify_document(
    doc: DocumentFeatures,
    *,
    features: Features | None = None,
    text_sample: str | None = None,
) -> DocumentClass:
    """Classify a document into one of the nine DocumentClass values.

    Priority order (highest wins):
      0 — Extension shortcuts  (CL-001, CL-002, CL-003)
      1 — Scanned PDF          (CL-004, CL-005) — only when ocr_confidence is not None
      2 — Hybrid PDF           (CL-006)
      3 — Complex PDF          (CL-007)
      4 — Simple PDF           (CL-008)
      5 — Fallback             → TEXT_PDF_SIMPLE

    CL-004 and CL-005 are mutually exclusive by construction (OR vs AND logic).
    The ocr_confidence is None guard ensures text-embedded PDFs never classify
    as scanned even if their density features overlap with the scanned conditions.

    When `features.b_shannon_classifier` is enabled and `text_sample` scores
    "garbled" via the Shannon composite metric, the result is escalated to
    SCANNED_PDF_NOISY regardless of the density heuristics. With the flag off
    or no text_sample provided, behaviour is byte-identical to pre-change.
    """
    if (
        features is not None
        and text_sample is not None
        and features.is_enabled("b_shannon_classifier")
    ):
        from .shannon_classifier import classify_by_entropy

        if classify_by_entropy(text_sample) == "garbled":
            return DocumentClass.SCANNED_PDF_NOISY

    ext = doc.extension

    # ------------------------------------------------------------------
    # Priority 0 — Extension shortcuts (CL-001, CL-002, CL-003)
    # ------------------------------------------------------------------

    if ext == ".docx":
        return DocumentClass.OFFICE_DOC

    if ext == ".pptx":
        return DocumentClass.OFFICE_SLIDE

    if ext in {".xlsx", ".csv"}:
        if doc.non_empty_col_ratio > 0.8:
            return DocumentClass.SPREADSHEET_STRUCTURED
        return DocumentClass.SPREADSHEET_UNSTRUCTURED

    # ------------------------------------------------------------------
    # Priority 1 — Scanned PDF (CL-004, CL-005)
    # Only applies when OCR was actually run (ocr_confidence is not None).
    # ------------------------------------------------------------------

    if doc.ocr_confidence is not None:
        if doc.ocr_confidence < 0.85 or doc.garbled_ratio >= 0.05:
            return DocumentClass.SCANNED_PDF_NOISY  # CL-004
        return DocumentClass.SCANNED_PDF_CLEAN      # CL-005

    # ------------------------------------------------------------------
    # Priority 2 — Hybrid PDF (CL-006)
    # ------------------------------------------------------------------

    if 0.3 <= doc.text_density <= 0.7 and doc.image_density >= 0.2:
        return DocumentClass.HYBRID_PDF

    # ------------------------------------------------------------------
    # Priority 3 — Complex PDF (CL-007)
    # ------------------------------------------------------------------

    if doc.text_density > 0.6 and (
        doc.table_clues >= 0.2 or doc.vector_density >= 0.2
    ):
        return DocumentClass.TEXT_PDF_COMPLEX

    # ------------------------------------------------------------------
    # Priority 4 — Simple PDF (CL-008)
    # ------------------------------------------------------------------

    if (
        doc.text_density > 0.85
        and doc.table_clues < 0.1
        and doc.image_density < 0.1
    ):
        return DocumentClass.TEXT_PDF_SIMPLE

    # ------------------------------------------------------------------
    # Priority 5 — Fallback (conservative; orchestrator fallback chain
    # will catch any misclassifications downstream)
    # ------------------------------------------------------------------

    return DocumentClass.TEXT_PDF_SIMPLE
