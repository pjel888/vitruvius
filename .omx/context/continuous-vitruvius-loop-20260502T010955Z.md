# Continuous Vitruvius Loop Context

- Task: continuously improve Vitruvius as a KG-first AEC knowledge system with canonical stewardship, visible relationships, and safe Resource Layer behavior.
- Desired outcome: verify current state, select highest-value unblocked improvement, implement safely, validate, record progress, and checkpoint next action.
- Known metrics to verify: 10,018 nodes, 13,670 edges, 544 duplicate groups, 2 unresolved P0 groups, approvals 0, admitted relationships 0, resources 7, nodeResourceLinks 9, P1 packets 20.
- Constraints: no fake approvals/resources/provenance; no reckless merges; preserve graph and Resource Layer; admin-gated mutation; no production edge admission without approval.
- Current candidate improvement: enrich P1 decision packets with source snapshot hashes/evidence-locking and validation, because P0 is blocked by missing real approval and Kimi previously deferred source graph/resource snapshot hashes.
- Likely touchpoints: api/graph/canonicalStewardship.ts, api/canonicalGraphStewardship.test.ts, 006_System-Manifests/graph-canonical/p1-decision-packets.json, continuous .ai reports.
- Tooling caveats: morph codebase_search returned 429; code-review-graph YAML parser warnings; GitNexus broad dirty worktree critical risk.
