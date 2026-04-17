---
task: hlurb-dhsud-agency-split-correction
created: 2026-04-18
status: complete
---

# Audit — HLURB and DHSUD agency split correction

## Reality check
The combined raw folder is an operator storage shortcut, not a truthful agency model. The currently admitted tranche-12 guidance files are clearly DHSUD-branded 2025 publications, while the same raw folder also contains older HLURB materials.

## Safe scope
- do not rename or move the raw folder yet
- introduce a logical/raw-folder split in tranche metadata and source-prep handling
- update tranche-12 and tracking docs so they say `DHSUD` for the staged guidance surfaces and explicitly note the combined raw-folder reality
