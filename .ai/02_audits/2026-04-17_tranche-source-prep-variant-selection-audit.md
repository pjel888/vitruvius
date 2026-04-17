---
task: tranche-source-prep-variant-selection
created: 2026-04-17
status: complete
---

# Audit — Tranche source-prep variant selection

## Reality check
The current source-prep stage scans every file in a tranche folder. That violates the tranche contract when the manifest explicitly narrows authoritative variants.

## Risk
Excluded or auxiliary files can create avoidable prep failures and degrade tranche truthfulness.

## Safe fix
Constrain source-prep file enumeration to manifest-selected raw files and skip manifest-excluded files entirely.
