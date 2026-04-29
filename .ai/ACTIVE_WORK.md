# Active Work

**Updated:** 2026-04-29
**Scope:** only active and incomplete work belongs here

## NOW

### 1. KG-first cleanup — Phase 2+ operator and adapter reconciliation
- **Status:** active final validation/commit slice
- **Why it matters:** Phase 1 live-doc reconciliation is complete. The remaining safe cleanup is behavior-preserving operator wording, source-adapter docstring clarification, and active-plan status reconciliation so the repo consistently presents KG-first/AEC-MEPFS as the product direction while retaining source custody, extraction staging, evidence preparation, compatibility infrastructure, and historical provenance support.
- **Evidence:** `/.ai/03_plans/kg-first-cleanup/README.md`, `/.ai/03_plans/kg-first-cleanup/2026-04-29_phase1_docs_reconciliation_validation_log.md`, `/.ai/03_plans/kg-first-cleanup/2026-04-29_phase2_plus_cli_and_adapter_validation_log.md`, `scripts/vitruvius/cli_experience.py`, `scripts/tests/test_cli_operator_experience.py`
- **Next concrete action:** finish verification, commit the behavior-preserving Phase 2/3/4 slice, and keep deletion/refactor work blocked unless exact no-caller proof, tests, and rollback evidence exist.
- **Guardrails:** no raw-source writes, no numbered layer renames, no generated artifact deletion, no KG rebuild/reload/reset, no Neo4j mutation, no protected payload ingest/exposure, no API or Explorer behavior change.

### 2. AEC-MEPFS authored backbone and file-backed local runtime
- **Status:** implemented locally; production/protected gates remain hard-blocked
- **Why it matters:** the product direction is authored KG/backbone first, with source attachment and guarded evidence admission layered beneath it.
- **Evidence:** `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_actual_aec_mepfs_implementation_cutover_packet.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/final-aec-mepfs-actual-implementation-closure-packet.md`, `/.ai/05_logs/2026-04-28_aec_mepfs_actual_implementation_cutover_validation.md`, `/.ai/03_plans/AEC-MEPFS-Backbone/2026-04-29_broad_taxonomy_real_semantic_enrichment_packet.md`, `/006_System-Manifests/aec-mepfs-backbone/taxonomy-expansion/20260429T015840Z/all-taxonomy-deep-population-report.json`
- **Next concrete action:** continue only with bounded rights-safe taxonomy, relationship, source-overlay, or performance work under dedicated packets. Production Neo4j promotion requires production credentials and backup/restore/rollback proof; protected payload admission requires valid external legal/steward/source-rights authority.

## NEXT

### 3. Delete-later candidates
- **Status:** blocked by design for this cleanup pass
- **Why it matters:** the legacy source/evidence modules remain compatibility and provenance infrastructure under the KG-first product direction.
- **Next concrete action:** do not delete until GitNexus proves no callers, all docs/tests/config references are reconciled, replacement paths are documented, regression tests prove no behavior loss, and rollback is clean `git revert`.

### 4. Future source-overlay/content work
- **Status:** gated
- **Why it matters:** attaching source evidence to KG nodes is a product feature, but it is not a cleanup task and must respect protected-payload and source-rights gates.
- **Next concrete action:** reopen only through a dedicated evidence-admission or source-overlay packet.

## LATER / BLOCKED

- Production Neo4j live graph promotion: blocked without target credentials and backup/restore/rollback transcript.
- Protected source payload admission: blocked without valid external legal/steward/source-rights authority.
- Legacy pipeline deletion: out of scope until exact no-caller proof, reference cleanup, replacement documentation, regression tests, and rollback proof exist.
