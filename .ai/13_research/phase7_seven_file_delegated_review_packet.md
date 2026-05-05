# Phase 7 Seven-File Delegated Review Packet

**Date:** 2026-05-06
**Prepared for:** Project-owner-delegated external AI reviewer (Claude, Kimi, or OpenCode)
**Reviewer identity rule:** record the reviewer as external AI, not biological human.

## Required Verdict

Return exactly one verdict:

- `PASS_COMMIT_SAFE_FILES`
- `PASS_REVERT_SAFE_FILES`
- `PASS_QUARANTINE_ONLY`
- `NEEDS_PROJECT_OWNER_REVIEW`
- `BLOCK_PHASE7`

## Safety Constraints

- Do not begin Phase 7 implementation.
- Do not create candidates, Resources, or nodeResourceLinks.
- Do not promote candidates or auto-link files.
- Do not verify external URLs, DOIs, ISBNs, PDFs, or source truth.
- Do not mutate Resource Layer production registries.
- Do not mutate graph-canonical registries.
- Do not admit graph edges, aliases, redirects, tombstones, or canonical merges.
- Do not process P0 Concrete/Reinforced Concrete or high-risk P1 packets.
- Do not stage quarantined `003_Canonical-Knowledge-Layer` artifacts, generated source markdown artifacts, production registries, graph-canonical registries, or transaction manifests.

## Current Verified Metrics

- Branch: `main`
- HEAD/origin: `358f18bd244029b4077b306afe328b9cee0cbd4e` before this seven-file review commit.
- Admitted relationships: 264.
- Base graph edges: 13,670.
- Effective graph edges: 13,934.
- `CROSS_DOMAIN_EQUIVALENT`: 0.
- `CROSS_DOMAIN_ALIGNMENT`: 22.
- Resource Layer: 7 resources, 9 nodeResourceLinks, 4 resource candidates.
- External metadata candidates: 0 production records.
- Local files indexed/admitted: 25 / 0.
- Standards missing/blocked: 2 / 3.
- ASCE 7 and ACI 318 remain incomplete and not learner-trusted.
- Production Resource Layer registries: clean.
- Graph-canonical registries: clean.

## Dirty Worktree Classification

Initial dirty entries: 818.

- `unrelated_canonical_source_file`: 439.
- `generated_conversion_or_source_markdown_artifact`: 371.
- `needs_reviewer_review`: 7.
- `safe_local_artifact`: 1 (`nul`).
- `unsafe_executable_script`: 0.
- `production_resource_layer_registry`: 0.
- `graph_canonical_registry`: 0.
- `unknown`: 0.

## Seven File Classification And Proposed Action

| File | Classification | Risk | Proposed action |
|---|---|---|---|
| `README.md` | intentional documentation change; revised during review to remove raw `rm -rf` instructions | Low/medium | Commit if reviewer accepts guarded wording |
| `scripts/pipeline_cli.py` | intentional code change; pipeline/Neo4j error handling | Medium/high | Commit if reviewer accepts tests and fail-closed behavior |
| `scripts/tests/test_canonicalize_body.py` | intentional tests | Low | Commit |
| `scripts/tests/test_kg_pipeline_force_path.py` | intentional tests plus Windows-safe existing assertion repair | Low/medium | Commit |
| `scripts/vitruvius/canonicalize.py` | intentional canonicalization behavior; source cards include full text; refined Markdown preferred | Critical impact by GitNexus | Commit only if reviewer accepts |
| `scripts/vitruvius/kg/neo4j_client.py` | intentional connectivity-status helper | Medium | Commit if reviewer accepts |
| `scripts/vitruvius/rules/slug_alias_registry.yaml` | one local slug collision mapping | Medium/high | Commit if reviewer accepts local-evidence-only scope |

## Validation Evidence

Passed:

- Resource validator: PASS.
- Graph validator: PASS.
- Canonical validator: PASS.
- API tests: PASS, 398.
- Explorer tests: PASS, 118.
- Explorer build: PASS.
- Python KG regression: PASS, 118.
- `scripts/tests/test_canonicalize_body.py`: PASS, 34.
- `scripts/tests/test_kg_pipeline_force_path.py`: PASS, 16.
- `pipeline_cli.py --help`: PASS.
- `pipeline_cli.py run-kg-pipeline --help`: PASS.
- `git diff --check -- <seven files>`: PASS.

Optional broader selector:

- `scripts/tests --ignore=bench -k "canonicalize or pipeline_cli or slug or neo4j or kg_pipeline"`: 208 passed, 19 failed, 18 skipped.
- Failures are Windows path-separator expectations in tests outside the authorized seven-file set.
- The selector without bench ignores fails collection on POSIX-only `resource` module imports.

## Questions For Reviewer

1. Is each file classification correct?
2. Are any changes unsafe?
3. Are any files safe to commit?
4. Are any files safe to revert?
5. Are any files still requiring project-owner review?
6. Are any mutation/admission/promotion risks introduced?
7. Is Phase 7 implementation still blocked?
8. What exact action should be taken for each of the seven files?

## Files That Must Not Be Staged

- Dirty `003_Canonical-Knowledge-Layer` files.
- Generated conversion/source markdown artifacts.
- Production Resource Layer registries.
- Graph-canonical registries.
- Transaction manifests.
- `nul`.
- Any file outside the seven reviewed files and scoped `.ai` reports/logs/state updates.

## Reviewer Caveat To Preserve

This is a delegated external AI review, not a biological human review, not source truth, and not production approval by itself.
