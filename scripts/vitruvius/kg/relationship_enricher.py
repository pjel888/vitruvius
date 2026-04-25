"""Taxonomy-aware MVP relationship enrichment for existing KG snapshots.

This module deliberately works from already-derived artifacts: an existing
``KgV2Snapshot`` and, when provided, canonical source pages that already exist
in ``003_Canonical-Knowledge-Layer/shared/sources``. It does not rescan raw
sources, rebuild canonical sources, or flip taxonomy-v2 flags.

It adds reviewable semantic relationship assertions from existing rule evidence
and canonical source "Referenced Concepts" sections so the Explorer can show a
more useful concept-centric MVP graph while the governed backbone is still being
admitted.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .edge_materializer import EdgeMaterializer
from .enums import EdgeType, InferenceType, NodeType, ValidationState
from .json_evidence_store import KgV2Snapshot
from .schemas import CanonicalNode, CreatedBy, RelationshipAssertion


ENRICHMENT_STAGE = "mvp_taxonomy_relationship_enrichment"

STRUCTURAL_EDGE_TYPES = {
    EdgeType.BELONGS_TO,
    EdgeType.HAS_CHILD,
    EdgeType.DEFINED_BY,
    EdgeType.SUPPORTED_BY,
}

CONSTRAIN_CUES = (
    "shall not",
    "must not",
    "not exceed",
    "not occupy more than",
    "maximum",
    "minimum",
    "at least",
    "restricted",
    "limits established",
    "subject to",
    "prohibited",
    "limited to",
    "within the limits",
)

REQUIRE_CUES = (
    "shall have",
    "shall be provided",
    "shall provide",
    "required",
    "requires",
    "requirement",
    "requirements",
    "must have",
    "shall conform",
    "shall comply",
    "in accordance with",
    "pursuant to",
)

CALCULATION_CUES = (
    "determined by",
    "computed by",
    "calculated by",
    "dividing",
    "ratio",
    "factor",
    "per occupant",
)

REGULATORY_CUES = (
    "permit",
    "certificate",
    "approval",
    "zoning ordinance",
    "code",
    "regulation",
    "regulated",
    "governed by",
)

GENERIC_SINGLE_WORDS = {
    "area",
    "building",
    "buildings",
    "code",
    "construction",
    "development",
    "facility",
    "facilities",
    "government",
    "local",
    "ordinance",
    "permit",
    "permits",
    "project",
    "projects",
    "rule",
    "rules",
    "section",
    "source",
    "standard",
    "standards",
    "use",
    "uses",
    "water",
}

ALLOW_SINGLE_WORDS = {
    "stairs",
    "stair",
    "yards",
    "yard",
    "setbacks",
    "setback",
}


@dataclass(frozen=True)
class ConceptAlias:
    concept_id: str
    phrase: str
    source: str


@dataclass
class PairEvidence:
    from_node_id: str
    to_node_id: str
    edge_type: EdgeType
    confidence: float
    evidence_ids: list[str] = field(default_factory=list)
    rule_ids: list[str] = field(default_factory=list)
    matched_phrases: set[str] = field(default_factory=set)
    cue: str = ""
    reasoning_samples: list[str] = field(default_factory=list)

    def merge(
        self,
        *,
        confidence: float,
        evidence_ids: list[str],
        rule_id: str,
        phrase: str,
        cue: str,
        reasoning_sample: str,
    ) -> None:
        self.confidence = max(self.confidence, confidence)
        self.matched_phrases.add(phrase)
        if cue and not self.cue:
            self.cue = cue
        if rule_id not in self.rule_ids:
            self.rule_ids.append(rule_id)
        for evidence_id in evidence_ids:
            if evidence_id not in self.evidence_ids:
                self.evidence_ids.append(evidence_id)
        if reasoning_sample and reasoning_sample not in self.reasoning_samples:
            self.reasoning_samples.append(reasoning_sample)


@dataclass
class SourceReference:
    doc_version_id: str
    source_uri: str
    title: str
    concept_ids: list[str]
    trust_level: str = ""
    canonical_status: str = ""


@dataclass
class SourcePairEvidence:
    from_node_id: str
    to_node_id: str
    edge_type: EdgeType
    confidence: float
    document_version_ids: list[str] = field(default_factory=list)
    source_titles: list[str] = field(default_factory=list)
    reasoning_samples: list[str] = field(default_factory=list)

    def merge(
        self,
        *,
        confidence: float,
        document_version_id: str,
        source_title: str,
        reasoning_sample: str,
    ) -> None:
        self.confidence = max(self.confidence, confidence)
        if document_version_id not in self.document_version_ids:
            self.document_version_ids.append(document_version_id)
        if source_title and source_title not in self.source_titles:
            self.source_titles.append(source_title)
        if reasoning_sample and reasoning_sample not in self.reasoning_samples:
            self.reasoning_samples.append(reasoning_sample)


@dataclass(frozen=True)
class RelationshipEnrichmentReport:
    input_assertion_count: int
    output_assertion_count: int
    added_assertion_count: int
    skipped_existing_count: int
    candidate_pair_count: int
    source_pair_count: int
    semantic_assertion_count: int
    added_source_support_count: int
    added_by_type: dict[str, int]
    output_path: str | None = None


def enrich_snapshot(
    snapshot: KgV2Snapshot,
    *,
    max_new_assertions: int = 160,
    repo_root: Path | None = None,
    add_source_support: bool = True,
    created_at: str | None = None,
) -> RelationshipEnrichmentReport:
    """Add deterministic, evidence-backed semantic assertions in-place."""
    created_at = created_at or _utc_now()
    input_assertion_count = len(snapshot.relationship_assertions)
    existing_keys = {
        (a.from_node_id, a.edge_type.value, a.to_node_id)
        for a in snapshot.relationship_assertions
    }

    concepts = {
        node.id: node
        for node in snapshot.canonical_nodes
        if node.type == NodeType.CONCEPT
    }
    rules = {
        node.id: node
        for node in snapshot.canonical_nodes
        if node.type == NodeType.RULE
    }
    evidence_quotes = {
        span.id: span.quote or span.normalized_text
        for span in snapshot.evidence_spans
    }

    rule_to_primary = _rule_primary_concepts(snapshot)
    rule_to_evidence = _rule_evidence_ids(snapshot)
    aliases = _build_concept_aliases(concepts.values())

    candidates: dict[tuple[str, str, str], PairEvidence] = {}
    skipped_existing = 0

    for rule_id, primary_ids in rule_to_primary.items():
        rule = rules.get(rule_id)
        if not rule:
            continue
        evidence_ids = rule_to_evidence.get(rule_id, [])
        if not evidence_ids:
            continue

        text = _rule_text(rule, evidence_ids, evidence_quotes)
        if not text:
            continue
        normalized_text = _normalize_for_match(text)

        for primary_id in primary_ids:
            primary = concepts.get(primary_id)
            if not primary:
                continue
            for alias in aliases:
                if alias.concept_id == primary_id:
                    continue
                target = concepts.get(alias.concept_id)
                if not target:
                    continue
                match = _find_phrase(normalized_text, alias.phrase)
                if not match:
                    continue
                predicate, cue = _infer_predicate(
                    primary=primary,
                    target=target,
                    normalized_text=normalized_text,
                    phrase=alias.phrase,
                    match_start=match.start(),
                    match_end=match.end(),
                )
                from_node_id, to_node_id = _orient_relationship(
                    primary=primary,
                    target=target,
                    predicate=predicate,
                    cue=cue,
                )
                key = (from_node_id, predicate.value, to_node_id)
                if key in existing_keys:
                    skipped_existing += 1
                    continue

                confidence = _confidence(alias=alias, cue=cue, primary=primary, target=target)
                if confidence < 0.74:
                    continue

                sample = _context_sample(normalized_text, match.start(), match.end())
                pair = candidates.get(key)
                if pair is None:
                    pair = PairEvidence(
                        from_node_id=from_node_id,
                        to_node_id=to_node_id,
                        edge_type=predicate,
                        confidence=confidence,
                    )
                    candidates[key] = pair
                pair.merge(
                    confidence=confidence,
                    evidence_ids=evidence_ids,
                    rule_id=rule_id,
                    phrase=alias.phrase,
                    cue=cue,
                    reasoning_sample=sample,
                )

    source_references = _source_references(snapshot, concepts, repo_root)
    source_candidates = _source_pair_candidates(
        source_references=source_references,
        concepts=concepts,
        existing_keys=existing_keys | set(candidates),
    )

    ordered = sorted(
        candidates.values(),
        key=lambda pair: (
            -pair.confidence,
            pair.edge_type.value,
            pair.from_node_id,
            pair.to_node_id,
        ),
    )[:max_new_assertions]

    remaining = max(0, max_new_assertions - len(ordered))
    ordered_source_pairs = sorted(
        source_candidates.values(),
        key=lambda pair: (
            -pair.confidence,
            -len(pair.document_version_ids),
            pair.edge_type.value,
            pair.from_node_id,
            pair.to_node_id,
        ),
    )[:remaining]

    added: list[RelationshipAssertion] = []
    for pair in ordered:
        from_node = concepts.get(pair.from_node_id)
        to_node = concepts.get(pair.to_node_id)
        if not from_node or not to_node:
            continue
        added.append(
            RelationshipAssertion(
                id=_assertion_id(pair.from_node_id, pair.edge_type, pair.to_node_id),
                edge_type=pair.edge_type,
                from_node_id=pair.from_node_id,
                to_node_id=pair.to_node_id,
                reasoning_summary=_reasoning_summary(from_node, pair.edge_type, to_node, pair),
                reasoning_detail=_reasoning_detail(from_node, to_node, pair),
                inference_type=InferenceType.RULE_BASED_DERIVATION,
                confidence=round(pair.confidence, 3),
                validation_status=ValidationState.REVIEW_REQUIRED,
                created_by=CreatedBy(mode="deterministic", pipeline_stage=ENRICHMENT_STAGE),
                review_state="pending",
                evidence_ids=pair.evidence_ids[:12],
                created_at=created_at,
                updated_at=created_at,
            )
        )

    for pair in ordered_source_pairs:
        from_node = concepts.get(pair.from_node_id)
        to_node = concepts.get(pair.to_node_id)
        if not from_node or not to_node:
            continue
        added.append(
            RelationshipAssertion(
                id=_assertion_id(pair.from_node_id, pair.edge_type, pair.to_node_id),
                edge_type=pair.edge_type,
                from_node_id=pair.from_node_id,
                to_node_id=pair.to_node_id,
                reasoning_summary=_source_pair_reasoning_summary(from_node, pair.edge_type, to_node, pair),
                reasoning_detail=_source_pair_reasoning_detail(from_node, to_node, pair),
                inference_type=InferenceType.RULE_BASED_DERIVATION,
                confidence=round(pair.confidence, 3),
                validation_status=ValidationState.REVIEW_REQUIRED,
                created_by=CreatedBy(mode="deterministic", pipeline_stage=ENRICHMENT_STAGE),
                review_state="pending",
                document_version_ids=pair.document_version_ids[:16],
                created_at=created_at,
                updated_at=created_at,
            )
        )

    source_support = []
    if add_source_support:
        source_support = _source_support_assertions(
            source_references=source_references,
            concepts=concepts,
            existing_keys=existing_keys,
            created_at=created_at,
        )
        added.extend(source_support)

    snapshot.relationship_assertions.extend(added)
    snapshot.fast_edges = _rematerialize_fast_edges(snapshot)
    snapshot.metadata = {
        **snapshot.metadata,
        "relationship_enrichment": {
            "stage": ENRICHMENT_STAGE,
            "created_at": created_at,
            "added_assertion_count": len(added),
            "candidate_pair_count": len(candidates),
            "source_pair_count": len(source_candidates),
            "added_source_support_count": len(source_support),
            "max_new_assertions": max_new_assertions,
            "added_by_type": _count_by_type(added),
            "note": "MVP overlay generated from existing snapshot rule evidence and canonical source references; no raw/canonical rebuild.",
        },
    }
    snapshot.metadata["entity_counts"] = snapshot.entity_counts()

    semantic_assertion_count = sum(
        1
        for assertion in snapshot.relationship_assertions
        if assertion.edge_type not in STRUCTURAL_EDGE_TYPES
    )
    return RelationshipEnrichmentReport(
        input_assertion_count=input_assertion_count,
        output_assertion_count=len(snapshot.relationship_assertions),
        added_assertion_count=len(added),
        skipped_existing_count=skipped_existing,
        candidate_pair_count=len(candidates),
        source_pair_count=len(source_candidates),
        semantic_assertion_count=semantic_assertion_count,
        added_source_support_count=len(source_support),
        added_by_type=_count_by_type(added),
    )


def enrich_snapshot_file(
    snapshot_path: Path,
    *,
    out_path: Path,
    max_new_assertions: int = 160,
    repo_root: Path | None = None,
) -> RelationshipEnrichmentReport:
    """Read, enrich, and write a snapshot file."""
    snapshot = KgV2Snapshot.read(snapshot_path)
    report = enrich_snapshot(
        snapshot,
        max_new_assertions=max_new_assertions,
        repo_root=repo_root,
    )
    snapshot.write(out_path)
    return RelationshipEnrichmentReport(
        input_assertion_count=report.input_assertion_count,
        output_assertion_count=report.output_assertion_count,
        added_assertion_count=report.added_assertion_count,
        skipped_existing_count=report.skipped_existing_count,
        candidate_pair_count=report.candidate_pair_count,
        source_pair_count=report.source_pair_count,
        semantic_assertion_count=report.semantic_assertion_count,
        added_source_support_count=report.added_source_support_count,
        added_by_type=report.added_by_type,
        output_path=out_path.as_posix(),
    )


def _rule_primary_concepts(snapshot: KgV2Snapshot) -> dict[str, list[str]]:
    by_rule: dict[str, list[str]] = defaultdict(list)
    for assertion in snapshot.relationship_assertions:
        if assertion.edge_type != EdgeType.DEFINED_BY:
            continue
        if assertion.to_node_id.startswith("rule-") and assertion.from_node_id.startswith("concept-"):
            by_rule[assertion.to_node_id].append(assertion.from_node_id)
    return dict(by_rule)


def _rule_evidence_ids(snapshot: KgV2Snapshot) -> dict[str, list[str]]:
    by_rule: dict[str, list[str]] = defaultdict(list)
    for assertion in snapshot.relationship_assertions:
        if assertion.edge_type != EdgeType.SUPPORTED_BY:
            continue
        if not assertion.from_node_id.startswith("rule-"):
            continue
        ids = list(assertion.evidence_ids)
        if assertion.to_node_id.startswith("span-") and assertion.to_node_id not in ids:
            ids.append(assertion.to_node_id)
        for evidence_id in ids:
            if evidence_id not in by_rule[assertion.from_node_id]:
                by_rule[assertion.from_node_id].append(evidence_id)
    return dict(by_rule)


def _source_references(
    snapshot: KgV2Snapshot,
    concepts: dict[str, CanonicalNode],
    repo_root: Path | None,
) -> list[SourceReference]:
    if repo_root is None:
        return []

    references: list[SourceReference] = []
    for doc_version in snapshot.document_versions:
        source_path = _resolve_source_path(repo_root, doc_version.source_uri)
        if not source_path or not source_path.exists():
            continue
        try:
            text = source_path.read_text(encoding="utf-8")
        except OSError:
            continue
        frontmatter, body = _split_frontmatter(text)
        concept_ids = [
            concept_id
            for concept_id in _extract_referenced_concept_ids(body)
            if concept_id in concepts
        ]
        if not concept_ids:
            continue
        references.append(
            SourceReference(
                doc_version_id=doc_version.id,
                source_uri=doc_version.source_uri,
                title=str(frontmatter.get("title") or doc_version.title or source_path.stem),
                concept_ids=concept_ids,
                trust_level=str(frontmatter.get("trust_level") or ""),
                canonical_status=str(frontmatter.get("canonical_status") or ""),
            )
        )
    return references


def _resolve_source_path(repo_root: Path, source_uri: str) -> Path | None:
    path = Path(source_uri)
    if path.is_absolute():
        return path
    return repo_root / path


def _split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    frontmatter: dict[str, object] = {}
    try:
        import yaml

        payload = yaml.safe_load(text[3:end].strip())
        if isinstance(payload, dict):
            frontmatter = payload
    except Exception:
        frontmatter = {}
    return frontmatter, text[end + 4:]


def _extract_referenced_concept_ids(body: str) -> list[str]:
    section = _referenced_concepts_section(body)
    candidates = section if section else body
    seen: set[str] = set()
    ordered: list[str] = []
    for concept_id in re.findall(r"concept-[a-z0-9-]+", candidates):
        if concept_id in seen:
            continue
        seen.add(concept_id)
        ordered.append(concept_id)
    return ordered


def _referenced_concepts_section(body: str) -> str:
    match = re.search(r"(?im)^##\s+Referenced Concepts\s*$", body)
    if not match:
        return ""
    rest = body[match.end():]
    next_heading = re.search(r"(?im)^##\s+", rest)
    if next_heading:
        rest = rest[:next_heading.start()]
    return rest


def _source_pair_candidates(
    *,
    source_references: list[SourceReference],
    concepts: dict[str, CanonicalNode],
    existing_keys: set[tuple[str, str, str]],
) -> dict[tuple[str, str, str], SourcePairEvidence]:
    total_sources = max(len(source_references), 1)
    concept_source_counts: Counter[str] = Counter()
    pair_sources: dict[tuple[str, str], list[SourceReference]] = defaultdict(list)
    for reference in source_references:
        concept_ids = sorted(set(reference.concept_ids))
        if len(concept_ids) < 2:
            continue
        for concept_id in concept_ids:
            concept_source_counts[concept_id] += 1
        for index, left in enumerate(concept_ids):
            for right in concept_ids[index + 1:]:
                pair_sources[(left, right)].append(reference)

    candidates: dict[tuple[str, str, str], SourcePairEvidence] = {}
    for (left_id, right_id), references in pair_sources.items():
        left = concepts.get(left_id)
        right = concepts.get(right_id)
        if not left or not right:
            continue
        if len(references) < _minimum_source_support(left, right):
            continue

        pmi, jaccard = _pair_association_metrics(
            left_id=left_id,
            right_id=right_id,
            cooccurrence_count=len(references),
            total_sources=total_sources,
            concept_source_counts=concept_source_counts,
        )
        if pmi < _minimum_source_pmi(left, right):
            continue

        predicate, from_node_id, to_node_id = _source_reference_relationship(left, right)
        key = (from_node_id, predicate.value, to_node_id)
        if key in existing_keys:
            continue

        confidence = _source_pair_confidence(left, right, references, pmi=pmi, jaccard=jaccard)
        if confidence < 0.76:
            continue

        pair = candidates.get(key)
        if pair is None:
            pair = SourcePairEvidence(
                from_node_id=from_node_id,
                to_node_id=to_node_id,
                edge_type=predicate,
                confidence=confidence,
            )
            candidates[key] = pair

        for reference in references[:8]:
            pair.merge(
                confidence=confidence,
                document_version_id=reference.doc_version_id,
                source_title=reference.title,
                reasoning_sample=(
                    f"{reference.title} references both {left.label} and {right.label} "
                    f"(PMI {pmi:.2f}, Jaccard {jaccard:.2f})"
                ),
            )

    return candidates


def _pair_association_metrics(
    *,
    left_id: str,
    right_id: str,
    cooccurrence_count: int,
    total_sources: int,
    concept_source_counts: Counter[str],
) -> tuple[float, float]:
    left_count = max(concept_source_counts[left_id], 1)
    right_count = max(concept_source_counts[right_id], 1)
    pmi = math.log((cooccurrence_count * total_sources) / (left_count * right_count), 2)
    jaccard = cooccurrence_count / max(left_count + right_count - cooccurrence_count, 1)
    return pmi, jaccard


def _minimum_source_pmi(left: CanonicalNode, right: CanonicalNode) -> float:
    important = {
        "concept-standards-of-professional-practice",
        "concept-code-of-ethics",
        "concept-general-conditions-of-contract",
        "concept-arbitration",
        "concept-mediation",
        "concept-temporary-special-permit",
        "concept-architectural-interiors",
    }
    if left.id in important or right.id in important:
        return 1.0
    return 1.5


def _minimum_source_support(left: CanonicalNode, right: CanonicalNode) -> int:
    important = {
        "concept-standards-of-professional-practice",
        "concept-code-of-ethics",
        "concept-general-conditions-of-contract",
        "concept-arbitration",
        "concept-mediation",
    }
    if left.id in important or right.id in important:
        return 1
    if _taxonomy_root(left) == _taxonomy_root(right):
        return 2
    return 2


def _source_reference_relationship(
    left: CanonicalNode,
    right: CanonicalNode,
) -> tuple[EdgeType, str, str]:
    if _is_regulatory_concept(left) and not _is_regulatory_concept(right):
        return EdgeType.REGULATED_BY, right.id, left.id
    if _is_regulatory_concept(right) and not _is_regulatory_concept(left):
        return EdgeType.REGULATED_BY, left.id, right.id

    left_root = _taxonomy_root(left)
    right_root = _taxonomy_root(right)
    practice_contract_roots = {"taxonomy-project-practice", "taxonomy-construction-execution"}
    if {left_root, right_root}.issubset(practice_contract_roots) and left_root != right_root:
        return EdgeType.USED_IN, left.id, right.id

    if "taxonomy-fire-life-safety" in {left_root, right_root}:
        if left_root == "taxonomy-fire-life-safety":
            return EdgeType.CONSTRAINS, left.id, right.id
        return EdgeType.CONSTRAINS, right.id, left.id

    if "taxonomy-accessibility" in {left_root, right_root}:
        if left_root == "taxonomy-accessibility":
            return EdgeType.CONSTRAINS, left.id, right.id
        return EdgeType.CONSTRAINS, right.id, left.id

    if "taxonomy-site-infrastructure" in {left_root, right_root} and "taxonomy-spaces-occupancy" in {left_root, right_root}:
        if left_root == "taxonomy-site-infrastructure":
            return EdgeType.CONSTRAINS, left.id, right.id
        return EdgeType.CONSTRAINS, right.id, left.id

    if left_root != right_root:
        return EdgeType.AFFECTS, left.id, right.id

    return EdgeType.RELATED_TO, left.id, right.id


def _source_pair_confidence(
    left: CanonicalNode,
    right: CanonicalNode,
    references: list[SourceReference],
    *,
    pmi: float,
    jaccard: float,
) -> float:
    support_count = len({reference.doc_version_id for reference in references})
    confidence = 0.72
    confidence += min(0.08, support_count * 0.02)
    confidence += min(0.06, max(0.0, pmi - 1.0) * 0.025)
    confidence += min(0.04, jaccard * 0.08)
    if _taxonomy_root(left) != _taxonomy_root(right):
        confidence += 0.03
    if any(reference.trust_level in {"primary", "high"} for reference in references):
        confidence += 0.03
    if any(reference.canonical_status == "validated" for reference in references):
        confidence += 0.02
    return min(confidence, 0.88)


def _source_support_assertions(
    *,
    source_references: list[SourceReference],
    concepts: dict[str, CanonicalNode],
    existing_keys: set[tuple[str, str, str]],
    created_at: str,
) -> list[RelationshipAssertion]:
    assertions: list[RelationshipAssertion] = []
    for reference in source_references:
        for concept_id in reference.concept_ids:
            concept = concepts.get(concept_id)
            if not concept:
                continue
            key = (concept_id, EdgeType.SUPPORTED_BY.value, reference.doc_version_id)
            if key in existing_keys:
                continue
            assertions.append(
                RelationshipAssertion(
                    id=_assertion_id(concept_id, EdgeType.SUPPORTED_BY, reference.doc_version_id),
                    edge_type=EdgeType.SUPPORTED_BY,
                    from_node_id=concept_id,
                    to_node_id=reference.doc_version_id,
                    reasoning_summary=(
                        f"{reference.title} lists {concept.label} as a referenced concept; "
                        "added as reviewable document support for concept-centric navigation."
                    ),
                    reasoning_detail=[
                        f"stage={ENRICHMENT_STAGE}",
                        f"source_uri={reference.source_uri}",
                        f"document_version_id={reference.doc_version_id}",
                        f"trust_level={reference.trust_level}",
                        f"canonical_status={reference.canonical_status}",
                    ],
                    inference_type=InferenceType.DIRECT_CITATION,
                    confidence=_source_support_confidence(reference),
                    validation_status=ValidationState.REVIEW_REQUIRED,
                    created_by=CreatedBy(mode="deterministic", pipeline_stage=ENRICHMENT_STAGE),
                    review_state="pending",
                    document_version_ids=[reference.doc_version_id],
                    created_at=created_at,
                    updated_at=created_at,
                )
            )
    return assertions


def _source_support_confidence(reference: SourceReference) -> float:
    confidence = 0.72
    if reference.trust_level in {"primary", "high"}:
        confidence += 0.08
    if reference.canonical_status == "validated":
        confidence += 0.04
    return min(confidence, 0.86)


def _build_concept_aliases(concepts: Iterable[CanonicalNode]) -> list[ConceptAlias]:
    aliases: dict[tuple[str, str], ConceptAlias] = {}
    for concept in concepts:
        raw_phrases = [
            concept.label,
            concept.display_label or "",
            concept.slug,
            concept.id,
            *concept.aliases,
        ]
        for raw_phrase in raw_phrases:
            for phrase in _phrase_variants(raw_phrase):
                if not _is_usable_alias(phrase):
                    continue
                key = (concept.id, phrase)
                aliases[key] = ConceptAlias(
                    concept_id=concept.id,
                    phrase=phrase,
                    source="concept_alias",
                )
    return sorted(
        aliases.values(),
        key=lambda alias: (-len(alias.phrase), alias.concept_id, alias.phrase),
    )


def _phrase_variants(value: str) -> list[str]:
    normalized = _normalize_for_match(value)
    for prefix in ("concept ", "taxonomy ", "topic ", "subtopic "):
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
            break
    variants = {normalized}
    if normalized.endswith("ies"):
        variants.add(f"{normalized[:-3]}y")
    elif normalized.endswith("s") and len(normalized) > 5:
        variants.add(normalized[:-1])
    else:
        variants.add(f"{normalized}s")
    return sorted(v for v in variants if v)


def _is_usable_alias(phrase: str) -> bool:
    tokens = phrase.split()
    if not tokens:
        return False
    if len(tokens) == 1:
        token = tokens[0]
        return token in ALLOW_SINGLE_WORDS or (len(token) >= 6 and token not in GENERIC_SINGLE_WORDS)
    meaningful = [token for token in tokens if token not in GENERIC_SINGLE_WORDS]
    return len(meaningful) >= 1


def _rule_text(
    rule: CanonicalNode,
    evidence_ids: list[str],
    evidence_quotes: dict[str, str],
) -> str:
    parts = [rule.label, rule.display_label or "", rule.summary]
    for evidence_id in evidence_ids[:3]:
        quote = evidence_quotes.get(evidence_id, "")
        if quote:
            parts.append(quote)
    return " ".join(part for part in parts if part).strip()


def _normalize_for_match(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _find_phrase(normalized_text: str, phrase: str) -> re.Match[str] | None:
    return re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", normalized_text)


def _infer_predicate(
    *,
    primary: CanonicalNode,
    target: CanonicalNode,
    normalized_text: str,
    phrase: str,
    match_start: int,
    match_end: int,
) -> tuple[EdgeType, str]:
    window = _context_sample(normalized_text, match_start, match_end)
    primary_root = _taxonomy_root(primary)
    target_root = _taxonomy_root(target)

    cue = _first_cue(window, CALCULATION_CUES)
    if cue:
        return EdgeType.AFFECTS, cue

    cue = _first_cue(window, CONSTRAIN_CUES)
    if cue:
        if _is_regulatory_concept(target) and not _is_regulatory_concept(primary):
            return EdgeType.REGULATED_BY, cue
        return EdgeType.CONSTRAINS, cue

    cue = _first_cue(window, REQUIRE_CUES)
    if cue:
        if _is_regulatory_concept(target) and not _is_regulatory_concept(primary):
            return EdgeType.REGULATED_BY, cue
        return EdgeType.REQUIRES, cue

    cue = _first_cue(window, REGULATORY_CUES)
    if cue and _is_regulatory_concept(target) and not _is_regulatory_concept(primary):
        return EdgeType.REGULATED_BY, cue

    if primary_root != target_root:
        if primary_root in {"taxonomy-fire-life-safety", "taxonomy-accessibility"}:
            return EdgeType.CONSTRAINS, "cross-domain safety/accessibility placement"
        if primary_root == "taxonomy-site-infrastructure":
            return EdgeType.CONSTRAINS, "cross-domain land-use placement"
        if primary_root == "taxonomy-regulatory-permits":
            return EdgeType.REGULATED_BY, "cross-domain regulatory placement"
        return EdgeType.AFFECTS, "cross-domain taxonomy co-mention"

    return EdgeType.INFLUENCES, f"same-taxonomy co-mention: {phrase}"


def _orient_relationship(
    *,
    primary: CanonicalNode,
    target: CanonicalNode,
    predicate: EdgeType,
    cue: str,
) -> tuple[str, str]:
    if predicate == EdgeType.REGULATED_BY:
        if _is_regulatory_concept(primary) and not _is_regulatory_concept(target):
            return target.id, primary.id
        return primary.id, target.id
    return primary.id, target.id


def _first_cue(text: str, cues: tuple[str, ...]) -> str:
    for cue in cues:
        if cue in text:
            return cue
    return ""


def _context_sample(text: str, start: int, end: int, window: int = 96) -> str:
    left = max(0, start - window)
    right = min(len(text), end + window)
    return text[left:right].strip()


def _confidence(
    *,
    alias: ConceptAlias,
    cue: str,
    primary: CanonicalNode,
    target: CanonicalNode,
) -> float:
    confidence = 0.72
    if alias.phrase == _normalize_for_match(target.label):
        confidence += 0.08
    if cue:
        confidence += 0.08
    if _taxonomy_root(primary) != _taxonomy_root(target):
        confidence += 0.04
    if len(alias.phrase.split()) >= 2:
        confidence += 0.03
    return min(confidence, 0.93)


def _taxonomy_root(node: CanonicalNode) -> str:
    return node.taxonomy_path[0] if node.taxonomy_path else ""


def _is_regulatory_concept(node: CanonicalNode) -> bool:
    root = _taxonomy_root(node)
    normalized = _normalize_for_match(" ".join([node.id, node.label, node.slug]))
    return (
        root == "taxonomy-regulatory-permits"
        or "zoning ordinance" in normalized
        or "permit" in normalized
        or "certificate" in normalized
    )


def _assertion_id(from_node_id: str, edge_type: EdgeType, to_node_id: str) -> str:
    raw = f"assert-mvp-{from_node_id}-{edge_type.value.lower()}-{to_node_id}"
    return re.sub(r"[^a-z0-9-]+", "-", raw.lower()).strip("-")


def _reasoning_summary(
    from_node: CanonicalNode,
    edge_type: EdgeType,
    to_node: CanonicalNode,
    pair: PairEvidence,
) -> str:
    from_label = from_node.display_label or from_node.label
    to_label = to_node.display_label or to_node.label
    cue = f" using '{pair.cue}' language" if pair.cue else ""
    return (
        f"Existing 001-Laws rule evidence links {from_label} to {to_label}{cue}; "
        f"generated as a reviewable {edge_type.value} relationship for the MVP graph."
    )


def _reasoning_detail(
    from_node: CanonicalNode,
    to_node: CanonicalNode,
    pair: PairEvidence,
) -> list[str]:
    return [
        f"stage={ENRICHMENT_STAGE}",
        f"from_taxonomy_path={' > '.join(from_node.taxonomy_path)}",
        f"to_taxonomy_path={' > '.join(to_node.taxonomy_path)}",
        f"matched_phrases={', '.join(sorted(pair.matched_phrases))}",
        f"supporting_rules={', '.join(pair.rule_ids[:8])}",
        f"evidence_samples={' | '.join(pair.reasoning_samples[:3])}",
    ]


def _source_pair_reasoning_summary(
    from_node: CanonicalNode,
    edge_type: EdgeType,
    to_node: CanonicalNode,
    pair: SourcePairEvidence,
) -> str:
    from_label = from_node.display_label or from_node.label
    to_label = to_node.display_label or to_node.label
    support_count = len(pair.document_version_ids)
    source_label = "source" if support_count == 1 else "sources"
    return (
        f"{support_count} existing canonical {source_label} reference both "
        f"{from_label} and {to_label}; generated as a reviewable "
        f"{edge_type.value} relationship for concept-centric navigation."
    )


def _source_pair_reasoning_detail(
    from_node: CanonicalNode,
    to_node: CanonicalNode,
    pair: SourcePairEvidence,
) -> list[str]:
    return [
        f"stage={ENRICHMENT_STAGE}",
        "basis=canonical_source_referenced_concepts",
        f"from_taxonomy_path={' > '.join(from_node.taxonomy_path)}",
        f"to_taxonomy_path={' > '.join(to_node.taxonomy_path)}",
        f"document_versions={', '.join(pair.document_version_ids[:12])}",
        f"source_titles={' | '.join(pair.source_titles[:6])}",
        f"evidence_samples={' | '.join(pair.reasoning_samples[:3])}",
    ]


def _rematerialize_fast_edges(snapshot: KgV2Snapshot) -> list[dict[str, object]]:
    materializer = EdgeMaterializer(snapshot)
    materializer.materialize(snapshot.relationship_assertions, skip_unvalidated=False)
    materializer.materialize_placements(snapshot.placement_assertions, skip_unvalidated=False)
    return materializer.write_snapshot(out_path=None)["edges"]


def _count_by_type(assertions: list[RelationshipAssertion]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for assertion in assertions:
        edge_type = assertion.edge_type.value
        counts[edge_type] = counts.get(edge_type, 0) + 1
    return dict(sorted(counts.items()))


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
