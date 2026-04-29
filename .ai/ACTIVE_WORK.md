# Active Work

**Updated:** 2026-04-29
**Scope:** only active and incomplete work belongs here

## NOW

### 1. KG-first cleanup — Phase 1 live-doc reconciliation
- **Status:** active implementation slice
- **Why it matters:** Vitruvius is now KG-first/AEC-MEPFS-first. Live docs must stop presenting the legacy raw/conversion/canonical pipeline as the product architecture going forward, while preserving the numbered layers as source custody, extraction staging, evidence preparation, compatibility infrastructure, and historical provenance support.
- **Evidence:** `/.ai/03_plans/kg-first-cleanup/README.md`, `/.ai/03_plans/kg-first-cleanup/2026-04-29_research_pack.md`, `/.ai/03_plans/kg-first-cleanup/2026-04-29_blast_radius_audit.md`, `/.ai/03_plans/kg-first-cleanup/2026-04-29_cleanup_strategy_plan.md`, `/.ai/03_plans/kg-first-cleanup/2026-04-29_plan_critique.md`, `/.ai/03_plans/kg-first-cleanup/2026-04-29_execution_checklist.md`
- **Next concrete action:** complete docs-only reconciliation, update validation evidence, and do not proceed to code-facing cleanup unless exact GitNexus impact plus tests-first proof exist.
- **Guardrails:** no raw-source writes, no numbered layer renames, no generated artifact deletion, no KG rebuild/reload/reset, no Neo4j mutation, no protected payload ingest/exposure, no API or Explorer behavior change.

### 2. AEC-MEPFS authored backbone and file-backed local runtime
- **Status:** implemented locally; production/protected gates remain hard-blocked
- **Why it matters:** the product direction is authored KG/backbone first, with source attachment and guarded evidence admission layered beneath it.
- **Evidence:** `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_actual_aec_mepfs_implementation_cutover_packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/final-aec-mepfs-actual-implementation-closure-packet.md`, `/.ai/05_logs/2026-04-28_aec_mepfs_actual_implementation_cutover_validation.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_broad_taxonomy_real_semantic_enrichment_packet.md`, `/006_System-Manifests/aec-mepfs-backbone/taxonomy-expansion/20260429T015840Z/all-taxonomy-deep-population-report.json`
- **Next concrete action:** continue only with bounded rights-safe taxonomy, relationship, source-overlay, or performance work under dedicated packets. Production Neo4j promotion requires production credentials and backup/restore/rollback proof; protected payload admission requires valid external legal/steward/source-rights authority.

## NEXT

### 3. Optional CLI/operator wording reconciliation
- **Status:** deferred until Phase 1 docs reconciliation is validated
- **Why it matters:** CLI help can clarify KG-first/source-evidence roles, but command behavior and output paths must remain stable.
- **Next concrete action:** only touch `scripts/pipeline_cli.py` after GitNexus freshness, exact symbol impact, and tests-first coverage are attached. Preserve every command, alias, output path, source ID, and runtime behavior.

### 4. Source-ingestion adapter clarification
- **Status:** deferred
- **Why it matters:** source-ingestion modules remain live compatibility and evidence-prep infrastructure.
- **Next concrete action:** prefer docstrings/comments and characterization tests; do not delete, rename paths, change IDs, change output formats, or move generated artifacts.

## LATER / BLOCKED

- Production Neo4j live graph promotion: blocked without target credentials and backup/restore/rollback transcript.
- Protected source payload admission: blocked without valid external legal/steward/source-rights authority.
- Legacy pipeline deletion: out of scope until exact no-caller proof, reference cleanup, replacement documentation, regression tests, and rollback proof exist.
