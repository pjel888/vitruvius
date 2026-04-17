---
task: bootstrap-artifact-promotion
created: 2026-04-18
status: complete
---

# Research — Bootstrap artifact promotion

## Goal
Reduce long-term dependence on generated bootstrap overlays by adding an explicit promotion path from generated canonical-rule overlays into the durable audited rules file.

## Current state
- starter non-laws lanes can scaffold generated rule entries into:
  - `config/datasets/canonical_rules.generated.yaml`
- `canonicalize.load_rules()` already merges the generated overlay with the base rules file
- there is currently no explicit promotion workflow to move reviewed generated rules into:
  - `scripts/vitruvius/rules/canonical_rules.yaml`

## Minimal useful next step
Add a command that:
1. selects generated rules by name
2. appends them to the durable base rules file if not already present
3. removes them from the generated overlay
4. reports exactly what was promoted / skipped

This keeps bootstrap generation and durable promotion as separate, auditable steps.
