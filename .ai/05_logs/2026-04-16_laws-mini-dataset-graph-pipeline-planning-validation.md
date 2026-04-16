---
task: laws-mini-dataset-graph-pipeline
phase: 09
created: 2026-04-16
author: REVIEWER
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Laws Mini Dataset Graph Pipeline Planning Validation

## What was created
- `.ai/04_tasks/laws-folder-mini-graph-pipeline-trigger.md`
- `.ai/10_state/baselines/laws-folder-mini-graph-pipeline-baseline.md`
- `.ai/13_research/laws-folder-mini-graph-pipeline-research.md`
- `.ai/02_audits/laws-folder-mini-graph-pipeline-audit.md`
- `.ai/03_plans/2026-04-16_laws-mini-dataset-graph-pipeline-plan.md`

## What was verified
- Planner produced an initial repo-grounded option set
- Architect review approved the revised milestone split and scoping constraints
- Critic approved the revised plan as bounded, truthful, and testable
- Plan index was updated to include the new live plan

## Consensus outcome
- Verdict: **APPROVED**
- Decision: proceed with a **manifest-backed core-laws-bundle scoped graph proof first** (`PD-1096`, `RA-9514`, `BP-344`, `BP-220`), not a generic laws-folder pipeline and not a direct raw-folder→graph claim

## Key planning answer
Yes, Vitruvius can already output a real knowledge graph, but the first truthful implementation target is a **4-folder core-laws-bundle scoped graph proof** built from manifest-selected canonical/promoted inputs with dataset-specific artifacts and no writes to global `latest_*` paths.

## Planning refinement after user follow-up
- The user explicitly asked that the **next step** be a path/blast-radius/optimization audit, not implementation.
- The live plan was updated so the first implementation-adjacent milestone is preceded by a path audit covering:
  - full source→graph mapping
  - blast-radius analysis
  - optimization triage
  - future Rust-candidate screening
- No execution approval is implied by this planning artifact alone.

## Additional user constraint captured
- The user explicitly elevated **8 GB M2-class low-spec viability** to a first-class goal.
- The live plan, research pack, and audit now treat low-spec operation as a real success criterion, while still rejecting premature or wrong-layer optimization.

## Team-assisted M0 deepening
- A bounded `omx team` analysis-only pass was used to deepen M0 without code edits.
- The useful returned evidence was integrated into the research/audit/plan layers:
  - stronger global-artifact coupling evidence
  - current artifact footprint notes
  - additional graph/query test-slice evidence
  - deeper low-spec and Rust-candidacy triage
  - concrete M1 decision defaults
  - clearer artifact freshness / completeness / thin-graph criteria
  - stronger go/no-go readiness framing
  - explicit `SUCCESS` / `PARTIAL` / `FAIL` rubric for M1

## Further execution-grade refinement
- Added an explicit **Implementation Forbidden Moves** section to the live plan.
- This now makes the planning artifact stronger by naming the shortcuts that would invalidate M1, including:
  - pilot bundle hardcoding
  - global `latest_*` reuse in dataset mode
  - direct raw-folder→graph shortcuts
  - default/global CLI repointing
  - premature Rust moves

## Additional planning hardening
- Added explicit **M0 Exit Criteria** to the live plan so the path-audit phase itself has a definition of done before implementation may begin.
- Added an explicit **Decision Closure Order** so unresolved M1 design choices are closed in a dependency-aware sequence rather than ad hoc.
- Added a **Verification Surface Map** tying likely M1 change areas to the primary test/validation surfaces that should be exercised later.
- Added the explicit **M1→M2 boundary recommendation** and **coverage/thin-graph reporting recommendation** into the audit so milestone widening is governed rather than ad hoc.
- Added a formal **M1 Evidence Package Template** so future execution has a concrete artifact bundle to produce before the proof can be accepted.
- Added an **Assumptions and Invalidation Triggers** register plus a **Defer Matrix After M1** so the plan is clearer about what is currently assumed and what should still stay out of scope even after first success.
## Additional M0 deepening — macro/codebase guardrails
- Added explicit **Default / Global Path Preservation Contract** to the live implementation plan.
- Added explicit **Pilot Distortion Guardrails** so the first four-folder bundle remains a manifest instance, not a code primitive.
- Added explicit **Rollout and Rollback Rules** to keep the first implementation slice reversible without touching existing global/shared artifacts.
- Added explicit **Dataset Output Freshness Contract** so scoped outputs cannot be mistaken for current truth.

