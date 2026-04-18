-- Vitruvius Knowledge Graph — PostgreSQL registry schema
-- Sprint KG Phase 0 (Readiness)
--
-- This schema powers the operational registry for:
--   - file inventory
--   - document versioning
--   - ingestion / extraction / review job tracking
--   - audit events
--   - canonical merge log
--   - review queue
--
-- Run with: psql -d vitruvius -f scripts/vitruvius/db/schema.sql

BEGIN;

-- ---------------------------------------------------------------------------
-- File registry (Layer 1 raw source tracking)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS file_registry (
    id            TEXT PRIMARY KEY,
    relative_path TEXT NOT NULL,
    name          TEXT NOT NULL,
    extension     TEXT NOT NULL,
    size_bytes    BIGINT NOT NULL,
    modified_utc  TIMESTAMPTZ NOT NULL,
    sha256        TEXT NOT NULL,
    parent_folder TEXT NOT NULL,
    top_category  TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_file_registry_sha256 ON file_registry(sha256);
CREATE INDEX IF NOT EXISTS idx_file_registry_parent ON file_registry(parent_folder);

-- ---------------------------------------------------------------------------
-- Document versions (immutable evidence anchor)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS document_version (
    id            TEXT PRIMARY KEY,
    document_id   TEXT NOT NULL,
    title         TEXT NOT NULL,
    source_uri    TEXT NOT NULL,
    mime_type     TEXT NOT NULL DEFAULT 'application/pdf',
    sha256        TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    supersedes    TEXT REFERENCES document_version(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_document_version_doc_id ON document_version(document_id);
CREATE INDEX IF NOT EXISTS idx_document_version_sha256 ON document_version(sha256);

-- ---------------------------------------------------------------------------
-- Ingestion runs (pipeline stage tracking)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ingestion_run (
    id            TEXT PRIMARY KEY,
    started_at    TIMESTAMPTZ DEFAULT NOW(),
    completed_at  TIMESTAMPTZ,
    status        TEXT NOT NULL DEFAULT 'running' CHECK (status IN ('running', 'completed', 'failed')),
    manifest_hash TEXT,
    error_message TEXT
);

-- ---------------------------------------------------------------------------
-- Extraction runs (LLM / deterministic extraction jobs)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS extraction_run (
    id                TEXT PRIMARY KEY,
    ingestion_run_id  TEXT REFERENCES ingestion_run(id) ON DELETE SET NULL,
    model             TEXT,
    pipeline_stage    TEXT NOT NULL,
    config_json       JSONB,
    started_at        TIMESTAMPTZ DEFAULT NOW(),
    completed_at      TIMESTAMPTZ,
    status            TEXT NOT NULL DEFAULT 'running' CHECK (status IN ('running', 'completed', 'failed'))
);

-- ---------------------------------------------------------------------------
-- Review queue (human + AI adjudication)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS review_queue (
    id              TEXT PRIMARY KEY,
    item_type       TEXT NOT NULL CHECK (item_type IN (
        'canonical_node', 'relationship_assertion', 'placement_assertion',
        'merge_assertion'
    )),
    item_id         TEXT NOT NULL,
    confidence      REAL NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    status          TEXT NOT NULL DEFAULT 'pending' CHECK (status IN (
        'pending', 'assigned', 'approved', 'rejected', 'escalated'
    )),
    assigned_to     TEXT,
    escalation_reason TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_review_queue_status ON review_queue(status);
CREATE INDEX IF NOT EXISTS idx_review_queue_type ON review_queue(item_type);

-- ---------------------------------------------------------------------------
-- Canonical merge log (audit trail for deduplication)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS canonical_merge_log (
    id          TEXT PRIMARY KEY,
    from_node_id TEXT NOT NULL,
    to_node_id   TEXT NOT NULL,
    merged_at    TIMESTAMPTZ DEFAULT NOW(),
    merge_reason TEXT NOT NULL,
    merged_by    TEXT
);

-- ---------------------------------------------------------------------------
-- Audit events (operational observability)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_event (
    id          TEXT PRIMARY KEY,
    event_type  TEXT NOT NULL,
    actor       TEXT NOT NULL,
    details     JSONB,
    timestamp   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_event_type ON audit_event(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_event_timestamp ON audit_event(timestamp);

-- ---------------------------------------------------------------------------
-- Candidate staging tables (pre-promotion)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS candidate_node (
    id                TEXT PRIMARY KEY,
    extraction_run_id TEXT REFERENCES extraction_run(id) ON DELETE CASCADE,
    type              TEXT NOT NULL,
    label             TEXT NOT NULL,
    summary           TEXT,
    taxonomy_path     TEXT[],
    aliases           TEXT[],
    span_ids          TEXT[],
    confidence        REAL NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    status            TEXT NOT NULL DEFAULT 'candidate' CHECK (status IN (
        'candidate', 'validated', 'review_required', 'rejected'
    )),
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS candidate_assertion (
    id                TEXT PRIMARY KEY,
    extraction_run_id TEXT REFERENCES extraction_run(id) ON DELETE CASCADE,
    edge_type         TEXT NOT NULL,
    from_node_id      TEXT NOT NULL,
    to_node_id        TEXT NOT NULL,
    reasoning_summary TEXT NOT NULL,
    inference_type    TEXT NOT NULL,
    confidence        REAL NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    evidence_ids      TEXT[],
    status            TEXT NOT NULL DEFAULT 'candidate' CHECK (status IN (
        'candidate', 'validated', 'review_required', 'rejected'
    )),
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

COMMIT;
