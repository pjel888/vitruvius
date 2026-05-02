# ACS External Apply Context Snapshot

- Task: Implement/fix remaining ACS external blockers as far as safely possible inside the repository.
- Desired outcome: safe repo-side application/preflight paths for steward duplicate decisions, numeric criteria packets, authority ledgers, protected payload admission readiness, and live-promotion readiness without fabricating facts or mutating production.
- Known facts: current file-backed ACS graph is 10,018 nodes / 13,670 relationships / 142 resolver cases; ACS quality 100/100; hardened gated review 20260501T083500Z_ACS_GATED_REVIEW_HARDENED has no writes/admissions.
- Constraints: no raw-layer writes; no KG rebuild/reset; no production Neo4j write without credentials and rollback proof; no protected source payload admission without explicit rights/ledger evidence; no numeric criteria values invented; canonical IDs stable; prior ADs append-only.
- Unknowns: whether production credentials exist in environment; whether real project/AHJ criteria or source-rights authority packets exist locally; whether steward duplicate decisions exist locally.
- Likely touchpoints: scripts/vitruvius/kg/architecture_civil_structural_gate_review.py, its tests, ACS docs/state, System-Manifests reports.
