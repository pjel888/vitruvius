---
task: tranche-source-admission-variant-selection
created: 2026-04-17
status: complete
---

# Audit — Tranche source-admission variant selection

## Reality check
The tranche pipeline is manifest-backed at the operator surface, but the current source-admission implementation still selected all prepared files in a law folder. That is inconsistent with the tranche safety model.

## Risks
- superseded or legacy variants can be silently admitted even when explicitly excluded
- blocked laws can lose configured anchor intent after writeback
- source-to-graph staging can overstate tranche truth coverage

## Safe scope
- keep the change inside `scripts/vitruvius/laws_readiness.py`
- add regression coverage for authoritative/excluded selection and manifest writeback preservation
- correct the tranche-3 canonical rule mismatch for PD-1151
