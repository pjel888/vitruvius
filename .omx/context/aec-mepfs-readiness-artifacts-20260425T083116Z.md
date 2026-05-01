---
task: aec-mepfs-readiness-artifacts
created: 2026-04-25T08:31:16Z
mode: ralph-ultrawork
status: active
---

# AEC-MEPFS Readiness Artifacts Context

## Task Statement

Produce the next AEC-MEPFS Backbone readiness-phase artifacts:

- source/standards/legal source pack
- L1/L2 taxonomy decision record
- governance/editorial control pack
- deterministic resolver spec
- taxonomy authoring and migration QA pack
- Philippines overlay pilot pack

## Desired Outcome

Create concrete, testable readiness-control documents under
`.ai/03_plans/AEC-MEPFS-Backbone/` so the architecture remains blocked from
runtime implementation until source rights, taxonomy governance, resolver,
authoring QA, and overlay criteria are explicit.

## Known Evidence

- The readiness plan is
  `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md`.
- The research integration addendum is
  `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_research_integration_addendum.md`.
- AECMEPFS++ research inputs live under `.ai/13_research/AECMEPFS++/`.
- The current packet says implementation remains `not ready`.

## Constraints

- This lane is documentation/readiness artifact production only.
- No source-code edits, Neo4j writes, graph rebuilds, feature-flag changes,
  backup/restore test runs, or derived-artifact cleanup are authorized.
- Kimi may be used as an auxiliary reviewer, but Codex owns integration and
  validation.
- Existing unrelated dirty work, including `explorer/package.json`, must not be
  modified by this task.

## Unknowns

- Which official source links are stable enough to cite in the source pack.
- Whether any source families must remain `unverified` until a later legal or
  steward review.
- Whether the first L1/L2 seed should accept the 18-domain proposal exactly or
  reduce it for MVP readiness.

## Likely Touchpoints

- `.ai/03_plans/AEC-MEPFS-Backbone/*.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/README.md`
- `.omx/plans/aec-mepfs-backbone-readiness-plan-20260425T010419Z.md`
- `.omx/state/sessions/019dc3b9-26f1-7262-aba4-816b6ac1f679/`
