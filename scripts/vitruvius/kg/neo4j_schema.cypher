// Vitruvius Knowledge Graph — Neo4j schema bootstrap
// Sprint KG Phase 0 (Readiness)
//
// Idempotent constraints and indexes for the v2-alpha evidence + canonical graph.
// Run from cypher-shell or the Neo4j Browser.
//
//   cat scripts/vitruvius/kg/neo4j_schema.cypher | cypher-shell -u neo4j -p <password>

// ---------------------------------------------------------------------------
// Constraints (unique node IDs)
// ---------------------------------------------------------------------------
CREATE CONSTRAINT canonical_node_id IF NOT EXISTS
    FOR (n:CanonicalNode) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT evidence_span_id IF NOT EXISTS
    FOR (e:EvidenceSpan) REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT document_version_id IF NOT EXISTS
    FOR (d:DocumentVersion) REQUIRE d.id IS UNIQUE;

CREATE CONSTRAINT section_id IF NOT EXISTS
    FOR (s:Section) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT chunk_id IF NOT EXISTS
    FOR (c:Chunk) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT taxonomy_id IF NOT EXISTS
    FOR (t:Taxonomy) REQUIRE t.id IS UNIQUE;

CREATE CONSTRAINT topic_id IF NOT EXISTS
    FOR (t:Topic) REQUIRE t.id IS UNIQUE;

CREATE CONSTRAINT subtopic_id IF NOT EXISTS
    FOR (t:Subtopic) REQUIRE t.id IS UNIQUE;

// ---------------------------------------------------------------------------
// Indexes (query performance)
// ---------------------------------------------------------------------------
CREATE INDEX canonical_node_type IF NOT EXISTS
    FOR (n:CanonicalNode) ON (n.type);

CREATE INDEX canonical_node_status IF NOT EXISTS
    FOR (n:CanonicalNode) ON (n.status);

CREATE INDEX canonical_node_label IF NOT EXISTS
    FOR (n:CanonicalNode) ON (n.label);

CREATE INDEX evidence_span_docv IF NOT EXISTS
    FOR (e:EvidenceSpan) ON (e.document_version_id);

CREATE INDEX evidence_span_doc_id IF NOT EXISTS
    FOR (e:EvidenceSpan) ON (e.document_id);

CREATE INDEX document_version_sha256 IF NOT EXISTS
    FOR (d:DocumentVersion) ON (d.sha256);

CREATE INDEX section_docv IF NOT EXISTS
    FOR (s:Section) ON (s.document_version_id);

CREATE INDEX taxonomy_label IF NOT EXISTS
    FOR (t:Taxonomy) ON (t.label);

CREATE INDEX topic_label IF NOT EXISTS
    FOR (t:Topic) ON (t.label);

CREATE INDEX subtopic_label IF NOT EXISTS
    FOR (t:Subtopic) ON (t.label);
