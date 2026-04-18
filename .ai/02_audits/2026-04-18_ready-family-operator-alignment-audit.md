---
task: ready-family-operator-alignment
created: 2026-04-18
status: complete
---

# Audit — ready-family operator alignment

## Reality check
The recent hardened build reduced duplicate-edge warnings to zero, but the broader one-command ready-family operator rerun brought the duplicate-edge warnings back.

## Safe scope
- change dataset source-to-graph manifest-append logic only
- do not invent new relationships
- prefer already-admitted canonical/shared relationship records over run-local duplicates with the same evidence id
