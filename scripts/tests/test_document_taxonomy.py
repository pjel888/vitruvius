from __future__ import annotations

import dataclasses

import pytest

from scripts.vitruvius.parsers.document_taxonomy import (
    DocumentClass,
    DocumentFeatures,
    classify_document,
)


# ---------------------------------------------------------------------------
# Enum / dataclass smoke tests
# ---------------------------------------------------------------------------


def test_document_class_has_nine_members() -> None:
    assert len(DocumentClass) == 9
    expected_values = {
        "text_pdf_simple",
        "text_pdf_complex",
        "scanned_pdf_clean",
        "scanned_pdf_noisy",
        "hybrid_pdf",
        "office_doc",
        "office_slide",
        "spreadsheet_structured",
        "spreadsheet_unstructured",
    }
    assert {m.value for m in DocumentClass} == expected_values


def test_document_features_frozen() -> None:
    features = DocumentFeatures(extension=".pdf")
    with pytest.raises((dataclasses.FrozenInstanceError, TypeError, AttributeError)):
        features.extension = ".docx"  # type: ignore[misc]


def test_document_features_kw_only() -> None:
    with pytest.raises(TypeError):
        DocumentFeatures(".pdf")  # type: ignore[misc]  # positional not allowed


# ---------------------------------------------------------------------------
# CL-001 — .docx → OFFICE_DOC
# ---------------------------------------------------------------------------


def test_cl001_docx_classifies_as_office_doc() -> None:
    features = DocumentFeatures(extension=".docx")
    assert classify_document(features) == DocumentClass.OFFICE_DOC


# ---------------------------------------------------------------------------
# CL-002 — .pptx → OFFICE_SLIDE
# ---------------------------------------------------------------------------


def test_cl002_pptx_classifies_as_office_slide() -> None:
    features = DocumentFeatures(extension=".pptx")
    assert classify_document(features) == DocumentClass.OFFICE_SLIDE


# ---------------------------------------------------------------------------
# CL-003 — .xlsx / .csv → SPREADSHEET_STRUCTURED or UNSTRUCTURED
# ---------------------------------------------------------------------------


def test_cl003_xlsx_structured_classifies_as_structured() -> None:
    features = DocumentFeatures(extension=".xlsx", non_empty_col_ratio=0.9)
    assert classify_document(features) == DocumentClass.SPREADSHEET_STRUCTURED


def test_cl003_xlsx_unstructured_classifies_as_unstructured() -> None:
    features = DocumentFeatures(extension=".xlsx", non_empty_col_ratio=0.5)
    assert classify_document(features) == DocumentClass.SPREADSHEET_UNSTRUCTURED


@pytest.mark.parametrize(
    "ratio, expected",
    [
        (0.9, DocumentClass.SPREADSHEET_STRUCTURED),
        (0.5, DocumentClass.SPREADSHEET_UNSTRUCTURED),
    ],
)
def test_cl003_csv_structured_and_unstructured(
    ratio: float, expected: DocumentClass
) -> None:
    features = DocumentFeatures(extension=".csv", non_empty_col_ratio=ratio)
    assert classify_document(features) == expected


# ---------------------------------------------------------------------------
# CL-004 — scanned PDF noisy
# ---------------------------------------------------------------------------


def test_cl004_scanned_pdf_noisy_low_confidence() -> None:
    # Low ocr_confidence triggers noisy even with no garbling
    features = DocumentFeatures(extension=".pdf", ocr_confidence=0.70, garbled_ratio=0.0)
    assert classify_document(features) == DocumentClass.SCANNED_PDF_NOISY


def test_cl004_scanned_pdf_noisy_high_garbled() -> None:
    # High garbled_ratio triggers noisy even with good confidence
    features = DocumentFeatures(extension=".pdf", ocr_confidence=0.95, garbled_ratio=0.10)
    assert classify_document(features) == DocumentClass.SCANNED_PDF_NOISY


# ---------------------------------------------------------------------------
# CL-005 — scanned PDF clean
# ---------------------------------------------------------------------------


def test_cl005_scanned_pdf_clean() -> None:
    features = DocumentFeatures(extension=".pdf", ocr_confidence=0.95, garbled_ratio=0.01)
    assert classify_document(features) == DocumentClass.SCANNED_PDF_CLEAN


# ---------------------------------------------------------------------------
# CL-006 — hybrid PDF
# ---------------------------------------------------------------------------


def test_cl006_hybrid_pdf() -> None:
    features = DocumentFeatures(extension=".pdf", text_density=0.5, image_density=0.3)
    assert classify_document(features) == DocumentClass.HYBRID_PDF


# ---------------------------------------------------------------------------
# CL-007 — text PDF complex
# ---------------------------------------------------------------------------


