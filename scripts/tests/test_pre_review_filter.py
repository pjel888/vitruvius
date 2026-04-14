"""Tests for the deterministic pre-review filter.

Triages candidates into auto_accept / auto_reject / needs_review BEFORE
they reach the LLM reviewer, so the LLM only judges genuinely uncertain
cases. See AD-018 in .ai/10_state/decisions.md for the design rationale.
"""

from vitruvius.pre_review_filter import TriageResult, triage_candidate, triage_candidates


def _cand(from_id, type_, to, occurrences=1, examples=None):
    return {
        "from": from_id,
        "type": type_,
        "to": to,
        "occurrences": occurrences,
        "sections": ["sec-101"],
        "examples": examples or ["Every building shall be classified in accordance with..."],
    }


# ---------- auto_reject rules ----------

def test_rule_r1_registry_incompatible_rejects():
    # concept -> defines -> concept is incompatible (defines needs source subject)
    result = triage_candidate(_cand("concept-a", "defines", "concept-b"))
    assert result.decision == "auto_reject"
    assert any("registry_incompatible" in r for r in result.reasons)


def test_rule_r2_evidence_too_short_rejects():
    result = triage_candidate(_cand("law-x", "governs", "concept-y", examples=["tiny"]))
    assert result.decision == "auto_reject"
    assert any("too_short" in r for r in result.reasons)


def test_negation_in_evidence_does_not_auto_reject():
    """Negation rule (R3) was removed on 2026-04-14 because it produced
    false rejects on legal text with embedded conditional clauses.
    Negated candidates now fall through to needs_review.
    """
    result = triage_candidate(_cand(
        "concept-a", "requires", "concept-b",
        examples=["Concept A requires compliance with concept B except in the following special cases enumerated below."],
    ))
    assert result.decision == "needs_review"


def test_rule_r5_self_reference_rejects():
    result = triage_candidate(_cand("concept-a", "requires", "concept-a"))
    assert result.decision == "auto_reject"
    assert any("self_reference" in r for r in result.reasons)


def test_rule_r7_endpoint_not_in_evidence_rejects():
    """If the evidence text doesn't mention the 'to' concept's phrase AND
    doesn't mention the 'from' concept's phrase, the regex extractor
    matched via a section window but the evidence is topically unrelated.
    This is the single most common false-positive pattern from the regex
    extractor: a noisy candidate where neither endpoint is in the actual
    evidence text.
    """
    # The evidence is about wood construction, not stairs at all.
    result = triage_candidate(_cand(
        "law-national-building-code-of-the-philippines",
        "governs",
        "concept-stairs",
        occurrences=2,
        examples=[
            "Type I buildings shall be of wood construction. The structural "
            "elements may be any of the materials permitted by this Code.",
        ],
    ))
    assert result.decision == "auto_reject"
    assert any("endpoint_not_in_evidence" in r for r in result.reasons)


def test_rule_r7_to_concept_in_evidence_passes():
    """If the evidence mentions the 'to' concept, R7 does not fire and
    the candidate proceeds through the other rules (ending in review).
    """
    result = triage_candidate(_cand(
        "concept-x",
        "requires",
        "concept-occupancy-classification",
        occurrences=1,
        examples=[
            "The occupancy classification shall be determined per the "
            "provisions of this section to ensure adequate safety margins "
            "and compliance with the regulatory framework."
        ],
    ))
    # Note: concept-x doesn't exist in the registry, so registry R1 may kick in
    # Let's use a valid pair instead
    result = triage_candidate(_cand(
        "concept-occupancy-separation",
        "requires",
        "concept-occupancy-classification",
        occurrences=1,
        examples=[
            "The occupancy classification shall be determined per the "
            "provisions of this section to ensure adequate safety margins "
            "and compliance with the regulatory framework."
        ],
    ))
    assert result.decision == "needs_review"


