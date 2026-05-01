# Context Snapshot — duplicate-canonical-source-id-fix

- created_utc: 20260415T233924Z
- task_statement: Resolve the underlying duplicate canonical source ID blocking graph integrity for the IRR source pages.
- desired_outcome: `build-graph` becomes green for duplicate-node integrity by removing or migrating the duplicate canonical source identity in a traceable way, with docs/state/logs updated honestly.

## Known Facts / Evidence
- PASS 2 fixed detection only; `build-graph` now fails on duplicate node id `irr-implementing-rules-and-regulations-of-the-national-building-code`.
- The duplicate currently comes from two files:
  - `003_Canonical-Knowledge-Layer/shared/sources/pd-1096-irr.md`
  - `003_Canonical-Knowledge-Layer/shared/sources/implementing-rules-and-regulations-of-the-national-building-code.md`
- PASS 2 explicitly deferred mutation because it required a migration/curation decision.
- User now explicitly requested the additional fix pass for the underlying duplicate canonical source id.

## Constraints
- Follow AGENTS/SEL: no blind ID mutation without a documented migration/decision.
- Keep the fix narrow; do not broaden into unrelated graph/query or feature work.
- Preserve truthfulness and auditability.
- Must validate via `build-graph`, targeted tests, and any impacted docs/state.

## Unknowns / Open Questions
- Which of the two duplicate source pages is authoritative vs expendable?
- Whether any relationship/concept/docs references require migration after deduplication.
- Whether the safest fix is delete/archive one draft page, re-id it, or otherwise mark it out of graph scope.

## Likely Touchpoints
- `003_Canonical-Knowledge-Layer/shared/sources/*.md`
- `scripts/vitruvius/graph/*` only if validation demands it (not expected for primary fix)
- `scripts/tests/test_graph_*` if fixtures or assertions need update
- `.ai/10_state/decisions.md`, `.ai/05_logs/*`, maybe the PASS 2 validation log and current-phase/active_context if reality changes
