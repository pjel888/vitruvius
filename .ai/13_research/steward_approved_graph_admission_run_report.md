# Steward-Approved Graph Admission Run Report

Date: 2026-05-02T06:03:16Z

## Summary

The project owner supplied standing steward authorization. This run converted that authorization into three scoped, action-specific approval records rather than a blanket approval record.

Implemented admissions:

| Candidate | Group | Packet | Decision | Admission |
|---|---|---|---|---|
| Deep Foundations | `dup-5c6457d515c1` | `p1-decision-packet-8a66e785d02a` | `GOVERNED_DISAMBIGUATION` | admitted: reciprocal CROSS_DOMAIN_ALIGNMENT |
| Shallow Foundations | `dup-6400e3e0c204` | `p1-decision-packet-d5a20759fdfd` | `GOVERNED_DISAMBIGUATION` | admitted: reciprocal CROSS_DOMAIN_ALIGNMENT |
| Buildings | `dup-ca1078594013` | `p1-decision-packet-fee6fbd9a0fc` | `DISAMBIGUATED_KEEP_SEPARATE` | steward_approved: metadata-only keep separate |


## Safety confirmations

- Production graph nodes added/deleted/renamed: 0.
- Base shadow graph file edge rows changed: 0.
- Active admitted stewardship relationship overlay edges added: 4.
- Merge/alias/redirect/tombstone records created: 0 / 0 / 0 / 0.
- Resource Layer resources/nodeResourceLinks changed: 0 / 0; counts remain 7 / 9.
- `CROSS_DOMAIN_EQUIVALENT` admitted edges: 0.
- Buildings visible graph edge admission: none; metadata-only disambiguation was recorded.

## Scoped approval records

- `canonical-approval-20260502055659-b9a6f6b671e2` for `dup-5c6457d515c1` / decision `canonical-20260502055659-9bcef6559923`: source `user_supplied_standing_steward_approval`, scope `non_destructive_edge_admission`, status `admitted`, manifest `canonical-tx-20260502055659-1db3a592dcbf`.
- `canonical-approval-20260502055700-0109b1ea4688` for `dup-6400e3e0c204` / decision `canonical-20260502055659-59a7c7db99fe`: source `user_supplied_standing_steward_approval`, scope `non_destructive_edge_admission`, status `admitted`, manifest `canonical-tx-20260502055700-16e059859bd5`.
- `canonical-approval-20260502055700-65171a76c4e6` for `dup-ca1078594013` / decision `canonical-20260502055700-8e92ff2fc366`: source `user_supplied_standing_steward_approval`, scope `metadata_only`, status `steward_approved`, manifest `canonical-tx-20260502055700-03aee1feeafc`.

## Admitted relationships

- `VTN-DOM-0000262--cross_domain_alignment--VTN-DOM-0003013`: `VTN-DOM-0000262` -> `VTN-DOM-0003013` type `CROSS_DOMAIN_ALIGNMENT`, approval `canonical-approval-20260502055659-b9a6f6b671e2`, decision `canonical-20260502055659-9bcef6559923`.
- `VTN-DOM-0003013--cross_domain_alignment--VTN-DOM-0000262`: `VTN-DOM-0003013` -> `VTN-DOM-0000262` type `CROSS_DOMAIN_ALIGNMENT`, approval `canonical-approval-20260502055659-b9a6f6b671e2`, decision `canonical-20260502055659-9bcef6559923`.
- `VTN-DOM-0000261--cross_domain_alignment--VTN-DOM-0003010`: `VTN-DOM-0000261` -> `VTN-DOM-0003010` type `CROSS_DOMAIN_ALIGNMENT`, approval `canonical-approval-20260502055700-0109b1ea4688`, decision `canonical-20260502055659-59a7c7db99fe`.
- `VTN-DOM-0003010--cross_domain_alignment--VTN-DOM-0000261`: `VTN-DOM-0003010` -> `VTN-DOM-0000261` type `CROSS_DOMAIN_ALIGNMENT`, approval `canonical-approval-20260502055700-0109b1ea4688`, decision `canonical-20260502055659-59a7c7db99fe`.


## Validation highlights

