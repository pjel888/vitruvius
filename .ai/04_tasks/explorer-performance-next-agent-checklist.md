# Explorer Performance Next-Agent Checklist

Primary handoff plan: `.ai/03_plans/explorer-performance-next-agent-handoff.md`

- [ ] Inspect current dirty worktree and separate Explorer performance files from prior KG files.
- [ ] Re-run focused graph-engine tests.
- [ ] Run real browser performance trace for `/explore`.
- [ ] Save browser profile summary under `.ai/02_audits/` and `006_System-Manifests/aec-mepfs-backbone/explorer-performance/<run-id>/`.
- [ ] If proven by trace, optimize `VisNetworkHost` selection/DataSet update deltas without changing UX.
- [ ] Re-run Explorer/API/build/safety validation.
- [ ] Run Kimi final read-only audit.
