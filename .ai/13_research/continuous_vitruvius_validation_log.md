# Continuous Vitruvius Validation Log

Last updated: 2026-05-02T08:28:30Z

## Summary

- Completed ACS relation-vocabulary and source-context gate review for the 13 Kimi-accepted/promising candidates from the prior candidate batch.
- Admitted 3 safe non-destructive ACS `CONSTRAINS` overlay relationships.
- Added canonical stewardship support for `AEC_RELATIONSHIP_ENRICHMENT` decisions and admitted `CONSTRAINS` / `REQUIRES` overlay relation types.
- Refreshed/rebased 20 P1 packet custody snapshots after graph/canonical state changed; preserved and carried forward 13 reviews.
- Recorded 3 additional advisory Kimi P1 reviews; P1 reviewed/unreviewed is now 16 / 4.
- Retaining Wall high-risk P1 packet remains blocked after Kimi second-pass review.
- No merge, alias, redirect, tombstone, node mutation, base graph rewrite, Resource Layer mutation, fake source context, standard edition, numerical criterion, AHJ claim, URL, or protected payload was introduced.

## Admitted ACS edges

| Edge ID | Source | Relation | Target | Category | Approval |
|---|---|---|---|---|---|
| `VTN-DOM-0012293--constrains--VTN-DOM-0003010` | `VTN-DOM-0012293` | `CONSTRAINS` | `VTN-DOM-0003010` | semantic/aec-mechanism | canonical-approval-20260502082323-e3de9bdf3b1f |
| `VTN-DOM-0012771--constrains--VTN-DOM-0000313` | `VTN-DOM-0012771` | `CONSTRAINS` | `VTN-DOM-0000313` | semantic/aec-mechanism | canonical-approval-20260502082323-e3de9bdf3b1f |
| `VTN-DOM-0012777--constrains--VTN-DOM-0012313` | `VTN-DOM-0012777` | `CONSTRAINS` | `VTN-DOM-0012313` | semantic/aec-mechanism | canonical-approval-20260502082323-e3de9bdf3b1f |

## Counts after admission

- Nodes: 10,018
- Base edges: 13,670
- Effective edges with admitted overlays: 13,677
- Approvals: 4
- Admitted relationships: 7
- Aliases / redirects / tombstones: 0 / 0 / 0
- Resources / nodeResourceLinks: 7 / 9
- P1 reviewed / unreviewed: 16 / 4

## Validation snapshot

- Targeted canonical validation passed after admission and P1 review updates.
- Targeted graph relationship validation passed: effective edges 13,677, issue count 0.
- Resource Layer validation passed with existing ASCE 7 / ACI 318 context warnings only.
- Selected-node visibility passed for all 3 new ACS edges plus Deep Foundations and Sendai/Toyo Ito regressions.
- Latest afterHash mismatches: 0.

## Kimi summary

Accepted:
- Soil Bearing Capacity `CONSTRAINS` Shallow Foundations as a broad conceptual constraint.
- Groundwater Design Level `CONSTRAINS` Excavation Support with caution and no dewatering/code/numeric claim.
- Structural Wind Load `CONSTRAINS` Facade Assembly as a broad authored ontology/domain-synthesis edge, with no ASCE/code/numeric/AHJ/source claim.

Rejected/deferred:
- Soil Bearing Capacity `CONSTRAINS` Foundation System was not admitted because that base edge already exists.
- Foundation Settlement `CONSTRAINS` Foundation System was deferred; settlement is a performance outcome/limit state and wording needs review.
- Column `REQUIRES` Foundation System was deferred as a lossy substitute for future `TRANSFERS_LOAD_TO` vocabulary.
- Lateral Earth Pressure `CONSTRAINS` Retaining Walls and Lateral Stability `REQUIRES` Shear Wall remain blocked/deferred due high-risk P1 overlap or existing edge duplication.

## Exact next action

Continue with the remaining 4 unreviewed P1 packets, then consider a second ACS admission batch only for low/medium-risk, Kimi-reviewed candidates whose relation vocabulary and source-context gates pass.


## Commands run so far

- `bun test api/canonicalGraphStewardship.test.ts` passed: 34 tests.
- `bun run api/validateCanonicalGraphStewardship.ts` passed after admission and P1 review updates.
- `bun run api/validateGraphRelationships.ts` passed after admission.
- `bun run api/validateResourceLayer.ts` passed with known standards-context warnings.
- Neighborhood/API visibility smoke passed for three ACS edges plus Deep Foundations and Sendai/Toyo Ito regressions.

## Final validation before commit

Completed: 2026-05-02T08:35:00Z

- `bun test api/canonicalGraphStewardship.test.ts` passed: 34 tests.
- `cd api && bun test` passed: 176 tests.
- `bun run api/validateGraphRelationships.ts` passed: nodes 10,018; base edges 13,670; effective edges 13,677; admitted overlays 7; issue count 0.
- `bun run api/validateCanonicalGraphStewardship.ts` passed: approvals 4; admitted relationships 7; P1 reviewed/unreviewed 16 / 4; latest afterHash mismatches 0; no stale P1 reviews.
- `bun run api/validateResourceLayer.ts` passed: resources/nodeResourceLinks 7 / 9; known ASCE 7 / ACI 318 standards-context warnings only.
- `cd explorer && bun test` passed: 112 tests.
- `cd explorer && bun run build` passed with the known Vite chunk-size warning.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` passed: 118 tests.
- Strict latest-afterHash validation passed with `VITRUVIUS_REQUIRE_LATEST_MANIFEST_AFTERHASH=true`.
- Strict packet-signature smoke produced expected blockers because no `VITRUVIUS_PACKET_HMAC_KEY` is configured; non-strict packet validation passes with 20 unsigned packets.
- Post-change code-intelligence refresh completed: GitNexus up to date, ChunkHound indexed successfully, code-review-graph rebuilt with pre-existing `tree-sitter-yaml` warnings and embedding-provider context-length warnings.
- GitNexus `detect-changes --repo vitruvius` reported CRITICAL risk because the worktree still contains unrelated pre-existing AEC relationship-improvement edits/artifacts; task-scoped code tests and validation passed, and unrelated AEC files were not staged for this task.
