# Phase 4 Wave 2 Relation Vocabulary Gate Report

Date: 2026-05-02T14:21:57Z
Baseline admitted relationships: 51
Final admitted relationships: 80
New admitted relationships: 29
Baseline effective edges: 13,721
Final effective edges: 13,750
Base graph edges: 13,670 unchanged
Nodes: 10,018 unchanged
Approvals: 8
Transaction manifests: 63
Latest afterHash mismatches: 0
Aliases/redirects/tombstones: 0/0/0
Resources/nodeResourceLinks: 7/9 unchanged
Decision: canonical-20260502120219-18fe43e2990b
Approval: canonical-approval-20260502120220-4855066acc7a
Admission manifest: canonical-tx-20260502120220-946788a6593c
P1 rebase manifest: canonical-tx-20260502120220-22378408f6e2

## Existing active admitted vocabulary used

- `CONSTRAINS`
- `REQUIRES`
- `TRANSFERS_LOAD_TO`
- `DISCHARGES_TO`
- `COORDINATES_WITH`

## Vocabulary result

- Accepted relation tuples: 29.
- Rejected by duplicate/existing edge check before Kimi: p4w2-003, p4w2-004, p4w2-005, p4w2-013, p4w2-019, p4w2-024, p4w2-028, p4w2-054.
- `CROSS_DOMAIN_EQUIVALENT` not used and remains blocked for active admitted relationships.
- User-listed relation families not currently in `ADMITTED_RELATIONSHIP_TYPES` (`INFORMS`, `AFFECTS`, `SUPPORTS`, `RESISTS`, `DRAINS_TO`, `COLLECTS`, `CONVEYS`, `MITIGATES`, `CONNECTS_TO`) were deferred to future relation-vocabulary design instead of being forced into production.

## Distribution before

`{"CROSS_DOMAIN_ALIGNMENT":4,"CONSTRAINS":5,"TRANSFERS_LOAD_TO":14,"DISCHARGES_TO":4,"COORDINATES_WITH":24}`

## Distribution after

`{"CROSS_DOMAIN_ALIGNMENT":4,"CONSTRAINS":8,"TRANSFERS_LOAD_TO":21,"DISCHARGES_TO":6,"COORDINATES_WITH":40,"REQUIRES":1}`
