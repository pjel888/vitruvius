# Continuous Vitruvius Decision Log

Last updated: 2026-05-02T09:31:05+0800

## Decision - P1 packet evidence-locking before additional duplicate triage

Because P0 Concrete/Reinforced Concrete admission is blocked by missing real steward approval, the safest high-value improvement was to make existing P1 review packets more trustworthy and auditable without changing graph truth. P1 packets now include source snapshots and hashes, and validation can detect tampering/staleness.

## Decision - Hashes are audit aids, not truth claims

Packet `sourceSnapshot.snapshotHash`, `groupInputHash`, `candidateEdgeNeighborhoodHash`, and `packetContentHash` are integrity signals only. They must not be interpreted as steward approval, source verification, ontology correctness, or merge safety.

## Decision - Continue no-production-mutation policy

No production duplicate merges, aliases, redirects, tombstones, admitted relationships, resource rewrites, or fake resources were created in this iteration.
