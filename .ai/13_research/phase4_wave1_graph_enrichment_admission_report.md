# Phase 4 Wave 1 Graph Enrichment Admission Report

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

## Outcome

Phase 4 Wave 1 target was reached. Active admitted relationships increased from 26 to 51 through 25 new non-destructive overlay edges.

## Admitted edges

- `VTN-DOM-0012266--transfers_load_to--VTN-DOM-0012263` (TRANSFERS_LOAD_TO): `VTN-DOM-0012266` -> `VTN-DOM-0012263`
- `VTN-DOM-0012265--transfers_load_to--VTN-DOM-0012264` (TRANSFERS_LOAD_TO): `VTN-DOM-0012265` -> `VTN-DOM-0012264`
- `VTN-DOM-0012264--transfers_load_to--VTN-DOM-0012269` (TRANSFERS_LOAD_TO): `VTN-DOM-0012264` -> `VTN-DOM-0012269`
- `VTN-DOM-0012780--transfers_load_to--VTN-DOM-0012781` (TRANSFERS_LOAD_TO): `VTN-DOM-0012780` -> `VTN-DOM-0012781`
- `VTN-DOM-0012781--transfers_load_to--VTN-DOM-0012782` (TRANSFERS_LOAD_TO): `VTN-DOM-0012781` -> `VTN-DOM-0012782`
- `VTN-DOM-0012779--transfers_load_to--VTN-DOM-0012780` (TRANSFERS_LOAD_TO): `VTN-DOM-0012779` -> `VTN-DOM-0012780`
- `VTN-DOM-0012785--transfers_load_to--VTN-DOM-0012782` (TRANSFERS_LOAD_TO): `VTN-DOM-0012785` -> `VTN-DOM-0012782`
- `VTN-DOM-0012788--transfers_load_to--VTN-DOM-0012793` (TRANSFERS_LOAD_TO): `VTN-DOM-0012788` -> `VTN-DOM-0012793`
- `VTN-DOM-0012792--coordinates_with--VTN-DOM-0012791` (COORDINATES_WITH): `VTN-DOM-0012792` -> `VTN-DOM-0012791`
- `VTN-DOM-0012791--coordinates_with--VTN-DOM-0012792` (COORDINATES_WITH): `VTN-DOM-0012791` -> `VTN-DOM-0012792`
- `VTN-DOM-0012793--coordinates_with--VTN-DOM-0012791` (COORDINATES_WITH): `VTN-DOM-0012793` -> `VTN-DOM-0012791`
- `VTN-DOM-0012791--coordinates_with--VTN-DOM-0012793` (COORDINATES_WITH): `VTN-DOM-0012791` -> `VTN-DOM-0012793`
- `VTN-DOM-0012794--coordinates_with--VTN-DOM-0012745` (COORDINATES_WITH): `VTN-DOM-0012794` -> `VTN-DOM-0012745`
- `VTN-DOM-0012745--coordinates_with--VTN-DOM-0012794` (COORDINATES_WITH): `VTN-DOM-0012745` -> `VTN-DOM-0012794`
- `VTN-DOM-0012059--coordinates_with--VTN-DOM-0000232` (COORDINATES_WITH): `VTN-DOM-0012059` -> `VTN-DOM-0000232`
- `VTN-DOM-0000232--coordinates_with--VTN-DOM-0012059` (COORDINATES_WITH): `VTN-DOM-0000232` -> `VTN-DOM-0012059`
- `VTN-DOM-0012739--coordinates_with--VTN-DOM-0012813` (COORDINATES_WITH): `VTN-DOM-0012739` -> `VTN-DOM-0012813`
- `VTN-DOM-0012813--coordinates_with--VTN-DOM-0012739` (COORDINATES_WITH): `VTN-DOM-0012813` -> `VTN-DOM-0012739`
- `VTN-DOM-0012058--coordinates_with--VTN-DOM-0012754` (COORDINATES_WITH): `VTN-DOM-0012058` -> `VTN-DOM-0012754`
- `VTN-DOM-0012754--coordinates_with--VTN-DOM-0012058` (COORDINATES_WITH): `VTN-DOM-0012754` -> `VTN-DOM-0012058`
- `VTN-DOM-0012758--discharges_to--VTN-DOM-0012759` (DISCHARGES_TO): `VTN-DOM-0012758` -> `VTN-DOM-0012759`
- `VTN-DOM-0012759--discharges_to--VTN-DOM-0012760` (DISCHARGES_TO): `VTN-DOM-0012759` -> `VTN-DOM-0012760`
- `VTN-DOM-0012765--discharges_to--VTN-DOM-0012760` (DISCHARGES_TO): `VTN-DOM-0012765` -> `VTN-DOM-0012760`
- `VTN-DOM-0012791--coordinates_with--VTN-DOM-0012782` (COORDINATES_WITH): `VTN-DOM-0012791` -> `VTN-DOM-0012782`
- `VTN-DOM-0012782--coordinates_with--VTN-DOM-0012791` (COORDINATES_WITH): `VTN-DOM-0012782` -> `VTN-DOM-0012791`

## Dry-run and approval

- Dry-run blockers: none.
- Scoped approval: `canonical-approval-20260502112100-5cd241c0a1d3`.
- Approval source: `user_supplied_standing_steward_approval`.
- Mutation scope: non-destructive graph relationship admission.
- Rollback capability: full; rollback by decision id marks overlay/approval records rolled back without rewriting base graph or Resource Layer.

## Graph visibility

All 25 newly admitted edges were verified through `/node/:id/neighborhood?depth=1&direction=both`. Target nodes, edges, and Node Inspector relationship entries were visible. Dynamic filters include `TRANSFERS_LOAD_TO`, `DISCHARGES_TO`, and `COORDINATES_WITH`; `CROSS_DOMAIN_EQUIVALENT` is absent.

## P1 packet custody

Graph/canonical state changed, so all 20 P1 packets were rebased and 20 reviews were carried forward. A transient local rebase using raw node shape produced hash mismatches; it was immediately superseded by validator-shaped rebase manifest `canonical-tx-20260502112148-d6defc99a5f5`, after which canonical validation reported 0 packet content hash mismatches and 0 stale source snapshots.

## Safety confirmations

- Base graph edges unchanged: 13,670.
- No merge, alias, redirect, or tombstone.
- No Resource Layer mutation.
- No fake source context, standard edition, AHJ/jurisdiction, numerical criterion, or protected payload claim.
- P0 Concrete/Reinforced Concrete remains unresolved and unchanged.
