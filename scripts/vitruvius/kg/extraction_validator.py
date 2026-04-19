"""Extraction Validator — deterministic gate between LLM output and canonical promotion.

Validates ``KnowledgeUnitCandidate`` and ``ExtractionResult`` objects against
a set of structural and semantic rules before they enter the canonicalization
pipeline.  This is the safety gate referenced in Phase 6 of the KG transition.

Rules
-----
E1  unit_type must be in the allowed vocabulary
E2  label must be non-empty and ≤ 200 chars
E3  text must be non-empty and ≤ 4096 chars
E4  confidence must be in [0.0, 1.0]
E5  span_ids must be non-empty (every candidate needs evidence)
E6  chunk_id must be non-empty (traceability)
E7  label must not be generic filler (e.g. "undefined", "n/a")
E8  text must not be pure repetition of label
E9  extraction_run_id must be non-empty
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .schemas import ExtractionResult, KnowledgeUnitCandidate


ALLOWED_UNIT_TYPES = {"concept", "definition", "rule", "procedure", "exception"}
GENERIC_FILLERS = {"undefined", "n/a", "none", "null", "", "unknown"}


@dataclass
class ExtractionValidationResult:
    passed: bool
    errors: list[str] = field(default_factory=list)
    candidate_id: str = ""


class ExtractionValidator:
    """Validate extracted candidates before canonical promotion."""

    def __init__(self, min_confidence: float = 0.0, strict_traceability: bool = True) -> None:
        self.min_confidence = min_confidence
        self.strict_traceability = strict_traceability

    # -- public API ----------------------------------------------------------

    def validate_candidate(
        self, candidate: KnowledgeUnitCandidate
    ) -> ExtractionValidationResult:
        """Validate a single candidate."""
        errors: list[str] = []

        # E1 unit_type
        if candidate.unit_type not in ALLOWED_UNIT_TYPES:
            errors.append(
                f"E1: unit_type '{candidate.unit_type}' not in {ALLOWED_UNIT_TYPES}"
            )

        # E2 label
        label = candidate.label.strip()
        if not label:
            errors.append("E2: label is empty")
        elif len(label) > 200:
            errors.append(f"E2: label length {len(label)} exceeds 200")

        # E3 text
        text = candidate.text.strip()
        if not text:
            errors.append("E3: text is empty")
        elif len(text) > 4096:
            errors.append(f"E3: text length {len(text)} exceeds 4096")

        # E4 confidence
        if not (0.0 <= candidate.confidence <= 1.0):
            errors.append(f"E4: confidence {candidate.confidence} outside [0.0, 1.0]")
        if candidate.confidence < self.min_confidence:
            errors.append(
                f"E4: confidence {candidate.confidence} below minimum {self.min_confidence}"
            )

        # E5 span_ids (optional unless strict_traceability)
        if self.strict_traceability and not candidate.span_ids:
            errors.append("E5: span_ids is empty (candidate lacks evidence)")

        # E6 chunk_id
        if not candidate.chunk_id:
            errors.append("E6: chunk_id is empty (not traceable)")

        # E7 generic filler label
        if label.lower() in GENERIC_FILLERS:
            errors.append(f"E7: label '{label}' is a generic filler")

        # E8 text is not just label repetition
        if text.lower() == label.lower():
            errors.append("E8: text is identical to label (no substantive content)")

        # E9 extraction_run_id (optional unless strict_traceability)
        if self.strict_traceability and not candidate.extraction_run_id:
            errors.append("E9: extraction_run_id is empty")

        passed = not errors
        return ExtractionValidationResult(
            passed=passed,
            errors=errors,
            candidate_id=candidate.id,
        )

    def validate_result(
        self, result: ExtractionResult
    ) -> list[ExtractionValidationResult]:
        """Validate all candidates in an extraction result."""
        return [self.validate_candidate(c) for c in result.candidates]

    def filter_valid(
        self, candidates: list[KnowledgeUnitCandidate]
    ) -> list[KnowledgeUnitCandidate]:
        """Return only candidates that pass validation."""
        valid: list[KnowledgeUnitCandidate] = []
        for cand in candidates:
            result = self.validate_candidate(cand)
            if result.passed:
                valid.append(cand)
        return valid
