# Explorer Source-Gap Navigation Context

## Task

Make graph-wide source-gap workqueue rows actionable in Explorer by letting operators jump from a workqueue item to the affected node.

## Desired Outcome

In the AEC-MEPFS rail Source gaps section:

- node-resource gaps expose an `Open node` action;
- relationship-source gaps expose `From` and `To` node actions when both endpoints are available;
- clicking an action selects/navigates to the node in Explorer.

## Constraints

- Read-only UI action only.
- No graph mutation.
- No Resource Layer mutation.
- No database writes.
- No source-link admission.