def test_rule_r7_from_concept_in_evidence_passes():
    """If the evidence mentions the 'from' concept (even if not the 'to'),
    R7 does not fire. This gives benefit of the doubt to candidates where
    at least one endpoint is discussed.
    """
    result = triage_candidate(_cand(
        "concept-occupancy-separation",
        "requires",
        "concept-occupancy-classification",
        occurrences=1,
        examples=[
            "Occupancy separation shall apply in accordance with the "
            "general provisions of the Code for buildings of mixed use "
            "configurations and related structural elements."
        ],
    ))
    # "occupancy separation" is present; "occupancy classification" is not.
    # R7 gives benefit of the doubt and sends to review.
    assert result.decision == "needs_review"


# ---------- auto_accept rules ----------

def test_rule_a1_strong_governs_pattern_accepts():
    # source->concept governs with recurrence + "shall" language
    result = triage_candidate(_cand(
        "law-national-building-code-of-the-philippines",
        "governs",
        "concept-building-permit",
        occurrences=3,
        examples=["No person shall erect any building without first obtaining a building permit issued under this Code."],
    ))
    assert result.decision == "auto_accept"
    assert result.confidence >= 0.90


def test_rule_a2_definitional_anchor_accepts():
    # source->concept defines with "shall mean"
    result = triage_candidate(_cand(
        "law-pd-1096",
        "defines",
        "concept-occupancy-classification",
        occurrences=2,
        examples=["Occupancy classification shall mean the categorization of a building by its use or occupancy..."],
    ))
    assert result.decision == "auto_accept"
    assert any("definitional" in r for r in result.reasons)


def test_rule_a4_concept_requires_pattern_accepts():
    """Concept->concept `requires` with 'shall comply' language and
    occurrences >= 2 is a strong deterministic auto-accept signal.
    """
    result = triage_candidate(_cand(
        "concept-occupancy-separation",
        "requires",
        "concept-occupancy-classification",
        occurrences=2,
        examples=["Occupancy separation shall comply with the classification rules set forth in this Code section."],
    ))
    assert result.decision == "auto_accept"
    assert any("concept_requires_pattern" in r for r in result.reasons)


def test_rule_a4_does_not_fire_without_keyword():
    """Without 'shall comply' or equivalent, concept->concept requires
    with low occurrence should still go to review.
    """
    result = triage_candidate(_cand(
        "concept-a",
        "requires",
        "concept-b",
        occurrences=2,
        examples=["Concept a may be related to concept b in certain contexts without strict requirement."],
    ))
    assert result.decision == "needs_review"


# ---------- needs_review (the fallthrough) ----------

def test_concept_to_concept_requires_goes_to_review():
    result = triage_candidate(_cand(
        "concept-occupancy-separation",
        "requires",
        "concept-occupancy-classification",
        occurrences=1,
        examples=["Occupancy separation requires analysis of the assigned occupancy classification group to determine fire-resistive ratings."],
    ))
    assert result.decision == "needs_review"


def test_single_occurrence_weak_evidence_goes_to_review():
    result = triage_candidate(_cand(
        "concept-a",
        "affects",
        "concept-b",
        occurrences=1,
        examples=["This section references concept a and concept b without clear linkage language."],
    ))
    assert result.decision == "needs_review"


# ---------- batch function ----------

def test_triage_candidates_returns_three_buckets():
    cands = [
        _cand("concept-x", "defines", "concept-y"),                          # auto_reject (R1)
        _cand("law-x", "governs", "concept-y", occurrences=3,
              examples=["No person shall erect any building without first obtaining a permit issued under this Code."]),  # auto_accept (A1)
        _cand("concept-a", "affects", "concept-b", occurrences=1,
              examples=["Section twelve references both concept a and concept b without clear linkage language."]),  # needs_review
    ]
    result = triage_candidates(cands)
    assert len(result["auto_accept"]) == 1
    assert len(result["auto_reject"]) == 1
    assert len(result["needs_review"]) == 1


def test_triage_result_dataclass():
    result = TriageResult(decision="auto_accept", confidence=0.95, reasons=["test"])
    assert result.decision == "auto_accept"
    assert result.confidence == 0.95
    assert result.reasons == ["test"]