- Canonical stewardship validation: passed, blockers 0, approvals 3, admittedRelationships 4, unresolvedDuplicateGroups 541.
- Graph relationship validation: passed, nodeCount 10018, effective edgeCount 13674 (base 13670 + admitted overlay 4), issueCount 0.
- Resource Layer validation: passed with known ASCE 7 / ACI 318 context warnings; Resource Layer counts unchanged.
- Neighborhood visibility: Deep and Shallow foundation nodes each return the reciprocal `CROSS_DOMAIN_ALIGNMENT` edge through `/node/:id/neighborhood?depth=1&direction=both`.
- Sendai Mediatheque / Toyo Ito regression remains visible.

## Known caveats

P1 decision packets are now stale relative to current canonical state because this run admitted stewardship decisions after packet generation. This is a warning, not a blocker; the next exact action is to refresh or rebase P1 packet custody snapshots and review hashes without losing review history.

## Next exact action

Refresh P1 decision-packet custody snapshots after the first admissions, preserving review history and making stale-review behavior explicit, then continue with the next low/medium-risk P1 admission candidates.



## 2026-05-02T06:05:37Z - Final validation update

- `cd api && bun test` passed: 172 tests. Initial expected-edge-count failures were fixed by updating admitted-overlay graph count contracts from 13,670 to 13,674 where API render output includes active admitted stewardship overlays.
- `cd explorer && bun test` passed: 112 tests.
- `cd explorer && bun run build` passed with known Vite chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` passed: 104 tests.
- `bun run api/validateCanonicalGraphStewardship.ts` passed with blockers 0; warnings note unsigned/stale P1 packet snapshots after admission.
- `bun run api/validateGraphRelationships.ts` passed with 10,018 nodes and 13,674 effective edges.
- `bun run api/validateResourceLayer.ts` passed with known ASCE 7 / ACI 318 context warnings.

## Post-Kimi implementation-safety repair (2026-05-02T06:20:00Z)

Kimi's final implementation-safety review was accepted. Before commit, the run repaired two custody issues:

- Approval records for Deep Foundations, Shallow Foundations, and Buildings now contain revalidated embedded snapshots with `ok: true` and no embedded false blocker snapshots.
- Buildings remains a metadata-only `DISAMBIGUATED_KEEP_SEPARATE` / governed-disambiguation decision; latent `CROSS_DOMAIN_ALIGNMENT` relationship proposals were cleared and no Buildings graph edge was admitted.
- A new `canonical_approval_metadata_revalidation` transaction manifest (`canonical-tx-20260502061917-f0d21c4f7013`) records the approval/decision metadata repair.
- Current canonical validation: blockers 0; approvals 3; admitted relationships 4; transaction manifests 30; latest afterHash mismatches 0.

Accepted Kimi suggestions: repair failed embedded validation snapshots; remove latent Buildings edge proposals; isolate commit scope. Rejected: none. Deferred: P1 packet custody snapshot refresh after admitted canonical state.

## Final validation pass (2026-05-02T06:22:30Z)

- `bun run api/validateCanonicalGraphStewardship.ts` ? passed; blockers 0; approvals 3; admittedRelationships 4; transactionManifests 30; latestAfterHashMismatches 0.
- `bun run api/validateGraphRelationships.ts` ? passed; 10,018 nodes; 13,670 base edges; 13,674 effective edges; issueCount 0.
- `bun run api/validateResourceLayer.ts` ? passed with known ASCE 7 / ACI 318 standards-context warnings; blockers 0.
- `cd api && bun test` ? passed; 172 tests.
- `cd explorer && bun test` ? passed; 112 tests.
- `cd explorer && bun run build` ? passed with known Vite chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` ? passed; 104 tests.

## Change-scope checks

- Post-implementation code-intelligence refresh completed. Known warnings remain: missing `tree-sitter-yaml` in code-review-graph and ChunkHound/code-review-graph embedding provider context-length errors; wrapper completed and GitNexus was up to date.
- GitNexus detect-changes on full worktree initially reported critical risk because unrelated unstaged AEC run-persistence files are present.
- GitNexus detect-changes on the staged admission scope reported medium risk: 39 files, 36 symbols, 5 affected processes.
- `git diff --cached --check` passed after removing trailing blank lines.


## 2026-05-02T07:20:07Z - Post-admission packet custody rebase

After the first steward-approved admissions, all 20 P1 decision packets were rebased against the current graph/canonical state. The admitted Deep/Shallow alignment packets and Buildings metadata-only packet now link to their specific approval/admission records. Existing Kimi reviews were carried forward with lineage/caveats; no new graph mutation occurred in the rebase.
