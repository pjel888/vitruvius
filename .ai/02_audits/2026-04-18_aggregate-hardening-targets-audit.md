---
task: aggregate-hardening-targets
created: 2026-04-18
status: complete
---

# Audit — Aggregate hardening targets

## Reality check
We can see the warning counts now, but the next execution step still requires humans to manually synthesize which families or folders are the best remediation targets.

## Safe scope
- reporting only
- no graph mutation
- no automatic remediation
- derive priorities from existing report truth only

## Follow-on adjustment
After the reporting command exposed the dominant warning clusters, the next safe widening step is still conservative:

- no new human-authored law interpretations
- no automatic `governs` claims
- only reuse already-admitted `Referenced Concepts` lists from canonical source pages
- emit weaker `covers` edges for currently orphan sources only

This keeps the remediation inside existing admitted source truth while materially improving connectivity.
