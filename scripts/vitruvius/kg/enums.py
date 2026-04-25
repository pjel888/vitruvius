"""Knowledge Graph transition — canonical enumerations.

These enums define the typed vocabulary for the taxonomy-centered,
evidence-backed canonical knowledge graph. They are used by Pydantic
schemas, Neo4j property constraints, and promotion validators.
"""

from __future__ import annotations

from enum import StrEnum


class NodeType(StrEnum):
    """Canonical node types for the knowledge graph."""

    TAXONOMY = "taxonomy"
    TOPIC = "topic"
    SUBTOPIC = "subtopic"
    CONCEPT = "concept"
    TERM = "term"
    DEFINITION = "definition"
    RULE = "rule"
    PROCEDURE = "procedure"
    EXCEPTION = "exception"
    CONSTRAINT = "constraint"
    EXAMPLE = "example"


class EdgeType(StrEnum):
    """Canonical edge types for materialized fast edges."""

    HAS_CHILD = "HAS_CHILD"
    BELONGS_TO = "BELONGS_TO"
    RELATED_TO = "RELATED_TO"
    DEFINED_BY = "DEFINED_BY"
    DEPENDS_ON = "DEPENDS_ON"
    APPLIES_TO = "APPLIES_TO"
    OVERRIDES = "OVERRIDES"
    CONTRADICTS = "CONTRADICTS"
    SAME_AS = "SAME_AS"
    PART_OF = "PART_OF"
    REQUIRES = "REQUIRES"
    SUPPORTED_BY = "SUPPORTED_BY"
    EXCLUDES = "EXCLUDES"
    CONSTRAINS = "CONSTRAINS"
    AFFECTS = "AFFECTS"
    INFLUENCES = "INFLUENCES"
    USED_IN = "USED_IN"
    EXECUTED_IN = "EXECUTED_IN"
    REGULATED_BY = "REGULATED_BY"


class InferenceType(StrEnum):
    """How an assertion was derived."""

    DIRECT_CITATION = "direct_citation"
    TAXONOMY_PLACEMENT = "taxonomy_placement"
    RULE_BASED_DERIVATION = "rule_based_derivation"
    SEMANTIC_SIMILARITY = "semantic_similarity"
    MULTI_HOP_INFERENCE = "multi_hop_inference"
    HUMAN_AUTHORED = "human_authored"


class ValidationState(StrEnum):
    """Lifecycle state for canonical nodes and assertions."""

    CANDIDATE = "candidate"
    VALIDATED = "validated"
    REVIEW_REQUIRED = "review_required"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
