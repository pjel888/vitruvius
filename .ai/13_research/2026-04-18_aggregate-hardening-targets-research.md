---
task: aggregate-hardening-targets
created: 2026-04-18
status: complete
---

# Research — Aggregate hardening targets

## Goal
Turn the combined ready-family graph reports into a compact prioritized hardening target list, then use the strongest low-risk signal already present in canonical sources to reduce warnings and partial coverage systematically.

## Current state
- build-report summary exists
- source-to-graph report already carries source-quality summaries
- there is no combined operator surface that fuses:
  - duplicate-edge warnings
  - orphan nodes
  - partial folders
  - high-severity / shallow representation paths

## Minimal useful step
Add one reporting command that combines build-report and source-to-graph evidence into prioritized hardening targets.

## Remediation hypothesis chosen
Many current orphan / partial law sources already contain a curated `## Referenced Concepts` section in the canonical source page body.

That signal is:
- already present in admitted canonical truth
- weaker than a reviewed `governs` relationship
- still strong enough to support a conservative source→concept connectivity edge for graph hardening

## Selected approach
- keep existing reviewed relationship files authoritative
- for sources with **zero incident edges**, derive conservative `covers` edges from the `Referenced Concepts` section only
- mark those inferred edges `unverified`
- do **not** widen already-connected sources with extra inferred edges
