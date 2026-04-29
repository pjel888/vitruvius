---
task: kg-first-cleanup
phase: implementation-plan
created: 2026-04-29
author: CODEX
status: PROPOSED
---

# KG-First Cleanup Strategy Plan

## Intent

Safely align the repository with the KG-first product direction without breaking
source custody, evidence extraction, AEC-MEPFS file-backed runtime behavior,
Explorer behavior, or historical validation evidence.

## Guiding Decision

The cleanup should be a **semantic reorientation**, not a purge. The old
layer-first code still has value as source ingestion, source identity, evidence
preparation, and compatibility infrastructure.

## In Scope For The Cleanup Program

- Plan-folder creation and planning evidence.
- Documentation reconciliation to KG-first language.
- CLI/help wording that presents old pipeline steps as evidence-prep adapters.
- Tests that lock existing behavior before any code cleanup.
- Optional archive/index updates for stale docs.
- Later, small adapter refactors that preserve behavior.

## Out Of Scope Until Separate Packet

- Deleting legacy pipeline modules.
- Renaming numbered layer directories.
- Bulk deleting generated artifacts.
- Modifying API or Explorer runtime behavior.
- KG rebuild/reload/reset.
- Neo4j mutation.
- Protected content ingest/exposure.
- Production graph promotion.

## Proposed Phases

### Phase 0 — Planning And Evidence (this slice)

Deliverables:

- `kg-first-cleanup/` plan folder.
- Research pack.
- Blast-radius audit.
- Strategy plan.
- Plan critique.
- Execution checklist.
- Validation log.

Exit criteria:

- Planning docs exist.
- `.ai/03_plans/INDEX.md` references this plan family.
- No product code changed.
- Git diff passes whitespace check.

### Phase 1 — Documentation Reconciliation

Goal: make live docs tell the truth: AEC-MEPFS is KG-first, while legacy layer
machinery remains source custody/evidence prep.

Candidate files:

- `README.md`
- `AGENTS.md`
- `scripts/AGENTS.md`
- `.ai/README.md`
- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/milestone-tracker.md`

Guardrails:

- Do not weaken raw-layer immutability.
- Do not remove old layer references where they describe actual filesystem
  contracts.
- Use language like "source custody / extraction staging / compatibility".

Verification:

- `git diff --check`
- reference scan for contradictory live claims
- no runtime tests needed unless code changes.

### Phase 2 — CLI Surface Rewording And Compatibility Tests

Goal: update operator-facing help and command grouping so KG-first work is clear
without changing behavior.

Candidate files:

- `scripts/pipeline_cli.py`
- `scripts/tests/test_dataset_pipeline_cli.py`
- relevant CLI help/operator-experience tests if present.

Guardrails:

- Run GitNexus impact for exact edited functions.
- Add/adjust tests before changing help behavior.
- Keep old commands and aliases working.

Verification:

- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -q`
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_pipeline_force_path.py -q`
- `git diff --check`

### Phase 3 — Source-Ingestion Adapter Cleanup

Goal: isolate old raw/conversion/canonical behavior behind clearer adapter names
while preserving paths and behavior.

Candidate files:

- `scripts/vitruvius/conversion.py`
- `scripts/vitruvius/normalization/refine.py`
- `scripts/vitruvius/canonicalize.py`
- `scripts/vitruvius/source_identity.py`
- `scripts/vitruvius/dataset_pipeline.py`

Guardrails:

- No directory renames.
- No source deletion.
- No generated artifact cleanup.
- Keep source ID parity.

Verification:

- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_conversion_fallback.py scripts/tests/test_refine.py scripts/tests/test_source_identity.py -q`
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_dataset_source_to_graph_pipeline.py -q`
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_evidence_ingestor.py -q`

### Phase 4 — Active/Archive Plan Surface Cleanup

Goal: reduce planning noise without losing evidence.

Candidate files:

- `.ai/03_plans/INDEX.md`
- `.ai/archive/ARCHIVE_INDEX.md`
- stale plan families under `.ai/03_plans/`

Guardrails:

- Archive or pointer, do not erase history.
- Do not move AEC-MEPFS active packets required by current state.
- Validate references after any move.

Verification:

- `find .ai/03_plans -maxdepth 2 -type f | sort`
- reference scan for moved paths
- `git diff --check`

### Phase 5 — Deletion Candidates Only After Proof

Goal: remove genuinely unused compatibility code only after concrete proof.

Prerequisites:

- exact GitNexus impact shows no runtime callers,
- tests pin old behavior or prove deprecation,
- docs and CLI expose migration path,
- rollback is a clean git revert,
- Kimi/advisory review has no unresolved concerns.

Verification:

- targeted Python tests,
- API/Explorer tests if touched,
- `npx --yes gitnexus@1.6.2-rc.10 detect-changes --repo vitruvius` if available,
- `git diff --check`.

## First Implementation Recommendation

Start with Phase 1 only. Do not touch product code until live documentation and
operator language agree on the new architecture.
