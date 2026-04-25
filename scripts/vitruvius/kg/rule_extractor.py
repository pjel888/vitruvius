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

import hashlib
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


def _humanize_identifier(value: str) -> str:
    """Convert a canonical id or path segment into a short human label."""
    text = value.strip()
    for prefix in (
        "concept-", "taxonomy-", "topic-", "subtopic-",
        "term-", "definition-", "rule-", "procedure-",
        "exception-", "constraint-", "example-", "handout-",
        "law-", "irr-", "source-", "reviewer-",
        "section-", "sec-", "doc-", "docv-",
    ):
        if text.startswith(prefix):
            text = text[len(prefix):]
            break
    text = re.sub(r"[-_]+", " ", text).strip()
    return text.title() if text else "Untitled"


def _normalize_display_label(value: str) -> str:
    """Whitespace-normalize a display label without truncating it."""
    normalized = re.sub(r"\s+", " ", value).strip()
    return normalized


def _compact_rule_display_label(value: str, suffix: str = "", max_length: int = 56) -> str:
    """Keep Explorer-facing rule titles semantic and short."""
    text = re.sub(r"(?i)<br\s*/?>", " ", value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = _normalize_display_label(text)
    text = re.sub(r"\s+\[[^\]]+\]$", "", text).strip()
    text = re.split(r"\s+—\s+", text, maxsplit=1)[0].strip()
    suffix_text = f" · {suffix}" if suffix else ""
    head_length = max(16, max_length - len(suffix_text))
    if len(text) <= head_length:
        return f"{text}{suffix_text}"
    words: list[str] = []
    for word in text.split():
        candidate = " ".join([*words, word])
        if len(candidate) > head_length:
            break
        words.append(word)
    head = " ".join(words) if words else text[:head_length].strip()
    return f"{head}{suffix_text}"


def _rule_section_suffix(section_id: str) -> str:
    """Return a short discriminator for compact rule display titles."""
    section_name = _section_display_name(section_id)
    if not section_name:
        return ""
    section_match = re.search(r"\bSection\s+([A-Za-z0-9.-]+)", section_name, re.IGNORECASE)
    if section_match:
        return f"Sec. {section_match.group(1)}"
    article_match = re.search(r"\bArticle\s+([IVXLCDM0-9.-]+)", section_name, re.IGNORECASE)
    if article_match:
        return f"Art. {article_match.group(1)}"
    return section_name[:18].strip()


def _source_faithful_summary(value: str) -> str:
    """Normalize generated rule summaries without adding truncation markers."""
    text = re.sub(r"(?i)<br\s*/?>", " ", value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^\s*[>»]+\s*", "", text)
    return _normalize_display_label(text)


def _title_if_all_lower(value: str) -> str:
    """Title-case legacy lowercase labels while preserving mixed-case labels."""
    return value.title() if value and value == value.lower() else value


def _concept_display_name(concept_id: str, snapshot: KgV2Snapshot) -> str:
    """Return the compact display name for a concept id."""
    for node in snapshot.canonical_nodes:
        if node.id == concept_id:
            return _title_if_all_lower(_normalize_display_label(node.display_label or node.label or _humanize_identifier(concept_id)))
    return _humanize_identifier(concept_id)


def _section_display_name(section_id: str) -> str:
    """Return a readable section suffix for a rule display label."""
    if not section_id:
        return ""
    section_name = _humanize_identifier(section_id)
    if section_id.startswith(("section-", "sec-")) and not section_name.lower().startswith("section"):
        section_name = f"Section {section_name}"
    return _normalize_display_label(section_name)


def _source_reference(source_id: str) -> str:
    """Return a compact stable source reference from a canonical source id."""
    if source_id.startswith(("doc-", "docv-")):
        return ""
    match = re.search(r"(?:^|-)([0-9a-f]{6})$", source_id, re.IGNORECASE)
    if match:
        return match.group(1)
    source_slug = source_id
    for prefix in ("law-", "irr-", "source-", "handout-", "reviewer-"):
        if source_slug.startswith(prefix):
            source_slug = source_slug[len(prefix):]
            break
    tokens = [token for token in re.split(r"[-_]+", source_slug) if token]
    tail = "-".join(tokens[-3:]) if tokens else ""
    digest = hashlib.sha1(source_id.encode("utf-8")).hexdigest()[:6]
    return f"{tail}-{digest}" if tail else digest


def _title_if_all_caps(value: str) -> str:
    """Title-case all-caps source titles while preserving normal mixed case."""
    text = value.strip()
    return text.title() if len(text) > 10 and text == text.upper() else text


def _source_display_name(
    source_id: str,
    snapshot: KgV2Snapshot,
    primary_span: Any | None = None,
) -> str:
    """Return a semantic source label for rule titles."""
    source_title = ""
    span_docv_id = getattr(primary_span, "document_version_id", "") if primary_span else ""
    span_doc_id = getattr(primary_span, "document_id", "") if primary_span else ""

    for doc_version in snapshot.document_versions:
        if span_docv_id and doc_version.id == span_docv_id:
            source_title = doc_version.title
            break
        if span_doc_id and doc_version.document_id == span_doc_id:
            source_title = doc_version.title
            break

    if not source_title:
        source_title = _humanize_identifier(source_id)

    source_title = _title_if_all_caps(_title_if_all_lower(_normalize_display_label(source_title)))
    source_ref = _source_reference(source_id)
    if source_ref and source_ref.lower() not in source_title.lower():
        source_title = f"{source_title} [{source_ref}]"
    return source_title


def _rule_display_label(
    concept_id: str,
    snapshot: KgV2Snapshot,
    section_id: str = "",
    source_id: str = "",
    primary_span: Any | None = None,
) -> str:
    """Build a durable semantic title for rule nodes without losing full text."""
    concept_name = _concept_display_name(concept_id, snapshot)
    return _compact_rule_display_label(f"{concept_name} Rule", _rule_section_suffix(section_id))



def _rule_label_from_evidence(
    evidence_snippet: str,
    reviewer_reason: str = "",
    concept_id: str = "",
    source_id: str = "",
) -> str:
    """Derive a source-faithful rule label from evidence text."""
    text = evidence_snippet.strip()
    if not text or text == "Legacy promotion pipeline assertion":
        text = reviewer_reason or ""
    if not text or text == "Legacy promotion pipeline assertion":
        # Fallback: construct from concept + source names
        concept_name = concept_id.replace("concept-", "").replace("-", " ").title()
        source_name = source_id.replace("handout-", "").replace("-", " ").title()
        text = f"{concept_name} rule from {source_name}"
    text = _source_faithful_summary(text)
    # Remove markdown artifacts, list markers, leading numbering
    text = re.sub(r"^#+\s*", "", text)
    text = re.sub(r"^[-*•]\s+", "", text)
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"^[a-zA-Z]\.\s*", "", text)
    # Use the first sentence without truncating; rule display titles are built
    # from concept/section/source metadata, while labels keep source wording.
    first_sent = text.split(".")[0].strip()
    if len(first_sent) < 15:
        first_sent = text.strip()
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

        # Keep the source-faithful label separate from the compact display title.
        display_label = _rule_display_label(
            concept_id, self.snapshot, section_id, source_id, primary_span
        )
        label = _rule_label_from_evidence(
            evidence_snippet,
            assertion.reasoning_summary,
            concept_id,
            source_id,
        )
        summary = evidence_snippet or assertion.reasoning_summary
        summary = _source_faithful_summary(summary)

        # Inherit taxonomy path from target concept
        taxonomy_path = _concept_taxonomy_path(concept_id, self.snapshot)

        rule_node = CanonicalNode(
            id=rule_id,
            type=NodeType.RULE,
            label=label,
            display_label=display_label,
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
                f"Evidence: {_source_faithful_summary(evidence_snippet)}",
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

        supported_target_id = primary_evidence_id
        if not supported_target_id and primary_span is not None:
            supported_target_id = primary_span.document_version_id or primary_span.document_id
        if not supported_target_id:
            supported_target_id = source_id

        # rule SUPPORTED_BY evidence span/document endpoint
        supported_by = RelationshipAssertion(
            id=f"assert-{rule_id}-supported-by",
            edge_type=EdgeType.SUPPORTED_BY,
            from_node_id=rule_id,
            to_node_id=supported_target_id,
            reasoning_summary=f"Rule supported by evidence endpoint {supported_target_id}",
            reasoning_detail=[
                f"Original assertion: {assertion.id}",
                f"Section: {section_id or 'unspecified'}",
                f"Source: {source_id}",
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
