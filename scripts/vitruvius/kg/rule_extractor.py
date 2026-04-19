"""Atomic rule extractor — Phase 2 evidence-backed edge rewire.

Converts document-to-concept relationship assertions into atomic ``rule-*``
nodes and rewires edges so that documents become evidence leaves rather than
primary nodes.

Before (legacy):
    source_document ──APPLIES_TO──► concept

After (Phase 2):
    concept ──DEFINED_BY──► rule-*
    rule-* ──SUPPORTED_BY──► source_document

Rules are generated deterministically at snapshot-build time from the
EvidenceSpan records already materialized by the EvidenceMaterializer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .enums import EdgeType, InferenceType, NodeType, ValidationState
from .json_evidence_store import KgV2Snapshot
from .schemas import CanonicalNode, CreatedBy, RelationshipAssertion


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_source_node(node_id: str, snapshot: KgV2Snapshot) -> bool:
    """Return True if *node_id* refers to a source document, not a concept."""
    # Explicit document-version ids
    if node_id.startswith("docv-") or node_id.startswith("doc-"):
        return True
    # Check against document_versions in snapshot
    for dv in snapshot.document_versions:
        if node_id in (dv.id, dv.document_id):
            return True
    # Heuristic: canonical nodes (concepts, taxonomy, topics, subtopics) have
    # structured prefixes.  Anything else is treated as a source.
    canonical_prefixes = (
        "concept-", "taxonomy-", "topic-", "subtopic-",
        "term-", "definition-", "rule-", "procedure-",
        "exception-", "constraint-", "example-",
    )
    return not node_id.startswith(canonical_prefixes)


def _concept_taxonomy_path(concept_id: str, snapshot: KgV2Snapshot) -> list[str]:
    """Look up the taxonomy_path of a concept node in the snapshot."""
    for node in snapshot.canonical_nodes:
        if node.id == concept_id and node.type.value == "concept":
            return list(node.taxonomy_path)
    return []



def _rule_label_from_evidence(
    evidence_snippet: str,
    reviewer_reason: str = "",
    concept_id: str = "",
    source_id: str = "",
) -> str:
    """Derive a concise rule label from evidence text."""
    text = evidence_snippet.strip()
    if not text or text == "Legacy promotion pipeline assertion":
        text = reviewer_reason or ""
    if not text or text == "Legacy promotion pipeline assertion":
        # Fallback: construct from concept + source names
        concept_name = concept_id.replace("concept-", "").replace("-", " ").title()
        source_name = source_id.replace("handout-", "").replace("-", " ").title()
        text = f"{concept_name} rule from {source_name}"
    text = text.strip()
    # Remove markdown artifacts, list markers, leading numbering
    text = re.sub(r"^#+\s*", "", text)
    text = re.sub(r"^[-*•]\s+", "", text)
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"^[a-zA-Z]\.\s*", "", text)
    # Use first sentence, capped at 120 chars
    first_sent = text.split(".")[0].strip()
    if len(first_sent) > 120:
        first_sent = first_sent[:117] + "..."
    if len(first_sent) < 15:
        # Too short — use more text up to 120 chars
        first_sent = text[:120].strip()
    return first_sent if first_sent else "Untitled rule"


def _make_rule_id(source_id: str, section_id: str, index: int) -> str:
    """Generate a deterministic rule canonical id."""
    section_part = section_id if section_id else "general"
    # Sanitize: keep alnum and hyphens
    section_part = "".join(c if c.isalnum() or c == "-" else "-" for c in section_part)
    source_part = "".join(c if c.isalnum() or c == "-" else "-" for c in source_id)
    return f"rule-{source_part}-{section_part}-{index:03d}"


# ---------------------------------------------------------------------------
# Rule extractor
# ---------------------------------------------------------------------------

@dataclass
class ExtractionResult:
    """Output of a single rule extraction."""

    rule_node: CanonicalNode
    defined_by: RelationshipAssertion
    supported_by: RelationshipAssertion
    original_assertion_id: str


class RuleExtractor:
    """Extract atomic rules from document-to-concept assertions and rewire edges."""

    def __init__(self, snapshot: KgV2Snapshot | None = None) -> None:
        self.snapshot = snapshot or KgV2Snapshot()
        self._warnings: list[str] = []
        self._rule_counter: dict[str, int] = {}

    # -- public API ------------------------------------------------------------

    def extract_all(self) -> KgV2Snapshot:
        """Run extraction over the snapshot and return the mutated snapshot."""
        if not self.snapshot.relationship_assertions:
            return self.snapshot

        new_assertions: list[RelationshipAssertion] = []
        removed_ids: set[str] = set()

        for assertion in self.snapshot.relationship_assertions:
            if not _is_source_node(assertion.from_node_id, self.snapshot):
                # Concept-to-concept: keep as-is
                new_assertions.append(assertion)
                continue

            result = self._extract_one(assertion)
            if result is None:
                # Fallback: keep original if extraction fails
                new_assertions.append(assertion)
                continue

            removed_ids.add(assertion.id)
            self.snapshot.canonical_nodes.append(result.rule_node)
            new_assertions.append(result.defined_by)
            new_assertions.append(result.supported_by)

        self.snapshot.relationship_assertions = new_assertions
        return self.snapshot

    # -- internal --------------------------------------------------------------

    def _extract_one(self, assertion: RelationshipAssertion) -> ExtractionResult | None:
        """Convert a single document→concept assertion into a rule node + two assertions."""
        source_id = assertion.from_node_id
        concept_id = assertion.to_node_id

        # Pick primary evidence (first evidence span id)
        primary_evidence_id = assertion.evidence_ids[0] if assertion.evidence_ids else ""
        primary_span = None
        for span in self.snapshot.evidence_spans:
            if span.id == primary_evidence_id:
                primary_span = span
                break

        evidence_snippet = primary_span.quote if primary_span else assertion.reasoning_summary
        section_id = ""
        if primary_span and primary_span.selector and hasattr(primary_span.selector, "heading_path"):
            hp = primary_span.selector.heading_path
            if hp:
                section_id = hp[-1]

        # Deterministic rule id
        counter_key = f"{source_id}:{section_id}"
        idx = self._rule_counter.get(counter_key, 0)
        self._rule_counter[counter_key] = idx + 1
        rule_id = _make_rule_id(source_id, section_id, idx)

        # Derive label and summary
        label = _rule_label_from_evidence(
            evidence_snippet, assertion.reasoning_summary, concept_id, source_id
        )
        summary = evidence_snippet[:500] if evidence_snippet else assertion.reasoning_summary

        # Inherit taxonomy path from target concept
        taxonomy_path = _concept_taxonomy_path(concept_id, self.snapshot)

        rule_node = CanonicalNode(
            id=rule_id,
            type=NodeType.RULE,
            label=label,
            slug=rule_id.replace("rule-", ""),
            summary=summary,
            taxonomy_path=taxonomy_path,
            aliases=[],
            status=assertion.validation_status,
            confidence=assertion.confidence,
            version=1,
            created_at=assertion.created_at,
            updated_at=assertion.updated_at,
            primary_assertion_id=f"assert-{rule_id}-defined-by",
        )

        # concept DEFINED_BY rule
        defined_by = RelationshipAssertion(
            id=f"assert-{rule_id}-defined-by",
            edge_type=EdgeType.DEFINED_BY,
            from_node_id=concept_id,
            to_node_id=rule_id,
            reasoning_summary=f"Concept defined by atomic rule extracted from {source_id}",
            reasoning_detail=[
                f"Original assertion: {assertion.id}",
                f"Source: {source_id}",
                f"Evidence: {evidence_snippet[:200]}..." if len(evidence_snippet) > 200 else f"Evidence: {evidence_snippet}",
            ],
            inference_type=InferenceType.DIRECT_CITATION,
            confidence=assertion.confidence,
            validation_status=assertion.validation_status,
            created_by=assertion.created_by,
            review_state=assertion.review_state,
            evidence_ids=list(assertion.evidence_ids),
            document_version_ids=list(assertion.document_version_ids),
            created_at=assertion.created_at,
            updated_at=assertion.updated_at,
            version=1,
        )

        # rule SUPPORTED_BY source
        supported_by = RelationshipAssertion(
            id=f"assert-{rule_id}-supported-by",
            edge_type=EdgeType.SUPPORTED_BY,
            from_node_id=rule_id,
            to_node_id=source_id,
            reasoning_summary=f"Rule supported by source document {source_id}",
            reasoning_detail=[
                f"Original assertion: {assertion.id}",
                f"Section: {section_id or 'unspecified'}",
            ],
            inference_type=InferenceType.DIRECT_CITATION,
            confidence=assertion.confidence,
            validation_status=assertion.validation_status,
            created_by=assertion.created_by,
            review_state=assertion.review_state,
            evidence_ids=list(assertion.evidence_ids),
            document_version_ids=list(assertion.document_version_ids),
            created_at=assertion.created_at,
            updated_at=assertion.updated_at,
            version=1,
        )

        return ExtractionResult(
            rule_node=rule_node,
            defined_by=defined_by,
            supported_by=supported_by,
            original_assertion_id=assertion.id,
        )
