# Continuous Vitruvius Quality Report

Date: 2026-05-02T10:24:13Z

## Summary

- Baseline admitted relationships: 14.
- Final admitted relationships: 26.
- New Phase 3 MVP admitted overlays: 12.
- Base graph edges: 13,670.
- Effective graph edges after overlays: 13,696.
- Approvals: 6.
- P1 packets reviewed/unreviewed: 20 / 0.
- P1 packet snapshots rebased: 20.
- Aliases / redirects / tombstones: 0 / 0 / 0.
- Resource Layer mutation: none.
- Merge: none.
- Fake source/standard/AHJ/numerical/protected-payload claim: none.

Quality gates applied: existing-node endpoint check, active relation vocabulary, duplicate base/overlay edge check, Kimi review or timeout-safe admission rule, dry-run, scoped approval, transaction manifests, rollback plan, P1 custody rebase, graph visibility verification, and targeted canonical/graph/resource validation.

Deferred candidates were not admitted when Kimi requested source context or duplicate checks failed.


## Broad validation before checkpoint

- API tests: passed (179 tests).
- Explorer tests: passed (112 tests).
- Explorer build: passed with existing chunk-size warning.
- Python KG AEC relationship tests: passed (118 tests).
- Strict latest-afterHash validation: passed.
- Strict packet-signature smoke: expected missing-HMAC-key blockers only; non-strict canonical validation rerun and passed.