## Additional execution-grade refinement — admission, traceability, authorization
- Added a formal **Pilot Bundle Admission Checklist** to the live plan so the four-folder bundle is admitted explicitly instead of inferred by folder heuristics.
- Added a formal **Requirement-to-Evidence Traceability Matrix** so each major execution requirement maps to a concrete proof artifact.
- Added a formal **M1 Authorization / Sign-Off Checklist** so implementation cannot begin on stale assumptions or stale code-intelligence context.
- Added supporting audit/research notes covering:
  - the BP-344-adjacent document under `001-Laws/DPWH/`
  - the need to refresh GitNexus before any later code-edit phase

## Additional execution-grade refinement — variant policy and negative verification
- Added a formal **Variant / Edition Admission Policy** to the live plan so the pilot cannot silently treat scans, summaries, illustrated editions, revised IRRs, and partial extracts as interchangeable.
- Added **pilot manifest entry metadata defaults** to the dataset contract so file-role ambiguity is handled in manifest data instead of code heuristics.
- Added a formal **Negative Verification Matrix** so future M1 validation defines the expected failure behavior for major misuse cases, not just the happy path.
- Added matching audit/research notes covering:
  - variant-rich evidence inside `PD-1096/`
  - role ambiguity already visible inside `BP-344/`

## Additional execution-grade refinement — bootstrap and touchpoint control
- Added a formal **Implementation Session Bootstrap Protocol** so the next execution session has a fixed pre-edit sequence.
- Added a formal **M1 Change Budget / Touchpoint Budget** so the first coding slice stays bounded unless evidence forces widening.
- Added matching audit guidance that the first implementation pass should enforce both bootstrap discipline and touchpoint discipline.

Fresh verification evidence:
- `git diff --check -- .ai/03_plans/2026-04-16_laws-mini-dataset-graph-pipeline-plan.md` → PASS
- The live plan now contains the new sections:
  - `Default / Global Path Preservation Contract`
  - `Pilot Distortion Guardrails`
  - `Rollout and Rollback Rules`
  - `Dataset Output Freshness Contract`
- The verification plan now explicitly includes:
  - preserving the default/global graph and query path when dataset mode is unused
  - rollback validation
  - freshness/selection validation
- `npx gitnexus status` → `Status: ⚠️ stale (re-run gitnexus analyze)` with `indexed commit: 616c14a` and `current commit: e3c2bda`
- raw-bundle inspection confirms a BP-344-adjacent source lives outside the pilot folder:
  - `001_Raw-Source-Layer/001-Laws/DPWH/DPWH DO037 Enforcement of BP344 along National Roads.pdf`
- all currently named verification-surface test files are present:
  - `scripts/tests/test_graph_builder.py`
  - `scripts/tests/test_graph_cli.py`
  - `scripts/tests/test_query_cli.py`
  - `scripts/tests/test_query_engine.py`
  - `scripts/tests/test_query_seed_accuracy.py`
  - `scripts/tests/test_run_promote.py`
  - `scripts/tests/test_integration_e2e.py`
  - `scripts/tests/test_pipeline_cli_byte_identity.py`
- raw-bundle file inspection confirms `PD-1096/` contains multiple distinct variant styles:
  - complete scan
  - full text
  - illustrated edition
  - summary
  - compact edition
  - multiple IRR/RIRR files and partial rule extracts
- raw-bundle file inspection confirms `BP-344/` contains at least two distinct variant/authority candidates:
  - `2024 Revised Implementing Rules and Regulations ...`
  - `BP-344 IRR Accessibility Law DPWH.pdf`
- likely initial M1 control-plane touchpoints are present in the repo:
  - `scripts/pipeline_cli.py`
  - `scripts/vitruvius/graph/cli.py`
  - `scripts/vitruvius/graph/builder.py`
  - `scripts/vitruvius/query/cli.py`
  - `scripts/vitruvius/ontology/cli.py`
  - `scripts/vitruvius/promotion/__init__.py`
  - `scripts/vitruvius/relationships_sections.py`
