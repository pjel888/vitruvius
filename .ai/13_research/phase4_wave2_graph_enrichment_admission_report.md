# Phase 4 Wave 2 Graph Enrichment Admission Report

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

## Target result

- Target admitted relationships: at least 75.
- Achieved admitted relationships: 80.
- Target reached: yes.

## Admitted edges

- `VTN-DOM-0012792--coordinates_with--VTN-DOM-0012782`
- `VTN-DOM-0012782--coordinates_with--VTN-DOM-0012792`
- `VTN-DOM-0012273--transfers_load_to--VTN-DOM-0000038`
- `VTN-DOM-0012282--transfers_load_to--VTN-DOM-0012273`
- `VTN-DOM-0012283--transfers_load_to--VTN-DOM-0012273`
- `VTN-DOM-0012297--transfers_load_to--VTN-DOM-0012273`
- `VTN-DOM-0012296--transfers_load_to--VTN-DOM-0012273`
- `VTN-DOM-0012293--constrains--VTN-DOM-0012782`
- `VTN-DOM-0000290--constrains--VTN-DOM-0000232`
- `VTN-DOM-0012758--discharges_to--VTN-DOM-0012760`
- `VTN-DOM-0012764--discharges_to--VTN-DOM-0012760`
- `VTN-DOM-0012059--coordinates_with--VTN-DOM-0012742`
- `VTN-DOM-0012059--coordinates_with--VTN-DOM-0012219`
- `VTN-DOM-0012752--coordinates_with--VTN-DOM-0000232`
- `VTN-DOM-0012741--coordinates_with--VTN-DOM-0012780`
- `VTN-DOM-0012261--coordinates_with--VTN-DOM-0012781`
- `VTN-DOM-0004714--coordinates_with--VTN-DOM-0012165`
- `VTN-DOM-0012739--coordinates_with--VTN-DOM-0000151`
- `VTN-DOM-0012780--coordinates_with--VTN-DOM-0012741`
- `VTN-DOM-0012781--coordinates_with--VTN-DOM-0012261`
- `VTN-DOM-0012165--coordinates_with--VTN-DOM-0004714`
- `VTN-DOM-0012742--coordinates_with--VTN-DOM-0012059`
- `VTN-DOM-0012219--coordinates_with--VTN-DOM-0012059`
- `VTN-DOM-0000232--coordinates_with--VTN-DOM-0012752`
- `VTN-DOM-0000151--coordinates_with--VTN-DOM-0012739`
- `VTN-DOM-0012782--transfers_load_to--VTN-DOM-0000038`
- `VTN-DOM-0012279--transfers_load_to--VTN-DOM-0000038`
- `VTN-DOM-0012773--constrains--VTN-DOM-0012273`
- `VTN-DOM-0012801--requires--VTN-DOM-0012800`

## Relation type distribution

Before: `{"CROSS_DOMAIN_ALIGNMENT":4,"CONSTRAINS":5,"TRANSFERS_LOAD_TO":14,"DISCHARGES_TO":4,"COORDINATES_WITH":24}`

After: `{"CROSS_DOMAIN_ALIGNMENT":4,"CONSTRAINS":8,"TRANSFERS_LOAD_TO":21,"DISCHARGES_TO":6,"COORDINATES_WITH":40,"REQUIRES":1}`

## Visibility validation

- Checked newly admitted edges: 29.
- Failures: 0.
- Dynamic filters: `COORDINATES_WITH`, `TRANSFERS_LOAD_TO`, `CONSTRAINS`, `DISCHARGES_TO`, and `REQUIRES` present; `CROSS_DOMAIN_EQUIVALENT` absent.

## Rollback and transaction status

- Rollback capability: full canonical rollback for decision `canonical-20260502120219-18fe43e2990b`.
- Admission manifest: `canonical-tx-20260502120220-946788a6593c`.
- P1 rebase manifest: `canonical-tx-20260502120220-22378408f6e2`.
- Latest afterHash mismatches: 0.

## Safety confirmations

No merge, alias, redirect, tombstone, Resource Layer mutation, fake source context, protected payload claim, AHJ/code/jurisdiction claim, or numerical design criterion was introduced.
