# Resource Layer Implementation Audit

Status: completed for implementation loop 1
Date: 2026-05-01

## Starting implementation reality
- No existing Resource Registry or NodeResourceLink runtime was found before this loop.
- Existing source-rights/source-family metadata was not a node-specific resource registry.
- Existing Explorer Sources tab rendered legacy evidence spans, not ranked reference resources.
- AEC-MEPFS selected node detail was file-backed and returned `evidence: []`.

## Gaps addressed
- [G001] Durable Resource model/registry: implemented.
- [G002] Durable NodeResourceLink model/registry: implemented.
- [G003] Source-family authority registry: implemented with 25 starter families.
- [G004] Ranking, verification support, deduplication, validation: implemented.
- [G005] Local corpus metadata/hash scanner: implemented and exercised.
- [G006] Candidate-only online adapter interface: implemented with Open Library adapter and mocked test.
- [G007] Sidebar resource display: implemented in `NodeInspector`.
- [G008] Metrics/reporting: implemented through `/resources/metrics` and final report.

## Risk outcomes
- [R001] Protected payload/path leakage: mitigated by keeping render graph unchanged and exposing only allowlisted resource summaries.
- [R002] Source overclaiming: mitigated by accepting only Kimi-approved seed links; ASCE/FHWA remain `needs_review`, ACI column link is `rejected`.
- [R003] Broken links: mitigated by URL health checks and validation rejecting accepted external resources without `lastCheckedAt`.
- [R004] Graph pollution: mitigated by separate resource registry; no resource graph nodes were created.
- [R005] Dirty working tree: scoped changes were made without reverting unrelated pre-existing modifications.
- [R006] Custody/provenance gap from final Kimi review: mitigated by adding `sourceRights` and `admissionProvenance` to Resource records.

## Tooling notes
- Morph codebase search returned HTTP 429.
- `omx explore` and `omx sparkshell` were unavailable in this Windows shell.
- ChunkHound deep research lacked LLM configuration, but regex/index refresh ran.
- Initial code-intelligence refresh completed; code-review-graph refresh warned about missing `tree-sitter-yaml` and an embedding batch `_Task.elapsed` issue.
