"""
Cross-Discipline Edge Validator

Validates that the knowledge graph conforms to the cross-discipline
relationship taxonomy defined in:
    .ai/06_specs/vitruvian-context/01_CROSS_DISCIPLINE_RELATIONSHIP_TAXONOMY.md

Run with: pytest scripts/tests/test_cross_discipline_validator.py -v
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Allowed predicates (closed vocabulary)
# ---------------------------------------------------------------------------

ALLOWED_CROSS_DISCIPLINE_PREDICATES = {
    "BELONGS_TO_DOMAIN",
    "USED_IN",
    "CONSTRAINS",
    "REQUIRES",
    "AFFECTS",
    "INFLUENCES",
    "EXECUTED_IN",
    "REGULATED_BY",
    "SUPPORTED_BY",
    "PRODUCES",
    "CONSUMES",
    "MAPS_TO_STANDARD",
    "EQUIVALENT_TO",
    "APPLIES_IN",
    "HAS_OVERLAY",
    "BASED_ON",
    "WITHIN_JURISDICTION",
    "GOVERNS",
    "DEFINED_BY",
    "SUPERSEDES",
    "SUPERSEDED_BY",
    "HAS_EDITION",
}


# ---------------------------------------------------------------------------
# Allowed domain pairs for cross-discipline influence edges
# ---------------------------------------------------------------------------

ALLOWED_DOMAIN_PAIRS: dict[str, set[str]] = {
    "taxonomy-structural": {
        "taxonomy-architecture",
        "taxonomy-construction",
        "taxonomy-mep",
    },
    "taxonomy-architecture": {
        "taxonomy-structural",
        "taxonomy-mep",
        "taxonomy-regulatory",
    },
    "taxonomy-mep": {
        "taxonomy-architecture",
        "taxonomy-structural",
    },
    "taxonomy-construction": {
        "taxonomy-architecture",
        "taxonomy-structural",
    },
    "taxonomy-regulatory": {
        "taxonomy-architecture",
        "taxonomy-structural",
        "taxonomy-mep",
    },
    "taxonomy-sustainability": {
        "taxonomy-architecture",
        "taxonomy-mep",
    },
    "taxonomy-fire-life-safety": {
        "taxonomy-architecture",
        "taxonomy-structural",
        "taxonomy-mep",
    },
    "taxonomy-accessibility": {
        "taxonomy-architecture",
        "taxonomy-structural",
    },
}


# ---------------------------------------------------------------------------
# Confidence thresholds
# ---------------------------------------------------------------------------

CONFIDENCE_THRESHOLDS = {
    "CONSTRAINS": 0.90,
    "REQUIRES": 0.90,
    "AFFECTS": 0.75,
    "INFLUENCES": 0.70,
    "USED_IN": 0.75,
    "EXECUTED_IN": 0.80,
    "REGULATED_BY": 0.95,
    "MAPS_TO_STANDARD": 0.70,
}


# ---------------------------------------------------------------------------
# Validation result
# ---------------------------------------------------------------------------

@dataclass
class ValidationViolation:
    rule: str
    concept_id: str
    detail: str
    severity: str  # "error" | "warning"


@dataclass
class ValidationResult:
    passed: bool
    violations: list[ValidationViolation] = field(default_factory=list)

    def add(self, rule: str, concept_id: str, detail: str, severity: str = "error") -> None:
        self.violations.append(ValidationViolation(rule, concept_id, detail, severity))
        if severity == "error":
            self.passed = False


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def validate_primary_domain_presence(
    concepts: list[dict[str, Any]],
    result: ValidationResult,
) -> None:
    """
    Rule: Every concept MUST have a primary_domain facet value.
    """
    for concept in concepts:
        cid = concept.get("canonical_id", concept.get("id", "unknown"))
        primary_domain = concept.get("primary_domain")
        if not primary_domain:
            result.add("PRIMARY_DOMAIN_MISSING", cid, "No primary_domain facet value found")


def validate_no_vague_cross_discipline_edges(
    edges: list[dict[str, Any]],
    result: ValidationResult,
) -> None:
    """
    Rule: No RELATED_TO, CONNECTED_TO, or SIMILAR_TO edges between different domains.
    """
    forbidden = {"RELATED_TO", "CONNECTED_TO", "SIMILAR_TO"}
    for edge in edges:
        etype = edge.get("type", "")
        if etype in forbidden:
            from_domain = edge.get("from_domain", "unknown")
            to_domain = edge.get("to_domain", "unknown")
            if from_domain != to_domain:
                result.add(
                    "VAGUE_CROSS_DISCIPLINE_EDGE",
                    edge.get("from", "unknown"),
                    f"Forbidden edge type '{etype}' from {from_domain} to {to_domain}",
                )


def validate_allowed_predicates(
    edges: list[dict[str, Any]],
    result: ValidationResult,
) -> None:
    """
    Rule: All edges MUST use predicates from the closed vocabulary.
    """
    for edge in edges:
        etype = edge.get("type", "")
        if etype not in ALLOWED_CROSS_DISCIPLINE_PREDICATES:
            result.add(
                "UNKNOWN_PREDICATE",
                edge.get("from", "unknown"),
                f"Edge type '{etype}' is not in the allowed predicate registry",
            )


def validate_domain_pair_constraints(
    edges: list[dict[str, Any]],
    result: ValidationResult,
) -> None:
    """
    Rule: Cross-discipline influence edges MUST connect allowed domain pairs.
    """
    influence_types = {"USED_IN", "CONSTRAINS", "REQUIRES", "AFFECTS", "INFLUENCES", "EXECUTED_IN", "REGULATED_BY"}

    for edge in edges:
        etype = edge.get("type", "")
        if etype not in influence_types:
            continue

        from_domain = edge.get("from_domain", "")
        to_domain = edge.get("to_domain", "")

        if from_domain == to_domain:
            # Intra-domain edges are not constrained by this rule
            continue

        allowed_targets = ALLOWED_DOMAIN_PAIRS.get(from_domain, set())
        if to_domain not in allowed_targets:
            result.add(
                "DISALLOWED_DOMAIN_PAIR",
                edge.get("from", "unknown"),
                f"Edge '{etype}' from '{from_domain}' to '{to_domain}' is not in the allowed matrix",
                severity="warning",  # Warn rather than error for migration phase
            )


def validate_confidence_thresholds(
    edges: list[dict[str, Any]],
    result: ValidationResult,
) -> None:
    """
    Rule: Cross-discipline edges MUST meet minimum confidence thresholds.
    """
    for edge in edges:
        etype = edge.get("type", "")
        threshold = CONFIDENCE_THRESHOLDS.get(etype)
        if threshold is None:
            continue

        confidence = edge.get("confidence", 0.0)
        if confidence < threshold:
            result.add(
                "CONFIDENCE_TOO_LOW",
                edge.get("from", "unknown"),
                f"Edge '{etype}' confidence {confidence} < threshold {threshold}",
                severity="warning",
            )


def validate_no_cycles(
    concepts: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    result: ValidationResult,
) -> None:
    """
    Rule: REQUIRES + DEPENDS_ON + CONSTRAINS edges must be acyclic per domain.
    """
    cycle_types = {"REQUIRES", "DEPENDS_ON", "CONSTRAINS"}

    # Group concepts by domain
    concept_domains = {}
    for concept in concepts:
        cid = concept.get("canonical_id", concept.get("id"))
        concept_domains[cid] = concept.get("primary_domain", "unknown")

    # Build adjacency list per domain
    domain_graphs: dict[str, dict[str, list[str]]] = {}
    for edge in edges:
        etype = edge.get("type", "")
        if etype not in cycle_types:
            continue

        from_id = edge.get("from")
        to_id = edge.get("to")
        domain = concept_domains.get(from_id, "unknown")

        if domain not in domain_graphs:
            domain_graphs[domain] = {}
        if from_id not in domain_graphs[domain]:
            domain_graphs[domain][from_id] = []
        domain_graphs[domain][from_id].append(to_id)

    # Detect cycles per domain using DFS
    for domain, graph in domain_graphs.items():
        visited = set()
        rec_stack = set()

        def _has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if _has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if _has_cycle(node):
                    result.add(
                        "CYCLE_DETECTED",
                        node,
                        f"Cycle detected in {cycle_types} edges within domain '{domain}'",
                    )
                    break


# ---------------------------------------------------------------------------
# Main entrypoint
# ---------------------------------------------------------------------------

def validate_cross_discipline_graph(
    concepts: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> ValidationResult:
    """
    Run all cross-discipline validators against a graph.

    Args:
        concepts: List of concept nodes with at least canonical_id and primary_domain.
        edges: List of edge dicts with keys: from, to, type, from_domain, to_domain, confidence.

    Returns:
        ValidationResult with passed=False if any error-level violation exists.
    """
    result = ValidationResult(passed=True)

    validate_primary_domain_presence(concepts, result)
    validate_no_vague_cross_discipline_edges(edges, result)
    validate_allowed_predicates(edges, result)
    validate_domain_pair_constraints(edges, result)
    validate_confidence_thresholds(edges, result)
    validate_no_cycles(concepts, edges, result)

    return result
