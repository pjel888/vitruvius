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
## Additional M0 deepening — macro/codebase guardrails
- Added explicit **Default / Global Path Preservation Contract** to the live implementation plan.
- Added explicit **Pilot Distortion Guardrails** so the first four-folder bundle remains a manifest instance, not a code primitive.
- Added explicit **Rollout and Rollback Rules** to keep the first implementation slice reversible without touching existing global/shared artifacts.
- Added explicit **Dataset Output Freshness Contract** so scoped outputs cannot be mistaken for current truth.

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
