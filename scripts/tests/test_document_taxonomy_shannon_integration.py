"""Integration: document_taxonomy honors features.b_shannon_classifier.

Task B.2 of Stream B. With the flag OFF, classify_document behaves exactly
as before. With the flag ON and a sample text that is garbled per the
Shannon composite metric, the classifier escalates the return to
SCANNED_PDF_NOISY regardless of what the density heuristics say.
"""

from __future__ import annotations

from vitruvius.features import Features
from vitruvius.parsers.document_taxonomy import (
    DocumentClass,
    DocumentFeatures,
    classify_document,
)
from vitruvius.parsers.shannon_classifier import classify_by_entropy


_GARBLED_SAMPLE = "B@1!d#$%^&*()+=<>?/|\\~`\x01\x02\x03\x04\x05\x06\x07\x0b\x0c\x0e\x0f\x10\x11\x12"


def _simple_pdf_features() -> DocumentFeatures:
    return DocumentFeatures(
        extension=".pdf",
        text_density=0.95,
        table_clues=0.05,
        image_density=0.05,
    )


def test_shannon_sample_is_actually_garbled() -> None:
    assert classify_by_entropy(_GARBLED_SAMPLE) == "garbled"


def test_high_entropy_text_with_flag_off_uses_baseline_density_only() -> None:
    doc = _simple_pdf_features()
    flags = Features(flags={})
    result = classify_document(
        doc,
        features=flags,
        text_sample=_GARBLED_SAMPLE,
    )
    assert result == DocumentClass.TEXT_PDF_SIMPLE


def test_high_entropy_text_with_flag_on_overrides_to_scanned_noisy() -> None:
    doc = _simple_pdf_features()
    flags = Features(flags={"b_shannon_classifier": True})
    result = classify_document(
        doc,
        features=flags,
        text_sample=_GARBLED_SAMPLE,
    )
    assert result == DocumentClass.SCANNED_PDF_NOISY


def test_flag_on_but_clean_sample_does_not_override() -> None:
    doc = _simple_pdf_features()
    flags = Features(flags={"b_shannon_classifier": True})
    result = classify_document(
        doc,
        features=flags,
        text_sample="The quick brown fox jumps over the lazy dog.",
    )
    assert result == DocumentClass.TEXT_PDF_SIMPLE


def test_flag_on_but_no_text_sample_does_not_override() -> None:
    doc = _simple_pdf_features()
    flags = Features(flags={"b_shannon_classifier": True})
    result = classify_document(doc, features=flags)
    assert result == DocumentClass.TEXT_PDF_SIMPLE


def test_existing_positional_call_still_works() -> None:
    doc = _simple_pdf_features()
    assert classify_document(doc) == DocumentClass.TEXT_PDF_SIMPLE
