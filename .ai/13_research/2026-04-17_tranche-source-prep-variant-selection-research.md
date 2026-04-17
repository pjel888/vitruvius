---
task: tranche-source-prep-variant-selection
created: 2026-04-17
status: complete
---

# Research — Tranche source-prep variant selection

## Problem
Tranche-7 source prep attempted to process the explicitly excluded `Board of Master Plumber.doc` file in `RA-1378`, causing a conversion failure even though the manifest already marked it out of authoritative scope.

## Need
Source prep should honor manifest-declared authoritative/raw-anchor intent and excluded variants, the same way source admission now does.

## Scope
- filter tranche source-prep file enumeration using manifest `authoritative_variant_paths`, `raw_anchor_paths`, and `excluded_variant_paths`
- keep excluded files visible in the manifest rather than attempting conversion
