# Phase 4 Wave 1 Relation Vocabulary Gate Report

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

## Gate result

- Reviewed candidates: 40.
- Vocabulary-valid candidates: 40.
- Relation types used: `TRANSFERS_LOAD_TO`, `COORDINATES_WITH`, `CONSTRAINS`, `DISCHARGES_TO`.
- New relation vocabulary added: none.
- `CROSS_DOMAIN_EQUIVALENT` admitted: no.
- Generic `related_to` admitted: no.
- Duplicate exact base/overlay edge blockers among admitted candidates: none.

## Admitted relation types

- `TRANSFERS_LOAD_TO`: conventional non-numerical load-path mechanism edges.
- `COORDINATES_WITH`: explicit coordination/interface edges; reciprocal pairs where symmetry was intended.
- `DISCHARGES_TO`: non-numerical drainage conveyance direction edges.

## Deferred/rejected vocabulary semantics

- Deferred `CONSTRAINS` candidates where Kimi found relation type too strong or wrong abstraction: p4w1-014, p4w1-015, p4w1-028.
- Rejected abstract/generic `COORDINATES_WITH` candidates: p4w1-026, p4w1-027, p4w1-036.
- Rejected/deferred flood/topography candidates where `CONSTRAINS`/coordination could imply regulatory or project criteria without source context: p4w1-029, p4w1-030, p4w1-031.
