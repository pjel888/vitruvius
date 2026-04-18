---
task: readme-refresh
created: 2026-04-18
status: complete
---

# Validation — README refresh

## Goal
Refresh `README.md` so it explains Vitruvius comprehensively in human-readable language first, while preserving the technical/operator view and current MVP automation state.

## Verification
- Reviewed updated table of contents and section headings.
- Confirmed the new sections exist:
  - `What Vitruvius is today`
  - `Current automation & MVP status`
  - `From raw file to graph`
- Confirmed the README now reflects current verified repository truths:
  - one-command laws graph path
  - generic family graph path
  - combined ready-family graph path
  - current MVP status framed in both human-readable and technical terms
  - explicit statement of the remaining operator-path hardening limitation

## Evidence
- `rg -n '^## ' README.md`
- `sed -n '284,470p' README.md`
- `sed -n '1376,1437p' README.md`

## Outcome
The README now better matches the current state of Vitruvius: a working document-to-knowledge-to-graph MVP platform with broader AEC/compliance ambitions still under active development.
