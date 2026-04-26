---
task: aec-mepfs-shadow-evidence-repo-state-hardening
phase: 05
created: 2026-04-26
author: CODEX
status: PASS
supersedes: null
---

# Twenty-Seventh Shadow Slice: Evidence Repo-State Hardening

## Scope

Harden the file-backed AEC-MEPFS shadow evidence reports and preview so
generation-time repository state distinguishes source-tree dirtiness from
generated evidence dirtiness.

This slice remains shadow-only and read-only. It does not promote the shadow
graph, write Neo4j, rebuild the KG, ingest protected content, change feature
flags, mount `/v2/resolve`, or make Explorer adopt the shadow graph by default.

## Audit Findings

- The route inventory, boundary audit, benchmark, and evidence manifest reports
  only recorded aggregate `working_tree_dirty`.
- Sequential evidence generation can make later reports dirty solely because
  prior generated reports exist under
  `006_System-Manifests/aec-mepfs-backbone/`.
- The API/Explorer evidence preview could not explain whether dirtiness came
  from source changes or generated evidence artifacts.
- Legacy manifests lack the new repo-state fields, so the preview must not
  silently render them as clean.

## Implementation Plan

1. Extend the four report generators with repo-state fields for source dirty
   status, generated-evidence dirty status, and both dirty path counts.
2. Parse `git status --short --untracked-files=all` so untracked generated
   report files are counted at file granularity.
3. Extend the sanitized `/v2/backbone/evidence` preview with the new
   repo-state freshness fields.
4. Render the fields in the explicit-action Explorer evidence preview and
   display legacy manifests as `unknown`, not clean.
5. Fail closed when a refreshed manifest explicitly reports source-tree
   dirtiness.
6. Cross-check evidence input report commit/source freshness where repo-state
   metadata is present.
7. Add focused Python, API, and Explorer tests for the new repo-state contract.

## Plan Critique

- [C001] Do not require runtime git shelling from the API route; this remains a
  file-backed preview over the manifest.
- [C002] Do not treat generated evidence dirtiness as a source integrity
  failure.
- [C003] Do not misrepresent old manifests that lack freshness fields.
- [C004] Do not expose raw report payloads or input hashes in Explorer.
- [C005] Do not regenerate the final evidence packet until the source-tree
  hardening commit is clean.

## Execution Checklist

- [x] Run impact review for report generators and preview builder.
- [x] Add source/generated repo-state split to route inventory, boundary audit,
  benchmark, and evidence manifest reports.
- [x] Add API preview fields with legacy `unknown` handling.
- [x] Add Explorer preview rendering for freshness availability, source dirty,
  source dirty path count, generated evidence dirty, and generated evidence
  dirty path count.
- [x] Add regression tests for generated evidence dirtiness, unknown legacy
  freshness, and source-dirty fail-closed behavior.
- [x] Add manifest cross-report freshness checks for divergent input commits
  and source-dirty input reports.
- [x] Run focused and affected verification.
- [x] Record advisory review results and residual risks.

## Explicit Non-Goals

- No Neo4j write, query, backup, restore, or cleanup.
- No KG rebuild/reset/load.
- No protected source content ingest.
- No feature flag cutover.
- No `/v2/resolve` or `/v2/resolve/trace` route mounting.
- No Explorer default graph adoption.
- No runtime resolver/API/Explorer/Neo4j benchmark threshold claim.

## Next Safe Slice

After this commit is clean and pushed, generate a fresh evidence packet from
the clean source tree using the hardened reports. That packet should show
`source_working_tree_dirty: false` while later reports may show
`generated_evidence_dirty: true` because earlier generated evidence files exist.
