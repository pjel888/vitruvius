# Broad Taxonomy Scaffold Placeholder Audit

Date: 2026-04-29  
Starting commit: 15dae0d0

## Baseline after Architecture-first enrichment

The Architecture branch had zero remaining scaffold L4 labels, but non-Architecture branches still contained placeholder L4 nodes.

Fixture: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`

- Total records: 5191
- Total relationships: 5167
- Remaining non-Architecture L4 scaffold labels: 2496
- Affected non-Architecture L3 parents: 1248
- Affected roots: ACC, CIV, COM, CON, DIG, ELE, FIG, FLS, GEO, HIS, HRC, LAW, MAT, MEC, OPS, PER, PLS, SAN, SEC, SMS, STR, SUS, URB

## Finding

The remaining scaffold labels were not acceptable final taxonomy content. They encoded a placeholder pattern rather than a useful discipline topic, for example `<Subtopic> Concepts` and `<Subtopic> Rule Context`.

## Required correction

Replace every remaining non-Architecture scaffold L4 child with concrete semantic L4 children. Preserve the existing L1/L2/L3 structure and keep the pass metadata-only and file-backed.
