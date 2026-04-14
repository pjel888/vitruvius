"""Deterministic pre-review filter (AD-018).

Triages regex-extracted relationship candidates BEFORE they reach the LLM
reviewer. The goal is to minimize LLM invocations on a resource-constrained
machine: auto-accept the structurally-obvious keeps, auto-reject the
structurally-obvious junk, and only hand the genuinely-uncertain middle
bucket to the LLM.

The filter uses only information already present in a candidate:
- `from` / `to` / `type` (for registry compatibility)
- `occurrences` (signal strength)
- `examples` (evidence text)

It never calls the LLM. It never touches disk except to load the registry.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


# Characteristic predicate phrases. Candidates whose evidence contains any of
# these for their declared predicate are strong auto-accept candidates.
PREDICATE_KEYWORDS: dict[str, list[re.Pattern]] = {
    "governs": [
        re.compile(r"\bshall\b", re.IGNORECASE),
        re.compile(r"\bissued under\b", re.IGNORECASE),
        re.compile(r"\bpursuant to\b", re.IGNORECASE),
        re.compile(r"\bthis code\b", re.IGNORECASE),
    ],
    "defines": [
        re.compile(r"\bshall mean\b", re.IGNORECASE),
        re.compile(r"\bis defined as\b", re.IGNORECASE),
        re.compile(r"\bmeans\b", re.IGNORECASE),
        re.compile(r"\brefers to\b", re.IGNORECASE),
    ],
    "requires": [
        re.compile(r"\bshall comply with\b", re.IGNORECASE),
        re.compile(r"\brequired to\b", re.IGNORECASE),
        re.compile(r"\bmust\b", re.IGNORECASE),
    ],
    "limits": [
        re.compile(r"\bshall not exceed\b", re.IGNORECASE),
        re.compile(r"\bmaximum\b", re.IGNORECASE),
        re.compile(r"\bno greater than\b", re.IGNORECASE),
    ],
}

# Negation markers. Evidence containing any of these near the main clause
# often represents an exception, not the relationship itself.
NEGATION_PATTERNS = [
    re.compile(r"\bshall not\b", re.IGNORECASE),
    re.compile(r"\bexcept\b", re.IGNORECASE),
    re.compile(r"\bunless\b", re.IGNORECASE),
    re.compile(r"\bdoes not apply\b", re.IGNORECASE),
    re.compile(r"\bno(?:t)?\s+required\b", re.IGNORECASE),
]

MIN_EVIDENCE_CHARS = 30


@dataclass
class TriageResult:
    decision: str  # "auto_accept" | "auto_reject" | "needs_review"
    confidence: float
    reasons: list[str] = field(default_factory=list)


def _infer_entity_type(entity_id: str) -> str:
    if not isinstance(entity_id, str):
        return "unknown"
    source_prefixes = ("law-", "irr-", "source-", "handout-", "reviewer-", "law-section-")
    if any(entity_id.startswith(p) for p in source_prefixes):
        return "source"
    if entity_id.startswith("concept-"):
        return "concept"
    if entity_id.startswith("attribute-"):
        return "attribute"
    if entity_id.startswith("section-"):
        return "section"
    return "unknown"


def _load_registry_compat_table() -> dict[str, set[tuple[str, str]]]:
    import yaml
    from .paths import get_repo_root

    path = get_repo_root() / "scripts" / "vitruvius" / "rules" / "relationship_registry.yaml"
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError:
        return {}

    table: dict[str, set[tuple[str, str]]] = {}
    for predicate, spec in (data.get("predicates") or {}).items():
        pairs: set[tuple[str, str]] = set()
        for pair in spec.get("allowed_pairs", []) or []:
            s = pair.get("subject_type")
            o = pair.get("object_type")
            if s and o:
                pairs.add((s, o))
        table[predicate] = pairs
    return table


def _max_example_length(candidate: dict[str, Any]) -> int:
    examples = candidate.get("examples") or []
    if not examples:
        return 0
    return max(len(ex) for ex in examples)


def _joined_examples(candidate: dict[str, Any]) -> str:
    return " ".join(candidate.get("examples") or [])


def _has_negation(text: str) -> bool:
    return any(p.search(text) for p in NEGATION_PATTERNS)


def _has_predicate_keyword(text: str, predicate: str) -> bool:
    patterns = PREDICATE_KEYWORDS.get(predicate, [])
    return any(p.search(text) for p in patterns)


def _endpoint_phrase(entity_id: str) -> str:
    """Convert 'concept-occupancy-classification' -> 'occupancy classification'.

    Used by R7 to check whether the endpoint's canonical phrase appears in
    the evidence text. Returns empty string for IDs that don't have a clear
    phrase form (e.g., law-* IDs are too long and specific to be useful).
    """
    if not isinstance(entity_id, str):
        return ""
    for prefix in ("concept-", "attribute-"):
        if entity_id.startswith(prefix):
            return entity_id[len(prefix):].replace("-", " ").lower()
    return ""


def _has_conceptish_endpoints(from_id: str, to_id: str) -> bool:
    """R7 applies when at least one endpoint is a concept or attribute.

    Skipped for source-to-source (supersedes) or other IDs where the
    canonical phrase form is not meaningful for substring matching.
    """
    conceptish_prefixes = ("concept-", "attribute-")
    return (
        isinstance(from_id, str) and any(from_id.startswith(p) for p in conceptish_prefixes)
    ) or (
        isinstance(to_id, str) and any(to_id.startswith(p) for p in conceptish_prefixes)
    )


def triage_candidate(
    candidate: dict[str, Any],
    registry_compat: dict[str, set[tuple[str, str]]] | None = None,
) -> TriageResult:
    """Apply the deterministic triage rules in order; first match wins."""
    if registry_compat is None:
        registry_compat = _load_registry_compat_table()

    from_id = candidate.get("from", "")
    to_id = candidate.get("to", "")
    predicate = candidate.get("type", "")
    occurrences = int(candidate.get("occurrences", 0))
    evidence = _joined_examples(candidate)
    evidence_len = _max_example_length(candidate)
    from_type = _infer_entity_type(from_id)
    to_type = _infer_entity_type(to_id)
    type_pair = (from_type, to_type)

    # ---------- auto_reject rules ----------

    # R5: self-reference
    if from_id == to_id and from_id:
        return TriageResult(
            decision="auto_reject",
            confidence=1.0,
            reasons=["self_reference"],
        )

    # R1: registry incompatibility
    if registry_compat:
        allowed = registry_compat.get(predicate, set())
        if allowed and type_pair not in allowed:
            return TriageResult(
                decision="auto_reject",
                confidence=1.0,
                reasons=[f"registry_incompatible: ({from_type}, {to_type}) not valid for '{predicate}'"],
            )

    # R2: evidence too short
    if evidence_len < MIN_EVIDENCE_CHARS:
        return TriageResult(
            decision="auto_reject",
            confidence=0.95,
            reasons=[f"evidence_too_short: max example {evidence_len} chars < {MIN_EVIDENCE_CHARS}"],
        )

    # R3 (negation) was removed 2026-04-14: legal text frequently contains
    # "except" / "shall not" as conditional clauses embedded in otherwise-
    # valid evidence. A naive regex match on those produced false rejects
    # for high-signal candidates (e.g., concept-occupancy-separation ->
    # requires -> concept-occupancy-classification, which had matched
    # "except" inside a clause that modified a different sub-point). Until
    # we have a clause-boundary-aware detector, route negated evidence to
    # the LLM for judgment.

    # R7: endpoint-not-in-evidence — if none of the conceptish endpoint
    # phrases appear in the evidence text, the regex extractor matched
    # the section window but the evidence is topically unrelated. This
    # is the single most common false-positive pattern we see.
    #
    # Logic:
    #   - Collect all non-empty endpoint phrases (source IDs have no phrase,
    #     concepts/attributes do).
    #   - If at least one such phrase exists, require at least one to appear
    #     in the evidence text. Otherwise reject.
    #   - If no endpoint has a phrase (e.g., source-to-source supersedes),
    #     skip this rule entirely.
    if _has_conceptish_endpoints(from_id, to_id):
        evidence_lower = evidence.lower()
        phrases = [p for p in (_endpoint_phrase(from_id), _endpoint_phrase(to_id)) if p]
        if phrases and not any(phrase in evidence_lower for phrase in phrases):
            return TriageResult(
                decision="auto_reject",
                confidence=0.85,
                reasons=[
                    f"endpoint_not_in_evidence: none of {phrases} appear in the evidence text"
                ],
            )

    # ---------- auto_accept rules ----------

    # A1: strong governs pattern
    if (
        predicate == "governs"
        and from_type == "source"
        and to_type == "concept"
        and occurrences >= 3
        and _has_predicate_keyword(evidence, "governs")
    ):
        return TriageResult(
            decision="auto_accept",
            confidence=0.95,
            reasons=["structural_governs_pattern: source->concept, occ>=3, characteristic language"],
        )

    # A2: definitional anchor
    if (
        predicate == "defines"
        and from_type == "source"
        and to_type == "concept"
        and _has_predicate_keyword(evidence, "defines")
    ):
        return TriageResult(
            decision="auto_accept",
            confidence=0.95,
            reasons=["definitional_anchor: source->concept, explicit definition language"],
        )

    # A3: high recurrence + valid types + keyword match
    if (
        occurrences >= 5
        and registry_compat
        and type_pair in registry_compat.get(predicate, set())
        and _has_predicate_keyword(evidence, predicate)
    ):
        return TriageResult(
            decision="auto_accept",
            confidence=0.90,
            reasons=[f"high_recurrence_signal: occ={occurrences}, type-valid, keyword-match"],
        )

    # A4: concept->concept `requires` pattern with characteristic language
    # and at least 2 occurrences. Captures the most common deterministic
    # concept-to-concept relationship we see in practice (e.g.,
    # "occupancy separation shall comply with the classification rules").
    if (
        predicate == "requires"
        and from_type == "concept"
        and to_type == "concept"
        and occurrences >= 2
        and _has_predicate_keyword(evidence, "requires")
    ):
        return TriageResult(
            decision="auto_accept",
            confidence=0.90,
            reasons=["concept_requires_pattern: concept->concept, occ>=2, 'shall comply' language"],
        )

    # ---------- needs_review (fallthrough) ----------
    return TriageResult(
        decision="needs_review",
        confidence=0.5,
        reasons=["no_deterministic_rule_matched"],
    )


def triage_candidates(
    candidates: list[dict[str, Any]],
    registry_compat: dict[str, set[tuple[str, str]]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Batch triage. Returns three named buckets."""
    if registry_compat is None:
        registry_compat = _load_registry_compat_table()

    buckets: dict[str, list[dict[str, Any]]] = {
        "auto_accept": [],
        "auto_reject": [],
        "needs_review": [],
    }
    for cand in candidates:
        result = triage_candidate(cand, registry_compat=registry_compat)
        enriched = dict(cand)
        enriched["triage"] = {
            "decision": result.decision,
            "confidence": result.confidence,
            "reasons": result.reasons,
        }
        buckets[result.decision].append(enriched)

    return buckets
