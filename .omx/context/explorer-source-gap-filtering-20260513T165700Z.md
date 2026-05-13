# Explorer Source-Gap Filtering Context

## Task

Add local triage filters to the Explorer rail Source gaps browser.

## Desired Outcome

Operators can switch between:

- all source gaps;
- node resource gaps;
- relationship source gaps.

The filter is local UI state only and does not make new API calls or mutate data.

## Constraints

- Read-only UI only.
- No graph mutation.
- No Resource Layer mutation.
- No source-link admission.
- No Neo4j/Postgres writes.
