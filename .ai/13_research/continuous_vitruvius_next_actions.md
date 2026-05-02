# Continuous Vitruvius Next Actions

Last updated: 2026-05-02T09:31:05+0800

## Immediate next action

Implement optional HMAC/signature support for P1 decision packet source snapshots and packet content hashes when a local environment key is configured. Keep local development unblocked when no key exists, but surface unsigned packet warnings in validation when signing is configured.

## Ordered queue

1. **P1 packet signature hardening**
   - Add optional HMAC over `sourceSnapshot.snapshotHash` and `packetContentHash`.
   - Validate missing/invalid signatures only when signing key is configured.
   - Update tests and canonical validation.

2. **P1 packet UI/export detail**
   - Show source snapshot hash, packet content hash, stale/tamper validation state, and advisory truth caveat in `/dev/canonical-review`.
   - Add export/open packet affordance if safe within current UI architecture.

3. **Top-P1 Kimi/domain review summaries**
   - Review top 5-10 P1 packets.
   - Record critique as advisory only.
   - Do not apply decisions or aliases.

4. **P0 approval readiness**
   - Keep Concrete/Reinforced Concrete packets current.
   - Do not approve/admit without real steward approval metadata.

5. **Dirty worktree reduction plan**
   - Group current dirty changes by subsystem.
   - Avoid overwriting unrelated human/prior-loop changes.