def test_cl007_text_pdf_complex_tables() -> None:
    features = DocumentFeatures(extension=".pdf", text_density=0.75, table_clues=0.3)
    assert classify_document(features) == DocumentClass.TEXT_PDF_COMPLEX


def test_cl007_text_pdf_complex_vectors() -> None:
    features = DocumentFeatures(extension=".pdf", text_density=0.75, vector_density=0.3)
    assert classify_document(features) == DocumentClass.TEXT_PDF_COMPLEX


# ---------------------------------------------------------------------------
# CL-008 — text PDF simple
# ---------------------------------------------------------------------------


def test_cl008_text_pdf_simple() -> None:
    features = DocumentFeatures(
        extension=".pdf",
        text_density=0.95,
        table_clues=0.05,
        image_density=0.05,
    )
    assert classify_document(features) == DocumentClass.TEXT_PDF_SIMPLE


# ---------------------------------------------------------------------------
# Fallback
# ---------------------------------------------------------------------------


def test_fallback_returns_text_pdf_simple() -> None:
    # text_density=0.5 with low images/tables/vectors — matches none of the
    # explicit PDF rules (not scanned, not hybrid range with enough image, not
    # complex, not simple-threshold), so falls back.
    features = DocumentFeatures(
        extension=".pdf",
        text_density=0.5,
        image_density=0.05,
        table_clues=0.05,
        vector_density=0.05,
    )
    assert classify_document(features) == DocumentClass.TEXT_PDF_SIMPLE


# ---------------------------------------------------------------------------
# Boundary / corner cases
# ---------------------------------------------------------------------------


def test_ocr_confidence_none_never_classifies_scanned() -> None:
    # ocr_confidence=None → CL-004/CL-005 are skipped entirely.
    # Features that would otherwise match CL-004 must not return SCANNED_PDF_NOISY.
    features = DocumentFeatures(
        extension=".pdf",
        ocr_confidence=None,  # explicit None — OCR was never run
        garbled_ratio=0.10,   # would trigger CL-004 if ocr_confidence were set
        text_density=0.5,
        image_density=0.05,
    )
    result = classify_document(features)
    assert result not in (DocumentClass.SCANNED_PDF_NOISY, DocumentClass.SCANNED_PDF_CLEAN)


def test_text_density_070_satisfies_hybrid_upper_bound() -> None:
    # 0.7 is the inclusive upper bound for CL-006: 0.3 <= td <= 0.7
    features = DocumentFeatures(extension=".pdf", text_density=0.7, image_density=0.2)
    assert classify_document(features) == DocumentClass.HYBRID_PDF


def test_text_density_030_satisfies_hybrid_lower_bound() -> None:
    # 0.3 is the inclusive lower bound for CL-006
    features = DocumentFeatures(extension=".pdf", text_density=0.3, image_density=0.2)
    assert classify_document(features) == DocumentClass.HYBRID_PDF


def test_ocr_confidence_boundary_085_classifies_clean() -> None:
    # Exactly 0.85 must go to CL-005 clean (>= 0.85), not CL-004 noisy (< 0.85)
    features = DocumentFeatures(
        extension=".pdf",
        ocr_confidence=0.85,
        garbled_ratio=0.01,
    )
    assert classify_document(features) == DocumentClass.SCANNED_PDF_CLEAN


def test_priority_extension_beats_features() -> None:
    # .docx with high text_density / ocr_confidence should still → OFFICE_DOC
    features = DocumentFeatures(
        extension=".docx",
        text_density=0.95,
        ocr_confidence=0.70,
        garbled_ratio=0.10,
        image_density=0.3,
    )
    assert classify_document(features) == DocumentClass.OFFICE_DOC


def test_priority_scanned_beats_hybrid() -> None:
    # A scanned noisy doc whose densities also satisfy the hybrid window must
    # still return SCANNED_PDF_NOISY (scanned > hybrid per §4 priority order).
    features = DocumentFeatures(
        extension=".pdf",
        ocr_confidence=0.70,   # CL-004 noisy
        garbled_ratio=0.0,
        text_density=0.5,      # also within CL-006 hybrid window
        image_density=0.3,
    )
    assert classify_document(features) == DocumentClass.SCANNED_PDF_NOISY


def test_spreadsheet_non_empty_col_ratio_080_is_unstructured() -> None:
    # CL-003 rule: STRUCTURED requires > 0.8 (strict). Exactly 0.8 → UNSTRUCTURED.
    features = DocumentFeatures(extension=".xlsx", non_empty_col_ratio=0.8)
    assert classify_document(features) == DocumentClass.SPREADSHEET_UNSTRUCTURED
