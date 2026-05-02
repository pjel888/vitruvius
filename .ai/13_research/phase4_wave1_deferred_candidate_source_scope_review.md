# Phase 4 Wave 1 Deferred Candidate Source-Scope Review

Date: 2026-05-02T11:25:29Z
Baseline active admitted relationships: 26
Final active admitted relationships: 51
New admitted relationships: 25
Baseline effective edges: 13,696
Final effective edges: 13,721
Base graph edges: 13,670 unchanged
Nodes: 10,018 unchanged
Approvals: 7
Transaction manifests: 60
Latest afterHash mismatches: 0
Aliases/redirects/tombstones: 0/0/0
Resources/nodeResourceLinks: 7/9 unchanged
Decision: canonical-20260502112100-b7a51ec7b419
Approval: canonical-approval-20260502112100-5cd241c0a1d3
Admission manifest: canonical-tx-20260502112100-243af2f4fb8d
P1 rebase manifest: canonical-tx-20260502112148-d6defc99a5f5

## Previously deferred examples

- Groundwater -> Excavation Support: remains deferred for source/reference context; no fake source or code basis was supplied.
- Facade Anchor Interface -> Facade Assembly: remains deferred for assembly/source context.
- Shaft Planning <-> Structural Core: remains deferred for directionality/source context.
- Soil Bearing Capacity -> Foundation System: remains a no-op/reject because an existing base relationship already covers the pair.

## Wave 1 Kimi-deferred/rejected candidates

- p4w1-008 deferred: load-transfer relation overclaims the abstraction level for Base Plate Connection -> Footing Foundation; accepted replacement is coordination-only p4w1-037/038.
- p4w1-014, p4w1-015, p4w1-028 deferred: relation type mismatch or too strong without `AFFECTS`/`INFORMS` vocabulary.
- p4w1-020 deferred: planning activity to natural phenomenon coordination is weak.
- p4w1-023, p4w1-024 deferred: drainage direction can be context-specific.
- p4w1-026, p4w1-027, p4w1-036 rejected: abstract endpoint/generic coordination.
- p4w1-029, p4w1-030, p4w1-031 rejected: possible project/regulatory-context implication without source basis.
