---
task: tranche-source-admission-variant-selection
created: 2026-04-17
status: complete
---

# Research — Tranche source-admission variant selection

## Problem
Fresh tranche-3 execution surfaced two correctness gaps:
1. source admission ignored manifest-level `authoritative_variant_paths` / `excluded_variant_paths`
2. source-admission manifest writeback erased configured raw-anchor intent for blocked laws

## Evidence
- `config/datasets/laws-tranche-3.yaml` initially excluded the legacy PD-1067 IRR variant, but source admission still admitted it.
- `PD-1151` stayed blocked because the filename says `PD 1152 Environmental Code` while the document text is PD 1151 / Philippine Environmental Policy.
- after admission writeback, blocked `PD-1151` lost its configured raw-anchor paths.

## Required correction
- manifest variant intent must influence prepared-candidate selection
- manifest writeback must preserve configured authoritative/raw anchors when no pages were admitted
- PD-1151 canonical rule must match the real document despite the misleading filename
