// Vitruvius Knowledge Graph — Neo4j Schema v2 (Taxonomy Governance)
//
// Idempotent constraints, indexes, and full-text search for:
// - Backbone nodes (L1–L4 domain hierarchy)
// - Canonical nodes with facet properties
// - Jurisdiction hierarchy
// - Authority document family / edition
// - Overlays and applicability rules
// - Standard references and mappings
// - Cross-discipline influence edges
//
// Run from cypher-shell or the Neo4j Browser:
//   cat scripts/vitruvius/kg/neo4j_schema_v2.cypher | cypher-shell -u neo4j -p <password>
//
// Authority: .ai/06_specs/vitruvian-context/04_schema_contract.md

// ---------------------------------------------------------------------------
// New labels: constraints (unique IDs)
// ---------------------------------------------------------------------------

CREATE CONSTRAINT backbone_node_id IF NOT EXISTS
    FOR (n:BackboneNode) REQUIRE n.canonical_id IS UNIQUE;

CREATE CONSTRAINT jurisdiction_code IF NOT EXISTS
    FOR (j:Jurisdiction) REQUIRE j.code IS UNIQUE;

CREATE CONSTRAINT authority_id IF NOT EXISTS
    FOR (a:Authority) REQUIRE a.canonical_id IS UNIQUE;

CREATE CONSTRAINT authority_document_family_id IF NOT EXISTS
    FOR (f:AuthorityDocumentFamily) REQUIRE f.canonical_id IS UNIQUE;

CREATE CONSTRAINT authority_document_edition_id IF NOT EXISTS
    FOR (e:AuthorityDocumentEdition) REQUIRE e.canonical_id IS UNIQUE;

CREATE CONSTRAINT applicability_rule_id IF NOT EXISTS
    FOR (r:ApplicabilityRule) REQUIRE r.canonical_id IS UNIQUE;

CREATE CONSTRAINT overlay_id IF NOT EXISTS
    FOR (o:Overlay) REQUIRE o.canonical_id IS UNIQUE;

CREATE CONSTRAINT standard_reference_id IF NOT EXISTS
    FOR (s:StandardReference) REQUIRE s.canonical_id IS UNIQUE;

// ---------------------------------------------------------------------------
// Extended CanonicalNode: add canonical_id uniqueness (separate from legacy id)
// ---------------------------------------------------------------------------

CREATE CONSTRAINT canonical_node_canonical_id IF NOT EXISTS
    FOR (n:CanonicalNode) REQUIRE n.canonical_id IS UNIQUE;

// ---------------------------------------------------------------------------
// Indexes: query performance
// ---------------------------------------------------------------------------

// Backbone
CREATE INDEX backbone_path_code IF NOT EXISTS
    FOR (n:BackboneNode) ON (n.path_code);

CREATE INDEX backbone_level IF NOT EXISTS
    FOR (n:BackboneNode) ON (n.level);

CREATE INDEX backbone_parent IF NOT EXISTS
    FOR (n:BackboneNode) ON (n.parent_path_code);

// Facet filtering on CanonicalNode
CREATE INDEX canonical_node_primary_domain IF NOT EXISTS
    FOR (n:CanonicalNode) ON (n.primary_domain);

CREATE INDEX canonical_node_knowledge_type IF NOT EXISTS
    FOR (n:CanonicalNode) ON (n.knowledge_type);

CREATE INDEX canonical_node_asset_scope IF NOT EXISTS
    FOR (n:CanonicalNode) ON (n.asset_scope);

CREATE INDEX canonical_node_lifecycle_stage IF NOT EXISTS
    FOR (n:CanonicalNode) ON (n.lifecycle_stage);

CREATE INDEX canonical_node_project_type IF NOT EXISTS
    FOR (n:CanonicalNode) ON (n.project_type);

CREATE INDEX canonical_node_performance_topic IF NOT EXISTS
    FOR (n:CanonicalNode) ON (n.performance_topic);

// Jurisdiction
CREATE INDEX jurisdiction_precedence IF NOT EXISTS
    FOR (j:Jurisdiction) ON (j.precedence_rank);

CREATE INDEX jurisdiction_parent IF NOT EXISTS
    FOR (j:Jurisdiction) ON (j.parent_code);

// Authority document edition
CREATE INDEX edition_family IF NOT EXISTS
    FOR (e:AuthorityDocumentEdition) ON (e.family_id);

CREATE INDEX edition_effective_date IF NOT EXISTS
    FOR (e:AuthorityDocumentEdition) ON (e.effective_date);

CREATE INDEX edition_status IF NOT EXISTS
    FOR (e:AuthorityDocumentEdition) ON (e.status);

// Overlay
CREATE INDEX overlay_concept IF NOT EXISTS
    FOR (o:Overlay) ON (o.concept_id);

CREATE INDEX overlay_jurisdiction IF NOT EXISTS
    FOR (o:Overlay) ON (o.jurisdiction_code);

CREATE INDEX overlay_effective_date IF NOT EXISTS
    FOR (o:Overlay) ON (o.effective_date);

// Standard reference
CREATE INDEX standard_system_code IF NOT EXISTS
    FOR (s:StandardReference) ON (s.system, s.code);

// Standard mapping
CREATE INDEX mapping_concept IF NOT EXISTS
    FOR (m:StandardMapping) ON (m.canonical_id);

// ---------------------------------------------------------------------------
// Full-text search index
// ---------------------------------------------------------------------------

CREATE FULLTEXT INDEX canonicalSearch IF NOT EXISTS
    FOR (n:CanonicalNode)
    ON EACH [n.label, n.aliases, n.summary, n.path_code];

// ---------------------------------------------------------------------------
// Edge type assertions (Neo4j 5.26+ — optional, improves query planning)
// ---------------------------------------------------------------------------

// Note: Neo4j Community does not support relationship constraints.
// These are documented as schema conventions for query authors.

// BELONGS_TO_DOMAIN: CanonicalNode -> BackboneNode
// HAS_PARENT: BackboneNode -> BackboneNode
// WITHIN_JURISDICTION: Jurisdiction -> Jurisdiction
// HAS_EDITION: AuthorityDocumentFamily -> AuthorityDocumentEdition
// SUPERSEDES: AuthorityDocumentEdition -> AuthorityDocumentEdition
// APPLIES_IN: ApplicabilityRule -> Jurisdiction
// GOVERNS: ApplicabilityRule -> AuthorityDocumentEdition
// HAS_OVERLAY: CanonicalNode -> Overlay
// BASED_ON: Overlay -> AuthorityDocumentEdition
// APPLIES_IN: Overlay -> Jurisdiction
// SUPPORTED_BY: CanonicalNode -> EvidenceSpan
// MAPS_TO_STANDARD: CanonicalNode -> StandardReference
// CONSTRAINS, AFFECTS, REQUIRES, INFLUENCES, USED_IN, EXECUTED_IN, REGULATED_BY
//   : CanonicalNode -> CanonicalNode or CanonicalNode -> BackboneNode
